# Copyright 2023 OpenSynergy Indonesia
# Copyright 2023 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models

from odoo.addons.ssi_decorator import ssi_decorator


class WorkLogAccountingEntry(models.Model):
    _name = "work_log_accounting_entry"
    _description = "Work Log To Accounting Entry"
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
        comodel_name="work_log_accounting_entry_type",
        string="Employee",
        required=True,
        ondelete="restrict",
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    date = fields.Date(
        string="Date",
        required=True,
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    detail_ids = fields.One2many(
        comodel_name="hr.work_log",
        inverse_name="accounting_entry_id",
        readonly=True,
    )
    summary_ids = fields.One2many(
        comodel_name="work_log_accounting_entry_summary",
        inverse_name="accounting_entry_id",
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

    @api.model
    def _get_policy_field(self):
        res = super(WorkLogAccountingEntry, self)._get_policy_field()
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
            self.accure_account_id = self.type_id.accrue_account_id

    @api.onchange("type_id")
    def onchange_journal_id(self):
        self.journal_id = False
        if self.type_id:
            self.journal_id = self.type_id.journal_id

    def action_populate(self):
        for record in self.sudo():
            record._populate()

    def _populate(self):
        self.ensure_one()
        work_logs = self.env["hr.work_log"].search(
            [
                ("employee_id", "=", self.employee_id.id),
                ("date", ">=", self.date_start),
                ("date", "<=", self.date_end),
                ("accounting_entry_id", "=", False),
                ("state", "=", "done"),
                (
                    "|",
                    (
                        "analytic_account_id",
                        "in",
                        [self.type_id.allowed_analytic_account_ids.ids],
                    ),
                    (
                        "analytic_account_id.group_id",
                        "in",
                        [self.type_id.allowed_analytic_group_ids.ids],
                    ),
                ),
            ]
        )

        work_logs.write({"accounting_entry_id": self.id})

        for detail in self.detail_ids:
            detail._update_summary(self.type_id)

    @ssi_decorator.post_done_action()
    def _10_create_accounting_entry(self):
        move = self.env["account.move"].create(self._prepare_accounting_entry_creation)
        self.write({"move_id": move.id})
        for summary in self.accounting_summary_ids:
            summary._create_move_line(move)

    @ssi_decorator.post_cancel_action()
    def _10_cancel_accounting_entry(self):
        if self.move_id:
            self.move_id.button_cancel()
            self.move_id.with_context(force_delete=True).unlink()
