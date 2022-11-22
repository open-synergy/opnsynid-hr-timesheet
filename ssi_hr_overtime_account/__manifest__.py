# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    "name": "Overtime Account",
    "version": "14.0.1.1.0",
    "website": "https://simetri-sinergi.id",
    "author": "PT. Simetri Sinergi Indonesia, OpenSynergy Indonesia",
    "license": "LGPL-3",
    "installable": True,
    "depends": [
        "ssi_hr_overtime",
        "ssi_financial_accounting",
    ],
    "data": [
        "views/hr_overtime_views.xml",
        "views/hr_overtime_type_views.xml",
    ],
}
