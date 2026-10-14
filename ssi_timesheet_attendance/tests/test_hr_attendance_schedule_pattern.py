# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestHrAttendanceSchedulePattern(YamlTransactionCase):
    """Cover the pattern schedule source of ``hr.timesheet``.

    Covers ``hr.attendance_schedule_pattern`` and its ``.line`` and
    ``.date`` children: the recurring rules, the special dates, the
    public holiday precedence, the inheritance of the source from
    the employee and the company, and the negative paths.
    """

    def test_hr_attendance_schedule_pattern(self):
        """Run the ``hr.attendance_schedule_pattern`` YAML scenarios."""
        self.run_yaml_scenario("test_data_hr_attendance_schedule_pattern.yaml")
