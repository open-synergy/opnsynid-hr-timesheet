# Copyright 2023 OpenSynergy Indonesia
# Copyright 2023 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class HrTimesheetDailySummary(models.Model):
    _inherit = 'hr.timesheet_daily_summary'

    total_work_log = fields.Float(
        string="Total Work Log",
        copy=False,
    )

    def _prepare_daily_summary_vals(self, sheet_id, date):
        vals = super(HrTimesheetDailySummary, self)._prepare_daily_summary_vals(sheet_id=sheet_id, date=date)
        total_work_log = 0
        work_log_ids = self.env['hr.work_log'].search([
            ('sheet_id', '=', sheet_id.id),
            ('date', '=', date),
            ('state', 'not in', ['cancel', 'reject']),
        ])
        for work_log_id in work_log_ids:
            total_work_log += work_log_id.amount
        vals.update({
            'total_work_log': total_work_log,
        })
        return vals
