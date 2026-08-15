# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class HrLeaveAllocation(models.Model):
    """Add a single Operating Unit to ``hr.leave_allocation``.

    Inherits ``mixin.single_operating_unit`` so every leave allocation
    carries an ``operating_unit_id``, defaulting to the current user's
    default operating unit.
    """

    _name = "hr.leave_allocation"
    _inherit = [
        "hr.leave_allocation",
        "mixin.single_operating_unit",
    ]
