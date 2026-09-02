# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)

from datetime import timedelta

from odoo import fields
from odoo.tests.common import TransactionCase, new_test_user, users


class TestAgreementTemplate(TransactionCase):
    def setUp(self):
        super().setUp()
        self.user_no_template_group = new_test_user(
            self.env,
            login="user_no_template_group",
            groups="base.group_user,agreement.group_agreement_user",
        )
        self.test_customer = self.env["res.partner"].create({"name": "TestCustomer"})
        self.test_agreement = self.env["agreement"].create(
            {
                "name": "TestAgreement",
                "code": "TA001",
                "partner_id": self.test_customer.id,
                "start_date": fields.Date.today(),
                "end_date": fields.Date.today() + timedelta(days=365),
            }
        )

    def test_recompute_logic(self):
        template = self.env["agreement"].create(
            {
                "name": "Template Agreement",
                "code": "TA001",
                "is_template": True,
            }
        )
        self.test_agreement.template_id = template.id
        message_count = len(self.test_agreement.message_ids)

        self.test_agreement.recompute_from_template()

        self.assertEqual(len(self.test_agreement.message_ids), message_count + 1)

    def test_create_new_agreement(self):
        self.test_agreement.create_new_agreement()
        new_agreement = self.env["agreement"].search([("name", "=", "New")])
        self.assertEqual(len(new_agreement), 1)

    def test_create_new_agreement_is_not_a_template(self):
        template = self.env["agreement"].create(
            {
                "name": "Template Agreement",
                "code": "TA002",
                "is_template": True,
            }
        )

        # the button is pressed from the template action, whose context makes
        # every new record a template by default
        template.with_context(default_is_template=True).create_new_agreement()

        new_agreement = self.env["agreement"].search(
            [("template_id", "=", template.id)]
        )
        self.assertEqual(len(new_agreement), 1)
        self.assertFalse(new_agreement.is_template)

    def test_action_open_recompute_from_template_wizard(self):
        template = self.env["agreement"].create(
            {
                "name": "Template Agreement",
                "code": "TA001",
                "is_template": True,
            }
        )
        self.test_agreement.template_id = template

        action = self.test_agreement.action_open_recompute_from_template_wizard()

        self.assertEqual(
            action["res_model"], "recompute.agreement.from.template.wizard"
        )
        self.assertEqual(action["target"], "new")
        self.assertEqual(
            action["context"]["default_agreement_id"],
            self.test_agreement.id,
        )

    def test_create_hidden_only_for_template_users(self):
        agreement = self.env["agreement"]
        self.assertEqual(
            agreement.get_view(view_type="list")["arch"].count('create="0"'), 1
        )
        self.assertNotIn(
            'create="0"',
            agreement.with_context(default_is_template=True).get_view(view_type="list")[
                "arch"
            ],
        )

    def test_create_visible_on_template_action(self):
        # the client strips the action context before calling get_views, only
        # the action id tells the template views apart from the agreement ones
        agreement = self.env["agreement"]
        template_action = self.env.ref("agreement.agreement_template_action")
        for view_type in ("list", "kanban", "form"):
            with self.subTest(view_type=view_type):
                self.assertIn(
                    'create="0"',
                    agreement.get_view(
                        view_type=view_type,
                        action_id=self.env.ref("agreement.agreement_action").id,
                    )["arch"],
                )
                self.assertNotIn(
                    'create="0"',
                    agreement.get_view(
                        view_type=view_type, action_id=template_action.id
                    )["arch"],
                )

    def test_template_create_only_for_managers(self):
        template_action_id = self.env.ref("agreement.agreement_template_action").id
        agreement_user = new_test_user(
            self.env,
            login="agreement_user",
            groups="base.group_user,agreement.group_agreement_user",
        )
        agreement_manager = new_test_user(
            self.env,
            login="agreement_manager",
            groups="base.group_user,agreement.group_agreement_manager",
        )

        def template_arch(user, view_type):
            return (
                self.env["agreement"]
                .with_user(user)
                .get_view(view_type=view_type, action_id=template_action_id)["arch"]
            )

        for view_type in ("list", "kanban", "form"):
            with self.subTest(view_type=view_type):
                self.assertIn('create="0"', template_arch(agreement_user, view_type))
                self.assertNotIn(
                    'create="0"', template_arch(agreement_manager, view_type)
                )

    @users("user_no_template_group")
    def test_create_visible_without_template_group(self):
        # the agreement groups imply the template group, so the implication has
        # to be dropped to get a user without it
        self.env.ref(
            "agreement.group_agreement_readonly"
        ).sudo().implied_ids -= self.env.ref("agreement.group_use_agreement_template")
        agreement = self.env["agreement"]
        self.assertNotIn('create="0"', agreement.get_view(view_type="list")["arch"])
