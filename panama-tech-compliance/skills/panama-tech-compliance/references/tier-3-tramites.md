# Tier 3 — Trámites: obligations with no code to audit

These have no file, no line number, and no fix that can be written. They are **filings, contracts, designations, and registrations**.

**Emit them as a separate checklist, never as code findings.** A "finding" whose fix is "sign a contract" wastes the reader's attention and makes the code findings look padded. Keep the two lists visually distinct in the report.

Every deadline and authority below is **⚠ PIN — verify before stating**.

## Output format

A table, with the derived column filled in from what the audit actually found:

| # | Obligation | Trigger | Where / with whom | Derived from |
|---|---|---|---|---|

The last column is what makes this useful rather than generic: `custodio contract — SendGrid` is actionable, `sign vendor contracts` is not. Populate it from the vendors, transfers, and data classes the code audit enumerated.

## Data protection (Ley 81 / ANTAI)

- **Custodio (processor) contracts** — one per third party that receives personal data. List them by name from the audit: cloud, email, SMS, analytics, CRM, support desk, payment processor, LLM/AI vendors, offshore contractors. Trigger: any PII leaving the responsable's control.
- **Internal data-protection policy** and records of processing activities — the accountability documentation ANTAI expects to see on inspection.
- **Privacy notice published and versioned** — the code stores a version pointer (see `ley-81-datos-personales.md`); publishing and legal review are human tasks.
- **Cross-border transfer safeguards** — the mechanism and any authorization/documentation for each destination the audit found. ⚠ PIN what's required.
- **Breach-notification runbook** — who decides it's notifiable, who drafts, who files with ANTAI, who notifies subjects, within what window. ⚠ PIN the deadline. Detection is code; the decision chain is not. A runbook that exists only after the incident is worthless.
- **Rights-request intake ownership** — a named human answers the published channel and meets the statutory clock.
- **Any ANTAI registration or notification duty** — ⚠ PIN whether one applies to this entity type; check `antai.gob.pa` rather than assuming.

## Electronic signature (Ley 51 de 2008)

- **PSC selection and certificate procurement** from a provider registered with the Dirección Nacional de Firma Electrónica.
- **Certificate renewal ownership** — a named owner and a calendar date. Expiry silently breaks signing and, separately, invoicing.
- **Registration as a storage/certification provider** — only if the business itself offers those services. ⚠ PIN.

## Electronic invoicing (SFEP / DGI)

- **SFEP enrollment** and channel selection (free tool vs. PAC) — see the 2026 thresholds in `factura-electronica-sfep.md`.
- **PAC contract** where volume or income exceeds the free-tool ceiling.
- **Fiscal certificate** procurement and renewal.
- **Contingency procedure documented** for DGI/PAC outages — the code handles the queue, a human handles the declaration.
- **Fiscal retention** of electronic documents. ⚠ PIN the period.

## Consumer (Ley 45 / ACODECO)

- **Terms and conditions reviewed by counsel** — the draft the skill produces is a draft.
- **Complaint channel** with a named responder, and awareness of ACODECO's process.
- **Substantiation files** for any advertising claim the audit flagged.

## Sector (only if Tier 2 applied)

- **AML**: compliance officer designation, manual, staff training, regulator registration, suspicious-activity reporting channel.
- **Credit data**: agreement with the credit bureau; consent-text review.
- **Public sector**: designated public-information officer; proactive-publication inventory.
- **Health**: clinical-records custody and retention policy.
- **Telecom**: ASEP concession or registration.

## Corporate baseline

- Entity registration and operations notice (aviso de operación) appropriate to the activity.
- IP assignment in employment and contractor agreements — otherwise the company may not own the code the audit just reviewed.

## Closing line for the report

State plainly: this checklist is derived from what the code showed, it is not exhaustive for the business, and completing it is not the same as being compliant. Recommend counsel review for anything with a ⚠ PIN that could not be verified from source.
