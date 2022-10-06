# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class HrTimesheet(models.Model):
    _name = "hr.timesheet"
    _inherit = [
        "hr.timesheet",
        "mixin.work_object",
    ]

    _work_log_create_page = True

    all_work_log_ids = fields.One2many(
        string="All Work Logs",
        comodel_name="hr.work_log",
        inverse_name="sheet_id",
        readonly=True,
    )
