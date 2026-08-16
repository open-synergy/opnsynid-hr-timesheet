# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import models


class HrLeaveRequestBatch(models.Model):
    """Add Documenso-backed approval to the leave request batch.

    When the batch's approval template defines a Documenso signing
    template, its multiple-approval flow is replaced by a single
    ``documenso.signature.request``: the batch is approved once that
    request is signed, and rejected if it is cancelled.
    """

    _name = "hr.leave_request_batch"
    _inherit = [
        "hr.leave_request_batch",
        "mixin.documenso_signing_approval",
    ]

    _documenso_signing_create_page = True
