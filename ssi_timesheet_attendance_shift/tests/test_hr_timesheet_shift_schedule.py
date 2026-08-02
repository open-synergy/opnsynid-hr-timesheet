# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from datetime import date

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestHrTimesheetShiftSchedule(YamlTransactionCase):
    """Cover shift-roster schedule generation on ``hr.timesheet``."""

    def test_hr_timesheet_shift_schedule(self):
        """Run the shift-roster schedule generator YAML scenarios."""
        self.run_yaml_scenario("test_data_hr_timesheet_shift_schedule.yaml")

    def test_get_shift_for_date_returns_matching_shift(self):
        """Assert the recordset ``_get_shift_for_date`` returns.

        Pure Python — trigger P1 (the value under test is the
        method's return value, not a side effect it leaves on a
        stored record), grounded in L-01 (``action: call`` discards
        whatever a method returns) and L-02 (the actual side of every
        YAML assert is always a dotted ``getattr`` on a record
        already sitting in the registry, so a bare recordset that is
        never stored anywhere cannot be compared at all).
        """
        obj_shift = self.env["hr.attendance_shift"]
        obj_pattern = self.env["hr.attendance_shift_pattern"]
        obj_assignment = self.env["hr.attendance_shift_assignment"]
        obj_employee = self.env["hr.employee"]
        obj_timesheet = self.env["hr.timesheet"]

        day_shift = obj_shift.create(
            {
                "name": "P1 Day Shift",
                "code": "/",
                "hour_start": 8.0,
                "duration": 8.0,
            }
        )
        pattern = obj_pattern.create(
            {
                "name": "P1 Pattern",
                "code": "/",
                "cycle_length": 2,
                "date_anchor": date(2024, 5, 1),
                "detail_ids": [
                    (0, 0, {"day_index": 1, "shift_id": day_shift.id}),
                    (0, 0, {"day_index": 2}),
                ],
            }
        )
        employee = obj_employee.create({"name": "P1 Employee", "tz": "UTC"})
        employee_no_assignment = obj_employee.create(
            {"name": "P1 Employee Without Assignment", "tz": "UTC"}
        )
        obj_assignment.create(
            {
                "employee_id": employee.id,
                "pattern_id": pattern.id,
                "cycle_offset": 0,
                "date_start": date(2024, 5, 1),
            }
        )
        timesheet = obj_timesheet.new({})

        shift_on_day = timesheet._get_shift_for_date(employee, date(2024, 5, 1))
        shift_on_off_day = timesheet._get_shift_for_date(employee, date(2024, 5, 2))
        shift_without_assignment = timesheet._get_shift_for_date(
            employee_no_assignment, date(2024, 5, 1)
        )

        self.assertEqual(shift_on_day, day_shift)
        self.assertFalse(shift_on_off_day)
        self.assertFalse(shift_without_assignment)
