# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class HrAttendanceShiftPattern(models.Model):
    """Represents a fixed-length rotation cycle of attendance shifts.

    ``resource.calendar`` only understands a two-week (odd/even)
    rotation, which cannot express a three-crew rolling pattern or a
    four-days-on/two-days-off pattern. This model instead stores an
    arbitrary-length cycle (``cycle_length`` days) as a set of detail
    lines (``detail_ids``), one per day-in-cycle, each optionally
    pointing at an ``hr.attendance_shift``.

    The cycle is always resolved relative to ``date_anchor`` — a
    single global reference date — never relative to a timesheet
    period's start date. This is a deliberate, binding design choice:
    anchoring to the timesheet period would reset the cycle every
    time a period boundary is crossed, breaking a rotation that spans
    across it. Several crews can reuse the same pattern by being
    assigned to it (``hr.attendance_shift_assignment``) with a
    different ``cycle_offset``, which shifts which day-in-cycle a
    given calendar date resolves to for that crew.
    """

    _name = "hr.attendance_shift_pattern"
    _inherit = ["mixin.master_data"]
    _description = "Attendance Shift Pattern"

    cycle_length = fields.Integer(
        string="Cycle Length (Days)",
        required=True,
        default=7,
        help=(
            "Number of days in one full rotation of this pattern. "
            "Every detail line's Day Index must fall within 1 and "
            "this value."
        ),
    )
    date_anchor = fields.Date(
        string="Cycle Anchor Date",
        required=True,
        help=(
            "Global reference date day-in-cycle 1 is resolved from. "
            "Shared by every crew assigned to this pattern — a crew's "
            "own Cycle Offset (on its assignment) is what makes its "
            "rotation start on a different day, not a different "
            "anchor."
        ),
    )
    detail_ids = fields.One2many(
        string="Cycle Days",
        comodel_name="hr.attendance_shift_pattern.detail",
        inverse_name="pattern_id",
        help=(
            "One line per day-in-cycle, from 1 to Cycle Length (Days). "
            "A line whose Shift is left empty means that day-in-cycle "
            "is a day off."
        ),
    )
