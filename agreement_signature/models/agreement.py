# Copyright (C) 2018 - TODAY, Pavlov Media
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class Agreement(models.Model):
    _inherit = "agreement"

    company_signed_date = fields.Date(
        string="Signed on",
        tracking=True,
        help="Date the contract was signed by Company.",
    )
    partner_signed_date = fields.Date(
        string="Signed on (Partner)",
        tracking=True,
        help="Date the contract was signed by the Partner.",
    )
    company_signed_user_id = fields.Many2one(
        "res.users",
        string="Signed By",
        tracking=True,
        help="The user at our company who authorized/signed the agreement or contract.",
    )
    partner_signed_user_id = fields.Many2one(
        "res.partner",
        string="Signed By (Partner)",
        tracking=True,
        help="Contact on the account that signed the agreement/contract.",
    )
    signed_contract_filename = fields.Char(string="Filename")
    signed_contract = fields.Binary(string="Signed Document", tracking=True)

    signature_date = fields.Date(
        compute="_compute_signature_date", store=True, tracking=True
    )

    @api.depends(
        "company_signed_date",
        "partner_signed_date",
    )
    def _compute_signature_date(self):
        for agreement in self:
            if agreement.company_signed_date and agreement.partner_signed_date:
                agreement.signature_date = max(
                    agreement.company_signed_date, agreement.partner_signed_date
                )
            else:
                agreement.signature_date = (
                    agreement.company_signed_date or agreement.partner_signed_date
                )
