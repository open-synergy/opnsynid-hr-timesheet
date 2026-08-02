# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase
from psycopg2 import IntegrityError

from odoo.tests import tagged
from odoo.tools import mute_logger


@tagged("post_install", "-at_install")
class TestHrAttendanceShiftPattern(YamlTransactionCase):
    """Cover CRUD, detail lines, and negative path of the pattern models.

    Covers ``hr.attendance_shift_pattern`` and its ``.detail`` child.
    """

    def test_hr_attendance_shift_pattern(self):
        """Run the ``hr.attendance_shift_pattern`` YAML scenarios."""
        self.run_yaml_scenario("test_data_hr_attendance_shift_pattern.yaml")

    @mute_logger("odoo.sql_db")
    def test_unlink_pattern_in_use_is_restricted(self):
        """Reject deleting a pattern still referenced by an assignment.

        Pure Python — trigger P5 (L-22: ``psycopg2.IntegrityError``
        raised by the ``pattern_id`` field's ``ondelete="restrict"``
        is outside the 12 error types ``expect_error`` understands).
        ``mute_logger("odoo.sql_db")`` silences the PostgreSQL ERROR
        line this deliberately triggers; without it
        ``oca_checklog_odoo`` fails the CI even though the test
        itself passes.
        """
        pattern = self.env["hr.attendance_shift_pattern"].create(
            {
                "name": "In-Use Pattern",
                "code": "/",
                "cycle_length": 7,
                "date_anchor": "2024-01-01",
            }
        )
        employee = self.env["hr.employee"].create({"name": "In-Use Pattern Employee"})
        self.env["hr.attendance_shift_assignment"].create(
            {
                "employee_id": employee.id,
                "pattern_id": pattern.id,
                "cycle_offset": 0,
                "date_start": "2024-01-01",
            }
        )
        with self.assertRaises(IntegrityError):
            pattern.unlink()
