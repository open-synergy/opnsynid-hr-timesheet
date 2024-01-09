# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from dateutil.rrule import DAILY, rrule

from odoo import _, api, fields, models
from odoo.exceptions import Warning as UserError

from odoo.addons.ssi_decorator import ssi_decorator


class HRLeave(models.Model):
    _name = "hr.leave"
    _inherit = [
        "mixin.transaction_confirm",
        "mixin.transaction_done",
        "mixin.transaction_cancel",
        "mixin.date_duration",
        "mixin.employee_document",
    ]
    _description = "Leaves"

    # Multiple Approval Attribute
    _approval_from_state = "draft"
    _approval_to_state = "done"
    _approval_state = "confirm"
    _after_approved_method = "action_done"

    # Attributes related to add element on view automatically
    _automatically_insert_view_element = True
    _automatically_insert_done_button = False
    _automatically_insert_done_policy_fields = False

    # Mixin duration attribute
    _date_start_readonly = True
    _date_end_readonly = True
    _date_start_states_list = ["draft"]
    _date_start_states_readonly = ["draft"]
    _date_end_states_list = ["draft"]
    _date_end_states_readonly = ["draft"]

    # Attributes related to add element on form view automatically
    _automatically_insert_multiple_approval_page = True
    _statusbar_visible_label = "draft,confirm,done,rejected"
    _policy_field_order = [
        "confirm_ok",
        "approve_ok",
        "reject_ok",
        "restart_approval_ok",
        "cancel_ok",
        "restart_ok",
        "manual_number_ok",
    ]
    _header_button_order = [
        "action_confirm",
        "action_approve_approval",
        "action_reject_approval",
        "%(ssi_transaction_cancel_mixin.base_select_cancel_reason_action)d",
        "action_restart",
    ]

    # Attributes related to add element on search view automatically
    _state_filter_order = [
        "dom_draft",
        "dom_confirm",
        "dom_reject",
        "dom_done",
        "dom_cancel",
    ]

    # Sequence attribute
    _create_sequence_state = "done"

    @api.depends(
        "employee_id",
        "date_start",
        "date_end",
    )
    def _compute_sheet(self):
        obj_sheet = self.env["hr.timesheet"]
        for record in self:
            sheet_id = False
            if record.employee_id and record.date_start and record.date_end:
                criteria = [
                    ("employee_id", "=", record.employee_id.id),
                    ("date_start", "<=", record.date_start),
                    ("date_end", ">=", record.date_end),
                ]
                sheet = obj_sheet.search(criteria, limit=1)
                if len(sheet) > 0:
                    sheet_id = sheet[0].id
            record.sheet_id = sheet_id

    sheet_id = fields.Many2one(
        string="# Timesheet",
        comodel_name="hr.timesheet",
        compute="_compute_sheet",
        store=True,
        compute_sudo=True,
    )

    @api.depends(
        "date_start",
        "date_end",
        "employee_id",
    )
    def _compute_schedule_ids(self):
        AttendanceSchedule = self.env["hr.timesheet_attendance_schedule"]
        for record in self:
            if record.date_start and record.date_end and record.employee_id:
                criteria = [
                    ("employee_id", "=", record.employee_id.id),
                    ("date", "<=", record.date_end),
                    ("date", ">=", record.date_start),
                ]
                schedule = AttendanceSchedule.search(criteria)
                record.schedule_ids = schedule.ids

    schedule_ids = fields.Many2many(
        string="Schedules",
        comodel_name="hr.timesheet_attendance_schedule",
        compute="_compute_schedule_ids",
        relation="rel_attendance_schedule_2_leave",
        column1="leave_id",
        column2="attendance_schedule_id",
        store=True,
        compute_sudo=True,
    )

    number_of_days = fields.Integer(
        string="Number of Days",
        required=True,
        default=0,
        readonly=True,
        states={
            "draft": [("readonly", False)],
        },
    )

    @api.depends(
        "date_start",
        "date_end",
    )
    def _compute_leave_duration(self):
        PublicHoliday = self.env["base.public.holiday"]
        for record in self:
            leave_duration = 0
            if record.date_start and record.date_end:
                leave_duration = len(record.schedule_ids)
                leave_dates = rrule(
                    DAILY,
                    dtstart=record.date_start,
                    count=leave_duration,
                )
                for leave_date in list(leave_dates):
                    if PublicHoliday.is_public_holiday(leave_date):
                        leave_duration -= 1
            record.leave_duration = leave_duration

    leave_duration = fields.Integer(
        string="Duration",
        compute="_compute_leave_duration",
        store=True,
        compute_sudo=True,
    )
    type_id = fields.Many2one(
        string="Leave Type",
        comodel_name="hr.leave_type",
        required=True,
        ondelete="restrict",
        readonly=True,
        states={
            "draft": [("readonly", False)],
        },
    )

    @api.depends(
        "type_id",
        "employee_id",
        "date_start",
        "date_end",
    )
    def _compute_leave_allocation_id(self):
        for record in self:
            result = False
            if (
                record.type_id
                and record.employee_id
                and record.date_start
                and record.date_end
            ):
                result = record._get_leave_allocation()
            record.leave_allocation_id = result

    leave_allocation_id = fields.Many2one(
        string="# Leave Allocation",
        comodel_name="hr.leave_allocation",
        ondelete="restrict",
        compute="_compute_leave_allocation_id",
        store=True,
        compute_sudo=True,
        readonly=True,
    )
    state = fields.Selection(
        string="State",
        selection=[
            ("draft", "Draft"),
            ("confirm", "Waiting for Approval"),
            ("done", "Done"),
            ("cancel", "Cancelled"),
            ("reject", "Rejected"),
        ],
        default="draft",
        copy=False,
    )

    @api.model
    def _get_policy_field(self):
        res = super(HRLeave, self)._get_policy_field()
        policy_field = [
            "confirm_ok",
            "approve_ok",
            "done_ok",
            "cancel_ok",
            "reject_ok",
            "restart_ok",
            "restart_approval_ok",
            "manual_number_ok",
        ]
        res += policy_field
        return res

    @api.onchange(
        "employee_id",
    )
    def onchange_policy_template_id(self):
        template_id = self._get_template_policy()
        self.policy_template_id = template_id

    @api.onchange(
        "leave_duration",
    )
    def onchange_number_of_day(self):
        self.number_of_days = self.leave_duration

    def _get_leave_allocation(self):
        self.ensure_one()
        LeaveAllocation = self.env["hr.leave_allocation"]
        criteria = [
            ("type_id", "=", self.type_id.id),
            ("employee_id", "=", self.employee_id.id),
            ("state", "=", "open"),
            ("num_of_days_available", ">=", self.number_of_days),
            ("date_start", "<=", self.date_start),
            ("date_extended", ">=", self.date_end),
        ]
        leave_allocation_id = LeaveAllocation.search(
            criteria, order="date_start asc", limit=1
        )
        return leave_allocation_id

    @api.constrains("sheet_id")
    def _constrains_sheet_id(self):
        for record in self.sudo():
            if not record.sheet_id:
                error_message = _(
                    """
                Context: Create Leave Request
                Database ID: %s
                Problem: Timesheet not found for employee %s
                Solution: Create Timesheet
                """
                    % (record.id, record.employee_id.name)
                )
                raise UserError(error_message)

    @api.constrains("date_start", "date_end", "employee_id")
    def _constrains_overlap(self):
        for record in self.sudo():
            if not record._check_overlap():
                error_message = _(
                    """
                Context: Change date start or date end on leave request
                Database ID: %s
                Problem: There are other leave(s) that overlap
                Solution: Change date start and date end
                """
                    % (record.id)
                )
                raise UserError(error_message)

    @api.constrains("type_id", "number_of_days")
    def _constrains_limit_request(self):
        for record in self.sudo():
            limit = record.type_id.limit_per_request
            if not record._check_limit_per_request():
                error_message = _(
                    """
                Context: Change type or number of days on leave request
                Database ID: %s
                Problem: Number of days exceed %s
                Solution: Reduce number of days so it is less or equal than %s
                """
                    % (record.id, limit, limit)
                )
                raise UserError(error_message)

    @api.constrains("state")
    def _constrains_confirm(self):
        for record in self.sudo():
            if record.state != "confirm":
                break

            if not record._check_leave_allocation_available():
                error_message = """
                    Context: Confirming leave
                    Database ID: %s
                    Problem: Leave need leave allocation request.
                             No available leave allocation request found
                             or number of available_days on leave allocation < number of days
                    Solution: - Create or check relevant leave allocation
                              - Edit date start or date end on leave request
                    """ % (
                    record.id
                )
                raise UserError(_(error_message))

    def _check_overlap(self):
        self.ensure_one()
        result = True
        Leave = self.env["hr.leave"]
        criteria = [
            ("employee_id", "=", self.employee_id.id),
            ("state", "not in", ["cancel", "reject"]),
            ("id", "!=", self.id),
            ("date_start", "<=", self.date_end),
            ("date_end", ">=", self.date_start),
        ]
        num_of_leave = Leave.search_count(criteria)
        if num_of_leave > 0:
            result = False

        return result

    def _check_limit_per_request(self):
        self.ensure_one()
        result = True
        if (
            self.type_id.apply_limit_per_request
            and self.number_of_days > self.type_id.limit_per_request
        ):
            result = False
        return result

    def _check_leave_allocation_available(self):
        self.ensure_one()
        result = True
        if self.type_id.need_allocation:
            if not self.leave_allocation_id:
                result = False
        return result

    @ssi_decorator.pre_confirm_action()
    def _compute_schedule_leave_allocation(self):
        self.ensure_one()
        if not self.schedule_ids:
            self._compute_schedule_ids()
        self._compute_leave_allocation_id()

    @ssi_decorator.pre_cancel_action()
    def _reopen_leave_allocation(self):
        self.ensure_one()
        leave_allocation_ids = self.mapped("leave_allocation_id").filtered(
            lambda allocation: allocation.state == "done"
        )
        if leave_allocation_ids:
            leave_allocation_ids.action_open()
