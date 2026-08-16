# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class HrLeaveRequestBatch(models.Model):
    """Add Operating Unit requirement to leave request batches.

    Pure ``_inherit`` extension: no method is added or overridden here.
    Mixing in ``mixin.single_operating_unit`` makes an Operating Unit
    mandatory on every ``hr.leave_request_batch`` record.
    """

    _name = "hr.leave_request_batch"
    _inherit = [
        "hr.leave_request_batch",
        "mixin.single_operating_unit",
    ]
