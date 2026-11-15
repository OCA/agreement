Companies sign many contracts with their customers and suppliers:
maintenance contracts, framework agreements, supply and service agreements,
non-disclosure agreements. Without a dedicated record, these documents end
up as attachments on a partner or on a sales order, and nobody can quickly
answer which agreements exist, with whom, and when they start or end.

This module answers that need with a dedicated *Agreement* record. It is
deliberately minimal and only stores what every agreement has in common:
identification, partner, sale or purchase domain and dates. It also provides
the *Agreements* application menu, the access roles and the settings page
that the other modules of the OCA `agreement` repository build upon, so a
company installs only the features it needs:

- `agreement_stage`: stage workflow for agreements.
- `agreement_signature`: signatories and signed document of agreements.
- `agreement_revision`: versions and revisions of agreements.
- `agreement_termination`: term dates, notices and termination tracking.
- `agreement_type`: hierarchical agreement types with sub-types.
- `agreement_legal` and `agreement_legal_content`: legal aspects and
  legal content of agreements.
- `agreement_sale`, `agreement_product`, `agreement_project` and
  `agreement_rebate`: links between agreements and sales, products,
  projects and rebates.

The module is multi-company aware: an agreement belongs to a company and
is only visible to users allowed to work in that company. Agreements
without a company are shared.
