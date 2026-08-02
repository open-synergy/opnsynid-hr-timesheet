# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestHrAttendanceShiftAssignment(YamlTransactionCase):
    """Cover CRUD and negative path of ``hr.attendance_shift_assignment``."""

    def test_hr_attendance_shift_assignment(self):
        """Run the ``hr.attendance_shift_assignment`` YAML scenarios."""
        self.run_yaml_scenario("test_data_hr_attendance_shift_assignment.yaml")
