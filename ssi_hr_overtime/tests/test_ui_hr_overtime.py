# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiHrOvertime(HttpSavepointCase):
    """Tour tests for the ``hr.overtime`` work instructions.

    Uses ``HttpSavepointCase`` rather than plain ``HttpCase``: in 14.0
    ``TransactionCase`` only assigns ``self.env`` inside instance
    ``setUp()``, so ``cls.env`` is not available in ``setUpClass()``.
    ``HttpSavepointCase`` (via ``SingleTransactionCase``) does set
    ``cls.env`` in ``setUpClass()``, which the tours below rely on to
    seed employees, timesheets and overtimes visible to the browser
    session.

    No group grant is needed here: ``ssi_hr_overtime``'s own demo data
    (``security/res_group_data.xml``) already adds ``base.user_admin``
    to ``hr_overtime_validator_group`` (which implies
    ``hr_overtime_user_group`` and ``hr_overtime_viewer_group``) and to
    ``overtime_all_group`` (data ownership), and admin is the sole member
    of the single-level ``approval.template`` approver group, so it can
    both act as the requesting user and the approver.

    Every fixture uses an overtime type with ``apply_limit_per_day``
    unchecked (``TOUR-OTTYPE``), so the Pre-Condition on **Limit Per
    Days** (see ``docs/hr_overtime/01-create.md``) never applies.

    Every fixture also needs a covering ``hr.timesheet`` record: ``hr.
    overtime``'s ``sheet_id`` is a required, constrained field
    (``_constrains_sheet_id``) computed from the employee's timesheets
    whose date range covers the overtime's **Date** — see
    ``docs/hr_overtime/01-create.md`` Pre-Condition.
    """

    @classmethod
    def setUpClass(cls):
        """Seed one employee/timesheet/overtime fixture per tour."""
        super().setUpClass()

        employee_model = cls.env["hr.employee"]
        timesheet_model = cls.env["hr.timesheet"]
        cls.timesheet_model = timesheet_model

        cls.working_schedule = cls.env["resource.calendar"].search(
            [], limit=1, order="id asc"
        )
        cls.overtime_type = cls.env["hr.overtime_type"].create(
            {
                "name": "TOUR-OTTYPE",
                "code": "/",
                "apply_limit_per_day": False,
            }
        )

        # --- 01-create.md: no overtime fixture — the tour creates it.
        cls.employee_create = employee_model.create({"name": "TOUR-EMP-OT-CREATE"})
        timesheet_model.create(
            cls._timesheet_values(cls.employee_create, "2026-01-01", "2026-01-31")
        )

        # --- 02-edit.md: Draft.
        cls.employee_edit = employee_model.create({"name": "TOUR-EMP-OT-EDIT"})
        timesheet_model.create(
            cls._timesheet_values(cls.employee_edit, "2026-02-01", "2026-02-28")
        )
        cls.overtime_edit = cls._create_overtime(
            cls.employee_edit,
            "2026-02-05",
            "2026-02-05 08:00:00",
            "2026-02-05 17:00:00",
        )

        # --- 03-delete.md: Draft, document number still "/".
        cls.employee_delete = employee_model.create({"name": "TOUR-EMP-OT-DELETE"})
        timesheet_model.create(
            cls._timesheet_values(cls.employee_delete, "2026-03-01", "2026-03-31")
        )
        cls.overtime_delete = cls._create_overtime(
            cls.employee_delete,
            "2026-03-05",
            "2026-03-05 08:00:00",
            "2026-03-05 17:00:00",
        )

        # --- 04-confirm.md: Draft, ready to Confirm.
        cls.employee_confirm = employee_model.create({"name": "TOUR-EMP-OT-CONFIRM"})
        timesheet_model.create(
            cls._timesheet_values(cls.employee_confirm, "2026-04-01", "2026-04-30")
        )
        cls.overtime_confirm = cls._create_overtime(
            cls.employee_confirm,
            "2026-04-05",
            "2026-04-05 08:00:00",
            "2026-04-05 17:00:00",
        )

        # --- 05-approve.md: Waiting for Approval; admin (Validator) is the
        # pending approver for the single-level "Standard" approval
        # template.
        cls.employee_approve = employee_model.create({"name": "TOUR-EMP-OT-APPROVE"})
        timesheet_model.create(
            cls._timesheet_values(cls.employee_approve, "2026-05-01", "2026-05-31")
        )
        cls.overtime_approve = cls._create_overtime(
            cls.employee_approve,
            "2026-05-05",
            "2026-05-05 08:00:00",
            "2026-05-05 17:00:00",
        )
        cls.overtime_approve.with_context(bypass_policy_check=True).action_confirm()

        # --- 06-reject.md: Waiting for Approval, independent record from
        # the approve fixture above.
        cls.employee_reject = employee_model.create({"name": "TOUR-EMP-OT-REJECT"})
        timesheet_model.create(
            cls._timesheet_values(cls.employee_reject, "2026-06-01", "2026-06-30")
        )
        cls.overtime_reject = cls._create_overtime(
            cls.employee_reject,
            "2026-06-05",
            "2026-06-05 08:00:00",
            "2026-06-05 17:00:00",
        )
        cls.overtime_reject.with_context(bypass_policy_check=True).action_confirm()

        # --- 10-cancel.md: Draft (cancel_ok also applies to confirm/done).
        # A global cancel reason is required by the wizard.
        cls.employee_cancel = employee_model.create({"name": "TOUR-EMP-OT-CANCEL"})
        timesheet_model.create(
            cls._timesheet_values(cls.employee_cancel, "2026-07-01", "2026-07-31")
        )
        cls.overtime_cancel = cls._create_overtime(
            cls.employee_cancel,
            "2026-07-05",
            "2026-07-05 08:00:00",
            "2026-07-05 17:00:00",
        )
        cls.cancel_reason = cls.env["base.cancel_reason"].create(
            {
                "name": "TOUR-OT-CANCEL-REASON",
                "code": "TOUR-OT-CR",
                "global_use": True,
            }
        )

        # --- 12-restart.md: Cancelled.
        cls.employee_restart = employee_model.create({"name": "TOUR-EMP-OT-RESTART"})
        timesheet_model.create(
            cls._timesheet_values(cls.employee_restart, "2026-08-01", "2026-08-31")
        )
        cls.overtime_restart = cls._create_overtime(
            cls.employee_restart,
            "2026-08-05",
            "2026-08-05 08:00:00",
            "2026-08-05 17:00:00",
        )
        restart_reason = cls.env["base.cancel_reason"].create(
            {
                "name": "TOUR-OT-RESTART-REASON",
                "code": "TOUR-OT-RR",
                "global_use": True,
            }
        )
        cls.overtime_restart.with_context(bypass_policy_check=True).action_cancel(
            restart_reason
        )

        # --- 13-reset-number.md: Draft, with a document number already
        # assigned (simulating a manually-numbered record) so the Reset
        # Document Number button has a visible effect.
        cls.employee_resetnum = employee_model.create({"name": "TOUR-EMP-OT-RESETNUM"})
        timesheet_model.create(
            cls._timesheet_values(cls.employee_resetnum, "2026-09-01", "2026-09-30")
        )
        cls.overtime_resetnum = cls._create_overtime(
            cls.employee_resetnum,
            "2026-09-05",
            "2026-09-05 08:00:00",
            "2026-09-05 17:00:00",
        )
        cls.overtime_resetnum.sudo().write({"name": "TOUR-OT-RESETNUM-999"})

        # --- 14-restart-approval.md: Waiting for Approval, with
        # approval_template_id cleared so the shipped policy.template
        # (which only grants restart_approval_ok while that field is
        # empty) evaluates to allowed — see the note in the IK itself.
        cls.employee_restart_approval = employee_model.create(
            {"name": "TOUR-EMP-OT-RESTARTAPPROVAL"}
        )
        timesheet_model.create(
            cls._timesheet_values(
                cls.employee_restart_approval, "2026-10-01", "2026-10-31"
            )
        )
        cls.overtime_restart_approval = cls._create_overtime(
            cls.employee_restart_approval,
            "2026-10-05",
            "2026-10-05 08:00:00",
            "2026-10-05 17:00:00",
        )
        cls.overtime_restart_approval.with_context(
            bypass_policy_check=True
        ).action_confirm()
        cls.overtime_restart_approval.sudo().write({"approval_template_id": False})

    @classmethod
    def _timesheet_values(cls, employee, date_start, date_end):
        """Build ``hr.timesheet.create()`` values covering an overtime.

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
    def _create_overtime(cls, employee, date, date_start, date_end):
        """Create an ``hr.overtime`` fixture covered by ``employee``'s
        timesheet.

        :param employee: ``hr.employee`` record the overtime is for
        :param str date: ISO date string, within a timesheet already
            created for ``employee``
        :param str date_start: datetime string on the same calendar day
            as ``date``
        :param str date_end: datetime string, at most 24 hours after
            ``date_start``
        :return: the created ``hr.overtime`` record
        :rtype: recordset
        """
        return cls.env["hr.overtime"].create(
            {
                "employee_id": employee.id,
                "type_id": cls.overtime_type.id,
                "date": date,
                "date_start": date_start,
                "date_end": date_end,
            }
        )

    def test_create(self):
        """Run the create tour for ``hr.overtime``.

        IK: docs/hr_overtime/01-create.md
        """
        self.start_tour("/web", "ssi_hr_overtime_hr_overtime_create", login="admin")

    def test_edit(self):
        """Run the edit tour for ``hr.overtime``.

        IK: docs/hr_overtime/02-edit.md
        """
        self.start_tour("/web", "ssi_hr_overtime_hr_overtime_edit", login="admin")

    def test_delete(self):
        """Run the delete tour for ``hr.overtime``.

        IK: docs/hr_overtime/03-delete.md
        """
        self.start_tour("/web", "ssi_hr_overtime_hr_overtime_delete", login="admin")

    def test_confirm(self):
        """Run the confirm tour for ``hr.overtime``.

        IK: docs/hr_overtime/04-confirm.md
        """
        self.start_tour("/web", "ssi_hr_overtime_hr_overtime_confirm", login="admin")

    def test_approve(self):
        """Run the approve tour for ``hr.overtime``.

        IK: docs/hr_overtime/05-approve.md
        """
        self.start_tour("/web", "ssi_hr_overtime_hr_overtime_approve", login="admin")

    def test_reject(self):
        """Run the reject tour for ``hr.overtime``.

        IK: docs/hr_overtime/06-reject.md
        """
        self.start_tour("/web", "ssi_hr_overtime_hr_overtime_reject", login="admin")

    def test_cancel(self):
        """Run the cancel tour for ``hr.overtime``.

        IK: docs/hr_overtime/10-cancel.md
        """
        self.start_tour("/web", "ssi_hr_overtime_hr_overtime_cancel", login="admin")

    def test_restart(self):
        """Run the restart tour for ``hr.overtime``.

        IK: docs/hr_overtime/12-restart.md
        """
        self.start_tour("/web", "ssi_hr_overtime_hr_overtime_restart", login="admin")

    def test_reset_number(self):
        """Run the reset document number tour for ``hr.overtime``.

        IK: docs/hr_overtime/13-reset-number.md
        """
        self.start_tour(
            "/web", "ssi_hr_overtime_hr_overtime_reset_number", login="admin"
        )

    def test_restart_approval(self):
        """Run the restart approval process tour for ``hr.overtime``.

        IK: docs/hr_overtime/14-restart-approval.md
        """
        self.start_tour(
            "/web", "ssi_hr_overtime_hr_overtime_restart_approval", login="admin"
        )
