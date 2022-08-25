# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Leave Management",
    "version": "8.0.1.0.0",
    "website": "https://simetri-sinergi.id",
    "author": "PT. Simetri Sinergi Indonesia, OpenSynergy Indonesia",
    "license": "LGPL-3",
    "installable": True,
    "depends": [
        "base_public_holiday",
        "base_multiple_approval",
        "base_workflow_policy",
        "base_sequence_configurator",
        "base_cancel_reason",
        "base_terminate_reason",
        "base_action_rule",
        "hr_timesheet_contract",
        "hr_timesheet_attendance_schedule",
        "web_readonly_bypass",
    ],
    "data": [
        "security/ir.model.access.csv",
        "data/ir_sequence_data.xml",
        "data/base_sequence_configurator_data.xml",
        "data/base_cancel_reason_configurator_data.xml",
        "data/base_workflow_policy_leave_data.xml",
        "data/base_workflow_policy_leave_all_data.xml",
        "data/ir_actions_server_data.xml",
        "data/ir_filters_data.xml",
        "data/base_action_rule_data.xml",
        "menu.xml",
        "views/hr_leave_type_views.xml",
        "views/hr_leave_views.xml",
        "views/hr_leave_allocation_views.xml",
        "views/hr_timesheet_sheet_views.xml",
    ],
    "demo": [
        "demo/hr_leave_type_data_demo.xml",
    ],
}
