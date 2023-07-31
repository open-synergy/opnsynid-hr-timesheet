# Copyright 2023 OpenSynergy Indonesia
# Copyright 2023 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class HRWorkLog(models.Model):
    _name = "hr.work_log"
    _inherit = ["hr.work_log"]

    expense_id = fields.Many2one(
        comodel_name="work_log_expense",
        string="# Expense",
        required=False,
        ondelete="set null",
    )

    def _update_summary(self):
        summary = self.env["work_log_expense_summary"].search(
            [
                ("account_id", "=", self.account_id.id),
                ("expense_id", "=", self.expense_id.id),
                ("product_id", "=", self.product_id.id),
                ("analytic_account_id", "=", self.analytic_account_id.id),
            ]
        )
        if len(summary) > 0:
            self._update_expense_summary(summary[0])
        elif len(summary) == 0:
            self._create_expense_summary()

    def _create_expense_summary(self):
        self.env["work_log_expense_summary"].create(
            self._prepare_create_expense_summary()
        )

    def _prepare_create_expense_summary(self):
        result = {
            "expense_id": self.expense_id.id,
            "account_id": self.account_id.id,
            "analytic_account_id": self.analytic_account_id.id,
            "product_id": self.product_id.id,
            "amount": self.price_subtotal,
        }
        return result

    def _update_expense_summary(self, summary):
        summary.write(
            {
                "amount": summary.amount + self.price_subtotal,
            }
        )
