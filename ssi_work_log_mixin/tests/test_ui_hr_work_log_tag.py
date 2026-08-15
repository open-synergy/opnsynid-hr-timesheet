# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiHrWorkLogTag(HttpSavepointCase):
    """Tour tests for the ``hr.work_log_tag`` work instructions.

    Uses ``HttpSavepointCase`` rather than plain ``HttpCase``: in 14.0
    ``TransactionCase`` only assigns ``self.env`` inside instance
    ``setUp()``, so ``cls.env`` is not available in ``setUpClass()``.
    ``HttpSavepointCase`` (via ``SingleTransactionCase``) does set
    ``cls.env`` in ``setUpClass()``, which the tours below rely on to
    seed fixture tags visible to the browser session.
    """

    @classmethod
    def setUpClass(cls):
        """Seed one fixture tag per tour.

        Pre-Condition common to every ``hr_work_log_tag`` IK: the actor
        is in group *Work Log Tags*. That group already lists
        ``base.user_admin`` in ``security/res_group_data.xml``, so no
        extra group grant is needed here.

        ``code`` (``mixin.master_data``, ``ssi_master_data_mixin``) is
        ``required=True`` with no field-level default, so every fixture
        must supply it explicitly — ``"/"`` is the SSI convention for
        "assign automatically later" (see
        ``ssi_master_data_mixin.mixin_master_data.code``'s own help text).
        """
        super().setUpClass()
        tag_model = cls.env["hr.work_log_tag"]

        # --- 02-edit.md
        cls.tag_edit = tag_model.create({"name": "TOUR-TAG-EDIT", "code": "/"})

        # --- 03-delete.md
        cls.tag_delete = tag_model.create({"name": "TOUR-TAG-DELETE", "code": "/"})

        # --- 04-deactivate.md
        cls.tag_deactivate = tag_model.create(
            {"name": "TOUR-TAG-DEACTIVATE", "code": "/"}
        )

        # --- 05-activate.md: already archived.
        cls.tag_activate = tag_model.create({"name": "TOUR-TAG-ACTIVATE", "code": "/"})
        cls.tag_activate.sudo().write({"active": False})

    def test_create(self):
        """Run the create tour for ``hr.work_log_tag``.

        IK: docs/hr_work_log_tag/01-create.md
        """
        self.start_tour(
            "/web", "ssi_work_log_mixin_hr_work_log_tag_create", login="admin"
        )

    def test_edit(self):
        """Run the edit tour for ``hr.work_log_tag``.

        IK: docs/hr_work_log_tag/02-edit.md
        """
        self.start_tour(
            "/web", "ssi_work_log_mixin_hr_work_log_tag_edit", login="admin"
        )

    def test_delete(self):
        """Run the delete tour for ``hr.work_log_tag``.

        IK: docs/hr_work_log_tag/03-delete.md
        """
        self.start_tour(
            "/web", "ssi_work_log_mixin_hr_work_log_tag_delete", login="admin"
        )

    def test_deactivate(self):
        """Run the deactivate tour for ``hr.work_log_tag``.

        IK: docs/hr_work_log_tag/04-deactivate.md
        """
        self.start_tour(
            "/web", "ssi_work_log_mixin_hr_work_log_tag_deactivate", login="admin"
        )

    def test_activate(self):
        """Run the activate tour for ``hr.work_log_tag``.

        IK: docs/hr_work_log_tag/05-activate.md
        """
        self.start_tour(
            "/web", "ssi_work_log_mixin_hr_work_log_tag_activate", login="admin"
        )
