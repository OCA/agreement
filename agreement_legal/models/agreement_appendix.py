# Copyright (C) 2018 - TODAY, Pavlov Media
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class AgreementAppendix(models.Model):
    _name = "agreement.appendix"
    _inherit = "agreement.dynamic.content.mixin"
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

    def _get_render_partner(self):
        return self.agreement_id.partner_id

    @api.depends("content", "agreement_id.partner_id.lang")
    def _compute_dynamic_content(self):
        for appendix in self:
            appendix.dynamic_content = appendix._render_dynamic("content")
