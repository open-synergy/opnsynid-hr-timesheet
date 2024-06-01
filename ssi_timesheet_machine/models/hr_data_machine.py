# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, fields, models
from odoo.exceptions import UserError


class HrDataMachine(models.Model):
    _name = "hr.data.machine"
    _inherit = ["mixin.master_data"]
    _description = "Attendance Machine"

    name = fields.Char(
        string="Machine",
    )
    device_id = fields.Char(
        string="Device ID",
    )
    user_ids = fields.One2many(
        comodel_name="hr.machine.user",
        inverse_name="machine_id",
        string="Users",
        required=False)

    def action_test_connection(self):
        pass
