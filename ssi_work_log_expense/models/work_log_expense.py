# Copyright 2023 OpenSynergy Indonesia
# Copyright 2023 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models

from odoo.addons.ssi_decorator import ssi_decorator


class WorkLogExpense(models.Model):
    _name = "work_log_expense"
    _description = "Work Log Expense"
    _inherit = [
        "mixin.employee_document",
        "mixin.date_duration",
        "mixin.transaction_confirm",
        "mixin.transaction_done",
        "mixin.transaction_cancel",
    ]

    _approval_from_state = "draft"
    _approval_to_state = "done"
    _approval_state = "confirm"
    _after_approved_method = "action_done"

    _create_sequence_state = "done"

    # Attributes related to add element on view automatically
    _automatically_insert_view_element = True
    _automatically_insert_multiple_approval_page = True

    _statusbar_visible_label = "draft,confirm,done"

    # Mixin duration attribute
    _date_start_readonly = True
    _date_end_readonly = True
    _date_start_required = True
    _date_end_required = True
    _date_start_states_list = ["draft"]
    _date_start_states_readonly = ["draft"]
    _date_end_states_list = ["draft"]
    _date_end_states_readonly = ["draft"]

    _policy_field_order = [
        "confirm_ok",
        "approve_ok",
        "reject_ok",
        "restart_approval_ok",
        "cancel_ok",
        "done_ok",
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

    type_id = fields.Many2one(
        comodel_name="work_log_expense_type",
        string="Type",
        required=True,
        ondelete="restrict",
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    allowed_analytic_account_ids = fields.Many2many(
        string="Allowed Analytic Accounts",
        comodel_name="account.analytic.account",
        compute="_compute_allowed_analytic_account_ids",
        store=False,
    )
    analytic_account_id = fields.Many2one(
        comodel_name="account.analytic.account",
        string="Analytic Account",
        ondelete="restrict",
        readonly=True,
        states={"draft": [("readonly", False)]},
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
    date = fields.Date(
        string="Date",
        required=True,
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    detail_ids = fields.One2many(
        comodel_name="hr.work_log",
        inverse_name="expense_id",
        readonly=True,
    )
    summary_ids = fields.One2many(
        comodel_name="work_log_expense_summary",
        inverse_name="expense_id",
        readonly=True,
    )
    amount = fields.Float(
        string="Amount Total",
        compute="_compute_amount",
        store=True,
    )
    accrue_account_id = fields.Many2one(
        comodel_name="account.account",
        string="Account",
        required=True,
        ondelete="restrict",
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    journal_id = fields.Many2one(
        comodel_name="account.journal",
        string="Journal",
        required=True,
        ondelete="restrict",
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    move_id = fields.Many2one(
        comodel_name="account.move",
        string="# Accounting Entry",
        readonly=True,
    )
    state = fields.Selection(
        string="State",
        selection=[
            ("draft", "Draft"),
            ("confirm", "Waiting for Approval"),
            ("done", "Done"),
            ("cancel", "Cancelled"),
            ("reject", "Reject"),
        ],
        default="draft",
        required=True,
        readonly=True,
    )

    @api.depends(
        "detail_ids",
        "detail_ids.price_subtotal",
    )
    def _compute_amount(self):
        for record in self:
            result = 0.0
            for detail in record.detail_ids:
                result += detail.price_subtotal
            record.amount = result

    @api.depends(
        "type_id",
    )
    def _compute_allowed_analytic_account_ids(self):
        AA = self.env["account.analytic.account"]
        for record in self:
            result = []
            if record.type_id and record.type_id.allowed_analytic_account_ids:
                result += record.type_id.allowed_analytic_account_ids.ids

            if record.type_id and record.type_id.allowed_analytic_group_ids:
                criteria = [
                    ("group_id", "in", record.type_id.allowed_analytic_group_ids.ids)
                ]
                result += AA.search(criteria).ids
            record.allowed_analytic_account_ids = result

    @api.model
    def _get_policy_field(self):
        res = super(WorkLogExpense, self)._get_policy_field()
        policy_field = [
            "confirm_ok",
            "approve_ok",
            "reject_ok",
            "restart_approval_ok",
            "cancel_ok",
            "done_ok",
            "restart_ok",
            "manual_number_ok",
        ]
        res += policy_field
        return res

    @api.onchange("type_id")
    def onchange_accrue_account_id(self):
        self.accrue_account_id = False
        if self.type_id:
            self.accrue_account_id = self.type_id.accrue_account_id

    @api.onchange("type_id")
    def onchange_journal_id(self):
        self.journal_id = False
        if self.type_id:
            self.journal_id = self.type_id.journal_id

    @api.onchange(
        "type_id",
    )
    def onchange_analytic_account_id(self):
        self.analytic_account_id = False

    def action_populate(self):
        for record in self.sudo():
            record._populate()

    def action_clear(self):
        for record in self.sudo():
            record._clear_detail()

    def _clear_detail(self):
        self.ensure_one()
        if self.detail_ids:
            self.detail_ids.write(
                {
                    "expense_id": False,
                }
            )

        self.summary_ids.unlink()

    def _prepare_populate_domain(self):
        self.ensure_one()
        result = [
            ("employee_id", "=", self.employee_id.id),
            ("date", ">=", self.date_start),
            ("date", "<=", self.date_end),
            ("expense_id", "=", False),
            ("state", "=", "done"),
        ]
        if self.analytic_account_id:
            result += [("analytic_account_id", "=", self.analytic_account_id.id)]
        else:
            result += [
                "|",
                (
                    "analytic_account_id",
                    "in",
                    self.type_id.allowed_analytic_account_ids.ids,
                ),
                (
                    "analytic_account_id.group_id",
                    "in",
                    self.type_id.allowed_analytic_group_ids.ids,
                ),
            ]
        return result

    def _populate(self):
        self.ensure_one()
        self._clear_detail()
        criteria = self._prepare_populate_domain()
        work_logs = self.env["hr.work_log"].search(criteria)
        work_logs.write({"expense_id": self.id})

        for detail in self.detail_ids:
            detail._update_summary()

    @ssi_decorator.post_done_action()
    def _10_create_expense(self):
        move = (
            self.env["account.move"]
            .with_context(check_move_validity=False)
            .create(self._prepare_expense_creation())
        )
        self.write({"move_id": move.id})
        self._create_debit_aml()
        for summary in self.summary_ids:
            summary._create_aml()
        move.action_post()

    @ssi_decorator.post_cancel_action()
    def _10_cancel_expense(self):
        if self.move_id:
            self.move_id.button_cancel()
            self.move_id.with_context(force_delete=True).unlink()

    def _prepare_expense_creation(self):
        self.ensure_one()
        return {
            "name": self.name,
            "date": self.date,
            "journal_id": self.journal_id.id,
        }

    def _create_debit_aml(self):
        self.env["account.move.line"].with_context(check_move_validity=False).create(
            self._prepare_debit_aml()
        )

    def _prepare_debit_aml(self):
        name = _("Work log expense")
        return {
            "move_id": self.move_id.id,
            "name": name,
            "account_id": self.accrue_account_id.id,
            "partner_id": self.employee_id.address_home_id.id,
            "journal_id": self.journal_id.id,
            "debit": 0.0,
            "credit": self.amount,
        }
