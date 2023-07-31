# Copyright 2023 OpenSynergy Indonesia
# Copyright 2023 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class HROvertime(models.Model):
    _name = "hr.overtime"
    _description = "Overtimes"
    _inherit = ["hr.overtime"]

    batch_id = fields.Many2one(
        comodel_name="hr.overtime_batch",
        string="Batch",
        ondelete="restrict",
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
