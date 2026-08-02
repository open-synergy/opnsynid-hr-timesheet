# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class HrTimesheetAttendanceSchedule(models.Model):
    """
    Adds the originating shift to a generated attendance schedule.
    Populated by the shift schedule generator
    (``hr.timesheet._get_schedule_data``) so that downstream modules
    — attendance matching, tolerance lookup — can read back which
    ``hr.attendance_shift`` a schedule line was generated from.
    """

    _inherit = "hr.timesheet_attendance_schedule"

    shift_id = fields.Many2one(
        string="Shift",
        comodel_name="hr.attendance_shift",
        ondelete="restrict",
        help=(
            "Shift this schedule line was generated from, when the "
            "owning timesheet's Schedule Source is Shift Roster. "
            "Left empty for schedule lines generated from a Working "
            "Schedule."
        ),
    )
