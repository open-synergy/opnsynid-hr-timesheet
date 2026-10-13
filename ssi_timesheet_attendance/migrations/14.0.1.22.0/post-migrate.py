# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
#
# Migration: 14.0.1.21.0 -> 14.0.1.22.0
#
# Changes: ``res.company.checkout_buffer`` is now also the tolerance of
#          the schedule window used to match an attendance to a slot,
#          and it defaults to 3.0. Companies still holding the old
#          implicit value (NULL or 0.0) would reject nearly every
#          attendance, so they are moved to the new default. Other
#          values were chosen on purpose and are left alone.
#          ``checkin_buffer`` is a new column filled by its default.

import logging

from openupgradelib import openupgrade

_logger = logging.getLogger(__name__)


@openupgrade.migrate()
def migrate(env, version):
    """Set ``checkout_buffer`` to 3.0 where it is NULL or 0.0.

    :param env: the migration environment
    :param version: the version being migrated to (unused)
    :return: nothing; updates ``res_company`` rows
    """
    rows = openupgrade.logged_query(
        env.cr,
        """
        UPDATE res_company
        SET checkout_buffer = %s
        WHERE checkout_buffer IS NULL OR checkout_buffer = 0
        """,
        (3.0,),
    )
    _logger.info("Set checkout_buffer=3.0 on %s company row(s).", rows)
