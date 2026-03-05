# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class HrLeaveAllocationRequestBatch(models.Model):
    _name = "hr.leave_allocation_request_batch"
    _inherit = [
        "hr.leave_allocation_request_batch",
        "mixin.single_operating_unit",
    ]
