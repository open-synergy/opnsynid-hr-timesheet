# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiHrTimesheetWorkLogMixin(HttpSavepointCase):
    """Tour test for the ``hr.timesheet`` Work Log extension.

    Covers the ``## Additional Fields`` delta this module adds to the
    base ``hr.timesheet`` Create work instruction (arketipe E1 — see
    the tour file's own header comment). Uses ``HttpSavepointCase``
    rather than plain ``HttpCase`` for the same reason as every other
    tour test in this repo: in 14.0 ``TransactionCase`` only assigns
    ``self.env`` inside instance ``setUp()``, not ``setUpClass()``.
    """

    def test_create(self):
        """Run the Work Log delta tour for ``hr.timesheet`` Create.

        IK: docs/hr_timesheet/01-create.md
        """
        self.start_tour("/web", "ssi_work_log_mixin_hr_timesheet_create", login="admin")
