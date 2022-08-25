# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
from datetime import datetime

from openerp import _, api, fields, models
from openerp.exceptions import Warning as UserError


class HrLeaveAllocation(models.Model):
    _name = "hr.leave_allocation"
    _inherit = [
        "mail.thread",
        "tier.validation",
        "base.sequence_document",
        "base.workflow_policy_object",
        "base.cancel.reason_common",
        "base.terminate.reason_common",
    ]
    _description = "Leave Allocation"
    _order = "date_start,id"

    _state_from = ["draft", "confirm"]
    _state_to = ["open"]

    name = fields.Char(
        string="# Document",
        default="/",
        required=True,
        copy=False,
        readonly=True,
        states={"draft": [("readonly", False)]},
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
    def _default_employee_id(self):
        employees = self.env.user.employee_ids
        if len(employees) > 0:
            return employees[0].id

    employee_id = fields.Many2one(
        string="Employee",
        comodel_name="hr.employee",
        default=lambda self: self._default_employee_id(),
        required=True,
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    department_id = fields.Many2one(
        string="Department",
        comodel_name="hr.department",
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    manager_id = fields.Many2one(
        string="Manager",
        comodel_name="hr.employee",
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    job_id = fields.Many2one(
        string="Job Position",
        comodel_name="hr.job",
        readonly=True,
        states={"draft": [("readonly", False)]},
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
        states={"draft": [("readonly", False)]},
    )

    date_start = fields.Date(
        string="Start Date",
        readonly=True,
        states={"draft": [("readonly", False)]},
        default=datetime.now().strftime("%Y-%m-%d"),
    )
    date_end = fields.Date(
        string="End Date",
        readonly=True,
        states={"draft": [("readonly", False)]},
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

    @api.multi
    @api.depends(
        "leave_ids",
        "leave_ids.number_of_days",
        "leave_ids.state",
        "leave_ids.type_id",
        "number_of_days",
    )
    def _compute_num_of_days(self):
        for leave in self:
            num_of_days_used = num_of_days_planned = num_of_days_available = 0.0
            for record in leave.leave_ids:
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

    num_of_days_used = fields.Integer(
        string="Used Days",
        compute="_compute_num_of_days",
        store=True,
    )
    num_of_days_planned = fields.Integer(
        string="Plannned Days",
        compute="_compute_num_of_days",
        store=True,
    )
    num_of_days_available = fields.Integer(
        string="Available Days",
        compute="_compute_num_of_days",
        store=True,
    )

    state = fields.Selection(
        string="State",
        selection=[
            ("draft", "Draft"),
            ("confirm", "Waiting for Approval"),
            ("open", "In Progress"),
            ("done", "Done"),
            ("cancel", "Cancelled"),
            ("rejected", "Rejected"),
            ("terminate", "Terminated"),
        ],
        default="draft",
        required=True,
        copy=False,
        readonly=True,
        states={"draft": [("readonly", False)]},
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
    done_ok = fields.Boolean(
        string="Can Finished",
        compute="_compute_policy",
    )
    cancel_ok = fields.Boolean(
        string="Can Cancel",
        compute="_compute_policy",
    )
    restart_ok = fields.Boolean(
        string="Can Restart",
        compute="_compute_policy",
    )
    terminate_ok = fields.Boolean(
        string="Can Terminate",
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
    restart_approval_ok = fields.Boolean(
        string="Can Restart Approval",
        compute="_compute_policy",
    )

    @api.multi
    def _compute_policy(self):
        _super = super(HrLeaveAllocation, self)
        _super._compute_policy()

    @api.multi
    def action_confirm(self):
        for record in self:
            record.write(record._prepare_confirm_data())
            record.request_validation()

    @api.multi
    def action_open(self):
        for record in self:
            record.write(record._prepare_open_data())

    @api.multi
    def action_done(self):
        for record in self:
            record.write(record._prepare_done_data())

    @api.multi
    def action_cancel(self):
        for record in self:
            record.write(record._prepare_cancel_data())
            record.restart_validation()

    @api.multi
    def action_terminate(self):
        for record in self:
            record.write(record._prepare_terminate_data())

    @api.multi
    def _prepare_confirm_data(self):
        self.ensure_one()
        return {
            "state": "confirm",
        }

    @api.multi
    def _prepare_open_data(self):
        self.ensure_one()
        ctx = self.env.context.copy()
        ctx.update(
            {
                "ir_sequence_date": self.date_start,
            }
        )
        sequence = self.with_context(ctx)._create_sequence()
        result = {
            "state": "open",
            "name": sequence,
        }
        return result

    @api.multi
    def _prepare_done_data(self):
        self.ensure_one()
        return {
            "state": "done",
        }

    @api.multi
    def _prepare_cancel_data(self):
        self.ensure_one()
        return {
            "state": "cancel",
        }

    @api.multi
    def _prepare_terminate_data(self):
        self.ensure_one()
        return {
            "state": "terminate",
        }

    @api.multi
    def validate_tier(self):
        _super = super(HrLeaveAllocation, self)
        _super.validate_tier()
        for document in self:
            if document.validated:
                document.action_open()

    @api.multi
    def restart_validation(self):
        _super = super(HrLeaveAllocation, self)
        _super.restart_validation()
        for document in self:
            document.request_validation()

    @api.onchange(
        "employee_id",
    )
    def onchange_department_id(self):
        self.department_id = False
        if self.employee_id:
            self.department_id = self.employee_id.department_id

    @api.onchange(
        "employee_id",
    )
    def onchange_manager_id(self):
        self.manager_id = False
        if self.employee_id:
            self.manager_id = self.employee_id.parent_id

    @api.onchange(
        "employee_id",
    )
    def onchange_job_id(self):
        self.job_id = False
        if self.employee_id:
            self.job_id = self.employee_id.job_id

    @api.multi
    def name_get(self):
        result = []
        for record in self:
            if record.name == "/":
                name = "*" + str(record.id)
            else:
                name = record.name
            result.append((record.id, name))
        return result

    @api.constrains("state")
    def _constrains_leave(self):
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

    @api.multi
    def _check_leave(self):
        self.ensure_one()
        result = True
        if self.leave_ids:
            result = False

        return result

    @api.constrains("date_start", "date_end")
    def _check_date_start_end(self):
        for record in self:
            if record.date_start and record.date_end:
                strWarning = _("Date end must be greater than date start")
                if record.date_end < record.date_start:
                    raise UserError(strWarning)
