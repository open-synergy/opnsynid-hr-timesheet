# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from datetime import timedelta

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

    def _match_shift_check_in(self, check_in):
        """Tell whether ``check_in`` falls in this line's shift window.

        The window spans from ``date_start`` minus the originating
        shift's early check-in tolerance to ``date_end`` plus its
        late check-out tolerance, both read from ``shift_id``. Used
        by ``hr.timesheet_attendance._compute_schedule()`` to match a
        shift-roster attendance to the schedule line it belongs to.

        :param check_in: ``datetime`` to test, or a falsy value
        :return: True when ``check_in`` lies in the tolerance window;
            always False when this line has no ``shift_id``, no
            ``date_start``/``date_end``, or ``check_in`` is falsy
        """
        self.ensure_one()
        if not (self.shift_id and self.date_start and self.date_end and check_in):
            return False
        window_start = self.date_start - timedelta(
            hours=self.shift_id.early_check_in_tolerance
        )
        window_end = self.date_end + timedelta(
            hours=self.shift_id.late_check_out_tolerance
        )
        return window_start <= check_in <= window_end
