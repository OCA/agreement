from odoo import Command
from odoo.tests import Form, TransactionCase


class TestAgreementCategory(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, tracking_disable=True))
        cls.partner = cls.env["res.partner"].create({"name": "Test Partner"})
        cls.category_nda = cls.env["agreement.category"].create({"name": "NDA"})
        cls.category_sla = cls.env["agreement.category"].create({"name": "SLA"})
        cls.agreement = cls.env["agreement"].create(
            {
                "name": "Test Agreement",
                "code": "TEST-CAT",
                "partner_id": cls.partner.id,
            }
        )

    def test_default_color(self):
        self.assertTrue(1 <= self.category_nda.color <= 11)

    def test_tag_agreement(self):
        self.agreement.category_ids = [
            Command.set((self.category_nda | self.category_sla).ids)
        ]
        self.assertEqual(self.category_nda.agreement_ids, self.agreement)
        self.assertEqual(self.category_sla.agreement_ids, self.agreement)
        tagged = self.env["agreement"].search(
            [("category_ids", "in", self.category_nda.ids)]
        )
        self.assertEqual(tagged, self.agreement)

    def test_tag_agreement_form(self):
        with Form(self.agreement) as agreement_form:
            agreement_form.category_ids.add(self.category_sla)
        self.assertEqual(self.agreement.category_ids, self.category_sla)

    def test_archive_category(self):
        self.agreement.category_ids = [Command.link(self.category_nda.id)]
        self.category_nda.action_archive()
        self.assertFalse(self.category_nda.active)
        self.assertNotIn(
            self.category_nda,
            self.env["agreement.category"].search([("name", "=", "NDA")]),
        )

    def test_copy_agreement_keeps_tags(self):
        self.agreement.category_ids = [Command.link(self.category_nda.id)]
        new_agreement = self.agreement.copy()
        self.assertEqual(new_agreement.category_ids, self.category_nda)
