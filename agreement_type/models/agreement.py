# Copyright (C) 2018 - TODAY, Pavlov Media
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from datetime import timedelta

from odoo import api, fields, models


class Agreement(models.Model):
    _inherit = "agreement"

    to_review_date = fields.Date(
        compute="_compute_to_review_date",
        store=True,
        readonly=False,
        help="Date used to warn us some days before agreement expires",
    )

    @api.depends("agreement_type_id", "end_date")
    def _compute_to_review_date(self):
        for record in self:
            if record.end_date:
                record.to_review_date = record.end_date + timedelta(
                    days=-record.agreement_type_id.review_days
                )

    @api.model
    def _alert_to_review_date(self):
        agreements = self.search(
            [
                ("to_review_date", "=", fields.Date.today()),
                ("agreement_type_id.review_user_id", "!=", False),
            ]
        )
        for agreement in agreements:
            if (
                self.env["mail.activity"].search_count(
                    [("res_id", "=", agreement.id), ("res_model", "=", self._name)]
                )
                == 0
            ):
                agreement.activity_schedule(
                    "agreement_legal_type.mail_activity_review_agreement",
                    user_id=agreement.agreement_type_id.review_user_id.id,
                    note=self.env._("Your activity is going to end soon"),
                )
