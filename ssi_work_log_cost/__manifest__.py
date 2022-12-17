# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Work Log Cost",
    "version": "14.0.1.1.0",
    "website": "https://simetri-sinergi.id",
    "author": "PT. Simetri Sinergi Indonesia, OpenSynergy Indonesia",
    "license": "LGPL-3",
    "installable": True,
    "depends": [
        "ssi_work_log_mixin",
        "ssi_product_line_account_mixin",
    ],
    "data": [
        "data/policy_template_data.xml",
        "views/hr_work_log_views.xml",
        "views/ir_model_views.xml",
    ],
}
