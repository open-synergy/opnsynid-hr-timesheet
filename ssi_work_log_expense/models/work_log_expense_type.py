# Copyright 2023 OpenSynergy Indonesia
# Copyright 2023 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class WorkLogExpenseType(models.Model):
    _name = "work_log_expense_type"
    _description = "Work Log To Expense Type"
    _inherit = ["mixin.master_data"]

    accrue_account_id = fields.Many2one(
        comodel_name="account.account",
        string="Account",
        required=True,
        ondelete="restrict",
    )
    journal_id = fields.Many2one(
        comodel_name="account.journal",
        string="Journal",
        required=True,
        ondelete="restrict",
    )
    allowed_analytic_group_ids = fields.Many2many(
        comodel_name="account.analytic.group",
        string="Allowed Analytic Groups",
        relation="rel_work_log_acc_entry_type_2_group",
        column1="type_id",
        column2="group_id",
    )
    allowed_analytic_account_ids = fields.Many2many(
        comodel_name="account.analytic.account",
        string="Allowed Analytic Accounts",
        relation="rel_work_log_acc_entry_type_2_account",
        column1="type_id",
        column2="account_id",
    )
