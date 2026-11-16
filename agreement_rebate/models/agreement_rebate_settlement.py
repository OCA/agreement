# Copyright 2020 Tecnativa - Carlos Dauden
# Copyright 2020 Tecnativa - Sergio Teruel
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import Command, api, fields, models
from odoo.fields import Domain
from odoo.tools.safe_eval import safe_eval


class AgreementRebateSettlement(models.Model):
    _name = "agreement.rebate.settlement"
    _description = "Agreement Rebate Settlement"
    _order = "date DESC"

    name = fields.Char(required=True, default="/")
    company_id = fields.Many2one(
        comodel_name="res.company",
        required=True,
        index=True,
        default=lambda self: self.env.company,
    )
    date = fields.Date(default=fields.Date.today)
    date_from = fields.Date()
    date_to = fields.Date()
    partner_id = fields.Many2one(
        comodel_name="res.partner",
    )
    line_ids = fields.One2many(
        comodel_name="agreement.rebate.settlement.line",
        inverse_name="settlement_id",
        string="Settlement Lines",
    )
    amount_invoiced = fields.Float()
    amount_rebate = fields.Float()
    invoice_id = fields.Many2one(comodel_name="account.move")
    active = fields.Boolean(default=True)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("name", "/") != "/":
                continue
            vals["name"] = self.env["ir.sequence"].next_by_code(
                "agreement.rebate.settlement"
            )
        return super().create(vals_list)

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

    def _create_invoices(self, invoice_group="settlement"):
        # Group lines to invoice
        lines_to_invoice = self.line_ids.filtered(
            lambda line: line.invoice_status == "to_invoice"
        )
        lines_by_group = lines_to_invoice.grouped(
            lambda line: line._get_invoice_key(invoice_group)
        )
        # Process each group
        invoice_vals_list = []
        for lines in lines_by_group.values():
            vals = lines[0]._prepare_invoice(invoice_group)
            vals["invoice_line_ids"] = [
                Command.create(line._prepare_invoice_line()) for line in lines
            ]
            # Reverse if the amount is negative
            if sum(lines.mapped("amount_invoiced")) < 0.0:
                vals["move_type"] = self._reverse_type_map(vals["move_type"])
                for line_vals in vals["invoice_line_ids"]:
                    line_vals[2]["price_unit"] *= -1
            invoice_vals_list.append(vals)
        return self.env["account.move"].create(invoice_vals_list)

    def action_show_detail(self):
        target_domains = self.line_ids.mapped("target_domain")
        domain = Domain.OR([safe_eval(d) for d in set(target_domains)])
        return {
            "name": self.env._("Details"),
            "type": "ir.actions.act_window",
            "res_model": "account.invoice.report",
            "view_mode": "pivot,list",
            "domain": domain,
            "context": self.env.context,
        }

    def action_show_settlement(self):
        action = self.env["ir.actions.act_window"]._for_xml_id(
            "agreement_rebate.agreement_rebate_settlement_action"
        )
        if len(self) == 1:
            form = self.env.ref("agreement_rebate.agreement_rebate_settlement_form")
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
            form = self.env.ref("agreement.agreement_form")
            action["views"] = [(form.id, "form")]
            action["res_id"] = agreements.id
        else:
            action["domain"] = [("id", "in", agreements.ids)]
        return action


class AgreementRebateSettlementLine(models.Model):
    _name = "agreement.rebate.settlement.line"
    _description = "Agreement Rebate Settlement Lines"
    _order = "date DESC"

    company_id = fields.Many2one(
        comodel_name="res.company",
        string="Company",
        related="settlement_id.company_id",
    )
    settlement_id = fields.Many2one(
        comodel_name="agreement.rebate.settlement",
        string="Rebate settlement",
        ondelete="cascade",
    )
    date = fields.Date(
        related="settlement_id.date",
        store=True,
    )
    partner_id = fields.Many2one(
        comodel_name="res.partner",
    )
    rebate_line_id = fields.Many2one(
        comodel_name="agreement.rebate.line",
    )
    rebate_section_id = fields.Many2one(
        comodel_name="agreement.rebate.section",
        string="Rebate section",
    )
    target_domain = fields.Char()
    amount_from = fields.Float(string="From", readonly=True)
    amount_to = fields.Float(string="To", readonly=True)
    percent = fields.Float(readonly=True)
    amount_gross = fields.Float()
    amount_invoiced = fields.Float()
    amount_rebate = fields.Float()
    agreement_id = fields.Many2one(
        comodel_name="agreement",
        required=True,
    )
    rebate_type = fields.Selection(
        related="agreement_id.rebate_type",
        string="Rebate type",
    )
    invoice_line_ids = fields.Many2many(
        comodel_name="account.move.line",
        relation="agreement_rebate_settlement_line_account_invoice_line_rel",
        column1="settlement_line_id",
        column2="invoice_line_id",
        string="Invoice lines",
    )
    invoice_status = fields.Selection(
        [
            ("invoiced", "Fully Invoiced"),
            ("to_invoice", "To Invoice"),
            ("no", "Nothing to Invoice"),
        ],
        compute="_compute_invoice_status",
        store=True,
        readonly=False,
    )
    active = fields.Boolean(default=True)

    @api.depends(
        "invoice_line_ids",
        "invoice_line_ids.parent_state",
        "invoice_line_ids.refund_line_ids",
    )
    def _compute_invoice_status(self):
        for line in self:
            if line.invoice_status == "no":
                continue
            invoice_lines = line.invoice_line_ids.filtered(
                lambda ln: ln.parent_state != "cancel"
            )
            refund_lines = invoice_lines.refund_line_ids.filtered(
                lambda ln: ln.parent_state != "cancel"
            )
            if invoice_lines and not refund_lines:
                line.invoice_status = "invoiced"
            else:
                line.invoice_status = "to_invoice"

    def write(self, vals):
        res = super().write(vals)
        if "active" in vals and not self.env.context.get(
            "skip_active_field_update", False
        ):
            if vals["active"]:
                # If one line is active settlement must be active
                settlements = self.mapped("settlement_id").filtered(
                    lambda s: not s.active
                )
            else:
                # If lines are archived and the settlement has not active lines, the
                # settlement must be archived
                settlements = self.mapped("settlement_id").filtered(
                    lambda s: s.active and not s.line_ids
                )
            settlements.with_context(skip_active_field_update=True).active = vals[
                "active"
            ]
        return res

    def _prepare_invoice(self, invoice_group="settlement"):
        """
        Prepare the dict of values to create the new invoice for a sales order.
        This method may be overridden to implement custom invoice generation
        (making sure to call super() to establish a clean extension chain).
        """
        self.ensure_one()
        company = self.company_id or self.env.user.company_id
        partner_id = self.env.context.get("default_partner_id", False)
        if not partner_id:
            if invoice_group == "settlement":
                partner_id = self.settlement_id.partner_id.id
            elif invoice_group == "partner":
                partner_id = self.partner_id.id
            elif invoice_group == "commercial_partner":
                partner_id = self.partner_id.commercial_partner_id.id
        return {
            "company_id": company.id,
            "partner_id": partner_id,
            "move_type": self.env.context.get("default_move_type", "out_invoice"),
            "ref": (self.agreement_id.name or ""),
            "invoice_origin": self.settlement_id.name,
        }

    def _prepare_invoice_line(self):
        self.ensure_one()
        return {
            "agreement_rebate_settlement_line_ids": [Command.set(self.ids)],
            "product_id": self.env.context.get("default_product_id", False),
            "price_unit": self.amount_rebate,
        }

    def _get_invoice_key(self, invoice_group="settlement"):
        if self.env.context.get("default_partner_id"):
            return self.env.context["default_partner_id"]
        if invoice_group == "settlement":
            return self.settlement_id.id
        if invoice_group == "partner":
            return self.partner_id.id
        if invoice_group == "commercial_partner":
            return self.partner_id.commercial_partner_id.id

    def action_show_detail(self):
        return {
            "name": self.env._("Details"),
            "type": "ir.actions.act_window",
            "res_model": "account.invoice.report",
            "view_mode": "pivot,list",
            "domain": self.target_domain,
            "context": self.env.context,
        }
