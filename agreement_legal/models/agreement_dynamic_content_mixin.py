# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class AgreementDynamicContentMixin(models.AbstractModel):
    """Encapsulates the dynamic-field-editor + inline-template rendering pattern.

    Used by ``agreement``, ``agreement.section``, ``agreement.clause``,
    ``agreement.recital`` and ``agreement.appendix`` to produce dynamic content
    fields where ``{{object.x}}`` placeholders inside HTML/Text values are
    expanded against the current record.

    Replaces the previously duplicated dynamic-field block (see OCA PR #105 on
    the 18.0 branch) and the per-model calls to the removed
    ``mail.template._render_template`` API.
    """

    _name = "agreement.dynamic.content.mixin"
    _description = "Agreement Dynamic Content Mixin"

    field_id = fields.Many2one(
        "ir.model.fields",
        string="Field",
        help="""Select target field from the related document model. If it is a
         relationship field you will be able to select a target field at the
         destination of the relationship.""",
    )
    sub_object_id = fields.Many2one(
        "ir.model",
        string="Sub-model",
        help="""When a relationship field is selected as first field, this
         field shows the document model the relationship goes to.""",
    )
    sub_model_object_field_id = fields.Many2one(
        "ir.model.fields",
        string="Sub-field",
        help="""When a relationship field is selected as first field, this
         field lets you select the target field within the destination document
          model (sub-model).""",
    )
    default_value = fields.Char(
        help="Optional value to use if the target field is empty."
    )
    copyvalue = fields.Char(
        string="Placeholder Expression",
        help="""Final placeholder expression, to be copy-pasted in the desired
         template field.""",
    )

    @api.onchange("field_id", "sub_model_object_field_id", "default_value")
    def onchange_copyvalue(self):
        self.sub_object_id = False
        self.copyvalue = False
        if self.field_id and not self.field_id.relation:
            self.copyvalue = "{{{{object.{} or {}}}}}".format(
                self.field_id.name, self.default_value or "''"
            )
            self.sub_model_object_field_id = False
        if self.field_id and self.field_id.relation:
            self.sub_object_id = self.env["ir.model"].search(
                [("model", "=", self.field_id.relation)], limit=1
            )
        if self.sub_model_object_field_id:
            self.copyvalue = "{{{{object.{}.{} or {}}}}}".format(
                self.field_id.name,
                self.sub_model_object_field_id.name,
                self.default_value or "''",
            )

    def _get_render_partner(self):
        """Return the partner whose lang to use when rendering. Override per model."""
        return self.env["res.partner"]

    def _render_dynamic(self, src_field):
        """Render an inline-template source on this single record.

        Replacement for ``mail.template._render_template`` (removed in 19.0).
        Uses ``mail.render.mixin._render_template`` with the inline_template
        engine, which understands the existing ``{{object.x}}`` placeholder
        syntax.
        """
        self.ensure_one()
        src = self[src_field]
        if not src:
            return src
        partner = self._get_render_partner()
        lang = (partner and partner.lang) or "en_US"
        rendered = (
            self.env["mail.render.mixin"]
            .with_context(lang=lang)
            ._render_template(
                src,
                self._name,
                [self.id],
                engine="inline_template",
            )
        )
        return rendered[self.id]
