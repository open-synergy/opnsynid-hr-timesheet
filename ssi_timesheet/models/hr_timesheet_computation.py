# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class HrTimesheetComputation(models.Model):
    """
    Stores one computed pay/allowance line for a timesheet sheet.

    Each line holds the amount produced by evaluating the linked
    ``hr.timesheet_computation_item`` formula (``amount``), an optional
    manual override (``correction_amount``), and the resulting
    ``final_amount`` that should be used downstream instead of
    ``amount`` alone.
    """

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
        compute_sudo=True,
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
    correction_amount = fields.Float(
        string="Correction Amount",
        default=0.0,
        required=True,
        help="Manual correction applied on top of the computed "
        "amount. Negative values are allowed, to reduce the "
        "computed amount for a single exceptional line without "
        "editing the item formula shared by every employee.",
    )
    final_amount = fields.Float(
        string="Final Amount",
        compute="_compute_final_amount",
        store=True,
        readonly=True,
        compute_sudo=True,
        help="Amount actually used downstream: the computed "
        "``amount`` plus the manual ``correction_amount``.",
    )

    @api.depends(
        "amount",
        "correction_amount",
    )
    def _compute_final_amount(self):
        """Sum the computed amount and the manual correction.

        :return: nothing; assigns ``final_amount``
        """
        for record in self:
            result = record.amount + record.correction_amount
            record.final_amount = result

    def _evaluate_computation(self, localdict):
        self.ensure_one()
        result = self.item_id._evaluate_computation(localdict)
        self.write({"amount": result})
        return result
