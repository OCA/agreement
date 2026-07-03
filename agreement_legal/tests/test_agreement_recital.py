# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from datetime import timedelta

from odoo import fields

from odoo.addons.base.tests.common import BaseCommon


class TestAgreementRectical(BaseCommon):
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
        cls.test_recital = cls.env["agreement.recital"].create(
            {
                "name": "TestRecital",
                "title": "Test",
                "content": "Test",
                "agreement_id": cls.test_agreement.id,
            }
        )

    def test_onchange_copyvalue(self):
        recital_01 = self.test_recital
        field_01 = self.env["ir.model.fields"].search(
            [("model", "=", "agreement.recital"), ("name", "=", "active")]
        )
        recital_01.field_id = field_01.id
        recital_01.onchange_copyvalue()
        self.assertEqual(recital_01.copyvalue, "{{object.active or ''}}")

    def test_onchange_copyvalue2(self):
        recital_01 = self.test_recital
        field_01 = self.env["ir.model.fields"].search(
            [("model", "=", "agreement.recital"), ("name", "=", "agreement_id")]
        )
        sub_field_01 = self.env["ir.model.fields"].search(
            [("model", "=", "agreement"), ("name", "=", "active")]
        )
        recital_01.field_id = field_01.id
        recital_01.onchange_copyvalue()
        self.assertEqual(recital_01.sub_object_id.model, "agreement")
        recital_01.sub_model_object_field_id = sub_field_01.id
        recital_01.onchange_copyvalue()
        self.assertEqual(recital_01.copyvalue, "{{object.agreement_id.active or ''}}")

    def test_compute_dynamic_content(self):
        recital_01 = self.test_recital
        recital_01.content = "{{object.name}}"
        self.assertEqual(recital_01.dynamic_content, "<p>TestRecital</p>")
