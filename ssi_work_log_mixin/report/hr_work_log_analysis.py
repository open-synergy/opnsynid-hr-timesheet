# Copyright 2023 OpenSynergy Indonesia
# Copyright 2023 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models, tools


class HrWorkLogAnalysis(models.Model):
    _name = "hr.work_log_analysis"
    _description = "Worklog Analysis"
    _order = 'department_id, employee_id'
    _auto = False
    _rec_name = "employee_id"

    department_id = fields.Many2one('hr.department', string='Department', readonly=True)
    employee_id = fields.Many2one('hr.employee', string='Employee', readonly=True)
    manager_id = fields.Many2one('hr.employee', string='Manager', readonly=True)
    job_id = fields.Many2one('hr.job', string='Job Position', readonly=True)
    analytic_account_id = fields.Many2one('account.analytic.account', string='Analytic Account', readonly=True)
    sheet_id = fields.Many2one('hr.timesheet', string='Timesheet', readonly=True)
    date_start = fields.Date(string='Date Start', readonly=True)
    date_end = fields.Date(string='Date End', readonly=True)
    amount = fields.Float(
        string='Amount',
        readonly=True)
    nbr = fields.Integer('# of Worklogs', readonly=True)

    def _select(self):
        select_str = """
             SELECT
                    (select 1 ) AS nbr,
                    l.id as id,
                    l.employee_id as employee_id,
                    l.department_id as department_id,
                    l.manager_id as manager_id,
                    l.job_id as job_id,
                    l.analytic_account_id as analytic_account_id,
                    l.sheet_id as sheet_id,
                    t.date_start as date_start,
                    t.date_end as date_end,
                    l.amount as amount
        """
        return select_str

    def _group_by(self):
        group_by_str = """
                GROUP BY
                    l.id,
                    l.employee_id,
                    l.department_id,
                    l.manager_id,
                    l.job_id,
                    l.analytic_account_id,
                    l.sheet_id,
                    t.date_start,
                    t.date_end,
                    l.amount
        """
        return group_by_str

    def init(self):
        tools.drop_view_if_exists(self._cr, self._table)
        self._cr.execute("""
            CREATE view %s as
              %s
              FROM hr_work_log l
              LEFT JOIN hr_timesheet t ON t.id = l.sheet_id
                WHERE l.state in ('confirm', 'done')
                %s
        """ % (self._table, self._select(), self._group_by()))
