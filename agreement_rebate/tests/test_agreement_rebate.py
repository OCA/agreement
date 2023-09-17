# Copyright 2020 Tecnativa - Carlos Dauden
# Copyright 2020 Tecnativa - Sergio Teruel
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from freezegun import freeze_time

from odoo import fields
from odoo.tests.common import Form, TransactionCase, tagged


@freeze_time("2022-02-01 09:30:00")
@tagged("-at_install", "post_install")
class TestAgreementRebate(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, tracking_disable=True))
        cls.Partner = cls.env["res.partner"]
        cls.ProductTemplate = cls.env["product.template"]
        cls.Product = cls.env["product.product"]
        cls.ProductCategory = cls.env["product.category"]
        cls.AccountInvoice = cls.env["account.move"]
        cls.AccountInvoiceLine = cls.env["account.move.line"]
        cls.AccountJournal = cls.env["account.journal"]
        cls.Agreement = cls.env["agreement"]
        cls.AgreementType = cls.env["agreement.type"]
        cls.ProductAttribute = cls.env["product.attribute"]
        cls.ProductAttributeValue = cls.env["product.attribute.value"]
        cls.ProductTmplAttributeValue = cls.env["product.template.attribute.value"]
        cls.AgreementSettlement = cls.env["agreement.rebate.settlement"]
        cls.AgreementSettlementCreateWiz = cls.env["agreement.settlement.create.wiz"]
        cls.rebate_type = [
            "global",
            "line",
            "section_total",
            "section_prorated",
        ]
        cls.category_all = cls.env.ref("product.product_category_all")
        cls.categ_1 = cls.ProductCategory.create(
            {"parent_id": cls.category_all.id, "name": "Category 1"}
        )
        cls.categ_2 = cls.ProductCategory.create(
            {"parent_id": cls.category_all.id, "name": "Category 2"}
        )
        cls.product_1 = cls.Product.create(
            {
                "name": "Product test 1",
                "categ_id": cls.categ_1.id,
                "list_price": 1000.00,
            }
        )
        cls.product_2 = cls.Product.create(
            {
                "name": "Product test 2",
                "categ_id": cls.categ_2.id,
                "list_price": 2000.00,
            }
        )
        # Create a product with variants
        cls.product_attribute = cls.ProductAttribute.create(
            {"name": "Test", "create_variant": "always"}
        )
        cls.product_attribute_value_test_1 = cls.ProductAttributeValue.create(
            {"name": "Test v1", "attribute_id": cls.product_attribute.id}
        )
        cls.product_attribute_value_test_2 = cls.ProductAttributeValue.create(
            {"name": "Test v2", "attribute_id": cls.product_attribute.id}
        )
        cls.product_template = cls.ProductTemplate.create(
            {
                "name": "Product template with variant test",
                "type": "consu",
                "list_price": 100.0,
                "attribute_line_ids": [
                    (
                        0,
                        0,
                        {
                            "attribute_id": cls.product_attribute.id,
                            "value_ids": [
                                (4, cls.product_attribute_value_test_1.id),
                                (4, cls.product_attribute_value_test_2.id),
                            ],
                        },
                    ),
                ],
            }
        )
        cls.partner_1 = cls.Partner.create(
            {"name": "partner test rebate 1", "ref": "TST-001"}
        )
        cls.partner_2 = cls.Partner.create(
            {"name": "partner test rebate 2", "ref": "TST-002"}
        )
        cls.invoice_partner_1 = cls.create_invoice(cls.partner_1)
        cls.invoice_partner_2 = cls.create_invoice(cls.partner_2)
        cls.agreement_type = cls.AgreementType.create(
            {"name": "Rebate", "domain": "sale", "is_rebate": True}
        )
        # Product to use when we create invoices from settlements
        cls.product_rappel = cls.Product.create(
            {"name": "Rappel sales", "categ_id": cls.categ_1.id, "list_price": 1.00}
        )

    @classmethod
    # Create some invoices for partner
    def create_invoice(cls, partner):
        move_form = Form(
            cls.env["account.move"].with_context(default_move_type="out_invoice")
        )
        move_form.invoice_date = fields.Date.from_string(
            "{}-01-01".format(fields.Date.today().year)
        )
        move_form.ref = "Test Customer Invoice"
        move_form.partner_id = partner
        products = (
            cls.product_template.product_variant_ids + cls.product_1 + cls.product_2
        )
        cls.create_invoice_line(move_form, products)
        invoice = move_form.save()
        invoice.action_post()
        return invoice

    @classmethod
    def create_invoice_line(cls, invoice_form, products):
        for product in products:
            with invoice_form.invoice_line_ids.new() as line_form:
                line_form.product_id = product
                # Assign distinct prices for product with variants
                if product == cls.product_template.product_variant_ids[0]:
                    line_form.price_unit = 300.00
                if product == cls.product_template.product_variant_ids[1]:
                    line_form.price_unit = 500.00

    # Create Agreements rebates for customers for all available types
    def create_agreements_rebate(self, rebate_type, partner):
        agreement = self.Agreement.create(
            {
                "domain": "sale",
                "start_date": "{}-01-01".format(fields.Date.today().year),
                "rebate_type": rebate_type,
                "name": "A discount {} for all lines for {}".format(
                    rebate_type, partner.name
                ),
                "code": "R-{}-{}".format(rebate_type, partner.ref),
                "partner_id": partner.id,
                "agreement_type_id": self.agreement_type.id,
                "rebate_discount": 10,
                "rebate_line_ids": [
                    (
                        0,
                        0,
                        {
                            "rebate_target": "product",
                            "rebate_product_ids": [(6, 0, self.product_1.ids)],
                            "rebate_discount": 20,
                        },
                    ),
                    (
                        0,
                        0,
                        {
                            "rebate_target": "product",
                            "rebate_product_ids": [
                                (6, 0, self.product_template.product_variant_ids[0].ids)
                            ],
                            "rebate_discount": 30,
                        },
                    ),
                    (
                        0,
                        0,
                        {
                            "rebate_target": "product_tmpl",
                            "rebate_product_tmpl_ids": [
                                (6, 0, self.product_2.product_tmpl_id.ids)
                            ],
                            "rebate_discount": 40,
                        },
                    ),
                    (
                        0,
                        0,
                        {
                            "rebate_target": "category",
                            "rebate_category_ids": [(6, 0, self.category_all.ids)],
                            "rebate_discount": 40,
                        },
                    ),
                ],
                "rebate_section_ids": [
                    (
                        0,
                        0,
                        {
                            "amount_from": 0.00,
                            "amount_to": 100.00,
                            "rebate_discount": 10,
                        },
                    ),
                    (
                        0,
                        0,
                        {
                            "amount_from": 100.01,
                            "amount_to": 300.00,
                            "rebate_discount": 20,
                        },
                    ),
                    (
                        0,
                        0,
                        {
                            "amount_from": 300.01,
                            "amount_to": 6000.00,
                            "rebate_discount": 30,
                        },
                    ),
                ],
            }
        )
        return agreement

    def get_settlements_from_action(self, action):
        if action.get("res_id", False):
            return self.AgreementSettlement.browse(action["res_id"])
        else:
            return self.AgreementSettlement.search(action["domain"])

    def create_settlement_wizard(self, agreements=False):
        vals = {
            "date_to": "{}-12-31".format(fields.Date.today().year),
        }
        if agreements:
            vals["agreement_ids"] = [(6, 0, agreements.ids)]
        settlement_wiz = self.AgreementSettlementCreateWiz.create(vals)
        return settlement_wiz

    def test_create_settlement_wo_filters_global(self):
        # Invoice Lines:
        # Product template variants: 300, 500
        # Product 1: 1000
        # Product 2: 2000
        # Total by invoice: 3800 amount invoiced

        # Global rebate without filters
        agreement_global = self.create_agreements_rebate("global", self.partner_1)
        agreement_global.rebate_line_ids = False
        settlement_wiz = self.create_settlement_wizard(agreement_global)
        settlements = self.get_settlements_from_action(
            settlement_wiz.action_create_settlement()
        )
        self.assertEqual(len(settlements), 1)
        self.assertEqual(settlements.amount_invoiced, 3800)
        self.assertEqual(settlements.amount_rebate, 380)

    def test_create_settlement_wo_filters_line(self):
        # Line rebate without filters
        agreement = self.create_agreements_rebate("line", self.partner_1)
        agreement.rebate_line_ids = False
        settlement_wiz = self.create_settlement_wizard(agreement)
        settlements = self.get_settlements_from_action(
            settlement_wiz.action_create_settlement()
        )
        self.assertEqual(len(settlements), 0)

    def test_create_settlement_wo_filters_section_total(self):
        # section_total rebate without filters
        agreement = self.create_agreements_rebate("section_total", self.partner_1)
        agreement.rebate_line_ids = False
        settlement_wiz = self.create_settlement_wizard(agreement)
        settlements = self.get_settlements_from_action(
            settlement_wiz.action_create_settlement()
        )
        self.assertEqual(len(settlements), 1)
        self.assertEqual(settlements.amount_invoiced, 3800)
        self.assertEqual(settlements.amount_rebate, 1140)

    def test_create_settlement_wo_filters_section_prorated(self):
        # section_prorated rebate without filters
        agreement = self.create_agreements_rebate("section_prorated", self.partner_1)
        agreement.rebate_line_ids = False
        settlement_wiz = self.create_settlement_wizard(agreement)
        settlements = self.get_settlements_from_action(
            settlement_wiz.action_create_settlement()
        )
        self.assertEqual(len(settlements), 1)
        self.assertEqual(settlements.amount_invoiced, 3800)
        self.assertAlmostEqual(settlements.amount_rebate, 1120.00, 2)

    def _create_agreement_product_filter(self, agreement_type):
        agreement = self.create_agreements_rebate(agreement_type, self.partner_1)
        agreement.rebate_line_ids = [
            (5, 0),
            (
                0,
                0,
                {
                    "rebate_target": "product",
                    "rebate_product_ids": [(6, 0, self.product_1.ids)],
                    "rebate_discount": 20,
                },
            ),
        ]
        return agreement

    def test_create_settlement_products_filters_global(self):
        # Invoice Lines:
        # Product template variants: 300, 500
        # Product 1: 1000
        # Product 2: 2000
        # Total by invoice: 3800 amount invoiced
        agreement = self._create_agreement_product_filter("global")
        settlement_wiz = self.create_settlement_wizard(agreement)
        settlements = self.get_settlements_from_action(
            settlement_wiz.action_create_settlement()
        )
        self.assertEqual(len(settlements), 1)
        self.assertEqual(settlements.amount_invoiced, 1000)
        self.assertEqual(settlements.amount_rebate, 100)

    def test_create_settlement_products_filters_line(self):
        agreement = self._create_agreement_product_filter("line")
        settlement_wiz = self.create_settlement_wizard(agreement)
        settlements = self.get_settlements_from_action(
            settlement_wiz.action_create_settlement()
        )
        self.assertEqual(len(settlements), 1)
        self.assertEqual(settlements.amount_invoiced, 1000)
        self.assertEqual(settlements.amount_rebate, 200)

    def test_create_settlement_products_filters_section_total(self):
        agreement = self._create_agreement_product_filter("section_total")
        settlement_wiz = self.create_settlement_wizard(agreement)
        settlements = self.get_settlements_from_action(
            settlement_wiz.action_create_settlement()
        )
        self.assertEqual(len(settlements), 1)
        self.assertEqual(settlements.amount_invoiced, 1000)
        self.assertEqual(settlements.amount_rebate, 300)

    def test_create_settlement_products_filters_section_prorated(self):
        agreement = self._create_agreement_product_filter("section_prorated")
        settlement_wiz = self.create_settlement_wizard(agreement)
        settlements = self.get_settlements_from_action(
            settlement_wiz.action_create_settlement()
        )
        self.assertEqual(len(settlements), 1)
        self.assertEqual(settlements.amount_invoiced, 1000)
        self.assertAlmostEqual(settlements.amount_rebate, 280, 2)

    def _create_invoice_wizard(self):
        sale_journal = self.env["account.journal"].search(
            [("type", "=", "sale")], limit=1
        )
        wiz_create_invoice_form = Form(self.env["agreement.invoice.create.wiz"])
        wiz_create_invoice_form.date_from = "2022-01-01"
        wiz_create_invoice_form.date_to = "2022-12-31"
        wiz_create_invoice_form.invoice_type = "out_invoice"
        wiz_create_invoice_form.journal_id = sale_journal
        wiz_create_invoice_form.product_id = self.product_rappel
        wiz_create_invoice_form.agreement_type_ids.add(self.agreement_type)
        return wiz_create_invoice_form.save()

    def test_invoice_agreements(self):
        # Create some rebate settlements
        agreement = self._create_agreement_product_filter("section_total")
        settlement_wiz = self.create_settlement_wizard(agreement)
        settlements = self.get_settlements_from_action(
            settlement_wiz.action_create_settlement()
        )
        wiz_create_invoice = self._create_invoice_wizard()
        wiz_create_invoice.agreement_ids = [(6, 0, agreement.ids)]
        wiz_create_invoice.settlements_ids = [(6, 0, settlements.ids)]
        action = wiz_create_invoice.action_create_invoice()
        invoices = self.env["account.move"].search(action["domain"])
        self.assertTrue(invoices)

        # Force invoice to partner
        invoices.unlink()
        wiz_create_invoice.invoice_partner_id = self.partner_2
        action = wiz_create_invoice.action_create_invoice()
        invoices = self.env["account.move"].search(action["domain"])
        self.assertEqual(invoices.partner_id, self.partner_2)
