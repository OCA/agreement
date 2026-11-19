from odoo import api, fields, models


class AgreementDynamicContentMixin(models.AbstractModel):
    _name = "agreement.dynamic.content.mixin"
    _description = "Agreement Dynamic Content Mixin"

    field_id = fields.Many2one(
        "ir.model.fields",
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

    def copy_data(self, default=None):
        vals_list = super().copy_data(default)
        name_field = self._fields.get("name")
        if name_field and "name" not in (default or {}):
            for record, vals in zip(self, vals_list, strict=True):
                if vals is not None:
                    translations = (
                        record._get_stored_translations("name")
                        if name_field.translate
                        else None
                    )
                    vals["name"] = (
                        translations.normalize(record.env, name_field)
                        if translations
                        else record.name
                    )
        return vals_list

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
                [("model", "=", self.field_id.relation)]
            )[0]
        if self.sub_model_object_field_id:
            self.copyvalue = "{{{{object.{}.{} or {}}}}}".format(
                self.field_id.name,
                self.sub_model_object_field_id.name,
                self.default_value or "''",
            )
