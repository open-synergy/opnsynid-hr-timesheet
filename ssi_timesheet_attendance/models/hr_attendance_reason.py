# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class HrAttendanceReason(models.Model):
    _name = "hr.attendance_reason"
    _inherit = ["mixin.master_data"]
    _description = "Attendance Reason"

    name = fields.Char(
        string="Reason",
    )
