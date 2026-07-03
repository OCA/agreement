# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo.addons.base.tests.common import BaseCommon


class TestAgreementLegalModels(BaseCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, tracking_disable=True))

    def test_agreement_subtype(self):
        agreement_type = self.env["agreement.type"].create(
            {"name": "Subtype Type", "domain": "sale"}
        )
        subtype = self.env["agreement.subtype"].create(
            {"name": "Subtype", "agreement_type_id": agreement_type.id}
        )
        self.assertEqual(subtype.agreement_type_id, agreement_type)
        self.assertTrue(subtype.active)

    def test_agreement_stage(self):
        stage = self.env["agreement.stage"].create(
            {"name": "Custom Stage", "stage_type": "agreement"}
        )
        self.assertEqual(stage.stage_type, "agreement")
        self.assertTrue(stage.active)

    def test_res_config_settings_fields(self):
        settings_model = self.env["res.config.settings"]
        for field_name in (
            "module_agreement_sale",
            "module_agreement_project",
        ):
            self.assertIn(field_name, settings_model._fields)
            self.assertEqual(settings_model._fields[field_name].type, "boolean")
