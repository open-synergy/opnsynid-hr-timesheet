# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestHrAttendanceShift(YamlTransactionCase):
    """Cover CRUD, compute, and negative path of ``hr.attendance_shift``."""

    def test_hr_attendance_shift(self):
        """Run the ``hr.attendance_shift`` YAML scenarios."""
        self.run_yaml_scenario("test_data_hr_attendance_shift.yaml")
