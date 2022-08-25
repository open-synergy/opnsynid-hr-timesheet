# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from openerp import _, api, fields, models
from openerp.exceptions import Warning as UserError


class HrLeaveType(models.Model):
    _name = "hr.leave_type"
    _inherit = [
        "mail.thread",
    ]
    _description = "Leave Type"

    name = fields.Char(
        string="Name",
        required=True,
    )
    code = fields.Char(
        string="Code",
        required=True,
    )
    sequence_id = fields.Many2one(
        string="Sequence",
        comodel_name="ir.sequence",
        company_dependent=True,
    )
    need_allocation = fields.Boolean(
        string="Need Allocation",
        default=False,
    )
    apply_limit_per_request = fields.Boolean(
        string="Apply Limit Per Request",
        default=False,
    )
    limit_per_request = fields.Integer(
        string="Limit Per Request",
        default=False,
    )
    exclude_public_holiday = fields.Boolean(
        string="Exclude Public Holiday",
        default=False,
    )
    exclude_rest_day = fields.Boolean(
        string="Exclude Rest Day",
        default=False,
    )
    active = fields.Boolean(
        string="Active",
        default=True,
    )
    note = fields.Text(
        string="Note",
    )
    # POLICY LEAVE
    leave_confirm_group_ids = fields.Many2many(
        string="Allowed to Confirm",
        comodel_name="res.groups",
        relation="rel_leave_type_confirm_groups",
        column1="leave_type_id",
        column2="group_id",
    )
    leave_cancel_group_ids = fields.Many2many(
        string="Allowed to Cancel",
        comodel_name="res.groups",
        relation="rel_leave_type_cancel_groups",
        column1="leave_type_id",
        column2="group_id",
    )
    leave_restart_group_ids = fields.Many2many(
        string="Allowed to Restart",
        comodel_name="res.groups",
        relation="rel_leave_type_restart_groups",
        column1="leave_type_id",
        column2="group_id",
    )
    leave_approve_group_ids = fields.Many2many(
        string="Allowed to Approve",
        comodel_name="res.groups",
        relation="rel_leave_type_approve_groups",
        column1="leave_type_id",
        column2="group_id",
    )
    leave_reject_group_ids = fields.Many2many(
        string="Allowed to Reject",
        comodel_name="res.groups",
        relation="rel_leave_type_reject_groups",
        column1="leave_type_id",
        column2="group_id",
    )
    leave_restart_approval_group_ids = fields.Many2many(
        string="Allowed to Restart Approval",
        comodel_name="res.groups",
        relation="rel_leave_type_restart_approval_groups",
        column1="leave_type_id",
        column2="group_id",
    )
    # POLICY LEAVE ALLOCATION
    leave_all_confirm_group_ids = fields.Many2many(
        string="Allowed to Confirm",
        comodel_name="res.groups",
        relation="rel_leave_type_all_confirm_groups",
        column1="leave_type_id",
        column2="group_id",
    )
    leave_all_done_group_ids = fields.Many2many(
        string="Allowed to Finish",
        comodel_name="res.groups",
        relation="rel_leave_type_all_done_groups",
        column1="leave_type_id",
        column2="group_id",
    )
    leave_all_cancel_group_ids = fields.Many2many(
        string="Allowed to Cancel",
        comodel_name="res.groups",
        relation="rel_leave_type_all_cancel_groups",
        column1="leave_type_id",
        column2="group_id",
    )
    leave_all_terminate_group_ids = fields.Many2many(
        string="Allowed to Terminate",
        comodel_name="res.groups",
        relation="rel_leave_type_all_terminate_groups",
        column1="leave_type_id",
        column2="group_id",
    )
    leave_all_restart_group_ids = fields.Many2many(
        string="Allowed to Restart",
        comodel_name="res.groups",
        relation="rel_leave_type_all_restart_groups",
        column1="leave_type_id",
        column2="group_id",
    )
    leave_all_approve_group_ids = fields.Many2many(
        string="Allowed to Approve",
        comodel_name="res.groups",
        relation="rel_leave_type_all_approve_groups",
        column1="leave_type_id",
        column2="group_id",
    )
    leave_all_reject_group_ids = fields.Many2many(
        string="Allowed to Approve",
        comodel_name="res.groups",
        relation="rel_leave_type_all_reject_groups",
        column1="leave_type_id",
        column2="group_id",
    )
    leave_all_restart_approval_group_ids = fields.Many2many(
        string="Allowed to Restart Approval",
        comodel_name="res.groups",
        relation="rel_leave_type_all_restart_approval_groups",
        column1="leave_type_id",
        column2="group_id",
    )

    @api.returns("self", lambda value: value.id)
    def copy(self, default=None):
        self.ensure_one()
        if default is None:
            default = {}
        if "code" not in default:
            default["code"] = _("%s (copy)", self.code)
        return super(HrLeaveType, self).copy(default=default)

    @api.constrains("code")
    def _check_duplicate_code(self):
        error_msg = _("Duplicate code not allowed")
        for record in self:
            criteria = [
                ("code", "=", record.code),
                ("id", "!=", record.id),
            ]
            count_duplicate = self.search_count(criteria)
            if count_duplicate > 0:
                raise UserError(error_msg)
