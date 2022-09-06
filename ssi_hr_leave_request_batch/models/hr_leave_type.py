# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
from openerp import fields, models


class HrLeaveType(models.Model):
    _inherit = "hr.leave_type"

    sequence_batch_id = fields.Many2one(
        string="Sequence Batch",
        comodel_name="ir.sequence",
        company_dependent=True,
    )
    batch_confirm_group_ids = fields.Many2many(
        string="Allowed to Confirm",
        comodel_name="res.groups",
        relation="rel_leave_type_batch_confirm_groups",
        column1="leave_type_id",
        column2="group_id",
    )
    batch_cancel_group_ids = fields.Many2many(
        string="Allowed to Cancel",
        comodel_name="res.groups",
        relation="rel_leave_type_batch_cancel_groups",
        column1="leave_type_id",
        column2="group_id",
    )
    batch_restart_group_ids = fields.Many2many(
        string="Allowed to Restart",
        comodel_name="res.groups",
        relation="rel_leave_type_batch_restart_groups",
        column1="leave_type_id",
        column2="group_id",
    )
    batch_approve_group_ids = fields.Many2many(
        string="Allowed to Approve",
        comodel_name="res.groups",
        relation="rel_leave_type_batch_approve_groups",
        column1="leave_type_id",
        column2="group_id",
    )
    batch_reject_group_ids = fields.Many2many(
        string="Allowed to Reject",
        comodel_name="res.groups",
        relation="rel_leave_type_batch_reject_groups",
        column1="leave_type_id",
        column2="group_id",
    )
    batch_restart_approval_group_ids = fields.Many2many(
        string="Allowed to Restart Approval",
        comodel_name="res.groups",
        relation="rel_leave_type_batch_restart_approval_groups",
        column1="leave_type_id",
        column2="group_id",
    )
