# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from datetime import timedelta

from odoo import fields, models


class HrAttendanceSchedulePattern(models.Model):
    """Describes a recurring attendance pattern built from frequencies.

    A working schedule (``resource.calendar``) cannot say "the second
    Saturday of every month is a working day" or "every Saturday
    except the last one". A pattern states such rules with
    ``frequency`` records (recurrence rules): each line says on which
    days the employee works or is off, and each date line overrides
    one calendar date.

    A pattern produces at most one slot per day, inside a single
    calendar day. A pattern that crosses midnight, or that needs more
    than one slot a day, belongs to a shift roster or a working
    schedule instead.
    """

    _name = "hr.attendance_schedule_pattern"
    _inherit = ["mixin.master_data"]
    _description = "Attendance Schedule Pattern"

    line_ids = fields.One2many(
        string="Pattern Lines",
        comodel_name="hr.attendance_schedule_pattern.line",
        inverse_name="pattern_id",
        help=(
            "Recurring rules of the pattern. An Off line wins over a "
            "Work line that covers the same day; among Work lines the "
            "first one by sequence wins."
        ),
    )
    date_ids = fields.One2many(
        string="Special Dates",
        comodel_name="hr.attendance_schedule_pattern.date",
        inverse_name="pattern_id",
        help=(
            "Exceptions that override the recurring rules on one "
            "calendar date. A national public holiday still wins "
            "over a special date."
        ),
    )

    def _get_work_slots(self, date_start, date_end):
        """Resolve the working slot of every day in a period.

        For each day, a special date wins; otherwise an Off line that
        covers the day removes it; otherwise the first Work line (by
        sequence) that covers the day gives the slot. Public holidays
        are not handled here: the caller skips them.

        :param date_start: first day of the period
        :type date_start: datetime.date
        :param date_end: last day of the period, inclusive
        :type date_end: datetime.date
        :return: ``{date: (hour_from, hour_to, line)}`` for each day
            that has a slot; ``line`` is the pattern line that gave
            the slot, or an empty recordset for a special date
        :rtype: dict
        """
        self.ensure_one()
        result = {}
        empty_line = self.env["hr.attendance_schedule_pattern.line"]
        specials = {
            record.date: record
            for record in self.date_ids
            if date_start <= record.date <= date_end
        }
        lines = self.line_ids.sorted(key=lambda line: (line.sequence, line.id))
        line_dates = {line.id: line._get_dates(date_start, date_end) for line in lines}
        for offset in range((date_end - date_start).days + 1):
            day = date_start + timedelta(days=offset)
            if day in specials:
                special = specials[day]
                if special.effect == "work":
                    result[day] = (special.hour_from, special.hour_to, empty_line)
                continue
            if any(
                line.effect == "off" and day in line_dates[line.id] for line in lines
            ):
                continue
            for line in lines:
                if line.effect == "work" and day in line_dates[line.id]:
                    result[day] = (line.hour_from, line.hour_to, line)
                    break
        return result
