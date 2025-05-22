# Copyright (C) 2020 - TODAY, Marcel Savegnago - Escodoo
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
import odoo.tests.common as common

from odoo.addons.base.tests.common import DISABLED_MAIL_CONTEXT


class TestAgreementHelpdeskMgmt(common.TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, **DISABLED_MAIL_CONTEXT))
        cls.partner = cls.env["res.partner"].create(
            {
                "name": "Test Partner",
                "email": "test@test.com",
            }
        )
        cls.agreement = cls.env["agreement"].create(
            {
                "name": "Test Agreement",
                "code": "AGREEMENT001",
                "partner_id": cls.partner.id,
            }
        )
        cls.ticket = cls.env["helpdesk.ticket"].create(
            {
                "name": "Test Helpdesk Ticket",
                "description": "Test Helpdesk Ticket",
                "partner_id": cls.partner.id,
                "agreement_id": cls.agreement.id,
            }
        )

    def test_compute_ticket_count(self):
        self.agreement._compute_ticket_count()
        self.assertEqual(self.agreement.ticket_count, 1)

    def test_action_view_ticket(self):
        result = self.agreement.action_view_ticket()
        self.assertEqual(result["res_id"], self.ticket.id)
