# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from freezegun import freeze_time

from odoo.tests import tagged
from odoo.tests.common import TransactionCase


@tagged("post_install", "-at_install")
class TestTimesheetSignOut(TransactionCase):
    """Test ``HRTimesheet._sign_out()``'s same-day check-out path.

    Pure Python — trigger P6 (L-16: the YAML evaluator cannot freeze
    time, and this scenario needs the attendance's ``date`` and the
    check-out date derived from the real clock to fall on the exact
    same calendar day, which is only reliable under a frozen clock).
    """

    @classmethod
    def setUpClass(cls):
        """Create an employee with an open, same-day attendance.

        :return: None
        """
        super().setUpClass()
        cls.working_schedule = cls.env["resource.calendar"].search(
            [], limit=1, order="id asc"
        )
        cls.employee = cls.env["hr.employee"].create(
            {"name": "Test Employee Sign Out Same Day"}
        )
        with freeze_time("2024-06-10 12:00:00"):
            cls.timesheet = cls.env["hr.timesheet"].create(
                {
                    "employee_id": cls.employee.id,
                    "date_start": "2024-06-01",
                    "date_end": "2024-06-30",
                    "working_schedule_id": cls.working_schedule.id,
                }
            )
            cls.timesheet.action_open()
            cls.attendance = cls.env["hr.timesheet_attendance"].create(
                {
                    "employee_id": cls.employee.id,
                    "date": "2024-06-10",
                    "check_in": "2024-06-10 08:00:00",
                    "sheet_id": cls.timesheet.id,
                }
            )

    @freeze_time("2024-06-10 17:00:00")
    def test_sign_out_same_day_updates_existing_attendance(self):
        """Same-day sign-out updates the open attendance in place.

        Pure Python — trigger P6 (L-16: freezing time is required to
        guarantee the check-out date equals the attendance date, the
        condition that keeps ``_sign_out()`` out of the cross-day
        branch this issue's fix touches). No new anomaly attendance
        should be created and the existing one should be closed.
        """
        self.timesheet._sign_out()

        attendances = self.env["hr.timesheet_attendance"].search(
            [("employee_id", "=", self.employee.id)]
        )
        self.assertEqual(len(attendances), 1)
        self.assertEqual(attendances.id, self.attendance.id)
        self.assertTrue(attendances.check_out)
