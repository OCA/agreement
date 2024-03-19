# Copyright 2020 Tecnativa - Carlos Dauden
# Copyright 2020 Tecnativa - Sergio Teruel
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, fields, models


class Agreement(models.Model):
    _inherit = "agreement"

    rebate_type = fields.Selection(
        selection=[
            ("global", "Global (A discount global for all lines)"),
            ("line", "Line (A discount for every line)"),
            ("section_total", "Compute total and apply discount rule match"),
            ("section_prorated", "Calculate the discount in each amount section"),
        ],
        string="rebate type",
    )
    rebate_line_ids = fields.One2many(
        comodel_name="agreement.rebate.line",
        string="Agreement rebate lines",
        inverse_name="agreement_id",
        copy=True,
    )
    rebate_section_ids = fields.One2many(
        comodel_name="agreement.rebate.section",
        string="Agreement rebate sections",
        inverse_name="agreement_id",
        copy=True,
    )
    rebate_discount = fields.Float(digits="Discount", default=0.0)
    is_rebate = fields.Boolean(
        related="agreement_type_id.is_rebate", string="Is rebate agreement type"
    )
    additional_consumption = fields.Float(default=0.0)
