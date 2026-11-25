# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)

from datetime import timedelta

from odoo import fields
from odoo.tests.common import TransactionCase


class TestAgreementType(TransactionCase):
    def setUp(self):
        super().setUp()
        self.test_customer = self.env["res.partner"].create({"name": "TestCustomer"})
        self.agreement_type = self.env["agreement.type"].create(
            {"name": "Test Agreement Type", "domain": "sale"}
        )
        self.test_agreement = self.env["agreement"].create(
            {
                "name": "TestAgreement",
                "code": "TA001",
                "partner_id": self.test_customer.id,
                "start_date": fields.Date.today(),
                "end_date": fields.Date.today() + timedelta(days=365),
            }
        )

    # A sub-type is an agreement type with a parent type
    def test_subtype_hierarchy(self):
        subtype = self.env["agreement.type"].create(
            {"name": "Test Sub-Type", "parent_type_id": self.agreement_type.id}
        )
        self.assertIn(subtype, self.agreement_type.child_type_ids)
        self.test_agreement.write(
            {
                "agreement_type_id": subtype.id,
            }
        )
        self.assertEqual(self.test_agreement.agreement_type_id, subtype)

    # The review cron schedules an activity on the review date
    def test_cron(self):
        self.agreement_type.write(
            {"review_user_id": self.env.user.id, "review_days": 0}
        )
        self.agreement_type.flush_recordset()
        self.test_agreement.write({"agreement_type_id": self.agreement_type.id})
        self.test_agreement.flush_recordset()
        self.test_agreement.invalidate_recordset()
        self.assertFalse(
            self.env["mail.activity"].search_count(
                [
                    ("res_id", "=", self.test_agreement.id),
                    ("res_model", "=", self.test_agreement._name),
                ]
            )
        )
        self.env["agreement"]._alert_to_review_date()
        self.assertFalse(
            self.env["mail.activity"].search_count(
                [
                    ("res_id", "=", self.test_agreement.id),
                    ("res_model", "=", self.test_agreement._name),
                ]
            )
        )
        self.test_agreement.to_review_date = fields.Date.today()
        self.env["agreement"]._alert_to_review_date()
        self.assertTrue(
            self.env["mail.activity"].search_count(
                [
                    ("res_id", "=", self.test_agreement.id),
                    ("res_model", "=", self.test_agreement._name),
                ]
            )
        )
