# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, fields, models
from odoo.exceptions import UserError


class HrMachineUser(models.Model):
    _name = "hr.machine.user"
    _description = "Machine User"
    _rec_name = "employee_id"

    machine_id = fields.Many2one(
        comodel_name="hr.data.machine",
        string="Machine",
        ondelete="cascade"
    )
    pin = fields.Char(
        required=True,
        string="PIN",
    )
    employee_id = fields.Many2one(
        comodel_name="hr.employee",
        string="Employee",
        required=False
    )
    employee_name = fields.Char(
        related="employee_id.name",
        string="Employee Name",
    )
    device_id = fields.Char(
        string="Device ID",
        related="machine_id.device_id",
        store=True,
    )
