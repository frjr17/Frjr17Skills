# Tier 2 — Sector and adjacent regimes

> Last verified against source: never — written 2026-07-28 from model knowledge. Every ⚠ PIN value is unconfirmed.

Load the sections that match the system. Each is partly verifiable in code; all article numbers here are **⚠ PIN — fetch before citing**. These sit *on top of* Ley 81, never instead of it.

---

## Credit and financial data — Ley 24 de 2002 (APC)

**Applies when**: the system reports to, queries, or stores credit-history data (agencias de información de datos de crédito, e.g. APC).

Credit data has its own consent, accuracy, and dispute rules that predate and sit alongside Ley 81.

Audit: explicit consent captured for the credit query (separate from general T&C, evidenced per query); a dispute/rectification path for contested entries; retention limits on adverse history (⚠ PIN the period); no credit data leaking into general-purpose tables, logs, or analytics; access to credit data restricted and audit-logged per read.

Grep: `apc`, `buro`, `credit_score`, `historial`, `score`, credit-bureau SDK clients, any table storing a score or delinquency flag.

---

## AML / KYC — Ley 23 de 2015 (+ Ley 129 de 2020, beneficiarios finales)

**Applies when**: the system is a regulated sujeto obligado — fintech, payments, remittances, crypto, real estate, corporate services. If unsure whether the business is in scope, that determination is a lawyer question; flag it and continue.

Audit: identity verification actually enforced server-side before transacting (not a UI step that can be skipped — see business-logic flaws in `harden-web-security`); sanctions/PEP screening with a defined rescreening cadence; beneficial-ownership capture for corporate customers; transaction monitoring and suspicious-activity path; record retention (⚠ PIN the period, typically longer than commercial retention and therefore **overriding a Ley 81 deletion request** — state the interaction); tamper-evident audit trail.

Regulated entities also face **SBP / SMV acuerdos** on technology risk, cybersecurity, and outsourcing. ⚠ PIN the applicable acuerdo numbers from `superbancos.gob.pa` / `supervalores.gob.pa` — do not cite one from memory.

Grep: `kyc`, `aml`, `sanction`, `ofac`, `pep`, `beneficial_owner`, `beneficiario_final`, onboarding state machines, transaction-limit logic.

---

## Accessibility — Ley 42 de 1999 (+ AIG norms for public-facing government systems)

**Applies when**: public-sector or government-facing systems (strongest obligation), and as a defensible standard everywhere else.

Panama's equal-opportunity framework for persons with disabilities extends to access to information and services. Government digital services additionally follow **AIG** (Autoridad Nacional para la Innovación Gubernamental) standards. ⚠ PIN the specific WCAG level and version currently required for government systems.

Don't re-derive the audit here — run the **`web-design-guidelines`** skill and cite its output. Minimum bar: keyboard operability, visible focus, contrast, form labels, alt text, no keyboard traps, semantic structure.

---

## Software and content licensing — Ley 64 de 2012 (Derecho de Autor)

**Applies when**: always, at low cost — it's a dependency scan.

Audit: OSS licenses in the dependency tree against how the product ships (copyleft in a proprietary distributed binary is the classic finding); third-party assets — fonts, icons, stock images, sample data — with actual licenses; AI-generated code and assets of unclear provenance; the project's own license and IP assignment for contractors.

Grep: `package.json`/`requirements.txt`/`go.mod`/`Cargo.toml` license fields, `LICENSE` files in vendored code, font and image asset directories.

---

## Public sector — Ley 6 de 2002 (Transparencia, habeas data)

**Applies when**: the system is operated by or for a public entity.

Adds duties Ley 81 does not: proactive publication of specified information, a request channel for public information with statutory response deadlines (⚠ PIN), and **habeas data** as a constitutional remedy — meaning a citizen can compel access/correction through the courts, not only through ANTAI.

Audit: is there a public-information request channel with tracked deadlines; is required information actually published; is the classification of restricted/confidential data documented rather than ad hoc.

---

## Health data — Ley 68 de 2003 (derechos del paciente / historia clínica)

**Applies when**: the system stores clinical records or patient data. ⚠ PIN the law number and scope — verify before citing.

Health data is sensitive under Ley 81 *and* subject to medical-records confidentiality and retention rules. Audit: access control per clinician role with per-access audit logging; patient right to their own record; retention that likely **exceeds** general limits (⚠ PIN); no clinical data in analytics, logs, LLM prompts, or test fixtures. Non-production databases seeded from a production clinical dump is a Critical.

---

## Telecom — Ley 31 de 1996 (ASEP)

**Applies when**: the system provides telecommunications services — VoIP, SMS gateways, connectivity resale. Concession/registration questions are trámites → `tier-3-tramites.md`. Communications metadata is personal data → Ley 81.

---

## Cybercrime — Código Penal, delitos informáticos (+ Convenio de Budapest)

**Applies as**: a scope constraint, not a compliance checklist.

Panama criminalizes unauthorized access, interception, data interference, and related conduct, and has aligned with the Budapest Convention framework (⚠ PIN the adopting law and article ranges).

Two practical uses: (1) it bounds what security testing is lawful — the `harden-web-security` scope guard applies, and testing without written authorization is a criminal question, not a policy one; (2) an incident with criminal exposure has a reporting path distinct from ANTAI breach notification. Note both; don't attempt criminal-law analysis.
