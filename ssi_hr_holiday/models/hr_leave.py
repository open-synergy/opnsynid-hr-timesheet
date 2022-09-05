# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from datetime import datetime

from dateutil.relativedelta import relativedelta
from dateutil.rrule import DAILY, rrule
from openerp import _, api, fields, models
from openerp.exceptions import Warning as UserError


class HRLeave(models.Model):
    _name = "hr.leave"
    _inherit = [
        "mail.thread",
        "tier.validation",
        "base.sequence_document",
        "base.workflow_policy_object",
        "base.cancel.reason_common",
        "base.terminate.reason_common",
    ]
    _description = "Leaves"
    _state_from = ["draft", "confirm"]
    _state_to = ["done"]

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

    @api.depends(
        "employee_id",
        "date_start",
        "date_end",
    )
    def _compute_sheet(self):
        obj_sheet = self.env["hr_timesheet_sheet.sheet"]
        for record in self:
            sheet_id = False
            if record.employee_id and record.date_start and record.date_end:
                criteria = [
                    ("employee_id", "=", record.employee_id.id),
                    ("date_from", "<=", record.date_start),
                    ("date_to", ">=", record.date_end),
                ]
                sheet = obj_sheet.search(criteria, limit=1)
                if len(sheet) > 0:
                    sheet_id = sheet[0].id
                else:
                    strWarning = _("No Timesheet Found")
                    raise UserError(strWarning)
            record.sheet_id = sheet_id

    sheet_id = fields.Many2one(
        string="# Timesheet",
        comodel_name="hr_timesheet_sheet.sheet",
        compute="_compute_sheet",
        store=True,
        compute_sudo=True,
    )

    @api.depends(
        "date_start",
        "date_end",
        "employee_id",
    )
    def _compute_schedule_ids(self):
        obj_att_schedule = self.env["hr.timesheet_attendance_schedule"]
        for record in self:

            if record.date_start and record.date_end and record.employee_id:
                # TODO
                dt_start = fields.Datetime.from_string(
                    record.date_start
                ) + relativedelta(hours=-7)
                dt_end = fields.Datetime.from_string(record.date_end) + relativedelta(
                    hours=16
                )

                str_start = fields.Datetime.to_string(dt_start)
                str_end = fields.Datetime.to_string(dt_end)
                criteria = [
                    ("employee_id", "=", record.employee_id.id),
                    ("date_start", "<=", str_end),
                    ("date_start", ">=", str_start),
                ]
                schedule = obj_att_schedule.search(criteria)
                record.schedule_ids = schedule.ids

    schedule_ids = fields.Many2many(
        string="Schedules",
        comodel_name="hr.timesheet_attendance_schedule",
        compute="_compute_schedule_ids",
        relation="rel_attendance_schedule_2_leave",
        column1="leave_id",
        column2="attendance_schedule_id",
        store=True,
    )

    number_of_days = fields.Integer(
        string="Number of Days",
        required=True,
        default=0,
        readonly=True,
        states={
            "draft": [("readonly", False)],
        },
    )

    @api.depends(
        "date_start",
        "date_end",
    )
    def _compute_leave_duration(self):
        obj_public_holiday = self.env["base.public.holiday"]
        for record in self:
            leave_duration = 0
            if record.date_start and record.date_end:
                leave_duration = len(record.schedule_ids)
                dt_date_start = datetime.strptime(record.date_start, "%Y-%m-%d")
                leave_dates = rrule(
                    DAILY,
                    dtstart=dt_date_start,
                    count=leave_duration,
                )
                for leave_date in list(leave_dates):
                    if obj_public_holiday.is_public_holiday(leave_date):
                        leave_duration -= 1
            record.leave_duration = leave_duration

    leave_duration = fields.Integer(
        string="Duration",
        compute="_compute_leave_duration",
        store=True,
        compute_sudo=True,
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

    @api.multi
    @api.depends(
        "type_id",
        "employee_id",
        "date_start",
        "date_end",
    )
    def _compute_leave_allocation_id(self):
        for record in self:
            result = False
            if (
                record.type_id
                and record.employee_id
                and record.date_start
                and record.date_end
            ):
                result = record._get_leave_allocation()
            record.leave_allocation_id = result

    leave_allocation_id = fields.Many2one(
        string="# Leave Allocation",
        comodel_name="hr.leave_allocation",
        ondelete="restrict",
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
    def _get_leave_allocation(self):
        self.ensure_one()
        obj_hr_leave_all = self.env["hr.leave_allocation"]
        result = False
        criteria = [
            "&",
            "&",
            "&",
            "&",
            ("type_id", "=", self.type_id.id),
            ("employee_id", "=", self.employee_id.id),
            ("state", "=", "open"),
            ("num_of_days_available", ">=", self.number_of_days),
            "|",
            "&",
            ("date_start", "<=", self.date_start),
            ("date_end", "=", False),
            "&",
            ("date_start", "<=", self.date_start),
            ("date_end", ">=", self.date_end),
        ]
        leave_allocations = obj_hr_leave_all.search(
            criteria, order="date_start asc", limit=1
        )
        if len(leave_allocations) > 0:
            result = leave_allocations[0]
        return result

    @api.multi
    def _compute_policy(self):
        _super = super(HRLeave, self)
        _super._compute_policy()

    @api.multi
    def action_confirm(self):
        for record in self:
            if not record.schedule_ids:
                record._compute_schedule_ids()
            record._compute_leave_allocation_id()
            record.write(record._prepare_confirm_data())
            record.request_validation()

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
    def action_restart(self):
        for record in self:
            record.write(record._prepare_restart_data())

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
        _super = super(HRLeave, self)
        _super.validate_tier()
        for document in self:
            if document.validated:
                document.action_done()

    @api.multi
    def restart_validation(self):
        _super = super(HRLeave, self)
        _super.restart_validation()
        for document in self:
            document.request_validation()

    @api.onchange(
        "employee_id",
        "type_id",
        "date_start",
        "date_end",
    )
    def onchange_leave_allocation_id(self):
        self.leave_allocation_id = False
        if self.type_id and self.employee_id and self.date_start and self.date_end:
            allocation = self._get_leave_allocation()
            if allocation:
                self.leave_allocation_id = allocation

    @api.onchange(
        "leave_duration",
    )
    def onchange_number_of_day(self):
        self.number_of_days = self.leave_duration

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

    @api.constrains("date_start", "date_end", "employee_id")
    def _constrains_overlap(self):
        for record in self.sudo():
            if not record._check_overlap():
                error_message = _(
                    """
                Context: Change date start or date end on leave request
                Database ID: %s
                Problem: There are other leave(s) that overlap
                Solution: Change date start and date end
                """
                    % (record.id)
                )
                raise UserError(error_message)

    @api.constrains("type_id", "number_of_days")
    def _constrains_limit_request(self):
        for record in self.sudo():
            limit = record.type_id.limit_per_request
            if not record._check_limit_per_request():
                error_message = _(
                    """
                Context: Change type or number of days on leave request
                Database ID: %s
                Problem: Number of days exceed %s
                Solution: Reduce number of days so it is less or equal than %s
                """
                    % (record.id, limit, limit)
                )
                raise UserError(error_message)

    @api.constrains("state")
    def _constrains_confirm(self):
        for record in self.sudo():
            if record.state != "confirm":
                break

            if not record._check_leave_allocation_available():
                error_message = """
                Context: Confirming leave
                Database ID: %s
                Problem: Leave need leave request. No available leave request found
                Solution: Create relevant leave allocation
                """ % (
                    record.id
                )
                raise UserError(_(error_message))

    @api.multi
    def _check_overlap(self):
        self.ensure_one()
        result = True
        Leave = self.env["hr.leave"]
        criteria = [
            ("employee_id", "=", self.employee_id.id),
            ("state", "not in", ["cancel", "reject"]),
            ("id", "!=", self.id),
            ("date_start", "<=", self.date_end),
            ("date_end", ">=", self.date_start),
        ]
        num_of_leave = Leave.search_count(criteria)
        if num_of_leave > 0:
            result = False

        return result

    @api.multi
    def _check_limit_per_request(self):
        self.ensure_one()
        result = True
        if (
            self.type_id.apply_limit_per_request
            and self.number_of_days > self.type_id.limit_per_request
        ):
            result = False
        return result

    @api.multi
    def _check_leave_allocation_available(self):
        self.ensure_one()
        result = True
        if self.type_id.need_allocation:
            if not self.leave_allocation_id:
                result = False
        return result

    @api.constrains("date_start", "date_end")
    def _check_date_start_end(self):
        for record in self:
            if record.date_start and record.date_end:
                strWarning = _("Date end must be greater than date start")
                if record.date_end < record.date_start:
                    raise UserError(strWarning)
