# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiHrLeaveAllocation(HttpSavepointCase):
    """Tour tests for the ``hr.leave_allocation`` work instructions.

    Uses ``HttpSavepointCase`` rather than plain ``HttpCase``: in 14.0
    ``TransactionCase`` only assigns ``self.env`` inside instance
    ``setUp()``, so ``cls.env`` is not available in ``setUpClass()``.
    ``HttpSavepointCase`` (via ``SingleTransactionCase``) does set
    ``cls.env`` in ``setUpClass()``, which the tours below rely on to
    seed employees and allocations visible to the browser session.

    No group grant is needed here: ``ssi_hr_holiday``'s own demo data
    (``security/res_group_data.xml``) already adds ``base.user_admin``
    to ``hr_leave_allocation_validator_group`` (which implies ``hr_leave_
    allocation_user_group`` and ``hr_leave_allocation_viewer_group``) and
    to ``leave_allocation_all_group`` (data ownership), and admin is the
    sole member of the single-level ``approval.template`` approver group,
    so it can both act as the requesting user and the approver.

    Unlike ``hr.leave``, ``hr.leave_allocation`` has no covering-timesheet
    constraint, so fixtures only need an employee.
    """

    @classmethod
    def setUpClass(cls):
        """Seed one employee/allocation fixture per tour."""
        super().setUpClass()

        employee_model = cls.env["hr.employee"]
        allocation_model = cls.env["hr.leave_allocation"]
        cls.allocation_model = allocation_model

        cls.leave_type = cls.env["hr.leave_type"].create(
            {
                "name": "TOUR-LTYPE-ALLOC",
                "code": "/",
                "need_allocation": True,
            }
        )

        # --- 01-create.md: no allocation fixture — the tour creates it.
        employee_model.create({"name": "TOUR-EMP-ALLOC-CREATE"})

        # --- 02-edit.md: Draft.
        cls.employee_edit = employee_model.create({"name": "TOUR-EMP-ALLOC-EDIT"})
        cls.allocation_edit = cls._create_allocation(
            cls.employee_edit, "2026-01-01", "2026-01-31"
        )

        # --- 03-delete.md: Draft, document number still "/".
        cls.employee_delete = employee_model.create({"name": "TOUR-EMP-ALLOC-DELETE"})
        cls.allocation_delete = cls._create_allocation(
            cls.employee_delete, "2026-02-01", "2026-02-28"
        )

        # --- 04-confirm.md: Draft, ready to Confirm.
        cls.employee_confirm = employee_model.create({"name": "TOUR-EMP-ALLOC-CONFIRM"})
        cls.allocation_confirm = cls._create_allocation(
            cls.employee_confirm, "2026-03-01", "2026-03-31"
        )

        # --- 05-approve.md: Waiting for Approval; admin (Validator) is
        # the pending approver for the single-level "Standard" approval.
        # template.
        cls.employee_approve = employee_model.create({"name": "TOUR-EMP-ALLOC-APPROVE"})
        cls.allocation_approve = cls._create_allocation(
            cls.employee_approve, "2026-04-01", "2026-04-30"
        )
        cls.allocation_approve.with_context(bypass_policy_check=True).action_confirm()

        # --- 06-reject.md: Waiting for Approval, independent record from
        # the approve fixture above.
        cls.employee_reject = employee_model.create({"name": "TOUR-EMP-ALLOC-REJECT"})
        cls.allocation_reject = cls._create_allocation(
            cls.employee_reject, "2026-05-01", "2026-05-31"
        )
        cls.allocation_reject.with_context(bypass_policy_check=True).action_confirm()

        # --- 10-cancel.md: Draft (cancel_ok also applies to confirm/open/
        # done/reject). A global cancel reason is required by the wizard.
        cls.employee_cancel = employee_model.create({"name": "TOUR-EMP-ALLOC-CANCEL"})
        cls.allocation_cancel = cls._create_allocation(
            cls.employee_cancel, "2026-06-01", "2026-06-30"
        )
        cls.cancel_reason = cls.env["base.cancel_reason"].create(
            {
                "name": "TOUR-ALLOC-CANCEL-REASON",
                "code": "TOUR-AL-CR",
                "global_use": True,
            }
        )

        # --- 11-terminate.md: Done. Reached via Confirm/Approve (which
        # lands In Progress) then forced to Done directly — the open ->
        # done automatic transition (docs/hr_leave_allocation/
        # 09-auto-done.md) has no UI steps of its own and is out of scope
        # for this tour set; only the Pre-Condition state ("Status is
        # Done") matters for 11-terminate.md.
        cls.employee_terminate = employee_model.create(
            {"name": "TOUR-EMP-ALLOC-TERMINATE"}
        )
        cls.allocation_terminate = cls._create_allocation(
            cls.employee_terminate, "2026-07-01", "2026-07-31"
        )
        cls.allocation_terminate.with_context(bypass_policy_check=True).action_confirm()
        cls.allocation_terminate.with_context(
            bypass_policy_check=True
        ).action_approve_approval()
        cls.allocation_terminate.sudo().write({"state": "done"})
        cls.terminate_reason = cls.env["base.terminate_reason"].create(
            {
                "name": "TOUR-ALLOC-TERMINATE-REASON",
                "code": "TOUR-AL-TR",
                "global_use": True,
            }
        )

        # --- 12-restart.md: Cancelled.
        cls.employee_restart = employee_model.create({"name": "TOUR-EMP-ALLOC-RESTART"})
        cls.allocation_restart = cls._create_allocation(
            cls.employee_restart, "2026-08-01", "2026-08-31"
        )
        restart_reason = cls.env["base.cancel_reason"].create(
            {
                "name": "TOUR-ALLOC-RESTART-REASON",
                "code": "TOUR-AL-RR",
                "global_use": True,
            }
        )
        cls.allocation_restart.with_context(bypass_policy_check=True).action_cancel(
            restart_reason
        )

        # --- 13-reset-number.md: Draft, with a document number already
        # assigned (simulating a manually-numbered record) so the Reset
        # Document Number button has a visible effect.
        cls.employee_resetnum = employee_model.create(
            {"name": "TOUR-EMP-ALLOC-RESETNUM"}
        )
        cls.allocation_resetnum = cls._create_allocation(
            cls.employee_resetnum, "2026-09-01", "2026-09-30"
        )
        cls.allocation_resetnum.sudo().write({"name": "TOUR-ALLOC-RESETNUM-999"})

        # --- 14-restart-approval.md: Waiting for Approval, with
        # approval_template_id cleared so the shipped policy.template
        # (which only grants restart_approval_ok while that field is
        # empty) evaluates to allowed — see the note in the IK itself.
        cls.employee_restart_approval = employee_model.create(
            {"name": "TOUR-EMP-ALLOC-RESTARTAPPROVAL"}
        )
        cls.allocation_restart_approval = cls._create_allocation(
            cls.employee_restart_approval, "2026-10-01", "2026-10-31"
        )
        cls.allocation_restart_approval.with_context(
            bypass_policy_check=True
        ).action_confirm()
        cls.allocation_restart_approval.sudo().write({"approval_template_id": False})

    @classmethod
    def _create_allocation(cls, employee, date_start, date_end):
        """Create an ``hr.leave_allocation`` fixture for ``employee``.

        :param employee: ``hr.employee`` record the allocation is for
        :param str date_start: ISO date string
        :param str date_end: ISO date string
        :return: the created ``hr.leave_allocation`` record
        :rtype: recordset
        """
        return cls.allocation_model.create(
            {
                "employee_id": employee.id,
                "type_id": cls.leave_type.id,
                "date_start": date_start,
                "date_end": date_end,
                "date_extended": date_end,
                "number_of_days": 12,
            }
        )

    def test_create(self):
        """Run the create tour for ``hr.leave_allocation``.

        IK: docs/hr_leave_allocation/01-create.md
        """
        self.start_tour(
            "/web", "ssi_hr_holiday_hr_leave_allocation_create", login="admin"
        )

    def test_edit(self):
        """Run the edit tour for ``hr.leave_allocation``.

        IK: docs/hr_leave_allocation/02-edit.md
        """
        self.start_tour(
            "/web", "ssi_hr_holiday_hr_leave_allocation_edit", login="admin"
        )

    def test_delete(self):
        """Run the delete tour for ``hr.leave_allocation``.

        IK: docs/hr_leave_allocation/03-delete.md
        """
        self.start_tour(
            "/web", "ssi_hr_holiday_hr_leave_allocation_delete", login="admin"
        )

    def test_confirm(self):
        """Run the confirm tour for ``hr.leave_allocation``.

        IK: docs/hr_leave_allocation/04-confirm.md
        """
        self.start_tour(
            "/web", "ssi_hr_holiday_hr_leave_allocation_confirm", login="admin"
        )

    def test_approve(self):
        """Run the approve tour for ``hr.leave_allocation``.

        IK: docs/hr_leave_allocation/05-approve.md
        """
        self.start_tour(
            "/web", "ssi_hr_holiday_hr_leave_allocation_approve", login="admin"
        )

    def test_reject(self):
        """Run the reject tour for ``hr.leave_allocation``.

        IK: docs/hr_leave_allocation/06-reject.md
        """
        self.start_tour(
            "/web", "ssi_hr_holiday_hr_leave_allocation_reject", login="admin"
        )

    def test_cancel(self):
        """Run the cancel tour for ``hr.leave_allocation``.

        IK: docs/hr_leave_allocation/10-cancel.md
        """
        self.start_tour(
            "/web", "ssi_hr_holiday_hr_leave_allocation_cancel", login="admin"
        )

    def test_terminate(self):
        """Run the terminate tour for ``hr.leave_allocation``.

        IK: docs/hr_leave_allocation/11-terminate.md
        """
        self.start_tour(
            "/web", "ssi_hr_holiday_hr_leave_allocation_terminate", login="admin"
        )

    def test_restart(self):
        """Run the restart tour for ``hr.leave_allocation``.

        IK: docs/hr_leave_allocation/12-restart.md
        """
        self.start_tour(
            "/web", "ssi_hr_holiday_hr_leave_allocation_restart", login="admin"
        )

    def test_reset_number(self):
        """Run the reset document number tour for ``hr.leave_allocation``.

        IK: docs/hr_leave_allocation/13-reset-number.md
        """
        self.start_tour(
            "/web", "ssi_hr_holiday_hr_leave_allocation_reset_number", login="admin"
        )

    def test_restart_approval(self):
        """Run the restart approval process tour for ``hr.leave_allocation``.

        IK: docs/hr_leave_allocation/14-restart-approval.md
        """
        self.start_tour(
            "/web",
            "ssi_hr_holiday_hr_leave_allocation_restart_approval",
            login="admin",
        )
