# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiHrWorkLog(HttpSavepointCase):
    """Tour tests for the ``hr.work_log`` work instructions.

    Uses ``HttpSavepointCase`` rather than plain ``HttpCase``: in 14.0
    ``TransactionCase`` only assigns ``self.env`` inside instance
    ``setUp()``, so ``cls.env`` is not available in ``setUpClass()``.
    ``HttpSavepointCase`` (via ``SingleTransactionCase``) does set
    ``cls.env`` in ``setUpClass()``, which the tours below rely on to
    seed a fixture timesheet and its work log lines visible to the
    browser session.

    Every ``hr_work_log`` IK is written starting from a single
    timesheet's Work Log tab (docs/hr_work_log/01-create.md note), so
    every tour below shares one On Progress ``hr.timesheet`` fixture
    (employee *TOUR-EMP-WORKLOG*) and distinguishes its own work log
    line by a unique **Description**.
    """

    @classmethod
    def setUpClass(cls):
        """Grant access and seed one work log fixture per tour.

        Pre-Condition common to every ``hr_work_log`` IK: the actor is
        in group *Work log — User* (state-specific actions require
        *Work log — Validator*). ``admin`` already belongs to both
        (and to *All*, the broadest data-ownership group) via
        ``security/res_group_data.xml``, so no extra group grant is
        needed here.

        The fixture timesheet's **Employee** is also assigned to
        ``admin`` as their own employee: ``01-create.md``'s Flow does
        not list *Employee* among the fields the user fills in when
        adding a work log line, so it must resolve through a default —
        this satisfies both that default and the
        ``hr_work_log_internal_user_rule`` record rule.

        The link is written from the ``hr.employee`` side
        (``user_id``), not via ``res.users.employee_id`` — the latter
        (``hr/models/res_users.py``) is ``compute='_compute_company_
        employee', store=False`` with **no inverse**, so writing it
        directly is silently a no-op; confirmed via CI (PR #245, run
        31925098655): the create tour's new work log line kept
        defaulting to admin's original demo employee ("Timesheet for
        Mitchell Admin ... not found"). ``hr.employee`` also carries a
        ``unique (user_id, company_id)`` SQL constraint, so admin's
        pre-existing demo employee is unlinked first.
        """
        super().setUpClass()
        employee_model = cls.env["hr.employee"]
        timesheet_model = cls.env["hr.timesheet"]
        work_log_model = cls.env["hr.work_log"]

        admin_user = cls.env.ref("base.user_admin")
        if admin_user.employee_id:
            admin_user.employee_id.sudo().write({"user_id": False})
        cls.employee = employee_model.create({"name": "TOUR-EMP-WORKLOG"})
        cls.employee.sudo().write({"user_id": admin_user.id})

        working_schedule = cls.env["resource.calendar"].search(
            [], limit=1, order="id asc"
        )
        timesheet_values = {
            "employee_id": cls.employee.id,
            "date_start": "2026-01-01",
            "date_end": "2026-01-31",
        }
        if "working_schedule_id" in timesheet_model._fields:
            timesheet_values["working_schedule_id"] = working_schedule.id
        cls.timesheet = timesheet_model.create(timesheet_values)
        cls.timesheet.with_context(bypass_policy_check=True).action_open()

        # Document Type (ir.model for hr.timesheet) must allow at least
        # one Analytic Account — Pre-Condition of 01-create.md ("the
        # allowed Analytic Account list is configured on the Document
        # Type... out of scope for this Work Instruction", but still
        # needed here so the tour has a selectable option).
        cls.analytic_account = cls.env["account.analytic.account"].create(
            {"name": "TOUR-WORKLOG-AA"}
        )
        cls.ir_model_timesheet = cls.env["ir.model"].search(
            [("model", "=", "hr.timesheet")]
        )
        cls.ir_model_timesheet.sudo().write(
            {
                "work_log_aa_selection_method": "fixed",
                "work_log_aa_ids": [(6, 0, [cls.analytic_account.id])],
            }
        )

        cls.cancel_reason = cls.env["base.cancel_reason"].create(
            {
                "name": "TOUR-WORKLOG-CANCEL-REASON",
                "code": "TOUR-WL-CR",
                "global_use": True,
            }
        )

        def create_work_log(description):
            """Create a Draft ``hr.work_log`` line on the fixture sheet.

            :param str description: unique label used by the tour to
                locate this line in the Work Log tab
            :return: the created work log record
            :rtype: recordset of ``hr.work_log``
            """
            return work_log_model.create(
                {
                    "model_id": cls.ir_model_timesheet.id,
                    "work_object_id": cls.timesheet.id,
                    "employee_id": cls.employee.id,
                    "description": description,
                    "date": "2026-01-15",
                    "analytic_account_id": cls.analytic_account.id,
                    "amount": 4.0,
                }
            )

        # --- 02-edit.md: Draft.
        cls.work_log_edit = create_work_log("TOUR-WL-EDIT")

        # --- 03-delete.md: Draft.
        cls.work_log_delete = create_work_log("TOUR-WL-DELETE")

        # --- 04-confirm.md: Draft.
        cls.work_log_confirm = create_work_log("TOUR-WL-CONFIRM")

        # --- 05-approve.md: Waiting for Approval (state=confirm); admin
        # (Validator) is the pending approver for the single-level
        # "Standard" approval.template.
        cls.work_log_approve = create_work_log("TOUR-WL-APPROVE")
        cls.work_log_approve.with_context(bypass_policy_check=True).action_confirm()

        # --- 06-reject.md: Waiting for Approval, independent record
        # from the approve fixture above.
        cls.work_log_reject = create_work_log("TOUR-WL-REJECT")
        cls.work_log_reject.with_context(bypass_policy_check=True).action_confirm()

        # --- 10-cancel.md: Draft (cancel_ok also applies to draft,
        # confirm and done).
        cls.work_log_cancel = create_work_log("TOUR-WL-CANCEL")

        # --- 12-restart.md: Cancelled (state=cancel).
        cls.work_log_restart = create_work_log("TOUR-WL-RESTART")
        cls.work_log_restart.with_context(bypass_policy_check=True).action_cancel(
            cls.cancel_reason
        )

        # --- 13-reset-number.md: Draft, with a document number already
        # assigned (simulating a manually-numbered record) so the Reset
        # Document Number button has a visible effect.
        cls.work_log_resetnum = create_work_log("TOUR-WL-RESETNUM")
        cls.work_log_resetnum.sudo().write({"name": "TOUR-WL-RESETNUM-999"})

        # --- 14-restart-approval.md: Waiting for Approval, with
        # approval_template_id cleared so the shipped policy.template
        # (which only grants restart_approval_ok while that field is
        # empty) evaluates to allowed — see the note in the IK itself.
        cls.work_log_restart_approval = create_work_log("TOUR-WL-RESTARTAPPROVAL")
        cls.work_log_restart_approval.with_context(
            bypass_policy_check=True
        ).action_confirm()
        cls.work_log_restart_approval.sudo().write({"approval_template_id": False})

    def test_create(self):
        """Run the create tour for ``hr.work_log``.

        IK: docs/hr_work_log/01-create.md
        """
        self.start_tour("/web", "ssi_work_log_mixin_hr_work_log_create", login="admin")

    def test_edit(self):
        """Run the edit tour for ``hr.work_log``.

        IK: docs/hr_work_log/02-edit.md
        """
        self.start_tour("/web", "ssi_work_log_mixin_hr_work_log_edit", login="admin")

    def test_delete(self):
        """Run the delete tour for ``hr.work_log``.

        IK: docs/hr_work_log/03-delete.md
        """
        self.start_tour("/web", "ssi_work_log_mixin_hr_work_log_delete", login="admin")

    def test_confirm(self):
        """Run the confirm tour for ``hr.work_log``.

        IK: docs/hr_work_log/04-confirm.md
        """
        self.start_tour("/web", "ssi_work_log_mixin_hr_work_log_confirm", login="admin")

    def test_approve(self):
        """Run the approve tour for ``hr.work_log``.

        IK: docs/hr_work_log/05-approve.md
        """
        self.start_tour("/web", "ssi_work_log_mixin_hr_work_log_approve", login="admin")

    def test_reject(self):
        """Run the reject tour for ``hr.work_log``.

        IK: docs/hr_work_log/06-reject.md
        """
        self.start_tour("/web", "ssi_work_log_mixin_hr_work_log_reject", login="admin")

    def test_cancel(self):
        """Run the cancel tour for ``hr.work_log``.

        IK: docs/hr_work_log/10-cancel.md
        """
        self.start_tour("/web", "ssi_work_log_mixin_hr_work_log_cancel", login="admin")

    def test_restart(self):
        """Run the restart tour for ``hr.work_log``.

        IK: docs/hr_work_log/12-restart.md
        """
        self.start_tour("/web", "ssi_work_log_mixin_hr_work_log_restart", login="admin")

    def test_reset_number(self):
        """Run the reset document number tour for ``hr.work_log``.

        IK: docs/hr_work_log/13-reset-number.md
        """
        self.start_tour(
            "/web", "ssi_work_log_mixin_hr_work_log_reset_number", login="admin"
        )

    def test_restart_approval(self):
        """Run the restart approval process tour for ``hr.work_log``.

        IK: docs/hr_work_log/14-restart-approval.md
        """
        self.start_tour(
            "/web",
            "ssi_work_log_mixin_hr_work_log_restart_approval",
            login="admin",
        )
