# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from datetime import timedelta
from unittest.mock import patch

from lxml import etree

from odoo import fields

from odoo.addons.base.tests.common import BaseCommon


class TestAgreement(BaseCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, tracking_disable=True))
        cls.test_customer = cls.env["res.partner"].create({"name": "TestCustomer"})
        cls.agreement_type = cls.env["agreement.type"].create(
            {"name": "Test Agreement Type", "domain": "sale"}
        )
        cls.test_agreement = cls.env["agreement"].create(
            {
                "name": "TestAgreement",
                "description": "Test",
                "special_terms": "Test",
                "partner_id": cls.test_customer.id,
                "start_date": fields.Date.today(),
                "end_date": fields.Date.today() + timedelta(days=365),
                "state": "active",
            }
        )

    def test_onchange_copyvalue(self):
        agreement_01 = self.test_agreement
        field_01 = self.env["ir.model.fields"].search(
            [("model", "=", "agreement"), ("name", "=", "active")]
        )
        agreement_01.field_id = field_01.id
        agreement_01.onchange_copyvalue()
        self.assertEqual(agreement_01.copyvalue, "{{object.active or ''}}")

    def test_onchange_copyvalue2(self):
        agreement_01 = self.test_agreement
        field_01 = self.env["ir.model.fields"].search(
            [("model", "=", "agreement"), ("name", "=", "agreement_type_id")]
        )
        sub_field_01 = self.env["ir.model.fields"].search(
            [("model", "=", "agreement.type"), ("name", "=", "active")]
        )
        agreement_01.field_id = field_01.id
        agreement_01.onchange_copyvalue()
        self.assertEqual(agreement_01.sub_object_id.model, "agreement.type")
        agreement_01.sub_model_object_field_id = sub_field_01.id
        agreement_01.onchange_copyvalue()
        self.assertEqual(
            agreement_01.copyvalue, "{{object.agreement_type_id.active or ''}}"
        )

    def test_create_new_version(self):
        agreement_01 = self.test_agreement
        agreement_01.create_new_version()
        old_agreement = self.env["agreement"].search(
            [("code", "=", agreement_01.code + "-V1"), ("active", "=", False)]
        )
        self.assertEqual(len(old_agreement), 1)
        new_agreement = self.env["agreement"].search(
            [("name", "=", "TestAgreement"), ("version", "=", 2)]
        )
        self.assertEqual(len(new_agreement), 1)

    def test_create_new_agreement(self):
        agreement_01 = self.test_agreement
        agreement_01.create_new_agreement()
        new_agreement = self.env["agreement"].search([("name", "=", "New")])
        self.assertEqual(len(new_agreement), 1)

    def test_compute_dynamic_description(self):
        agreement_01 = self.test_agreement
        agreement_01.description = "{{object.name}}"
        self.assertEqual(agreement_01.dynamic_description, "TestAgreement")

    def test_compute_dynamic_parties(self):
        agreement_01 = self.test_agreement
        agreement_01.parties = "{{object.name}}"
        self.assertEqual(agreement_01.dynamic_parties, "<p>TestAgreement</p>")

    def test_compute_dynamic_special_terms(self):
        agreement_01 = self.test_agreement
        agreement_01.special_terms = "{{object.name}}"
        self.assertEqual(agreement_01.dynamic_special_terms, "TestAgreement")

    def test_read_group_stage_ids(self):
        agreement_01 = self.test_agreement
        self.assertEqual(
            agreement_01._read_group_stage_ids(self.env["agreement.stage"], [], "id"),
            self.env["agreement.stage"].search(
                [("stage_type", "=", "agreement")], order="id"
            ),
        )

    def test_agreement_fields_view_get(self):
        res = self.env["agreement"].get_view(
            view_id=self.ref("agreement_legal.partner_agreement_form_view"),
            view_type="form",
        )
        doc = etree.XML(res["arch"])
        field = doc.xpath("//field[@name='partner_contact_id']")
        self.assertEqual(field[0].get("readonly", ""), "bool(readonly)")

    def test_action_create_new_version(self):
        self.test_agreement.create_new_version()
        self.assertEqual(self.test_agreement.state, "draft")
        self.assertEqual(len(self.test_agreement.previous_version_agreements_ids), 1)

    def test_cron(self):
        self.agreement_type.write(
            {"review_user_id": self.env.user.id, "review_days": 0}
        )
        self.agreement_type.flush_recordset()
        self.test_agreement.write({"agreement_type_id": self.agreement_type.id})
        self.test_agreement.flush_recordset()
        self.test_agreement.invalidate_recordset()
        self.assertFalse(
            self.env["mail.activity"].search_count(
                [
                    ("res_id", "=", self.test_agreement.id),
                    ("res_model", "=", self.test_agreement._name),
                ]
            )
        )
        self.env["agreement"]._alert_to_review_date()
        self.assertFalse(
            self.env["mail.activity"].search_count(
                [
                    ("res_id", "=", self.test_agreement.id),
                    ("res_model", "=", self.test_agreement._name),
                ]
            )
        )
        self.test_agreement.to_review_date = fields.Date.today()
        self.env["agreement"]._alert_to_review_date()
        self.assertTrue(
            self.env["mail.activity"].search_count(
                [
                    ("res_id", "=", self.test_agreement.id),
                    ("res_model", "=", self.test_agreement._name),
                ]
            )
        )

    def test_partner_action(self):
        action = self.test_agreement.partner_id.action_open_agreement()
        self.assertIn(
            self.test_agreement, self.env[action["res_model"]].search(action["domain"])
        )
        self.assertEqual(1, self.test_agreement.partner_id.agreements_count)

    def test_agreement_kanban_menu_template(self):
        res = self.env["agreement"].get_view(
            view_id=self.ref("agreement_legal.view_project_agreement_kanban"),
            view_type="kanban",
        )
        doc = etree.XML(res["arch"])
        kanban = doc.xpath("//kanban")[0]
        self.assertEqual(kanban.get("highlight_color"), "color")
        self.assertTrue(doc.xpath("//templates/t[@t-name='menu']"))
        self.assertFalse(doc.xpath("//div[hasclass('o_dropdown_kanban')]"))
        self.assertFalse(doc.xpath("//*[contains(@t-attf-class, 'kanban_getcolor')]"))

    def test_agreement_kanban_color_field(self):
        self.test_agreement.color = 4
        self.assertEqual(self.test_agreement.color, 4)
        self.test_agreement.write({"color": 8})
        self.assertEqual(self.test_agreement.color, 8)

    def test_create_new_version_from_draft(self):
        self.test_agreement.state = "draft"
        version = self.test_agreement.version
        self.test_agreement.create_new_version()
        self.assertEqual(self.test_agreement.version, version + 1)

    def test_alert_to_review_date_skips_existing_activity(self):
        self.agreement_type.write(
            {"review_user_id": self.env.user.id, "review_days": 0}
        )
        self.test_agreement.write({"agreement_type_id": self.agreement_type.id})
        self.test_agreement.to_review_date = fields.Date.today()
        self.env["mail.activity"].create(
            {
                "res_id": self.test_agreement.id,
                "res_model_id": self.env.ref("agreement.model_agreement").id,
                "activity_type_id": self.env.ref("mail.mail_activity_data_todo").id,
                "user_id": self.env.user.id,
            }
        )
        before = self.env["mail.activity"].search_count(
            [
                ("res_id", "=", self.test_agreement.id),
                ("res_model", "=", self.test_agreement._name),
            ]
        )
        self.env["agreement"]._alert_to_review_date()
        after = self.env["mail.activity"].search_count(
            [
                ("res_id", "=", self.test_agreement.id),
                ("res_model", "=", self.test_agreement._name),
            ]
        )
        self.assertEqual(before, after)

    def test_get_default_stage_id_fallback(self):
        real_ref = self.env.ref

        def ref(xmlid, raise_if_not_found=True):
            if xmlid == "agreement_legal.agreement_stage_new":
                raise ValueError
            return real_ref(xmlid, raise_if_not_found=raise_if_not_found)

        with patch.object(self.env, "ref", side_effect=ref):
            self.env.ref("base.main_company")
            self.assertFalse(self.env["agreement"]._get_default_stage_id())

    def test_agreement_copy(self):
        template = self.env["agreement"].create(
            {
                "name": "Template",
                "is_template": True,
                "partner_id": self.test_customer.id,
            }
        )
        section = self.env["agreement.section"].create(
            {
                "name": "Section",
                "content": "Section",
                "agreement_id": template.id,
            }
        )
        self.env["agreement.clause"].create(
            {
                "name": "Clause",
                "content": "Clause",
                "agreement_id": template.id,
                "section_id": section.id,
            }
        )
        copy = template.copy()
        self.assertTrue(copy.clauses_ids)
        self.assertEqual(copy.clauses_ids.agreement_id, copy)

    def test_agreement_write_revision(self):
        revision = self.test_agreement.revision
        self.test_agreement.write({"name": "Updated"})
        self.assertEqual(self.test_agreement.revision, revision + 1)

    def test_create_agreement_from_template_action(self):
        template = self.env["agreement"].create(
            {
                "name": "Template",
                "is_template": True,
                "partner_id": self.test_customer.id,
            }
        )
        action = template.create_new_agreement()
        self.assertEqual(action["res_model"], "agreement")
        self.assertEqual(action["type"], "ir.actions.act_window")

    def test_get_view_merges_existing_readonly(self):
        res = self.env["agreement"].get_view(
            view_id=self.ref("agreement_legal.partner_agreement_form_view"),
            view_type="form",
        )
        doc = etree.XML(res["arch"])
        field = doc.xpath("//field[@name='sub_object_id']")
        self.assertEqual(field[0].get("readonly"), "(1) or (bool(readonly))")

    def test_write_with_explicit_revision(self):
        revision = self.test_agreement.revision
        self.test_agreement.write({"revision": revision, "name": "Explicit revision"})
        self.assertEqual(self.test_agreement.revision, revision)

    def test_create_with_explicit_code_and_stage(self):
        stage = self.env.ref("agreement_legal.agreement_stage_new")
        agreement = self.env["agreement"].create(
            {
                "name": "Explicit",
                "code": "EXPLICIT",
                "stage_id": stage.id,
                "partner_id": self.test_customer.id,
            }
        )
        self.assertEqual(agreement.code, "EXPLICIT")
        self.assertEqual(agreement.stage_id, stage)

    def test_get_view_non_form(self):
        res = self.env["agreement"].get_view(view_type="list")
        self.assertIn("arch", res)
