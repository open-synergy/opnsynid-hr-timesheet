# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class HRTimesheet(models.Model):
    _name = "hr.timesheet"
    _inherit = "hr.timesheet"

    leave_ids = fields.One2many(
        string="Leaves",
        comodel_name="hr.leave",
        inverse_name="sheet_id",
        readonly=True,
    )
