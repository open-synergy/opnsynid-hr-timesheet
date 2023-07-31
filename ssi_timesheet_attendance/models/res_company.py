# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    checkout_buffer = fields.Float(
        string="Check Out Buffer",
        digits=(2, 2),
    )
    check_out_reason_id = fields.Many2one(
        string="Check Out Reason",
        comodel_name="hr.attendance_reason",
    )
    check_in_reason_id = fields.Many2one(
        string="Check In Reason",
        comodel_name="hr.attendance_reason",
    )
