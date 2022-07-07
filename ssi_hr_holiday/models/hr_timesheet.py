# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import _, api, fields, models
from odoo.exceptions import Warning as UserError


class HRTimesheet(models.Model):
    _inherit = "hr.timesheet"

    leave_ids = fields.One2many(
        string="Leaves",
        comodel_name="hr.leave",
        inverse_name="sheet_id",
        readonly=True,
    )

    # constrains STATE cancel
    @api.constrains("state")
    def _check_state_leave_ids(self):
        for record in self.sudo():
            for leave in record.leave_ids:
                if record.state in ["cancel", "reject"]:
                    if leave.state in ["done", "confirm"]:
                        strWarning = _(
                            "Some Data Leaves already Progress ..\nCancel data leave first .."
                        )
                        raise UserError(strWarning)
                if record.state in ["done"]:
                    if leave.state in ["draft", "confirm"]:
                        strWarning = _(
                            "Some Data Leaves not Confirmed ..\nConfirm data leave first .."
                        )
                        raise UserError(strWarning)
