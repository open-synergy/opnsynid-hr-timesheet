# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestTimesheetComputationAnalysis(YamlTransactionCase):
    """Cover ``correction_amount``/``final_amount`` on the SQL view
    report ``hr.timesheet_computation_analysis``.
    """

    def test_timesheet_computation_analysis(self):
        """Run the correction/final amount scenarios on the report."""
        self.run_yaml_scenario("test_data_timesheet_computation_analysis.yaml")
