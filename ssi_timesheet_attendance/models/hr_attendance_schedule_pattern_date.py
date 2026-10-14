# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class HrAttendanceSchedulePatternDate(models.Model):
    """Represents one special date of an attendance schedule pattern.

    Overrides the recurring rules of the pattern on one calendar
    date: the employee works from ``hour_from`` to ``hour_to``, or is
    off. A national public holiday still wins over it.
    """

    _name = "hr.attendance_schedule_pattern.date"
    _description = "Attendance Schedule Pattern - Special Date"
    _order = "pattern_id, date, id"

    pattern_id = fields.Many2one(
        string="# Pattern",
        comodel_name="hr.attendance_schedule_pattern",
        required=True,
        ondelete="cascade",
    )
    date = fields.Date(
        string="Date",
        required=True,
        help="Calendar date this exception applies to. Unique per pattern.",
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
            "Work gives a schedule slot on this date, even when the "
            "recurring rules say otherwise. Off removes the date."
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
    note = fields.Char(
        string="Note",
        help="Free text that explains the exception.",
    )

    @api.constrains("pattern_id", "date")
    def _check_date_unique(self):
        """Reject a date already used by a sibling special date.

        :raises ValidationError: when another special date of the
            same pattern has the same ``date``
        """
        for record in self.sudo():
            domain = [
                ("pattern_id", "=", record.pattern_id.id),
                ("date", "=", record.date),
                ("id", "!=", record.id),
            ]
            if self.search_count(domain) > 0:
                error_message = _("Special date must be unique within a pattern")
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
