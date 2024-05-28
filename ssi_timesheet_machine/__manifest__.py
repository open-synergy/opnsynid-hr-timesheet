# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
# pylint: disable=locally-disabled, manifest-required-author
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
        "menu.xml",
        "views/hr_machine_views.xml",
    ],
}
