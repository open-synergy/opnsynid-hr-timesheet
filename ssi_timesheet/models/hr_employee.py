# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class HrEmployeeBase(models.AbstractModel):
    _inherit = "hr.employee.base"
    _name = "hr.employee.base"

    timesheet_computation_ids = fields.Many2many(
        string="Timesheet Computations",
        comodel_name="hr.timesheet_computation_item",
        relation="rel_employee_2_timesheet_computation_id",
        column1="employee_id",
        column2="item_id",
    )
