# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestHrLeaveRequestBatch(YamlTransactionCase):
    """Cover the ``hr.leave_request_batch`` document workflow."""

    def test_hr_leave_request_batch(self):
        """Run the draft to done workflow scenario of the batch."""
        self.run_yaml_scenario("test_data_hr_leave_request_batch.yaml")
