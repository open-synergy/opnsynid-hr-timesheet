# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
from openerp import fields, models


class HrLeave(models.Model):
    _inherit = "hr.leave"

    batch_id = fields.Many2one(
        string="Batch ID",
        comodel_name="hr.leave_request_batch",
        ondelete="restrict",
        readonly=True,
    )
