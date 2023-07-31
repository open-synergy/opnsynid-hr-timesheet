# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import UserError
from odoo.tools.safe_eval import safe_eval


class HROvertime(models.Model):
    _inherit = "hr.overtime"

    @api.depends(
        "type_id",
        "employee_id",
    )
    def _compute_allowed_analytic_account_ids(self):
        for document in self:
            result = []
            if document.type_id:
                type = document.type_id
                if type.analytic_account_method == "fixed":
                    if type.analytic_account_ids:
                        result = type.analytic_account_ids.ids
                elif type.analytic_account_method == "python":
                    analytic_account_ids = document._evaluate_analytic_account()
                    if analytic_account_ids:
                        result = analytic_account_ids
            document.allowed_analytic_account_ids = result

    allowed_analytic_account_ids = fields.Many2many(
        string="Allowed Analytic Accounts",
        comodel_name="account.analytic.account",
        compute="_compute_allowed_analytic_account_ids",
        store=False,
    )
    analytic_account_id = fields.Many2one(
        string="Analytic Account",
        comodel_name="account.analytic.account",
        required=False,
        ondelete="restrict",
        readonly=True,
        states={
            "draft": [("readonly", False)],
        },
    )

    def _get_localdict(self):
        self.ensure_one()
        return {
            "env": self.env,
            "document": self,
        }

    def _evaluate_analytic_account(self):
        self.ensure_one()
        res = False
        localdict = self._get_localdict()
        try:
            safe_eval(self.type_id.python_code, localdict, mode="exec", nocopy=True)
            if "result" in localdict:
                res = localdict["result"]
        except Exception as error:
            msg_err = _("Error evaluating conditions.\n %s") % error
            raise UserError(msg_err)
        return res

    @api.onchange(
        "type_id",
    )
    def onchange_analytic_account_id(self):
        if self.type_id:
            self.analytic_account_id = False
