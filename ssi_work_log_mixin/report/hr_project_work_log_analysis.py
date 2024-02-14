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
            p.id as id,
            l.employee_id as employee_id,
            l.department_id as department_id,
            p.user_id as manager_id,
            l.job_id as job_id,
            l.analytic_account_id as analytic_account_id,
            l.sheet_id as sheet_id,
            l.date as date,
            l.amount as amount,
            l.state as state
        """
        return select_str

    @api.model
    def _from(self):
        from_str = """
        FROM project_project p
        LEFT JOIN project_task t ON t.project_id = p.id
        LEFT JOIN hr_work_log l ON (l.work_object_id = t.id AND l.model_name = 'project.task')
        LEFT JOIN ir_model m ON m.id = l.model_id
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
            p.id,
            l.employee_id,
            l.department_id,
            p.user_id,
            l.job_id,
            l.analytic_account_id,
            l.sheet_id,
            l.date,
            l.amount,
            l.state
        """
        return group_by_str
