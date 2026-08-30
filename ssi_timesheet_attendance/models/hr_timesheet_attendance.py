# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from datetime import datetime

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools import format_datetime


class HRTimesheetAttendance(models.Model):
    _name = "hr.timesheet_attendance"
    _description = "Timesheet Attendance"
    _order = "date desc,check_in desc"

    @api.model
    def _default_employee_id(self):
        return self.env.user.employee_id

    date = fields.Date(
        string="Date",
        required=True,
    )

    @api.depends("date", "employee_id")
    def _compute_sheet(self):
        """Resolve the open ``hr.timesheet`` sheet covering ``date``.

        :raises UserError: if ``date`` is set but no open sheet covers it.
        """
        obj_sheet = self.env["hr.timesheet"]
        for record in self:
            if not record.date:
                # New/incomplete record: nothing to search for yet. Leave
                # ``sheet_id`` empty instead of raising - the required
                # constraint on ``sheet_id`` will block save until ``date``
                # (and therefore ``sheet_id``) is filled in.
                record.sheet_id = False
                continue
            criteria = [
                ("employee_id", "=", record.employee_id.id),
                ("date_start", "<=", record.date),
                ("date_end", ">=", record.date),
                ("state", "=", "open"),
            ]
            sheet = obj_sheet.search(criteria, limit=1)
            if len(sheet) > 0:
                record.sheet_id = sheet[0].id
            else:
                strWarning = _(
                    "Sheet Not FOUND .. Check in "
                    + fields.Datetime.context_timestamp(self, record.check_in).strftime(
                        "%m/%d/%Y, %H:%M:%S"
                    )
                )
                raise UserError(strWarning)

    sheet_id = fields.Many2one(
        string="Sheet",
        comodel_name="hr.timesheet",
        ondelete="cascade",
        required=True,
        compute="_compute_sheet",
        store=True,
        compute_sudo=True,
    )
    check_in = fields.Datetime(
        string="Check In",
        default=fields.Datetime.now,
        required=True,
    )
    check_out = fields.Datetime(
        string="Check Out",
    )

    @api.depends(
        "check_in",
        "check_out",
    )
    def _compute_state(self):
        for attn in self:
            if attn.check_in and attn.check_out:
                attn.state = "present"
            elif (attn.check_in and not attn.check_out) or (
                not attn.check_in and attn.check_out
            ):
                attn.state = "open"

    state = fields.Selection(
        string="State",
        selection=[
            ("open", "Open"),
            ("present", "Present"),
        ],
        default="open",
        required=True,
        compute="_compute_state",
        store=True,
        compute_sudo=True,
    )

    employee_id = fields.Many2one(
        string="Employee",
        comodel_name="hr.employee",
        default=lambda self: self._default_employee_id(),
        required=True,
        ondelete="restrict",
    )
    schedule_id = fields.Many2one(
        string="Attendance Schedule",
        comodel_name="hr.timesheet_attendance_schedule",
        compute="_compute_schedule",
        store=True,
        compute_sudo=True,
    )
    valid_check_in = fields.Datetime(
        string="Valid Check In",
        compute="_compute_valid",
        store=True,
        compute_sudo=True,
    )
    valid_check_out = fields.Datetime(
        string="Valid Check Out",
        compute="_compute_valid",
        store=True,
        compute_sudo=True,
    )
    total_hour = fields.Float(
        string="Total Hour",
        compute="_compute_hour",
        store=True,
        compute_sudo=True,
    )
    total_valid_hour = fields.Float(
        string="Total Valid Hour",
        compute="_compute_valid",
        store=True,
        compute_sudo=True,
    )
    reason_check_in_id = fields.Many2one(
        string="Reason In",
        comodel_name="hr.attendance_reason",
        ondelete="restrict",
    )
    reason_check_out_id = fields.Many2one(
        string="Reason Out",
        comodel_name="hr.attendance_reason",
        ondelete="restrict",
    )
    check_in_latitude = fields.Float(
        string="Check In Latitude",
        digits=(16, 7),
        readonly=True,
        help="Device latitude recorded at check-in time. Filled by the "
        "attendance mobile client; 0.0 on records created without a "
        "geolocation reading (menu, Sign In/Sign Out, top bar widget).",
    )
    check_in_longitude = fields.Float(
        string="Check In Longitude",
        digits=(16, 7),
        readonly=True,
        help="Device longitude recorded at check-in time. Filled by the "
        "attendance mobile client; 0.0 on records created without a "
        "geolocation reading (menu, Sign In/Sign Out, top bar widget).",
    )
    check_in_accuracy = fields.Float(
        string="Check In Accuracy",
        digits=(16, 2),
        readonly=True,
        help="Accuracy of the check-in location reading, in meters, as "
        "reported by the device. 0.0 when no geolocation reading was "
        "taken.",
    )
    check_out_latitude = fields.Float(
        string="Check Out Latitude",
        digits=(16, 7),
        readonly=True,
        help="Device latitude recorded at check-out time. Filled by the "
        "attendance mobile client; 0.0 on records created without a "
        "geolocation reading (menu, Sign In/Sign Out, top bar widget).",
    )
    check_out_longitude = fields.Float(
        string="Check Out Longitude",
        digits=(16, 7),
        readonly=True,
        help="Device longitude recorded at check-out time. Filled by the "
        "attendance mobile client; 0.0 on records created without a "
        "geolocation reading (menu, Sign In/Sign Out, top bar widget).",
    )
    check_out_accuracy = fields.Float(
        string="Check Out Accuracy",
        digits=(16, 2),
        readonly=True,
        help="Accuracy of the check-out location reading, in meters, as "
        "reported by the device. 0.0 when no geolocation reading was "
        "taken.",
    )

    @api.constrains(
        "check_in_latitude",
        "check_in_longitude",
        "check_out_latitude",
        "check_out_longitude",
    )
    def _check_geolocation_range(self):
        """Validate that latitude/longitude stay within valid ranges.

        Devices leave these fields at their default ``0.0`` on every
        record that never captures geolocation - menu-created rows,
        the **Sign In** / **Sign Out** actions, and the top bar
        widget - so ``0.0`` and the ``(0, 0)`` pair are intentionally
        accepted here. Only a value genuinely outside a valid
        latitude/longitude range is rejected; accuracy is not
        validated, since its acceptable threshold is an operational
        policy, not a modeling constraint.

        :raises ValidationError: if a latitude is outside ``-90..90``
            or a longitude is outside ``-180..180``.
        """
        for record in self:
            for fname in ("check_in_latitude", "check_out_latitude"):
                value = record[fname]
                if value < -90.0 or value > 90.0:
                    raise ValidationError(
                        _("Latitude must be between -90 and 90 degrees.")
                    )
            for fname in ("check_in_longitude", "check_out_longitude"):
                value = record[fname]
                if value < -180.0 or value > 180.0:
                    raise ValidationError(
                        _("Longitude must be between -180 and 180 degrees.")
                    )

    @api.depends(
        "date",
        "check_in",
    )
    def _compute_check_date(self):
        for record in self:
            result = False
            if record.check_in and record.date:
                conv_dt = format_datetime(
                    self.env, record.check_in, dt_format="yyyy-MM-dd"
                )
                date_check_in = datetime.strptime(conv_dt, "%Y-%m-%d").date()
                if record.date != date_check_in:
                    result = True
            record.check_date = result

    check_date = fields.Boolean(
        string="Check Date",
        compute="_compute_check_date",
        help="Date is not the same as check in",
        store=True,
    )

    @api.depends(
        "schedule_id",
        "schedule_id.date_start",
        "schedule_id.date_end",
        "check_in",
        "check_out",
    )
    def _compute_valid(self):
        """Derive the valid check-in/out window and its duration.

        ``valid_check_in``/``valid_check_out`` are the start/end of
        the intersection between ``[check_in, check_out]`` and
        ``[schedule_id.date_start, schedule_id.date_end]``.
        ``total_valid_hour`` is that intersection's duration, in
        hours. All three fields are assigned on every branch -
        including the branch where no valid window exists - so a
        stale value from a previous computation never survives.

        :raises: nothing; the absence of a valid window is not an
            error, it yields ``False``/``0.0``.
        """
        for record in self:
            valid_check_in = valid_check_out = False
            total_valid_hour = 0.0
            if (
                record.schedule_id.date_start
                and record.schedule_id.date_end
                and record.check_in
                and record.check_out
            ):
                if (
                    record.check_out > record.schedule_id.date_start
                    and record.check_in < record.schedule_id.date_end
                    and record.check_out > record.check_in
                    and record.schedule_id.date_end > record.schedule_id.date_start
                ):
                    date_start = max(record.schedule_id.date_start, record.check_in)
                    date_end = min(record.schedule_id.date_end, record.check_out)
                    delta = date_end - date_start
                    total_valid_hour = delta.total_seconds() / 3600.0
                    valid_check_in = date_start
                    valid_check_out = date_end
            record.valid_check_in = valid_check_in
            record.valid_check_out = valid_check_out
            record.total_valid_hour = total_valid_hour

    @api.depends(
        "check_in",
        "check_out",
    )
    def _compute_hour(self):
        for record in self:
            result = 0.0
            if record.check_in and record.check_out:
                result = (record.check_out - record.check_in).total_seconds() / 3600.0
            record.total_hour = result

    @api.depends(
        "date",
        "check_in",
        "employee_id",
    )
    def _compute_schedule(self):
        """Resolve the schedule slot that covers this attendance.

        Runs a three-tier search, per record, stopping at the first
        tier that matches - always among slots of the same
        ``employee_id`` and always with an explicit ``order`` so the
        result is deterministic even when more than one slot could
        match:

        1. the slot whose ``date_start``/``date_end`` window
           **contains** ``check_in``, without any date filter - this
           also covers a check-in that falls after midnight on a
           shift that started the day before;
        2. failing that, among the slots dated ``date``, the one
           whose ``date_start`` is **closest** to ``check_in`` - this
           covers an early arrival or a late departure that falls
           outside every slot's window;
        3. failing both, ``schedule_id`` is left ``False`` - a
           legitimate outcome for attendance recorded on a day with
           no schedule slot (holiday, unplanned overtime, or an
           employee without a schedule).

        :raises: nothing; an unresolved schedule is not an error.
        """
        obj_schedule = self.env["hr.timesheet_attendance_schedule"]
        for attn in self:
            schedule = obj_schedule.browse()
            if attn.check_in:
                schedule = obj_schedule.search(
                    [
                        ("employee_id", "=", attn.employee_id.id),
                        ("date_start", "<=", attn.check_in),
                        ("date_end", ">=", attn.check_in),
                    ],
                    order="date_start",
                    limit=1,
                )
            if not schedule:
                candidates = obj_schedule.search(
                    [
                        ("employee_id", "=", attn.employee_id.id),
                        ("date", "=", attn.date),
                    ],
                    order="date_start",
                )
                if candidates:
                    if attn.check_in:
                        schedule = min(
                            candidates,
                            key=lambda candidate: abs(
                                (candidate.date_start - attn.check_in).total_seconds()
                            ),
                        )
                    else:
                        schedule = candidates[0]
            attn.schedule_id = schedule.id if schedule else False

    @api.model
    def create(self, values):
        """Create the attendance and refresh its daily summary date.

        Only the newly created record's own ``date`` is affected, so
        ``generate_daily_summary()`` is called with that single date
        instead of sweeping the whole sheet.

        :param values: field values for the new record
        :return: the created ``hr.timesheet_attendance`` record
        """
        res = super(HRTimesheetAttendance, self).create(values)
        res.sheet_id.generate_daily_summary(dates=[res.date])
        return res

    def write(self, values):
        """Update the attendance and refresh the affected summaries.

        The dates in effect *before* this write are captured first,
        since ``super().write()`` overwrites them; the daily summary
        is then regenerated for the union of the old and new dates,
        so moving an attendance from one date to another refreshes
        both the origin and the destination summaries. ``date`` is a
        required field, so both the pre-write and post-write values
        are always set on an existing record -- no falsy guard is
        needed around either one.

        :param values: field values to write
        :return: the value returned by the parent ``write()``
        """
        old_date_by_id = {rec.id: rec.date for rec in self}
        res = super(HRTimesheetAttendance, self).write(values)
        for rec in self:
            if "date" in values or "check_in" in values or "check_out" in values:
                affected_dates = {old_date_by_id[rec.id], rec.date}
                rec.sheet_id.generate_daily_summary(dates=affected_dates)
        return res
