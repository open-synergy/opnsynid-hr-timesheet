# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestTimesheetAttendanceSchedule(YamlTransactionCase):
    """Scenario tests for ``hr.timesheet_attendance_schedule``.

    Covers sheet resolution against covering/non-covering timesheets
    and the ``res.company`` checkout buffer default.
    """

    def test_timesheet_attendance_schedule(self):
        """Run the schedule sheet-resolution and company scenarios."""
        self.run_yaml_scenario("test_data_timesheet_attendance_schedule.yaml")
