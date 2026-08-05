# Copyright (C) 2026 Pop Solutions
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import HttpCase, tagged


@tagged("post_install", "-at_install")
class TestAgreementPortal(HttpCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.partner = cls.env["res.partner"].create({"name": "Portal Partner"})
        cls.other_partner = cls.env["res.partner"].create({"name": "Other Partner"})
        cls.portal_user = (
            cls.env["res.users"]
            .with_context(no_reset_password=True)
            .create(
                {
                    "login": "portal-agreement@test.example.com",
                    "name": "Portal Agreement User",
                    "partner_id": cls.partner.id,
                    "groups_id": [(6, 0, [cls.env.ref("base.group_portal").id])],
                    "password": "portal-agreement",
                }
            )
        )
        cls.agreement = cls.env["agreement"].create(
            {
                "name": "My Portal Agreement",
                "code": "PORTAL-1",
                "partner_id": cls.partner.id,
            }
        )
        cls.other_agreement = cls.env["agreement"].create(
            {
                "name": "Foreign Agreement",
                "code": "PORTAL-2",
                "partner_id": cls.other_partner.id,
            }
        )

    def test_access_url(self):
        self.assertEqual(
            self.agreement.access_url, f"/my/agreements/{self.agreement.id}"
        )

    def test_portal_list_shows_own_agreements_only(self):
        self.authenticate("portal-agreement@test.example.com", "portal-agreement")
        response = self.url_open("/my/agreements")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"My Portal Agreement", response.content)
        self.assertNotIn(b"Foreign Agreement", response.content)

    def test_portal_detail_page(self):
        self.authenticate("portal-agreement@test.example.com", "portal-agreement")
        response = self.url_open(f"/my/agreements/{self.agreement.id}")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"My Portal Agreement", response.content)

    def test_portal_detail_denied_without_access(self):
        self.authenticate("portal-agreement@test.example.com", "portal-agreement")
        response = self.url_open(f"/my/agreements/{self.other_agreement.id}")
        self.assertNotIn(b"Foreign Agreement", response.content)

    def test_portal_detail_with_access_token(self):
        self.other_agreement._portal_ensure_token()
        response = self.url_open(
            f"/my/agreements/{self.other_agreement.id}"
            f"?access_token={self.other_agreement.access_token}"
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Foreign Agreement", response.content)
