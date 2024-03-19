# Copyright 2020 Tecnativa - Carlos Dauden
# Copyright 2020 Tecnativa - Sergio Teruel
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import _, api, fields, models
from odoo.osv import expression
from odoo.tools.safe_eval import safe_eval


class AgreementRebateSettlement(models.Model):
    _name = "agreement.rebate.settlement"
    _description = "Agreement Rebate Settlement"
    _order = "date DESC"

    name = fields.Char(required=True, default="/")
    company_id = fields.Many2one(
        comodel_name="res.company",
        string="Company",
        required=True,
        index=True,
        default=lambda self: self.env.company,
    )
    date = fields.Date(default=fields.Date.today)
    date_from = fields.Date()
    date_to = fields.Date()
    partner_id = fields.Many2one(
        comodel_name="res.partner",
        string="Partner",
    )
    line_ids = fields.One2many(
        comodel_name="agreement.rebate.settlement.line",
        inverse_name="settlement_id",
        string="Settlement Lines",
    )
    amount_invoiced = fields.Float()
    amount_rebate = fields.Float()
    invoice_id = fields.Many2one(comodel_name="account.move", string="Invoice")
    active = fields.Boolean(default=True)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("name", "/") != "/":
                continue
            vals["name"] = self.env["ir.sequence"].next_by_code(
                "agreement.rebate.settlement"
            )
        return super(AgreementRebateSettlement, self).create(vals_list)

    def write(self, vals):
        res = super().write(vals)
        if "active" in vals and not self.env.context.get(
            "skip_active_field_update", False
        ):
            lines = self.with_context(active_test=False).line_ids.filtered(
                lambda ln: ln.active != vals["active"]
            )
            lines.with_context(skip_active_field_update=True).active = vals["active"]
        return res

    def _reverse_type_map(self, inv_type):
        return {
            "out_invoice": "out_refund",
            "out_refund": "out_invoice",
            "in_invoice": "in_refund",
            "in_refund": "in_invoice",
        }.get(inv_type)

    def create_invoice(self):
        invoice_dic = {}
        for line in self.mapped("line_ids"):
            key = line._get_invoice_key()
            if key not in invoice_dic:
                invoice_dic[key] = line._prepare_invoice()
                invoice_dic[key]["processed_settlements"] = line.settlement_id
                invoice_dic[key]["check_amount"] = 0.0
            elif line.settlement_id not in invoice_dic[key]["processed_settlements"]:
                invoice_dic[key]["invoice_origin"] = "{}, {}".format(
                    invoice_dic[key]["invoice_origin"], line.settlement_id.name
                )
                invoice_dic[key]["processed_settlements"] |= line.settlement_id
            inv_line_vals = line._prepare_invoice_line(invoice_dic[key])
            invoice_dic[key]["invoice_line_ids"].append((0, 0, inv_line_vals))
            invoice_dic[key]["check_amount"] += line.amount_invoiced
        for values in invoice_dic.values():
            values.pop("processed_settlements", None)
            values.pop("line_ids", None)
            if values.pop("check_amount", 0.0) < 0.0:
                for line_vals in values["invoice_line_ids"]:
                    line_vals[2]["price_unit"] *= -1
                values["move_type"] = self._reverse_type_map(values["move_type"])
        invoices = self.env["account.move"].create(invoice_dic.values())
        return invoices

    def action_show_detail(self):
        target_domains = self.line_ids.mapped("target_domain")
        domain = expression.OR([safe_eval(d) for d in set(target_domains)])
        return {
            "name": _("Details"),
            "type": "ir.actions.act_window",
            "res_model": "account.invoice.report",
            "view_mode": "pivot,tree",
            "domain": domain,
            "context": self.env.context,
        }

    def action_show_settlement(self):
        action = self.env["ir.actions.act_window"]._for_xml_id(
            "agreement_rebate.agreement_rebate_settlement_action"
        )
        if len(self) == 1:
            form = self.env.ref("agreement_rebate.agreement_rebate_settlement_view_form")
            action["views"] = [(form.id, "form")]
            action["res_id"] = self.id
        else:
            action["domain"] = [("id", "in", self.ids)]
        return action

    def action_show_settlement_lines(self):
        action = self.env["ir.actions.act_window"]._for_xml_id(
            "agreement_rebate.agreement_rebate_settlement_line_action"
        )
        action["domain"] = [("settlement_id", "in", self.ids)]
        return action

    def action_show_agreement(self):
        agreements = self.line_ids.mapped("agreement_id")
        action = self.env["ir.actions.act_window"]._for_xml_id(
            "agreement.agreement_action"
        )
        if len(agreements) == 1:
            form = self.env.ref("agreement.agreement_view_form")
            action["views"] = [(form.id, "form")]
            action["res_id"] = agreements.id
        else:
            action["domain"] = [("id", "in", agreements.ids)]
        return action
