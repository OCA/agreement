# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from unittest.mock import patch

from odoo.addons.agreement_legal import uninstall_hook
from odoo.addons.base.tests.common import BaseCommon


class TestAgreementLegalMenuUninstall(BaseCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, tracking_disable=True))

    def test_agreement_menu_not_replaced_by_legal_root(self):
        """agreement_legal must use its own root menu, not agreement.agreement_menu."""
        legal_root = self.env.ref("agreement_legal.agreement_legal_menu_root")
        agreement_menu = self.env.ref("agreement.agreement_menu")
        dashboard = self.env.ref("agreement_legal.agreement_dashboard")

        self.assertNotEqual(legal_root.id, agreement_menu.id)
        self.assertTrue(legal_root.active)
        self.assertFalse(legal_root.parent_id)
        self.assertEqual(dashboard.parent_id, legal_root)

    def test_uninstall_hook_restores_agreement_menu(self):
        """uninstall_hook must reactivate the base Agreements app menu."""
        agreement_root = self.env.ref("agreement.agreement_menu_root")
        agreement_menu = self.env.ref("agreement.agreement_menu")

        self.assertFalse(agreement_root.active)
        self.assertTrue(agreement_menu.active)

        uninstall_hook(self.env)

        self.assertTrue(agreement_root.active)
        self.assertTrue(agreement_menu.active)

    def test_uninstall_hook_noop_when_menu_missing(self):
        real_ref = self.env.ref

        def ref(xmlid, raise_if_not_found=True):
            if xmlid == "agreement.agreement_menu_root":
                return False
            return real_ref(xmlid, raise_if_not_found=raise_if_not_found)

        with patch.object(self.env, "ref", side_effect=ref):
            self.env.ref("base.main_company")
            uninstall_hook(self.env)
