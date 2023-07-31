# Copyright 2023 OpenSynergy Indonesia
# Copyright 2023 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, fields, models


class WorkLogExpenseSummary(models.Model):
    _name = "work_log_expense_summary"
    _description = "Work Log Expense Summary"

    expense_id = fields.Many2one(
        comodel_name="work_log_expense",
        string="# Expense",
        required=True,
        ondelete="cascade",
    )
    analytic_account_id = fields.Many2one(
        comodel_name="account.analytic.account",
        string="Analytic Account",
        required=True,
        ondelete="restrict",
    )
    account_id = fields.Many2one(
        comodel_name="account.account",
        string="Account",
        required=True,
        ondelete="restrict",
    )
    product_id = fields.Many2one(
        comodel_name="product.product",
        string="Product",
        required=True,
        ondelete="restrict",
    )
    amount = fields.Float(
        string="Amount",
    )
    move_line_id = fields.Many2one(
        string="Move Line",
        comodel_name="account.move.line",
        readonly=True,
    )

    def _create_aml(
        self,
    ):
        self.ensure_one()
        move = self.expense_id.move_id
        name = "Work log expense - %s" % (self.product_id.name)
        ml = (
            self.env["account.move.line"]
            .with_context(check_move_validity=False)
            .create(
                {
                    "name": _(name),
                    "move_id": move.id,
                    "account_id": self.account_id.id,
                    "analytic_account_id": self.analytic_account_id.id,
                    "product_id": self.product_id.id,
                    "partner_id": self.expense_id.employee_id.address_home_id.id,
                    "debit": self.amount,
                    "credit": 0.0,
                }
            )
        )
        self.write(
            {
                "move_line_id": ml.id,
            }
        )
