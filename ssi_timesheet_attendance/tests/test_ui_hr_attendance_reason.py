# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiHrAttendanceReason(HttpSavepointCase):
    """Tour tests for the ``hr.attendance_reason`` work instructions.

    Uses ``HttpSavepointCase`` rather than plain ``HttpCase``: in 14.0
    ``TransactionCase`` only assigns ``self.env`` inside instance
    ``setUp()``, so ``cls.env`` is not available in ``setUpClass()``.
    ``HttpSavepointCase`` (via ``SingleTransactionCase``) does set
    ``cls.env`` in ``setUpClass()``, which the tours below rely on to
    seed reasons visible to the browser session.
    """

    @classmethod
    def setUpClass(cls):
        """Grant the configurator group and seed one reason per tour.

        Pre-Condition common to every ``hr_attendance_reason`` IK: the
        actor is in group *Attendance Reason* — without it the
        Attendance Reasons menu is never rendered for "admin" and every
        tour dies on its first step. The group is already granted to
        ``admin`` by this module's own security data
        (``security/res_group_data.xml``); the explicit grant below is
        defensive and mirrors the pattern used by every other tour suite
        in this repo.
        """
        super().setUpClass()
        cls.env.ref("ssi_timesheet_attendance.hr_attendance_reason_group").sudo().write(
            {"users": [(4, cls.env.ref("base.user_admin").id)]}
        )

        reason_model = cls.env["hr.attendance_reason"]

        cls.reason_edit = reason_model.create(
            {
                "name": "TOUR-REASON-EDIT-UI",
                "code": "REASON-EDIT",
            }
        )
        cls.reason_delete = reason_model.create(
            {
                "name": "TOUR-REASON-DELETE-UI",
                "code": "REASON-DELETE",
            }
        )
        cls.reason_deactivate = reason_model.create(
            {
                "name": "TOUR-REASON-DEACTIVATE-UI",
                "code": "REASON-DEACT",
            }
        )
        cls.reason_activate = reason_model.create(
            {
                "name": "TOUR-REASON-ACTIVATE-UI",
                "code": "REASON-ACT",
                "active": False,
            }
        )
        cls.reason_reset_code = reason_model.create(
            {
                "name": "TOUR-REASON-RESETCODE-UI",
                "code": "REASON-RESET",
            }
        )

    def test_create(self):
        """Run the create tour for ``hr.attendance_reason``.

        IK: docs/hr_attendance_reason/01-create.md
        """
        self.start_tour(
            "/web",
            "ssi_timesheet_attendance_hr_attendance_reason_create",
            login="admin",
        )

    def test_edit(self):
        """Run the edit tour for ``hr.attendance_reason``.

        IK: docs/hr_attendance_reason/02-edit.md
        """
        self.start_tour(
            "/web",
            "ssi_timesheet_attendance_hr_attendance_reason_edit",
            login="admin",
        )

    def test_delete(self):
        """Run the delete tour for ``hr.attendance_reason``.

        IK: docs/hr_attendance_reason/03-delete.md
        """
        self.start_tour(
            "/web",
            "ssi_timesheet_attendance_hr_attendance_reason_delete",
            login="admin",
        )

    def test_deactivate(self):
        """Run the deactivate tour for ``hr.attendance_reason``.

        IK: docs/hr_attendance_reason/04-deactivate.md
        """
        self.start_tour(
            "/web",
            "ssi_timesheet_attendance_hr_attendance_reason_deactivate",
            login="admin",
        )

    def test_activate(self):
        """Run the activate tour for ``hr.attendance_reason``.

        IK: docs/hr_attendance_reason/05-activate.md
        """
        self.start_tour(
            "/web",
            "ssi_timesheet_attendance_hr_attendance_reason_activate",
            login="admin",
        )

    def test_reset_code(self):
        """Run the reset code tour for ``hr.attendance_reason``.

        IK: docs/hr_attendance_reason/06-reset-code.md
        """
        self.start_tour(
            "/web",
            "ssi_timesheet_attendance_hr_attendance_reason_reset_code",
            login="admin",
        )
