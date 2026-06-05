# Agreement Legal Report Custom — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a standalone v16 module `agreement_legal_report_custom` that overrides the QWeb report `agreement_legal.report_agreement_document` with Moka's styled French layout, without modifying the OCA module.

**Architecture:** Pure view-inheritance module (no Python). One template record inherits `agreement_legal.report_agreement_document` and `xpath … position="replace"` swaps the whole `t-name` block. FR/v17 fields (`siren`, `partner_id.company_registry`) are wrapped in `t-if` `_fields` guards so the PDF never crashes; `l10n_fr_siret` is a hard dependency for the common case.

**Tech Stack:** Odoo 16.0 Community, QWeb/XML, Docker (`odoo16` service, DB `moka-dev`). Module path `~/Moka/16.0/agreement/agreement_legal_report_custom/` is mounted at `/home/odoo/src/user`.

---

## File Structure

```
agreement_legal_report_custom/
├── __init__.py            # empty
├── __manifest__.py        # depends agreement_legal + l10n_fr_siret
├── README.rst
└── report/
    └── agreement_report.xml   # inherit + xpath replace of the report template
```

---

### Task 1: Module scaffold (manifest + init)

**Files:**
- Create: `agreement_legal_report_custom/__init__.py`
- Create: `agreement_legal_report_custom/__manifest__.py`

- [ ] **Step 1: Create empty `__init__.py`**

(No Python in this module.)

```python
```

- [ ] **Step 2: Create `__manifest__.py`**

```python
# Copyright 2026 Moka Tourisme
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Agreement Legal Report Custom",
    "summary": "Custom French QWeb layout for the agreement legal report",
    "version": "16.0.1.0.0",
    "category": "Partner",
    "author": "Moka Tourisme, Odoo Community Association (OCA)",
    "website": "https://github.com/Moka-Tourisme/agreement",
    "license": "AGPL-3",
    "depends": [
        "agreement_legal",
        "l10n_fr_siret",
    ],
    "data": [
        "report/agreement_report.xml",
    ],
    "installable": True,
}
```

- [ ] **Step 3: Commit**

```bash
git add agreement_legal_report_custom/__init__.py agreement_legal_report_custom/__manifest__.py
git commit -m "[ADD] agreement_legal_report_custom: module scaffold"
```

---

### Task 2: Report override template

**Files:**
- Create: `agreement_legal_report_custom/report/agreement_report.xml`

- [ ] **Step 1: Create `report/agreement_report.xml`**

Inherit the OCA template and replace the inner `t-name` node with the styled
content. The three FR/v17 field spans are guarded with `_fields` checks
(`doc.company_id.siren`, `doc.partner_id.siren`, `doc.partner_id.company_registry`);
`doc.company_id.company_registry` stays unguarded (exists in v16 core).

```xml
<?xml version="1.0" encoding="utf-8" ?>
<odoo>
    <template
        id="report_agreement_document_custom"
        inherit_id="agreement_legal.report_agreement_document"
    >
        <xpath
            expr="//t[@t-name='agreement.report_agreement_document']"
            position="replace"
        >
            <t t-name="agreement.report_agreement_document">
                <t t-call="web.html_container">
                    <t t-foreach="docs" t-as="doc">
                        <t t-call="web.external_layout">
                            <style type="text/css">
                                body { font-family: 'Arial', sans-serif; font-size: 10pt; color: #1a1a1a; }
                                p, li { text-align: justify; line-height: 1.2; margin-bottom: 6px; margin-top: 0; }
                                .doc-title-block { text-align: center; padding: 40px 0 30px 0; border-bottom: 3px solid #2c2c2c; margin-bottom: 30px; }
                                .doc-title-block img { width: 220px; margin-bottom: 30px; display: block; margin-left: auto; margin-right: auto; }
                                .doc-title-block h1 { font-size: 22pt; font-weight: bold; text-transform: uppercase; letter-spacing: 2px; color: #1a1a1a; margin-bottom: 8px; }
                                .doc-title-block .subtitle { font-size: 11pt; color: #555555; font-style: italic; margin-top: 6px; }
                                h2 { font-size: 13pt; font-weight: bold; text-transform: uppercase; letter-spacing: 1px; color: #1a1a1a; border-bottom: 2px solid #1a1a1a; padding-bottom: 4px; margin-top: 36px; margin-bottom: 12px; }
                                h3 { font-size: 11pt; font-weight: bold; color: #2c2c2c; margin-top: 18px; margin-bottom: 8px; border-left: 3px solid #555555; padding-left: 8px; }
                                h4 { font-size: 10pt; font-weight: bold; color: #333333; margin-top: 12px; margin-bottom: 6px; text-decoration: underline; }
                                .section_tbody td p { margin-bottom: 3px; margin-top: 3px; line-height: 1.5; }
                                ul, ol { margin-left: 20px; margin-bottom: 8px; padding-left: 16px; }
                                li { margin-bottom: 4px; }
                                .signature-table { width: 100%; border-collapse: collapse; margin-top: 40px; }
                                .signature-table th { background-color: #2c2c2c; color: #ffffff; font-size: 10pt; font-weight: bold; text-align: center; padding: 8px 12px; border: 1px solid #2c2c2c; }
                                .signature-table td { vertical-align: top; padding: 16px 20px; border: 1px solid #cccccc; width: 50%; }
                                .signature-table td p { margin-bottom: 6px; text-align: left; }
                                .signature-table img { height: 80px; margin-top: 10px; }
                                .page-break-after { page-break-after: always; }
                                .appendix-title { font-size: 16pt; font-weight: bold; text-transform: uppercase; border-bottom: 2px solid #1a1a1a; padding-bottom: 6px; margin-bottom: 20px; page-break-before: always; }
                                .non-contractuel { font-size: 8pt; color: #888888; text-align: center; margin-top: 20px; font-style: italic; }
                                address { font-style: normal; line-height: 1.6; margin-bottom: 8px; }
                            </style>
                            <div id="couverture" class="page-break-after">
                                <div style="text-align: center; padding: 20px 0;">
                                    <img
                                        t-if="doc.company_id.logo"
                                        t-attf-src="data:image/*;base64,{{doc.company_id.logo}}"
                                        style="width: 250px;"
                                    />
                                    <h1 t-field="doc.template_id.name" />
                                    <div name="description">
                                        <span t-field="doc.partner_id.name" />
                                    </div>
                                </div>
                                <h2>Parties</h2>
                                <t t-if="doc.use_parties_content">
                                    <div name="parties">
                                        <p t-field="doc.dynamic_parties" />
                                    </div>
                                </t>
                                <t t-if="not doc.use_parties_content">
                                    <div name="parties">
                                        <h3>ENTRE LES SOUSSIGNÉS :</h3>
                                        <p>
                                            La Société <strong><span
                                                    t-field="doc.company_id.partner_id.name"
                                                /></strong>,
                                            SAS au capital de 10 000€, dont le siège social est situé au
                                            <span t-field="doc.company_id.partner_id.street" />,
                                            <span t-field="doc.company_id.partner_id.zip" />
                                            <span t-field="doc.company_id.partner_id.city" />
                                            (<span
                                                t-field="doc.company_id.partner_id.country_id.name"
                                            />),
                                            immatriculée au registre du commerce et des sociétés de
                                            <span t-field="doc.company_id.company_registry" />,
                                            sous le n°<t
                                                t-if="'siren' in doc.company_id._fields"
                                            ><span t-field="doc.company_id.siren" /></t>,
                                            représentée par <span
                                                t-field="doc.company_contact_id.name"
                                            />,
                                            <span t-field="doc.company_contact_id.title.name" />,
                                            son représentant légal actuellement en fonctions, domicilié en cette qualité audit siège,
                                        </p>
                                        <p><em>Ci-après désignée "le Prestataire",</em></p>
                                        <p>D'UNE PART,</p>
                                        <h3>ET :</h3>
                                        <p>
                                            <strong><span t-field="doc.partner_id.name" /></strong>,
                                            <span t-field="doc.partner_id.company_type" />,
                                            dont le siège social est situé
                                            <span t-field="doc.partner_id.street" />,
                                            <span t-field="doc.partner_id.zip" />
                                            <span t-field="doc.partner_id.city" />
                                            (<span t-field="doc.partner_id.country_id.name" />),
                                            immatriculée au registre du commerce et des sociétés de
                                            <t
                                                t-if="'company_registry' in doc.partner_id._fields"
                                            ><span t-field="doc.partner_id.company_registry" /></t>
                                            sous le n°<t
                                                t-if="'siren' in doc.partner_id._fields"
                                            ><span t-field="doc.partner_id.siren" /></t>,
                                            représentée par <span
                                                t-field="doc.partner_contact_id.name"
                                            />,
                                            <span t-field="doc.partner_contact_id.function" />,
                                            son représentant légal actuellement en fonctions, domicilié en cette qualité audit siège,
                                        </p>
                                        <p><em>Ci-après désignée "le Client",</em></p>
                                        <p>D'AUTRE PART,</p>
                                        <p><strong>INDIVIDUELLEMENT DÉNOMMÉE «PARTIE» ET ENSEMBLE DÉNOMMÉES «PARTIES».</strong></p>
                                    </div>
                                </t>
                            </div>
                            <div id="contenu" class="page-break-after">
                                <t t-if="doc.recital_ids">
                                    <div t-foreach="doc.recital_ids" t-as="r">
                                        <t t-if="r.title">
                                            <h3 t-field="r.title" />
                                        </t>
                                        <p t-field="r.dynamic_content" />
                                    </div>
                                </t>
                                <div t-foreach="doc.sections_ids" t-as="s">
                                    <t t-if="s.title">
                                        <h3 t-field="s.title" />
                                    </t>
                                    <p t-field="s.dynamic_content" />
                                    <div t-foreach="s.clauses_ids" t-as="c">
                                        <t t-if="c.title">
                                            <h4 t-field="c.title" />
                                        </t>
                                        <p t-field="c.dynamic_content" />
                                    </div>
                                </div>
                                <t t-if="special_term">
                                    <h2>Special Terms</h2>
                                    <div name="special_term">
                                        <p t-field="doc.dynamic_special_terms" />
                                    </div>
                                </t>
                                <h2>Signatures</h2>
                                <table class="table table-condensed">
                                    <theader>
                                        <tr>
                                            <th width="50%">Partner</th>
                                            <th width="50%">Company</th>
                                        </tr>
                                    </theader>
                                    <tbody class="section_tbody">
                                        <tr>
                                            <td>
                                                <p t-field="doc.partner_id" />
                                                <p>
                                                    By:
                                                    <span t-field="doc.partner_contact_id.name" />,
                                                    <span t-field="doc.partner_contact_id.function" />
                                                </p>
                                                <p>Date:</p>
                                            </td>
                                            <td>
                                                <p t-field="doc.company_id.partner_id" />
                                                <p>
                                                    By:
                                                    <span t-field="doc.company_contact_id.name" />,
                                                    <span t-field="doc.company_contact_id.function" />
                                                </p>
                                                <p>
                                                    Date:
                                                    <span t-field="doc.company_signed_date" />
                                                </p>
                                                <img
                                                    t-if="doc.signed_contract"
                                                    t-attf-src="data:image/*;base64,{{doc.signed_contract}}"
                                                    style="height: 80px;"
                                                />
                                            </td>
                                        </tr>
                                    </tbody>
                                </table>
                            </div>
                            <div id="annexes">
                                <div t-foreach="doc.appendix_ids" t-as="a">
                                    <div class="page-break-after">
                                        <h1 t-field="a.title" />
                                        <p t-field="a.dynamic_content" />
                                    </div>
                                </div>
                            </div>
                        </t>
                    </t>
                </t>
            </t>
        </xpath>
    </template>
</odoo>
```

- [ ] **Step 2: Validate XML is well-formed**

Run: `python3 -c "import xml.dom.minidom,sys; xml.dom.minidom.parse('agreement_legal_report_custom/report/agreement_report.xml'); print('OK')"`
Expected: `OK`

- [ ] **Step 3: Commit**

```bash
git add agreement_legal_report_custom/report/agreement_report.xml
git commit -m "[ADD] agreement_legal_report_custom: override report_agreement_document"
```

---

### Task 3: README

**Files:**
- Create: `agreement_legal_report_custom/README.rst`

- [ ] **Step 1: Create minimal README.rst** (OCA-style short form)

```rst
=============================
Agreement Legal Report Custom
=============================

Overrides the ``agreement_legal.report_agreement_document`` QWeb report with a
styled French layout (cover page, "Parties" boilerplate, sections/clauses,
signatures, appendices).

FR-specific fields (``siren``, partner ``company_registry``) are rendered only
when present, so the report renders on any localization.

**Configuration**

The company boilerplate (legal form, share capital) is currently hard-coded in
the template. Edit ``report/agreement_report.xml`` to adapt it.

**Credits**

* Moka Tourisme
```

- [ ] **Step 2: Commit**

```bash
git add agreement_legal_report_custom/README.rst
git commit -m "[ADD] agreement_legal_report_custom: README"
```

---

### Task 4: Install + render verification

- [ ] **Step 1: Install the module (pulls agreement_legal + l10n_fr_siret, with demo)**

```bash
cd ~/Moka/16.0 && docker compose run --rm odoo16 \
  odoo -d moka-dev -i agreement_legal_report_custom \
  --without-demo=False --stop-after-init
```
Expected: ends with `Modules loaded.` and no traceback. Confirm template loaded:
the log shows the module installing without ParseError.

- [ ] **Step 2: Restart to reload the registry**

```bash
cd ~/Moka/16.0 && docker compose restart odoo16
```

- [ ] **Step 3: Render the report headless on a demo agreement (smoke test)**

```bash
cd ~/Moka/16.0 && docker compose exec -T odoo16 odoo shell -d moka-dev --no-http << 'PY'
agr = env['agreement'].search([], limit=1)
assert agr, "no agreement record to render"
report = env.ref('agreement_legal.partner_agreement_contract_document')
pdf, _ = report._render_qweb_pdf(agr.ids)
print("PDF_BYTES", len(pdf))
PY
```
Expected: prints `PDF_BYTES <n>` with n > 0 and **no QWeb/Field traceback**.
(If `odoo shell` heredoc is unavailable, render via the UI: open an agreement →
Print → *Agreement*.)

- [ ] **Step 4: Verify the override actually replaced the original**

The rendered PDF/HTML must show the French cover ("ENTRE LES SOUSSIGNÉS :")
rather than the OCA default ("Company Information"). Inspect via UI preview
(Print → *Agreement Preview*) or grep the HTML render:

```bash
cd ~/Moka/16.0 && docker compose exec -T odoo16 odoo shell -d moka-dev --no-http << 'PY'
agr = env['agreement'].search([], limit=1)
report = env.ref('agreement_legal.partner_agreement_contract_document_preview')
html, _ = report._render_qweb_html(agr.ids)
body = html.decode() if isinstance(html, bytes) else html
assert "SOUSSIGNÉS" in body or "PARTIES" in body, "override not applied"
print("OVERRIDE_OK")
PY
```
Expected: prints `OVERRIDE_OK`.

---

## Self-Review notes

- **Spec coverage:** override technique (Task 2), dependency + guards (Task 2),
  module name/location (Task 1), crash-proof on missing FR module (Task 4 Step 3),
  override-applied check (Task 4 Step 4). All spec sections covered.
- **Guards:** three guarded spans match the spec table exactly; `company_id.company_registry` intentionally unguarded.
- **No placeholders:** all file contents are complete and literal.
```
