# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiHrTimesheetAttendance(HttpSavepointCase):
    """Tour tests for the ``hr.timesheet_attendance`` work instructions.

    Uses ``HttpSavepointCase`` rather than plain ``HttpCase``: in 14.0
    ``TransactionCase`` only assigns ``self.env`` inside instance
    ``setUp()``, so ``cls.env`` is not available in ``setUpClass()``.
    ``HttpSavepointCase`` (via ``SingleTransactionCase``) does set
    ``cls.env`` in ``setUpClass()``, which the tours below rely on to
    seed an open timesheet and attendance rows visible to the browser
    session.
    """

    @classmethod
    def setUpClass(cls):
        """Grant the required group and seed an open timesheet for admin.

        Pre-Condition common to every IK in this model: an
        ``hr.timesheet`` for the current user's employee, covering the
        record's **Date**, exists with status **On Progress** — ``Sheet``
        is resolved automatically from **Date** and the employee, and
        saving fails otherwise. Since ``employee_id`` on this model
        defaults (and, per the view, is invisible) to
        ``self.env.user.employee_id``, the tours run as "admin" need an
        ``hr.employee`` linked to that user.
        """
        super().setUpClass()
        cls.env.ref(
            "ssi_timesheet_attendance.hr_timesheet_attendance_group"
        ).sudo().write({"users": [(4, cls.env.ref("base.user_admin").id)]})

        admin_user = cls.env.ref("base.user_admin")
        employee_model = cls.env["hr.employee"]
        cls.admin_employee = employee_model.search(
            [("user_id", "=", admin_user.id)], limit=1
        )
        if not cls.admin_employee:
            cls.admin_employee = employee_model.create(
                {
                    "name": "TOUR-ADMIN-ATTENDANCE-EMPLOYEE",
                    "user_id": admin_user.id,
                }
            )

        working_schedule = cls.env["resource.calendar"].search(
            [], limit=1, order="id asc"
        )
        cls.timesheet_open = cls.env["hr.timesheet"].create(
            {
                "employee_id": cls.admin_employee.id,
                "date_start": "2026-01-01",
                "date_end": "2026-01-31",
                "working_schedule_id": working_schedule.id,
            }
        )
        cls.timesheet_open.with_context(bypass_policy_check=True).action_open()

        attendance_model = cls.env["hr.timesheet_attendance"]

        # --- 02-edit.md: Check In filled, Check Out still empty (Open),
        # so the tour's Check Out fill exercises the Present transition.
        cls.attendance_edit = attendance_model.create(
            {
                "date": "2026-01-16",
                "employee_id": cls.admin_employee.id,
                "check_in": "2026-01-16 08:00:00",
            }
        )

        # --- 03-delete.md: a fully closed attendance record.
        cls.attendance_delete = attendance_model.create(
            {
                "date": "2026-01-20",
                "employee_id": cls.admin_employee.id,
                "check_in": "2026-01-20 08:00:00",
                "check_out": "2026-01-20 17:00:00",
            }
        )

    def test_create(self):
        """Run the create tour for ``hr.timesheet_attendance``.

        IK: docs/hr_timesheet_attendance/01-create.md
        """
        self.start_tour(
            "/web",
            "ssi_timesheet_attendance_hr_timesheet_attendance_create",
            login="admin",
        )

    def test_edit(self):
        """Run the edit tour for ``hr.timesheet_attendance``.

        IK: docs/hr_timesheet_attendance/02-edit.md
        """
        self.start_tour(
            "/web",
            "ssi_timesheet_attendance_hr_timesheet_attendance_edit",
            login="admin",
        )

    def test_delete(self):
        """Run the delete tour for ``hr.timesheet_attendance``.

        IK: docs/hr_timesheet_attendance/03-delete.md
        """
        self.start_tour(
            "/web",
            "ssi_timesheet_attendance_hr_timesheet_attendance_delete",
            login="admin",
        )
