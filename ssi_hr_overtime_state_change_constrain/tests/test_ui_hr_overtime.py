# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

# HttpSavepointCase — BUKAN HttpCase. In 14.0, plain HttpCase does not
# set up cls.env in setUpClass; HttpSavepointCase does.
from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiHrOvertime(HttpSavepointCase):
    """Tour test for the ``hr.overtime`` state change constrain delta.

    ``base.user_admin`` is already a member of
    ``hr_overtime_validator_group`` (which implies the ``User`` group)
    via ``ssi_hr_overtime``'s ``security/res_group_data.xml``, so no
    extra group setup is needed here for the Overtimes menu or the
    Status Checks tab this module adds.
    """

    def test_create(self):
        """Run the create delta tour for ``hr.overtime``.

        IK: docs/hr_overtime/01-create.md
        """
        self.start_tour(
            "/web",
            "ssi_hr_overtime_state_change_constrain_hr_overtime_create",
            login="admin",
        )
