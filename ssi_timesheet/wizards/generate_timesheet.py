# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import _, fields, models
from odoo.exceptions import UserError


class GenerateTimesheet(models.TransientModel):
    _name = "hr.generate_timesheet"
    _inherit = [
        "mixin.date_duration",
    ]
    _description = "Generate Timesheet"

    employee_ids = fields.Many2many(
        string="Employee",
        comodel_name="hr.employee",
        relation="rel_hr_employee_2_generate_timesheet",
        column1="wizard_id",
        column2="employee_id",
        required=True,
    )
    working_schedule_id = fields.Many2one(
        string="Working Schedule",
        comodel_name="resource.calendar",
    )

    def _prepare_data_timesheet(self, employee):
        self.ensure_one()
        data = {}
        if self._check_data(employee):
            working_schedule_id = (
                self.working_schedule_id
                and self.working_schedule_id.id
                or employee.resource_calendar_id.id
            )
            data = {
                "employee_id": employee.id,
                "working_schedule_id": working_schedule_id,
                "date_start": self.date_start,
                "date_end": self.date_end,
            }
        return data

    def _check_data(self, employee):
        self.ensure_one()
        obj_hr_timesheet = self.env["hr.timesheet"]

        if not employee.user_id:
            msg_error = _("Employee %s must be linked to a user.") % (employee.name)
            raise UserError(msg_error)

        if not employee.resource_calendar_id:
            msg_error = _("Employee %s must have working schedule.") % (employee.name)
            raise UserError(msg_error)

        criteria = [
            ("employee_id", "=", employee.id),
            ("date_start", "<=", self.date_start),
            ("date_end", ">=", self.date_end),
        ]

        timesheet = obj_hr_timesheet.search(criteria)

        if timesheet:
            msg_error = _("Timesheet already exists for %s.") % (employee.name)
            raise UserError(msg_error)
        return True

    def _trigger_timesheet_onchange(self, timesheet):
        self.ensure_one()
        timesheet.onchange_department_id()
        timesheet.onchange_manager_id()
        timesheet.onchange_job_id()
        timesheet.action_compute_schedule()

    def action_generate(self):
        self.ensure_one()
        obj_hr_timesheet = self.env["hr.timesheet"]
        for employee in self.employee_ids:
            data = self._prepare_data_timesheet(employee)
            timesheet = obj_hr_timesheet.create(data)
            if timesheet:
                self._trigger_timesheet_onchange(timesheet)
