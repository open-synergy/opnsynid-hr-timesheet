# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from unittest.mock import patch

from odoo_yaml_test import YamlTransactionCase

from odoo.exceptions import UserError
from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestTimesheetScheduleRebuild(YamlTransactionCase):
    """Test the schedule rebuild guards of ``hr.timesheet``.

    Pure Python - trigger P6 (L-15: the YAML evaluator cannot patch a
    method, and the base module has no real blocker to exercise, so
    the hook has to be patched to return one).

    The fixture is built in ``setUp()``: ``YamlTransactionCase`` is a
    ``TransactionCase``, which only has ``self.env`` there.
    """

    def setUp(self):
        """Create an employee, a Monday calendar and an open timesheet.

        The calendar has a single Monday slot from 08:00 to 17:00 and
        the schedules are created once so the tests find slots.

        :return: None
        """
        super().setUp()
        self.calendar = self.env["resource.calendar"].create(
            {
                "name": "Test Monday Calendar",
                "tz": "Asia/Jakarta",
                "attendance_ids": [
                    (
                        0,
                        0,
                        {
                            "name": "Monday",
                            "dayofweek": "0",
                            "hour_from": 8.0,
                            "hour_to": 17.0,
                        },
                    )
                ],
            }
        )
        self.employee = self.env["hr.employee"].create(
            {
                "name": "Test Employee Schedule Rebuild",
                "tz": "Asia/Jakarta",
            }
        )
        self.timesheet = self.env["hr.timesheet"].create(
            {
                "employee_id": self.employee.id,
                "date_start": "2024-07-01",
                "date_end": "2024-07-01",
                "working_schedule_id": self.calendar.id,
            }
        )
        self.timesheet.action_open()
        self.timesheet.action_compute_schedule()

    def test_rebuild_refused_by_blocker_keeps_slots(self):
        """A blocker refuses the rebuild and names its records.

        Pure Python - trigger P6 (L-15: the base module returns no
        blocker, so the hook has to be patched to return one). The
        slots must still exist and the message must name the record.
        """
        partner = self.env["res.partner"].create({"name": "Blocking Document"})
        slots = self.timesheet.schedule_ids
        self.assertTrue(slots)
        model_class = type(self.env["hr.timesheet"])
        with patch.object(
            model_class,
            "_get_schedule_rebuild_blockers",
            return_value=[("Test Document", partner)],
        ):
            with self.assertRaises(UserError) as context:
                self.timesheet.action_compute_schedule()
        message = str(context.exception)
        self.assertIn("Test Document", message)
        self.assertIn("Blocking Document", message)
        self.assertEqual(self.timesheet.schedule_ids, slots)
