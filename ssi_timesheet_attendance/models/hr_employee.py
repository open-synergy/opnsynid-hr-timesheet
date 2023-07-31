# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class HrEmployeeBase(models.AbstractModel):
    _inherit = "hr.employee.base"
    _name = "hr.employee.base"

    timesheet_ids = fields.One2many(
        string="Timesheet(s)",
        comodel_name="hr.timesheet",
        inverse_name="employee_id",
    )

    @api.depends(
        "timesheet_ids",
        "timesheet_ids.date_start",
        "timesheet_ids.date_end",
    )
    def _compute_active_timesheet_id(self):
        for record in self:
            result = False
            Timesheet = self.env["hr.timesheet"]
            criteria = [
                ("employee_id", "=", record.id),
                ("date_start", "<=", fields.Date.today()),
                ("date_end", ">=", fields.Date.today()),
            ]
            timesheets = Timesheet.search(criteria)
            if len(timesheets) > 0:
                result = timesheets[0]
            record.active_timesheet_id = result

    active_timesheet_id = fields.Many2one(
        string="Active Timesheet",
        comodel_name="hr.timesheet",
        compute="_compute_active_timesheet_id",
        store=True,
    )

    attendance_ids = fields.One2many(
        string="Attendance(s)",
        comodel_name="hr.timesheet_attendance",
        inverse_name="employee_id",
    )

    @api.depends("attendance_ids")
    def _compute_latest_attendance_id(self):
        for record in self:
            result = False
            if record.attendance_ids:
                result = record.attendance_ids[0]
            record.latest_attendance_id = result

    latest_attendance_id = fields.Many2one(
        string="Latest Attedance",
        comodel_name="hr.timesheet_attendance",
        compute="_compute_latest_attendance_id",
        store=True,
    )

    @api.depends(
        "latest_attendance_id",
    )
    def _compute_attendance_status(self):
        for record in self:
            result = "sign_out"
            if (
                record.latest_attendance_id
                and not record.latest_attendance_id.check_out
            ):
                result = "sign_in"
            record.attendance_status = result

    attendance_status = fields.Selection(
        string="Attendance Status",
        selection=[
            ("sign_in", "Sign In"),
            ("sign_out", "Sign Out"),
        ],
        compute="_compute_attendance_status",
        store=False,
    )

    def action_sign_in(self):
        for record in self.sudo():
            record._sign_in()

    def action_sign_out(self):
        for record in self.sudo():
            record._sign_out()

    def _sign_in(self):
        self.ensure_one()
        if not self.active_timesheet_id:
            error_message = _(
                """
            Context: Sign in from employee data
            Database ID: %s
            Problem: No active timesheet
            Solution: Create timesheet
            """
                % (self.id)
            )
            raise ValidationError(error_message)
        self.active_timesheet_id.action_sign_in()

    def _sign_out(self):
        self.ensure_one()
        if not self.active_timesheet_id:
            error_message = _(
                """
            Context: Sign out from employee data
            Database ID: %s
            Problem: No active timesheet
            Solution: Create timesheet
            """
                % (self.id)
            )
            raise ValidationError(error_message)
        self.active_timesheet_id.action_sign_out()
