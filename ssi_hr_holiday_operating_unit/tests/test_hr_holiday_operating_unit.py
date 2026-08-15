# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestHrHolidayOperatingUnit(YamlTransactionCase):
    """YAML scenario tests for the ``ssi_hr_holiday_operating_unit`` glue.

    Covers the ``operating_unit_id`` field added to ``hr.leave`` by
    ``mixin.single_operating_unit``.
    """

    def test_hr_holiday_operating_unit(self):
        """Run the leave-with-operating-unit YAML scenario."""
        self.run_yaml_scenario("test_data_hr_holiday_operating_unit.yaml")
