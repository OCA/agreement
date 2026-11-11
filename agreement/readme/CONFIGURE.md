## Access rights

The module creates an *Agreement* privilege with three roles. Assign them in
*Settings \> Users & Companies \> Users*, tab *Access Rights*:

- *Read-Only Users*: see the *Agreements* menu and read agreements.
- *User*: create, edit, delete and archive agreements, and read agreement
  types. When the module is installed, every existing internal user
  receives this role.
- *Manager*: in addition, manage agreement types and the *Agreements*
  settings.

Agreement types and agreement templates are available to every user with
one of these roles.

## Settings

Go to *Agreements \> Configuration \> Settings* (Manager role required).

![Agreements settings](../static/description/screenshot_settings.png)

- *Advanced Features* offers shortcuts to the agreement types and agreement
  templates and lets you install the extension modules for signatures,
  termination, stages, hierarchical types, revisions and legal content.
- *Connections* lets you install the modules linking agreements to
  projects, sales, rebates and products.

## Agreements of contacts on the partner form

By default, the *Agreements* smart button on the partner form only shows
the agreements linked directly to that partner. To also show the
agreements of its contacts on a company:

1. Activate the developer mode.
2. Go to *Settings \> Technical \> System Parameters* and create a
   parameter with the key `agreement.partner_show_child_agreements` and the
   value `True`.

The smart button of a company then counts and opens its own agreements and
the agreements of all its contacts. The smart button of a contact still
shows only the agreements of that contact. Delete the parameter to restore
the default behavior.

## Agreement types

Go to *Agreements \> Configuration \> Types* (Manager role required) and
create the types you need. Each type has a name and a default domain
(*Sale* or *Purchase*) that is applied to agreements of that type. Types
can be archived.
