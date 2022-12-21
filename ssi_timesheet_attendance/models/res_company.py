# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
from odoo import api, fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    checkout_buffer = fields.Float(
        string="Check Out Buffer",
        digits=(2, 2),
    )

    @api.model
    def _default_check_out_reason_id(self):
        data = self.env.ref(
            "ssi_timesheet_attendance.hr_attendance_reason_check_out"
        ).id
        return data

    check_out_reason_id = fields.Many2one(
        string="Check Out Reason",
        comodel_name="hr.attendance_reason",
        default=lambda self: self._default_check_out_reason_id(),
        ondelete="restrict",
    )

    @api.model
    def _default_check_in_reason_id(self):
        return self.env.ref("ssi_timesheet_attendance.hr_attendance_reason_check_in").id

    check_in_reason_id = fields.Many2one(
        string="Check In Reason",
        comodel_name="hr.attendance_reason",
        default=lambda self: self._default_check_in_reason_id(),
        ondelete="restrict",
    )
