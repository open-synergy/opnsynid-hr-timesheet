# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class HrEmployeeBase(models.AbstractModel):
    """
    Adds a default attendance schedule source to the employee.
    ``schedule_source`` is copied onto a new ``hr.timesheet`` of this
    employee (via ``onchange_schedule_source``) so each employee's
    usual generation mode does not have to be re-selected on every
    timesheet.
    """

    _inherit = "hr.employee.base"
    _name = "hr.employee.base"

    schedule_source = fields.Selection(
        string="Schedule Source",
        selection=[
            ("working_schedule", "Working Schedule"),
            ("shift", "Shift Roster"),
        ],
        required=True,
        default="working_schedule",
        help=(
            "Default attendance schedule source copied onto a new "
            "timesheet's own Schedule Source when this employee is "
            "set on it."
        ),
    )
