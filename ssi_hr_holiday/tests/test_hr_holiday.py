# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestHrHoliday(YamlTransactionCase):
    """Cover ``hr.leave`` and ``hr.leave_allocation`` CRUD and rules."""

    def test_hr_holiday(self):
        """Run the ``hr.leave``/``hr.leave_allocation`` YAML scenario."""
        self.run_yaml_scenario("test_data_hr_holiday.yaml")
