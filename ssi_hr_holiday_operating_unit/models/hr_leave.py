# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class HrLeave(models.Model):
    """Add a single Operating Unit to ``hr.leave``.

    Inherits ``mixin.single_operating_unit`` so every leave request
    carries an ``operating_unit_id``, defaulting to the current user's
    default operating unit.
    """

    _name = "hr.leave"
    _inherit = [
        "hr.leave",
        "mixin.single_operating_unit",
    ]
