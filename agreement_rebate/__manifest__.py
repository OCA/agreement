# Copyright 2020 Tecnativa - Carlos Dauden
# Copyright 2020 Tecnativa - Sergio Teruel
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Agreement Rebate",
    "summary": "Rebate in agreements",
    "version": "17.0.1.0.0",
    "development_status": "Beta",
    "category": "Agreement",
    "website": "https://github.com/OCA/agreement",
    "author": "Tecnativa, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": ["account_invoice_refund_link", "agreement"],
    "data": [
        "data/agreement_rebate_settlement_data.xml",
        "security/agreement_rebate_security.xml",
        "security/ir.model.access.csv",
        "views/agreement_rebate_condition_views.xml",
        "views/agreement_rebate_line_views.xml",
        "views/agreement_rebate_section_views.xml",
        "views/agreement_views.xml",
        "views/agreement_rebate_settlement_views.xml",
        "views/agreement_rebate_settlement_line_views.xml",
        "views/agreement_type_views.xml",
        "wizards/agreement_invoice_create_wiz_views.xml",
        "wizards/agreement_settlement_create_wiz_views.xml",
        "views/agreement_menu_views.xml",
    ],
}
