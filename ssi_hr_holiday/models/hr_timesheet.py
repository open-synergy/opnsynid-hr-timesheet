# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, fields, models


class HrTimesheet(models.Model):
    """
    Adds leave traceability to timesheets.
    Links each leave request whose period this timesheet covers back
    to the timesheet, so leaves are visible from their sheet.
    """

    _name = "hr.timesheet"
    _inherit = "hr.timesheet"

    leave_ids = fields.One2many(
        string="Leaves",
        comodel_name="hr.leave",
        inverse_name="sheet_id",
        readonly=True,
    )

    def _get_schedule_rebuild_blockers(self):
        """Add the active leaves that use a slot of this timesheet.

        A leave that is not cancelled or rejected and is linked to a
        slot of ``schedule_ids`` forbids rebuilding the schedule,
        because the link would be lost silently.

        :return: the blockers, each as ``(label, recordset)``
        :rtype: list
        """
        result = super()._get_schedule_rebuild_blockers()
        self.ensure_one()
        leaves = self.schedule_ids.mapped("leave_ids").filtered(
            lambda leave: leave.state not in ("cancel", "reject")
        )
        if leaves:
            result.append((_("Leave"), leaves))
        return result

    def action_compute_schedule(self):
        """Link the leaves of the period to the new schedule slots.

        Runs after the schedule is rebuilt. Every leave of the same
        employee that overlaps the period and is not cancelled or
        rejected gets its ``schedule_ids`` (and so its
        ``leave_duration``) computed again. The rebuild refuses to
        run while an active leave uses a slot, so this is the first
        link of the leaves, not a relink.

        :return: the result of the parent method
        """
        result = super().action_compute_schedule()
        Leave = self.env["hr.leave"].sudo()
        for sheet in self.sudo():
            criteria = [
                ("employee_id", "=", sheet.employee_id.id),
                ("date_start", "<=", sheet.date_end),
                ("date_end", ">=", sheet.date_start),
                ("state", "not in", ["cancel", "reject"]),
            ]
            Leave.search(criteria).modified(["employee_id"])
        return result
