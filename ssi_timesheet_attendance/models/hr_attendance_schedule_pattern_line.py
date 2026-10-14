# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class HrAttendanceSchedulePatternLine(models.Model):
    """Represents one recurring rule of an attendance schedule pattern.

    Belongs to exactly one ``hr.attendance_schedule_pattern``. The
    rule is a ``frequency`` (recurrence rule) that must repeat every
    one interval, plus what happens on the days it covers: the
    employee works from ``hour_from`` to ``hour_to``, or is off.
    """

    _name = "hr.attendance_schedule_pattern.line"
    _description = "Attendance Schedule Pattern - Line"
    _order = "pattern_id, sequence, id"

    pattern_id = fields.Many2one(
        string="# Pattern",
        comodel_name="hr.attendance_schedule_pattern",
        required=True,
        ondelete="cascade",
    )
    sequence = fields.Integer(
        string="Sequence",
        default=10,
        help="Order of the line. The first Work line that covers a day wins.",
    )
    frequency_id = fields.Many2one(
        string="Frequency",
        comodel_name="frequency",
        required=True,
        ondelete="restrict",
        help=(
            "Recurrence rule that selects the days of this line. It "
            "must repeat every 1 interval; for example every week on "
            "Saturday, or every month on the second Saturday."
        ),
    )
    effect = fields.Selection(
        string="Effect",
        selection=[
            ("work", "Work"),
            ("off", "Off"),
        ],
        required=True,
        default="work",
        help=(
            "Work gives a schedule slot on the days the frequency "
            "covers. Off removes the day, even when a Work line "
            "covers it too."
        ),
    )
    hour_from = fields.Float(
        string="Hour From",
        help="Start of the working slot, as hours of the day (0.0 to 24.0).",
    )
    hour_to = fields.Float(
        string="Hour To",
        help="End of the working slot, as hours of the day (0.0 to 24.0).",
    )
    date_start = fields.Date(
        string="Valid From",
        help="First day this line applies. Empty means no lower limit.",
    )
    date_end = fields.Date(
        string="Valid Until",
        help="Last day this line applies. Empty means no upper limit.",
    )

    @api.constrains("frequency_id")
    def _check_frequency_interval(self):
        """Reject a frequency that does not repeat every 1 interval.

        :raises ValidationError: when ``frequency_id.interval`` is
            not 1
        """
        for record in self.sudo():
            if record.frequency_id.interval != 1:
                error_message = _(
                    "Frequency of a pattern line must repeat every 1 interval"
                )
                raise ValidationError(error_message)

    @api.constrains("effect", "hour_from", "hour_to")
    def _check_hour_range(self):
        """Reject a working slot outside a single calendar day.

        :raises ValidationError: when ``effect`` is ``work`` and the
            hours do not satisfy ``0 <= hour_from < hour_to <= 24``
        """
        for record in self.sudo():
            if record.effect != "work":
                continue
            if not 0.0 <= record.hour_from < record.hour_to <= 24.0:
                error_message = _(
                    "Working hours must satisfy 0 <= Hour From < Hour To <= 24"
                )
                raise ValidationError(error_message)

    def _get_dates(self, date_start, date_end):
        """Return the days of a period that this line covers.

        The period is cut to the line's validity range. The days are
        computed from the frequency in UTC, which keeps calendar
        dates untouched.

        :param date_start: first day of the period
        :type date_start: datetime.date
        :param date_end: last day of the period, inclusive
        :type date_end: datetime.date
        :return: the covered days
        :rtype: set
        """
        self.ensure_one()
        start = max(date_start, self.date_start) if self.date_start else date_start
        end = min(date_end, self.date_end) if self.date_end else date_end
        if start > end:
            return set()
        rule = self.frequency_id._get_rrule(dtstart=start, until=end, tz="UTC")
        return {value.date() for value in rule}
