# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestHrGenerateTimesheetShift(YamlTransactionCase):
    """Cover the shift date-continuity check on the timesheet generator
    wizard (``hr.generate_timesheet``), and the flow of the schedule
    source from the company and the employee into the timesheet."""

    def test_hr_generate_timesheet_shift(self):
        """Run the shift date-continuity YAML scenarios."""
        self.run_yaml_scenario("test_data_hr_generate_timesheet_shift.yaml")

    def test_schedule_source_selection_has_shift(self):
        """Assert the three schedule sources exist with this module.

        Pure Python — trigger P1 (the value under test is the return
        value of ``fields_get()``, not a side effect on a stored
        record), grounded in L-01 (``action: call`` discards whatever
        a method returns). ``ssi_timesheet_attendance`` offers
        ``working_schedule`` and ``pattern``; this module adds
        ``shift`` to the timesheet, the employee and the company.
        """
        expected = ["working_schedule", "pattern", "shift"]
        for model in ("hr.timesheet", "hr.employee", "res.company"):
            field = (
                "default_schedule_source"
                if model == "res.company"
                else "schedule_source"
            )
            selection = self.env[model].fields_get([field])[field]["selection"]
            self.assertEqual(sorted(key for key, _label in selection), sorted(expected))
