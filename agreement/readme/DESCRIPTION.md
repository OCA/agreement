This module adds an *Agreement* object to Odoo so that contracts and other
agreements concluded with customers and suppliers can be registered and
followed in one place. Each agreement has a code, a name, a partner, a
*Sale* or *Purchase* domain, and signature, start and end dates. The partner
may be a contact person of a company: the company is stored on the
agreement as *Commercial Entity*, and the agreement code must be unique per
commercial entity and company.

Agreements have a chatter with tracked field changes and activities, can be
archived, are listed on the partner form through a smart button, and are
protected by three access roles (Read-Only Users, User and Manager).
Optionally, agreements can be classified with *agreement types*, which
preset the domain, and flagged as *templates* that can be duplicated to
create new agreements.

This module is the base of the OCA agreement modules. Its settings page
lets you install extensions for stages, signatures, revisions, termination,
legal content, and links to sales, products, projects and rebates.
