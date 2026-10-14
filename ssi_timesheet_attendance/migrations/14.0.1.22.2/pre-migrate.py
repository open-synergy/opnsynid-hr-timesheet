# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
#
# Migration: 14.0.1.22.1 -> 14.0.1.22.2
#
# Changes: ``schedule_source`` moved from ``ssi_timesheet_attendance_shift``
#          to this module (the schedule source is now owned here and the
#          shift module only adds the ``shift`` value). The field keeps its
#          column and its values, but its ``ir_model_data`` rows still name
#          the shift module as owner. They are handed over before this
#          module loads, otherwise the loader would create a second set of
#          rows and the shift module would drop the old ones afterwards.

import logging

from openupgradelib import openupgrade

_logger = logging.getLogger(__name__)

# Every model that carries the field: the stored one, the abstract base
# it comes from, and the read-only public view that inherits the base.
_MODELS = (
    "hr.timesheet",
    "hr.employee.base",
    "hr.employee",
    "hr.employee.public",
)


@openupgrade.migrate()
def migrate(env, version):
    """Hand ``schedule_source`` over from the shift module to this one.

    :param env: the migration environment
    :param version: the version being migrated to (unused)
    :return: nothing; updates ``ir_model_data`` rows
    """
    for model in _MODELS:
        openupgrade.update_module_moved_fields(
            env.cr,
            model,
            ["schedule_source"],
            "ssi_timesheet_attendance_shift",
            "ssi_timesheet_attendance",
        )
        _logger.info("Moved schedule_source of %s to ssi_timesheet_attendance.", model)
