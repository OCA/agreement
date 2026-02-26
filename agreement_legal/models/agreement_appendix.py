# Copyright (C) 2018 - TODAY, Pavlov Media
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class AgreementAppendix(models.Model):
    _name = "agreement.appendix"
    _inherit = ["agreement.dynamic.content.mixin"]
    _description = "Agreement Appendices"
    _order = "sequence"

    name = fields.Char(required=True)
    title = fields.Char(
        required=True, help="The title is displayed on the PDF. The name is not."
    )
    sequence = fields.Integer(default=10)
    content = fields.Html()
    dynamic_content = fields.Html(
        compute="_compute_dynamic_content", help="compute dynamic Content"
    )
    agreement_id = fields.Many2one("agreement", string="Agreement", ondelete="cascade")
    active = fields.Boolean(
        default=True,
        help="If unchecked, it will allow you to hide this appendix without "
        "removing it.",
    )

    # compute the dynamic content for jinja expression
    def _compute_dynamic_content(self):
        MailTemplates = self.env["mail.template"]
        for appendix in self:
            lang = (
                appendix.agreement_id
                and appendix.agreement_id.partner_id.lang
                or "en_US"
            )
            content = MailTemplates.with_context(lang=lang)._render_template(
                appendix.content, "agreement.appendix", [appendix.id]
            )[appendix.id]
            appendix.dynamic_content = content
