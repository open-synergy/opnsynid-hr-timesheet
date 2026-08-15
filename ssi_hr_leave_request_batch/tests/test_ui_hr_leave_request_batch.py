# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiHrLeaveRequestBatch(HttpSavepointCase):
    """Tour tests for the ``hr.leave_request_batch`` work instructions.

    Uses ``HttpSavepointCase`` rather than plain ``HttpCase``: in 14.0
    ``TransactionCase`` only assigns ``self.env`` inside instance
    ``setUp()``, so ``cls.env`` is not available in ``setUpClass()``.
    ``HttpSavepointCase`` (via ``SingleTransactionCase``) does set
    ``cls.env`` in ``setUpClass()``, which the tours below rely on to
    seed leave types, employees, and batches visible to the browser
    session.

    ``base.user_admin`` is already a member of
    ``hr_leave_request_batch_validator_group`` (this module's own demo
    data, ``security/res_group_data.xml``), which implies
    ``hr_leave_request_batch_user_group``/``..._viewer_group`` and is
    the sole member of the single-level "Standard" ``approval.template``
    approver group, so it can both act as the requesting user and the
    approver. Unlike ``hr_leave_request_batch_validator_group``, none of
    the data-ownership groups (Company / Company and All Child
    Companies / All) are pre-granted to admin, so every fixture below
    sets ``user_id`` explicitly to ``base.user_admin`` — otherwise
    ``hr_leave_request_batch_internal_user_rule``
    (``[('user_id', '=', user.id)]``) would hide records created by
    ``cls.env`` (which runs as SUPERUSER) from the "admin" browser
    session (odoo-development-ui-test skill, "Base class 14.0" note).

    Every fixture from ``04-confirm`` onward leaves **Employee(s)**
    empty: confirming with employees populated creates one
    ``hr.leave`` document per employee, which in turn needs a covering
    ``hr.timesheet`` (and, if the leave type needs allocation, an
    ``hr.leave_allocation``) — see
    ``docs/hr_leave_request_batch/04-confirm.md`` Pre-Condition and its
    "If Employee(s) is empty" Post-Condition branch. That
    hr.leave-creation branch, and the prerequisites it drags in, are out
    of scope for this tour set (covered by ``ssi_hr_holiday``'s own
    ``hr.leave`` tour set).
    """

    @classmethod
    def setUpClass(cls):
        """Seed one leave type/employee/batch fixture per tour."""
        super().setUpClass()

        cls.admin_user = cls.env.ref("base.user_admin")

        # --- 01-create.md: no batch fixture — the tour creates it. Only
        # the Type and Employee it picks from the dropdown/dialog need
        # to pre-exist.
        cls._create_leave_type("TOUR-LRBATCH-TYPE-CREATE")
        cls.employee_create = cls.env["hr.employee"].create(
            {"name": "TOUR-LRBATCH-EMP-CREATE"}
        )

        # --- 02-edit.md: Draft.
        type_edit = cls._create_leave_type("TOUR-LRBATCH-TYPE-EDIT")
        cls.batch_edit = cls._create_batch(type_edit, "2026-02-05", "2026-02-05")

        # --- 03-delete.md: Draft, document number still "/".
        type_delete = cls._create_leave_type("TOUR-LRBATCH-TYPE-DELETE")
        cls.batch_delete = cls._create_batch(type_delete, "2026-03-05", "2026-03-05")

        # --- 04-confirm.md: Draft, ready to Confirm.
        type_confirm = cls._create_leave_type("TOUR-LRBATCH-TYPE-CONFIRM")
        cls.batch_confirm = cls._create_batch(type_confirm, "2026-04-05", "2026-04-05")

        # --- 05-approve.md: Waiting for Approval; admin (Validator) is
        # the pending approver for the single-level "Standard" approval
        # template.
        type_approve = cls._create_leave_type("TOUR-LRBATCH-TYPE-APPROVE")
        cls.batch_approve = cls._create_batch(type_approve, "2026-05-05", "2026-05-05")
        cls.batch_approve.with_context(bypass_policy_check=True).action_confirm()

        # --- 06-reject.md: Waiting for Approval, independent record
        # from the approve fixture above.
        type_reject = cls._create_leave_type("TOUR-LRBATCH-TYPE-REJECT")
        cls.batch_reject = cls._create_batch(type_reject, "2026-06-05", "2026-06-05")
        cls.batch_reject.with_context(bypass_policy_check=True).action_confirm()

        # --- 10-cancel.md: Draft (cancel_ok also applies to
        # confirm/done/reject). A global cancel reason is required by
        # the wizard.
        type_cancel = cls._create_leave_type("TOUR-LRBATCH-TYPE-CANCEL")
        cls.batch_cancel = cls._create_batch(type_cancel, "2026-07-05", "2026-07-05")
        cls.cancel_reason = cls.env["base.cancel_reason"].create(
            {
                "name": "TOUR-LRBATCH-CANCEL-REASON",
                "code": "TOUR-LRB-CR",
                "global_use": True,
            }
        )

        # --- 12-restart.md: Cancelled.
        type_restart = cls._create_leave_type("TOUR-LRBATCH-TYPE-RESTART")
        cls.batch_restart = cls._create_batch(type_restart, "2026-08-05", "2026-08-05")
        restart_reason = cls.env["base.cancel_reason"].create(
            {
                "name": "TOUR-LRBATCH-RESTART-REASON",
                "code": "TOUR-LRB-RR",
                "global_use": True,
            }
        )
        cls.batch_restart.with_context(bypass_policy_check=True).action_cancel(
            restart_reason
        )

        # --- 13-reset-number.md: Draft, with a document number already
        # assigned (simulating a manually-numbered record) so the Reset
        # Document Number button has a visible effect.
        type_resetnum = cls._create_leave_type("TOUR-LRBATCH-TYPE-RESETNUM")
        cls.batch_resetnum = cls._create_batch(
            type_resetnum, "2026-09-05", "2026-09-05"
        )
        cls.batch_resetnum.sudo().write({"name": "TOUR-LRBATCH-RESETNUM-999"})

        # --- 14-restart-approval.md: Waiting for Approval, with
        # approval_template_id cleared so the shipped policy.template
        # (which only grants restart_approval_ok while that field is
        # empty) evaluates to allowed — see the note in the IK itself.
        type_reapproval = cls._create_leave_type("TOUR-LRBATCH-TYPE-REAPPROVAL")
        cls.batch_reapproval = cls._create_batch(
            type_reapproval, "2026-10-05", "2026-10-05"
        )
        cls.batch_reapproval.with_context(bypass_policy_check=True).action_confirm()
        cls.batch_reapproval.sudo().write({"approval_template_id": False})

    @classmethod
    def _create_leave_type(cls, name):
        """Create an ``hr.leave_type`` fixture used by one tour.

        :param str name: unique name, also used as the tour's
            dropdown-pick and list-row search anchor
        :return: the created ``hr.leave_type`` record
        :rtype: recordset
        """
        return cls.env["hr.leave_type"].create(
            {
                "name": name,
                "code": "/",
                "need_allocation": False,
            }
        )

    @classmethod
    def _create_batch(cls, leave_type, date_start, date_end, employee=False):
        """Create an ``hr.leave_request_batch`` fixture.

        :param leave_type: ``hr.leave_type`` record for the batch
        :param str date_start: ISO date string
        :param str date_end: ISO date string, not before ``date_start``
        :param employee: optional ``hr.employee`` record to include in
            **Employee(s)**
        :return: the created ``hr.leave_request_batch`` record
        :rtype: recordset
        """
        values = {
            "type_id": leave_type.id,
            "date_start": date_start,
            "date_end": date_end,
            "user_id": cls.admin_user.id,
        }
        if employee:
            values["employee_ids"] = [(6, 0, employee.ids)]
        return cls.env["hr.leave_request_batch"].create(values)

    def test_create(self):
        """Run the create tour for ``hr.leave_request_batch``.

        IK: docs/hr_leave_request_batch/01-create.md
        """
        self.start_tour(
            "/web",
            "ssi_hr_leave_request_batch_hr_leave_request_batch_create",
            login="admin",
        )

    def test_edit(self):
        """Run the edit tour for ``hr.leave_request_batch``.

        IK: docs/hr_leave_request_batch/02-edit.md
        """
        self.start_tour(
            "/web",
            "ssi_hr_leave_request_batch_hr_leave_request_batch_edit",
            login="admin",
        )

    def test_delete(self):
        """Run the delete tour for ``hr.leave_request_batch``.

        IK: docs/hr_leave_request_batch/03-delete.md
        """
        self.start_tour(
            "/web",
            "ssi_hr_leave_request_batch_hr_leave_request_batch_delete",
            login="admin",
        )

    def test_confirm(self):
        """Run the confirm tour for ``hr.leave_request_batch``.

        IK: docs/hr_leave_request_batch/04-confirm.md
        """
        self.start_tour(
            "/web",
            "ssi_hr_leave_request_batch_hr_leave_request_batch_confirm",
            login="admin",
        )

    def test_approve(self):
        """Run the approve tour for ``hr.leave_request_batch``.

        IK: docs/hr_leave_request_batch/05-approve.md
        """
        self.start_tour(
            "/web",
            "ssi_hr_leave_request_batch_hr_leave_request_batch_approve",
            login="admin",
        )

    def test_reject(self):
        """Run the reject tour for ``hr.leave_request_batch``.

        IK: docs/hr_leave_request_batch/06-reject.md
        """
        self.start_tour(
            "/web",
            "ssi_hr_leave_request_batch_hr_leave_request_batch_reject",
            login="admin",
        )

    def test_cancel(self):
        """Run the cancel tour for ``hr.leave_request_batch``.

        IK: docs/hr_leave_request_batch/10-cancel.md
        """
        self.start_tour(
            "/web",
            "ssi_hr_leave_request_batch_hr_leave_request_batch_cancel",
            login="admin",
        )

    def test_restart(self):
        """Run the restart tour for ``hr.leave_request_batch``.

        IK: docs/hr_leave_request_batch/12-restart.md
        """
        self.start_tour(
            "/web",
            "ssi_hr_leave_request_batch_hr_leave_request_batch_restart",
            login="admin",
        )

    def test_reset_number(self):
        """Run the reset document number tour for ``hr.leave_request_batch``.

        IK: docs/hr_leave_request_batch/13-reset-number.md
        """
        self.start_tour(
            "/web",
            "ssi_hr_leave_request_batch_hr_leave_request_batch_reset_number",
            login="admin",
        )

    def test_restart_approval(self):
        """Run the restart approval process tour for the batch model.

        IK: docs/hr_leave_request_batch/14-restart-approval.md
        """
        self.start_tour(
            "/web",
            "ssi_hr_leave_request_batch_hr_leave_request_batch_restart_approval",
            login="admin",
        )
