# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class TimesheetSummaryReport(models.TransientModel):
    _name = "hr.timesheet_summary_report"
    _description = "Timesheet Summary Report"

    date_start = fields.Date(
        string="Date Start",
        required=True,
        help="Only timesheets starting on or after this date are included.",
    )
    date_end = fields.Date(
        string="Date End",
        required=True,
        help="Only timesheets ending on or before this date are included.",
    )

    def _get_timesheet_domain(self):
        self.ensure_one()
        return [
            ("state", "=", "done"),
            ("date_start", ">=", self.date_start),
            ("date_end", "<=", self.date_end),
        ]

    def _get_timesheets(self):
        self.ensure_one()
        return self.env["hr.timesheet"].search(
            self._get_timesheet_domain(),
            order="employee_id, date_start",
        )

    def action_export_xlsx(self):
        self.ensure_one()
        report = self.env.ref("ssi_timesheet.action_report_timesheet_summary_xlsx")
        return report.report_action(self, data={"wizard_id": self.id})
