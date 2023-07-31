# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class HRTimesheet(models.Model):
    _name = "hr.timesheet"
    _inherit = [
        "hr.timesheet",
        "mixin.state_change_constrain",
        "mixin.status_check",
    ]

    _status_check_create_page = True
