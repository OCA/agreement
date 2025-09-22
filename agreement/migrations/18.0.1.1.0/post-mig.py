from openupgradelib import openupgrade


def migrate(cr, version):
    openupgrade.update_module_moved_fields(
        cr,
        "res.partner",
        ["agreement_ids", "agreements_count"],
        "agreement_legal",
        "agreement",
    )
