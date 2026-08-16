# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models

from odoo.addons.ssi_decorator import ssi_decorator


class HrLeaveRequestBatch(models.Model):
    """
    Groups a single time off request into one approvable document so
    that an identical leave period can be granted to many employees at
    once.

    Confirming the batch materialises one ``hr.leave`` record per
    selected employee, and every later transition of the batch
    (approve, reject, restart, cancel) is relayed to those child time
    off requests so the batch and its children never drift apart.
    """

    _name = "hr.leave_request_batch"
    _description = "Leave Request Batch"
    _inherit = [
        "mixin.transaction_confirm",
        "mixin.transaction_done",
        "mixin.transaction_cancel",
        "mixin.date_duration",
    ]

    # Multiple Approval Attribute
    _approval_from_state = "draft"
    _approval_to_state = "done"
    _approval_state = "confirm"
    _after_approved_method = "action_done"

    # Attributes related to add element on view automatically
    _automatically_insert_view_element = True
    _automatically_insert_done_button = False
    _automatically_insert_done_policy_fields = False

    # Attributes related to add element on form view automatically
    _automatically_insert_multiple_approval_page = True
    _statusbar_visible_label = "draft,confirm,done"
    _policy_field_order = [
        "confirm_ok",
        "approve_ok",
        "reject_ok",
        "restart_approval_ok",
        "cancel_ok",
        "restart_ok",
        "manual_number_ok",
    ]
    _header_button_order = [
        "action_confirm",
        "action_approve_approval",
        "action_reject_approval",
        "%(ssi_transaction_cancel_mixin.base_select_cancel_reason_action)d",
        "action_restart",
    ]

    # Attributes related to add element on search view automatically
    _state_filter_order = [
        "dom_draft",
        "dom_confirm",
        "dom_reject",
        "dom_done",
        "dom_cancel",
    ]

    # Mixin duration attribute
    _date_start_readonly = True
    _date_end_readonly = True
    _date_start_states_list = ["draft"]
    _date_start_states_readonly = ["draft"]
    _date_end_states_list = ["draft"]
    _date_end_states_readonly = ["draft"]

    # Sequence attribute
    _auto_fill_sequence = True
    _create_sequence_state = "done"

    @api.model
    def _get_policy_field(self):
        res = super(HrLeaveRequestBatch, self)._get_policy_field()
        policy_field = [
            "confirm_ok",
            "approve_ok",
            "done_ok",
            "cancel_ok",
            "reject_ok",
            "restart_ok",
            "restart_approval_ok",
            "manual_number_ok",
        ]
        res += policy_field
        return res

    @ssi_decorator.insert_on_form_view()
    def _insert_form_element(self, view_arch):
        if self._automatically_insert_view_element:
            view_arch = self._reconfigure_statusbar_visible(view_arch)
        return view_arch

    state = fields.Selection(
        string="State",
        selection=[
            ("draft", "Draft"),
            ("confirm", "Waiting for Approval"),
            ("done", "Done"),
            ("cancel", "Cancelled"),
            ("reject", "Rejected"),
        ],
        default="draft",
        copy=False,
        required=True,
    )

    type_id = fields.Many2one(
        string="Type",
        comodel_name="hr.leave_type",
        required=True,
        ondelete="restrict",
        readonly=True,
        states={
            "draft": [("readonly", False)],
        },
    )

    employee_ids = fields.Many2many(
        string="Employee(s)",
        comodel_name="hr.employee",
        relation="rel_leave_request_batch_2_employee",
        column1="leave_request_batch_id",
        column2="employee_id",
        readonly=True,
        states={
            "draft": [("readonly", False)],
        },
    )

    leave_request_ids = fields.One2many(
        string="Time Off",
        comodel_name="hr.leave",
        inverse_name="batch_id",
        readonly=True,
    )

    def _create_leave_request(self, employee_ids):
        """Materialise one ``hr.leave`` per employee of this batch.

        Employees that already own a child time off request on this
        batch are skipped, so the method stays safe to call again after
        a restart. Each new request copies ``date_start``, ``date_end``
        and ``type_id`` from the batch, then gets its dependent fields
        filled by ``_trigger_onchange``.

        :param employee_ids: ``hr.employee`` recordset to grant leave to
        """
        self.ensure_one()
        obj_leave_request = self.env["hr.leave"]
        for employee_id in employee_ids:
            leave_request_ids = self.leave_request_ids.filtered(
                lambda x: x.employee_id.id == employee_id.id
            )
            if not leave_request_ids:
                leave_id = obj_leave_request.create(
                    {
                        "date_start": self.date_start,
                        "date_end": self.date_end,
                        "batch_id": self.id,
                        "employee_id": employee_id.id,
                        "type_id": self.type_id.id,
                    }
                )
                self._trigger_onchange(leave_id)

    def _trigger_onchange(self, leave):
        """Fill the derived fields of a batch-created time off request.

        ``hr.leave`` computes its number of days and its department,
        manager and job from onchange handlers, which never run when the
        record is created programmatically. Calling them here keeps a
        batch-created request identical to one typed in by a user.

        :param leave: a single ``hr.leave`` record created by this batch
        """
        self.ensure_one()
        leave.onchange_number_of_day()
        leave.onchange_department_id()
        leave.onchange_manager_id()
        leave.onchange_job_id()

    def _confirm_leave_request(self, leave_request_ids):
        """Send every child time off request into its approval flow.

        :param leave_request_ids: ``hr.leave`` recordset of this batch
        """
        self.ensure_one()
        for leave_request in leave_request_ids:
            leave_request.action_confirm()

    # BUTTON CONFIRM
    def action_confirm(self):
        """Submit the batch and its time off requests for approval.

        On top of the mixin transition, this creates the missing child
        ``hr.leave`` records for every selected employee and confirms
        all of them, so the approver reviews the batch and its children
        in one pass.
        """
        _super = super(HrLeaveRequestBatch, self)
        _super.action_confirm()
        for record in self.sudo():
            if record.employee_ids:
                record._create_leave_request(record.employee_ids)
            if record.leave_request_ids:
                record._confirm_leave_request(record.leave_request_ids)

    def _approve_leave_request(self, leave_request_ids):
        """Approve every child time off request of this batch.

        :param leave_request_ids: ``hr.leave`` recordset of this batch
        """
        self.ensure_one()
        for leave_request in leave_request_ids:
            leave_request.action_approve_approval()

    # BUTTON APPROVAL
    def action_approve_approval(self):
        """Approve the batch and cascade the approval to its children.

        Once the last approver signs off, the batch reaches ``done`` and
        every child ``hr.leave`` is approved as well, granting the time
        off to all employees of the batch at the same moment.
        """
        _super = super(HrLeaveRequestBatch, self)
        _super.action_approve_approval()
        for record in self.sudo():
            if record.leave_request_ids:
                record._approve_leave_request(record.leave_request_ids)

    def _reject_leave_request(self, leave_request_ids):
        """Reject every child time off request of this batch.

        :param leave_request_ids: ``hr.leave`` recordset of this batch
        """
        self.ensure_one()
        for leave_request in leave_request_ids:
            leave_request.action_reject_approval()

    # BUTTON REJECT
    def action_reject_approval(self):
        """Reject the batch and cascade the rejection to its children.

        No employee of the batch keeps the requested time off: every
        child ``hr.leave`` is rejected together with the batch itself.
        """
        _super = super(HrLeaveRequestBatch, self)
        _super.action_reject_approval()
        for record in self.sudo():
            if record.leave_request_ids:
                record._reject_leave_request(record.leave_request_ids)

    def _restart_leave_request(self, leave_request_ids):
        """Send every child time off request back to ``draft``.

        :param leave_request_ids: ``hr.leave`` recordset of this batch
        """
        self.ensure_one()
        for leave_request in leave_request_ids:
            leave_request.action_restart()

    # BUTTON RESTART
    def action_restart(self):
        """Reopen the batch and its children for editing.

        The batch returns to ``draft`` and every child ``hr.leave`` is
        restarted with it, so the employee list or the leave period can
        be corrected and submitted again.
        """
        _super = super(HrLeaveRequestBatch, self)
        _super.action_restart()
        for record in self.sudo():
            if record.leave_request_ids:
                record._restart_leave_request(record.leave_request_ids)

    def _cancel_leave_request(self, leave_request_ids, cancel_reason):
        """Cancel every child time off request with the batch reason.

        :param leave_request_ids: ``hr.leave`` recordset of this batch
        :param cancel_reason: ``base.cancel_reason`` recorded on the
            batch, reused as the reason of each child request
        """
        self.ensure_one()
        for leave_request in leave_request_ids:
            leave_request.action_cancel(cancel_reason)

    # BUTTON CANCEL
    def action_cancel(self, cancel_reason=False):
        """Cancel the batch and cascade the cancellation downwards.

        The reason picked by the user on the batch is passed on to every
        child ``hr.leave``, so the whole batch carries one explanation.

        :param cancel_reason: ``base.cancel_reason`` chosen by the user
        """
        _super = super(HrLeaveRequestBatch, self)
        _super.action_cancel()
        for record in self.sudo():
            if record.leave_request_ids:
                record._cancel_leave_request(record.leave_request_ids, cancel_reason)
