from random import randint

from odoo import fields, models


class AgreementCategory(models.Model):
    _name = "agreement.category"
    _description = "Agreement Tags"
    _order = "name"

    def _get_default_color(self):
        return randint(1, 11)

    name = fields.Char(required=True, translate=True)
    color = fields.Integer(
        default=lambda self: self._get_default_color(), aggregator=False
    )
    active = fields.Boolean(
        default=True,
        help="The active field allows you to hide the tag without removing it.",
    )
    agreement_ids = fields.Many2many(
        "agreement",
        column1="category_id",
        column2="agreement_id",
        string="Agreements",
        copy=False,
    )
