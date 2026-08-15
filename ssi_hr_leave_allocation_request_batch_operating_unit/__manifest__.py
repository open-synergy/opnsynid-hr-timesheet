# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
# pylint: disable=locally-disabled, manifest-required-author
{
    "name": "Leave Allocation Request Batch + Operating Unit",
    "version": "14.0.1.1.0",
    "website": "https://simetri-sinergi.id",
    "author": "OpenSynergy Indonesia, PT. Simetri Sinergi Indonesia",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "ssi_hr_leave_allocation_request_batch",
        "ssi_operating_unit_mixin",
        "web_tour",
    ],
    "data": [
        "security/res_group/res_group_data.xml",
        "security/ir_rule/ir_rule_data.xml",
        "views/hr_leave_allocation_request_batch_view.xml",
        "views/ssi_hr_leave_allocation_request_batch_operating_unit_assets_tests.xml",
    ],
}
