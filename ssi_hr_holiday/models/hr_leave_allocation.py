# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import UserError
from odoo.tools import pytz

from odoo.addons.ssi_decorator import ssi_decorator


class HrLeaveAllocation(models.Model):
    """
    Represents an allocation of leave days granted to an employee.
    Tracks how many days were granted, used, planned, and still
    available, and automatically terminates allocations past their
    extended expiry date via a scheduled action.
    """

    _name = "hr.leave_allocation"
    _inherit = [
        "mixin.transaction_confirm",
        "mixin.transaction_open",
        "mixin.transaction_done",
        "mixin.transaction_cancel",
        "mixin.transaction_terminate",
        "mixin.date_duration",
        "mixin.employee_document",
    ]
    _description = "Leave Allocation"
    _order = "date_start,id"

    _approval_from_state = "draft"
    _approval_to_state = "open"
    _approval_state = "confirm"
    _after_approved_method = "action_open"
    _create_sequence_state = "open"

    # Attributes related to add element on view automatically
    _automatically_insert_view_element = True

    # Attributes related to add element on duration_view automatically
    _date_start_readonly = True
    _date_end_readonly = True
    _date_end_required = True
    _date_start_states_list = ["draft"]
    _date_start_states_readonly = ["draft"]
    _date_end_states_list = ["draft"]
    _date_end_states_readonly = ["draft"]

    # Attributes related to add element on form view automatically
    _automatically_insert_multiple_approval_page = True
    _automatically_insert_done_policy_fields = False
    _automatically_insert_done_button = False

    _statusbar_visible_label = "draft,confirm,open,done,terminate"

    _policy_field_order = [
        "confirm_ok",
        "open_ok",
        "approve_ok",
        "done_ok",
        "reject_ok",
        "restart_approval_ok",
        "cancel_ok",
        "restart_ok",
        "terminate_ok",
        "manual_number_ok",
    ]

    _header_button_order = [
        "action_confirm",
        "action_approve_approval",
        "action_reject_approval",
        "action_open",
        "action_done",
        "%(ssi_transaction_cancel_mixin.base_select_cancel_reason_action)d",
        "action_restart",
        "action_terminate",
    ]

    # Attributes related to add element on search view automatically
    _state_filter_order = [
        "dom_draft",
        "dom_confirm",
        "dom_reject",
        "dom_open",
        "dom_done",
        "dom_cancel",
        "dom_terminate",
    ]

    @api.depends(
        "leave_ids",
        "leave_ids.number_of_days",
        "leave_ids.state",
        "leave_ids.type_id",
        "number_of_days",
    )
    def _compute_num_of_days(self):
        """Compute used, planned and available days on this allocation.

        Sums ``number_of_days`` of ``leave_ids`` grouped by state
        (``done`` counts as used, ``confirm`` counts as planned), and
        derives available days as ``number_of_days`` minus both.
        """
        for leave in self:
            num_of_days_used = num_of_days_planned = 0.0
            for record in leave.leave_ids:
                if record.state == "done":
                    num_of_days_used += record.number_of_days
                if record.state == "confirm":
                    num_of_days_planned += record.number_of_days
            num_of_days_available = (
                leave.number_of_days - num_of_days_used - num_of_days_planned
            )
            leave.num_of_days_used = num_of_days_used
            leave.num_of_days_planned = num_of_days_planned
            leave.num_of_days_available = num_of_days_available

    type_id = fields.Many2one(
        string="Leave Type",
        comodel_name="hr.leave_type",
        required=True,
        ondelete="restrict",
        readonly=True,
        states={
            "draft": [("readonly", False)],
        },
    )
    number_of_days = fields.Integer(
        string="Number of Days",
        required=True,
        readonly=True,
        states={
            "draft": [("readonly", False)],
        },
    )
    leave_ids = fields.One2many(
        string="Leaves",
        comodel_name="hr.leave",
        inverse_name="leave_allocation_id",
        readonly=True,
    )
    num_of_days_used = fields.Integer(
        string="Used Days",
        compute="_compute_num_of_days",
        store=True,
        compute_sudo=True,
    )
    num_of_days_planned = fields.Integer(
        string="Plannned Days",
        compute="_compute_num_of_days",
        store=True,
        compute_sudo=True,
    )
    num_of_days_available = fields.Integer(
        string="Available Days",
        compute="_compute_num_of_days",
        store=True,
        compute_sudo=True,
    )
    state = fields.Selection(
        string="State",
        selection=[
            ("draft", "Draft"),
            ("confirm", "Waiting for Approval"),
            ("open", "In Progress"),
            ("done", "Done"),
            ("cancel", "Cancelled"),
            ("reject", "Rejected"),
            ("terminate", "Terminated"),
        ],
        default="draft",
        copy=False,
    )
    can_be_extended = fields.Boolean(
        string="Can be Extended",
        default=False,
        readonly=True,
        states={
            "draft": [("readonly", False)],
        },
    )
    date_extended = fields.Date(
        string="Date Extended",
        required=True,
        default=False,
        readonly=True,
        states={
            "draft": [("readonly", False)],
        },
    )

    @api.depends("policy_template_id")
    def _compute_policy(self):
        """Recompute approval policy on ``policy_template_id`` change.

        Overridden only to add ``policy_template_id`` as an explicit
        dependency on top of the mixin's own compute; delegates the
        whole computation to ``super()``.
        """
        _super = super(HrLeaveAllocation, self)
        _super._compute_policy()

    @api.model
    def _get_policy_field(self):
        res = super(HrLeaveAllocation, self)._get_policy_field()
        policy_field = [
            "confirm_ok",
            "approve_ok",
            "open_ok",
            "done_ok",
            "cancel_ok",
            "reject_ok",
            "restart_ok",
            "restart_approval_ok",
            "terminate_ok",
            "manual_number_ok",
        ]
        res += policy_field
        return res

    @api.onchange(
        "employee_id",
    )
    def onchange_policy_template_id(self):
        """Set the policy template when ``employee_id`` changes.

        Resolves the template through ``_get_template_policy`` so the
        approval policy fields follow the selected employee.
        """
        template_id = self._get_template_policy()
        self.policy_template_id = template_id

    @api.constrains("state")
    def _constrains_leave(self):
        """Forbid cancelling an allocation that still has active leaves.

        Delegates to ``_check_leave`` and raises ``UserError`` when
        the allocation is being cancelled while it still has leaves
        that are not ``cancel``/``reject``.
        """
        for record in self.sudo():
            if record.state == "cancel" and not record._check_leave():
                error_message = _(
                    """
                Context: Cancel leave allocation
                Database ID: %s
                Problem: Leave already exist for this allocation
                Solution: Cancel leave request
                """
                    % (record.id)
                )
                raise UserError(error_message)

    @api.constrains(
        "date_start",
        "date_end",
        "employee_id",
    )
    def _constrains_overlap(self):
        """Forbid allocations whose dates overlap another allocation.

        Delegates the check to ``_check_overlap`` and raises
        ``UserError`` when an overlapping, non-cancelled/rejected
        allocation already exists for the same employee.
        """
        for record in self.sudo():
            if not record._check_overlap():
                error_message = _(
                    """
                Context: Change date start or date end on leave request
                Database ID: %s
                Problem: There are other leave(s) allocation that overlap
                Solution: Change date start and date end
                """
                    % (record.id)
                )
                raise UserError(error_message)

    def _check_leave(self):
        """Check that no active leave still references this allocation.

        :return: ``False`` when ``leave_ids`` has a leave whose state
            is not ``cancel``/``reject``, ``True`` otherwise
        """
        result = True
        if self.leave_ids.filtered(
            lambda leave: leave.state not in ("cancel", "reject")
        ):
            result = False
        return result

    def _check_overlap(self):
        """Check whether this allocation overlaps another allocation.

        :return: ``False`` when another non-cancelled/rejected
            allocation of the same employee overlaps this record's
            date range, ``True`` otherwise
        """
        self.ensure_one()
        result = True
        criteria = [
            ("employee_id", "=", self.employee_id.id),
            ("state", "not in", ["cancel", "reject"]),
            ("id", "!=", self.id),
            ("date_start", "<=", self.date_end),
            ("date_end", ">=", self.date_start),
        ]
        overlap = self.search_count(criteria)
        if overlap > 0:
            result = False

        return result

    @api.onchange(
        "date_end",
        "can_be_extended",
        "date_extended",
    )
    def onchange_date_extended(self):
        """Keep ``date_extended`` consistent with ``date_end``.

        Resets ``date_extended`` to ``date_end`` when it is empty or
        ``can_be_extended`` is off, and warns (clamping the value)
        when a manually set ``date_extended`` is earlier than
        ``date_end``.
        """
        if not self.date_extended or not self.can_be_extended:
            self.date_extended = self.date_end
        if self.date_end and self.date_extended < self.date_end:
            self.date_extended = self.date_end
            return {
                "warning": {
                    "title": "Wrong value",
                    "message": "Date extended can not be less than date end.",
                }
            }

    def _cron_terminate(self, terminate_reason_code=False):
        """Terminate allocations whose extended date has passed.

        Scheduled action entry point: searches ``open`` allocations
        whose ``date_extended`` is before today (in the admin user's,
        or current user's, timezone) and terminates them using the
        terminate reason matching ``terminate_reason_code``.

        :param terminate_reason_code: ``code`` of the
            ``base.terminate_reason`` applied to matched allocations
        """
        try:
            user_id = self.env.ref("base.user_admin")
        except Exception:
            user_id = self.env.user
        tz = pytz.timezone(user_id.tz or "Asia/Jakarta")
        current_datetime = pytz.utc.localize(fields.Datetime.now()).astimezone(tz)
        allocation_ids = self.search(
            [
                ("date_extended", "<", current_datetime.date()),
                ("state", "=", "open"),
            ]
        )
        terminate_reason__id = self.env["base.terminate_reason"].search(
            [
                ("code", "=", terminate_reason_code),
            ],
            limit=1,
        )
        allocation_ids.action_terminate(terminate_reason=terminate_reason__id)

    @ssi_decorator.insert_on_form_view()
    def _insert_form_element(self, view_arch):
        if self._automatically_insert_view_element:
            view_arch = self._reconfigure_statusbar_visible(view_arch)
        return view_arch
