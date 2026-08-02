# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import HttpCase, tagged


@tagged("post_install", "-at_install")
class TestUiHrAttendanceShift(HttpCase):
    """Tour tests for the ``hr.attendance_shift`` work instructions."""

    @classmethod
    def setUpClass(cls):
        """Grant the configurator group and seed shifts the tours reuse."""
        super().setUpClass()
        # Pre-Condition: the Attendance Shifts menu is gated by the
        # "Attendance Shift" configurator group. Without it the tour dies
        # on its first step — the menu is never rendered for "admin".
        cls.env.ref(
            "ssi_timesheet_attendance_shift.attendance_shift_group"
        ).sudo().write({"users": [(4, cls.env.ref("base.user_admin").id)]})
        cls.shift_edit = cls.env["hr.attendance_shift"].create(
            {
                "name": "TOUR-SHIFT-EDIT",
                "code": "/",
                "hour_start": 6.0,
                "duration": 8.0,
            }
        )
        cls.shift_delete = cls.env["hr.attendance_shift"].create(
            {
                "name": "TOUR-SHIFT-DELETE",
                "code": "/",
                "hour_start": 9.0,
                "duration": 8.0,
            }
        )
        cls.shift_deactivate = cls.env["hr.attendance_shift"].create(
            {
                "name": "TOUR-SHIFT-DEACTIVATE",
                "code": "/",
                "hour_start": 7.0,
                "duration": 8.0,
            }
        )
        cls.shift_activate = cls.env["hr.attendance_shift"].create(
            {
                "name": "TOUR-SHIFT-ACTIVATE",
                "code": "/",
                "hour_start": 7.0,
                "duration": 8.0,
                "active": False,
            }
        )

    def test_create(self):
        """Run the create tour for ``hr.attendance_shift``.

        IK: docs/hr_attendance_shift/01-create.md
        """
        self.start_tour(
            "/web",
            "ssi_timesheet_attendance_shift_hr_attendance_shift_create",
            login="admin",
        )

    def test_edit(self):
        """Run the edit tour for ``hr.attendance_shift``.

        IK: docs/hr_attendance_shift/02-edit.md
        """
        self.start_tour(
            "/web",
            "ssi_timesheet_attendance_shift_hr_attendance_shift_edit",
            login="admin",
        )

    def test_delete(self):
        """Run the delete tour for ``hr.attendance_shift``.

        IK: docs/hr_attendance_shift/03-delete.md
        """
        self.start_tour(
            "/web",
            "ssi_timesheet_attendance_shift_hr_attendance_shift_delete",
            login="admin",
        )

    def test_deactivate(self):
        """Run the deactivate tour for ``hr.attendance_shift``.

        IK: docs/hr_attendance_shift/04-deactivate.md
        """
        self.start_tour(
            "/web",
            "ssi_timesheet_attendance_shift_hr_attendance_shift_deactivate",
            login="admin",
        )

    def test_activate(self):
        """Run the activate tour for ``hr.attendance_shift``.

        IK: docs/hr_attendance_shift/05-activate.md
        """
        self.start_tour(
            "/web",
            "ssi_timesheet_attendance_shift_hr_attendance_shift_activate",
            login="admin",
        )
