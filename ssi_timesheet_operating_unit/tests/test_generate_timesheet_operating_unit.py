# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestGenerateTimesheetOperatingUnit(YamlTransactionCase):
    """Cover operating unit propagation through the Generate Timesheet
    wizard (``hr.generate_timesheet``).
    """

    def test_generate_timesheet_operating_unit(self):
        """Run the Generate Timesheet operating unit scenario."""
        self.run_yaml_scenario("test_data_generate_timesheet_operating_unit.yaml")
