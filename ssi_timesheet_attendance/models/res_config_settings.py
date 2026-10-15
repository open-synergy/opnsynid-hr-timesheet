# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    """
    Exposes timesheet attendance company configuration on Settings.

    Mirrors ``res.company``'s check-in/check-out buffers, its default
    check-in/check-out reasons, and the registered attendance
    location requirement, so they can be edited from the Settings
    screen instead of the Companies form.

    The schedule fields are not prefixed with ``default_`` because
    Odoo treats such names as default value settings that need a
    ``default_model`` attribute.
    """

    _inherit = "res.config.settings"

    checkin_buffer = fields.Float(
        related="company_id.checkin_buffer",
        readonly=False,
    )
    checkout_buffer = fields.Float(
        related="company_id.checkout_buffer",
        readonly=False,
    )
    check_out_reason_id = fields.Many2one(
        related="company_id.check_out_reason_id",
        readonly=False,
    )
    check_in_reason_id = fields.Many2one(
        related="company_id.check_in_reason_id",
        readonly=False,
    )
    attendance_location_required = fields.Boolean(
        related="company_id.attendance_location_required",
        readonly=False,
    )
    schedule_source = fields.Selection(
        related="company_id.default_schedule_source",
        readonly=False,
    )
    schedule_pattern_id = fields.Many2one(
        related="company_id.default_schedule_pattern_id",
        readonly=False,
    )
