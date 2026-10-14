# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class GenerateTimesheet(models.TransientModel):
    # Extension of ``hr.generate_timesheet``: the generated timesheet
    # takes the schedule source and the schedule pattern of its
    # employee. ``ssi_timesheet`` already rebuilds the schedule after
    # creation (``_trigger_timesheet_onchange``), so nothing else is
    # overridden here.

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
