# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models


class HRTimesheetAttendance(models.Model):
    _name = "hr.timesheet_attendance"
    _inherit = [
        "hr.timesheet_attendance",
        "mixin.single_operating_unit",
    ]

    @api.onchange("sheet_id")
    def onchange_operating_unit_id(self):
        if self.sheet_id:
            self.operating_unit_id = self.sheet_id.operating_unit_id
