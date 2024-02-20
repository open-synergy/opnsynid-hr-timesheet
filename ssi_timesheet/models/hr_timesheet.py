# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import Warning as UserError
from datetime import datetime, timedelta


class HRTimesheet(models.Model):
    _name = "hr.timesheet"
    _inherit = [
        "mixin.transaction_open",
        "mixin.transaction_confirm",
        "mixin.transaction_done",
        "mixin.transaction_cancel",
        "mixin.date_duration",
        "mixin.employee_document",
    ]
    _description = "Timesheet"
    _approval_from_state = "confirm"
    _approval_to_state = "done"
    _approval_state = "confirm"
    _after_approved_method = "action_done"
    _create_sequence_state = "open"

    # Attributes related to add element on view automatically
    _automatically_insert_view_element = True

    # Attributes related to add element on form view automatically
    _automatically_insert_multiple_approval_page = True
    _automatically_insert_done_policy_fields = False
    _automatically_insert_done_button = False

    _statusbar_visible_label = "draft,open,confirm,done"

    _policy_field_order = [
        "open_ok",
        "confirm_ok",
        "approve_ok",
        "reject_ok",
        "restart_approval_ok",
        "cancel_ok",
        "restart_ok",
        "manual_number_ok",
    ]

    _header_button_order = [
        "action_open",
        "action_confirm",
        "action_approve_approval",
        "action_reject_approval",
        "%(ssi_transaction_cancel_mixin.base_select_cancel_reason_action)d",
        "action_restart",
    ]

    # Attributes related to add element on search view automatically
    _state_filter_order = [
        "dom_draft",
        "dom_open",
        "dom_confirm",
        "dom_reject",
        "dom_done",
        "dom_cancel",
    ]

    # Mixin duration attribute
    _date_start_readonly = True
    _date_end_readonly = True
    _date_start_states_list = ["draft"]
    _date_start_states_readonly = ["draft"]
    _date_end_states_list = ["draft"]
    _date_end_states_readonly = ["draft"]

    computation_ids = fields.One2many(
        string="Computations",
        comodel_name="hr.timesheet_computation",
        inverse_name="sheet_id",
        readonly=True,
    )
    state = fields.Selection(
        string="State",
        selection=[
            ("draft", "Draft"),
            ("open", "In Progress"),
            ("confirm", "Waiting for Approval"),
            ("done", "Done"),
            ("cancel", "Cancelled"),
            ("reject", "Rejected"),
        ],
        default="draft",
        copy=False,
    )
    daily_summary_ids = fields.One2many(
        comodel_name='hr.timesheet_daily_summary',
        inverse_name='sheet_id',
        string='Daily Summary',
        readonly=True)

    @api.depends("policy_template_id")
    def _compute_policy(self):
        _super = super(HRTimesheet, self)
        _super._compute_policy()

    @api.model
    def _get_policy_field(self):
        res = super(HRTimesheet, self)._get_policy_field()
        policy_field = [
            "open_ok",
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

    def _prepare_daily_summary_values(self):
        self.ensure_one()
        daily_summary_values = []
        if self.state in ('open', 'confirm', 'done'):
            delta = self.date_end - self.date_start
            date_ranges = []
            for i in range(delta.days + 1):
                day = self.date_start + timedelta(days=i)
                date_ranges.append(day)
            for current_date in date_ranges:
                vals = self.env['hr.timesheet_daily_summary']._prepare_daily_summary_vals(
                    sheet_id=self,
                    date=current_date
                )
                daily_summary_values.append(vals)
        return daily_summary_values

    def generate_daily_summary(self):
        for rec in self.filtered(lambda r: r.state in ['open', 'confirm', 'done']):
            daily_summary_values = rec._prepare_daily_summary_values()
            existing_dates = []
            obj_daily_summary = self.env['hr.timesheet_daily_summary']
            for daily_summary_val in daily_summary_values:
                summary_id = obj_daily_summary.search([
                    ('sheet_id', '=', rec.id),
                    ('date', '=', daily_summary_val['date']),
                ], limit=1)
                if not summary_id:
                    obj_daily_summary.create(daily_summary_val)
                else:
                    to_write = {}
                    for key, val in daily_summary_val.items():
                        if summary_id[key] != val:
                            to_write[key] = val
                    if to_write:
                        summary_id.write(to_write)
                existing_dates.append(daily_summary_val['date'])
            to_delete_summary_ids = obj_daily_summary.search([
                ('sheet_id', '=', rec.id),
                ('date', 'not in', existing_dates),
            ])
            to_delete_summary_ids.unlink()

    def get_trigger_fields_daily_summary(self):
        return [
            'state',
            'date_start',
            'date_end',
        ]

    def write(self, values):
        res = super(HRTimesheet, self).write(values)
        for rec in self:
            if any(field in values for field in self.get_trigger_fields_daily_summary()):
                rec.generate_daily_summary()
        return res

    @api.onchange(
        "employee_id",
    )
    def onchange_policy_template_id(self):
        template_id = self._get_template_policy()
        self.policy_template_id = template_id

    def action_compute_computation(self):
        for record in self.sudo():
            record._compute_computation()

    def action_reload_timesheet_computation(self):
        for record in self.sudo():
            record._reload_timesheet_computation()
            record._compute_computation()

    def action_open(self):
        _super = super(HRTimesheet, self)
        _super.action_open()
        for record in self.sudo():
            record._reload_timesheet_computation()
            record._compute_computation()

    def action_confirm(self):
        _super = super(HRTimesheet, self)
        _super.action_confirm()
        for record in self.sudo():
            record._compute_computation()

    def _get_computation_localdict(self):
        self.ensure_one()
        return {
            "document": self,
            "env": self.env,
        }

    def _compute_computation(self):
        self.ensure_one()
        localdict = self._get_computation_localdict()
        for computation in self.computation_ids:
            result = computation._evaluate_computation(localdict)
            localdict[computation.code] = result

    def _reload_timesheet_computation(self):
        self.ensure_one()
        self.computation_ids.unlink()
        result = []
        for computation in self.employee_id.timesheet_computation_ids:
            result.append((0, 0, {"item_id": computation.id}))
        self.write({"computation_ids": result})

    @api.constrains(
        "employee_id",
        "date_start",
    )
    def _check_overlap_date_start(self):
        for record in self.sudo():
            if record.employee_id and record.date_start:
                criteria = [
                    ("employee_id", "=", record.employee_id.id),
                    ("id", "<>", record.id),
                    ("date_start", "<=", record.date_start),
                    ("date_end", ">=", record.date_start),
                ]
                check = record.search(criteria)
                if len(check) > 0:
                    strWarning = _("Date start with the same employee can't overlap")
                    raise UserError(strWarning)

    @api.constrains(
        "employee_id",
        "date_end",
    )
    def _check_overlap_date_end(self):
        for record in self.sudo():
            if record.employee_id and record.date_end:
                criteria = [
                    ("employee_id", "=", record.employee_id.id),
                    ("id", "<>", record.id),
                    ("date_start", "<=", record.date_end),
                    ("date_end", ">=", record.date_end),
                ]
                check = record.search(criteria)
                if len(check) > 0:
                    strWarning = _("Date end with the same employee can't overlap")
                    raise UserError(strWarning)
