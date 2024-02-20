# Copyright 2023 OpenSynergy Indonesia
# Copyright 2023 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class HrTimesheetDailySummary(models.Model):
    _name = "hr.timesheet_daily_summary"
    _description = "HR Timesheet Daily Summary"
    _rec_name = "date"
    _order = "date"

    sheet_id = fields.Many2one(
        string="# Sheet",
        comodel_name="hr.timesheet",
        required=True,
        ondelete="cascade",
    )
    date = fields.Date(
        string='Date',
        required=True
    )

    def _prepare_daily_summary_vals(self, sheet_id, date):
        vals = {
            'sheet_id': sheet_id.id,
            'date': date,
        }
        return vals
