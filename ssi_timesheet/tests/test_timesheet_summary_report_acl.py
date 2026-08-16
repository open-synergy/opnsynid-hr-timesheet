# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestTimesheetSummaryReportAcl(YamlTransactionCase):
    """Scenario tests for the ``hr.timesheet_summary_report`` wizard ACL."""

    def test_timesheet_summary_report_acl(self):
        """Run the ACL scenario for ``hr.timesheet_summary_report``."""
        self.run_yaml_scenario("test_data_timesheet_summary_report_acl.yaml")
