# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiWorkLogExpense(HttpSavepointCase):
    """Tour tests for the ``work_log_expense`` work instructions.

    Uses ``HttpSavepointCase`` rather than plain ``HttpCase``: in 14.0
    ``TransactionCase`` only assigns ``self.env`` inside instance
    ``setUp()``, so ``cls.env`` is not available in ``setUpClass()``.
    ``HttpSavepointCase`` (via ``SingleTransactionCase``) does set
    ``cls.env`` in ``setUpClass()``, which the tours below rely on to
    seed the expense type and the draft expenses the browser session
    has to find.
    """

    @classmethod
    def setUpClass(cls):
        """Seed the expense type and one draft expense per tour.

        Pre-Condition common to every ``work_log_expense`` IK: the actor
        is in group *Work Log Expense — User* and an active
        ``work_log_expense_type`` carrying an Account and a Journal
        exists. ``admin`` already holds *Work Log Expense — Validator*
        (which implies *User*, which implies *Viewer*, the group gating
        the menu) and *Work Log Expense — All* through
        ``security/res_group_data.xml``, so no group has to be granted
        here.

        The create tour relies on the Employee field being filled by
        ``mixin.employee_document._default_employee_id``, so the tour
        user is guaranteed a linked employee below. The remaining tours
        each get their own employee, whose name is the unique marker
        the tour uses to pick its row out of the list.

        ``user_id`` is set explicitly on every expense: ``cls.env`` runs
        as SUPERUSER, and ``work_log_expense_internal_user_rule``
        (``user_id = user.id``) would otherwise hide the fixtures from
        the tour session. ``accrue_account_id`` and ``journal_id`` are
        set explicitly too, because ``.create()`` never runs the
        ``type_id`` onchange that fills them in the form.
        """
        super().setUpClass()
        cls.admin = cls.env.ref("base.user_admin")
        employee_model = cls.env["hr.employee"]
        expense_model = cls.env["work_log_expense"]

        # The create tour never touches the Employee field, because the
        # IK says it is filled automatically from the current user's
        # employee. Reuse the employee CI demo data already links to
        # admin: hr.employee carries a unique(user_id, company_id) SQL
        # constraint, so creating a second one would fail.
        cls.employee_admin = employee_model.search(
            [("user_id", "=", cls.admin.id)], limit=1
        )
        if not cls.employee_admin:
            cls.employee_admin = employee_model.create(
                {"name": "TOUR-WLE-EMP-CREATE", "user_id": cls.admin.id}
            )

        cls.account = cls.env["account.account"].search([], limit=1, order="id asc")
        cls.journal = cls.env["account.journal"].search([], limit=1, order="id asc")
        cls.expense_type = cls.env["work_log_expense_type"].create(
            {
                "name": "TOUR-WLE-TYPE",
                "code": "TWLE01",
                "accrue_account_id": cls.account.id,
                "journal_id": cls.journal.id,
            }
        )

        # --- 02-edit.md: draft expense, still editable.
        cls.employee_edit = employee_model.create({"name": "TOUR-WLE-EMP-EDIT"})
        cls.expense_edit = expense_model.create(
            cls._expense_values(cls.employee_edit, "2026-01-01", "2026-01-31")
        )

        # --- 03-delete.md: draft expense, document number still "/".
        cls.employee_delete = employee_model.create({"name": "TOUR-WLE-EMP-DELETE"})
        cls.expense_delete = expense_model.create(
            cls._expense_values(cls.employee_delete, "2026-02-01", "2026-02-28")
        )

        # --- 04-confirm.md: draft expense waiting to be confirmed.
        cls.employee_confirm = employee_model.create({"name": "TOUR-WLE-EMP-CONFIRM"})
        cls.expense_confirm = expense_model.create(
            cls._expense_values(cls.employee_confirm, "2026-03-01", "2026-03-31")
        )

    @classmethod
    def _expense_values(cls, employee, date_start, date_end):
        """Return the create values of a draft work log expense.

        :param employee: Employee the expense is raised for.
        :type employee: recordset
        :param str date_start: First date of the work log range.
        :param str date_end: Last date of the work log range.
        :return: Values accepted by ``work_log_expense.create()``.
        :rtype: dict
        """
        return {
            "user_id": cls.admin.id,
            "employee_id": employee.id,
            "type_id": cls.expense_type.id,
            "date": date_start,
            "date_start": date_start,
            "date_end": date_end,
            "accrue_account_id": cls.account.id,
            "journal_id": cls.journal.id,
        }

    def test_create(self):
        """Run the create tour for ``work_log_expense``.

        Populate is clicked but its result is only gated on the button
        cycle finishing: no ``hr.work_log`` is seeded, so the action may
        legitimately produce zero lines, and line contents are unit-test
        territory rather than tour territory.

        IK: docs/work_log_expense/01-create.md
        """
        self.start_tour(
            "/web",
            "ssi_work_log_expense_work_log_expense_create",
            login="admin",
        )

    def test_edit(self):
        """Run the edit tour for ``work_log_expense``.

        Populate is clicked under the same limitation described in
        :meth:`test_create`.

        IK: docs/work_log_expense/02-edit.md
        """
        self.start_tour(
            "/web",
            "ssi_work_log_expense_work_log_expense_edit",
            login="admin",
        )

    def test_delete(self):
        """Run the delete tour for ``work_log_expense``.

        The record is selected by opening it and using its own Action
        menu, because the 14.0 list-selector checkbox is unreliable; the
        Post-Condition reached is the one the IK describes.

        IK: docs/work_log_expense/03-delete.md
        """
        self.start_tour(
            "/web",
            "ssi_work_log_expense_work_log_expense_delete",
            login="admin",
        )

    def test_confirm(self):
        """Run the confirm tour for ``work_log_expense``.

        IK: docs/work_log_expense/04-confirm.md
        """
        self.start_tour(
            "/web",
            "ssi_work_log_expense_work_log_expense_confirm",
            login="admin",
        )
