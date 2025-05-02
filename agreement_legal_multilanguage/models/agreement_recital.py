# Copyright 2025 (APSL-Nagarro) - Antoni Marroig
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class AgreementRecital(models.Model):
    _inherit = "agreement.recital"

    name = fields.Char(required=True, translate=True)
    title = fields.Char(
        help="The title is displayed on the PDF. The name is not.", translate=True
    )
    content = fields.Html(translate=True)
    default_value = fields.Char(
        help="Optional value to use if the target field is empty.", translate=True
    )
    copyvalue = fields.Char(
        string="Placeholder Expression",
        help="""Final placeholder expression, to be copy-pasted in the desired
         template field.""",
        translate=True,
    )
