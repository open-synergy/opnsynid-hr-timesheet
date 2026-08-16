# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiWorkLogRate(HttpSavepointCase):
    """Tour tests for the ``work_log_rate`` work instructions.

    Uses ``HttpSavepointCase`` rather than plain ``HttpCase``: in 14.0
    ``TransactionCase`` only assigns ``self.env`` inside instance
    ``setUp()``, so ``cls.env`` is not available in ``setUpClass()``.
    ``HttpSavepointCase`` (via ``SingleTransactionCase``) does set
    ``cls.env`` in ``setUpClass()``, which the tours below rely on to
    seed the employees and work log rates the browser session opens.
    """

    @classmethod
    def setUpClass(cls):
        """Seed one fixture per tour, in the state its IK requires.

        Access is already satisfied by module data and therefore not
        granted here: ``security/res_group_data.xml`` puts
        ``base.user_admin`` in *Work Log Rate — Validator* (which
        implies *User*, which implies *Viewer*, the group gating the
        menu) and in the *All* data-ownership group, so the record rule
        never hides the seeded records from the tour session.

        The create tour also needs a product and a pricelist to pick in
        the *General Rates* tab; both carry tour-specific names so the
        autocomplete dropdown can never resolve to a record shipped by
        another module.
        """
        super().setUpClass()

        employee_model = cls.env["hr.employee"]
        rate_model = cls.env["work_log_rate"]
        cls.rate_model = rate_model

        # --- 01-create.md: the general rate line the tour adds needs a
        # product and a pricelist that exist before the browser starts.
        cls.product = cls.env["product.product"].create({"name": "TOUR-WLR-PRODUCT"})
        cls.pricelist = cls.env["product.pricelist"].create(
            {"name": "TOUR-WLR-PRICELIST"}
        )
        cls.employee_create = employee_model.create({"name": "TOUR-WLR-EMP-CREATE"})

        # --- 02-edit.md: Draft. Date End is seeded to a value the tour
        # does not reuse, so the Post-Condition assertion cannot pass on
        # the fixture value alone. It still has to sit *after* Date Start:
        # mixin.date_duration._check_date_start_end raises "Date end must
        # be greater than date start" whenever date_end < date_start, and
        # the tour's own new value (02/28/2026) obeys the same rule.
        cls.employee_edit = employee_model.create({"name": "TOUR-WLR-EMP-EDIT"})
        cls.rate_edit = rate_model.create(
            cls._rate_values(cls.employee_edit, "2026-02-01", "2026-02-10")
        )

        # --- 03-delete.md: Draft, document number still "/".
        cls.employee_delete = employee_model.create({"name": "TOUR-WLR-EMP-DELETE"})
        cls.rate_delete = rate_model.create(
            cls._rate_values(cls.employee_delete, "2026-03-01", "2026-03-31")
        )

        # --- 04-confirm.md: Draft, confirmed by the tour itself.
        cls.employee_confirm = employee_model.create({"name": "TOUR-WLR-EMP-CONFIRM"})
        cls.rate_confirm = rate_model.create(
            cls._rate_values(cls.employee_confirm, "2026-04-01", "2026-04-30")
        )

    @classmethod
    def _rate_values(cls, employee, date_start, date_end):
        """Build the create values for one draft work log rate.

        Dates are always passed as fixed literals, never derived from
        "today": a relative base makes the fixture cross a month or year
        boundary depending on when CI happens to run.

        :param employee: ``hr.employee`` record the rate applies to.
        :param str date_start: First date the rate is valid for.
        :param str date_end: Last date the rate is valid for. Must not
            be earlier than ``date_start``, or
            ``mixin.date_duration._check_date_start_end`` aborts
            ``setUpClass`` before any tour runs.
        :return: Dict of values accepted by ``work_log_rate.create``.
        """
        return {
            "employee_id": employee.id,
            "date": date_start,
            "date_start": date_start,
            "date_end": date_end,
        }

    def test_create(self):
        """Run the create tour for ``work_log_rate``.

        IK: docs/work_log_rate/01-create.md
        """
        self.start_tour(
            "/web",
            "ssi_work_log_cost_work_log_rate_create",
            login="admin",
        )

    def test_edit(self):
        """Run the edit tour for ``work_log_rate``.

        IK: docs/work_log_rate/02-edit.md
        """
        self.start_tour(
            "/web",
            "ssi_work_log_cost_work_log_rate_edit",
            login="admin",
        )

    def test_delete(self):
        """Run the delete tour for ``work_log_rate``.

        IK: docs/work_log_rate/03-delete.md
        """
        self.start_tour(
            "/web",
            "ssi_work_log_cost_work_log_rate_delete",
            login="admin",
        )

    def test_confirm(self):
        """Run the confirm tour for ``work_log_rate``.

        IK: docs/work_log_rate/04-confirm.md
        """
        self.start_tour(
            "/web",
            "ssi_work_log_cost_work_log_rate_confirm",
            login="admin",
        )
