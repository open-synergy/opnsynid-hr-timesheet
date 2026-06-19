# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
# pylint: disable=locally-disabled, manifest-required-author
{
    "name": "Timesheet + Operating Unit",
    "version": "14.0.1.1.0",
    "website": "https://simetri-sinergi.id",
    "author": "OpenSynergy Indonesia, PT. Simetri Sinergi Indonesia",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "ssi_timesheet",
        "ssi_operating_unit_mixin",
        "ssi_hr_employee_operating_unit",
    ],
    "data": [
        "security/res_group/hr_timesheet.xml",
        "security/ir_rule/hr_timesheet.xml",
        "views/hr_timesheet_views.xml",
        "wizards/timesheet_summary_report.xml",
    ],
}
