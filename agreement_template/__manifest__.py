# Copyright (C) 2018 - TODAY, Pavlov Media
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Agreement Template",
    "summary": "Template features for agreements",
    "author": "Pavlov Media, "
    "Open Source Integrators, "
    "Yves Goldberg (Ygol Internetwork), "
    "Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/agreement",
    "category": "Partner",
    "license": "AGPL-3",
    "version": "19.0.1.0.0",
    "depends": ["agreement", "web"],
    "excludes": ["agreement_legal"],
    "data": [
        "security/ir.model.access.csv",
        "wizards/create_agreement_wizard.xml",
        "wizards/recompute_agreement_from_template_wizard.xml",
        "views/agreement.xml",
    ],
    "demo": ["demo/agreement_template_demo.xml"],
    "development_status": "Beta",
    "maintainers": ["max3903", "ygol"],
}
