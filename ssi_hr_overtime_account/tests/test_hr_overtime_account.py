# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestHrOvertimeAccount(YamlTransactionCase):
    """Test analytic account selection on ``hr.overtime``.

    Covers both ``fixed`` and ``python`` analytic account selection
    methods configured on ``hr.overtime_type``.
    """

    def test_hr_overtime_account(self):
        """Run the analytic account selection scenario."""
        self.run_yaml_scenario("test_data_hr_overtime_account.yaml")
