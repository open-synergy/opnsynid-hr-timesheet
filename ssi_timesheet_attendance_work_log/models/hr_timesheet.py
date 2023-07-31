# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class HRTimesheet(models.Model):
    _inherit = "hr.timesheet"

    attendance_work_log_diff = fields.Float(
        string="Attendance - Work Log",
        compute="_compute_attendance_work_log_diff",
        store=False,
    )

    def _compute_attendance_work_log_diff(self):
        for record in self:
            result = (
                record.total_attendance + record.running_attendance
            ) - record.total_work_log
            record.attendance_work_log_diff = result
