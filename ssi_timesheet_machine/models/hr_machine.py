# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, fields, models
from odoo.exceptions import UserError


class HrMachine(models.Model):
    _name = "hr.machine"
    _inherit = ["mixin.master_data"]
    _description = "Attendance Machine"

    name = fields.Char(
        string="Machine",
    )

    def action_test_connection(self):
        pass
