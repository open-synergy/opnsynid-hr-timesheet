# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Work Log Mixin",
    "version": "14.0.1.16.0",
    "website": "https://simetri-sinergi.id",
    "author": "OpenSynergy Indonesia, PT. Simetri Sinergi Indonesia",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "analytic",
        "ssi_timesheet",
        "ssi_hr",
    ],
    "data": [
        "menu.xml",
        "security/ir_module_category_data.xml",
        "security/res_group_data.xml",
        "security/ir.model.access.csv",
        "security/ir_rule_data.xml",
        "data/ir_sequence_data.xml",
        "data/sequence_template_data.xml",
        "data/approval_template_data.xml",
        "data/policy_template_data.xml",
        "templates/work_log_mixin_templates.xml",
        "views/ir_model_views.xml",
        "views/hr_work_log_tag_views.xml",
        "views/hr_work_log_views.xml",
        "views/hr_timesheet_views.xml",
        "views/account_analytic_account_views.xml",
        "report/hr_work_log_analysis.xml",
        "report/hr_project_work_log_analysis.xml",
    ],
}
