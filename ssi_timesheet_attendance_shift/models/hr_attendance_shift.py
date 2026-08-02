# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class HrAttendanceShift(models.Model):
    """Represents a work shift declared as a start hour plus a duration.

    ``resource.calendar.attendance`` cannot express a block of work that
    crosses midnight: it only stores ``hour_from``/``hour_to`` and clamps
    both to the 0-23.99 range, so an overnight shift (e.g. a security
    guard shift 18:00-06:00) must be split into two calendar lines and is
    then reported as two disjoint attendance intervals. This model keeps
    such a shift as a single record by storing ``hour_start`` and
    ``duration`` instead of a stored end hour. ``hour_end`` and
    ``cross_day`` are display-only fields derived from those two — every
    schedule computation always uses ``duration``, never ``hour_end``.
    """

    _name = "hr.attendance_shift"
    _inherit = ["mixin.master_data"]
    _description = "Attendance Shift"

    hour_start = fields.Float(
        string="Work From",
        required=True,
        help="Hour of day, in the 0-23.99 range, at which the shift starts.",
    )
    duration = fields.Float(
        string="Duration (Hours)",
        required=True,
        help=(
            "Length of the shift in hours, counted from Work From. "
            "Schedule matching always uses this value — Work To is a "
            "display-only value derived from it, never the other way "
            "around."
        ),
    )
    hour_end = fields.Float(
        string="Work To",
        compute="_compute_hour_end",
        store=True,
        compute_sudo=True,
        help=(
            "Display-only hour at which the shift ends, computed as "
            "(Work From + Duration) modulo 24. Never used to compute "
            "schedules — that is always based on Duration."
        ),
    )
    cross_day = fields.Boolean(
        string="Cross Day",
        compute="_compute_cross_day",
        store=True,
        compute_sudo=True,
        help=(
            "Display-only flag, True when Work From plus Duration goes "
            "past midnight into the next day."
        ),
    )
    early_check_in_tolerance = fields.Float(
        string="Early Check In Tolerance",
        default=2.0,
        help=(
            "Matching window, in hours, before Work From within which an "
            "attendance check-in is still considered part of this shift. "
            "This is not a lateness policy: lateness itself is still "
            "computed from the raw time difference by "
            "hr.timesheet_attendance_schedule."
        ),
    )
    late_check_out_tolerance = fields.Float(
        string="Late Check Out Tolerance",
        default=3.0,
        help=(
            "Matching window, in hours, after the shift end within which "
            "an attendance check-out is still considered part of this "
            "shift. This is not a lateness policy — see Early Check In "
            "Tolerance."
        ),
    )

    @api.depends("hour_start", "duration")
    def _compute_hour_end(self):
        """Derive the display-only end hour from start hour and duration.

        :return: nothing; assigns ``hour_end``
        """
        for record in self:
            result = (record.hour_start + record.duration) % 24
            record.hour_end = result

    @api.depends("hour_start", "duration")
    def _compute_cross_day(self):
        """Flag shifts whose start plus duration crosses past midnight.

        :return: nothing; assigns ``cross_day``
        """
        for record in self:
            result = False
            if record.hour_start + record.duration > 24:
                result = True
            record.cross_day = result

    @api.constrains("hour_start")
    def _check_hour_start(self):
        """Reject a Work From hour outside the 0-23.99 range.

        :raises ValidationError: when ``hour_start`` is not in [0, 23.99]
        """
        for record in self.sudo():
            if not record._check_hour_start_condition():
                error_message = "Work from must be between 0 and 23.99"
                raise ValidationError(_(error_message))

    def _check_hour_start_condition(self):
        """Tell whether ``hour_start`` lies within the 0-23.99 range.

        Extension point: override to relax or tighten the bounds.

        :return: True when valid; never raises
        """
        self.ensure_one()
        return 0 <= self.hour_start <= 23.99

    @api.constrains("duration")
    def _check_duration(self):
        """Reject a duration that is not strictly positive and <= 24.

        :raises ValidationError: when ``duration`` is outside (0, 24]
        """
        for record in self.sudo():
            if not record._check_duration_condition():
                error_message = "Duration must be greater than 0 and at most 24 hours"
                raise ValidationError(_(error_message))

    def _check_duration_condition(self):
        """Tell whether ``duration`` lies within the (0, 24] range.

        Extension point: override to relax or tighten the bounds.

        :return: True when valid; never raises
        """
        self.ensure_one()
        return 0 < self.duration <= 24
