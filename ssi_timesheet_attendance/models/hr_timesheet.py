# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from datetime import datetime

import pytz

from odoo import _, api, fields, models
from odoo.exceptions import UserError
from odoo.tools import format_datetime


class HRTimesheet(models.Model):
    _inherit = "hr.timesheet"

    @api.depends(
        "attendance_ids",
        "attendance_ids.check_in",
        "attendance_ids.check_out",
    )
    def _compute_total_attendance(self):
        for sheet in self:
            sheet.total_attendance = 0.0
            for attendance in sheet.attendance_ids:
                sheet.total_attendance += attendance.total_hour

    working_schedule_id = fields.Many2one(
        string="Working Schedule",
        comodel_name="resource.calendar",
        required=True,
        readonly=True,
        states={
            "draft": [("readonly", False)],
        },
    )
    total_attendance = fields.Float(
        string="Total Attendance",
        compute="_compute_total_attendance",
        store=True,
    )
    attendance_ids = fields.One2many(
        string="Attendances",
        comodel_name="hr.timesheet_attendance",
        inverse_name="sheet_id",
        readonly=True,
        states={
            "open": [
                ("readonly", False),
            ],
        },
    )

    @api.depends("attendance_ids")
    def _compute_latest_attendance_id(self):
        for record in self:
            result = False
            if record.attendance_ids:
                result = record.attendance_ids[0]
            record.latest_attendance_id = result

    latest_attendance_id = fields.Many2one(
        string="Latest Attedance",
        comodel_name="hr.timesheet_attendance",
        compute="_compute_latest_attendance_id",
        store=True,
    )
    attendance_status = fields.Selection(
        string="Attendance Status",
        selection=[
            ("sign_in", "Sign In"),
            ("sign_out", "Sign Out"),
        ],
        related="employee_id.attendance_status",
    )
    schedule_ids = fields.One2many(
        string="Attendance Schedule",
        comodel_name="hr.timesheet_attendance_schedule",
        inverse_name="sheet_id",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
            "open": [
                ("readonly", False),
            ],
        },
    )

    def _prepare_schedule_data(self, start, stop):
        self.ensure_one()
        pytz.timezone(self.env.user.tz)
        start_conv_dt = fields.Datetime.to_string(start.astimezone(pytz.UTC))
        stop_conv_dt = fields.Datetime.to_string(stop.astimezone(pytz.UTC))
        return {
            "date_start": start_conv_dt,
            "date_end": stop_conv_dt,
            "employee_id": self.employee_id.id,
        }

    def _get_schedule_data(self):
        self.ensure_one()
        res = []
        obj_public_holiday = self.env["base.public.holiday"]
        if self.working_schedule_id and self.date_start and self.date_end:
            start_dt = datetime.combine(self.date_start, datetime.min.time())
            end_dt = datetime.combine(self.date_end, datetime.max.time())
            tz = pytz.timezone(self.env.user.tz)
            if not start_dt.tzinfo:
                start_dt = start_dt.replace(tzinfo=tz)
            if not end_dt.tzinfo:
                end_dt = end_dt.replace(tzinfo=tz)
            resource = self.employee_id.resource_id
            schedule_ids = self.working_schedule_id._attendance_intervals_batch(
                start_dt=start_dt,
                end_dt=end_dt,
                resources=resource,
            )[resource.id]
            if schedule_ids:
                for start, stop, _res in schedule_ids:
                    if not obj_public_holiday.is_public_holiday(start):
                        schedule_data = self._prepare_schedule_data(start, stop)
                        res.append((0, 0, schedule_data))
        return res

    @api.onchange(
        "employee_id",
    )
    def onchange_working_schedule_id(self):
        self.working_schedule_id = False
        if self.employee_id:
            self.working_schedule_id = self.employee_id.resource_calendar_id

    def action_compute_schedule(self):
        for document in self.sudo():
            data = []
            document.schedule_ids.unlink()
            data = document._get_schedule_data()
            document.write({"schedule_ids": data})
            document.attendance_ids._compute_schedule()
            document.schedule_ids._compute_attendance()

    @api.constrains(
        "employee_id",
        "date_start",
    )
    def _check_overlap_date_start(self):
        for record in self:
            if record.employee_id and record.date_start:
                criteria = [
                    ("employee_id", "=", record.employee_id.id),
                    ("id", "<>", record.id),
                    ("date_start", "<=", record.date_start),
                    ("date_end", ">=", record.date_start),
                ]
                check = self.search(criteria)
                if len(check) > 0:
                    strWarning = _("Date start with the same employee can't overlap")
                    raise UserError(strWarning)

    @api.constrains(
        "employee_id",
        "date_end",
    )
    def _check_overlap_date_end(self):
        for record in self:
            if record.employee_id and record.date_end:
                criteria = [
                    ("employee_id", "=", record.employee_id.id),
                    ("id", "<>", record.id),
                    ("date_start", "<=", record.date_end),
                    ("date_end", ">=", record.date_end),
                ]
                check = self.search(criteria)
                if len(check) > 0:
                    strWarning = _("Date end with the same employee can't overlap")
                    raise UserError(strWarning)

    def action_sign_in(self, reason=False):
        for record in self.sudo():
            record._sign_in(reason=reason)

    def action_sign_out(self, reason=False):
        for record in self.sudo():
            record._sign_out(reason=reason)

    def _sign_in(self, reason=False):
        self.ensure_one()
        Attendance = self.env["hr.timesheet_attendance"]
        Attendance.create(self._prepare_attendance_data_creation(reason))

    def _prepare_attendance_data_creation(self, reason=False):
        conv_dt = format_datetime(
            self.env, fields.Datetime.now(), dt_format="yyyy-MM-dd"
        )
        value = {
            "date": conv_dt,
            "employee_id": self.employee_id.id,
            "check_in": fields.Datetime.now(),
            "reason_check_in_id": reason and reason.id or False,
            "sheet_id": self.id,
        }
        return value

    def _get_system_reason_out(self):
        self.ensure_one()
        if self.env.company.check_out_reason_id:
            return self.env.company.check_out_reason_id.id
        else:
            return self.env.ref(
                "ssi_timesheet_attendance.hr_attendance_reason_check_out"
            ).id

    def _get_system_reason_in(self):
        self.ensure_one()
        if self.env.company.check_in_reason_id:
            return self.env.company.check_in_reason_id.id
        else:
            return self.env.ref(
                "ssi_timesheet_attendance.hr_attendance_reason_check_in"
            ).id

    def _prepare_attendance_data_uncommon(self):
        self.ensure_one()
        conv_dt = format_datetime(
            self.env, fields.Datetime.now(), dt_format="yyyy-MM-dd"
        )
        value = {
            "date": conv_dt,
            "employee_id": self.employee_id.id,
            "check_in": fields.Datetime.now(),
            "check_out": fields.Datetime.now(),
            "reason_check_in_id": self._get_system_reason_in(),
            "reason_check_out_id": self._get_system_reason_out(),
            "sheet_id": self.id,
        }
        return value

    def _sign_out(self, reason=False):
        self.ensure_one()
        Attendance = self.env["hr.timesheet_attendance"]
        latest_attendance_id = self.employee_id.latest_attendance_id
        if latest_attendance_id:
            check_out = fields.Datetime.now()
            schedule = latest_attendance_id.schedule_id
            schedule_check_out = schedule.date_end
            _check = (check_out - schedule_check_out).total_seconds() / 3600.0
            company = self.env.company
            checkout_buffer = company.checkout_buffer
            if _check > checkout_buffer:
                Attendance.create(self._prepare_attendance_data_uncommon())
            else:
                self.employee_id.latest_attendance_id.write(
                    self._prepare_attendance_data_update(reason=reason)
                )

    def _prepare_attendance_data_update(self, reason=False):
        self.ensure_one()
        return {
            "check_out": fields.Datetime.now(),
            "reason_check_out_id": reason and reason.id or False,
        }

    def _prepare_domain_sign_out(self):
        self.ensure_one()
        criteria = [
            ("sheet_id", "=", self.employee_id.active_timesheet_id.id),
            ("date", "=", fields.Date.today()),
            ("check_out", "=", False),
        ]
        return criteria

    def unlink(self):
        _super = super(HRTimesheet, self)
        schedule_ids = self.mapped("schedule_ids")
        if schedule_ids:
            schedule_ids.unlink()
        return _super.unlink()
