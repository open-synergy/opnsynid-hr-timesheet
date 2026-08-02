# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
# pylint: disable=locally-disabled, manifest-required-author
{
    "name": "Timesheet Attendance Shift",
    "version": "14.0.1.0.0",
    "website": "https://simetri-sinergi.id",
    "author": "OpenSynergy Indonesia, PT. Simetri Sinergi Indonesia",
    "contributors": [
        "Andhitia Rama <andhitia.r@gmail.com>",
    ],
    "license": "AGPL-3",
    "installable": True,
    "application": False,
    "depends": [
        "ssi_timesheet_attendance",
        "ssi_master_data_mixin",
        "ssi_hr",
        "web_tour",
    ],
    "data": [
        "security/res_groups/hr_attendance_shift.xml",
        "security/ir_model_access/hr_attendance_shift.xml",
        "security/ir_model_access/hr_attendance_shift_pattern.xml",
        "security/ir_model_access/hr_attendance_shift_assignment.xml",
        "views/hr_attendance_shift_views.xml",
        "views/hr_attendance_shift_pattern_views.xml",
        "views/hr_attendance_shift_assignment_views.xml",
        "views/ssi_timesheet_attendance_shift_assets.xml",
    ],
}
