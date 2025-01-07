# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from datetime import datetime

from odoo import _, api, fields, models
from odoo.exceptions import Warning as UserError


class HROvertime(models.Model):
    _name = "hr.overtime"
    _inherit = [
        "mixin.transaction_confirm",
        "mixin.transaction_done",
        "mixin.transaction_cancel",
        "mixin.datetime_duration",
        "mixin.employee_document",
    ]
    _description = "Overtimes"

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

    type_id = fields.Many2one(
        string="Overtime Type",
        comodel_name="hr.overtime_type",
        required=True,
        ondelete="restrict",
        readonly=True,
        states={
            "draft": [("readonly", False)],
        },
    )
    apply_limit_per_day = fields.Boolean(
        related="type_id.apply_limit_per_day",
        store=False,
        readonly=True,
    )
    limit_per_day = fields.Integer(
        related="type_id.limit_per_day",
        store=False,
        readonly=True,
    )

    @api.depends(
        "employee_id",
        "date",
    )
    def _compute_sheet(self):
        obj_sheet = self.env["hr.timesheet"]
        for record in self:
            sheet_id = False
            if record.employee_id and record.date:
                criteria = [
                    ("employee_id", "=", record.employee_id.id),
                    ("date_start", "<=", record.date),
                    ("date_end", ">=", record.date),
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

    date = fields.Date(
        string="Date",
        required=True,
        default=lambda self: fields.Date.today(),
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    date_start = fields.Datetime(
        required=True,
        readonly=True,
        default=lambda self: fields.Datetime.now(),
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    date_end = fields.Datetime(
        required=True,
        readonly=True,
        default=lambda self: fields.Datetime.now(),
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )

    planned_hour = fields.Float(
        string="Planned Hours",
        required=True,
        default=0,
        store=True,
        compute="_compute_hour",
        compute_sudo=True,
        readonly=True,
    )
    realized_hour = fields.Float(
        string="Realiazed Hours",
        required=True,
        default=0,
        store=True,
        compute="_compute_hour",
        compute_sudo=True,
        readonly=True,
    )

    @api.depends(
        "date_start",
        "date_end",
        "attendance_ids",
    )
    def _compute_hour(self):
        for record in self:
            planned_hour = 0.0
            realized_hour = 0.0
            if record.date_start and record.date_end:
                planned_hour = (
                    record.date_end - record.date_start
                ).total_seconds() / 3600.0
                if record.attendance_ids:
                    for data in record.attendance_ids:
                        start = record.date_start
                        end = record.date_end
                        if record.date_start < data.check_in:
                            start = data.check_in
                        if record.date_end > data.check_out:
                            end = data.check_out
                        realized_hour += (end - start).total_seconds() / 3600.0
            record.realized_hour = realized_hour
            record.planned_hour = planned_hour

    attendance_ids = fields.Many2many(
        string="Attendances",
        comodel_name="hr.timesheet_attendance",
        relation="rel_attendance_2_overtime",
        column1="overtime_id",
        column2="attendance_id",
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
        res = super(HROvertime, self)._get_policy_field()
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
        _super = super(HROvertime, self)
        res = _super._prepare_cancel_data(cancel_reason)
        res["attendance_ids"] = False
        return res

    def action_confirm(self):
        _super = super(HROvertime, self)
        for record in self.sudo():
            # Function get attendance
            record._get_attendance()
        _super.action_confirm()

    def _get_attendance(self):
        self.ensure_one()
        obj_att = self.env["hr.timesheet_attendance"]
        criteria = [
            ("employee_id", "=", self.employee_id.id),
            ("date", "=", self.date),
        ]
        att = obj_att.search(criteria)
        if len(att) > 0:
            for record in att:
                record._compute_overtime_ids()

    @api.onchange(
        "employee_id",
    )
    def onchange_policy_template_id(self):
        template_id = self._get_template_policy()
        self.policy_template_id = template_id

    @api.constrains("sheet_id")
    def _constrains_sheet_id(self):
        for record in self.sudo():
            if not record.sheet_id:
                error_message = _(
                    """
                Context: Create Overtime
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
                Context: Change date start or date end on overtime request
                Database ID: %s
                Problem: There are other overtime(s) that overlap
                Solution: Change date start and date end
                """
                    % (record.id)
                )
                raise UserError(error_message)

    def _check_overlap(self):
        self.ensure_one()
        result = True
        overtime = self.env["hr.overtime"]
        criteria = [
            ("employee_id", "=", self.employee_id.id),
            ("state", "not in", ["cancel", "reject"]),
            ("id", "!=", self.id),
            ("date_start", "<=", self.date_end),
            ("date_end", ">=", self.date_start),
        ]
        num_of_overtime = overtime.search_count(criteria)
        if num_of_overtime > 0:
            result = False

        return result

    @api.constrains("date", "planned_hour", "employee_id")
    def _constrains_limit(self):
        for record in self.sudo():
            if not record.apply_limit_per_day:
                break
            if not record._check_limit():
                error_message = _(
                    """
                Context: Change date start or date end on overtime request
                Database ID: %s
                Problem: Total OT Planned cannot bigger than limit per days
                Solution: Change date start or date end
                """
                    % (record.id)
                )
                raise UserError(error_message)

    def _check_limit(self):
        self.ensure_one()
        result = True
        criteria = [
            ("employee_id", "=", self.employee_id.id),
            ("state", "not in", ["cancel", "reject"]),
            ("id", "!=", self.id),
            ("date", "=", self.date),
            ("type_id", "=", self.type_id.id),
        ]
        overtime_ids = self.search(criteria)
        total_ot = 0.0
        if overtime_ids:
            for rec in overtime_ids:
                total_ot += rec.planned_hour
        if total_ot + self.planned_hour > self.limit_per_day:
            result = False
        return result

    @api.constrains("date", "date_start")
    def _constrains_start(self):
        for record in self.sudo():
            if not record._check_start():
                error_message = _(
                    """
                Context: Change date start on overtime request
                Database ID: %s
                Problem: Date and Date Start is different
                Solution: Change date start
                """
                    % (record.id)
                )
                raise UserError(error_message)

    def _check_start(self):
        self.ensure_one()
        result = True
        cek_date = datetime.date(
            fields.Datetime.context_timestamp(self, self.date_start)
        )
        if cek_date != self.date:
            result = False
        return result

    @api.constrains("date_start", "date_end")
    def _constrains_date_start_end(self):
        for record in self.sudo():
            if not record._check_date_start_end():
                error_message = _(
                    """
                Context: Change date start or date end on overtime request
                Database ID: %s
                Problem: Date End Must Bigger than date Start
                Solution: Change date start and date end
                """
                    % (record.id)
                )
                raise UserError(error_message)
            if not record._check_diff_date_start_end():
                error_message = _(
                    """
                Context: Change date start or date end on overtime request
                Database ID: %s
                Problem: The Different Betwen Date End dand Date Start < 24
                Solution: Change date start and date end
                """
                    % (record.id)
                )
                raise UserError(error_message)

    def _check_diff_date_start_end(self):
        self.ensure_one()
        result = True
        diff_hour = (self.date_end - self.date_start).total_seconds() / 3600.0
        if diff_hour > 24.0:
            result = False
        return result

    def _check_date_start_end(self):
        self.ensure_one()
        result = True
        if self.date_end < self.date_start:
            result = False
        return result

    @api.onchange(
        "date",
    )
    def onchange_date_start_end(self):
        dt_datetime = datetime.combine(self.date, datetime.min.time())
        if not self.date_start:
            self.date_start = dt_datetime
        if not self.date_end:
            self.date_end = dt_datetime
