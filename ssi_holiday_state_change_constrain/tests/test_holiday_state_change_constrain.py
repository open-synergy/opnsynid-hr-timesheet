# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestHolidayStateChangeConstrain(YamlTransactionCase):
    """Scenarios covering the ``hr.leave``/``hr.leave_allocation``
    state change constrain and status check mixins."""

    def test_holiday_state_change_constrain(self):
        """Run the state change constrain scenario."""
        self.run_yaml_scenario("test_data_holiday_state_change_constrain.yaml")
