# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class HrAttendanceShiftAssignment(models.Model):
    """Assigns an attendance shift pattern to one employee (crew).

    Standalone record with no workflow of its own: it links an
    employee to a rotation pattern for a date range, with a
    ``cycle_offset`` that is the sole thing distinguishing one crew
    from another when several crews share the same pattern. A given
    calendar date's day-in-cycle is resolved as::

        ((date - pattern.date_anchor).days - cycle_offset)
            % pattern.cycle_length + 1

    That formula is a binding design decision consumed by the shift
    generator (out of scope for this module) and must not be
    reimplemented differently there. An empty ``date_end`` means the
    assignment has no end date — it applies indefinitely.
    """

    _name = "hr.attendance_shift_assignment"
    _description = "Attendance Shift Assignment"
    _order = "employee_id, date_start desc"
    _rec_name = "employee_id"

    employee_id = fields.Many2one(
        string="Employee",
        comodel_name="hr.employee",
        required=True,
        ondelete="cascade",
    )
    pattern_id = fields.Many2one(
        string="Pattern",
        comodel_name="hr.attendance_shift_pattern",
        required=True,
        ondelete="restrict",
        help="Rotation pattern this employee is assigned to.",
    )
    cycle_offset = fields.Integer(
        string="Cycle Offset (Days)",
        required=True,
        default=0,
        help=(
            "Number of days subtracted from the day-in-cycle formula "
            "before taking the modulo. This is the crew distinguisher: "
            "several employees can share the same Pattern with "
            "different offsets so each starts the rotation on a "
            "different day."
        ),
    )
    date_start = fields.Date(
        string="Date Start",
        required=True,
        help="First calendar date this assignment applies from.",
    )
    date_end = fields.Date(
        string="Date End",
        help=(
            "Last calendar date this assignment applies to. Left "
            "empty, the assignment has no end date."
        ),
    )

    @api.constrains("employee_id", "date_start", "date_end")
    def _check_date_overlap(self):
        """Reject a date range overlapping another of the same employee.

        :raises ValidationError: when this assignment's date range
            overlaps another assignment of the same employee
        """
        for record in self.sudo():
            if not record._check_date_overlap_condition():
                error_message = (
                    "Shift assignment date range cannot overlap for "
                    "the same employee"
                )
                raise ValidationError(_(error_message))

    def _check_date_overlap_condition(self):
        """Tell whether no sibling assignment overlaps this one.

        An empty ``date_end`` (either on this record or on the
        sibling being compared to) is treated as unbounded into the
        future.

        Extension point: override to change the overlap rule.

        :return: True when no overlap is found; never raises
        """
        self.ensure_one()
        domain = [
            ("employee_id", "=", self.employee_id.id),
            ("id", "!=", self.id),
        ]
        if self.date_end:
            domain.append(("date_start", "<=", self.date_end))
        domain += [
            "|",
            ("date_end", ">=", self.date_start),
            ("date_end", "=", False),
        ]
        return self.search_count(domain) == 0

    @api.constrains("date_start", "date_end")
    def _check_date_end(self):
        """Reject a Date End earlier than Date Start.

        :raises ValidationError: when ``date_end`` precedes
            ``date_start``
        """
        for record in self.sudo():
            if not record._check_date_end_condition():
                error_message = "Date end cannot be earlier than date start"
                raise ValidationError(_(error_message))

    def _check_date_end_condition(self):
        """Tell whether Date End is not earlier than Date Start.

        Extension point: override to relax or tighten the bounds.

        :return: True when valid; never raises
        """
        self.ensure_one()
        if not self.date_end:
            return True
        return self.date_end >= self.date_start
