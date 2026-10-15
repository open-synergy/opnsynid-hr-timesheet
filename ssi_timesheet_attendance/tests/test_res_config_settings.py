# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestResConfigSettings(YamlTransactionCase):
    """Cover the attendance fields of ``res.config.settings``.

    Covers the opening of the Settings form and the saving of the
    default schedule source and pattern to the company.
    """

    def test_res_config_settings(self):
        """Run the ``res.config.settings`` YAML scenarios."""
        self.run_yaml_scenario("test_data_res_config_settings.yaml")
