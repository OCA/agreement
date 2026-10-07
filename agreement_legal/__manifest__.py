# Copyright (C) 2018 - TODAY, Pavlov Media
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Agreements Legal",
    "summary": "Manage Agreements, LOI and Contracts",
    "author": "Pavlov Media, "
    "Gray Matter Logic, "
    "Yves Goldberg (Ygol Internetwork), "
    "Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/agreement",
    "category": "Partner",
    "license": "AGPL-3",
    "version": "19.0.1.0.0",
    "depends": ["contacts", "agreement", "product", "web"],
    "data": [
        "data/cron.xml",
        "data/ir_sequence.xml",
        "data/agreement_stage.xml",
        "data/agreement_type.xml",
        "security/ir.model.access.csv",
        "report/agreement.xml",
        "views/res_config_settings.xml",
        "views/agreement_appendix.xml",
        "views/agreement_clause.xml",
        "views/agreement_recital.xml",
        "views/agreement_section.xml",
        "views/agreement_stages.xml",
        "views/agreement_type.xml",
        "views/agreement_subtype.xml",
        "views/agreement.xml",
        "views/menu.xml",
        "wizards/create_agreement_wizard.xml",
        "wizards/recompute_agreement_from_template_wizard.xml",
    ],
    "demo": [
        "demo/agreement_subtype.xml",
        "demo/agreement.xml",
        "demo/agreement_recital.xml",
        "demo/agreement_section.xml",
        "demo/agreement_clause.xml",
        "demo/agreement_appendix.xml",
        "demo/agreement_line.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "agreement_legal/static/src/js/**/*",
            "agreement_legal/static/src/xml/**/*",
        ],
    },
    "installable": True,
    "application": True,
    "uninstall_hook": "uninstall_hook",
    "development_status": "Beta",
    "maintainers": ["max3903", "ygol"],
}
