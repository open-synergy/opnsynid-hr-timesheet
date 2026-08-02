# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiHrAttendanceShiftAssignment(HttpSavepointCase):
    """Tour tests for ``hr.attendance_shift_assignment`` work instructions.

    Uses ``HttpSavepointCase`` rather than plain ``HttpCase``: in 14.0
    ``TransactionCase`` only assigns ``self.env`` inside instance
    ``setUp()``, so ``cls.env`` is not available in ``setUpClass()``.
    ``HttpSavepointCase`` (via ``SingleTransactionCase``) does set
    ``cls.env`` in ``setUpClass()``, which the tours below rely on to
    seed records visible to the browser session.
    """

    @classmethod
    def setUpClass(cls):
        """Grant the configurator group and seed data the tours reuse."""
        super().setUpClass()
        # Pre-Condition: the Attendance Shift Assignments menu is gated
        # by the "Attendance Shift" configurator group. Without it the
        # tour dies on its first step — the menu is never rendered for
        # "admin".
        cls.env.ref(
            "ssi_timesheet_attendance_shift.attendance_shift_group"
        ).sudo().write({"users": [(4, cls.env.ref("base.user_admin").id)]})
        cls.pattern = cls.env["hr.attendance_shift_pattern"].create(
            {
                "name": "TOUR-ASSIGN-PATTERN",
                "code": "/",
                "cycle_length": 7,
                "date_anchor": "2024-01-01",
            }
        )
        cls.employee_create = cls.env["hr.employee"].create(
            {"name": "TOUR-ASSIGN-CREATE-EMPLOYEE"}
        )
        cls.employee_edit = cls.env["hr.employee"].create(
            {"name": "TOUR-ASSIGN-EDIT-EMPLOYEE"}
        )
        cls.assignment_edit = cls.env["hr.attendance_shift_assignment"].create(
            {
                "employee_id": cls.employee_edit.id,
                "pattern_id": cls.pattern.id,
                "cycle_offset": 0,
                "date_start": "2024-01-01",
            }
        )
        cls.employee_delete = cls.env["hr.employee"].create(
            {"name": "TOUR-ASSIGN-DELETE-EMPLOYEE"}
        )
        cls.assignment_delete = cls.env["hr.attendance_shift_assignment"].create(
            {
                "employee_id": cls.employee_delete.id,
                "pattern_id": cls.pattern.id,
                "cycle_offset": 0,
                "date_start": "2024-01-01",
            }
        )

    def test_create(self):
        """Run the create tour for ``hr.attendance_shift_assignment``.

        IK: docs/hr_attendance_shift_assignment/01-create.md
        """
        self.start_tour(
            "/web",
            "ssi_timesheet_attendance_shift_hr_attendance_shift_assignment_create",
            login="admin",
        )

    def test_edit(self):
        """Run the edit tour for ``hr.attendance_shift_assignment``.

        IK: docs/hr_attendance_shift_assignment/02-edit.md
        """
        self.start_tour(
            "/web",
            "ssi_timesheet_attendance_shift_hr_attendance_shift_assignment_edit",
            login="admin",
        )

    def test_delete(self):
        """Run the delete tour for ``hr.attendance_shift_assignment``.

        IK: docs/hr_attendance_shift_assignment/03-delete.md
        """
        self.start_tour(
            "/web",
            "ssi_timesheet_attendance_shift_hr_attendance_shift_assignment_delete",
            login="admin",
        )
