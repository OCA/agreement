# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)

from datetime import timedelta

from odoo import fields

from odoo.addons.base.tests.common import BaseCommon


class TestAgreementSection(BaseCommon):
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
        cls.test_section = cls.env["agreement.section"].create(
            {
                "name": "TestSection",
                "title": "Test",
                "content": "Test",
                "agreement_id": cls.test_agreement.id,
            }
        )

    # TEST 01: Set 'Field' for dynamic placeholder, test onchange method
    def test_onchange_copyvalue(self):
        section_01 = self.test_section
        field_01 = self.env["ir.model.fields"].search(
            [("model", "=", "agreement.section"), ("name", "=", "active")]
        )
        section_01.field_id = field_01.id
        section_01.onchange_copyvalue()
        self.assertEqual(section_01.copyvalue, "{{object.active or ''}}")

    # TEST 02: Set related 'Field' for dynamic placeholder to
    # test onchange method
    def test_onchange_copyvalue2(self):
        section_01 = self.test_section
        field_01 = self.env["ir.model.fields"].search(
            [("model", "=", "agreement.section"), ("name", "=", "agreement_id")]
        )
        sub_field_01 = self.env["ir.model.fields"].search(
            [("model", "=", "agreement"), ("name", "=", "active")]
        )
        section_01.field_id = field_01.id
        section_01.onchange_copyvalue()
        self.assertEqual(section_01.sub_object_id.model, "agreement")
        section_01.sub_model_object_field_id = sub_field_01.id
        section_01.onchange_copyvalue()
        self.assertEqual(section_01.copyvalue, "{{object.agreement_id.active or ''}}")

    # TEST 03: Test Dynamic Field
    def test_compute_dynamic_content(self):
        section_01 = self.test_section
        section_01.content = "{{object.name}}"
        self.assertEqual(section_01.dynamic_content, "<p>TestSection</p>")
