# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import models


class HrLeaveAllocation(models.Model):
    _name = "hr.leave_allocation"
    _inherit = [
        "hr.leave_allocation",
        "mixin.documenso_signing_approval",
    ]

    _documenso_signing_create_page = True
