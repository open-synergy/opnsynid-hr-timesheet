# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import UserError
from odoo.tools.safe_eval import safe_eval


class HROvertime(models.Model):
    """Add analytic account selection to ``hr.overtime``.

    Depending on the configuration of ``hr.overtime_type``, the allowed
    analytic accounts are either a fixed list or the result of a Python
    code evaluation. The chosen analytic account is stored on
    ``analytic_account_id`` and is editable only while the document is
    in ``draft`` state.
    """

    _inherit = "hr.overtime"

    @api.depends(
        "type_id",
        "employee_id",
    )
    def _compute_allowed_analytic_account_ids(self):
        """Compute the analytic accounts allowed for this document.

        The result depends on ``type_id.analytic_account_method``: for
        ``fixed`` it is the type's configured ``analytic_account_ids``;
        for ``python`` it is the result of evaluating
        ``type_id.python_code`` via ``_evaluate_analytic_account``.
        """
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
        """Build the local variables available to ``python_code``.

        :return: dict exposing ``env`` (Odoo Environment) and
            ``document`` (this ``hr.overtime`` record) to the
            ``safe_eval`` call in ``_evaluate_analytic_account``
        """
        self.ensure_one()
        return {
            "env": self.env,
            "document": self,
        }

    def _evaluate_analytic_account(self):
        """Evaluate ``type_id.python_code`` to get analytic accounts.

        Executes the overtime type's ``python_code`` with the
        ``env``/``document`` variables from ``_get_localdict``. The
        code is expected to assign a list of ``account.analytic.account``
        ids to a ``result`` variable.

        :return: list of analytic account ids, or ``False`` when the
            code does not set ``result``
        :raises UserError: when the code evaluation raises an exception
        """
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
