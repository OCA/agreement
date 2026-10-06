# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)

from datetime import timedelta

from lxml import etree

from odoo import fields
from odoo.tests.common import TransactionCase


class TestAgreementStage(TransactionCase):
    def setUp(self):
        super().setUp()
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

    # Check the kanban group_expand returns the agreement stages
    def test_read_group_stage_ids(self):
        agreement_01 = self.test_agreement
        self.assertEqual(
            agreement_01._read_group_stage_ids(self.env["agreement.stage"], [], "id"),
            self.env["agreement.stage"].search(
                [("stage_type", "=", "agreement")], order="id"
            ),
        )

    # Check the stage-driven read-only lock is injected in the form view
    def test_agreement_fields_view_get(self):
        res = self.env["agreement"].get_view(
            view_id=self.ref("agreement_stage.partner_agreement_form_view"),
            view_type="form",
        )
        doc = etree.XML(res["arch"])
        field = doc.xpath("//field[@name='name']")
        self.assertEqual(field[0].get("readonly", ""), "bool(readonly)")
