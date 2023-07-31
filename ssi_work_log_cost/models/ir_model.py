# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class IrModel(models.Model):
    _name = "ir.model"
    _inherit = "ir.model"

    # Product
    work_log_product_selection_method = fields.Selection(
        string="Product Selection Method",
        selection=[
            ("fixed", "Fixed"),
            ("python", "Python Code"),
        ],
        default="fixed",
        required=False,
    )
    work_log_product_ids = fields.Many2many(
        string="Allowed Work Log Products",
        comodel_name="product.product",
        relation="rel_model_2_work_log_product",
        column1="model_id",
        column2="product_id",
    )
    work_log_product_categ_ids = fields.Many2many(
        string="Allowed Work Log Product Categories",
        comodel_name="product.category",
        relation="rel_model_2_work_log_product_category",
        column1="model_id",
        column2="categ_id",
    )
    work_log_product_python_code = fields.Text(
        string="Python Code for Work Log Product",
        default="""# Available variables:
#  - env: Odoo Environment on which the action is triggered.
#  - document: record on which the action is triggered; may be void.
#  - result: Return result, the value is list of Analytic Accounts.
result = []""",
        copy=True,
    )
    default_worklog_usage_id = fields.Many2one(
        string="Default Worklog Usage",
        comodel_name="product.usage_type",
        ondelete="restrict",
    )

    # Pricelist
    work_log_pricelist_selection_method = fields.Selection(
        string="Pricelist Selection Method",
        selection=[
            ("fixed", "Fixed"),
            ("python", "Python Code"),
        ],
        default="fixed",
        required=False,
    )
    work_log_pricelist_ids = fields.Many2many(
        string="Allowed Work Log Pricelists",
        comodel_name="product.pricelist",
        relation="rel_model_2_work_log_pricelist",
        column1="model_id",
        column2="pricelist_id",
    )
    work_log_pricelist_python_code = fields.Text(
        string="Python Code for Work Log Pricelist",
        default="""# Available variables:
#  - env: Odoo Environment on which the action is triggered.
#  - document: record on which the action is triggered; may be void.
#  - result: Return result, the value is list of Analytic Accounts.
result = []""",
        copy=True,
    )
