# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class AccountAnalyticAccount(models.Model):
    _inherit = "account.analytic.account"

    allowed_work_log_user_ids = fields.Many2many(
        string="Allowed Work Log Responsible",
        comodel_name="res.users",
        relation="rel_acc_analytic_acc_2_user",
        column1="analytic_account_id",
        column2="user_id",
    )
