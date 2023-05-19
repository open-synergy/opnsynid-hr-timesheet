# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import _, api, fields, models
from odoo.exceptions import UserError

from odoo.addons.ssi_decorator import ssi_decorator


class HrLeaveAllocationRequestBatch(models.Model):
    _name = "hr.leave_allocation_request_batch"
    _description = "Leave Allocation Request Batch"
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
    _statusbar_visible_label = "draft,confirm,done,reject"
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

    # Sequence attribute
    _auto_fill_sequence = True
    _create_sequence_state = "done"

    @api.model
    def _get_policy_field(self):
        res = super(HrLeaveAllocationRequestBatch, self)._get_policy_field()
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
    )
    type_id = fields.Many2one(
        string="Type",
        comodel_name="hr.leave_type",
        required=True,
        ondelete="restrict",
    )
    number_of_days = fields.Integer(
        string="Number Of Days",
        required=True,
    )
    employee_ids = fields.Many2many(
        comodel_name="hr.employee",
        relation="rel_leave_allocation_request_batch_2_employee",
        column1="leave_allocation_request_batch_id",
        column2="employee_id",
        string="Employee",
    )
    leave_allocation_request_ids = fields.One2many(
        comodel_name="hr.leave_allocation",
        inverse_name="batch_id",
        string="Leave Allocation Request",
    )
    can_be_extended = fields.Boolean(
        string='Can be Extended',
        default=False,
        readonly=True,
        states={
            "draft": [("readonly", False)],
        },
    )
    date_extended = fields.Date(
        string='Date Extended',
        required=True,
        default=False,
        readonly=True,
        states={
            "draft": [("readonly", False)],
        },
    )

    def check_leave_allocation(self, employee):
        self.ensure_one()
        obj_leave_allocation = self.env["hr.leave_allocation"]
        criteria = [
            "&",
            ("employee_id", "=", employee.id),
            "|",
            "&",
            ("date_start", "<=", self.date_start),
            ("date_extended", ">=", self.date_start),
            "&",
            ("date_start", "<=", self.date_extended),
            ("date_extended", ">=", self.date_extended),
        ]
        allocation_ids = obj_leave_allocation.search(criteria)
        if allocation_ids:
            error_message = "Leave allocation is already created for %s" % (
                employee.name
            )
            raise UserError(_(error_message))
        else:
            return False

    @ssi_decorator.post_confirm_action()
    def _01_create_leave_allocation_request(self):
        obj_leave_allocation_request = self.env["hr.leave_allocation"]
        for record in self:
            if record.employee_ids and not record.leave_allocation_request_ids:
                for employee_id in record.employee_ids:
                    if not record.check_leave_allocation(employee_id):
                        allocation_id = obj_leave_allocation_request.create(
                            {
                                "date_start": self.date_start,
                                "date_end": self.date_end,
                                "can_be_extended": self.can_be_extended,
                                "date_extended": self.date_extended,
                                "batch_id": self.id,
                                "employee_id": employee_id.id,
                                "type_id": self.type_id.id,
                                "number_of_days": self.number_of_days,
                            }
                        )
                        record._trigger_onchange(allocation_id)

    def _trigger_onchange(self, allocation):
        self.ensure_one()
        allocation.onchange_department_id()
        allocation.onchange_manager_id()
        allocation.onchange_job_id()

    @ssi_decorator.post_confirm_action()
    def _02_confirm_leave_allocation_request(self):
        for record in self:
            if record.leave_allocation_request_ids:
                record.leave_allocation_request_ids.action_approve_approval()

    @ssi_decorator.post_approve_action()
    def _approve_leave_allocation_request(self):
        for record in self:
            if record.leave_allocation_request_ids:
                record.leave_allocation_request_ids.action_approve_approval()

    @ssi_decorator.post_reject_action()
    def _reject_leave_allocation_request(self):
        for record in self:
            if record.leave_allocation_request_ids:
                record.leave_allocation_request_ids.action_reject()

    @ssi_decorator.post_done_action()
    def _done_leave_allocation_request(self):
        for record in self:
            if record.leave_allocation_request_ids:
                record.leave_allocation_request_ids.action_done()

    @ssi_decorator.post_restart_action()
    def _restart_leave_allocation_request(self):
        for record in self:
            if record.leave_allocation_request_ids:
                record.leave_allocation_request_ids.action_restart()

    @ssi_decorator.post_cancel_action()
    def _cancel_leave_allocation_request(self):
        for record in self:
            if record.leave_allocation_request_ids:
                record.leave_allocation_request_ids.action_cancel()

    @api.onchange(
        'date_end',
        'can_be_extended',
        'date_extended',
    )
    def onchange_date_extended(self):
        if not self.date_extended or not self.can_be_extended:
            self.date_extended = self.date_end
        if self.date_end and self.date_extended < self.date_end:
            self.date_extended = self.date_end
            return {'warning': {
                'title': 'Wrong value',
                'message': 'Date extended can not be less than date end.',
            }}
