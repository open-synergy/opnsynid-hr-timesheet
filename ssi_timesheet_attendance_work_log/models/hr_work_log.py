# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models


class HRWorkLog(models.Model):
    _name = "hr.work_log"
    _inherit = [
        "hr.work_log",
    ]

    @api.onchange("sheet_id")
    def onchange_amount(self):
        if self.sheet_id:
            self.amount = self.sheet_id.attendance_work_log_diff

    @api.model
    def create(self, values):
        """Create the work log and refresh its daily summary date.

        Only the newly created record's own ``date`` is affected, so
        ``generate_daily_summary()`` is called with that single date
        instead of sweeping the whole sheet.

        :param values: field values for the new record
        :return: the created ``hr.work_log`` record
        """
        res = super(HRWorkLog, self).create(values)
        res.sheet_id.generate_daily_summary(dates=[res.date])
        return res

    def write(self, values):
        """Update the work log and refresh the affected summaries.

        The dates in effect *before* this write are captured first,
        since ``super().write()`` overwrites them; the daily summary
        is then regenerated for the union of the old and new dates,
        so moving a work log from one date to another refreshes both
        the origin and the destination summaries. ``date`` is a
        required field, so both the pre-write and post-write values
        are always set on an existing record -- no falsy guard is
        needed around either one.

        :param values: field values to write
        :return: the value returned by the parent ``write()``
        """
        old_date_by_id = {rec.id: rec.date for rec in self}
        res = super(HRWorkLog, self).write(values)
        for rec in self:
            if "date" in values or "amount" in values:
                affected_dates = {old_date_by_id[rec.id], rec.date}
                rec.sheet_id.generate_daily_summary(dates=affected_dates)
        return res
