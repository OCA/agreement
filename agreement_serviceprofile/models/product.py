# Copyright (C) 2019 - TODAY, Open Source Integrators
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    service_tracking = fields.Selection(
        selection_add=[
            ("serviceprofile", "Service Profile"),
        ],
        ondelete={"serviceprofile": "set default"},
    )

    def _service_tracking_blacklist(self):
        return super()._service_tracking_blacklist() + ["serviceprofile"]
