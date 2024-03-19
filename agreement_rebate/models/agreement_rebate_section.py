# Copyright 2020 Tecnativa - Carlos Dauden
# Copyright 2020 Tecnativa - Sergio Teruel
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, fields, models


class AgreementRebateSection(models.Model):
    _name = "agreement.rebate.section"
    _description = "Agreement Rebate Section"

    agreement_id = fields.Many2one(comodel_name="agreement", string="Agreement")
    amount_from = fields.Float(string="From")
    amount_to = fields.Float(string="To")
    rebate_discount = fields.Float(string="% Dto")
