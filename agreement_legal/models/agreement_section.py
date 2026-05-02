# Copyright (C) 2018 - TODAY, Pavlov Media
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class AgreementSection(models.Model):
    _name = "agreement.section"
    _inherit = "agreement.dynamic.content.mixin"
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

    def _get_render_partner(self):
        return self.agreement_id.partner_id

    @api.depends("content", "agreement_id.partner_id.lang")
    def _compute_dynamic_content(self):
        for section in self:
            section.dynamic_content = section._render_dynamic("content")
