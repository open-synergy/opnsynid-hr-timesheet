# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class HrLeave(models.Model):
    _inherit = "hr.leave"

    batch_id = fields.Many2one(
        "hr.leave_request_batch", string="Batch", ondelete="restrict"
    )
