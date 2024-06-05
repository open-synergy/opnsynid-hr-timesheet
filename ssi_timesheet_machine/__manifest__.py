# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Timesheet Machine",
    "version": "14.0.1.0.0",
    "website": "https://simetri-sinergi.id",
    "author": "OpenSynergy Indonesia, PT. Simetri Sinergi Indonesia",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "ssi_master_data_mixin",
        "ssi_timesheet_attendance",
    ],
    "data": [
        "security/res_group_data.xml",
        "security/ir.model.access.csv",
        "data/ir_cron.xml",
        "menu.xml",
        "views/hr_data_machine_views.xml",
        "views/hr_attendance_machine_views.xml",
        "views/res_config_settings_view.xml",
        "wizard/hr_attendance_machine_import_wizard_views.xml",
    ],
}
