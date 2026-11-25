# Copyright (C) 2018 - TODAY, Pavlov Media
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Agreements Legal - Products/Services",
    "summary": "Add products and services to agreements",
    "author": "Pavlov Media, Open Source Integrators, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/agreement",
    "category": "Partner",
    "license": "AGPL-3",
    "version": "19.0.1.0.0",
    "depends": ["agreement", "agreement_template", "product"],
    "excludes": ["agreement_legal"],
    "data": [
        "security/ir.model.access.csv",
        "views/agreement.xml",
        "views/menu.xml",
        "wizards/recompute_agreement_from_template_wizard.xml",
    ],
    "development_status": "Beta",
}
