# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestHrLeaveAllocationRequestBatchOperatingUnit(YamlTransactionCase):
    """YAML scenario tests for the operating unit glue module.

    Covers the ``operating_unit_id`` field added to
    ``hr.leave_allocation_request_batch`` by
    ``mixin.single_operating_unit``.
    """

    def test_hr_leave_allocation_request_batch_operating_unit(self):
        """Run the batch-with-operating-unit YAML scenario."""
        self.run_yaml_scenario(
            "test_data_hr_leave_allocation_request_batch_operating_unit.yaml"
        )
