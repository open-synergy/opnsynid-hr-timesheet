# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class HrTimesheetComputationItem(models.Model):
    _name = "hr.timesheet_computation_item"
    _inherit = ["mixin.master_data"]
    _description = "Timesheet Computation Item"

    DEFAULT_PYTHON_CODE = """# Available variables:
#  - env: Odoo Environment on which the action is triggered.
#  - document: record on which the action is triggered; may be void.
#  - result: Return result, the value is boolean."""

    name = fields.Char(
        string="Name",
    )
    python_code = fields.Text(
        string="Python Code",
        default=DEFAULT_PYTHON_CODE,
        copy=True,
    )
