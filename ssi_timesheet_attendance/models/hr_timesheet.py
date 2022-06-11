# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models


class HRTimesheet(models.Model):
    _inherit = "hr.timesheet"

    @api.depends(
        "attendance_ids",
        "attendance_ids.check_in",
        "attendance_ids.check_out",
    )
    def _compute_total_attendance(self):
        for sheet in self:
            sheet.total_attendance = 0.0
            # for attendance in sheet.attendance_ids.sorted(key=lambda r: r.check_in:
            for attendance in sheet.attendance_ids:
                sheet.total_attendance += attendance.total_hour

    working_schedule_id = fields.Many2one(
        string="Working Schedule",
        comodel_name="resource.calendar",
        # related="employee_id.resource_calendar_id",
        store=True,
    )
    total_attendance = fields.Float(
        string="Total Attendance",
        compute="_compute_total_attendance",
        store=True,
    )
    attendance_ids = fields.One2many(
        string="Attendances",
        comodel_name="hr.timesheet_attendance",
        inverse_name="sheet_id",
        readonly=True,
        states={
            "open": [
                ("readonly", False),
            ],
        },
    )
    schedule_ids = fields.One2many(
        string="Attendance Schedule",
        comodel_name="hr.timesheet_attendance_schedule",
        inverse_name="sheet_id",
        readonly=True,
        states={
            "drafSt": [
                ("readonly", False),
            ],
            "open": [
                ("readonly", False),
            ],
        },
    )

    @api.onchange(
        "employee_id",
    )
    def onchange_working_schedule_id(self):
        self.working_schedule_id = False
        if self.employee_id:
            self.working_schedule_id = self.employee_id.resource_calendar_id

    # def _create_schedule(self):
