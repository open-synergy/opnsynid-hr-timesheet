# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class IrModel(models.Model):
    _name = "ir.model"
    _inherit = "ir.model"

    work_log_aa_selection_method = fields.Selection(
        string="Analytic Account Selection Method",
        selection=[
            ("fixed", "Fixed"),
            ("python", "Python Code"),
        ],
        default="fixed",
        required=False,
    )
    work_log_aa_ids = fields.Many2many(
        string="Analytic Accounts",
        comodel_name="account.analytic.account",
        relation="rel_model_2_analytic_account",
        column1="model_id",
        column2="analytic_account_id",
    )
    python_code = fields.Text(
        string="Python Code",
        default="""# Available variables:
#  - env: Odoo Environment on which the action is triggered.
#  - document: record on which the action is triggered; may be void.
#  - result: Return result, the value is list of Analytic Accounts.
result = []""",
        copy=True,
    )
