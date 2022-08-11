# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import _, api, fields, models
from odoo.exceptions import Warning as UserError


class HRTimesheetAttendance(models.Model):
    _name = "hr.timesheet_attendance"
    _description = "Timesheet Attendance"
    _order = "date,check_in"

    @api.model
    def _default_employee_id(self):
        return self.env.user.employee_id

    date = fields.Date(
        string="Date",
        required=True,
    )

    @api.depends("date")
    def _compute_sheet(self):
        obj_sheet = self.env["hr.timesheet"]
        for record in self:
            criteria = [
                ("employee_id", "=", record.employee_id.id),
                ("date_start", "<=", record.date),
                ("date_end", ">=", record.date),
                ("state", "=", "open"),
            ]
            sheet = obj_sheet.search(criteria, limit=1)
            if len(sheet) > 0:
                record.sheet_id = sheet[0].id
            else:
                strWarning = _(
                    "Sheet Not FOUND .. Check in "
                    + fields.Datetime.context_timestamp(self, record.check_in).strftime(
                        "%m/%d/%Y, %H:%M:%S"
                    )
                )
                raise UserError(strWarning)

    sheet_id = fields.Many2one(
        string="Sheet",
        comodel_name="hr.timesheet",
        ondelete="cascade",
        required=True,
        compute="_compute_sheet",
        store=True,
        compute_sudo=True,
    )
    check_in = fields.Datetime(
        string="Check In",
        default=fields.Datetime.now,
        required=True,
    )
    check_out = fields.Datetime(
        string="Check Out",
    )

    @api.depends(
        "check_in",
        "check_out",
    )
    def _compute_state(self):
        for attn in self:
            if attn.check_in and attn.check_out:
                attn.state = "present"
            elif (attn.check_in and not attn.check_out) or (
                not attn.check_in and attn.check_out
            ):
                attn.state = "open"

    state = fields.Selection(
        string="State",
        selection=[
            ("open", "Open"),
            ("present", "Present"),
        ],
        default="open",
        required=True,
        compute="_compute_state",
        store=True,
        compute_sudo=True,
    )

    employee_id = fields.Many2one(
        string="Employee",
        comodel_name="hr.employee",
        default=lambda self: self._default_employee_id(),
        required=True,
        ondelete="restrict",
    )
    schedule_id = fields.Many2one(
        string="Attendance Schedule",
        comodel_name="hr.timesheet_attendance_schedule",
        compute="_compute_schedule",
        store=True,
        compute_sudo=True,
    )
    valid_check_in = fields.Datetime(
        string="Valid Check In",
        compute="_compute_valid",
        store=True,
        compute_sudo=True,
    )
    valid_check_out = fields.Datetime(
        string="Valid Check Out",
        compute="_compute_valid",
        store=True,
        compute_sudo=True,
    )
    total_hour = fields.Float(
        string="Total Hour",
        compute="_compute_hour",
        store=True,
        compute_sudo=True,
    )
    total_valid_hour = fields.Float(
        string="Total Valid Hour",
        compute="_compute_valid",
        store=True,
        compute_sudo=True,
    )
    reason_check_in_id = fields.Many2one(
        string="Reason In",
        comodel_name="hr.attendance_reason",
        ondelete="restrict",
    )
    reason_check_out_id = fields.Many2one(
        string="Reason Out",
        comodel_name="hr.attendance_reason",
        ondelete="restrict",
    )

    @api.depends(
        "schedule_id",
        "schedule_id.date_start",
        "schedule_id.date_end",
        "check_in",
        "check_out",
    )
    def _compute_valid(self):
        for record in self:
            valid_check_in = valid_check_out = False
            if record.schedule_id:
                if record.check_in >= record.schedule_id.date_start:
                    valid_check_in = record.check_in
                elif record.check_in < record.schedule_id.date_start:
                    valid_check_in = record.schedule_id.date_start
                if record.check_out:
                    if record.check_out < record.schedule_id.date_end:
                        if record.check_out < record.schedule_id.date_start:
                            valid_check_out = record.schedule_id.date_start
                        else:
                            valid_check_out = record.check_out
                    elif record.check_out >= record.schedule_id.date_end:
                        valid_check_out = record.schedule_id.date_end
                record.valid_check_in = valid_check_in
                record.valid_check_out = valid_check_out
                if record.valid_check_in and record.valid_check_out:
                    record.total_valid_hour = (
                        record.valid_check_out - record.valid_check_in
                    ).total_seconds() / 3600.0
                else:
                    record.total_valid_hour = 0.0

    @api.depends(
        "check_in",
        "check_out",
    )
    def _compute_hour(self):
        for record in self:
            result = 0.0
            if record.check_in and record.check_out:
                result = (record.check_out - record.check_in).total_seconds() / 3600.0
            record.total_hour = result

    @api.depends("date")
    def _compute_schedule(self):
        obj_schedule = self.env["hr.timesheet_attendance_schedule"]
        for attn in self:
            # company = attn.employee_id.company_id
            criteria = [
                ("employee_id", "=", attn.employee_id.id),
                ("date", "=", attn.date),
            ]
            schedules = obj_schedule.search(criteria, limit=1)
            attn.schedule_id = schedules[0].id if len(schedules) > 0 else False