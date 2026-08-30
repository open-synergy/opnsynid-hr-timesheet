# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestHrTimesheetAttendanceLocationLink(YamlTransactionCase):
    """Cover linking attendance coordinates to registered locations.

    Exercises ``check_in_location_id``/``check_out_location_id`` on
    ``hr.timesheet_attendance`` and the
    ``res.company.attendance_location_required`` rejection gate.
    """

    def test_hr_timesheet_attendance_location_link(self):
        """Run the attendance-location-link YAML scenario file."""
        self.run_yaml_scenario("test_data_hr_timesheet_attendance_location_link.yaml")
