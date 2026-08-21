# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

# HttpSavepointCase — BUKAN HttpCase. In 14.0, plain HttpCase does not
# set up cls.env in setUpClass; HttpSavepointCase does.
from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiHrOvertime(HttpSavepointCase):
    """Tour test for the ``hr.overtime`` Documenso signing delta."""

    @classmethod
    def setUpClass(cls):
        """Create an Overtime already Waiting for Approval.

        ``base.user_admin`` is already a member of
        ``hr_overtime_validator_group`` (which implies the ``User``
        and ``Viewer`` groups) via ``ssi_hr_overtime``'s
        ``security/res_group_data.xml``, so it can create and confirm
        the record directly, without extra group setup. A dedicated
        Overtime Type with ``apply_limit_per_day = False`` is created,
        matching the fixture pattern in
        ``ssi_hr_overtime/tests/test_ui_hr_overtime.py``. An
        ``hr.timesheet`` covering the overtime's date is also created
        for the employee — ``_constrains_sheet_id`` requires
        ``sheet_id`` (computed from a matching ``hr.timesheet``) to be
        set. Pre-Condition IK 05-approve.md (delta): the record is
        already Waiting for Approval, reached here via
        ``action_confirm()`` in Python, not via UI clicks. The
        "Standard" approval template used by ``ssi_hr_overtime`` demo
        data has no Documenso Signing Template configured, so the
        Signature Requests tab is present
        (``_documenso_signing_create_page = True``) but the base
        Approve/OK Flow is unaffected -- this tour does not exercise
        it.
        """
        super().setUpClass()
        cls.admin = cls.env.ref("base.user_admin")

        employee = (
            cls.env["hr.employee"]
            .with_user(cls.admin)
            .create({"name": "TOUR-EMP-OT-DOCUMENSO-APPROVE"})
        )
        overtime_type = (
            cls.env["hr.overtime_type"]
            .with_user(cls.admin)
            .create(
                {
                    "name": "TOUR-OTTYPE-DOCUMENSO",
                    "code": "/",
                    "apply_limit_per_day": False,
                }
            )
        )
        timesheet_values = {
            "employee_id": employee.id,
            "date_start": "2026-01-01",
            "date_end": "2026-01-31",
        }
        if "working_schedule_id" in cls.env["hr.timesheet"]._fields:
            timesheet_values[
                "working_schedule_id"
            ] = cls.env.company.resource_calendar_id.id
        cls.env["hr.timesheet"].with_user(cls.admin).create(timesheet_values)
        cls.overtime = (
            cls.env["hr.overtime"]
            .with_user(cls.admin)
            .create(
                {
                    "employee_id": employee.id,
                    "type_id": overtime_type.id,
                    "date": "2026-01-15",
                    "date_start": "2026-01-15 08:00:00",
                    "date_end": "2026-01-15 10:00:00",
                }
            )
        )
        cls.overtime.with_context(bypass_policy_check=True).action_confirm()

    def test_approve(self):
        """Run the approve tour for the Documenso signing delta.

        IK: docs/hr_overtime/05-approve.md (E2a delta -- Modified Flow)
        """
        self.start_tour(
            "/web",
            "ssi_hr_overtime_documenso_signing_hr_overtime_approve",
            login="admin",
        )
