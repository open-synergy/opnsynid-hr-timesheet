# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiHrTimesheet(HttpSavepointCase):
    """Tour tests for the ``hr.timesheet`` work instructions added by
    ``ssi_timesheet_attendance`` (the Working Schedule field delta, and
    the Sign In / Sign Out / Create Schedules actions).

    Uses ``HttpSavepointCase`` rather than plain ``HttpCase``: in 14.0
    ``TransactionCase`` only assigns ``self.env`` inside instance
    ``setUp()``, so ``cls.env`` is not available in ``setUpClass()``.
    ``HttpSavepointCase`` (via ``SingleTransactionCase``) does set
    ``cls.env`` in ``setUpClass()``, which the tours below rely on to
    seed employees and timesheets visible to the browser session.
    """

    @classmethod
    def setUpClass(cls):
        """Grant the required group and seed one fixture per tour.

        Pre-Condition common to every ``hr_timesheet`` IK exercised
        here: the actor is in group *Timesheets — User* — granting
        *Timesheet Attendance* (implied by this module's own security
        data) to ``admin`` covers it. Unlike ``hr.timesheet_attendance``,
        the ``employee_id`` used by Sign In / Sign Out / Create
        Schedules is the timesheet's OWN employee, not the logged-in
        user's — so each fixture below uses its own dedicated employee,
        independent from "admin".
        """
        super().setUpClass()
        cls.env.ref(
            "ssi_timesheet_attendance.hr_timesheet_attendance_group"
        ).sudo().write({"users": [(4, cls.env.ref("base.user_admin").id)]})

        employee_model = cls.env["hr.employee"]
        timesheet_model = cls.env["hr.timesheet"]
        attendance_model = cls.env["hr.timesheet_attendance"]
        working_schedule = cls.env["resource.calendar"].search(
            [], limit=1, order="id asc"
        )
        cls.working_schedule = working_schedule

        # --- 15-sign-in.md: On Progress, no attendance recorded yet, so
        # Attendance Status defaults to Sign Out and the Sign In button
        # is visible.
        cls.employee_sign_in = employee_model.create({"name": "TOUR-EMP-SIGNIN"})
        cls.timesheet_sign_in = timesheet_model.create(
            {
                "employee_id": cls.employee_sign_in.id,
                "date_start": "2026-01-01",
                "date_end": "2026-01-31",
                "working_schedule_id": working_schedule.id,
            }
        )
        cls.timesheet_sign_in.with_context(bypass_policy_check=True).action_open()

        # --- 16-sign-out.md: On Progress, with an already-open (no
        # Check Out) attendance record, so Attendance Status is Sign In
        # and the Sign Out button is visible.
        cls.employee_sign_out = employee_model.create({"name": "TOUR-EMP-SIGNOUT"})
        cls.timesheet_sign_out = timesheet_model.create(
            {
                "employee_id": cls.employee_sign_out.id,
                "date_start": "2026-02-01",
                "date_end": "2026-02-28",
                "working_schedule_id": working_schedule.id,
            }
        )
        cls.timesheet_sign_out.with_context(bypass_policy_check=True).action_open()
        cls.attendance_sign_out = attendance_model.create(
            {
                "date": "2026-02-01",
                "employee_id": cls.employee_sign_out.id,
                "check_in": "2026-02-01 08:00:00",
            }
        )

        # --- 17-compute-schedule.md: Draft, with Working Schedule, Date
        # Start and Date End filled, and no Attendance Schedule lines
        # yet.
        cls.employee_schedule = employee_model.create({"name": "TOUR-EMP-SCHEDULE"})
        cls.timesheet_schedule = timesheet_model.create(
            {
                "employee_id": cls.employee_schedule.id,
                "date_start": "2026-03-01",
                "date_end": "2026-03-31",
                "working_schedule_id": working_schedule.id,
            }
        )

    def test_create(self):
        """Run the create-delta tour for ``hr.timesheet``.

        IK: docs/hr_timesheet/01-create.md
        """
        self.start_tour(
            "/web", "ssi_timesheet_attendance_hr_timesheet_create", login="admin"
        )

    def test_sign_in(self):
        """Run the sign in tour for ``hr.timesheet``.

        IK: docs/hr_timesheet/15-sign-in.md
        """
        self.start_tour(
            "/web", "ssi_timesheet_attendance_hr_timesheet_sign_in", login="admin"
        )

    def test_sign_out(self):
        """Run the sign out tour for ``hr.timesheet``.

        IK: docs/hr_timesheet/16-sign-out.md
        """
        self.start_tour(
            "/web", "ssi_timesheet_attendance_hr_timesheet_sign_out", login="admin"
        )

    def test_compute_schedule(self):
        """Run the create schedules tour for ``hr.timesheet``.

        IK: docs/hr_timesheet/17-compute-schedule.md
        """
        self.start_tour(
            "/web",
            "ssi_timesheet_attendance_hr_timesheet_compute_schedule",
            login="admin",
        )
