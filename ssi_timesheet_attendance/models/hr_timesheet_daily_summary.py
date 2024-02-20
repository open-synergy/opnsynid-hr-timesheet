# Copyright 2023 OpenSynergy Indonesia
# Copyright 2023 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class HrTimesheetDailySummary(models.Model):
    _inherit = 'hr.timesheet_daily_summary'

    total_attendance = fields.Float(
        string="Total Attendance",
        copy=False,
    )
    total_valid_attendance = fields.Float(
        string="Total Valid Attendance",
        copy=False,
    )

    def _prepare_daily_summary_vals(self, sheet_id, date):
        vals = super(HrTimesheetDailySummary, self)._prepare_daily_summary_vals(sheet_id=sheet_id, date=date)
        total_attendance = 0
        total_valid_attendance = 0
        attendance_ids = self.env['hr.timesheet_attendance'].search([
            ('sheet_id', '=', sheet_id.id),
            ('date', '=', date),
        ])
        for attendance_id in attendance_ids:
            total_attendance += attendance_id.total_hour
            total_valid_attendance += attendance_id.total_valid_hour
        vals.update({
            'total_attendance': total_attendance,
            'total_valid_attendance': total_valid_attendance,
        })
        return vals
