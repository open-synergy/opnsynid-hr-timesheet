# Copyright 2023 OpenSynergy Indonesia
# Copyright 2023 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class WorkLogAccountingEntrySummary(models.Model):
    _name = "work_log_accounting_entry_summary"
    _description = "Work Log To Accounting Entry Summary"

    accounting_entry_id = fields.Many2one(
        comodel_name="work_log_accounting_entry",
        string="Account Entry",
        required=True,
        ondelete="cascade",
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
    debit = fields.Float(
        string="Debit",
    )
    credit = fields.Float(
        string="Credit",
    )

    def _create_aml(self, move):
        self.env["account.move.line"].with_context(check_move_validity=False).create(
            {
                "move_id": move.id,
                "account_id": self.account_id.id,
                "product_id": self.product_id.id,
                "partner_id": self.employee_id.home_address_id.id,
                "debit": self.debit,
                "credit": self.credit,
            }
        )
