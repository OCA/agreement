# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from datetime import timedelta

from odoo import fields

from odoo.addons.base.tests.common import BaseCommon


class TestAgreementLine(BaseCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, tracking_disable=True))
        cls.test_customer = cls.env["res.partner"].create({"name": "TestCustomer"})
        cls.agreement_type = cls.env["agreement.type"].create(
            {"name": "Test Agreement Type", "domain": "sale"}
        )
        cls.test_agreement = cls.env["agreement"].create(
            {
                "name": "TestAgreement",
                "description": "Test",
                "special_terms": "Test",
                "partner_id": cls.test_customer.id,
                "start_date": fields.Date.today(),
                "end_date": fields.Date.today() + timedelta(days=365),
            }
        )
        cls.test_product1 = cls.env["product.product"].create({"name": "TEST1"})
        cls.test_product2 = cls.env["product.product"].create({"name": "TEST2"})
        cls.test_line = cls.env["agreement.line"].create(
            {
                "product_id": cls.test_product1.id,
                "name": "Test",
                "uom_id": 1,
                "agreement_id": cls.test_agreement.id,
            }
        )

    def test_onchange_product_id(self):
        line_01 = self.test_line
        line_01.product_id = self.test_product2.id
        line_01._onchange_product_id()
        self.assertEqual(line_01.name, "TEST2")
