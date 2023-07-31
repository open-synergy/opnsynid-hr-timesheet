# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    checkout_buffer = fields.Float(
        related="company_id.checkout_buffer",
        readonly=False,
    )
    check_out_reason_id = fields.Many2one(
        related="company_id.check_out_reason_id",
        readonly=False,
    )
    check_in_reason_id = fields.Many2one(
        related="company_id.check_in_reason_id",
        readonly=False,
    )
