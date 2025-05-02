# Copyright 2025 (APSL-Nagarro) - Antoni Marroig
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class AgreementSubtype(models.Model):
    _inherit = "agreement.subtype"

    name = fields.Char(string="Sub-Type Name", required=True, translate=True)
