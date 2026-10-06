# Copyright (C) 2018 - TODAY, Pavlov Media
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Agreement Stage",
    "summary": "Add a stage workflow to legal agreements",
    "author": "Pavlov Media, "
    "Open Source Integrators, "
    "Yves Goldberg (Ygol Internetwork), "
    "Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/agreement",
    "category": "Partner",
    "license": "AGPL-3",
    "version": "19.0.1.0.0",
    "depends": ["agreement"],
    "excludes": ["agreement_legal"],
    "data": [
        "security/ir.model.access.csv",
        "data/agreement_stage.xml",
        "views/agreement_stages.xml",
        "views/agreement.xml",
        "views/menu.xml",
    ],
    "development_status": "Beta",
    "maintainers": ["max3903", "ygol"],
}
