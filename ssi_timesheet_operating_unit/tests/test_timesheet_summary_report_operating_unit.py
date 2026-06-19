# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestTimesheetSummaryReportOperatingUnit(YamlTransactionCase):
    def _create_done_timesheet(self, name, date_start, date_end, item, operating_unit):
        admin = self.env.ref("base.user_admin")
        employee = self.env["hr.employee"].create(
            {
                "name": name,
                "timesheet_computation_ids": [(6, 0, item.ids)],
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
                    "operating_unit_id": operating_unit.id,
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
        return timesheet

    def test_operating_unit_filter(self):
        """When operating_unit_id is set, only that OU's timesheets are kept."""
        operating_units = self.env["operating.unit"].search([], limit=2)
        self.assertEqual(
            len(operating_units), 2, "Need at least two operating units for this test."
        )
        ou_a, ou_b = operating_units[0], operating_units[1]
        item = self.env["hr.timesheet_computation_item"].create(
            {
                "name": "OU Count",
                "code": "TSUM_OU",
                "python_code": "result = 1.0",
            }
        )
        ts_a = self._create_done_timesheet(
            "RPT OU A", "2024-06-01", "2024-06-30", item, ou_a
        )
        ts_b = self._create_done_timesheet(
            "RPT OU B", "2024-07-01", "2024-07-31", item, ou_b
        )

        wizard = self.env["hr.timesheet_summary_report"].create(
            {
                "date_start": "2024-01-01",
                "date_end": "2024-12-31",
                "operating_unit_id": ou_a.id,
            }
        )
        timesheets = wizard._get_timesheets()
        self.assertIn(ts_a, timesheets)
        self.assertNotIn(ts_b, timesheets)

    def test_no_operating_unit_filter_keeps_all(self):
        """Without operating_unit_id the domain ignores the OU criterion."""
        operating_units = self.env["operating.unit"].search([], limit=2)
        self.assertEqual(len(operating_units), 2)
        ou_a, ou_b = operating_units[0], operating_units[1]
        item = self.env["hr.timesheet_computation_item"].create(
            {
                "name": "OU Count All",
                "code": "TSUM_OU_ALL",
                "python_code": "result = 1.0",
            }
        )
        ts_a = self._create_done_timesheet(
            "RPT OU All A", "2024-08-01", "2024-08-31", item, ou_a
        )
        ts_b = self._create_done_timesheet(
            "RPT OU All B", "2024-09-01", "2024-09-30", item, ou_b
        )

        wizard = self.env["hr.timesheet_summary_report"].create(
            {"date_start": "2024-01-01", "date_end": "2024-12-31"}
        )
        timesheets = wizard._get_timesheets()
        self.assertIn(ts_a, timesheets)
        self.assertIn(ts_b, timesheets)
