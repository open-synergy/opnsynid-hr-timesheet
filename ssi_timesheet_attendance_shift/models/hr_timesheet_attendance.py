# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models


class HrTimesheetAttendance(models.Model):
    """Matches a shift-roster attendance to its schedule by time range.

    ``ssi_timesheet_attendance`` matches an attendance to a schedule
    line by exact calendar-date equality, which cannot represent a
    shift crossing midnight: a check-in after midnight would land on
    the wrong schedule line, or none at all. This module adds a
    tolerance-window, time-based match for timesheets whose Schedule
    Source is Shift Roster, and derives the attendance's business
    ``date`` from the matched schedule so the whole cross-day
    interval books under a single calendar date — the shift's start
    date. Timesheets whose Schedule Source is Working Schedule are
    untouched: they keep going through ``super()`` unchanged.
    """

    _inherit = "hr.timesheet_attendance"

    @api.depends(
        "check_in",
        "sheet_id",
        "sheet_id.schedule_source",
    )
    def _compute_schedule(self):
        """Match by check-in time window for shift-roster timesheets.

        Falls through to ``super()`` untouched whenever the owning
        timesheet (``sheet_id``) is empty or its ``schedule_source``
        is not ``shift`` — the Working Schedule branch inherited from
        ``ssi_timesheet_attendance`` is never modified by this
        module, and an attendance without a timesheet yet never
        raises because of this override. For Shift Roster timesheets,
        searches the employee's shift-generated schedule lines for
        the one whose tolerance window (``date_start`` minus the
        shift's early check-in tolerance, to ``date_end`` plus the
        shift's late check-out tolerance) contains ``check_in``; when
        several match, the one whose ``date_start`` is closest to
        ``check_in`` wins. When a match is found, ``date`` is
        overwritten with the matched schedule's ``date`` — the
        shift's start date. Falls back to ``super()`` when no
        schedule line matches, so a shift-roster attendance without a
        matching shift schedule never raises either.

        :return: nothing; assigns ``schedule_id`` and, only for a
            matched shift schedule, ``date``
        """
        obj_schedule = self.env["hr.timesheet_attendance_schedule"]
        for attn in self:
            if not attn.sheet_id or attn.sheet_id.schedule_source != "shift":
                super(HrTimesheetAttendance, attn)._compute_schedule()
                continue
            domain = [
                ("employee_id", "=", attn.employee_id.id),
                ("shift_id", "!=", False),
            ]
            candidates = obj_schedule.search(domain)
            matches = candidates.filtered(
                lambda schedule, attn=attn: schedule._match_shift_check_in(
                    attn.check_in
                )
            )
            if not matches:
                super(HrTimesheetAttendance, attn)._compute_schedule()
                continue
            best = min(
                matches,
                key=lambda schedule: abs(
                    (schedule.date_start - attn.check_in).total_seconds()
                ),
            )
            attn.schedule_id = best.id
            attn.date = best.date

    def _is_cross_day_shift_attendance(self):
        """Tell whether this attendance is pinned to a cross-day shift.

        Used by this module's ``hr.timesheet._sign_out()`` override to
        decide whether the date-anomaly branch inherited from
        ``ssi_timesheet_attendance`` should be skipped.

        :return: True when ``schedule_id.shift_id.cross_day`` is set
        """
        self.ensure_one()
        shift = self.schedule_id.shift_id
        return bool(shift and shift.cross_day)
