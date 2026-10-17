# Copyright (C) 2018 - TODAY, Pavlov Media
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Agreement Termination",
    "summary": "Term dates, notices, review reminders and termination tracking for "
    "agreements",
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
        "data/cron.xml",
        "views/agreement.xml",
    ],
    "development_status": "Beta",
}
