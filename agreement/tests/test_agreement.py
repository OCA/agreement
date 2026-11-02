# Copyright 2021 Ecosoft Co., Ltd (http://ecosoft.co.th)
# Copyright 2021 Sergio Teruel - Tecnativa
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)

from lxml import etree

from odoo import Command
from odoo.tests.common import TransactionCase


class TestAgreement(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, tracking_disable=True))
        cls.agreement_type = cls.env["agreement.type"].create(
            {
                "name": "Test Agreement Type",
                "domain": "purchase",
            }
        )
        cls.agreement = cls.env["agreement"].create(
            {
                "code": "TEST-AGREEMENT",
                "name": "Test agreement",
            }
        )
        cls.user_no_agreement = cls.env["res.users"].create(
            {
                "name": "User without agreement access",
                "login": "user_without_agreement_access",
                "group_ids": [Command.link(cls.env.ref("base.group_user").id)],
            }
        )

    def test_domain_selection(self):
        domain_agreement_type = self.env["agreement.type"]._domain_selection()
        domain_agreement = self.env["agreement"]._domain_selection()
        self.assertEqual(domain_agreement_type, domain_agreement)

    def test_agreement_type_change(self):
        self.agreement.write({"agreement_type_id": self.agreement_type.id})
        self.assertEqual(self.agreement.domain, self.agreement_type.domain)

    def test_compute_display_name(self):
        display_name = self.agreement.display_name
        self.assertEqual(display_name, f"[{self.agreement.code}] {self.agreement.name}")

    def test_copy(self):
        agreement1 = self.agreement.copy(default={"code": "Test Code"})
        agreement2 = self.agreement.copy()
        self.assertEqual(agreement1.code, "Test Code")
        self.assertEqual(agreement2.code, f"{self.agreement.code} (copy)")

    def test_agreements_count_no_agreement_access(self):
        """Users without any agreement group can still open a partner form."""
        partner = self.env["res.partner"].create({"name": "Partner with agreement"})
        self.agreement.partner_id = partner
        self.assertFalse(
            self.user_no_agreement.has_group("agreement.group_agreement_readonly")
        )
        self.assertEqual(partner.with_user(self.user_no_agreement).agreements_count, 1)

    def test_agreement_button_hidden_without_access(self):
        """The Agreements stat button is restricted to agreement users."""
        arch = etree.fromstring(
            self.env.ref("agreement.partner_form").get_combined_arch()
        )
        button = arch.xpath("//button[@name='action_open_agreement']")
        self.assertEqual(len(button), 1)
        self.assertEqual(button[0].get("groups"), "agreement.group_agreement_readonly")
        self.assertFalse(
            self.user_no_agreement.has_group("agreement.group_agreement_readonly")
        )
