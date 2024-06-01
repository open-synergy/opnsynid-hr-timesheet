# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, fields, models
from odoo.exceptions import UserError


class HrAttendanceMachine(models.Model):
    _name = "hr.attendance.machine"
    _description = "Attendance Machine"
    _rec_name = "employee_id"

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
        string="Is Transfer",
        required=False,
        copy=False,
    )
