# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
#
# Migration: 14.0.1.4.1 -> 14.0.1.4.2
#
# Changes: ``schedule_source`` moved to ``ssi_timesheet_attendance``, which
#          now shows it on the employee form itself. The employee view that
#          this module used to add it (``hr_employee_view_shift_form``) is
#          removed from the code, so its record is deleted here instead of
#          being left to the loader.

import logging

from openupgradelib import openupgrade

_logger = logging.getLogger(__name__)


@openupgrade.migrate()
def migrate(env, version):
    """Delete the employee view that the shift module no longer ships.

    :param env: the migration environment
    :param version: the version being migrated to (unused)
    :return: nothing; deletes the ``ir.ui.view`` record when it exists
    """
    openupgrade.delete_records_safely_by_xml_id(
        env,
        ["ssi_timesheet_attendance_shift.hr_employee_view_shift_form"],
    )
    _logger.info("Deleted view hr_employee_view_shift_form.")
