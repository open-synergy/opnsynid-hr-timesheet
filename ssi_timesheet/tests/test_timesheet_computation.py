# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestTimesheetComputation(YamlTransactionCase):
    """Cover ``correction_amount``/``final_amount`` on
    ``hr.timesheet_computation`` and the in-place reconciliation of
    ``_reload_timesheet_computation``.
    """

    def test_timesheet_computation(self):
        """Run the correction/final amount reconciliation scenarios."""
        self.run_yaml_scenario("test_data_timesheet_computation.yaml")
