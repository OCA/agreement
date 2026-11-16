# © 2017 Akretion (Alexis de Lattre <alexis.delattre@akretion.com>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    agreement_id = fields.Many2one(
        comodel_name="agreement",
        ondelete="restrict",
        tracking=True,
        copy=False,
    )

    agreement_type_id = fields.Many2one(
        comodel_name="agreement.type",
        ondelete="restrict",
        tracking=True,
    )
