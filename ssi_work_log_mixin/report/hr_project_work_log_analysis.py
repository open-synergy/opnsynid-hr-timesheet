# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class HrProjectWorkLogAnalysis(models.Model):
    _name = "hr.project_work_log_analysis"
    _description = "Project Worklog Analysis"
    _order = "department_id, employee_id"
    _auto = False
    _rec_name = "employee_id"

    department_id = fields.Many2one(
        string="Department",
        comodel_name="hr.department",
        readonly=True,
    )
    employee_id = fields.Many2one(
        string="Employee",
        comodel_name="hr.employee",
        readonly=True,
    )
    manager_id = fields.Many2one(
        string="Project Manager",
        comodel_name="res.users",
        readonly=True,
    )
    job_id = fields.Many2one(
        string="Job Position",
        comodel_name="hr.job",
        readonly=True,
    )
    analytic_account_id = fields.Many2one(
        string="Analytic Account",
        comodel_name="account.analytic.account",
        readonly=True,
    )
    sheet_id = fields.Many2one(
        string="Timesheet",
        comodel_name="hr.timesheet",
        readonly=True,
    )
    date_start = fields.Date(
        string="Date Start",
        readonly=True,
    )
    date_end = fields.Date(
        string="Date End",
        readonly=True,
    )
    date = fields.Date(
        string="Date",
        readonly=True,
    )
    amount = fields.Float(
        string="Duration",
        readonly=True,
    )
    nbr = fields.Integer(
        string="# of Worklogs",
        readonly=True,
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
    )

    @property
    def _table_query(self):
        return "%s %s %s %s" % (
            self._select(),
            self._from(),
            self._where(),
            self._group_by(),
        )

    @api.model
    def _select(self):
        select_str = """
        SELECT
            (select 1 ) AS nbr,
            l.id as id,
            l.employee_id as employee_id,
            l.department_id as department_id,
            CASE
                WHEN p.user_id IS NOT NULL THEN p.user_id
                ELSE e2.user_id
            END AS manager_id,
            l.job_id as job_id,
            l.analytic_account_id as analytic_account_id,
            l.sheet_id as sheet_id,
            ts.date_start,
            ts.date_end,
            l.date as date,
            l.amount as amount,
            l.state as state
        """
        return select_str

    @api.model
    def _from(self):
        from_str = """
        FROM hr_work_log l
        LEFT JOIN hr_timesheet ts ON ts.id = l.sheet_id
        LEFT JOIN project_project p ON p.analytic_account_id = l.analytic_account_id
        LEFT JOIN hr_employee e ON e.id = l.employee_id
        LEFT JOIN hr_employee e2 ON e2.id = e.parent_id
        """
        return from_str

    @api.model
    def _where(self):
        where_str = """

        """
        return where_str

    @api.model
    def _group_by(self):
        group_by_str = """
        GROUP BY
            l.id,
            l.employee_id,
            l.department_id,
            p.user_id,
            e2.user_id,
            l.job_id,
            l.analytic_account_id,
            l.sheet_id,
            ts.date_start,
            ts.date_end,
            l.date,
            l.amount,
            l.state
        """
        return group_by_str
