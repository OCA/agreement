# Copyright (C) 2022 Rafnix Guzman
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class Agreement(models.Model):
    _name = "agreement"
    _inherit = ["agreement", "portal.mixin"]

    def _compute_access_url(self):
        res = super()._compute_access_url()
        for record in self:
            record.access_url = f"/my/agreements/{record.id}"
        return res
