# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)

from odoo import Command
from odoo.tests.common import TransactionCase

from ..models.res_partner import SHOW_CHILD_AGREEMENTS_PARAM


class TestResPartner(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, tracking_disable=True))
        cls.company = cls.env["res.partner"].create(
            {"name": "Test Company", "is_company": True}
        )
        cls.contact = cls.env["res.partner"].create(
            {"name": "Test Contact", "parent_id": cls.company.id}
        )
        cls.other_contact = cls.env["res.partner"].create(
            {"name": "Other Contact", "parent_id": cls.company.id}
        )
        Agreement = cls.env["agreement"]
        cls.company_agreement = Agreement.create(
            {
                "code": "COMPANY",
                "name": "Company agreement",
                "partner_id": cls.company.id,
            }
        )
        cls.contact_agreement = Agreement.create(
            {
                "code": "CONTACT",
                "name": "Contact agreement",
                "partner_id": cls.contact.id,
            }
        )
        cls.agreement_user = cls.env["res.users"].create(
            {
                "name": "Agreement Read-Only User",
                "login": "agreement_readonly_user",
                "group_ids": [
                    Command.link(cls.env.ref("base.group_user").id),
                    Command.link(cls.env.ref("agreement.group_agreement_readonly").id),
                ],
            }
        )

    def _set_show_child_agreements(self, value):
        self.env["ir.config_parameter"].sudo().set_param(
            SHOW_CHILD_AGREEMENTS_PARAM, value
        )
        self.env.invalidate_all()

    def _open_agreements(self, partner):
        action = partner.action_open_agreement()
        return self.env["agreement"].search(action["domain"])

    def test_direct_agreements_by_default(self):
        """Without the system parameter only direct agreements are shown."""
        partners = self.company | self.contact | self.other_contact
        self.assertEqual(partners.mapped("agreements_count"), [1, 1, 0])
        self.assertEqual(self._open_agreements(self.company), self.company_agreement)
        self.assertEqual(self._open_agreements(self.contact), self.contact_agreement)

    def test_child_agreements_with_parameter(self):
        """With the system parameter, a company also shows the agreements of
        its contacts, while a contact still shows only its own."""
        self._set_show_child_agreements("True")
        partners = self.company | self.contact | self.other_contact
        self.assertEqual(partners.mapped("agreements_count"), [2, 1, 0])
        self.assertEqual(
            self._open_agreements(self.company),
            self.company_agreement | self.contact_agreement,
        )
        self.assertEqual(self._open_agreements(self.contact), self.contact_agreement)
        self.assertFalse(self._open_agreements(self.other_contact))

    def test_child_agreements_count_single_partner(self):
        """The company count includes its contacts also when computed alone."""
        self._set_show_child_agreements("True")
        self.assertEqual(self.company.agreements_count, 2)

    def test_open_agreements_non_admin(self):
        """A user with agreement access can use the smart button."""
        action = self.company.with_user(self.agreement_user).action_open_agreement()
        self.assertEqual(action["res_model"], "agreement")
        self.assertEqual(action["context"]["default_partner_id"], self.company.id)
