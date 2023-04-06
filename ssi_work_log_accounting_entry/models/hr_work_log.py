# Copyright 2023 OpenSynergy Indonesia
# Copyright 2023 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class HRWorkLog(models.Model):
    _name = "hr.work_log"
    _inherit = ["hr.work_log"]

    accounting_entry_id = fields.Many2one(
        comodel_name="work_log_accounting_entry",
        string="Accounting Entry",
        required=True,
        # ondelete="set null"
    )

    def _update_summary(self, work_log_accounting_entry_type):
        summary = self.env["work_log_accounting_summary"].search(
            [
                ("account_id", "=", self.account_id.id),
                ("accounting_entry_id", "=", self.accounting_entry_id.id),
                ("product_id", "=", self.product_id.id),
            ]
        )
        if len(summary) > 0:
            self._update_accounting_entry_summary(summary[0])
        elif len(summary) == 0:
            self._create_accounting_entry_summary()

    def _create_accounting_entry_summary(self):
        self.env["work_log_accounting_entry_summary"].create(
            {self._prepare_create_accounting_entry_summary()}
        )

    def _prepare_create_accounting_entry_summary(self):
        debit = self._get_debit_credit()
        credit = self._get_debit_credit()
        result = {
            "accounting_entry_id": self.accounting_entry_id.id,
            "account_id": self.account_id.id,
            "product_id": self.product_id.id,
            "debit": debit,
            "credit": credit,
        }
        return result

    def _get_debit_credit(self):
        ttype = self.accounting_entry_id.type_id
        if ttype.direction == "income":
            debit = 0.0
            credit = self.price_subtotal
        elif ttype.direction == "expense":
            credit = 0.0
            debit = self.price_subtotal

        return {credit, debit}

    def _update_accounting_entry_summary(self, summary):
        debit = self._get_debit_credit()
        credit = self._get_debit_credit()
        summary.write(
            {"debit": summary.debit + debit, "credit": summary.credit + credit}
        )
