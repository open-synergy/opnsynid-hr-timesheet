# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class HRTimesheetAttendanceSchedule(models.Model):
    _name = "hr.timesheet_attendance_schedule"
    _inherit = "hr.timesheet_attendance_schedule"

    leave_ids = fields.Many2many(
        string="Leaves",
        comodel_name="hr.leave",
        relation="rel_attendance_schedule_2_leave",
        column1="attendance_schedule_id",
        column2="leave_id",
    )
