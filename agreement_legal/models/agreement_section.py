# Copyright (C) 2018 - TODAY, Pavlov Media
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class AgreementSection(models.Model):
    _name = "agreement.section"
    _inherit = ["agreement.dynamic.content.mixin"]
    _description = "Agreement Sections"
    _order = "sequence"

    name = fields.Char(required=True)
    title = fields.Char(help="The title is displayed on the PDF. The name is not.")
    sequence = fields.Integer()
    agreement_id = fields.Many2one("agreement", string="Agreement", ondelete="cascade")
    clauses_ids = fields.One2many(
        "agreement.clause", "section_id", string="Clauses", copy=True
    )
    content = fields.Html(string="Section Content")
    dynamic_content = fields.Html(
        compute="_compute_dynamic_content", help="compute dynamic Content"
    )
    active = fields.Boolean(
        default=True,
        help="If unchecked, it will allow you to hide the agreement without "
        "removing it.",
    )

    # compute the dynamic content for jinja expression
    def _compute_dynamic_content(self):
        MailTemplates = self.env["mail.template"]
        for section in self:
            lang = (
                section.agreement_id and section.agreement_id.partner_id.lang or "en_US"
            )
            content = MailTemplates.with_context(lang=lang)._render_template(
                section.content, "agreement.section", [section.id]
            )[section.id]
            section.dynamic_content = content
