# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiHrTimesheetComputationItem(HttpSavepointCase):
    """Tour tests for the ``hr.timesheet_computation_item`` work instructions.

    Uses ``HttpSavepointCase`` rather than plain ``HttpCase``: in 14.0
    ``TransactionCase`` only assigns ``self.env`` inside instance
    ``setUp()``, so ``cls.env`` is not available in ``setUpClass()``.
    ``HttpSavepointCase`` (via ``SingleTransactionCase``) does set
    ``cls.env`` in ``setUpClass()``, which the tours below rely on to
    seed computation items visible to the browser session.
    """

    @classmethod
    def setUpClass(cls):
        """Grant the configurator group and seed one item per tour.

        Pre-Condition common to every IK in this model: the actor is in
        group *Timesheet Computation Item* — without it the
        Configuration menu is never rendered for "admin" and every tour
        dies on its first step.
        """
        super().setUpClass()
        cls.env.ref("ssi_timesheet.hr_timesheet_computation_item_group").sudo().write(
            {"users": [(4, cls.env.ref("base.user_admin").id)]}
        )

        item_model = cls.env["hr.timesheet_computation_item"]

        cls.item_edit = item_model.create(
            {
                "name": "TOUR-COMP-EDIT-UI",
                "code": "TCI-EDIT",
                "python_code": "result = True",
            }
        )
        cls.item_delete = item_model.create(
            {
                "name": "TOUR-COMP-DELETE-UI",
                "code": "TCI-DELETE",
                "python_code": "result = True",
            }
        )
        cls.item_deactivate = item_model.create(
            {
                "name": "TOUR-COMP-DEACTIVATE-UI",
                "code": "TCI-DEACTIVATE",
                "python_code": "result = True",
            }
        )
        cls.item_activate = item_model.create(
            {
                "name": "TOUR-COMP-ACTIVATE-UI",
                "code": "TCI-ACTIVATE",
                "python_code": "result = True",
                "active": False,
            }
        )
        cls.item_reset_code = item_model.create(
            {
                "name": "TOUR-COMP-RESETCODE-UI",
                "code": "TCI-RESET",
                "python_code": "result = True",
            }
        )

    def test_create(self):
        """Run the create tour for ``hr.timesheet_computation_item``.

        IK: docs/hr_timesheet_computation_item/01-create.md
        """
        self.start_tour(
            "/web",
            "ssi_timesheet_hr_timesheet_computation_item_create",
            login="admin",
        )

    def test_edit(self):
        """Run the edit tour for ``hr.timesheet_computation_item``.

        IK: docs/hr_timesheet_computation_item/02-edit.md
        """
        self.start_tour(
            "/web", "ssi_timesheet_hr_timesheet_computation_item_edit", login="admin"
        )

    def test_delete(self):
        """Run the delete tour for ``hr.timesheet_computation_item``.

        IK: docs/hr_timesheet_computation_item/03-delete.md
        """
        self.start_tour(
            "/web",
            "ssi_timesheet_hr_timesheet_computation_item_delete",
            login="admin",
        )

    def test_deactivate(self):
        """Run the deactivate tour for ``hr.timesheet_computation_item``.

        IK: docs/hr_timesheet_computation_item/04-deactivate.md
        """
        self.start_tour(
            "/web",
            "ssi_timesheet_hr_timesheet_computation_item_deactivate",
            login="admin",
        )

    def test_activate(self):
        """Run the activate tour for ``hr.timesheet_computation_item``.

        IK: docs/hr_timesheet_computation_item/05-activate.md
        """
        self.start_tour(
            "/web",
            "ssi_timesheet_hr_timesheet_computation_item_activate",
            login="admin",
        )

    def test_reset_code(self):
        """Run the reset code tour for ``hr.timesheet_computation_item``.

        IK: docs/hr_timesheet_computation_item/06-reset-code.md
        """
        self.start_tour(
            "/web",
            "ssi_timesheet_hr_timesheet_computation_item_reset_code",
            login="admin",
        )
