# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiHrOvertimeBatch(HttpSavepointCase):
    """Tour test for the create-delta work instruction added by
    ``ssi_hr_overtime_batch_operating_unit`` (the Operating Unit
    field) on ``hr.overtime_batch``.

    Uses ``HttpSavepointCase`` rather than plain ``HttpCase``: in 14.0
    ``TransactionCase`` only assigns ``self.env`` inside instance
    ``setUp()``, so ``cls.env`` is not available in ``setUpClass()``.
    ``HttpSavepointCase`` (via ``SingleTransactionCase``) does set
    ``cls.env`` in ``setUpClass()``.
    """

    @classmethod
    def setUpClass(cls):
        """Grant the Multi Operating Unit group so the field is shown.

        Pre-Condition common to ``01-create.md``'s ``Additional
        Fields`` delta: the actor must belong to
        ``operating_unit.group_multi_operating_unit`` for the
        Operating Unit field to be visible on the create form.
        """
        super().setUpClass()
        cls.env.ref("operating_unit.group_multi_operating_unit").sudo().write(
            {"users": [(4, cls.env.ref("base.user_admin").id)]}
        )

    def test_create(self):
        """Run the create-delta tour for ``hr.overtime_batch``.

        IK: docs/hr_overtime_batch/01-create.md
        """
        self.start_tour(
            "/web",
            "ssi_hr_overtime_batch_operating_unit_hr_overtime_batch_create",
            login="admin",
        )
