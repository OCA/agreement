# Copyright (C) 2018 - TODAY, Pavlov Media
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Agreement Revision",
    "summary": "Track versions and revisions of legal agreements",
    "author": "Pavlov Media, "
    "Open Source Integrators, "
    "Yves Goldberg (Ygol Internetwork), "
    "Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/agreement",
    "category": "Partner",
    "license": "AGPL-3",
    "version": "19.0.1.0.0",
    "depends": ["agreement", "agreement_template"],
    "excludes": ["agreement_legal"],
    "data": [
        "views/agreement.xml",
        "wizards/recompute_agreement_from_template_wizard.xml",
    ],
    "development_status": "Beta",
    "maintainers": ["max3903", "ygol"],
}
