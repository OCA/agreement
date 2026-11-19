# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)

from odoo.addons.base.tests.common import BaseCommon


class TestAgreementStage(BaseCommon):
    _test_user_groups = (
        "base.group_user",
        "agreement.group_agreement_manager",
        "base.group_erp_manager",
        "base.group_system",
    )

    def test_default_stage_type(self):
        stage = self.env["agreement.stage"].create({"name": "Default Stage Type"})
        self.assertEqual(stage.stage_type, "agreement")
