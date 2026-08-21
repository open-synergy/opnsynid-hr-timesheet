# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models


class HrTimesheetAttendance(models.Model):
    """Adds Operating Unit ownership to timesheet attendance records.

    Restricts each attendance record to a single operating unit via
    ``mixin.single_operating_unit``, enabling operating unit based
    visibility and security rules for the document. The field
    auto-fills from the linked ``sheet_id`` (see
    ``onchange_operating_unit_id``) instead of only the current user's
    default operating unit.
    """

    _name = "hr.timesheet_attendance"
    _inherit = [
        "hr.timesheet_attendance",
        "mixin.single_operating_unit",
    ]

    @api.onchange("sheet_id")
    def onchange_operating_unit_id(self):
        if self.sheet_id:
            self.operating_unit_id = self.sheet_id.operating_unit_id
