# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiHrLeave(HttpSavepointCase):
    """Tour tests for the ``hr.leave`` work instructions.

    Uses ``HttpSavepointCase`` rather than plain ``HttpCase``: in 14.0
    ``TransactionCase`` only assigns ``self.env`` inside instance
    ``setUp()``, so ``cls.env`` is not available in ``setUpClass()``.
    ``HttpSavepointCase`` (via ``SingleTransactionCase``) does set
    ``cls.env`` in ``setUpClass()``, which the tours below rely on to
    seed employees, timesheets and leaves visible to the browser
    session.

    No group grant is needed here: ``ssi_hr_holiday``'s own demo data
    (``security/res_group_data.xml``) already adds ``base.user_admin``
    to ``hr_leave_validator_group`` (which implies ``hr_leave_user_group``
    and ``hr_leave_viewer_group``) and to ``leave_all_group`` (data
    ownership), and admin is the sole member of the single-level
    ``approval.template`` approver group, so it can both act as the
    requesting user and the approver.

    Every fixture uses a leave type with ``need_allocation`` unchecked
    (``TOUR-LTYPE-LEAVE``), so the Pre-Condition on an available
    ``hr.leave_allocation`` (see ``docs/hr_leave/04-confirm.md``) never
    applies — leave allocation coverage is out of scope for these tours,
    it belongs to ``hr.leave_allocation``'s own IK/tour set.

    Every fixture also needs a covering ``hr.timesheet`` record: ``hr.
    leave``'s ``sheet_id`` is a required, constrained field
    (``_constrains_sheet_id``) computed from the employee's timesheets
    whose date range covers the leave — see ``docs/hr_leave/01-create.md``
    Pre-Condition.
    """

    @classmethod
    def setUpClass(cls):
        """Seed one employee/timesheet/leave fixture per tour."""
        super().setUpClass()

        employee_model = cls.env["hr.employee"]
        timesheet_model = cls.env["hr.timesheet"]
        cls.timesheet_model = timesheet_model

        cls.working_schedule = cls.env["resource.calendar"].search(
            [], limit=1, order="id asc"
        )
        cls.leave_type = cls.env["hr.leave_type"].create(
            {
                "name": "TOUR-LTYPE-LEAVE",
                "code": "/",
                "need_allocation": False,
            }
        )

        # --- 01-create.md: no leave fixture — the tour creates it.
        cls.employee_create = employee_model.create({"name": "TOUR-EMP-LEAVE-CREATE"})
        timesheet_model.create(
            cls._timesheet_values(cls.employee_create, "2026-01-01", "2026-01-31")
        )

        # --- 02-edit.md: Draft.
        cls.employee_edit = employee_model.create({"name": "TOUR-EMP-LEAVE-EDIT"})
        timesheet_model.create(
            cls._timesheet_values(cls.employee_edit, "2026-02-01", "2026-02-28")
        )
        cls.leave_edit = cls._create_leave(
            cls.employee_edit, "2026-02-05", "2026-02-05"
        )

        # --- 03-delete.md: Draft, document number still "/".
        cls.employee_delete = employee_model.create({"name": "TOUR-EMP-LEAVE-DELETE"})
        timesheet_model.create(
            cls._timesheet_values(cls.employee_delete, "2026-03-01", "2026-03-31")
        )
        cls.leave_delete = cls._create_leave(
            cls.employee_delete, "2026-03-05", "2026-03-05"
        )

        # --- 04-confirm.md: Draft, ready to Confirm.
        cls.employee_confirm = employee_model.create({"name": "TOUR-EMP-LEAVE-CONFIRM"})
        timesheet_model.create(
            cls._timesheet_values(cls.employee_confirm, "2026-04-01", "2026-04-30")
        )
        cls.leave_confirm = cls._create_leave(
            cls.employee_confirm, "2026-04-05", "2026-04-05"
        )

        # --- 05-approve.md: Waiting for Approval; admin (Validator) is the
        # pending approver for the single-level "Standard" approval.
        # template.
        cls.employee_approve = employee_model.create({"name": "TOUR-EMP-LEAVE-APPROVE"})
        timesheet_model.create(
            cls._timesheet_values(cls.employee_approve, "2026-05-01", "2026-05-31")
        )
        cls.leave_approve = cls._create_leave(
            cls.employee_approve, "2026-05-05", "2026-05-05"
        )
        cls.leave_approve.with_context(bypass_policy_check=True).action_confirm()

        # --- 06-reject.md: Waiting for Approval, independent record from
        # the approve fixture above.
        cls.employee_reject = employee_model.create({"name": "TOUR-EMP-LEAVE-REJECT"})
        timesheet_model.create(
            cls._timesheet_values(cls.employee_reject, "2026-06-01", "2026-06-30")
        )
        cls.leave_reject = cls._create_leave(
            cls.employee_reject, "2026-06-05", "2026-06-05"
        )
        cls.leave_reject.with_context(bypass_policy_check=True).action_confirm()

        # --- 10-cancel.md: Draft (cancel_ok also applies to confirm/done).
        # A global cancel reason is required by the wizard.
        cls.employee_cancel = employee_model.create({"name": "TOUR-EMP-LEAVE-CANCEL"})
        timesheet_model.create(
            cls._timesheet_values(cls.employee_cancel, "2026-07-01", "2026-07-31")
        )
        cls.leave_cancel = cls._create_leave(
            cls.employee_cancel, "2026-07-05", "2026-07-05"
        )
        cls.cancel_reason = cls.env["base.cancel_reason"].create(
            {
                "name": "TOUR-LEAVE-CANCEL-REASON",
                "code": "TOUR-LV-CR",
                "global_use": True,
            }
        )

        # --- 12-restart.md: Cancelled.
        cls.employee_restart = employee_model.create({"name": "TOUR-EMP-LEAVE-RESTART"})
        timesheet_model.create(
            cls._timesheet_values(cls.employee_restart, "2026-08-01", "2026-08-31")
        )
        cls.leave_restart = cls._create_leave(
            cls.employee_restart, "2026-08-05", "2026-08-05"
        )
        restart_reason = cls.env["base.cancel_reason"].create(
            {
                "name": "TOUR-LEAVE-RESTART-REASON",
                "code": "TOUR-LV-RR",
                "global_use": True,
            }
        )
        cls.leave_restart.with_context(bypass_policy_check=True).action_cancel(
            restart_reason
        )

        # --- 13-reset-number.md: Draft, with a document number already
        # assigned (simulating a manually-numbered record) so the Reset
        # Document Number button has a visible effect.
        cls.employee_resetnum = employee_model.create(
            {"name": "TOUR-EMP-LEAVE-RESETNUM"}
        )
        timesheet_model.create(
            cls._timesheet_values(cls.employee_resetnum, "2026-09-01", "2026-09-30")
        )
        cls.leave_resetnum = cls._create_leave(
            cls.employee_resetnum, "2026-09-05", "2026-09-05"
        )
        cls.leave_resetnum.sudo().write({"name": "TOUR-LEAVE-RESETNUM-999"})

        # --- 14-restart-approval.md: Waiting for Approval, with
        # approval_template_id cleared so the shipped policy.template
        # (which only grants restart_approval_ok while that field is
        # empty) evaluates to allowed — see the note in the IK itself.
        cls.employee_restart_approval = employee_model.create(
            {"name": "TOUR-EMP-LEAVE-RESTARTAPPROVAL"}
        )
        timesheet_model.create(
            cls._timesheet_values(
                cls.employee_restart_approval, "2026-10-01", "2026-10-31"
            )
        )
        cls.leave_restart_approval = cls._create_leave(
            cls.employee_restart_approval, "2026-10-05", "2026-10-05"
        )
        cls.leave_restart_approval.with_context(
            bypass_policy_check=True
        ).action_confirm()
        cls.leave_restart_approval.sudo().write({"approval_template_id": False})

    @classmethod
    def _timesheet_values(cls, employee, date_start, date_end):
        """Build ``hr.timesheet.create()`` values covering a leave.

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
    def _create_leave(cls, employee, date_start, date_end):
        """Create an ``hr.leave`` fixture covered by ``employee``'s
        timesheet.

        :param employee: ``hr.employee`` record the leave is for
        :param str date_start: ISO date string, within a timesheet
            already created for ``employee``
        :param str date_end: ISO date string, within a timesheet
            already created for ``employee``
        :return: the created ``hr.leave`` record
        :rtype: recordset
        """
        return cls.env["hr.leave"].create(
            {
                "employee_id": employee.id,
                "type_id": cls.leave_type.id,
                "date_start": date_start,
                "date_end": date_end,
                "number_of_days": 1,
            }
        )

    def test_create(self):
        """Run the create tour for ``hr.leave``.

        IK: docs/hr_leave/01-create.md
        """
        self.start_tour("/web", "ssi_hr_holiday_hr_leave_create", login="admin")

    def test_edit(self):
        """Run the edit tour for ``hr.leave``.

        IK: docs/hr_leave/02-edit.md
        """
        self.start_tour("/web", "ssi_hr_holiday_hr_leave_edit", login="admin")

    def test_delete(self):
        """Run the delete tour for ``hr.leave``.

        IK: docs/hr_leave/03-delete.md
        """
        self.start_tour("/web", "ssi_hr_holiday_hr_leave_delete", login="admin")

    def test_confirm(self):
        """Run the confirm tour for ``hr.leave``.

        IK: docs/hr_leave/04-confirm.md
        """
        self.start_tour("/web", "ssi_hr_holiday_hr_leave_confirm", login="admin")

    def test_approve(self):
        """Run the approve tour for ``hr.leave``.

        IK: docs/hr_leave/05-approve.md
        """
        self.start_tour("/web", "ssi_hr_holiday_hr_leave_approve", login="admin")

    def test_reject(self):
        """Run the reject tour for ``hr.leave``.

        IK: docs/hr_leave/06-reject.md
        """
        self.start_tour("/web", "ssi_hr_holiday_hr_leave_reject", login="admin")

    def test_cancel(self):
        """Run the cancel tour for ``hr.leave``.

        IK: docs/hr_leave/10-cancel.md
        """
        self.start_tour("/web", "ssi_hr_holiday_hr_leave_cancel", login="admin")

    def test_restart(self):
        """Run the restart tour for ``hr.leave``.

        IK: docs/hr_leave/12-restart.md
        """
        self.start_tour("/web", "ssi_hr_holiday_hr_leave_restart", login="admin")

    def test_reset_number(self):
        """Run the reset document number tour for ``hr.leave``.

        IK: docs/hr_leave/13-reset-number.md
        """
        self.start_tour("/web", "ssi_hr_holiday_hr_leave_reset_number", login="admin")

    def test_restart_approval(self):
        """Run the restart approval process tour for ``hr.leave``.

        IK: docs/hr_leave/14-restart-approval.md
        """
        self.start_tour(
            "/web", "ssi_hr_holiday_hr_leave_restart_approval", login="admin"
        )
