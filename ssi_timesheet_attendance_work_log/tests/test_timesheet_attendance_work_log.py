# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestTimesheetAttendanceWorkLog(YamlTransactionCase):
    def test_timesheet_attendance_work_log(self):
        self.run_yaml_scenario("test_data_timesheet_attendance_work_log.yaml")
