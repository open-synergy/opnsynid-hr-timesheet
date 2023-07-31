# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo import _, api, fields, models
from odoo.exceptions import Warning as UserError


class HRTimesheetAttendanceSchedule(models.Model):
    _name = "hr.timesheet_attendance_schedule"
    _inherit = [
        "mixin.datetime_duration",
    ]
    _description = "Timesheet Attendance Schedule"
    _rec_name = "id"
    _order = "sheet_id,date"

    @api.model
    def _default_employee_id(self):
        return self.env.user.employee_id

    @api.depends("date_start")
    def _compute_date(self):
        for record in self:
            record.date = False
            if record.date_start:
                date_start = fields.Datetime.to_datetime(record.date_start)
                record.date = fields.Datetime.context_timestamp(self, date_start)

    @api.depends(
        "date",
        "employee_id",
    )
    def _compute_sheet(self):
        obj_sheet = self.env["hr.timesheet"]
        for record in self:
            criteria = [
                ("employee_id", "=", record.employee_id.id),
                ("date_start", "<=", record.date),
                ("date_end", ">=", record.date),
            ]
            sheet = obj_sheet.search(criteria, limit=1)
            if len(sheet) > 0:
                record.sheet_id = sheet[0].id
            else:
                raise UserError(str(record.date))

    @api.depends(
        "attendance_ids",
        "attendance_ids.check_in",
        "attendance_ids.check_out",
        "attendance_ids.total_hour",
        "attendance_ids.total_valid_hour",
    )
    def _compute_attendance(self):
        obj_attendance = self.env["hr.timesheet_attendance"]
        for schedule in self:
            real_date_start = real_date_end = False
            real_work_hour = real_valid_hour = 0.0
            criteria = [
                ("schedule_id", "=", schedule.id),
            ]
            attendances = obj_attendance.search(criteria, order="check_in")
            if attendances:
                real_date_start = attendances[0].check_in
                for record in attendances:
                    real_date_end = record.check_out
                    if record.check_in and record.check_out:
                        real_work_hour += record.total_hour
                        real_valid_hour += record.total_valid_hour

            schedule.real_date_start = real_date_start
            schedule.real_date_end = real_date_end
            schedule.real_work_hour = real_work_hour
            schedule.real_valid_hour = real_valid_hour

    @api.depends(
        "real_date_start",
        "real_date_end",
    )
    def _compute_state(self):
        for attn in self:
            if attn.real_date_start and attn.real_date_end:
                attn.state = "present"
            elif (attn.real_date_start and not attn.real_date_end) or (
                not attn.real_date_start and attn.real_date_end
            ):
                attn.state = "open"
            elif not attn.real_date_start and not attn.real_date_start:
                attn.state = "absence"

    @api.depends(
        "date_start",
        "date_end",
        "real_date_start",
        "real_date_start",
    )
    def _compute_work_hour(self):
        for attn in self:
            schedule_work_hour = (
                early_start_hour
            ) = late_start_hour = finish_early_hour = finish_late_hour = 0.0
            dt_schedule_start = (
                fields.Datetime.from_string(attn.date_start)
                if attn.date_start
                else False
            )
            dt_schedule_end = (
                fields.Datetime.from_string(attn.date_end) if attn.date_end else False
            )
            dt_real_start = (
                fields.Datetime.from_string(attn.real_date_start)
                if attn.real_date_start
                else False
            )
            dt_real_end = (
                fields.Datetime.from_string(attn.real_date_end)
                if attn.real_date_end
                else False
            )

            if dt_schedule_start and dt_schedule_end:
                schedule_work_hour = (
                    dt_schedule_end - dt_schedule_start
                ).total_seconds() / 3600.0

            if dt_schedule_start and dt_real_start:
                if dt_schedule_start > dt_real_start:
                    early_start_hour = (
                        dt_schedule_start - dt_real_start
                    ).total_seconds() / 3600.0

                if dt_schedule_start < dt_real_start:
                    late_start_hour = (
                        dt_real_start - dt_schedule_start
                    ).total_seconds() / 3600.0

            if dt_schedule_end and dt_real_end:
                if dt_schedule_end > dt_real_end:
                    finish_early_hour = (
                        dt_schedule_end - dt_real_end
                    ).total_seconds() / 3600.0

                if dt_schedule_end < dt_real_end:
                    finish_late_hour = (
                        dt_real_end - dt_schedule_end
                    ).total_seconds() / 3600.0

            attn.schedule_work_hour = schedule_work_hour
            attn.early_start_hour = early_start_hour
            attn.late_start_hour = late_start_hour
            attn.finish_early_hour = finish_early_hour
            attn.finish_late_hour = finish_late_hour

    date = fields.Date(
        string="Date",
        compute="_compute_date",
        store=True,
        compute_sudo=True,
    )
    sheet_id = fields.Many2one(
        string="# Timesheet",
        comodel_name="hr.timesheet",
        compute="_compute_sheet",
        store=True,
        compute_sudo=True,
    )
    employee_id = fields.Many2one(
        string="Employee",
        comodel_name="hr.employee",
        default=lambda self: self._default_employee_id(),
        required=True,
    )
    attendance_ids = fields.One2many(
        string="Attendances",
        comodel_name="hr.timesheet_attendance",
        inverse_name="schedule_id",
    )
    real_date_start = fields.Datetime(
        string="Real Date Start",
        compute="_compute_attendance",
        store=True,
        readonly=True,
        compute_sudo=True,
    )
    real_date_end = fields.Datetime(
        string="Real Date End",
        compute="_compute_attendance",
        store=True,
        readonly=True,
        compute_sudo=True,
    )
    state = fields.Selection(
        string="State",
        selection=[
            ("absence", "Absence"),
            ("open", "Open"),
            ("present", "Present"),
        ],
        default="absence",
        required=True,
        compute="_compute_state",
        store=True,
        compute_sudo=True,
    )
    schedule_work_hour = fields.Float(
        string="Schedule Work Hour",
        compute="_compute_work_hour",
        store=True,
        compute_sudo=True,
    )
    real_work_hour = fields.Float(
        string="Real Work Hour",
        compute="_compute_attendance",
        store=True,
        compute_sudo=True,
    )
    real_valid_hour = fields.Float(
        string="Real Valid Hour",
        compute="_compute_attendance",
        store=True,
        compute_sudo=True,
    )
    early_start_hour = fields.Float(
        string="Early Start",
        compute="_compute_work_hour",
        store=True,
        compute_sudo=True,
    )
    late_start_hour = fields.Float(
        string="Late Start",
        compute="_compute_work_hour",
        store=True,
        compute_sudo=True,
    )
    finish_early_hour = fields.Float(
        string="Finish Early",
        compute="_compute_work_hour",
        store=True,
        compute_sudo=True,
    )
    finish_late_hour = fields.Float(
        string="Finish Late",
        compute="_compute_work_hour",
        store=True,
        compute_sudo=True,
    )

    @api.constrains("schedule_work_hour")
    def _check_schedule_work_hour(self):
        for record in self.sudo():
            if record.schedule_work_hour:
                strWarning = _("Schedule Hours Cannot Greater Than 24 Hours")
                if record.schedule_work_hour > 23.99:
                    raise UserError(strWarning)

    @api.constrains("date_start")
    def _check_sheet(self):
        for record in self.sudo():
            if record.date_start:
                strWarning = _(
                    "Date Start on Attendance Schedule MUST be in TIME SHEET range ..."
                )
                if (record.date < record.sheet_id.date_start) or (
                    record.date > record.sheet_id.date_end
                ):
                    raise UserError(strWarning)
