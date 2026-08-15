# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

# HttpSavepointCase — BUKAN HttpCase. In 14.0, plain HttpCase does not
# set up cls.env in setUpClass; HttpSavepointCase does.
from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiHrLeave(HttpSavepointCase):
    """Tour test for the ``hr.leave`` Documenso signing delta."""

    @classmethod
    def setUpClass(cls):
        """Create a Leave already Waiting for Approval.

        ``base.user_admin`` is already a member of
        ``hr_leave_validator_group`` (which implies the ``User`` and
        ``Viewer`` groups) via ``ssi_hr_holiday``'s
        ``security/res_group_data.xml``, so it can create and confirm
        the record directly, without extra group setup. Pre-Condition
        IK 05-approve.md (delta): the record is already Waiting for
        Approval, reached here via ``action_confirm()`` in Python, not
        via UI clicks. The "Standard" approval template used by
        ``ssi_hr_holiday`` demo data has no Documenso Signing Template
        configured, so the Signature Requests tab is present
        (``_documenso_signing_create_page = True``) but the base
        Approve/OK Flow is unaffected -- this tour does not exercise
        it.
        """
        super().setUpClass()
        cls.admin = cls.env.ref("base.user_admin")

        employee = (
            cls.env["hr.employee"]
            .with_user(cls.admin)
            .create({"name": "Tour HR Holiday Documenso Leave Employee"})
        )
        leave_type = cls.env["hr.leave_type"].search([], limit=1, order="id asc")
        cls.leave = (
            cls.env["hr.leave"]
            .with_user(cls.admin)
            .create(
                {
                    "employee_id": employee.id,
                    "type_id": leave_type.id,
                    "date_start": "2026-01-15 08:00:00",
                    "date_end": "2026-01-15 17:00:00",
                }
            )
        )
        cls.leave.with_context(bypass_policy_check=True).action_confirm()

    def test_approve(self):
        """Run the approve tour for the Documenso signing delta.

        IK: docs/hr_leave/05-approve.md (E2a delta -- Modified Flow)
        """
        self.start_tour(
            "/web",
            "ssi_hr_holiday_documenso_signing_hr_leave_approve",
            login="admin",
        )
