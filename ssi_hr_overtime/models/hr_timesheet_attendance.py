# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class HRTimesheetAttendance(models.Model):
    _name = "hr.timesheet_attendance"
    _inherit = "hr.timesheet_attendance"

    overtime_ids = fields.Many2many(
        string="Overtimes",
        comodel_name="hr.overtime",
        compute="_compute_overtime_ids",
        relation="rel_attendance_2_overtime",
        column1="attendance_id",
        column2="overtime_id",
        store=True,
        compute_sudo=True,
    )

    @api.depends(
        "check_in",
        "check_out",
        "employee_id",
    )
    def _compute_overtime_ids(self):
        obj_ot = self.env["hr.overtime"]
        data = []
        for record in self:
            if record.check_in and record.check_out and record.employee_id:
                criteria = [
                    "&",
                    ("employee_id", "=", record.employee_id.id),
                    "|",
                    "&",
                    ("date_start", "<=", record.check_out),
                    ("date_start", ">=", record.check_in),
                    "&",
                    ("date_end", "<=", record.check_out),
                    ("date_end", ">=", record.check_in),
                ]
                ot = obj_ot.search(criteria)
                data = ot.ids
                record.overtime_ids = data
