This module lets portal users see the agreements linked to their commercial
partner (or agreements they follow) in the "My Account" area of the portal.

It adds:

- an **Agreements** card on the portal home page with a record counter,
- a paginated, sortable list at `/my/agreements`,
- a detail page per agreement, shareable with a portal access token.

Only the fields of the base `agreement` module are shown (name, reference,
start and end dates, partner). Extensions displaying fields from other
agreement modules can inherit the `portal_agreement_page` template.
