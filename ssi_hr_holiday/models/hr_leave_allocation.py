# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class HrLeaveAllocation(models.Model):
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
        "leave_ids.number_of_days",
        "leave_ids.state",
        "leave_ids.type_id",
        "number_of_days",
    )
    def _compute_num_of_days(self):
        for leave in self:
            num_of_days_used = num_of_days_planned = num_of_days_available = 0.0
            for record in self.leave_ids:
                if record.state == "done":
                    num_of_days_used += record.number_of_days
                if record.state in ["draft", "confirm"]:
                    num_of_days_planned += record.number_of_days
            num_of_days_available = (
                leave.number_of_days - num_of_days_used - num_of_days_planned
            )
            leave.num_of_days_used = num_of_days_used
            leave.num_of_days_planned = num_of_days_planned
            leave.num_of_days_available = num_of_days_available

    date_start = fields.DateCallable(
        states={
            "draft": [("readonly", False)],
            "confirm": [("readonly", False)],
        },
    )
    date_end = fields.DateCallable(
        string="Valid Until",
        required=False,
        readonly=True,
        states={
            "draft": [("readonly", False)],
            "confirm": [("readonly", False)],
        },
    )
    type_id = fields.Many2one(
        string="Leave Type",
        comodel_name="hr.leave_type",
        required=True,
        ondelete="restrict",
        readonly=True,
        states={
            "draft": [("readonly", False)],
            "confirm": [("readonly", False)],
        },
    )
    number_of_days = fields.Integer(
        string="Number of Days",
        required=True,
        readonly=True,
        states={
            "draft": [("readonly", False)],
            "confirm": [("readonly", False)],
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

    @api.depends("policy_template_id")
    def _compute_policy(self):
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
        template_id = self._get_template_policy()
        self.policy_template_id = template_id

    # Check STATE
    @api.constrains("state")
    def _check_state(self):
        for record in self.sudo():
            if record.state in ["cancel", "reject"]:
                if record.leave_ids:
                    raise UserError(
                        _(
                            "Leave Allocation have Leave Request \n"
                            + "Data Allocation cannot be cancelled or rejected"
                        )
                    )
