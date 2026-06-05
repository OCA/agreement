=============================
Agreement Legal Report Custom
=============================

Overrides the ``agreement_legal.report_agreement_document`` QWeb report with a
styled French layout (cover page, "Parties" boilerplate, sections/clauses,
signatures, appendices).

FR-specific fields (``siren``, partner ``company_registry``) are rendered only
when present, so the report renders on any localization.

Configuration
=============

The company boilerplate (legal form, share capital) is currently hard-coded in
the template. Edit ``report/agreement_report.xml`` to adapt it.

Credits
=======

* Moka Tourisme
