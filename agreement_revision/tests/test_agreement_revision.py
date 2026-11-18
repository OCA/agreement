# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)

from datetime import timedelta

from odoo import fields
from odoo.tests.common import TransactionCase


class TestAgreementRevision(TransactionCase):
    def setUp(self):
        super().setUp()
        self.test_customer = self.env["res.partner"].create({"name": "TestCustomer"})
        self.agreement_type = self.env["agreement.type"].create(
            {"name": "Test Agreement Type", "domain": "sale"}
        )
        self.test_agreement = self.env["agreement"].create(
            {
                "name": "TestAgreement",
                "code": "AG-001",
                "partner_id": self.test_customer.id,
                "start_date": fields.Date.today(),
                "end_date": fields.Date.today() + timedelta(days=365),
                "state": "active",
            }
        )

    def test_create_new_version(self):
        agreement_01 = self.test_agreement
        agreement_01.create_new_version()
        old_agreement = self.env["agreement"].search(
            [("code", "=", agreement_01.code + "-V1"), ("active", "=", False)]
        )
        self.assertEqual(len(old_agreement), 1)
        new_agreement = self.env["agreement"].search(
            [("name", "=", "TestAgreement"), ("version", "=", 2)]
        )
        self.assertEqual(len(new_agreement), 1)

    def test_action_create_new_version(self):
        self.test_agreement.create_new_version()
        self.assertEqual(self.test_agreement.state, "draft")
        self.assertEqual(len(self.test_agreement.previous_version_agreements_ids), 1)
