# Copyright 2025 (APSL-Nagarro) - Antoni Marroig
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class AgreementStage(models.Model):
    _inherit = "agreement.stage"

    name = fields.Char(string="Stage Name", required=True, translate=True)
