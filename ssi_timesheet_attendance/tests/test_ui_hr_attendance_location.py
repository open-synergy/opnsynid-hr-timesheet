# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiHrAttendanceLocation(HttpSavepointCase):
    """Tour tests for the ``hr.attendance_location`` work instructions.

    Uses ``HttpSavepointCase`` rather than plain ``HttpCase``: in 14.0
    ``TransactionCase`` only assigns ``self.env`` inside instance
    ``setUp()``, so ``cls.env`` is not available in ``setUpClass()``.
    ``HttpSavepointCase`` (via ``SingleTransactionCase``) does set
    ``cls.env`` in ``setUpClass()``, which the tours below rely on to
    seed locations visible to the browser session.
    """

    @classmethod
    def setUpClass(cls):
        """Grant the configurator group and seed one location per tour.

        Pre-Condition common to every ``hr_attendance_location`` IK:
        the actor is in group *Attendance Location* — without it the
        Attendance Locations menu is never rendered for "admin" and
        every tour dies on its first step. The group is already
        granted to ``admin`` by this module's own security data
        (``security/res_group_data.xml``); the explicit grant below is
        defensive and mirrors the pattern used by every other tour
        suite in this repo.
        """
        super().setUpClass()
        cls.env.ref(
            "ssi_timesheet_attendance.hr_attendance_location_group"
        ).sudo().write({"users": [(4, cls.env.ref("base.user_admin").id)]})

        location_model = cls.env["hr.attendance_location"]

        cls.location_edit = location_model.create(
            {
                "name": "TOUR-LOCATION-EDIT-UI",
                "code": "LOCATION-EDIT",
                "latitude": -6.9,
                "longitude": 107.6,
            }
        )
        cls.location_delete = location_model.create(
            {
                "name": "TOUR-LOCATION-DELETE-UI",
                "code": "LOCATION-DELETE",
                "latitude": -6.9,
                "longitude": 107.6,
            }
        )
        cls.location_deactivate = location_model.create(
            {
                "name": "TOUR-LOCATION-DEACTIVATE-UI",
                "code": "LOCATION-DEACT",
                "latitude": -6.9,
                "longitude": 107.6,
            }
        )
        cls.location_activate = location_model.create(
            {
                "name": "TOUR-LOCATION-ACTIVATE-UI",
                "code": "LOCATION-ACT",
                "latitude": -6.9,
                "longitude": 107.6,
                "active": False,
            }
        )
        cls.location_reset_code = location_model.create(
            {
                "name": "TOUR-LOCATION-RESETCODE-UI",
                "code": "OLDCODE99",
                "latitude": -6.9,
                "longitude": 107.6,
            }
        )

    def test_create(self):
        """Run the create tour for ``hr.attendance_location``.

        IK: docs/hr_attendance_location/01-create.md
        """
        self.start_tour(
            "/web",
            "ssi_timesheet_attendance_hr_attendance_location_create",
            login="admin",
        )

    def test_edit(self):
        """Run the edit tour for ``hr.attendance_location``.

        IK: docs/hr_attendance_location/02-edit.md
        """
        self.start_tour(
            "/web",
            "ssi_timesheet_attendance_hr_attendance_location_edit",
            login="admin",
        )

    def test_delete(self):
        """Run the delete tour for ``hr.attendance_location``.

        IK: docs/hr_attendance_location/03-delete.md
        """
        self.start_tour(
            "/web",
            "ssi_timesheet_attendance_hr_attendance_location_delete",
            login="admin",
        )

    def test_deactivate(self):
        """Run the deactivate tour for ``hr.attendance_location``.

        IK: docs/hr_attendance_location/04-deactivate.md
        """
        self.start_tour(
            "/web",
            "ssi_timesheet_attendance_hr_attendance_location_deactivate",
            login="admin",
        )

    def test_activate(self):
        """Run the activate tour for ``hr.attendance_location``.

        IK: docs/hr_attendance_location/05-activate.md
        """
        self.start_tour(
            "/web",
            "ssi_timesheet_attendance_hr_attendance_location_activate",
            login="admin",
        )

    def test_reset_code(self):
        """Run the reset code tour for ``hr.attendance_location``.

        IK: docs/hr_attendance_location/06-reset-code.md
        """
        self.start_tour(
            "/web",
            "ssi_timesheet_attendance_hr_attendance_location_reset_code",
            login="admin",
        )
