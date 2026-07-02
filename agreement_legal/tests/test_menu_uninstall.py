# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)

from odoo.tests import tagged
from odoo.tests.common import TransactionCase

from odoo.addons.agreement_legal import uninstall_hook


@tagged("post_install", "-at_install")
class TestAgreementLegalMenuUninstall(TransactionCase):
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
