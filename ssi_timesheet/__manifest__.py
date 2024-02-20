# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Timesheets",
    "version": "14.0.1.8.0",
    "website": "https://simetri-sinergi.id",
    "author": "OpenSynergy Indonesia, PT. Simetri Sinergi Indonesia",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "ssi_hr",
        "ssi_master_data_mixin",
        "ssi_transaction_open_mixin",
        "ssi_transaction_confirm_mixin",
        "ssi_transaction_done_mixin",
        "ssi_transaction_cancel_mixin",
        "ssi_duration_mixin",
        "ssi_employee_document_mixin",
    ],
    "data": [
        "security/ir_module_category_data.xml",
        "security/res_group_data.xml",
        "security/ir.model.access.csv",
        "security/ir_rule_data.xml",
        "data/ir_sequence_data.xml",
        "data/sequence_template_data.xml",
        "data/policy_template_data.xml",
        "data/approval_template_data.xml",
        "menu.xml",
        "views/hr_timesheet_computation_item_views.xml",
        "views/hr_timesheet_views.xml",
        "views/hr_employee_views.xml",
        "wizards/generate_timesheet.xml",
        "reports/hr_timesheet_computation_analysis.xml",
    ],
}
