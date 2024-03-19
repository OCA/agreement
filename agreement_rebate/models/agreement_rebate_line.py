# Copyright 2020 Tecnativa - Carlos Dauden
# Copyright 2020 Tecnativa - Sergio Teruel
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, fields, models


class AgreementRebateLine(models.Model):
    _name = "agreement.rebate.line"
    _description = "Agreement Rebate Lines"

    agreement_id = fields.Many2one(comodel_name="agreement", string="Agreement")
    rebate_target = fields.Selection(
        [
            ("product", "Product variant"),
            ("product_tmpl", "Product templates"),
            ("category", "Product categories"),
            ("condition", "Rebate condition"),
            ("domain", "Rebate domain"),
        ]
    )
    rebate_product_ids = fields.Many2many(
        comodel_name="product.product",
        string="Products",
    )
    rebate_product_tmpl_ids = fields.Many2many(
        comodel_name="product.template",
        string="Product templates",
    )
    rebate_category_ids = fields.Many2many(
        comodel_name="product.category",
        string="Product categories",
    )
    rebate_condition_id = fields.Many2one(
        comodel_name="agreement.rebate.condition",
        string="Rebate condition",
    )
    rebate_domain = fields.Char(
        compute="_compute_rebate_domain",
        store=True,
        readonly=False,
    )
    rebate_discount = fields.Float()

    @api.depends(
        "rebate_target",
        "rebate_product_ids",
        "rebate_product_tmpl_ids",
        "rebate_category_ids",
        "rebate_condition_id",
    )
    def _compute_rebate_domain(self):
        for line in self:
            rebate_domain = []
            if line.rebate_target == "product":
                rebate_domain = [("product_id", "in", line.rebate_product_ids.ids)]
            elif line.rebate_target == "product_tmpl":
                rebate_domain = [
                    (
                        "product_id.product_tmpl_id",
                        "in",
                        line.rebate_product_tmpl_ids.ids,
                    )
                ]
            elif line.rebate_target == "category":
                rebate_domain = [
                    ("product_id.categ_id", "in", line.rebate_category_ids.ids)
                ]
            elif line.rebate_target == "condition":
                rebate_domain = line.rebate_condition_id.rebate_domain or []
            line.rebate_domain = str(rebate_domain)
