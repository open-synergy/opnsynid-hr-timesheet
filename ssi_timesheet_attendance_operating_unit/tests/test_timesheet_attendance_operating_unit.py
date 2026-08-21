# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestTimesheetAttendanceOperatingUnit(YamlTransactionCase):
    """Test Operating Unit ownership on ``hr.timesheet_attendance``.

    Covers creating an attendance record with an explicit Operating
    Unit, and the ``onchange_operating_unit_id`` auto-fill from the
    linked timesheet ``sheet_id``.
    """

    def test_timesheet_attendance_operating_unit(self):
        """Run the Operating Unit scenarios for attendance records."""
        self.run_yaml_scenario("test_data_timesheet_attendance_operating_unit.yaml")
