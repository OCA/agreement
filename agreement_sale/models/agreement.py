# Copyright 2024 - TODAY, Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class Agreement(models.Model):
    _inherit = "agreement"

    sale_order_count = fields.Integer(
        compute="_compute_sale_order_count", string="# Sale Orders"
    )

    def _compute_sale_order_count(self):
        for agreement in self:
            agreement.sale_order_count = self.env["sale.order"].search_count(
                [("agreement_id", "=", agreement.id)]
            )

    def action_view_sale_order(self):
        for agreement in self:
            sale_order_ids = self.env["sale.order"].search(
                [("agreement_id", "=", agreement.id)]
            )
            action = self.env["ir.actions.act_window"]._for_xml_id(
                "sale.action_quotations"
            )
            if len(sale_order_ids) == 1:
                action["views"] = [(self.env.ref("sale.view_order_form").id, "form")]
                action["res_id"] = sale_order_ids.ids[0]
            else:
                action["domain"] = [("id", "in", sale_order_ids.ids)]
            return action
