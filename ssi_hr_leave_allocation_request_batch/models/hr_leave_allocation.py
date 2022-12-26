# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class HrLeaveAllocation(models.Model):
    _inherit = "hr.leave_allocation"

    batch_id = fields.Many2one(
        comodel_name="hr.leave_allocation_request_batch", string="Batch"
    )
