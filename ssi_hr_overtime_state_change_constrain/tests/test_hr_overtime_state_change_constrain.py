# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestHrOvertimeStateChangeConstrain(YamlTransactionCase):
    """Cover the ``hr.overtime`` State Change Constrain mixin install.

    Verifies the ``mixin.state_change_constrain`` and
    ``mixin.status_check`` inherit does not break the base
    ``hr.overtime`` creation flow.
    """

    def test_hr_overtime_state_change_constrain(self):
        """Run the "HR Overtime - State Change Constrain" scenario."""
        self.run_yaml_scenario("test_data_hr_overtime_state_change_constrain.yaml")
