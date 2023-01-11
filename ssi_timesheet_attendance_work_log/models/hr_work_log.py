# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

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
