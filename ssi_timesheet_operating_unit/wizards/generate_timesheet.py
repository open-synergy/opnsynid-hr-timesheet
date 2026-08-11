# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class GenerateTimesheet(models.TransientModel):
    """
    Propagates the employee's operating unit to timesheets created by
    the Generate Timesheet wizard.

    ``hr.generate_timesheet.action_generate`` builds each ``hr.timesheet``
    from a plain dict via ``create()``, bypassing the Form API and the
    ``onchange_operating_unit_id`` onchange that normally derives
    ``operating_unit_id`` from ``employee_id``. This extension re-applies
    that propagation directly inside ``_prepare_data_timesheet`` so the
    generated timesheet always carries the operating unit of the
    employee it belongs to, regardless of the operating unit of the
    user running the wizard.
    """

    _inherit = "hr.generate_timesheet"

    def _prepare_data_timesheet(self, employee):
        """Add ``operating_unit_id`` to the base ``hr.timesheet`` values.

        Calls ``super()`` first, then, only when the resulting dict is
        not empty, sets ``operating_unit_id`` to
        ``employee.operating_unit_id``. The employee is the sole source
        of truth for the timesheet's operating unit, so an employee
        with no operating unit intentionally produces a timesheet with
        no operating unit as well.

        :param employee: ``hr.employee`` record the timesheet is
            generated for
        :return: dict of ``hr.timesheet`` values, or an empty dict when
            the base implementation refuses to generate the timesheet
        """
        res = super()._prepare_data_timesheet(employee)
        if res:
            res["operating_unit_id"] = employee.operating_unit_id.id
        return res
