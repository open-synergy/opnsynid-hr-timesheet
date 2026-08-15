# Copyright 2023 OpenSynergy Indonesia
# Copyright 2023 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class HrLeave(models.Model):
    """
    Blocks ``hr.leave`` state transitions until configured Status Check
    items are satisfied. Adds ``mixin.state_change_constrain`` and
    ``mixin.status_check`` on top of the base leave document, so the
    ``state`` constraint enforces any active
    ``state.change.constrain.template`` that targets this model.
    """

    _name = "hr.leave"
    _inherit = [
        "hr.leave",
        "mixin.state_change_constrain",
        "mixin.status_check",
    ]

    _status_check_create_page = True
