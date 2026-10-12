# Copyright (C) 2018 - TODAY, Pavlov Media
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class Agreement(models.Model):
    _inherit = "agreement"

    version = fields.Integer(
        default=1,
        copy=False,
        help="The versions are used to keep track of document history and "
        "previous versions can be referenced.",
    )
    revision = fields.Integer(
        default=0, copy=False, help="The revision will increase with every save event."
    )
    previous_version_agreements_ids = fields.One2many(
        "agreement",
        compute="_compute_previous_version_agreements",
        string="Previous Versions",
        context={"active_test": False},
    )

    state = fields.Selection(
        [("draft", "Draft"), ("active", "Active"), ("inactive", "Inactive")],
        default="draft",
        tracking=True,
    )

    parent_agreement_id = fields.Many2one(
        "agreement",
        string="Parent Agreement",
        help="Link this agreement to a parent agreement. For example if this "
        "agreement is an amendment to another agreement. This list will "
        "only show other agreements related to the same account.",
    )
    child_agreements_ids = fields.One2many(
        "agreement",
        "parent_agreement_id",
        string="Child Agreements",
        copy=False,
        domain=[("active", "=", True)],
    )

    create_uid_parent = fields.Many2one(
        "res.users", compute="_compute_create_uid_parent", string="Created by (parent)"
    )
    create_date_parent = fields.Datetime(
        related="parent_agreement_id.create_date", string="Created on (parent)"
    )

    @api.depends("parent_agreement_id")
    def _compute_previous_version_agreements(self):
        for agreement in self:
            previous_versions = self.search(
                [
                    ("parent_agreement_id", "=", agreement.id),
                    "|",
                    ("active", "=", True),
                    ("active", "=", False),
                ]
            )
            agreement.previous_version_agreements_ids = previous_versions

    @api.depends("parent_agreement_id")
    def _compute_create_uid_parent(self):
        for agreement in self:
            agreement.create_uid_parent = (
                agreement.parent_agreement_id.create_uid
                if agreement.parent_agreement_id
                else agreement.create_uid
            )
            agreement.create_date_parent = (
                agreement.parent_agreement_id.create_date
                if agreement.parent_agreement_id
                else agreement.create_date
            )

    def _get_old_version_default_vals(self):
        self.ensure_one()
        default_vals = {
            "name": f"{self.name} - OLD VERSION",
            "active": False,
        }
        return default_vals

    def _get_old_version_default_vals(self):
        self.ensure_one()
        default_vals = {
            "name": f"{self.name} - OLD VERSION",
            "active": False,
            "version": self.version,
            "revision": self.revision,
            "code": f"{self.code}-V{str(self.version)}",
            "parent_agreement_id": self.id,
        }

        return default_vals

    def _get_new_agreement_default_vals(self):
        vals = super()._get_new_agreement_default_vals()
        vals["version"] = 1
        vals["revision"] = 0
        return vals

    def recompute_from_template(self):
        res = super().recompute_from_template()
        if self.template_id:
            template = self.template_id
            self.child_agreements_ids.unlink()
            for child in template.child_agreements_ids:
                child.copy({"parent_agreement_id": self.id})
        return res

    # Create New Version Button
    def create_new_version(self):
        for rec in self:
            if not rec.state == "draft":
                # Make sure status is draft
                rec.state = "draft"
            # Make a current copy and mark it as old
            rec.copy(default=rec._get_old_version_default_vals())
            # Update version, created by and created on
            rec.update({"version": rec.version + 1})
            # Reset revision to 0 since it's a new version
        return super().write({"revision": 0})

    # Increments the revision on each save action
    def write(self, vals):
        res = True
        for rec in self:
            has_revision = False
            if "revision" not in vals:
                vals["revision"] = rec.revision + 1
                has_revision = True
            res = super(Agreement, rec).write(vals)
            if has_revision:
                vals.pop("revision")
        return res
