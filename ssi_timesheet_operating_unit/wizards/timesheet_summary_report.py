# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class TimesheetSummaryReport(models.TransientModel):
    _name = "hr.timesheet_summary_report"
    _inherit = "hr.timesheet_summary_report"

    operating_unit_id = fields.Many2one(
        string="Operating Unit",
        comodel_name="operating.unit",
        help="When set, only timesheets of this operating unit are included.",
    )

    def _get_timesheet_domain(self):
        self.ensure_one()
        domain = super()._get_timesheet_domain()
        if self.operating_unit_id:
            domain.append(("operating_unit_id", "=", self.operating_unit_id.id))
        return domain
