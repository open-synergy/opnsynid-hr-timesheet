# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models


class HRWorkLog(models.Model):
    _name = "hr.work_log"
    _inherit = [
        "hr.work_log",
    ]

    @api.onchange("sheet_id")
    def onchange_amount(self):
        if self.sheet_id:
            self.amount = self.sheet_id.attendance_work_log_diff

    @api.model
    def create(self, values):
        res = super(HRWorkLog, self).create(values)
        res.sheet_id.generate_daily_summary()
        return res

    def write(self, values):
        res = super(HRWorkLog, self).write(values)
        for rec in self:
            if 'date' in values or 'amount' in values:
                rec.sheet_id.generate_daily_summary()
        return res
