# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class HrTimesheetComputation(models.Model):
    _name = "hr.timesheet_computation"
    _description = "Timesheet Computation"
    _order = "sheet_id,sequence,id"

    sheet_id = fields.Many2one(
        string="# Sheet",
        comodel_name="hr.timesheet",
        required=True,
        ondelete="cascade",
    )
    sequence = fields.Integer(
        string="Sequence",
        default=5,
        readonly=False,
    )
    code = fields.Char(
        string="Code",
        related="item_id.code",
        store=True,
        readonly=True,
    )
    item_id = fields.Many2one(
        string="Item",
        comodel_name="hr.timesheet_computation_item",
        required=True,
        ondelete="restrict",
    )
    amount = fields.Float(
        string="Amount",
        default=0.0,
        required=True,
        readonly=True,
    )

    def _evaluate_computation(self, localdict):
        self.ensure_one()
        result = self.item_id._evaluate_computation(localdict)
        self.write({"amount": result})
        return result
