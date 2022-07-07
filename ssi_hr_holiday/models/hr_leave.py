# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).


from odoo import _, api, fields, models
from odoo.exceptions import Warning as UserError


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

    # Attributes related to add element on duration_view automatically
    _date_start_readonly = True
    _date_end_readonly = True

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
        if self.employee_id and self.date_start and self.date_end:
            obj_sheet = self.env["hr.timesheet"]
            for record in self:
                sheet_id = False
                # check date_start
                criteria = [
                    ("employee_id", "=", record.employee_id.id),
                    ("date_start", "<=", record.date_start),
                    ("date_end", ">=", record.date_end),
                    ("state", "in", ["draft", "open"]),
                ]
                sheet = obj_sheet.search(criteria, limit=1)
                if len(sheet) > 0:
                    sheet_id = sheet[0].id
                else:
                    strWarning = _(
                        "Sheet Not FOUND or State Is Closed or Cancelled\n"
                        + "Please Check Timesheet First"
                    )
                    raise UserError(strWarning)
                record.sheet_id = sheet_id

    sheet_id = fields.Many2one(
        string="Sheet",
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
        if self.date_start and self.date_end and self.employee_id:
            obj_schedule = self.env["hr.timesheet_attendance_schedule"]
            for record in self:
                pass
                # check date_start
                criteria = [
                    ("employee_id", "=", record.employee_id.id),
                    ("date", "<=", record.date_end),
                    ("date", ">=", record.date_start),
                ]
                schedule = obj_schedule.search(criteria)
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
        leave_duration = 0
        for record in self:
            if record.date_start and record.date_end:
                leave_duration = (record.date_end - record.date_start).days + 1
            record.leave_duration = leave_duration

    leave_duration = fields.Integer(
        string="Duration",
        compute="_compute_leave_duration",
        default=0,
        store=True,
        compute_sudo=True,
    )
    date_start = fields.DateCallable(
        states={
            "draft": [("readonly", False)],
        },
    )
    date_end = fields.DateCallable(
        states={
            "draft": [("readonly", False)],
        },
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

    leave_allocation_id = fields.Many2one(
        string="Leave Allocation",
        comodel_name="hr.leave_allocation",
        ondelete="restrict",
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

    def _prepare_cancel_data(self, cancel_reason=False):
        self.ensure_one()
        _super = super(HRLeave, self)
        res = _super._prepare_cancel_data(cancel_reason)
        res["sheet_id"] = False
        res["schedule_ids"] = False
        res["leave_allocation_id"] = False
        return res

    def action_confirm(self):
        _super = super(HRLeave, self)
        _super.action_confirm()
        for record in self.sudo():
            if not record.schedule_ids:
                record._compute_schedule_ids()
            # sheet
            if not record.sheet_id:
                record._compute_sheet()
            # allocation
            if record.type_id.need_allocation:
                record._get_leave_allocation_id()

    @api.onchange(
        "employee_id",
    )
    def onchange_policy_template_id(self):
        template_id = self._get_template_policy()
        self.policy_template_id = template_id

    @api.onchange(
        "employee_id",
        "type_id",
    )
    def onchange_leave_allocation_id(self):
        self.leave_allocation_id = False

    @api.onchange(
        "leave_duration",
    )
    def onchange_number_of_day(self):
        self.number_of_days = self.leave_duration

    def _get_leave_allocation_id(self):
        obj_la = self.env["hr.leave_allocation"]
        for leave in self:
            leave_allocation_id = False
            if leave.employee_id and leave.type_id and leave.date_start:
                criteria = [
                    "|",
                    "&",
                    "&",
                    "&",
                    "&",
                    "&",
                    ("type_id", "=", leave.type_id.id),
                    ("employee_id", "=", leave.employee_id.id),
                    ("date_start", "<=", leave.date_start),
                    ("date_end", "=", False),
                    ("state", "=", "open"),
                    ("num_of_days_available", ">=", leave.number_of_days),
                    "&",
                    "&",
                    "&",
                    "&",
                    "&",
                    ("type_id", "=", leave.type_id.id),
                    ("employee_id", "=", leave.employee_id.id),
                    ("date_start", "<=", leave.date_start),
                    ("date_end", ">=", leave.date_end),
                    ("state", "=", "open"),
                    ("num_of_days_available", ">=", leave.number_of_days),
                ]
                la = obj_la.search(criteria, order="date_start asc", limit=1)
                if len(la) > 0:
                    leave_allocation_id = la[0].id
                else:
                    strWarning = _(
                        "Leave Allocation Not FOUND ..\nPlease Check Leave Allocation"
                    )
                    raise UserError(strWarning)
                leave.leave_allocation_id = leave_allocation_id

    @api.constrains("date_start", "date_end")
    def _check_date_start_end(self):
        for leave in self:
            obj_leave = self.env["hr.leave"]
            # cek date_start
            str_error = _("Date Start has been used on another request")
            criteria = [
                ("employee_id", "=", leave.employee_id.id),
                ("date_start", "<=", leave.date_start),
                ("date_end", ">=", leave.date_start),
                ("state", "not in", ["cancel", "reject"]),
                ("id", "!=", leave.id),
            ]
            if len(obj_leave.search(criteria)) > 0:
                raise UserError(str_error)
            # cek date_end
            str_error = _("Date End has been used on another leave")
            criteria = [
                ("employee_id", "=", leave.employee_id.id),
                ("date_start", "<=", leave.date_end),
                ("date_end", ">=", leave.date_end),
                ("state", "not in", ["cancel", "reject"]),
                ("id", "!=", leave.id),
            ]
            if len(obj_leave.search(criteria)) > 0:
                raise UserError(str_error)
            # cek date_start date_end
            str_error = _("Date Start and Date End has been used on another leave")
            criteria = [
                ("employee_id", "=", leave.employee_id.id),
                ("date_start", ">=", leave.date_start),
                ("date_end", "<=", leave.date_end),
                ("state", "not in", ["cancel", "reject"]),
                ("id", "!=", leave.id),
            ]
            if len(obj_leave.search(criteria)) > 0:
                raise UserError(str_error)

    @api.constrains("type_id", "number_of_days")
    def _check_limit_request(self):
        for leave in self:
            if leave.type_id.apply_limit_per_request:
                if leave.number_of_days > leave.type_id.limit_per_request:
                    limit = str(leave.type_id.limit_per_request)
                    str_error = _("Number of days must <= limit %s days" % (limit))
                    raise UserError(str_error)

    # Check STATE
    @api.constrains("state")
    def _check_state(self):
        for record in self.sudo():
            if record.state in ["cancel", "reject"]:
                # raise UserError("Constraint 1 "+str(record.sheet_id.state))
                if record.sheet_id.state == "done":
                    str_error = _("You cannot process ..\nSheet already DONE")
                    raise UserError(str_error)
                if record.leave_allocation_id.state in ["done", "terminate"]:
                    str_error = _(
                        "You cannot process ..\n" + "Allocation already DONE/Terminate"
                    )
                    raise UserError(str_error)
