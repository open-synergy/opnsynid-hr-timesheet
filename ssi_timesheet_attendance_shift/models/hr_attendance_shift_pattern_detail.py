# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class HrAttendanceShiftPatternDetail(models.Model):
    """Represents one day-in-cycle line of an attendance shift pattern.

    Belongs to exactly one ``hr.attendance_shift_pattern`` and states
    which ``hr.attendance_shift`` (if any) applies on that day-in-cycle.
    An empty ``shift_id`` is a first-class value meaning "day off" —
    it is intentionally not required.
    """

    _name = "hr.attendance_shift_pattern.detail"
    _description = "Attendance Shift Pattern - Detail"
    _order = "pattern_id, day_index"

    pattern_id = fields.Many2one(
        string="# Pattern",
        comodel_name="hr.attendance_shift_pattern",
        required=True,
        ondelete="cascade",
    )
    day_index = fields.Integer(
        string="Day Index",
        required=True,
        help=(
            "Position of this line within the parent pattern's cycle, "
            "counted from 1 to the pattern's Cycle Length (Days)."
        ),
    )
    shift_id = fields.Many2one(
        string="Shift",
        comodel_name="hr.attendance_shift",
        help=(
            "Shift that applies on this day-in-cycle. Left empty, this "
            "day-in-cycle is a day off — not incomplete data."
        ),
    )

    @api.constrains("day_index", "pattern_id")
    def _check_day_index_range(self):
        """Reject a Day Index outside the parent's cycle length.

        :raises ValidationError: when ``day_index`` is not between 1
            and the parent pattern's ``cycle_length``
        """
        for record in self.sudo():
            if not record._check_day_index_range_condition():
                error_message = (
                    "Day index must be between 1 and the pattern " "cycle length"
                )
                raise ValidationError(_(error_message))

    def _check_day_index_range_condition(self):
        """Tell whether ``day_index`` lies within ``[1, cycle_length]``.

        Extension point: override to relax or tighten the bounds.

        :return: True when valid; never raises
        """
        self.ensure_one()
        return 1 <= self.day_index <= self.pattern_id.cycle_length

    @api.constrains("day_index", "pattern_id")
    def _check_day_index_unique(self):
        """Reject a Day Index already used by a sibling detail line.

        :raises ValidationError: when another line of the same
            pattern already uses this ``day_index``
        """
        for record in self.sudo():
            if not record._check_day_index_unique_condition():
                error_message = "Day index must be unique within a pattern"
                raise ValidationError(_(error_message))

    def _check_day_index_unique_condition(self):
        """Tell whether ``day_index`` is unique within the pattern.

        Extension point: override to change the uniqueness rule.

        :return: True when unique; never raises
        """
        self.ensure_one()
        domain = [
            ("pattern_id", "=", self.pattern_id.id),
            ("day_index", "=", self.day_index),
            ("id", "!=", self.id),
        ]
        return self.search_count(domain) == 0
