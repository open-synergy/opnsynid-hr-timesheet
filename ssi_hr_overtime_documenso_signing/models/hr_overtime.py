# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import models


class HrOvertime(models.Model):
    """Adds Documenso e-signature approval to overtime requests.

    A **Signature Requests** tab is added to the form. When the
    ``approval.template`` in effect defines a Documenso signing
    template, confirming the overtime creates a single
    ``documenso.signature.request`` instead of standard approval
    records, and the document is approved automatically once that
    request is signed (or moved to the rejection state if the signer
    cancels) — see ``mixin.documenso_signing_approval``.
    """

    _name = "hr.overtime"
    _inherit = [
        "hr.overtime",
        "mixin.documenso_signing_approval",
    ]

    _documenso_signing_create_page = True
