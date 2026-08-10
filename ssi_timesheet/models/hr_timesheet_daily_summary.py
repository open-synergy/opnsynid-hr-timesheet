# Copyright 2023 OpenSynergy Indonesia
# Copyright 2023 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class HrTimesheetDailySummary(models.Model):
    _name = "hr.timesheet_daily_summary"
    _description = "HR Timesheet Daily Summary"
    _rec_name = "date"
    _order = "date"

    sheet_id = fields.Many2one(
        string="# Sheet",
        comodel_name="hr.timesheet",
        required=True,
        ondelete="cascade",
    )
    date = fields.Date(string="Date", required=True)

    def _prepare_daily_summary_vals(self, sheet_id, date):
        vals = {
            "sheet_id": sheet_id.id,
            "date": date,
        }
        return vals

    def _get_daily_summary_diff(self, vals):
        """Return only the pairs of ``vals`` that differ from ``self``.

        Extension point: this is the single place that decides whether
        an existing daily summary needs to be written. ``self`` is one
        existing record (``ensure_one()``); ``vals`` is the dict built
        by ``_prepare_daily_summary_vals()`` (possibly extended with
        extra fields by an override in another module).

        Comparing values naively (``self[key] != vals[key]``) is wrong
        for ``many2one`` fields: ``self[key]`` returns a recordset
        while ``vals[key]`` stores its integer id, so the comparison
        always evaluates as "different" and Odoo logs a "Comparing
        apples and oranges" warning. This method compares
        ``self[key].id`` against ``vals[key]`` for ``many2one`` fields
        (looked up via ``self._fields[key].type``) and ``self[key]``
        directly for every other field type, so it stays correct for
        fields added by subclasses without hardcoding field names.

        :param vals: dict of proposed values, as built by
            ``_prepare_daily_summary_vals()``
        :return: dict containing only the key/value pairs of ``vals``
            that differ from the values currently stored on ``self``;
            empty when nothing changed
        """
        self.ensure_one()
        diff = {}
        for key, val in vals.items():
            field = self._fields[key]
            if field.type == "many2one":
                stored_val = self[key].id
            else:
                stored_val = self[key]
            if stored_val != val:
                diff[key] = val
        return diff
