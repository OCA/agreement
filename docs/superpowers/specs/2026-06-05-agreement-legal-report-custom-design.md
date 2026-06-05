# Design — `agreement_legal_report_custom`

Date: 2026-06-05
Odoo: 16.0 Community
Status: approved (pending written-spec review)

## Problem

The OCA module `agreement_legal` ships a hard-coded QWeb report template
`agreement_legal.report_agreement_document` used to render the agreement PDF
(and HTML preview). Moka needs a different, styled French layout (cover page,
"Parties" boilerplate, sections/clauses, signatures, appendices) without
modifying the OCA module, so the OCA mirror stays clean and upgradable.

## Goal

A standalone add-on that overrides the report template with the provided
French/styled version, leaving the OCA module untouched and the report action
unchanged.

## Decisions (validated with user)

1. **Location:** inside this repo at
   `~/Moka/16.0/agreement/agreement_legal_report_custom/`.
2. **Override technique:** view inheritance — `inherit_id` on
   `agreement_legal.report_agreement_document` with an `xpath … position="replace"`
   that swaps the whole `t-name` block. Keeps the inheritance link and is
   cleanly disableable; the report action's `report_name` is untouched.
3. **Missing-field handling:** depend on `l10n_fr_siret` (provides `siren`) **and**
   guard every field not guaranteed in v16 core with a `t-if` on `_fields`, so the
   PDF never crashes even if a localization module is absent.
4. **Module name:** `agreement_legal_report_custom`.

## Field availability (verified against v16 sources)

A `t-field` on a non-existent field path crashes PDF rendering in v16, so each
referenced field was checked:

| Field | v16 status | Provider | Handling |
|---|---|---|---|
| `doc.company_id.company_registry` | exists | core `res.company` | unguarded |
| `doc.partner_id.company_registry` | **absent** (added on `res.partner` in v17) | — | `t-if "'company_registry' in doc.partner_id._fields"` |
| `doc.company_id.siren` | **absent in core l10n_fr** (only `siret`) | OCA `l10n_fr_siret` | `t-if "'siren' in doc.company_id._fields"` |
| `doc.partner_id.siren` | **absent in core l10n_fr** | OCA `l10n_fr_siret` | `t-if "'siren' in doc.partner_id._fields"` |
| `doc.partner_id.company_type` | exists | core `res.partner` | unguarded |
| `doc.company_id.partner_id.{name,street,zip,city,country_id}` | exists | core | unguarded |
| `doc.company_contact_id.{name,title.name,function}` | exists | core `res.partner` | unguarded |
| `doc.partner_contact_id.{name,function}` | exists | core `res.partner` | unguarded |
| `doc.template_id.name` | exists | `agreement` | unguarded |
| `doc.use_parties_content`, `doc.dynamic_parties`, `doc.dynamic_special_terms` | exists | `agreement_legal` | unguarded |
| `doc.recital_ids`, `doc.sections_ids`, `s.clauses_ids`, `doc.appendix_ids` | exists | `agreement_legal` | unguarded |
| `doc.company_signed_date`, `doc.signed_contract` | exists | `agreement_legal` | unguarded |

`l10n_fr_siret` is aggregated in this project via `repos.d/oca.yml` (OCA
`l10n-france`), so the hard dependency resolves. The `t-if` guards keep the
dependency effectively soft at render time.

## Module structure

```
agreement_legal_report_custom/
├── __init__.py            # empty — no Python code
├── __manifest__.py
├── README.rst
└── report/
    └── agreement_report.xml
```

### `__manifest__.py`

- `name`: "Agreement Legal Report Custom"
- `summary`: "Custom French QWeb layout for the agreement legal report"
- `version`: `16.0.1.0.0`
- `license`: `AGPL-3`
- `category`: `Partner`
- `author` / `website`: Moka / OCA style
- `depends`: `["agreement_legal", "l10n_fr_siret"]`
- `data`: `["report/agreement_report.xml"]`
- `installable`: `True`

### `report/agreement_report.xml`

```xml
<odoo>
  <template id="report_agreement_document_custom"
            inherit_id="agreement_legal.report_agreement_document">
    <xpath expr="//t[@t-name='agreement.report_agreement_document']" position="replace">
      <t t-name="agreement.report_agreement_document">
        <!-- provided styled content, with t-if guards on siren / partner company_registry -->
      </t>
    </xpath>
  </template>
</odoo>
```

The content is the user-provided template verbatim, except FR/v17 fields wrapped
in `_fields` guards. Hard-coded boilerplate ("SAS au capital de 10 000€", legal
representation wording) is kept verbatim as specified (flagged as
non-configurable; out of scope for this change).

## Out of scope

- No Python, no new fields, no config parameters.
- No change to the report action records.
- No change to the OCA `agreement_legal` module.

## Verification

1. `docker compose run --rm odoo16 odoo -d <db> -i agreement_legal_report_custom --stop-after-init`
2. `docker compose restart odoo16`
3. Open an agreement → print "Agreement" (PDF) and "Agreement Preview" (HTML):
   the custom French layout renders, no QWeb traceback.
4. Test on a partner/company **without** `l10n_fr_siret` data: guarded blocks are
   skipped, report still renders.
```
