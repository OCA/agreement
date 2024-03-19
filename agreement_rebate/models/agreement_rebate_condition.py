# Copyright 2020 Tecnativa - Carlos Dauden
# Copyright 2020 Tecnativa - Sergio Teruel
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, fields, models


class AgreementRebateCondition(models.Model):
    _name = "agreement.rebate.condition"
    _description = "Agreement Rebate Condition"

    name = fields.Char(string="Rebate condition")
    rebate_domain = fields.Char(string="Domain")
