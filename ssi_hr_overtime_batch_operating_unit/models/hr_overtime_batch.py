# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class HrOvertimeBatch(models.Model):
    """Add Operating Unit requirement to overtime batches.

    Pure ``_inherit`` extension: no method is added or overridden here.
    Mixing in ``mixin.single_operating_unit`` makes an Operating Unit
    mandatory on every ``hr.overtime_batch`` record, gating its
    visibility to users granted the operating units the record belongs
    to (see the ``ir.rule`` shipped by this module).
    """

    _name = "hr.overtime_batch"
    _inherit = [
        "hr.overtime_batch",
        "mixin.single_operating_unit",
    ]
