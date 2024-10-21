# Copyright 2021 Ecosoft Co., Ltd (http://ecosoft.co.th)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class CreateAgreementWizard(models.TransientModel):
    _name = "create.agreement.wizard"
    _description = "Create Agreement Wizard"

    template_id = fields.Many2one(
        "agreement",
        string="Template",
        required=True,
        domain=[("is_template", "=", True)],
    )
    name = fields.Char(string="Title", required=True)

    def _create_agreement(self):
        self.ensure_one()
        agreement = self.template_id._create_new_agreement()
        agreement.write(
            {
                "name": self.name,
                "description": self.name,
                "template_id": self.template_id.id,
                "revision": 0,
            }
        )
        return agreement

    def create_agreement(self):
        agreement = self._create_agreement()
        return agreement.action_view_agreement(agreement)
