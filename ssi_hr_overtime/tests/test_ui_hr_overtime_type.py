# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiHrOvertimeType(HttpSavepointCase):
    """Tour tests for the ``hr.overtime_type`` work instructions.

    Uses ``HttpSavepointCase`` rather than plain ``HttpCase``: in 14.0
    ``TransactionCase`` only assigns ``self.env`` inside instance
    ``setUp()``, so ``cls.env`` is not available in ``setUpClass()``.
    ``HttpSavepointCase`` (via ``SingleTransactionCase``) does set
    ``cls.env`` in ``setUpClass()``, which the tours below rely on to
    seed overtime type records visible to the browser session.

    No group grant is needed here: ``ssi_hr_overtime``'s own demo data
    (``security/res_group_data.xml``) already adds ``base.user_admin``
    to ``hr_overtime_type_group``.
    """

    @classmethod
    def setUpClass(cls):
        """Seed one overtime type fixture per state-changing tour."""
        super().setUpClass()
        overtime_type_model = cls.env["hr.overtime_type"]

        # --- 02-edit.md
        cls.type_edit = overtime_type_model.create(
            {"name": "TOUR-OTTYPE-EDIT", "code": "/"}
        )

        # --- 03-delete.md
        cls.type_delete = overtime_type_model.create(
            {"name": "TOUR-OTTYPE-DELETE", "code": "/"}
        )

        # --- 04-deactivate.md
        cls.type_deactivate = overtime_type_model.create(
            {"name": "TOUR-OTTYPE-DEACTIVATE", "code": "/"}
        )

        # --- 05-activate.md — already archived.
        cls.type_activate = overtime_type_model.create(
            {"name": "TOUR-OTTYPE-ACTIVATE", "code": "/", "active": False}
        )

    def test_create(self):
        """Run the create tour for ``hr.overtime_type``.

        IK: docs/hr_overtime_type/01-create.md
        """
        self.start_tour(
            "/web", "ssi_hr_overtime_hr_overtime_type_create", login="admin"
        )

    def test_edit(self):
        """Run the edit tour for ``hr.overtime_type``.

        IK: docs/hr_overtime_type/02-edit.md
        """
        self.start_tour("/web", "ssi_hr_overtime_hr_overtime_type_edit", login="admin")

    def test_delete(self):
        """Run the delete tour for ``hr.overtime_type``.

        IK: docs/hr_overtime_type/03-delete.md
        """
        self.start_tour(
            "/web", "ssi_hr_overtime_hr_overtime_type_delete", login="admin"
        )

    def test_deactivate(self):
        """Run the deactivate tour for ``hr.overtime_type``.

        IK: docs/hr_overtime_type/04-deactivate.md
        """
        self.start_tour(
            "/web", "ssi_hr_overtime_hr_overtime_type_deactivate", login="admin"
        )

    def test_activate(self):
        """Run the activate tour for ``hr.overtime_type``.

        IK: docs/hr_overtime_type/05-activate.md
        """
        self.start_tour(
            "/web", "ssi_hr_overtime_hr_overtime_type_activate", login="admin"
        )
