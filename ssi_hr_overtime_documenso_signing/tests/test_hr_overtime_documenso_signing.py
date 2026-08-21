# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestHrOvertimeDocumensoSigning(YamlTransactionCase):
    """Cover the ``hr.overtime`` Documenso signing mixin installation.

    Verifies the ``mixin.documenso_signing_approval`` inherit does not
    break the base ``hr.overtime`` creation flow.
    """

    def test_hr_overtime_documenso_signing(self):
        """Run the "HR Overtime - Documenso Signing Mixin" scenario."""
        self.run_yaml_scenario("test_data_hr_overtime_documenso_signing.yaml")
