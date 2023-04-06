# Copyright 2023 OpenSynergy Indonesia
# Copyright 2023 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class WorkLogAccountingEntryType(models.Model):
    _name = "work_log_accounting_entry_type"
    _description = "Work Log To Accounting Entry Type"
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
    direction = fields.Selection(
        string="Direction",
        selection=[("income", "Income"), ("expense", "Expense")],
        default="income",
        required=True,
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
