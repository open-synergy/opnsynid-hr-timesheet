# -*- coding: utf-8 -*-
# Copyright 2020 PT. Simetri Sinergi Indonesia
# Copyright 2020 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import fields, models


class HrEmployee(models.Model):
    _name = "hr.employee"
    _inherit = "hr.employee"

    active_leave_allocation_ids = fields.One2many(
        string="Active Leave Allocation",
        comodel_name="hr.leave_allocation",
        inverse_name="employee_id",
        domain=[
            ("state", "=", "open"),
        ],
    )

    def _get_available_leave_allocation(self, leave_type_id):
        self.ensure_one()
        result = 0
        criteria = [
            ("employee_id", "=", self.id),
            ("type_id", "=", leave_type_id),
            ("state", "=", "open"),
        ]
        LeaveAllocation = self.env["hr.leave_allocation"]
        for leave_allocation in LeaveAllocation.search(criteria):
            result += leave_allocation.num_of_days_available
        return result
