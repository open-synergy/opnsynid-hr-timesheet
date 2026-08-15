# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiHrLeaveAllocationRequestBatch(HttpSavepointCase):
    """Tour tests for the ``hr.leave_allocation_request_batch`` work
    instructions.

    Uses ``HttpSavepointCase`` rather than plain ``HttpCase``: in 14.0
    ``TransactionCase`` only assigns ``self.env`` inside instance
    ``setUp()``, so ``cls.env`` is not available in ``setUpClass()``.
    ``HttpSavepointCase`` (via ``SingleTransactionCase``) does set
    ``cls.env`` in ``setUpClass()``, which the tours below rely on to
    seed leave types, employees and batches visible to the browser
    session.

    No group grant is needed here: ``ssi_hr_leave_allocation_request_
    batch``'s own module data (``security/res_group_data.xml``) already
    adds ``base.user_admin`` to ``hr_leave_allocation_request_batch_
    validator_group`` (which implies ``hr_leave_allocation_request_
    batch_user_group`` and ``hr_leave_allocation_request_batch_viewer_
    group``), and admin is the sole member of the single-level
    ``approval.template`` approver group, so it can both act as the
    requesting user and the approver.

    ``employee_ids`` is a required field on this model, so every batch
    fixture below includes at least one employee — unlike sibling batch
    modules where the employee list may be left empty.
    """

    @classmethod
    def setUpClass(cls):
        """Seed one leave type/employee/batch fixture per tour."""
        super().setUpClass()

        employee_model = cls.env["hr.employee"]

        # --- 01-create.md: no batch fixture — the tour creates it. Only
        # the Type and Employee it picks from the dropdown/dialog need to
        # pre-exist.
        cls._create_leave_type("TOUR-BATCH-LTYPE-CREATE")
        employee_model.create({"name": "TOUR-BATCH-EMP-CREATE"})

        # --- 02-edit.md: Draft.
        type_edit = cls._create_leave_type("TOUR-BATCH-LTYPE-EDIT")
        employee_edit = employee_model.create({"name": "TOUR-BATCH-EMP-EDIT"})
        cls.batch_edit = cls._create_batch(
            type_edit, employee_edit, "2026-02-05", "2026-02-10"
        )

        # --- 03-delete.md: Draft, document number still "/".
        type_delete = cls._create_leave_type("TOUR-BATCH-LTYPE-DELETE")
        employee_delete = employee_model.create({"name": "TOUR-BATCH-EMP-DELETE"})
        cls.batch_delete = cls._create_batch(
            type_delete, employee_delete, "2026-03-05", "2026-03-10"
        )

        # --- 04-confirm.md: Draft, ready to Confirm.
        type_confirm = cls._create_leave_type("TOUR-BATCH-LTYPE-CONFIRM")
        cls.employee_confirm = employee_model.create({"name": "TOUR-BATCH-EMP-CONFIRM"})
        cls.batch_confirm = cls._create_batch(
            type_confirm, cls.employee_confirm, "2026-04-05", "2026-04-10"
        )

        # --- 05-approve.md: Waiting for Approval; admin (Validator) is
        # the pending approver for the single-level "Standard" approval
        # template.
        type_approve = cls._create_leave_type("TOUR-BATCH-LTYPE-APPROVE")
        cls.employee_approve = employee_model.create({"name": "TOUR-BATCH-EMP-APPROVE"})
        cls.batch_approve = cls._create_batch(
            type_approve, cls.employee_approve, "2026-05-05", "2026-05-10"
        )
        cls.batch_approve.with_context(bypass_policy_check=True).action_confirm()

        # --- 06-reject.md: Waiting for Approval, independent record from
        # the approve fixture above.
        type_reject = cls._create_leave_type("TOUR-BATCH-LTYPE-REJECT")
        employee_reject = employee_model.create({"name": "TOUR-BATCH-EMP-REJECT"})
        cls.batch_reject = cls._create_batch(
            type_reject, employee_reject, "2026-06-05", "2026-06-10"
        )
        cls.batch_reject.with_context(bypass_policy_check=True).action_confirm()

        # --- 10-cancel.md: Draft (cancel_ok also applies to
        # confirm/done/reject). A global cancel reason is required by the
        # wizard.
        type_cancel = cls._create_leave_type("TOUR-BATCH-LTYPE-CANCEL")
        employee_cancel = employee_model.create({"name": "TOUR-BATCH-EMP-CANCEL"})
        cls.batch_cancel = cls._create_batch(
            type_cancel, employee_cancel, "2026-07-05", "2026-07-10"
        )
        cls.cancel_reason = cls.env["base.cancel_reason"].create(
            {
                "name": "TOUR-BATCH-CANCEL-REASON",
                "code": "TOUR-BATCH-CR",
                "global_use": True,
            }
        )

        # --- 12-restart.md: Cancelled.
        type_restart = cls._create_leave_type("TOUR-BATCH-LTYPE-RESTART")
        employee_restart = employee_model.create({"name": "TOUR-BATCH-EMP-RESTART"})
        cls.batch_restart = cls._create_batch(
            type_restart, employee_restart, "2026-08-05", "2026-08-10"
        )
        restart_reason = cls.env["base.cancel_reason"].create(
            {
                "name": "TOUR-BATCH-RESTART-REASON",
                "code": "TOUR-BATCH-RR",
                "global_use": True,
            }
        )
        cls.batch_restart.with_context(bypass_policy_check=True).action_cancel(
            restart_reason
        )

        # --- 13-reset-number.md: Draft, with a document number already
        # assigned (simulating a manually-numbered record) so the Reset
        # Document Number button has a visible effect.
        type_resetnum = cls._create_leave_type("TOUR-BATCH-LTYPE-RESETNUM")
        employee_resetnum = employee_model.create({"name": "TOUR-BATCH-EMP-RESETNUM"})
        cls.batch_resetnum = cls._create_batch(
            type_resetnum, employee_resetnum, "2026-09-05", "2026-09-10"
        )
        cls.batch_resetnum.sudo().write({"name": "TOUR-BATCH-RESETNUM-999"})

        # --- 14-restart-approval.md: Waiting for Approval, with
        # approval_template_id cleared so the shipped policy.template
        # (which only grants restart_approval_ok while that field is
        # empty) evaluates to allowed — see the note in the IK itself.
        type_reapproval = cls._create_leave_type("TOUR-BATCH-LTYPE-REAPPROVAL")
        employee_reapproval = employee_model.create(
            {"name": "TOUR-BATCH-EMP-REAPPROVAL"}
        )
        cls.batch_reapproval = cls._create_batch(
            type_reapproval, employee_reapproval, "2026-10-05", "2026-10-10"
        )
        cls.batch_reapproval.with_context(bypass_policy_check=True).action_confirm()
        cls.batch_reapproval.sudo().write({"approval_template_id": False})

    @classmethod
    def _create_leave_type(cls, name):
        """Create an ``hr.leave_type`` fixture with allocation enabled.

        Only types with **Need Allocation** checked can be selected as
        this batch model's **Type** (see the view's ``domain`` on
        ``type_id``).

        :param str name: unique name, also used as the tour's
            dropdown-pick and list-row search anchor
        :return: the created ``hr.leave_type`` record
        :rtype: recordset
        """
        return cls.env["hr.leave_type"].create(
            {
                "name": name,
                "code": "/",
                "need_allocation": True,
            }
        )

    @classmethod
    def _create_batch(cls, leave_type, employee, date_start, date_end):
        """Create an ``hr.leave_allocation_request_batch`` fixture.

        ``employee_ids`` and ``date_extended`` are both required fields
        on this model; ``date_extended`` is set equal to ``date_end`` to
        mirror what the ``onchange_date_extended`` onchange would fill
        in when **Can be Extended** is left unchecked.

        :param leave_type: ``hr.leave_type`` record for the batch
        :param employee: ``hr.employee`` record to include in
            **Employee(s)**
        :param str date_start: ISO date string
        :param str date_end: ISO date string, on or after ``date_start``
        :return: the created ``hr.leave_allocation_request_batch`` record
        :rtype: recordset
        """
        return cls.env["hr.leave_allocation_request_batch"].create(
            {
                "type_id": leave_type.id,
                "number_of_days": 5,
                "employee_ids": [(6, 0, employee.ids)],
                "date_start": date_start,
                "date_end": date_end,
                "date_extended": date_end,
            }
        )

    def test_create(self):
        """Run the create tour for ``hr.leave_allocation_request_batch``.

        IK: docs/hr_leave_allocation_request_batch/01-create.md
        """
        self.start_tour(
            "/web",
            "ssi_hr_leave_allocation_request_batch_"
            "hr_leave_allocation_request_batch_create",
            login="admin",
        )

    def test_edit(self):
        """Run the edit tour for ``hr.leave_allocation_request_batch``.

        IK: docs/hr_leave_allocation_request_batch/02-edit.md
        """
        self.start_tour(
            "/web",
            "ssi_hr_leave_allocation_request_batch_"
            "hr_leave_allocation_request_batch_edit",
            login="admin",
        )

    def test_delete(self):
        """Run the delete tour for ``hr.leave_allocation_request_batch``.

        IK: docs/hr_leave_allocation_request_batch/03-delete.md
        """
        self.start_tour(
            "/web",
            "ssi_hr_leave_allocation_request_batch_"
            "hr_leave_allocation_request_batch_delete",
            login="admin",
        )

    def test_confirm(self):
        """Run the confirm tour for ``hr.leave_allocation_request_batch``.

        IK: docs/hr_leave_allocation_request_batch/04-confirm.md
        """
        self.start_tour(
            "/web",
            "ssi_hr_leave_allocation_request_batch_"
            "hr_leave_allocation_request_batch_confirm",
            login="admin",
        )

    def test_approve(self):
        """Run the approve tour for ``hr.leave_allocation_request_batch``.

        IK: docs/hr_leave_allocation_request_batch/05-approve.md
        """
        self.start_tour(
            "/web",
            "ssi_hr_leave_allocation_request_batch_"
            "hr_leave_allocation_request_batch_approve",
            login="admin",
        )

    def test_reject(self):
        """Run the reject tour for ``hr.leave_allocation_request_batch``.

        IK: docs/hr_leave_allocation_request_batch/06-reject.md
        """
        self.start_tour(
            "/web",
            "ssi_hr_leave_allocation_request_batch_"
            "hr_leave_allocation_request_batch_reject",
            login="admin",
        )

    def test_cancel(self):
        """Run the cancel tour for ``hr.leave_allocation_request_batch``.

        IK: docs/hr_leave_allocation_request_batch/10-cancel.md
        """
        self.start_tour(
            "/web",
            "ssi_hr_leave_allocation_request_batch_"
            "hr_leave_allocation_request_batch_cancel",
            login="admin",
        )

    def test_restart(self):
        """Run the restart tour for ``hr.leave_allocation_request_batch``.

        IK: docs/hr_leave_allocation_request_batch/12-restart.md
        """
        self.start_tour(
            "/web",
            "ssi_hr_leave_allocation_request_batch_"
            "hr_leave_allocation_request_batch_restart",
            login="admin",
        )

    def test_reset_number(self):
        """Run the reset document number tour.

        IK: docs/hr_leave_allocation_request_batch/13-reset-number.md
        """
        self.start_tour(
            "/web",
            "ssi_hr_leave_allocation_request_batch_"
            "hr_leave_allocation_request_batch_reset_number",
            login="admin",
        )

    def test_restart_approval(self):
        """Run the restart approval process tour.

        IK: docs/hr_leave_allocation_request_batch/14-restart-approval.md
        """
        self.start_tour(
            "/web",
            "ssi_hr_leave_allocation_request_batch_"
            "hr_leave_allocation_request_batch_restart_approval",
            login="admin",
        )
