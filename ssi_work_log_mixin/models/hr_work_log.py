# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import _, api, fields, models
from odoo.exceptions import UserError
from odoo.tools.safe_eval import safe_eval


class HRWorkLog(models.Model):
    _name = "hr.work_log"
    _description = "HR Work Log"

    name = fields.Char(
        string="Description",
        required=True,
    )

    @api.model
    def _default_model_id(self):
        model = False
        obj_ir_model = self.env["ir.model"]
        model_name = self.env.context.get("work_log_model", False)
        if model_name:
            criteria = [("model", "=", model_name)]
            model = obj_ir_model.search(criteria)
        return model

    model_id = fields.Many2one(
        string="Document Type",
        comodel_name="ir.model",
        index=True,
        required=True,
        ondelete="cascade",
        default=lambda self: self._default_model_id(),
    )
    model_name = fields.Char(
        related="model_id.model",
        index=True,
        store=True,
    )
    work_object_id = fields.Many2oneReference(
        string="Document ID",
        index=True,
        required=True,
        readonly=True,
        model_field="model_name",
    )

    @api.model
    def _selection_target_model(self):
        return [(model.model, model.name) for model in self.env["ir.model"].search([])]

    @api.depends(
        "model_id",
        "work_object_id",
    )
    def _compute_work_object_reference(self):
        for document in self:
            result = False
            if document.model_id and document.work_object_id:
                result = "%s,%s" % (document.model_name, document.work_object_id)
            document.work_object_reference = result

    work_object_reference = fields.Reference(
        string="# Document",
        compute="_compute_work_object_reference",
        store=True,
        selection="_selection_target_model",
    )
    date = fields.Date(
        string="Date",
        required=True,
    )
    amount = fields.Float(
        string="Amount",
        required=True,
    )

    @api.depends(
        "model_id",
    )
    def _compute_allowed_analytic_account_ids(self):
        for document in self:
            result = []
            if document.model_id:
                model = document.model_id
                if model.work_log_aa_selection_method == "fixed":
                    if model.work_log_aa_ids:
                        result = model.work_log_aa_ids.ids
                elif model.work_log_aa_selection_method == "python":
                    analytic_account_ids = self._evaluate_analytic_account(model)
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
        required=True,
    )

    @api.depends(
        "employee_id",
        "date",
    )
    def _compute_sheet_id(self):
        obj_hr_timesheet = self.env["hr.timesheet"]
        for document in self:
            result = False
            criteria = [
                ("employee_id", "=", document.employee_id.id),
                ("date_start", "<=", document.date),
                ("date_end", ">=", document.date),
                ("state", "=", "open"),
            ]
            timesheet = obj_hr_timesheet.search(criteria)
            if timesheet:
                result = timesheet.id
            document.sheet_id = result

    sheet_id = fields.Many2one(
        string="Timesheet",
        comodel_name="hr.timesheet",
        compute="_compute_sheet_id",
        store=True,
        required=False,
        ondelete="restrict",
    )

    @api.model
    def _default_employee_id(self):
        result = False
        obj_hr_employee = self.env["hr.employee"]
        user = self.env.user
        criteria = [("user_id", "=", user.id)]
        employee = obj_hr_employee.search(criteria)
        if employee:
            result = employee.id
        return result

    employee_id = fields.Many2one(
        string="Employee",
        comodel_name="hr.employee",
        required=True,
        default=lambda self: self._default_employee_id(),
    )

    def _get_localdict(self):
        self.ensure_one()
        object = self.env[self.model_name]
        document = object.browse(self.work_object_id)
        return {
            "env": self.env,
            "document": document,
        }

    def _evaluate_analytic_account(self, model):
        self.ensure_one()
        res = False
        localdict = self._get_localdict()
        try:
            safe_eval(model.python_code, localdict, mode="exec", nocopy=True)
            if "result" in localdict:
                res = localdict["result"]
        except Exception as error:
            msg_err = _("Error evaluating conditions.\n %s") % error
            raise UserError(msg_err)
        return res

    @api.constrains("sheet_id")
    def _check_sheet_id(self):
        for document in self:
            if not document.sheet_id:
                strWarning = _("Timesheet for %s on %s not found") % (
                    document.employee_id.name,
                    document.date,
                )
                raise UserError(strWarning)
