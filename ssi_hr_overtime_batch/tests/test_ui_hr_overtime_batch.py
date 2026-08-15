# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiHrOvertimeBatch(HttpSavepointCase):
    """Tour tests for the ``hr.overtime_batch`` work instructions.

    Uses ``HttpSavepointCase`` rather than plain ``HttpCase``: in 14.0
    ``TransactionCase`` only assigns ``self.env`` inside instance
    ``setUp()``, so ``cls.env`` is not available in ``setUpClass()``.
    ``HttpSavepointCase`` (via ``SingleTransactionCase``) does set
    ``cls.env`` in ``setUpClass()``, which the tours below rely on to
    seed overtime types, employees, timesheets and batches visible to
    the browser session.

    No group grant is needed here: ``ssi_hr_overtime_batch``'s own demo
    data (``security/res_group_data.xml``) already adds
    ``base.user_admin`` to ``hr_overtime_batch_validator_group`` (which
    implies ``hr_overtime_batch_user_group`` and
    ``hr_overtime_batch_viewer_group``) and to
    ``hr_overtime_batch_all_group`` (data ownership), and admin is the
    sole member of the single-level ``approval.template`` approver
    group, so it can both act as the requesting user and the approver.

    Every fixture that reaches state ``confirm`` needs a covering
    ``hr.timesheet`` record for its employee: confirming a batch creates
    one ``hr.overtime`` document per employee (see
    ``docs/hr_overtime_batch/04-confirm.md``), and ``hr.overtime``'s own
    ``sheet_id`` is a required, constrained field computed from the
    employee's timesheets whose date range covers the overtime's date —
    see ``ssi_hr_overtime/docs/hr_overtime/01-create.md`` Pre-Condition.
    Every overtime type used also keeps ``apply_limit_per_day``
    unchecked, so that Pre-Condition never applies.
    """

    @classmethod
    def setUpClass(cls):
        """Seed one overtime type/employee/timesheet/batch per tour."""
        super().setUpClass()

        employee_model = cls.env["hr.employee"]
        timesheet_model = cls.env["hr.timesheet"]
        cls.timesheet_model = timesheet_model

        cls.working_schedule = cls.env["resource.calendar"].search(
            [], limit=1, order="id asc"
        )

        # --- 01-create.md: no batch fixture — the tour creates it. Only
        # the Overtime Type and Employee it picks from the dropdowns need
        # to pre-exist.
        cls._create_overtime_type("TOUR-BATCH-OTTYPE-CREATE")
        cls.employee_create = employee_model.create({"name": "TOUR-BATCH-EMP-CREATE"})
        timesheet_model.create(
            cls._timesheet_values(cls.employee_create, "2026-01-01", "2026-01-31")
        )

        # --- 02-edit.md: Draft, no employee needed.
        type_edit = cls._create_overtime_type("TOUR-BATCH-OTTYPE-EDIT")
        cls.batch_edit = cls._create_batch(
            type_edit, "2026-02-05 08:00:00", "2026-02-05 17:00:00"
        )

        # --- 03-delete.md: Draft, document number still "/".
        type_delete = cls._create_overtime_type("TOUR-BATCH-OTTYPE-DELETE")
        cls.batch_delete = cls._create_batch(
            type_delete, "2026-03-05 08:00:00", "2026-03-05 17:00:00"
        )

        # --- 04-confirm.md: Draft, ready to Confirm.
        type_confirm = cls._create_overtime_type("TOUR-BATCH-OTTYPE-CONFIRM")
        cls.employee_confirm = employee_model.create({"name": "TOUR-BATCH-EMP-CONFIRM"})
        timesheet_model.create(
            cls._timesheet_values(cls.employee_confirm, "2026-04-01", "2026-04-30")
        )
        cls.batch_confirm = cls._create_batch(
            type_confirm,
            "2026-04-05 08:00:00",
            "2026-04-05 17:00:00",
            cls.employee_confirm,
        )

        # --- 05-approve.md: Waiting for Approval; admin (Validator) is
        # the pending approver for the single-level "Standard" approval
        # template.
        type_approve = cls._create_overtime_type("TOUR-BATCH-OTTYPE-APPROVE")
        cls.employee_approve = employee_model.create({"name": "TOUR-BATCH-EMP-APPROVE"})
        timesheet_model.create(
            cls._timesheet_values(cls.employee_approve, "2026-05-01", "2026-05-31")
        )
        cls.batch_approve = cls._create_batch(
            type_approve,
            "2026-05-05 08:00:00",
            "2026-05-05 17:00:00",
            cls.employee_approve,
        )
        cls.batch_approve.with_context(bypass_policy_check=True).action_confirm()

        # --- 06-reject.md: Waiting for Approval, independent record from
        # the approve fixture above.
        type_reject = cls._create_overtime_type("TOUR-BATCH-OTTYPE-REJECT")
        cls.employee_reject = employee_model.create({"name": "TOUR-BATCH-EMP-REJECT"})
        timesheet_model.create(
            cls._timesheet_values(cls.employee_reject, "2026-06-01", "2026-06-30")
        )
        cls.batch_reject = cls._create_batch(
            type_reject,
            "2026-06-05 08:00:00",
            "2026-06-05 17:00:00",
            cls.employee_reject,
        )
        cls.batch_reject.with_context(bypass_policy_check=True).action_confirm()

        # --- 10-cancel.md: Draft (cancel_ok also applies to
        # confirm/done). A global cancel reason is required by the
        # wizard.
        type_cancel = cls._create_overtime_type("TOUR-BATCH-OTTYPE-CANCEL")
        cls.batch_cancel = cls._create_batch(
            type_cancel, "2026-07-05 08:00:00", "2026-07-05 17:00:00"
        )
        cls.cancel_reason = cls.env["base.cancel_reason"].create(
            {
                "name": "TOUR-BATCH-CANCEL-REASON",
                "code": "TOUR-BATCH-CR",
                "global_use": True,
            }
        )

        # --- 12-restart.md: Cancelled.
        type_restart = cls._create_overtime_type("TOUR-BATCH-OTTYPE-RESTART")
        cls.batch_restart = cls._create_batch(
            type_restart, "2026-08-05 08:00:00", "2026-08-05 17:00:00"
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
        type_resetnum = cls._create_overtime_type("TOUR-BATCH-OTTYPE-RESETNUM")
        cls.batch_resetnum = cls._create_batch(
            type_resetnum, "2026-09-05 08:00:00", "2026-09-05 17:00:00"
        )
        cls.batch_resetnum.sudo().write({"name": "TOUR-BATCH-RESETNUM-999"})

        # --- 14-restart-approval.md: Waiting for Approval, with
        # approval_template_id cleared so the shipped policy.template
        # (which only grants restart_approval_ok while that field is
        # empty) evaluates to allowed — see the note in the IK itself.
        type_reapproval = cls._create_overtime_type("TOUR-BATCH-OTTYPE-REAPPROVAL")
        cls.employee_reapproval = employee_model.create(
            {"name": "TOUR-BATCH-EMP-REAPPROVAL"}
        )
        timesheet_model.create(
            cls._timesheet_values(cls.employee_reapproval, "2026-10-01", "2026-10-31")
        )
        cls.batch_reapproval = cls._create_batch(
            type_reapproval,
            "2026-10-05 08:00:00",
            "2026-10-05 17:00:00",
            cls.employee_reapproval,
        )
        cls.batch_reapproval.with_context(bypass_policy_check=True).action_confirm()
        cls.batch_reapproval.sudo().write({"approval_template_id": False})

    @classmethod
    def _create_overtime_type(cls, name):
        """Create an ``hr.overtime_type`` fixture used by one tour.

        :param str name: unique name, also used as the tour's
            dropdown-pick and list-row search anchor
        :return: the created ``hr.overtime_type`` record
        :rtype: recordset
        """
        return cls.env["hr.overtime_type"].create(
            {
                "name": name,
                "code": "/",
                "apply_limit_per_day": False,
            }
        )

    @classmethod
    def _timesheet_values(cls, employee, date_start, date_end):
        """Build ``hr.timesheet.create()`` values covering a batch.

        Includes ``working_schedule_id`` only when the field exists —
        it is added by the sibling ``ssi_timesheet_attendance_shift``
        module (installed alongside this one in this repo's CI), which
        requires it whenever ``schedule_source`` keeps its default
        ``working_schedule`` value.

        :param employee: ``hr.employee`` record the timesheet is for
        :param str date_start: ISO date string
        :param str date_end: ISO date string
        :return: values ready for ``hr.timesheet.create()``
        :rtype: dict
        """
        values = {
            "employee_id": employee.id,
            "date_start": date_start,
            "date_end": date_end,
        }
        if "working_schedule_id" in cls.timesheet_model._fields:
            values["working_schedule_id"] = cls.working_schedule.id
        return values

    @classmethod
    def _create_batch(cls, overtime_type, date_start, date_end, employee=False):
        """Create an ``hr.overtime_batch`` fixture.

        :param overtime_type: ``hr.overtime_type`` record for the batch
        :param str date_start: datetime string
        :param str date_end: datetime string, after ``date_start``
        :param employee: optional ``hr.employee`` record to include in
            **Employee(s)**
        :return: the created ``hr.overtime_batch`` record
        :rtype: recordset
        """
        values = {
            "type_id": overtime_type.id,
            "date_start": date_start,
            "date_end": date_end,
        }
        if employee:
            values["employee_ids"] = [(6, 0, employee.ids)]
        return cls.env["hr.overtime_batch"].create(values)

    def test_create(self):
        """Run the create tour for ``hr.overtime_batch``.

        IK: docs/hr_overtime_batch/01-create.md
        """
        self.start_tour(
            "/web", "ssi_hr_overtime_batch_hr_overtime_batch_create", login="admin"
        )

    def test_edit(self):
        """Run the edit tour for ``hr.overtime_batch``.

        IK: docs/hr_overtime_batch/02-edit.md
        """
        self.start_tour(
            "/web", "ssi_hr_overtime_batch_hr_overtime_batch_edit", login="admin"
        )

    def test_delete(self):
        """Run the delete tour for ``hr.overtime_batch``.

        IK: docs/hr_overtime_batch/03-delete.md
        """
        self.start_tour(
            "/web", "ssi_hr_overtime_batch_hr_overtime_batch_delete", login="admin"
        )

    def test_confirm(self):
        """Run the confirm tour for ``hr.overtime_batch``.

        IK: docs/hr_overtime_batch/04-confirm.md
        """
        self.start_tour(
            "/web", "ssi_hr_overtime_batch_hr_overtime_batch_confirm", login="admin"
        )

    def test_approve(self):
        """Run the approve tour for ``hr.overtime_batch``.

        IK: docs/hr_overtime_batch/05-approve.md
        """
        self.start_tour(
            "/web", "ssi_hr_overtime_batch_hr_overtime_batch_approve", login="admin"
        )

    def test_reject(self):
        """Run the reject tour for ``hr.overtime_batch``.

        IK: docs/hr_overtime_batch/06-reject.md
        """
        self.start_tour(
            "/web", "ssi_hr_overtime_batch_hr_overtime_batch_reject", login="admin"
        )

    def test_cancel(self):
        """Run the cancel tour for ``hr.overtime_batch``.

        IK: docs/hr_overtime_batch/10-cancel.md
        """
        self.start_tour(
            "/web", "ssi_hr_overtime_batch_hr_overtime_batch_cancel", login="admin"
        )

    def test_restart(self):
        """Run the restart tour for ``hr.overtime_batch``.

        IK: docs/hr_overtime_batch/12-restart.md
        """
        self.start_tour(
            "/web", "ssi_hr_overtime_batch_hr_overtime_batch_restart", login="admin"
        )

    def test_reset_number(self):
        """Run the reset document number tour for ``hr.overtime_batch``.

        IK: docs/hr_overtime_batch/13-reset-number.md
        """
        self.start_tour(
            "/web",
            "ssi_hr_overtime_batch_hr_overtime_batch_reset_number",
            login="admin",
        )

    def test_restart_approval(self):
        """Run the restart approval process tour for ``hr.overtime_batch``.

        IK: docs/hr_overtime_batch/14-restart-approval.md
        """
        self.start_tour(
            "/web",
            "ssi_hr_overtime_batch_hr_overtime_batch_restart_approval",
            login="admin",
        )
