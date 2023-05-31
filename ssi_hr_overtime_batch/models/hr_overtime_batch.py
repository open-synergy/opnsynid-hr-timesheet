# Copyright 2023 OpenSynergy Indonesia
# Copyright 2023 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import _, api, fields, models
from odoo.exceptions import UserError

from odoo.addons.ssi_decorator import ssi_decorator


class HROvertimeBatch(models.Model):
    _name = "hr.overtime_batch"
    _description = "Overtime Batch"
    _inherit = [
        "mixin.datetime_duration",
        "mixin.transaction_confirm",
        "mixin.transaction_done",
        "mixin.transaction_cancel",
    ]
    _order = "date_start desc, id"

    # Multiple Approval Attribute
    _approval_from_state = "draft"
    _approval_to_state = "done"
    _approval_state = "confirm"
    _after_approved_method = "action_done"

    # Attributes related to add element on view automatically
    _automatically_insert_view_element = True
    _automatically_insert_done_button = False
    _automatically_insert_done_policy_fields = False

    # Mixin duration attribute
    _date_start_readonly = True
    _date_end_readonly = True
    _date_start_states_list = ["draft"]
    _date_start_states_readonly = ["draft"]
    _date_end_states_list = ["draft"]
    _date_end_states_readonly = ["draft"]

    # Attributes related to add element on form view automatically
    _automatically_insert_multiple_approval_page = True
    _statusbar_visible_label = "draft,confirm,done,rejected"
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
    _create_sequence_state = "done"

    name = fields.Char(string="# Document")
    type_id = fields.Many2one(
        comodel_name="hr.overtime_type",
        string="Overtime Type",
        required=True,
        ondelete="restrict",
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    employee_ids = fields.Many2many(
        comodel_name="hr.employee",
        string="Employee(s)",
        relation="rel_overtime_batch_2_employee",
        column1="overtime_batch_id",
        column2="employee_id",
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    overtime_ids = fields.One2many(
        comodel_name="hr.overtime",
        inverse_name="batch_id",
        string="Overtime(s)",
        readonly=True,
    )
    date_start = fields.Datetime(
        string="Date Start",
        required=True,
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    date_end = fields.Datetime(
        string="Date End",
        required=True,
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
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

    @api.model
    def _get_policy_field(self):
        res = super(HROvertimeBatch, self)._get_policy_field()
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

    def check_overtime(self, employee):
        self.ensure_one()
        obj_overtime = self.env["hr.overtime"]
        criteria = [
            "&",
            ("employee_id", "=", employee.id),
            "|",
            "&",
            ("date_start", "<=", self.date_start),
            ("date_end", ">=", self.date_start),
            "&",
            ("date_start", "<=", self.date_end),
            ("date_end", ">=", self.date_end),
        ]
        overtime_ids = obj_overtime.search(criteria)
        if overtime_ids:
            error_message = "Overtime is already created for %s" % (employee.name)
            raise UserError(_(error_message))
        else:
            return False

    @ssi_decorator.post_confirm_action()
    def _01_create_overtime(self):
        obj_overtime = self.env["hr.overtime"]
        for rec in self:
            if rec.employee_ids and not rec.overtime_ids:
                for employee_id in rec.employee_ids:
                    if not rec.check_overtime(employee_id):
                        overtime_id = obj_overtime.create(
                            {
                                "date": self.date_start.date(),
                                "date_start": self.date_start,
                                "date_end": self.date_end,
                                "batch_id": self.id,
                                "employee_id": employee_id.id,
                                "type_id": self.type_id.id,
                            }
                        )
                        rec._trigger_onchange(overtime_id)

    def _trigger_onchange(self, overtime):
        self.ensure_one()
        overtime.onchange_department_id()
        overtime.onchange_manager_id()
        overtime.onchange_job_id()

    @ssi_decorator.post_confirm_action()
    def _02_confirm_overtime(self):
        for rec in self:
            if rec.overtime_ids:
                rec.overtime_ids.action_confirm()

    @ssi_decorator.post_approve_action()
    def _approve_overtime(self):
        for rec in self:
            if rec.overtime_ids:
                rec.overtime_ids.action_approve_approval()

    @ssi_decorator.post_reject_action()
    def _reject_overtime(self):
        for rec in self:
            if rec.overtime_ids:
                rec.overtime_ids.action_reject_approval()

    @ssi_decorator.post_cancel_action()
    def _cancel_overtime(self):
        for rec in self:
            if rec.overtime_ids:
                rec.overtime_ids.action_cancel()

    @ssi_decorator.post_restart_action()
    def _restart_overtime(self):
        for rec in self:
            if rec.overtime_ids:
                rec.overtime_ids.action_restart()
