# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import pytz

from odoo import _, fields, models
from odoo.exceptions import UserError


class HrAttendanceMachine(models.Model):
    _name = "hr.attendance.machine"
    _description = "Attendance Machine"
    _rec_name = "employee_id"
    _order = "scan_date desc, employee_id"

    pin = fields.Char(
        required=True,
        string="PIN",
    )
    scan_date = fields.Datetime(
        string="Scan Date",
    )
    verify = fields.Selection(
        string="Verify",
        selection=[
            ("finger", "1 - Finger"),
            ("rfid", "2 - RFID"),
            ("other", "3 - Other"),
        ],
        default=False,
    )
    status_scan = fields.Selection(
        string="Status",
        selection=[
            ("sign_in", "1 - Sign In"),
            ("sign_out", "2 - Sign Out"),
            ("break_in", "3 - Break In"),
            ("break_out", "4 - Break Out"),
            ("overtime_in", "4 - Lembur In"),
            ("overtime_out", "5 - Lembur Out"),
            ("meeting_in", "6 - Meeting In"),
            ("meeting_out", "7 - Meeting Out"),
            ("client_in", "8 - Klien In"),
            ("client_out", "9 - Klien Out"),
        ],
        default=False,
    )
    employee_id = fields.Many2one(
        comodel_name="hr.employee",
        string="Employee",
        required=False
    )
    device_id = fields.Char(
        string="Device ID",
    )
    is_transfer = fields.Boolean(
        string="Is Transfer?",
        required=False,
        copy=False,
        readonly=True,
    )

    def action_generate_attendances(self):
        # perlu diurutkan kembali
        attendance_machine_ids = self.search([
            ("id", "in", self.ids)
        ], order="employee_id, scan_date asc")
        for rec in attendance_machine_ids:
            if not rec.scan_date or rec.status_scan not in ("sign_in", "sign_out"):
                continue
            tz = pytz.timezone(rec.employee_id.tz or "Asia/Jakarta")
            current_datetime = pytz.utc.localize(rec.scan_date).astimezone(tz)
            current_date = current_datetime.date()
            criteria = [
                ("company_id", "=", rec.employee_id.company_id.id),
                ("employee_id", "=", rec.employee_id.id),
                ("state", "=", "open"),
                ("date_start", "<=", current_date),
                ("date_end", ">=", current_date),
            ]
            timesheet_id = self.env["hr.timesheet"].search(criteria, limit=1)
            if not timesheet_id:
                raise UserError(_(f"Timesheet for employee {rec.employee_id.display_name} not found."))
            attendance_obj = self.env["hr.timesheet_attendance"]
            attendance_reason_obj = self.env["hr.attendance_reason"]
            reason_in_id = attendance_reason_obj.search([
                ("code", "=", "SYS-IN")
            ], limit=1)
            reason_out_id = attendance_reason_obj.search([
                ("code", "=", "SYS-OUT")
            ], limit=1)
            attendance_vals = {
                "sheet_id": timesheet_id.id,
                "employee_id": rec.employee_id.id,
            }
            if rec.status_scan == "sign_in":
                attendance_vals.update({
                    "date": current_date,
                    "check_in": rec.scan_date,
                })
                attendance_obj.create(attendance_vals)
            elif rec.status_scan == "sign_out":
                latest_attendance_id = rec.employee_id.latest_attendance_id
                _check = 0
                checkout_buffer = 0
                if latest_attendance_id:
                    check_out = rec.scan_date
                    if latest_attendance_id.date != current_date:
                        schedule = latest_attendance_id.schedule_id
                        schedule_check_out = schedule.date_end
                        _check = (check_out - schedule_check_out).total_seconds() / 3600.0
                        company = self.env.company
                        checkout_buffer = company.checkout_buffer
                if not latest_attendance_id or (_check > checkout_buffer):
                    attendance_vals.update({
                        "date": current_date,
                        "check_in": rec.scan_date,
                        "check_out": rec.scan_date,
                        "reason_check_in_id": reason_in_id.id,
                        "reason_check_out_id": reason_out_id.id,
                    })
                    attendance_obj.create(attendance_vals)
                else:
                    attendance_vals.update({
                        "check_out": rec.scan_date,
                    })
                    latest_attendance_id.write(attendance_vals)
            rec.write({"is_transfer": True})

    def _cron_generate_attendances(self):
        attendance_machine_ids = self.env["hr.attendance.machine"].search([
            ("is_transfer", "=", False)
        ])
        attendance_machine_ids.action_generate_attendances()
