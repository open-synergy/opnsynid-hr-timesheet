# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, fields, models
from odoo.exceptions import UserError
from odoo.tools.safe_eval import safe_eval


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

    def _evaluate_computation(self, localdict):
        self.ensure_one()
        try:
            safe_eval(self.python_code, localdict, mode="exec", nocopy=True)
            result = localdict["result"]
        except Exception as error:
            msg_err = _("Error evaluating conditions.\n %s") % error
            raise UserError(msg_err)
        return result
