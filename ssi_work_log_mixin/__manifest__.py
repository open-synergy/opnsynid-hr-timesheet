# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Work Log Mixin",
    "version": "14.0.1.0.0",
    "website": "https://simetri-sinergi.id",
    "author": "PT. Simetri Sinergi Indonesia, OpenSynergy Indonesia",
    "license": "LGPL-3",
    "installable": True,
    "depends": [
        "ssi_timesheet",
    ],
    "data": [
        "menu.xml",
        "security/ir.model.access.csv",
        "templates/work_log_mixin_templates.xml",
        "views/ir_model_views.xml",
        "views/hr_work_log_views.xml",
        "views/hr_timesheet_views.xml",
    ],
}