# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class HrLeave(models.Model):
    """
    Links a time off request back to the batch that produced it.

    Requests created one by one leave the batch reference empty; only
    those materialised by ``hr.leave_request_batch`` carry it. The link
    is what lets the batch relay its own transitions to its children and
    keeps the origin of a mass-granted leave auditable.
    """

    _inherit = "hr.leave"

    batch_id = fields.Many2one(
        string="# Batch",
        comodel_name="hr.leave_request_batch",
        ondelete="restrict",
    )
