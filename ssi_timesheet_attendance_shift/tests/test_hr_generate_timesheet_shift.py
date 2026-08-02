# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestHrGenerateTimesheetShift(YamlTransactionCase):
    """Cover the shift date-continuity check on the timesheet generator
    wizard (``hr.generate_timesheet``)."""

    def test_hr_generate_timesheet_shift(self):
        """Run the shift date-continuity YAML scenarios."""
        self.run_yaml_scenario("test_data_hr_generate_timesheet_shift.yaml")
