# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from datetime import date

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestDailySummary(YamlTransactionCase):
    """Cover ``generate_daily_summary()`` on ``hr.timesheet``.

    Runs the YAML scenarios that create/regenerate/extend the daily
    summary rows of a timesheet.
    """

    def test_daily_summary(self):
        """Run the daily summary generation scenarios."""
        self.run_yaml_scenario("test_data_daily_summary.yaml")

    def _create_sheet(self, employee_name, date_start, date_end):
        """Create a bare ``hr.timesheet`` for the diff fixtures below.

        :param employee_name: name of the throwaway employee created
        :param date_start: start date of the timesheet
        :param date_end: end date of the timesheet
        :return: the created ``hr.timesheet`` record
        """
        employee = self.env["hr.employee"].create({"name": employee_name})
        working_schedule = self.env["resource.calendar"].search([], limit=1)
        return self.env["hr.timesheet"].create(
            {
                "employee_id": employee.id,
                "date_start": date_start,
                "date_end": date_end,
                "working_schedule_id": working_schedule.id,
            }
        )

    def test_get_daily_summary_diff_no_change(self):
        """Return ``{}`` when ``vals`` matches the stored summary.

        Pure Python — trigger P1 (L-01/L-02: the return value of
        ``_get_daily_summary_diff`` is asserted directly, which
        ``action: call`` discards and no YAML ``assert`` can reach
        since it is not a field stored on any record).
        """
        sheet = self._create_sheet(
            "Test Employee Diff No Change", "2024-01-01", "2024-01-01"
        )
        summary = self.env["hr.timesheet_daily_summary"].create(
            {"sheet_id": sheet.id, "date": "2024-01-01"}
        )
        vals = summary._prepare_daily_summary_vals(sheet_id=sheet, date=summary.date)
        self.assertEqual(summary._get_daily_summary_diff(vals), {})

    def test_get_daily_summary_diff_changed_date(self):
        """Report only ``date``, never ``sheet_id``, when dates differ.

        Pure Python — trigger P1 (L-01/L-02: same reasoning as above).
        This is the regression guard for the original bug: ``sheet_id``
        is a ``many2one`` naively compared as ``recordset != int``,
        which was always "different" even when nothing changed. A
        correct implementation must never report ``sheet_id`` here,
        since only ``date`` was changed.
        """
        sheet = self._create_sheet(
            "Test Employee Diff Changed Date", "2024-01-01", "2024-01-02"
        )
        summary = self.env["hr.timesheet_daily_summary"].create(
            {"sheet_id": sheet.id, "date": "2024-01-01"}
        )
        vals = summary._prepare_daily_summary_vals(sheet_id=sheet, date="2024-01-02")
        diff = summary._get_daily_summary_diff(vals)
        self.assertIn("date", diff)
        self.assertNotIn("sheet_id", diff)

    def test_prepare_daily_summary_values_dates_filter(self):
        """Restrict the built vals to the requested ``dates`` only.

        Pure Python — trigger P1 (L-01/L-02: the return value of
        ``_prepare_daily_summary_values`` is a plain list of dicts,
        which ``action: call`` discards and no YAML ``assert`` can
        reach since it is not a field stored on any record). On a
        three-day sheet, passing a single in-period date must build
        vals for exactly that date, not the full period.
        """
        admin = self.env.ref("base.user_admin")
        sheet = self._create_sheet(
            "Test Employee Prepare Values Dates", "2024-01-01", "2024-01-03"
        )
        sheet.with_user(admin).action_open()

        daily_summary_values = sheet._prepare_daily_summary_values(
            dates=[date(2024, 1, 2)]
        )

        self.assertEqual(len(daily_summary_values), 1)
        self.assertEqual(daily_summary_values[0]["date"], date(2024, 1, 2))
