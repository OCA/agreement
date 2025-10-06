# Copyright 2020 - TODAY, Open Source Integrators
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Agreement Helpdesk Mgmt",
    "summary": """
            Link a helpdesk ticket to an agreement""",
    "version": "18.0.1.0.0",
    "license": "AGPL-3",
    "author": "Open Source Integrators,Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/agreement",
    "images": ["static/description/banner.png"],
    "depends": [
        "agreement",
        "helpdesk_mgmt",
    ],
    "data": [
        "views/helpdesk_ticket.xml",
        "views/agreement.xml",
    ],
    "maintainers": ["bodedra"],
}
