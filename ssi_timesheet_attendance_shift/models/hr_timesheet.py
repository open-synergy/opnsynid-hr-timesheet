# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from datetime import datetime, timedelta

import pytz

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class HrTimesheet(models.Model):
    """
    Adds a shift-roster based schedule generator to ``hr.timesheet``.
    Lets a timesheet pick between the pre-existing working-schedule
    generation (``resource.calendar``-based, untouched by this
    module) and a shift-roster generation that walks the employee's
    ``hr.attendance_shift_assignment`` day by day and produces one
    schedule line per shift, able to cross midnight as a single
    block instead of being split at day boundaries.
    """

    _inherit = "hr.timesheet"

    schedule_source = fields.Selection(
        string="Schedule Source",
        selection=[
            ("working_schedule", "Working Schedule"),
            ("shift", "Shift Roster"),
        ],
        required=True,
        default="working_schedule",
        readonly=True,
        states={
            "draft": [("readonly", False)],
        },
        help=(
            "Where this timesheet's attendance schedule "
            "(``schedule_ids``) is generated from. Working Schedule "
            "keeps the pre-existing resource.calendar-based "
            "generation; Shift Roster generates one schedule line "
            "per shift from the employee's rotation assignment "
            "instead."
        ),
    )
    working_schedule_id = fields.Many2one(
        required=False,
    )

    @api.constrains("schedule_source", "working_schedule_id")
    def _check_working_schedule_id_required(self):
        """Reject a missing Working Schedule when it is still needed.

        :raises ValidationError: when ``schedule_source`` is
            ``working_schedule`` and ``working_schedule_id`` is empty
        """
        for record in self.sudo():
            if not record._check_working_schedule_id_required_condition():
                error_message = (
                    "Working schedule is required when schedule "
                    "source is working schedule"
                )
                raise ValidationError(_(error_message))

    def _check_working_schedule_id_required_condition(self):
        """Tell whether Working Schedule is set when it is required.

        Reproduces, unchanged, the obligation the field used to
        enforce unconditionally as ``required=True`` — now scoped to
        the ``working_schedule`` source only.

        Extension point: override to relax or tighten the condition.

        :return: True when valid; never raises
        """
        self.ensure_one()
        if self.schedule_source == "working_schedule":
            return bool(self.working_schedule_id)
        return True

    @api.onchange("employee_id")
    def onchange_schedule_source(self):
        self.schedule_source = "working_schedule"
        if self.employee_id:
            self.schedule_source = self.employee_id.schedule_source

    def _get_schedule_data(self):
        """Dispatch schedule generation by ``schedule_source``.

        Falls through to ``super()`` untouched when the source is
        not ``shift`` — the working-schedule branch is never
        modified by this module. When the source is ``shift``, walks
        every calendar date from ``date_start`` to ``date_end``
        (inclusive) and, for each date, resolves the shift owned by
        that date via ``_get_shift_for_date``. A shift is owned by
        its *start* date only: the generated line's end may extend
        past ``date_end`` without being clipped, and a shift starting
        on the period's last day is booked whole into this period —
        the next period will not regenerate it.

        :return: list of ``(0, 0, values)`` tuples for
            ``schedule_ids``
        """
        self.ensure_one()
        if self.schedule_source != "shift":
            return super(HrTimesheet, self)._get_schedule_data()
        res = []
        if not (self.employee_id and self.date_start and self.date_end):
            return res
        obj_public_holiday = self.env["base.public.holiday"]
        tz = self._get_shift_timezone()
        num_days = (self.date_end - self.date_start).days
        for offset in range(num_days + 1):
            date_check = self.date_start + timedelta(days=offset)
            shift = self._get_shift_for_date(self.employee_id, date_check)
            if not shift:
                continue
            if obj_public_holiday.is_public_holiday(date_check, self.employee_id.id):
                continue
            naive_start = datetime.combine(date_check, datetime.min.time()) + timedelta(
                hours=shift.hour_start
            )
            start_dt = tz.localize(naive_start)
            stop_dt = start_dt + timedelta(hours=shift.duration)
            schedule_data = self._prepare_schedule_data(start_dt, stop_dt)
            schedule_data["shift_id"] = shift.id
            res.append((0, 0, schedule_data))
        return res

    def _get_shift_timezone(self):
        """Resolve the timezone used to localize shift start times.

        Falls back in order: the employee's resource timezone, the
        employee's company calendar timezone, the current user's
        timezone, then UTC. The result is always applied with
        ``pytz``'s ``localize()`` — never
        ``datetime.replace(tzinfo=...)``, which would produce a
        historical LMT offset instead of the real UTC offset.

        :return: a ``pytz`` timezone object
        """
        self.ensure_one()
        tz_name = (
            self.employee_id.resource_id.tz
            or self.employee_id.company_id.resource_calendar_id.tz
            or self.env.user.tz
            or "UTC"
        )
        return pytz.timezone(tz_name)

    def _sign_out(self, reason=False):
        """Close a cross-day shift attendance, skipping the anomaly path.

        Delegates unchanged to ``super()`` unless the employee's open
        attendance (``latest_attendance_id``) is pinned to a schedule
        line generated from a shift whose ``cross_day`` is True. For
        such an attendance, a check-out landing on the next calendar
        day is expected, not an anomaly: the date-mismatch comparison
        and ``checkout_buffer`` branch inherited from
        ``ssi_timesheet_attendance`` — which would otherwise leave
        the attendance open and create a new one — are skipped
        entirely, and the open attendance is closed directly. Every
        other case, including shift attendances that do not cross a
        day, keeps going through the inherited anomaly branch
        unchanged.

        :param reason: ``hr.attendance_reason`` record for the
            check-out, or a falsy value
        :return: nothing
        """
        self.ensure_one()
        latest_attendance_id = self.employee_id.latest_attendance_id
        if (
            latest_attendance_id
            and latest_attendance_id._is_cross_day_shift_attendance()
        ):
            latest_attendance_id.write(
                self._prepare_attendance_data_update(reason=reason)
            )
            return
        super(HrTimesheet, self)._sign_out(reason=reason)

    def _get_shift_for_date(self, employee, date_check):
        """Resolve the shift an employee's roster assigns on a date.

        Searches ``hr.attendance_shift_assignment`` for the
        assignment covering ``date_check``, then resolves the
        day-in-cycle against its pattern to read the matching detail
        line's shift. This is the official override point for a
        separate roster-resolution module: extend this method,
        never re-implement pattern resolution inside
        ``_get_schedule_data``.

        :param employee: ``hr.employee`` record the shift is looked
            up for
        :param date_check: ``datetime.date`` the shift is looked up
            on
        :return: ``hr.attendance_shift`` recordset, empty when the
            employee has no active assignment on ``date_check`` or
            the matching cycle day is a day off
        """
        self.ensure_one()
        obj_assignment = self.env["hr.attendance_shift_assignment"]
        domain = [
            ("employee_id", "=", employee.id),
            ("date_start", "<=", date_check),
            "|",
            ("date_end", ">=", date_check),
            ("date_end", "=", False),
        ]
        assignment = obj_assignment.search(domain, limit=1)
        if not assignment:
            return self.env["hr.attendance_shift"]
        pattern = assignment.pattern_id
        day_in_cycle = (
            (date_check - pattern.date_anchor).days - assignment.cycle_offset
        ) % pattern.cycle_length + 1
        detail = pattern.detail_ids.filtered(lambda d: d.day_index == day_in_cycle)
        if not detail or not detail.shift_id:
            return self.env["hr.attendance_shift"]
        return detail.shift_id
