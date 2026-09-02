# Copyright (C) 2018 - TODAY, Pavlov Media
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from lxml import etree

from odoo import api, fields, models


class Agreement(models.Model):
    _inherit = "agreement"

    readonly = fields.Boolean(related="stage_id.readonly")

    # Used for Kanban grouped_by view
    @api.model
    def _read_group_stage_ids(self, stages, domain, order=None):
        stage_ids = self.env["agreement.stage"].search(
            [("stage_type", "=", "agreement")]
        )
        return stage_ids

    stage_id = fields.Many2one(
        "agreement.stage",
        string="Stage",
        group_expand="_read_group_stage_ids",
        help="Select the current stage of the agreement.",
        default=lambda self: self._get_default_stage_id(),
        tracking=True,
        index=True,
        copy=False,
    )

    @api.model
    def _get_default_stage_id(self):
        try:
            stage_id = self.env.ref("agreement_legal_stage.agreement_stage_new").id
        except ValueError:
            stage_id = False
        return stage_id

    def _get_old_version_default_vals(self):
        vals = super()._get_old_version_default_vals()
        vals["stage_id"] = self.stage_id.id
        return vals

    def _fill_create_vals(self, vals):
        vals = super()._fill_create_vals(vals)
        if not vals.get("stage_id"):
            vals["stage_id"] = self._get_default_stage_id()
        return vals

    def _exclude_readonly_field(self):
        return ["stage_id"]

    def _get_agreement_readonly_domain(self):
        return "bool(readonly)"

    @api.model
    def get_view(self, view_id=None, view_type=False, **options):
        res = super().get_view(view_id, view_type, **options)
        # Readonly fields
        if view_type == "form":
            doc = etree.XML(res["arch"])
            for node in doc.xpath("//field[@name][not(ancestor::field)]"):
                if node.attrib.get("name") in self._exclude_readonly_field():
                    continue
                new_r_modifier = self._get_agreement_readonly_domain()
                old_r_modifier = node.attrib.get("readonly")
                if old_r_modifier:
                    new_r_modifier = f"({old_r_modifier}) or ({new_r_modifier})"
                node.attrib["readonly"] = new_r_modifier
            res["arch"] = etree.tostring(doc, encoding="unicode")
        return res
