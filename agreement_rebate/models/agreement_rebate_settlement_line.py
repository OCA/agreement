# Copyright 2020 Tecnativa - Carlos Dauden
# Copyright 2020 Tecnativa - Sergio Teruel
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import _, api, fields, models
from odoo.exceptions import UserError


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
        string="Partner",
    )
    rebate_line_id = fields.Many2one(
        comodel_name="agreement.rebate.line",
        string="Rebate Line",
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
        string="Agreement",
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

    def _prepare_invoice(self):
        """
        Prepare the dict of values to create the new invoice for a sales order.
        This method may be overridden to implement custom invoice generation
        (making sure to call super() to establish a clean extension chain).
        """
        self.ensure_one()
        company = self.company_id or self.env.user.company_id
        partner = self.env.context.get("partner_invoice", False)
        if not partner:
            invoice_group = self.env.context.get("invoice_group", "settlement")
            if invoice_group == "settlement":
                partner = self.settlement_id.partner_id
            elif invoice_group == "partner":
                partner = self.partner_id
            elif invoice_group == "commercial_partner":
                partner = self.partner_id.commercial_partner_id
        invoice_type = self.env.context.get("invoice_type", "out_invoice")
        journal_id = (
            self.env.context.get("journal_id")
            or self.env["account.move"]
            .with_company(company=company)
            .default_get(["journal_id"])["journal_id"]
        )
        if not journal_id:
            raise UserError(
                _("Please define an accounting sales journal for this company.")
            )
        vinvoice = self.env["account.move"].new(
            {
                "company_id": company.id,
                "partner_id": partner.id,
                "move_type": invoice_type,
                "journal_id": journal_id,
            }
        )
        # Get partner extra fields
        vinvoice._onchange_partner_id()
        invoice_vals = vinvoice._convert_to_write(vinvoice._cache)
        invoice_vals.update(
            {
                "ref": (self.agreement_id.name or ""),
                "invoice_origin": self.settlement_id.name,
                "invoice_line_ids": [],
                "currency_id": partner.currency_id.id,
                # 'comment': self.note,
                # 'user_id': self.user_id and self.user_id.id,
                # 'team_id': self.team_id.id,
            }
        )
        return invoice_vals

    def _prepare_invoice_line(self, invoice_vals):
        self.ensure_one()
        company = self.company_id or self.env.user.company_id
        product = self.env.context.get("product", False)
        invoice_line_vals = {
            "product_id": product.id,
            "quantity": 1.0,
            "product_uom_id": product.uom_id.id,
            "agreement_rebate_settlement_line_ids": [(4, self.id)],
        }
        invoice_line = (
            self.env["account.move.line"]
            .with_company(company=company)
            .new(invoice_line_vals)
        )
        invoice_vals_new = invoice_vals.copy()
        invoice_vals_new.pop("processed_settlements", None)
        invoice_vals_new.pop("check_amount", None)
        invoice = (
            self.env["account.move"]
            .with_company(
                company=company,
            )
            .new(invoice_vals_new)
        )
        invoice_line.move_id = invoice
        # Compute invoice line's name field
        invoice_line._compute_name()
        invoice_line_vals = invoice_line._convert_to_write(invoice_line._cache)
        invoice_line_vals.update(
            {
                "name": _(
                    "%(name)s - Period: %(date_from)s - %(date_to)s",
                    name=invoice_line_vals["name"],
                    date_from=self.settlement_id.date_from,
                    date_to=self.settlement_id.date_to,
                ),
                # 'account_analytic_id': self.analytic_account_id.id,
                # 'analytic_tag_ids': [(6, 0, self.analytic_tag_ids.ids)],
                "price_unit": self.amount_rebate,
            }
        )
        return invoice_line_vals

    def _get_invoice_key(self):
        invoice_group = self.env.context.get("invoice_group", "settlement")
        if invoice_group == "settlement":
            return self.settlement_id.id
        if invoice_group == "partner":
            return self.env.context.get("partner_id", self.partner_id.id)
        if invoice_group == "commercial_partner":
            return self.env.context.get(
                "partner_id", self.partner_id.commercial_partner_id.id
            )

    def action_show_detail(self):
        return {
            "name": _("Details"),
            "type": "ir.actions.act_window",
            "res_model": "account.invoice.report",
            "view_mode": "pivot,tree",
            "domain": self.target_domain,
            "context": self.env.context,
        }
