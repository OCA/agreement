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

    def create_agreement(self):
        return self.template_id.create_new_agreement(
            {
                "name": self.name,
            }
        )
