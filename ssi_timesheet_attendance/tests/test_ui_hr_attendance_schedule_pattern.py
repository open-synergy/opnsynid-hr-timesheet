# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiHrAttendanceSchedulePattern(HttpSavepointCase):
    """Tour tests for the ``hr.attendance_schedule_pattern`` work instructions.

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
        # Pre-Condition: the Attendance Schedule Patterns menu is gated
        # by the "Attendance Schedule Pattern" configurator group.
        # Without it the tour dies on its first step — the menu is never
        # rendered for "admin".
        cls.env.ref(
            "ssi_timesheet_attendance.attendance_schedule_pattern_group"
        ).sudo().write({"users": [(4, cls.env.ref("base.user_admin").id)]})
        cls.frequency = cls.env["frequency"].create(
            {
                "name": "TOUR-SCHED-PATTERN-FREQ",
                "code": "/",
                "interval": 1,
                "interval_type": "daily",
                "use_byweekday": True,
                "mo": True,
                "tu": True,
                "we": True,
                "th": True,
                "fr": True,
            }
        )
        cls.pattern_edit = cls.env["hr.attendance_schedule_pattern"].create(
            {
                "name": "TOUR-SCHED-PATTERN-EDIT",
                "code": "/",
            }
        )
        cls.pattern_delete = cls.env["hr.attendance_schedule_pattern"].create(
            {
                "name": "TOUR-SCHED-PATTERN-DELETE",
                "code": "/",
            }
        )

    def test_create(self):
        """Run the create tour for ``hr.attendance_schedule_pattern``.

        IK: docs/hr_attendance_schedule_pattern/01-create.md
        """
        self.start_tour(
            "/web",
            "ssi_timesheet_attendance_hr_attendance_schedule_pattern_create",
            login="admin",
        )

    def test_edit(self):
        """Run the edit tour for ``hr.attendance_schedule_pattern``.

        IK: docs/hr_attendance_schedule_pattern/02-edit.md
        """
        self.start_tour(
            "/web",
            "ssi_timesheet_attendance_hr_attendance_schedule_pattern_edit",
            login="admin",
        )

    def test_delete(self):
        """Run the delete tour for ``hr.attendance_schedule_pattern``.

        IK: docs/hr_attendance_schedule_pattern/03-delete.md
        """
        self.start_tour(
            "/web",
            "ssi_timesheet_attendance_hr_attendance_schedule_pattern_delete",
            login="admin",
        )
