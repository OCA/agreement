# Copyright 2026 Christopher Rogos
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    # Pre-create the new ``user_id`` column so the ORM does not fill existing
    # agreements with the field default (the current user). Existing records
    # keep an empty responsible user.
    openupgrade.logged_query(
        env.cr,
        """
        ALTER TABLE agreement
        ADD COLUMN IF NOT EXISTS user_id INTEGER
        """,
    )
