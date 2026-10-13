# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import fields, models


class ResCompany(models.Model):
    """
    Adds timesheet attendance configuration to the company record.

    Defines the check-in and check-out buffer tolerances used to
    match an attendance to a schedule slot (the check-out buffer
    also detects anomalous cross-date sign-outs), the default
    reasons applied when the system auto-creates check-in/check-out
    entries for them, and whether an attendance coordinate outside
    every registered ``hr.attendance_location`` is rejected.
    """

    _inherit = "res.company"

    checkin_buffer = fields.Float(
        string="Check In Buffer",
        digits=(2, 2),
        default=3.0,
        help=(
            "Tolerance, in hours, before the scheduled start of a "
            "schedule slot. An attendance is matched to a slot only "
            "when its check-in falls inside the slot's window: from "
            "this many hours before the slot starts until the check "
            "out buffer after the slot ends. A check-in outside "
            "every slot's window is left without a schedule."
        ),
    )
    checkout_buffer = fields.Float(
        string="Check Out Buffer",
        digits=(2, 2),
        default=3.0,
        help=(
            "Tolerance, in hours, after the scheduled end of a "
            "schedule slot. It is used twice. First, an attendance "
            "is matched to a slot only when its check-in is no "
            "later than this many hours after the slot ends. "
            "Second, it is the tolerance between the scheduled end "
            "of the attendance and the actual check-out time before "
            "a check-out recorded on a different date than its "
            "attendance is treated as an anomaly (a new attendance "
            "record is created instead of closing the current one). "
            "A value of 0.0 allows no tolerance at all."
        ),
    )
    check_out_reason_id = fields.Many2one(
        string="Check Out Reason",
        comodel_name="hr.attendance_reason",
        help=(
            "Default reason applied to the check-out of a "
            "system-generated attendance record created when a "
            "sign-out is detected as an anomaly (outside the check "
            "out buffer). Falls back to the module's default check "
            "out reason when left empty."
        ),
    )
    check_in_reason_id = fields.Many2one(
        string="Check In Reason",
        comodel_name="hr.attendance_reason",
        help=(
            "Default reason applied to the check-in of a "
            "system-generated attendance record created when a "
            "sign-out is detected as an anomaly (outside the check "
            "out buffer). Falls back to the module's default check "
            "in reason when left empty."
        ),
    )
    attendance_location_required = fields.Boolean(
        string="Require Registered Attendance Location",
        default=False,
        help=(
            "When enabled, an attendance whose check-in or check-out "
            "coordinate does not fall within any registered "
            "attendance location's radius is rejected. Does not, by "
            "itself, make a GPS reading mandatory - an attendance "
            "created without any coordinate at all (Sign In/Sign Out, "
            "the top bar widget, or the backend menu) is unaffected "
            "either way."
        ),
    )
