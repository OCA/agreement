# Copyright 2020-2022 Tecnativa - Víctor Martínez
# Copyright (C) 2022 Rafnix Guzman
# Copyright (C) 2026 Pop Solutions
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, http
from odoo.exceptions import AccessError, MissingError
from odoo.http import request

from odoo.addons.portal.controllers.portal import CustomerPortal
from odoo.addons.portal.controllers.portal import pager as portal_pager


class PortalAgreement(CustomerPortal):
    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        if "agreement_count" in counters:
            agreement_model = request.env["agreement"]
            agreement_count = (
                agreement_model.search_count([])
                if agreement_model.has_access("read")
                else 0
            )
            values["agreement_count"] = agreement_count
        return values

    def _agreement_get_page_view_values(self, agreement, access_token, **kwargs):
        values = {
            "page_name": "Agreements",
            "agreement": agreement,
        }
        return self._get_page_view_values(
            agreement, access_token, values, "my_agreements_history", False, **kwargs
        )

    def _get_filter_domain(self, kw):
        return []

    @http.route(
        ["/my/agreements", "/my/agreements/page/<int:page>"],
        type="http",
        auth="user",
        website=True,
    )
    def portal_my_agreements(self, page=1, sortby=None, **kw):
        values = self._prepare_portal_layout_values()
        agreement_model = request.env["agreement"]
        if not agreement_model.has_access("read"):
            return request.redirect("/my")
        domain = self._get_filter_domain(kw)
        searchbar_sortings = {
            "name": {"label": _("Name"), "order": "name desc"},
            "code": {"label": _("Reference"), "order": "code desc"},
        }
        if not sortby:
            sortby = "name"
        order = searchbar_sortings[sortby]["order"]
        agreement_count = agreement_model.search_count(domain)
        pager = portal_pager(
            url="/my/agreements",
            url_args={"sortby": sortby},
            total=agreement_count,
            page=page,
            step=self._items_per_page,
        )
        agreements = agreement_model.search(
            domain, order=order, limit=self._items_per_page, offset=pager["offset"]
        )
        request.session["my_agreements_history"] = agreements.ids[:100]
        values.update(
            {
                "agreements": agreements,
                "page_name": "Agreements",
                "pager": pager,
                "default_url": "/my/agreements",
                "searchbar_sortings": searchbar_sortings,
                "sortby": sortby,
            }
        )
        return request.render("agreement_portal.portal_my_agreements", values)

    @http.route(
        ["/my/agreements/<int:agreement_id>"],
        type="http",
        auth="public",
        website=True,
    )
    def portal_my_agreement_detail(self, agreement_id, access_token=None, **kw):
        try:
            agreement_sudo = self._document_check_access(
                "agreement", agreement_id, access_token
            )
        except (AccessError, MissingError):
            return request.redirect("/my")
        values = self._agreement_get_page_view_values(
            agreement_sudo, access_token, **kw
        )
        return request.render("agreement_portal.portal_agreement_page", values)
