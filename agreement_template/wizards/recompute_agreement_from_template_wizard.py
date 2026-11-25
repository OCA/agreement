# Copyright 2026 Antoni Marroig (APSL-Nagarro)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class RecomputeAgreementFromTemplateWizard(models.TransientModel):
    _name = "recompute.agreement.from.template.wizard"
    _description = "Recompute Agreement From Template Wizard"

    agreement_id = fields.Many2one("agreement", required=True, readonly=True)
    template_id = fields.Many2one(
        "agreement",
        related="agreement_id.template_id",
        readonly=True,
    )

    def action_recompute_from_template(self):
        self.ensure_one()
        self.agreement_id.recompute_from_template()
        return {"type": "ir.actions.act_window_close"}
