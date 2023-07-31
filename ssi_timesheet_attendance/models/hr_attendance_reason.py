# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, fields, models
from odoo.exceptions import UserError


class HrAttendanceReason(models.Model):
    _name = "hr.attendance_reason"
    _inherit = ["mixin.master_data"]
    _description = "Attendance Reason"

    name = fields.Char(
        string="Reason",
    )
    by_system = fields.Boolean(
        string="Created By System",
        default=False,
    )

    def unlink(self):
        for record in self:
            user = self.env.user
            if record.by_system and not user.has_group("base.group_erp_manager"):
                error_message = "Cannot delete this data"
                raise UserError(_(error_message))
        _super = super(HrAttendanceReason, self)
        _super.unlink()
