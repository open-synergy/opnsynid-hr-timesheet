# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class WorkLogRateGeneralRate(models.Model):
    _name = "work_log_rate.general_rate"
    _description = "Work Log Rate - General"

    rate_id = fields.Many2one(
        string="# Rate",
        comodel_name="work_log_rate",
        required=True,
        ondelete="cascade",
    )
    product_id = fields.Many2one(
        string="Product",
        comodel_name="product.product",
        required=True,
        ondelete="restrict",
    )
    pricelist_id = fields.Many2one(
        string="Pricelist",
        comodel_name="product.pricelist",
        required=True,
        ondelete="restrict",
    )
