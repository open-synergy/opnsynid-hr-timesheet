# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class HrLeaveType(models.Model):
    _name = "hr.leave_type"
    _inherit = ["mixin.master_data"]
    _description = "Leave Type"

    name = fields.Char(
        string="Leave Type",
    )
    need_allocation = fields.Boolean(
        string="Need Allocation",
        default=False,
    )
    apply_limit_per_request = fields.Boolean(
        string="Apply Limit Per Request",
        default=False,
    )
    limit_per_request = fields.Integer(
        string="Limit Per Request",
        default=False,
    )
    exclude_public_holiday = fields.Boolean(
        string="Exclude Public Holiday",
        default=False,
    )
    exclude_rest_day = fields.Boolean(
        string="Exclude Rest Day",
        default=False,
    )
