# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)

from datetime import timedelta

from odoo import fields
from odoo.tests.common import TransactionCase


class TestAgreementSignature(TransactionCase):
    def setUp(self):
        super().setUp()
        self.test_customer = self.env["res.partner"].create({"name": "TestCustomer"})
        self.test_user = self.env["res.users"].create(
            {"name": "TestSigner", "login": "test_signer"}
        )
        self.test_agreement = self.env["agreement"].create(
            {
                "name": "TestAgreement",
                "partner_id": self.test_customer.id,
                "start_date": fields.Date.today(),
                "end_date": fields.Date.today() + timedelta(days=365),
                "code": "TESTCODE2",
            }
        )

    def test_signature_fields(self):
        today = fields.Date.today()
        self.test_agreement.write(
            {
                "company_signed_date": today,
                "company_signed_user_id": self.test_user.id,
                "partner_signed_date": today,
                "partner_signed_user_id": self.test_customer.id,
                "code": "TESTCODE",
            }
        )
        self.assertEqual(self.test_agreement.company_signed_date, today)
        self.assertEqual(self.test_agreement.company_signed_user_id, self.test_user)
        self.assertEqual(self.test_agreement.partner_signed_date, today)
        self.assertEqual(self.test_agreement.partner_signed_user_id, self.test_customer)
