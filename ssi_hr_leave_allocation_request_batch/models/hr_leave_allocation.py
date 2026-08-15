# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class HrLeaveAllocation(models.Model):
    """
    Links a leave allocation back to the batch request that created it.
    Adds a backfill step so allocations left without ``date_extended``
    (e.g. created before this module, or outside the batch flow) get a
    sensible default from ``date_end``.
    """

    _inherit = "hr.leave_allocation"

    batch_id = fields.Many2one(
        comodel_name="hr.leave_allocation_request_batch", string="# Batch"
    )

    def _cron_recompute_wrong_value(self):
        """Backfill missing ``date_extended`` from ``date_end``.

        Extends the base cron: after the parent recomputation runs,
        every allocation still missing ``date_extended`` is defaulted
        to its own ``date_end`` so downstream logic never sees an
        empty value.
        """
        super(HrLeaveAllocation, self)._cron_recompute_wrong_value()
        allocation_batch_ids = self.search([("date_extended", "=", False)])
        for allocation_batch_id in allocation_batch_ids:
            allocation_batch_id.write({"date_extended": allocation_batch_id.date_end})
