# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class GenerateTimesheet(models.TransientModel):
    # Extension of ``hr.generate_timesheet``: the generated timesheet
    # takes the schedule source and the schedule pattern of its
    # employee. ``ssi_timesheet`` already rebuilds the schedule after
    # creation (``_trigger_timesheet_onchange``); this module takes
    # that call over explicitly (see below).

    _inherit = "hr.generate_timesheet"

    def _prepare_data_timesheet(self, employee):
        """Add the schedule source and pattern of the employee.

        :param employee: ``hr.employee`` the timesheet is generated for
        :return: the values of the new timesheet, with
            ``schedule_source`` and ``schedule_pattern_id``
        :rtype: dict
        """
        data = super(GenerateTimesheet, self)._prepare_data_timesheet(employee)
        if data:
            data.update(
                {
                    "schedule_source": employee.schedule_source,
                    "schedule_pattern_id": employee.schedule_pattern_id.id,
                }
            )
        return data

    def _trigger_timesheet_onchange(self, timesheet):
        """Rebuild the attendance schedule of the generated timesheet.

        Runs ``super()`` and then ``action_compute_schedule()``. This
        call takes over the one that ``ssi_timesheet`` makes in its own
        ``_trigger_timesheet_onchange`` and that is to be removed
        there: the schedule belongs to this module. While both exist
        the schedule is built twice; the rebuild deletes and creates
        the slots again, so the result is identical.

        :param timesheet: the ``hr.timesheet`` just generated
        :return: nothing
        """
        self.ensure_one()
        super(GenerateTimesheet, self)._trigger_timesheet_onchange(timesheet)
        timesheet.action_compute_schedule()
