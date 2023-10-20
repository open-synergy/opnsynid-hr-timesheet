# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import UserError
from odoo.tools.safe_eval import safe_eval


class HRWorkLog(models.Model):
    _name = "hr.work_log"
    _inherit = [
        "hr.work_log",
        "mixin.product_line_account",
    ]

    uom_quantity = fields.Float(
        compute="_compute_uom_quantity",
        store=True,
    )
    account_id = fields.Many2one(
        required=False,
    )
    currency_id = fields.Many2one(
        required=False,
    )
    allowed_worklog_product_ids = fields.Many2many(
        string="Allowed Worklog Products",
        comodel_name="product.product",
        compute="_compute_allowed_worklog_product_ids",
    )
    allowed_worklog_pricelist_ids = fields.Many2many(
        string="Allowed Worklog Pricelist",
        comodel_name="product.pricelist",
        compute="_compute_allowed_worklog_pricelist_ids",
    )
    show_cost_setting_ok = fields.Boolean(
        string="Show Cost Setting",
        compute="_compute_policy",
        compute_sudo=True,
    )

    @api.depends(
        "model_id",
    )
    def _compute_allowed_worklog_product_ids(self):
        Product = self.env["product.product"]
        for document in self:
            result = []
            if document.model_id:
                model = document.model_id
                if model.work_log_product_selection_method == "fixed":
                    if model.work_log_product_ids:
                        result += model.work_log_product_ids.ids
                    if model.work_log_product_categ_ids:
                        criteria = [
                            ("categ_id", "in", model.work_log_product_categ_ids.ids)
                        ]
                        result += Product.search(criteria).ids
                elif model.work_log_product_selection_method == "python":
                    product_ids = self._evaluate_worklog_product(model)
                    if product_ids:
                        result = product_ids
            document.allowed_worklog_product_ids = result

    @api.depends(
        "model_id",
        "currency_id",
        "employee_id",
        "date",
        "product_id",
    )
    def _compute_allowed_worklog_pricelist_ids(self):
        Pricelist = self.env["product.pricelist"]
        for document in self:
            result = []
            if document.model_id:
                model = document.model_id
                if model.work_log_pricelist_selection_method == "fixed":
                    if model.work_log_pricelist_ids:
                        result += model.work_log_pricelist_ids.ids
                elif model.work_log_pricelist_selection_method == "python":
                    pricelist_ids = document._evaluate_worklog_pricelist(model)
                    if pricelist_ids:
                        result = pricelist_ids
                if len(result) > 0:
                    criteria = [
                        ("id", "in", result),
                        ("currency_id", "=", document.currency_id.id),
                    ]
                    result = Pricelist.search(criteria).ids
            document.allowed_worklog_pricelist_ids = result

    def _compute_policy(self):
        _super = super(HRWorkLog, self)
        _super._compute_policy()

    @api.model
    def _get_policy_field(self):
        res = super(HRWorkLog, self)._get_policy_field()
        policy_field = [
            "show_cost_setting_ok",
        ]
        res += policy_field
        return res

    @api.onchange("product_id")
    def onchange_name(self):
        pass

    @api.depends(
        "amount",
    )
    def _compute_uom_quantity(self):
        for record in self:
            record.uom_quantity = record.amount

    @api.onchange(
        "allowed_worklog_pricelist_ids",
        "currency_id",
    )
    def onchange_pricelist_id(self):
        self.pricelist_id = False
        if self.allowed_worklog_pricelist_ids:
            self.pricelist_id = self.allowed_worklog_pricelist_ids[0]._origin.id

    @api.onchange(
        "allowed_worklog_product_ids",
        "model_id",
    )
    def onchange_product_id(self):
        self.product_id = False
        if self.allowed_worklog_product_ids:
            self.product_id = self.allowed_worklog_product_ids[0]._origin.id

    @api.onchange(
        "model_id",
    )
    def onchange_usage_id(self):
        self.usage_id = False
        if self.model_id:
            self.usage_id = self.model_id.default_worklog_usage_id

    def _evaluate_worklog_product(self, model):
        self.ensure_one()
        res = False
        localdict = self._get_localdict()
        try:
            safe_eval(
                model.work_log_product_python_code, localdict, mode="exec", nocopy=True
            )
            if "result" in localdict:
                res = localdict["result"]
        except Exception as error:
            msg_err = _("Error evaluating conditions.\n %s") % error
            raise UserError(msg_err)
        return res

    def _evaluate_worklog_pricelist(self, model):
        self.ensure_one()
        res = False
        localdict = self._get_localdict()
        try:
            safe_eval(
                model.work_log_pricelist_python_code,
                localdict,
                mode="exec",
                nocopy=True,
            )
            if "result" in localdict:
                res = localdict["result"]
        except Exception as error:
            msg_err = _("Error evaluating conditions.\n %s") % error
            raise UserError(msg_err)
        return res
