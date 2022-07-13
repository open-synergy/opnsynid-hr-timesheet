# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
# pylint: disable=locally-disabled, manifest-required-author
{
    "name": "Timesheet Attendance",
    "version": "14.0.1.2.0",
    "website": "https://simetri-sinergi.id",
    "author": "PT. Simetri Sinergi Indonesia, OpenSynergy Indonesia",
    "license": "LGPL-3",
    "installable": True,
    "depends": [
        "ssi_timesheet",
        "ssi_duration_mixin",
        "base_public_holiday",
    ],
    "data": [
        "security/res_group_data.xml",
        "security/ir.model.access.csv",
        "menu.xml",
        "views/hr_attendance_reason_views.xml",
        "views/hr_timesheet_views.xml",
    ],
}
