# Copyright 2023 OpenSynergy Indonesia
# Copyright 2023 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class HRLeave(models.Model):
    _name = "hr.leave"
    _inherit = [
        "hr.leave",
        "mixin.state_change_constrain",
        "mixin.status_check",
    ]

    _status_check_create_page = True
