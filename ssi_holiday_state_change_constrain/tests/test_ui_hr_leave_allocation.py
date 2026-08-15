# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

# HttpSavepointCase — BUKAN HttpCase. In 14.0, plain HttpCase does not
# set up cls.env in setUpClass; HttpSavepointCase does.
from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiHrLeaveAllocation(HttpSavepointCase):
    """Tour tests for the ``hr.leave_allocation`` state change constrain
    delta."""

    @classmethod
    def setUpClass(cls):
        """Grant the Viewer group the Leave Allocations menu requires."""
        super().setUpClass()
        # Pre-Condition: the Leave Allocations menu is gated by
        # hr_leave_allocation_viewer_group. Without it the tour dies on
        # its first step — the menu is never rendered.
        cls.env.ref("ssi_hr_holiday.hr_leave_allocation_viewer_group").sudo().write(
            {"users": [(4, cls.env.ref("base.user_admin").id)]}
        )

    def test_create(self):
        """Run the create delta tour for ``hr.leave_allocation``.

        IK: docs/hr_leave_allocation/01-create.md
        """
        self.start_tour(
            "/web",
            "ssi_holiday_state_change_constrain_hr_leave_allocation_create",
            login="admin",
        )
