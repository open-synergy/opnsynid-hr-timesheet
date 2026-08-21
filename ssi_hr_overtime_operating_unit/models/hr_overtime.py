# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class HrOvertime(models.Model):
    """Adds Operating Unit ownership to overtime documents.

    Restricts each overtime record to a single operating unit via
    ``mixin.single_operating_unit``, enabling operating unit based
    visibility and security rules for the document.
    """

    _name = "hr.overtime"
    _inherit = [
        "hr.overtime",
        "mixin.single_operating_unit",
    ]
