# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class HrWorkLogTag(models.Model):
    _name = "hr.work_log_tag"
    _inherit = ["mixin.master_data"]
    _description = "Work Log Tag"

    name = fields.Char(
        string="Work Log Tag",
    )
