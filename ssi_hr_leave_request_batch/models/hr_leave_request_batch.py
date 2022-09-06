# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from datetime import datetime

from openerp import _, api, fields, models
from openerp.exceptions import Warning as UserError


class HRLeaveRequestBatch(models.Model):
    _name = "hr.leave_request_batch"
    _inherit = [
        "mail.thread",
        "tier.validation",
        "base.sequence_document",
        "base.workflow_policy_object",
        "base.cancel.reason_common",
    ]
    _description = "Leave Request Batch"
    _state_from = ["draft", "confirm"]
    _state_to = ["done"]

    name = fields.Char(
        string="# Document",
        default="/",
        required=True,
        copy=False,
        readonly=True,
        states={
            "draft": [("readonly", False)],
        },
    )

    @api.model
    def _default_company_id(self):
        return self.env.user.company_id.id

    company_id = fields.Many2one(
        string="Company",
        comodel_name="res.company",
        required=True,
        default=lambda self: self._default_company_id(),
        copy=True,
    )

    @api.model
    def _default_user_id(self):
        return self.env.user.id

    user_id = fields.Many2one(
        string="Responsible",
        comodel_name="res.users",
        required=True,
        default=lambda self: self._default_user_id(),
        copy=False,
        readonly=True,
        states={
            "draft": [("readonly", False)],
        },
    )

    date_start = fields.Date(
        string="Start Date",
        readonly=True,
        required=True,
        states={
            "draft": [("readonly", False)],
        },
        default=datetime.now().strftime("%Y-%m-%d"),
    )
    date_end = fields.Date(
        string="End Date",
        readonly=True,
        required=True,
        states={
            "draft": [("readonly", False)],
        },
    )

    employee_ids = fields.Many2many(
        string="Employees",
        comodel_name="hr.employee",
        relation="rel_leave_2_employee",
        column1="leave_id",
        column2="employee_id",
        ondelete="restrict",
        required=True,
        readonly=True,
        states={
            "draft": [("readonly", False)],
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
        },
    )
    leave_ids = fields.One2many(
        string="Leaves",
        comodel_name="hr.leave",
        inverse_name="batch_id",
        readonly=True,
    )
    state = fields.Selection(
        string="State",
        selection=[
            ("draft", "Draft"),
            ("confirm", "Waiting for Approval"),
            ("done", "Done"),
            ("cancel", "Cancelled"),
        ],
        default="draft",
        copy=False,
    )
    note = fields.Text(
        string="Note",
        copy=True,
    )

    # Policy Field
    confirm_ok = fields.Boolean(
        string="Can Confirm",
        compute="_compute_policy",
    )
    cancel_ok = fields.Boolean(
        string="Can Cancel",
        compute="_compute_policy",
    )
    approve_ok = fields.Boolean(
        string="Can Approve",
        compute="_compute_policy",
    )
    reject_ok = fields.Boolean(
        string="Can Reject",
        compute="_compute_policy",
    )
    restart_ok = fields.Boolean(
        string="Can Restart",
        compute="_compute_policy",
    )
    restart_approval_ok = fields.Boolean(
        string="Can Restart Approval",
        compute="_compute_policy",
    )

    @api.multi
    def _compute_policy(self):
        _super = super(HRLeaveRequestBatch, self)
        _super._compute_policy()

    @api.multi
    def _trigger_onchange(self, leave):
        self.ensure_one()
        leave.onchange_leave_allocation_id()
        leave.onchange_number_of_day()
        leave.onchange_department_id()
        leave.onchange_manager_id()
        leave.onchange_job_id()

    @api.multi
    def _prepare_leave_data(self, employee_id):
        self.ensure_one()
        return {
            "employee_id": employee_id,
            "type_id": self.type_id.id,
            "date_start": self.date_start,
            "date_end": self.date_end,
            "batch_id": self.id,
        }

    @api.multi
    def _create_leave(self):
        self.ensure_one()
        obj_hr_leave = self.env["hr.leave"]
        for employee in self.employee_ids:
            if (
                len(self.leave_ids.filtered(lambda r: r.employee_id.id == employee.id))
                == 0
            ):
                leave_id = obj_hr_leave.create(self._prepare_leave_data(employee.id))
                self._trigger_onchange(leave_id)

    @api.multi
    def action_confirm(self):
        for document in self:
            document._create_leave()
            document.write(document._prepare_confirm_data())
            document.request_validation()
            document.leave_ids.action_confirm()

    @api.multi
    def action_done(self):
        for document in self:
            document.write(document._prepare_done_data())

    @api.multi
    def action_cancel(self):
        for document in self:
            document.write(document._prepare_cancel_data())
            document.restart_validation()
            document.leave_ids.action_cancel()
            document.leave_ids.write({"cancel_reason_id": document.cancel_reason_id.id})

    @api.multi
    def action_restart(self):
        for document in self:
            document.write(document._prepare_restart_data())
            document.leave_ids.action_restart()

    @api.multi
    def _prepare_confirm_data(self):
        self.ensure_one()
        return {
            "state": "confirm",
        }

    @api.multi
    def _prepare_done_data(self):
        self.ensure_one()
        ctx = self.env.context.copy()
        ctx.update(
            {
                "ir_sequence_date": self.date_start,
            }
        )
        sequence = self.with_context(ctx)._create_sequence()
        return {
            "state": "done",
            "name": sequence,
        }

    @api.multi
    def _prepare_cancel_data(self):
        self.ensure_one()
        return {
            "state": "cancel",
        }

    @api.multi
    def _prepare_restart_data(self):
        self.ensure_one()
        return {
            "state": "draft",
        }

    @api.multi
    def validate_tier(self):
        _super = super(HRLeaveRequestBatch, self)
        _super.validate_tier()
        for document in self:
            if document.validated:
                document.action_done()
                document.leave_ids.validate_tier()

    @api.multi
    def restart_validation(self):
        _super = super(HRLeaveRequestBatch, self)
        _super.restart_validation()
        for document in self:
            document.request_validation()
            document.leave_ids.request_validation()

    @api.multi
    def name_get(self):
        result = []
        for document in self:
            if document.name == "/":
                name = "*" + str(document.id)
            else:
                name = document.name
            result.append((document.id, name))
        return result

    @api.constrains("date_start", "date_end")
    def _check_date_start_end(self):
        for document in self:
            if document.date_start and document.date_end:
                strWarning = _("Date end must be greater than date start")
                if document.date_end < document.date_start:
                    raise UserError(strWarning)
