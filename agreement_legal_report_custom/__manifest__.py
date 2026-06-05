# Copyright 2026 Moka Tourisme
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Agreement Legal Report Custom",
    "summary": "Custom French QWeb layout for the agreement legal report",
    "version": "16.0.1.0.0",
    "category": "Partner",
    "author": "Moka Tourisme, Odoo Community Association (OCA)",
    "website": "https://github.com/Moka-Tourisme/agreement",
    "license": "AGPL-3",
    "depends": [
        "agreement_legal",
        "l10n_fr_siret",
    ],
    "data": [
        "report/agreement_report.xml",
    ],
    "installable": True,
}
