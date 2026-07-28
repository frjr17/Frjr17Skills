# Ley 81 de 2019 + D.E. 285 de 2021 — Protección de Datos Personales

Panama's general data-protection regime. In force since **29 March 2021**, regulated by **Decreto Ejecutivo 285 de 28 de mayo de 2021**. Regulator: **ANTAI** (Autoridad Nacional de Transparencia y Acceso a la Información), through its Dirección de Protección de Datos Personales.

This is ~80% of the compliance surface for a typical app. Audit it first and hardest.

## Applies to

Public and private entities that store, process, or transfer personal data **in Panamanian territory** — plus databases held in Panama regardless of where the subject is. Where a sector has its own data rules (banking, credit, health), Ley 81 is the **general regime and minimum floor**, not an alternative: the sector rule adds, it does not excuse.

Key structural point most implementations get wrong: the law splits roles into **responsable del tratamiento** (decides purposes and means) and **custodio / encargado** (processes on the responsable's instructions). Your app is usually the responsable and your vendors are custodios — which means a contract per vendor, and liability that does not transfer away.

## Core obligations to audit

**Lawful basis.** Consent must be obtained **at collection**, tied to a stated purpose, and be demonstrable. Not a pre-ticked box, not buried in T&C, not "by using this site you agree." Bundled consent for unrelated purposes (service + marketing + resale) is the single most common defect. ⚠ PIN the exemptions from consent (contract performance, legal duty, etc.) from the current text before relying on one.

**Purpose limitation.** Data used only for the purpose disclosed at collection. New purpose → new consent. Grep for analytics/ML/enrichment pipelines reading production PII that no notice ever mentioned.

**Data subject rights (ARCO + portabilidad).** Acceso, rectificación, cancelación, oposición, **portabilidad**. There must be a real, reachable channel and an operational path to satisfy each one — including deletion that actually reaches backups, replicas, search indexes, logs, caches, analytics warehouses, and every custodio. ⚠ PIN the response deadlines from D.E. 285; do not state a day count from memory.

**Datos sensibles.** Health, biometrics, religion, political views, sexual life, ethnic origin, and similar carry heightened protection and narrower processing grounds. Grep for them appearing in general-purpose tables, logs, or analytics events. ⚠ PIN the exact enumerated categories.

**Cross-border transfer.** Sending data abroad (a US cloud region, a SaaS vendor, an offshore support team) is regulated, requires disclosure, and requires safeguards. Almost every Panamanian startup on AWS `us-east-1` has an undisclosed transfer. ⚠ PIN the conditions and any adequacy/authorization mechanism.

**Security measures.** Proportionate technical and organizational controls. Overlaps directly with `harden-web-security` — run it and cite the results here rather than re-deriving them.

**Breach notification.** There is a duty to notify affected subjects and/or ANTAI on a security incident. ⚠ PIN the trigger threshold, the recipient, and the deadline — this is a number the model will confidently invent. Audit for whether a **detection and notification path exists at all**; a company that cannot tell it was breached cannot notify.

**Retention.** Data kept only as long as the purpose requires, then deleted or irreversibly anonymized. "Forever, because storage is cheap" is a finding.

**Registro / accountability.** Records of processing activities and internal policy. See `tier-3-tramites.md`.

## What to grep for

- **Consent**: is there a `consents` / `acceptance` record at all? Or just `users.terms_accepted BOOLEAN` with no purpose, version, timestamp, or evidence? A boolean proves nothing to a regulator.
- **Collection points**: every form, signup, webhook, third-party SDK, tracking pixel, session recorder. Each one collects; each needs a basis and a notice line.
- **Rights endpoints**: search for any route implementing access/export/delete. Usually absent entirely → Critical.
- **Deletion reach**: `DELETE FROM users` that leaves rows in `orders`, `events`, `audit_log`, Elasticsearch, S3, the analytics pipeline, and the CRM. Trace what deletion actually touches.
- **Sensitive data**: columns/fields for health, biometrics, ID scans, ethnicity; free-text `notes` fields that inevitably collect them; sensitive values in log lines.
- **Cross-border**: cloud region config, SaaS vendor list in env/config, CDN, email/SMS providers, LLM API calls with PII in the prompt.
- **Retention**: any scheduled deletion/anonymization job. Absent → Medium at minimum.
- **Custodio contracts**: every third party receiving PII needs one — enumerate them from code, hand the list to `tier-3-tramites.md`.
- **Logs**: PII, tokens, and full request bodies in application logs; log retention with no limit.
- **PII in prompts**: personal data sent to any LLM/AI vendor is both a transfer and a purpose question.

## Implementation spec (generate against the installed framework)

Do not add a compliance library. This is a table and a handful of endpoints.

**Consent record** — one row per (subject, purpose, grant/revoke): subject id, purpose key, granted bool, notice/policy version, timestamp, source (`web_signup`, `checkout`), and captured evidence (IP/user-agent or equivalent). Append-only; revocation is a new row, never an UPDATE. Consent is evidence — mutable consent is no consent.

**Rights endpoints** — authenticated, identity-verified, logged:
- *acceso / portabilidad* → machine-readable export of everything held on the subject
- *rectificación* → correction path
- *cancelación* → deletion that fans out to every store and every custodio (queue it; it will not be synchronous)
- *oposición* → per-purpose opt-out that the processing code actually honors

Each request logged with received-at and resolved-at, so the deadline is provable.

**Retention job** — scheduled, per data class, with the rule stated in code next to the class. Anonymization is acceptable where the record must survive for accounting.

**Aviso de privacidad** — in Spanish, at collection: identity of the responsable, purposes, categories collected, recipients and custodios, cross-border transfers, retention, how to exercise rights, contact. Versioned, so a consent row can point at the exact text shown. ⚠ Draft for counsel review — not final text.

## Cross-references

- Credit/financial data → `tier-2-sectoriales.md` (Ley 24 de 2002)
- Health records → `tier-2-sectoriales.md`
- Public-sector systems → `tier-2-sectoriales.md` (Ley 6 de 2002, habeas data)
- Security controls → the `harden-web-security` skill
- Registration, policies, custodio contracts → `tier-3-tramites.md`
