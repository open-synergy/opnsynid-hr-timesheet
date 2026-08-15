# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import models


class HrLeaveAllocation(models.Model):
    """Enable Documenso-signed approval on leave allocations.

    Adds the Documenso Signing tab to the ``hr.leave_allocation`` form and
    lets an ``approval.template`` route this document to a single
    ``documenso.signature.request`` instead of the regular approval-record
    flow, whenever the template defines a
    ``documenso_signing_template_id``.
    """

    _name = "hr.leave_allocation"
    _inherit = [
        "hr.leave_allocation",
        "mixin.documenso_signing_approval",
    ]

    _documenso_signing_create_page = True
