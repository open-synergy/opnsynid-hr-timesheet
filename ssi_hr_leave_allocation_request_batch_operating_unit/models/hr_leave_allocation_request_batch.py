# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class HrLeaveAllocationRequestBatch(models.Model):
    """Add operating unit ownership to leave allocation request batches.

    Mixes in ``mixin.single_operating_unit`` so every batch document
    carries an ``operating_unit_id``, gating its visibility to users
    granted the operating units the record belongs to (see the
    ``ir.rule`` shipped by this module).
    """

    _name = "hr.leave_allocation_request_batch"
    _inherit = [
        "hr.leave_allocation_request_batch",
        "mixin.single_operating_unit",
    ]
