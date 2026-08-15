# Copyright 2023 OpenSynergy Indonesia
# Copyright 2023 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class HrLeaveAllocation(models.Model):
    """
    Blocks ``hr.leave_allocation`` state transitions until configured
    Status Check items are satisfied. Adds
    ``mixin.state_change_constrain`` and ``mixin.status_check`` on top
    of the base leave allocation document, so the ``state`` constraint
    enforces any active ``state.change.constrain.template`` that
    targets this model.
    """

    _name = "hr.leave_allocation"
    _inherit = [
        "hr.leave_allocation",
        "mixin.state_change_constrain",
        "mixin.status_check",
    ]

    _status_check_create_page = True
