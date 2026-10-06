# Copyright (C) 2018 - TODAY, Pavlov Media
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class AgreementType(models.Model):
    _inherit = "agreement.type"

    parent_type_id = fields.Many2one(
        "agreement.type",
        string="Parent Type",
        ondelete="cascade",
        help="When set, this type is a sub-type of the selected parent type.",
    )
    child_type_ids = fields.One2many(
        "agreement.type", "parent_type_id", string="Sub-Types"
    )
    review_user_id = fields.Many2one(
        "res.users", help="User assigned automatically the activity on review date"
    )
    review_days = fields.Integer()

    @api.depends("name")
    def _compute_display_name(self):
        for agreement_type in self:
            agreement_type.display_name = (
                f"{agreement_type.parent_type_id.display_name} / {agreement_type.name}"
                if agreement_type.parent_type_id
                else agreement_type.name
            )
