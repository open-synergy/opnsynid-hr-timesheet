# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import models


class HrTimesheet(models.Model):
    _name = "hr.timesheet"
    _inherit = [
        "hr.timesheet",
        "mixin.documenso_signing",
    ]

    _documenso_signing_create_page = True
