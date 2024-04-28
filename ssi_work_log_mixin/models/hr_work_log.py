# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import UserError
from odoo.tools.safe_eval import safe_eval


class HRWorkLog(models.Model):
    _name = "hr.work_log"
    _inherit = [
        "mixin.transaction_confirm",
        "mixin.transaction_done",
        "mixin.transaction_cancel",
        "mixin.employee_document",
    ]
    _description = "HR Work Log"

    # Multiple Approval Attribute
    _approval_from_state = "draft"
    _approval_to_state = "done"
    _approval_state = "confirm"
    _after_approved_method = "action_done"

    # Attributes related to add element on view automatically
    _automatically_insert_view_element = True

    # Attributes related to add element on form view automatically
    _automatically_insert_multiple_approval_page = True
    _statusbar_visible_label = "draft,confirm,done,rejected"
    _policy_field_order = [
        "confirm_ok",
        "approve_ok",
        "reject_ok",
        "restart_approval_ok",
        "cancel_ok",
        "restart_ok",
        "manual_number_ok",
    ]
    _header_button_order = [
        "action_confirm",
        "action_approve_approval",
        "action_reject_approval",
        "%(ssi_transaction_cancel_mixin.base_select_cancel_reason_action)d",
        "action_restart",
    ]

    # Attributes related to add element on search view automatically
    _state_filter_order = [
        "dom_draft",
        "dom_confirm",
        "dom_reject",
        "dom_done",
        "dom_cancel",
    ]

    # Sequence attribute
    _create_sequence_state = "done"

    description = fields.Char(
        string="Description",
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
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
        readonly=True,
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
        readonly=False,
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
        string="Document Reference",
        compute="_compute_work_object_reference",
        store=True,
        selection="_selection_target_model",
    )

    @api.model
    def _default_date(self):
        return fields.Date.today()

    date = fields.Date(
        string="Date",
        required=True,
        default=lambda self: self._default_date(),
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    amount = fields.Float(
        string="Duration",
        required=True,
        default=0.0,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )

    @api.depends(
        "model_id",
        "date",
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
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    analytic_partner_id = fields.Many2one(
        string="Analytic Partner",
        related="analytic_account_id.partner_id",
        store=True,
    )
    analytic_group_id = fields.Many2one(
        string="Analytic Group",
        related="analytic_account_id.group_id",
        store=True,
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
    tag_ids = fields.Many2many(
        string="Tags",
        comodel_name="hr.work_log_tag",
        relation="rel_work_log_2_work_log_tag",
        column1="work_log_id",
        column2="tag_id",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    state = fields.Selection(
        string="State",
        selection=[
            ("draft", "Draft"),
            ("confirm", "Waiting for Approval"),
            ("done", "Done"),
            ("cancel", "Cancelled"),
            ("reject", "Rejected"),
        ],
        default="draft",
        copy=False,
    )

    @api.model
    def _get_policy_field(self):
        res = super(HRWorkLog, self)._get_policy_field()
        policy_field = [
            "confirm_ok",
            "approve_ok",
            "done_ok",
            "cancel_ok",
            "reject_ok",
            "restart_ok",
            "restart_approval_ok",
            "manual_number_ok",
        ]
        res += policy_field
        return res

    @api.onchange(
        "model_id",
    )
    def onchange_policy_template_id(self):
        template_id = self._get_template_policy()
        self.policy_template_id = template_id

    def _get_localdict(self):
        self.ensure_one()
        object = self.env[self.model_name]
        document = object.browse(self.work_object_id)
        return {
            "env": self.env,
            "document": document,
            "work_log": self,
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
