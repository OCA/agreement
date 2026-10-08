# Copyright 2017-2020 Akretion France (http://www.akretion.com/)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.addons.base.tests.common import BaseCommon


class TestAgreement(BaseCommon):
    @classmethod
    def setUpClass(self):
        super().setUpClass()
        self.test_customer = self.env["res.partner"].create({"name": "TestCustomer"})
        self.test_agreement_sale = self.env["agreement"].create(
            {
                "name": "TestAgreement-Sale",
                "code": "SALE",
                "partner_id": self.test_customer.id,
                "domain": "sale",
            }
        )
        self.test_agreement_purchase = self.env["agreement"].create(
            {
                "name": "TestAgreement-Purchase",
                "code": "PURCHASE",
                "partner_id": self.test_customer.id,
                "domain": "purchase",
            }
        )

    def test_compute_invoice_count(self):
        self.test_agreement_sale._compute_invoice_count()
        self.test_agreement_purchase._compute_invoice_count()
