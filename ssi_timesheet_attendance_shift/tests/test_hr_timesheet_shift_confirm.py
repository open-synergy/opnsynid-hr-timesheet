# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestHrTimesheetShiftConfirm(YamlTransactionCase):
    """Cover the Shift Roster pre-confirm checks on ``hr.timesheet``."""

    def test_hr_timesheet_shift_confirm(self):
        """Run the Shift Roster confirm-lock YAML scenarios."""
        self.run_yaml_scenario("test_data_hr_timesheet_shift_confirm.yaml")
