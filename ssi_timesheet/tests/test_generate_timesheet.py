# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestGenerateTimesheet(YamlTransactionCase):
    """Scenario tests for the ``hr.generate_timesheet`` wizard ACL."""

    def test_generate_timesheet(self):
        """Run the ACL scenario for ``hr.generate_timesheet``."""
        self.run_yaml_scenario("test_data_generate_timesheet.yaml")
