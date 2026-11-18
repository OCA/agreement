# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)

from datetime import timedelta

from odoo import fields
from odoo.tests.common import TransactionCase


class TestAgreementTermination(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, tracking_disable=True))
        cls.activity_type = cls.env.ref(
            "agreement_termination.mail_activity_review_agreement"
        )
        cls.partner = cls.env["res.partner"].create({"name": "TestCustomer"})
        cls.agreement = cls.env["agreement"].create(
            {
                "name": "TestAgreement",
                "code": "TA001",
                "partner_id": cls.partner.id,
                "start_date": fields.Date.today(),
                "end_date": fields.Date.today() + timedelta(days=365),
                "expiration_notice": 30,
            }
        )

    def _review_activities(self):
        return self.agreement.activity_ids.filtered(
            lambda a: a.activity_type_id == self.activity_type
        )

    # The review date is the end date minus the expiration notice
    def test_compute_to_review_date(self):
        self.assertEqual(
            self.agreement.to_review_date,
            self.agreement.end_date - timedelta(days=30),
        )
        self.agreement.expiration_notice = 10
        self.assertEqual(
            self.agreement.to_review_date,
            self.agreement.end_date - timedelta(days=10),
        )

    # The cron assigns a review activity to the last modifier, once only
    def test_cron_assigns_last_modifier(self):
        self.env["agreement"]._alert_to_review_date()
        self.assertFalse(self._review_activities())

        modifier = self.env["res.users"].create(
            {"name": "Last Modifier", "login": "last_modifier"}
        )
        self.agreement.with_user(modifier).sudo().write(
            {"to_review_date": fields.Date.today()}
        )
        self.assertEqual(self.agreement.write_uid, modifier)

        self.env["agreement"]._alert_to_review_date()
        activities = self._review_activities()
        self.assertEqual(len(activities), 1)
        self.assertEqual(activities.user_id, modifier)

        # Running the cron again does not duplicate the activity
        self.env["agreement"]._alert_to_review_date()
        self.assertEqual(len(self._review_activities()), 1)

    # Templates never get a review activity
    def test_cron_skips_templates(self):
        self.agreement.write(
            {"is_template": True, "to_review_date": fields.Date.today()}
        )
        self.env["agreement"]._alert_to_review_date()
        self.assertFalse(self._review_activities())
