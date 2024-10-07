from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    openupgrade.logged_query(
        env.cr,
        """UPDATE product_template SET detailed_type = 'serviceprofile'
        WHERE is_service_profile IS TRUE""",
    )
