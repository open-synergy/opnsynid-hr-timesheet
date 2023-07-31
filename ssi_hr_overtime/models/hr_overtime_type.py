# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class HROvertimeType(models.Model):
    _name = "hr.overtime_type"
    _inherit = ["mixin.master_data"]
    _description = "Overtime Type"

    name = fields.Char(
        string="Type",
    )
    apply_limit_per_day = fields.Boolean(
        string="Apply Limit Per Days",
        default=False,
    )
    limit_per_day = fields.Integer(
        string="Limit Per Days",
        default=0,
    )
