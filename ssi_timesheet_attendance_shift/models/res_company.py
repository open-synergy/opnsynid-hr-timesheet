# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResCompany(models.Model):
    # Adds the ``shift`` value to the default attendance schedule
    # source of the company. The field itself is owned by
    # ``ssi_timesheet_attendance``.

    _inherit = "res.company"

    default_schedule_source = fields.Selection(
        selection_add=[
            ("shift", "Shift Roster"),
        ],
        ondelete={"shift": "set default"},
    )
