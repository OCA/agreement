# Copyright (C) 2022 Rafnix Guzman
# Copyright (C) 2026 Pop Solutions
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Agreement Portal",
    "summary": "Let portal users see their agreements",
    "version": "18.0.1.0.0",
    "license": "AGPL-3",
    "website": "https://github.com/OCA/agreement",
    "category": "Contract",
    "author": "Pop Solutions, Odoo Community Association (OCA)",
    "maintainers": ["marcos-mendez"],
    "depends": ["portal", "agreement"],
    "data": [
        "security/ir.model.access.csv",
        "security/agreement_security.xml",
        "views/agreement_portal_templates.xml",
    ],
}
