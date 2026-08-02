# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from datetime import timedelta

from odoo import _, models
from odoo.exceptions import ValidationError


class GenerateTimesheet(models.TransientModel):
    """
    Adds a shift-roster date-continuity check to the timesheet
    generator wizard. A Shift Roster employee's next timesheet
    period must start exactly one day after the previous one ends,
    so the shift schedule generator
    (``hr.timesheet._get_schedule_data``) never has to resolve a
    date that belongs to no period. Employees without an active
    shift assignment covering the wizard's ``date_start``, and an
    employee's very first timesheet, are unaffected.
    """

    _inherit = "hr.generate_timesheet"

    def _check_data(self, employee):
        """Extend the base checks with shift date-continuity.

        Calls ``super()`` first, so every pre-existing rejection
        (employee without a user, without a working schedule, or
        with an overlapping timesheet already existing) keeps firing
        with the same order and message it always had.

        :param employee: ``hr.employee`` record timesheet data is
            being generated for
        :return: True when every check, base and shift continuity,
            passes
        :raises ValidationError: when the employee has an active
            shift assignment covering ``date_start`` and a previous
            timesheet that does not end exactly one day before
            ``date_start``
        """
        self.ensure_one()
        super(GenerateTimesheet, self)._check_data(employee)
        self._check_shift_continuity(employee)
        return True

    def _check_shift_continuity(self, employee):
        """Reject a Shift Roster period that leaves a date gap.

        A no-op when the employee has no active
        ``hr.attendance_shift_assignment`` covering this wizard's
        ``date_start``, or when the employee has no earlier
        timesheet — the first period of a shift employee never has a
        predecessor to be contiguous with.

        :param employee: ``hr.employee`` record being checked
        :return: nothing
        :raises ValidationError: when the employee's latest
            timesheet ending before ``date_start`` does not end
            exactly one day before it
        """
        self.ensure_one()
        obj_assignment = self.env["hr.attendance_shift_assignment"]
        assignment_domain = [
            ("employee_id", "=", employee.id),
            ("date_start", "<=", self.date_start),
            "|",
            ("date_end", ">=", self.date_start),
            ("date_end", "=", False),
        ]
        assignment = obj_assignment.search(assignment_domain, limit=1)
        if not assignment:
            return
        obj_hr_timesheet = self.env["hr.timesheet"]
        previous_timesheet = obj_hr_timesheet.search(
            [
                ("employee_id", "=", employee.id),
                ("date_end", "<", self.date_start),
            ],
            order="date_end desc",
            limit=1,
        )
        if not previous_timesheet:
            return
        expected_date_start = previous_timesheet.date_end + timedelta(days=1)
        if self.date_start != expected_date_start:
            error_message = _(
                "Timesheet period must start one day after the " "previous period ends"
            )
            raise ValidationError(error_message)
