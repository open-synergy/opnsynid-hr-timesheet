# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class HrEmployee(models.Model):
    _name = "hr.employee"
    _inherit = ["hr.employee"]

    work_log_rate_ids = fields.One2many(
        string="Work Log Rates",
        comodel_name="work_log_rate",
        inverse_name="employee_id",
    )
    work_log_rate_id = fields.Many2one(
        string="Active Work Log Rate",
        comodel_name="work_log_rate",
        compute="_compute_work_log_rate_id",
        store=True,
    )

    @api.depends(
        "work_log_rate_ids",
        "work_log_rate_ids.state",
        "work_log_rate_ids.date_start",
    )
    def _compute_work_log_rate_id(self):
        for record in self:
            result = False
            active_rates = record.work_log_rate_ids.filtered(
                lambda r: r.state == "open"
            )
            if len(active_rates) > 0:
                result = active_rates[0]
            record.work_log_rate_id = result

    def get_work_log_rate(self, date=False):
        self.ensure_one()
        result = self.work_log_rate_id
        if date:
            Rate = self.env["work_log_rate"]
            criteria = [
                ("employee_id", "=", self.id),
                ("state", "in", ["ready", "open", "done"]),
                "|",
                "&",
                ("date_start", "<=", date),
                ("date_end", "=", False),
                "&",
                ("date_start", "<=", date),
                ("date_end", ">=", date),
            ]
            rates = Rate.search(criteria)
            if len(rates) > 0:
                result = rates[0]
        return result
