# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestTimesheetSummaryReport(YamlTransactionCase):
    def _create_item(self, name, code, result):
        return self.env["hr.timesheet_computation_item"].create(
            {
                "name": name,
                "code": code,
                "python_code": "result = %s" % result,
            }
        )

    def _create_done_timesheet(self, name, date_start, date_end, items):
        admin = self.env.ref("base.user_admin")
        employee = self.env["hr.employee"].create(
            {
                "name": name,
                "timesheet_computation_ids": [(6, 0, items.ids)],
            }
        )
        calendar = self.env["resource.calendar"].search([], limit=1)
        timesheet = (
            self.env["hr.timesheet"]
            .with_user(admin)
            .create(
                {
                    "employee_id": employee.id,
                    "date_start": date_start,
                    "date_end": date_end,
                    "working_schedule_id": calendar.id,
                }
            )
        )
        timesheet.with_user(admin).action_open()
        timesheet.with_user(admin).with_context(
            bypass_policy_check=True
        ).action_confirm()
        timesheet.with_user(admin).with_context(
            bypass_policy_check=True
        ).action_approve_approval()
        return timesheet, employee

    def test_get_timesheets_filters_done_and_range(self):
        """Wizard only collects done timesheets inside the selected range."""
        item = self._create_item("Report Count", "TSUM_CNT", 5.0)
        ts_in, _emp = self._create_done_timesheet(
            "RPT Emp In", "2024-03-01", "2024-03-31", item
        )
        self.assertEqual(ts_in.state, "done")
        ts_out, _emp_out = self._create_done_timesheet(
            "RPT Emp Out", "2025-01-01", "2025-01-31", item
        )
        wizard = self.env["hr.timesheet_summary_report"].create(
            {"date_start": "2024-01-01", "date_end": "2024-12-31"}
        )
        timesheets = wizard._get_timesheets()
        self.assertIn(ts_in, timesheets)
        self.assertNotIn(ts_out, timesheets)

    def test_dynamic_columns_and_aggregation(self):
        """Columns are built from the items present; amounts sum per employee."""
        item_a = self._create_item("Count A", "TSUM_A", 3.0)
        item_b = self._create_item("Count B", "TSUM_B", 7.0)
        items = item_a + item_b
        timesheet, employee = self._create_done_timesheet(
            "RPT Emp XLSX", "2024-04-01", "2024-04-30", items
        )
        report = self.env["report.ssi_timesheet.timesheet_summary_xlsx"]

        columns = report._get_computation_items(timesheet)
        self.assertEqual(set(columns.ids), set(items.ids))

        amounts = report._get_amounts_by_employee(timesheet)
        self.assertEqual(amounts[employee.id][item_a.id], 3.0)
        self.assertEqual(amounts[employee.id][item_b.id], 7.0)

    def test_render_xlsx_produces_workbook(self):
        """The full xlsx render returns a valid (zip/xlsx) binary."""
        item = self._create_item("Count R", "TSUM_R", 2.0)
        self._create_done_timesheet("RPT Emp Render", "2024-05-01", "2024-05-31", item)
        wizard = self.env["hr.timesheet_summary_report"].create(
            {"date_start": "2024-01-01", "date_end": "2024-12-31"}
        )
        report = self.env.ref("ssi_timesheet.action_report_timesheet_summary_xlsx")
        content, ext = report._render_xlsx(wizard.ids, data={"wizard_id": wizard.id})
        self.assertEqual(ext, "xlsx")
        self.assertTrue(content)
        self.assertEqual(content[:2], b"PK")
