# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestHrLeaveSchedule(YamlTransactionCase):
    """Cover leave duration and the schedule rebuild restriction."""

    def test_hr_leave_schedule(self):
        """Run the leave duration and rebuild restriction scenarios."""
        self.run_yaml_scenario("test_data_hr_leave_schedule.yaml")
