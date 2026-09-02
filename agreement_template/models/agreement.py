# Copyright (C) 2018 - TODAY, Pavlov Media
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class Agreement(models.Model):
    _inherit = "agreement"

    template_id = fields.Many2one(
        "agreement", string="Template", domain=[("is_template", "=", True)]
    )

    @api.model
    def _is_agreement_template_action(self, **options):
        """Tell whether the views are requested by the agreement template action.

        The web client only forwards ``lang`` and ``*_view_ref`` context keys to
        ``get_views``, so ``default_is_template`` never reaches the server from
        the client. The action id is passed along though, which makes it the
        reliable way to tell the template views from the agreement ones. The
        context is still honored for direct server side ``get_view`` calls.
        """
        if self.env.context.get("default_is_template"):
            return True
        action_id = self.env["ir.model.data"]._xmlid_to_res_id(
            "agreement.agreement_template_action", raise_if_not_found=False
        )
        return bool(action_id) and options.get("action_id") == action_id

    @api.model
    def _must_create_from_template(self, **options):
        """Agreements are created through the template wizard, templates aren't."""
        return self.env.user.has_group(
            "agreement.group_use_agreement_template"
        ) and not self._is_agreement_template_action(**options)

    @api.model
    def _must_hide_create(self, **options):
        """Tell whether the create button has to be removed from the views."""
        if self._is_agreement_template_action(**options):
            # templates are a configuration matter, only managers write them
            return not self.env.user.has_group("agreement.group_agreement_manager")
        return self._must_create_from_template(**options)

    @api.model
    def _get_view_cache_key(self, view_id=None, view_type="form", **options):
        key = super()._get_view_cache_key(view_id, view_type, **options)
        return key + (self._must_hide_create(**options),)

    @api.model
    def _get_view(self, view_id=None, view_type="form", **options):
        arch, view = super()._get_view(view_id, view_type, **options)
        if view_type in ("form", "kanban", "list") and self._must_hide_create(
            **options
        ):
            arch.set("create", "0")
        return arch, view

    def _get_new_agreement_default_vals(self):
        self.ensure_one()
        return {
            "name": self.env._("New"),
            # ``is_template`` is not copied, so ``create`` would otherwise fall
            # back on the ``default_is_template`` of the template action context
            "is_template": False,
            "template_id": self.id,
        }

    def action_view_agreement(self):
        return {
            "res_model": "agreement",
            "type": "ir.actions.act_window",
            "view_mode": "form",
            "view_type": "form",
            "res_id": self.id,
        }

    def create_new_agreement(self, vals=None):
        defaults = self._get_new_agreement_default_vals()
        defaults.update(vals or {})
        res = self.copy(defaults)
        return res.action_view_agreement()

    def recompute_from_template(self):
        if self.template_id:
            template = self.template_id
            self.message_post(
                body=self.env._(
                    "Agreement recomputed from template %s",
                    template.display_name,
                )
            )
        return None

    def action_open_recompute_from_template_wizard(self):
        self.ensure_one()
        return {
            "name": self.env._("Recompute From Template"),
            "res_model": "recompute.agreement.from.template.wizard",
            "type": "ir.actions.act_window",
            "view_mode": "form",
            "target": "new",
            "context": {
                "default_agreement_id": self.id,
                "default_template_id": self.template_id.id,
            },
        }
