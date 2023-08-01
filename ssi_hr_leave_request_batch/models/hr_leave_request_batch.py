# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models


class HrLeaveRequestBatch(models.Model):
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
        self.ensure_one()
        leave.onchange_number_of_day()
        leave.onchange_department_id()
        leave.onchange_manager_id()
        leave.onchange_job_id()

    def _confirm_leave_request(self, leave_request_ids):
        self.ensure_one()
        for leave_request in leave_request_ids:
            leave_request.action_confirm()

    # BUTTON CONFIRM
    def action_confirm(self):
        _super = super(HrLeaveRequestBatch, self)
        _super.action_confirm()
        for record in self.sudo():
            if record.employee_ids:
                record._create_leave_request(record.employee_ids)
            if record.leave_request_ids:
                record._confirm_leave_request(record.leave_request_ids)

    def _approve_leave_request(self, leave_request_ids):
        self.ensure_one()
        for leave_request in leave_request_ids:
            leave_request.action_approve_approval()

    # BUTTON APPROVAL
    def action_approve_approval(self):
        _super = super(HrLeaveRequestBatch, self)
        _super.action_approve_approval()
        for record in self.sudo():
            if record.leave_request_ids:
                record._approve_leave_request(record.leave_request_ids)

    def _reject_leave_request(self, leave_request_ids):
        self.ensure_one()
        for leave_request in leave_request_ids:
            leave_request.action_reject_approval()

    # BUTTON REJECT
    def action_reject_approval(self):
        _super = super(HrLeaveRequestBatch, self)
        _super.action_reject_approval()
        for record in self.sudo():
            if record.leave_request_ids:
                record._reject_leave_request(record.leave_request_ids)

    def _restart_leave_request(self, leave_request_ids):
        self.ensure_one()
        for leave_request in leave_request_ids:
            leave_request.action_restart()

    # BUTTON RESTART
    def action_restart(self):
        _super = super(HrLeaveRequestBatch, self)
        _super.action_restart()
        for record in self.sudo():
            if record.leave_request_ids:
                record._restart_leave_request(record.leave_request_ids)

    def _cancel_leave_request(self, leave_request_ids, cancel_reason):
        self.ensure_one()
        for leave_request in leave_request_ids:
            leave_request.action_cancel(cancel_reason)

    # BUTTON CANCEL
    def action_cancel(self, cancel_reason=False):
        _super = super(HrLeaveRequestBatch, self)
        _super.action_cancel()
        for record in self.sudo():
            if record.leave_request_ids:
                record._cancel_leave_request(record.leave_request_ids, cancel_reason)
