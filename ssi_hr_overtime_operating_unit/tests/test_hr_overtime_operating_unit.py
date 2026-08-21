# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestHrOvertimeOperatingUnit(YamlTransactionCase):
    """Scenario test for the ``hr.overtime`` Operating Unit mixin."""

    def test_hr_overtime_operating_unit(self):
        """Run the Operating Unit creation scenario for ``hr.overtime``."""
        self.run_yaml_scenario("test_data_hr_overtime_operating_unit.yaml")
