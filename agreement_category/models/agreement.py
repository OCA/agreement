from odoo import fields, models


class Agreement(models.Model):
    _inherit = "agreement"

    category_ids = fields.Many2many(
        "agreement.category",
        column1="agreement_id",
        column2="category_id",
        string="Tags",
        tracking=True,
        help="Classify the agreement with as many tags as needed.",
    )
