# Copyright (C) 2018 - TODAY, Pavlov Media
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from datetime import timedelta

from odoo import api, fields, models


class Agreement(models.Model):
    _name = "agreement"
    _inherit = ["agreement"]

    expiration_notice = fields.Integer(
        string="Exp. Notice (Days)",
        tracking=True,
        help="Number of Days before expiration to be notified.",
    )
    change_notice = fields.Integer(
        string="Change Notice (Days)",
        tracking=True,
        help="Number of Days to be notified before changes.",
    )
    termination_requested = fields.Date(
        string="Termination Requested Date",
        tracking=True,
        help="Date that a request for termination was received.",
    )
    termination_date = fields.Date(
        tracking=True, help="Date that the contract was terminated."
    )
    notification_address_id = fields.Many2one(
        "res.partner",
        string="Notification Address",
        help="The address to send notifications to, if different from "
        "customer address.(Address Type = Other)",
    )
    to_review_date = fields.Date(
        compute="_compute_to_review_date",
        store=True,
        readonly=False,
        help="Date on which the last modifier is reminded to review the "
        "agreement. Defaults to the end date minus the expiration notice.",
    )

    @api.depends("end_date", "expiration_notice")
    def _compute_to_review_date(self):
        for record in self:
            if record.end_date:
                record.to_review_date = record.end_date - timedelta(
                    days=record.expiration_notice
                )

    @api.model
    def _alert_to_review_date(self):
        """Cron: schedule a review activity for agreements whose review date
        is today, assigned to the user who last modified the agreement."""
        activity_type = self.env.ref(
            "agreement_termination.mail_activity_review_agreement"
        )
        agreements = self.search(
            [
                ("to_review_date", "=", fields.Date.today()),
                ("is_template", "=", False),
            ]
        )
        for agreement in agreements:
            if agreement.activity_ids.filtered(
                lambda a: a.activity_type_id == activity_type
            ):
                continue
            reviewer = agreement.user_id or agreement.write_uid or agreement.create_uid
            agreement.activity_schedule(
                "agreement_termination.mail_activity_review_agreement",
                user_id=reviewer.id,
                note=self.env._("This agreement is going to end soon"),
            )
