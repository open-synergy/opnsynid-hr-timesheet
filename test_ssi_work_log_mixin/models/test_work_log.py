# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class TestWorkLogMixin(models.Model):
    _name = "test.work_log_mixin"
    _description = "Test Work Log Mixin"
    _inherit = [
        "mixin.work_object",
    ]

    _work_log_create_page = True

    name = fields.Char(
        string="# Document",
        default="/",
    )
    code = fields.Char(
        string="Code",
        default="000",
    )
    note = fields.Text(
        string="Note",
    )
