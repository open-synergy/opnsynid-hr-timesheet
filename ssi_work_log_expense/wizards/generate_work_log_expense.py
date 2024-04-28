# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class GenerateWorkLogExpense(models.TransientModel):
    _name = "generate_work_log_expense"
    _description = "Generate Work Log Expense"

    type_id = fields.Many2one(
        string="Type",
        comodel_name="work_log_expense_type",
        required=True,
        default=lambda r: r._default_type_id(),
    )
    analytic_account_id = fields.Many2one(
        string="Analytic Account",
        comodel_name="account.analytic.account",
    )
    date_start = fields.Date(
        string="Date Start",
        required=True,
    )
    date_end = fields.Date(
        string="Date End",
        required=True,
    )
    date = fields.Date(
        string="Date",
        required=True,
    )

    @api.model
    def _default_type_id(self):
        return self.env.context.get("active_id", False)

    def action_confirm(self):
        for wizard in self.sudo():
            wizard._generate_data()

    def _generate_data(self):
        self.ensure_one()
        WorkLog = self.env["hr.work_log"]
        employees = WorkLog.search(self._prepare_populate_domain()).mapped(
            "employee_id"
        )
        for employee in employees:
            self._create_work_log_expense(employee)

    def _prepare_populate_domain(self):
        self.ensure_one()
        result = [
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

    def _create_work_log_expense(self, employee):
        self.ensure_one()
        Expense = self.env["work_log_expense"]
        data = self._prepare_work_log_expense_data(employee)
        expense = Expense.create(data)
        expense.action_populate()

    def _prepare_work_log_expense_data(self, employee):
        self.ensure_one()
        return {
            "employee_id": employee.id,
            "date_start": self.date_start,
            "date_end": self.date_end,
            "date": self.date,
            "type_id": self.type_id.id,
            "analytic_account_id": self.analytic_account_id
            and self.analytic_account_id.id
            or False,
            "accrue_account_id": self.type_id.accrue_account_id.id,
            "journal_id": self.type_id.journal_id.id,
        }
