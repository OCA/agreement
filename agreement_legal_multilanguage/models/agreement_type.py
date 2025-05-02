# Copyright 2025 (APSL-Nagarro) - Antoni Marroig
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class AgreementType(models.Model):
    _inherit = "agreement.type"

    name = fields.Char(required=True, translate=True)
