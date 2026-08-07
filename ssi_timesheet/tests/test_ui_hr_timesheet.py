# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiHrTimesheet(HttpSavepointCase):
    """Tour tests for the ``hr.timesheet`` work instructions.

    Uses ``HttpSavepointCase`` rather than plain ``HttpCase``: in 14.0
    ``TransactionCase`` only assigns ``self.env`` inside instance
    ``setUp()``, so ``cls.env`` is not available in ``setUpClass()``.
    ``HttpSavepointCase`` (via ``SingleTransactionCase``) does set
    ``cls.env`` in ``setUpClass()``, which the tours below rely on to
    seed employees and timesheets visible to the browser session.
    """

    @classmethod
    def setUpClass(cls):
        """Grant the Validator group and seed one fixture per tour.

        Pre-Condition common to every ``hr_timesheet`` IK: the actor is
        in group *Timesheets — User* (or a state-specific action
        requires *Timesheets — Validator*). Granting *Validator* to
        ``admin`` covers both, since it implies *User* which implies
        *Viewer* (menu access).

        Each state-transition tour needs its own employee/timesheet
        pair already sitting in the state the IK's Pre-Condition
        requires; those are built here by calling the transition
        methods directly with ``bypass_policy_check``, mirroring how
        ``tests/test_data_timesheet.yaml`` prepares the same states.
        """
        super().setUpClass()
        cls.env.ref("ssi_timesheet.hr_timesheet_validator_group").sudo().write(
            {"users": [(4, cls.env.ref("base.user_admin").id)]}
        )

        employee_model = cls.env["hr.employee"]
        item_model = cls.env["hr.timesheet_computation_item"]
        timesheet_model = cls.env["hr.timesheet"]

        # --- 01-create.md: employee with a registered computation item,
        # so the tour's Reload button click has a deterministic row to
        # wait for.
        cls.employee_create = employee_model.create({"name": "TOUR-EMP-CREATE"})
        item_create = item_model.create(
            {
                "name": "TOUR-COMP-CREATE",
                "code": "TCC01",
                "python_code": "result = True",
            }
        )
        cls.employee_create.timesheet_computation_ids = [(6, 0, [item_create.id])]

        # --- 02-edit.md: draft timesheet, employee also carries a
        # registered computation item for the same Reload gate.
        cls.employee_edit = employee_model.create({"name": "TOUR-EMP-EDIT"})
        item_edit = item_model.create(
            {
                "name": "TOUR-COMP-EDIT",
                "code": "TCE01",
                "python_code": "result = True",
            }
        )
        cls.employee_edit.timesheet_computation_ids = [(6, 0, [item_edit.id])]
        cls.timesheet_edit = timesheet_model.create(
            {
                "employee_id": cls.employee_edit.id,
                "date_start": "2026-01-01",
                "date_end": "2026-01-31",
            }
        )

        # --- 03-delete.md: draft timesheet, document number still "/".
        cls.employee_delete = employee_model.create({"name": "TOUR-EMP-DELETE"})
        cls.timesheet_delete = timesheet_model.create(
            {
                "employee_id": cls.employee_delete.id,
                "date_start": "2026-02-01",
                "date_end": "2026-02-28",
            }
        )

        # --- 04-confirm.md: On Progress (state=open).
        cls.employee_confirm = employee_model.create({"name": "TOUR-EMP-CONFIRM"})
        cls.timesheet_confirm = timesheet_model.create(
            {
                "employee_id": cls.employee_confirm.id,
                "date_start": "2026-03-01",
                "date_end": "2026-03-31",
            }
        )
        cls.timesheet_confirm.with_context(bypass_policy_check=True).action_open()

        # --- 05-approve.md: Waiting for Approval (state=confirm); admin
        # (Validator) is the pending approver for the single-level
        # "Standard - Timesheet" approval.template.
        cls.employee_approve = employee_model.create({"name": "TOUR-EMP-APPROVE"})
        cls.timesheet_approve = timesheet_model.create(
            {
                "employee_id": cls.employee_approve.id,
                "date_start": "2026-04-01",
                "date_end": "2026-04-30",
            }
        )
        cls.timesheet_approve.with_context(bypass_policy_check=True).action_open()
        cls.timesheet_approve.with_context(bypass_policy_check=True).action_confirm()

        # --- 06-reject.md: Waiting for Approval, independent record from
        # the approve fixture above.
        cls.employee_reject = employee_model.create({"name": "TOUR-EMP-REJECT"})
        cls.timesheet_reject = timesheet_model.create(
            {
                "employee_id": cls.employee_reject.id,
                "date_start": "2026-05-01",
                "date_end": "2026-05-31",
            }
        )
        cls.timesheet_reject.with_context(bypass_policy_check=True).action_open()
        cls.timesheet_reject.with_context(bypass_policy_check=True).action_confirm()

        # --- 07-start.md: Draft, ready to Start.
        cls.employee_start = employee_model.create({"name": "TOUR-EMP-START"})
        cls.timesheet_start = timesheet_model.create(
            {
                "employee_id": cls.employee_start.id,
                "date_start": "2026-06-01",
                "date_end": "2026-06-30",
            }
        )

        # --- 10-cancel.md: Draft (cancel_ok also applies to draft,
        # confirm and done). A global cancel reason is required by the
        # wizard.
        cls.employee_cancel = employee_model.create({"name": "TOUR-EMP-CANCEL"})
        cls.timesheet_cancel = timesheet_model.create(
            {
                "employee_id": cls.employee_cancel.id,
                "date_start": "2026-07-01",
                "date_end": "2026-07-31",
            }
        )
        cls.cancel_reason = cls.env["base.cancel_reason"].create(
            {
                "name": "TOUR-CANCEL-REASON",
                "code": "TOUR-CR",
                "global_use": True,
            }
        )

        # --- 12-restart.md: Cancelled (state=cancel).
        cls.employee_restart = employee_model.create({"name": "TOUR-EMP-RESTART"})
        cls.timesheet_restart = timesheet_model.create(
            {
                "employee_id": cls.employee_restart.id,
                "date_start": "2026-08-01",
                "date_end": "2026-08-31",
            }
        )
        restart_reason = cls.env["base.cancel_reason"].create(
            {
                "name": "TOUR-RESTART-REASON",
                "code": "TOUR-RR",
                "global_use": True,
            }
        )
        cls.timesheet_restart.with_context(bypass_policy_check=True).action_cancel(
            restart_reason
        )

        # --- 13-reset-number.md: Draft, with a document number already
        # assigned (simulating a manually-numbered record) so the Reset
        # Document Number button has a visible effect.
        cls.employee_resetnum = employee_model.create({"name": "TOUR-EMP-RESETNUM"})
        cls.timesheet_resetnum = timesheet_model.create(
            {
                "employee_id": cls.employee_resetnum.id,
                "date_start": "2026-09-01",
                "date_end": "2026-09-30",
            }
        )
        cls.timesheet_resetnum.sudo().write({"name": "TOUR-RESETNUM-999"})

        # --- 14-restart-approval.md: Waiting for Approval, with
        # approval_template_id cleared so the shipped policy.template
        # (which only grants restart_approval_ok while that field is
        # empty) evaluates to allowed — see the note in the IK itself.
        cls.employee_restart_approval = employee_model.create(
            {"name": "TOUR-EMP-RESTARTAPPROVAL"}
        )
        cls.timesheet_restart_approval = timesheet_model.create(
            {
                "employee_id": cls.employee_restart_approval.id,
                "date_start": "2026-10-01",
                "date_end": "2026-10-31",
            }
        )
        cls.timesheet_restart_approval.with_context(
            bypass_policy_check=True
        ).action_open()
        cls.timesheet_restart_approval.with_context(
            bypass_policy_check=True
        ).action_confirm()
        cls.timesheet_restart_approval.sudo().write({"approval_template_id": False})

    def test_create(self):
        """Run the create tour for ``hr.timesheet``.

        IK: docs/hr_timesheet/01-create.md
        """
        self.start_tour("/web", "ssi_timesheet_hr_timesheet_create", login="admin")

    def test_edit(self):
        """Run the edit tour for ``hr.timesheet``.

        IK: docs/hr_timesheet/02-edit.md
        """
        self.start_tour("/web", "ssi_timesheet_hr_timesheet_edit", login="admin")

    def test_delete(self):
        """Run the delete tour for ``hr.timesheet``.

        IK: docs/hr_timesheet/03-delete.md
        """
        self.start_tour("/web", "ssi_timesheet_hr_timesheet_delete", login="admin")

    def test_confirm(self):
        """Run the confirm tour for ``hr.timesheet``.

        IK: docs/hr_timesheet/04-confirm.md
        """
        self.start_tour("/web", "ssi_timesheet_hr_timesheet_confirm", login="admin")

    def test_approve(self):
        """Run the approve tour for ``hr.timesheet``.

        IK: docs/hr_timesheet/05-approve.md
        """
        self.start_tour("/web", "ssi_timesheet_hr_timesheet_approve", login="admin")

    def test_reject(self):
        """Run the reject tour for ``hr.timesheet``.

        IK: docs/hr_timesheet/06-reject.md
        """
        self.start_tour("/web", "ssi_timesheet_hr_timesheet_reject", login="admin")

    def test_start(self):
        """Run the start tour for ``hr.timesheet``.

        IK: docs/hr_timesheet/07-start.md
        """
        self.start_tour("/web", "ssi_timesheet_hr_timesheet_start", login="admin")

    def test_cancel(self):
        """Run the cancel tour for ``hr.timesheet``.

        IK: docs/hr_timesheet/10-cancel.md
        """
        self.start_tour("/web", "ssi_timesheet_hr_timesheet_cancel", login="admin")

    def test_restart(self):
        """Run the restart tour for ``hr.timesheet``.

        IK: docs/hr_timesheet/12-restart.md
        """
        self.start_tour("/web", "ssi_timesheet_hr_timesheet_restart", login="admin")

    def test_reset_number(self):
        """Run the reset document number tour for ``hr.timesheet``.

        IK: docs/hr_timesheet/13-reset-number.md
        """
        self.start_tour(
            "/web", "ssi_timesheet_hr_timesheet_reset_number", login="admin"
        )

    def test_restart_approval(self):
        """Run the restart approval process tour for ``hr.timesheet``.

        IK: docs/hr_timesheet/14-restart-approval.md
        """
        self.start_tour(
            "/web", "ssi_timesheet_hr_timesheet_restart_approval", login="admin"
        )
