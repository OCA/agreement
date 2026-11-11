# Copyright (C) 2018 - TODAY, Pavlov Media
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models

SHOW_CHILD_AGREEMENTS_PARAM = "agreement.partner_show_child_agreements"


class Partner(models.Model):
    _inherit = "res.partner"

    agreement_ids = fields.One2many("agreement", "partner_id", string="Agreements")
    agreements_count = fields.Integer(compute="_compute_agreements_count")

    @api.model
    def _agreement_show_child_agreements(self):
        """Return whether the Agreements smart button also includes the
        agreements of the child contacts (system parameter)."""
        return bool(
            self.env["ir.config_parameter"]
            .sudo()
            .get_param(SHOW_CHILD_AGREEMENTS_PARAM, False)
        )

    @api.depends("agreement_ids")
    def _compute_agreements_count(self):
        self.agreements_count = 0
        show_child = self._agreement_show_child_agreements()
        partners = self
        if show_child:
            partners = self.with_context(active_test=False).search_fetch(
                [("id", "child_of", self.ids)], ["parent_id"]
            )
        results = self.env["agreement"]._read_group(
            [("partner_id", "in", partners.ids)],
            ["partner_id"],
            ["__count"],
        )
        self_ids = set(self._ids)
        for partner, count in results:
            if not show_child:
                if partner.id in self_ids:
                    partner.agreements_count = count
                continue
            # add the count to the partner and to all its parents in self
            while partner:
                if partner.id in self_ids:
                    partner.agreements_count += count
                partner = partner.parent_id

    def action_open_agreement(self):
        self.ensure_one()
        action = self.env["ir.actions.act_window"]._for_xml_id(
            "agreement.agreement_action"
        )
        operator = "child_of" if self._agreement_show_child_agreements() else "="
        action.update(
            {
                "domain": [("partner_id", operator, self.id)],
                "context": {"default_partner_id": self.id},
            }
        )
        return action
