---
name: panama-tech-compliance
description: Verify and implement compliance with Panamanian technology law — data protection (Ley 81 de 2019 / ANTAI), electronic documents and signatures (Ley 51 de 2008), electronic invoicing (SFEP / DGI), consumer protection (Ley 45 de 2007 / ACODECO), plus sector rules for fintech, health, public sector and accessibility. Audits the codebase for what is verifiable in code, and emits a filing/trámite checklist for what is not. Use when the user asks about Panamanian legal or regulatory compliance, cumplimiento legal en Panamá, Ley 81, protección de datos personales, ANTAI, habeas data, firma electrónica, factura electrónica, CUFE, ACODECO, or whether an app is legal to launch in Panama.
---

# Panama Tech Compliance

Audit a system against Panamanian technology law, report what's non-compliant, then implement the parts that are code.

## Reality check

This is **pre-lawyer triage, not legal advice**. It finds gaps a lawyer would otherwise find at billable rates, and implements the mechanical parts. It does not certify compliance, and it cannot judge how ANTAI, ACODECO, the DGI, or a court would actually rule on a specific fact pattern. Say this in the report, every time.

Two more limits, stated up front so the user calibrates:

- **Only some obligations live in code.** Consent capture, rights endpoints, retention jobs, invoice XML — those are auditable. Registering with an authority, signing a custodio contract, obtaining a certificate — those are trámites. Never dress a trámite up as a code finding; it produces a "fix" that can't be written.
- **The model's memory of Panamanian article numbers, deadlines, and thresholds is not reliable.** See below. This is the single biggest failure mode of this skill.

## Verify against source — MANDATORY

Before asserting **any** article number, deadline, monetary threshold, percentage, or penalty in the report: fetch it. Model recall of Panamanian legal detail is exactly where this turns into confident fabrication.

| Source | Use for |
|---|---|
| `gacetaoficial.gob.pa` | Authoritative text of any ley / decreto ejecutivo |
| `antai.gob.pa` | Ley 81 guidance, ANTAI resolutions, breach & registration procedure |
| `dgi.mef.gob.pa/_7FacturaElectronica` | SFEP rules, PAC list, thresholds, schema versions |
| `firmaelectronica.gob.pa` | Registered PSCs, certificate requirements |
| `acodeco.gob.pa` | Consumer-protection resolutions |
| `superbancos.gob.pa` / `supervalores.gob.pa` | Acuerdos for regulated financial entities |

Rules:
- Reference files here mark uncertain values with **⚠ PIN** — that marker means *do not state this number without fetching it first*.
- If a fetch fails, write `unverified — confirm with counsel` in the finding. Do **not** substitute recall.
- Laws change. A reference file is a map of *what to check*, never a substitute for the current text.

## Router — load only what applies

Read `references/` files on demand, not up front.

| Load | When the system… |
|---|---|
| `ley-81-datos-personales.md` | touches personal data of anyone in Panama — **almost always; start here** |
| `ley-51-firma-electronica.md` | e-signs contracts, accepts signed documents, or stores documents as legal records |
| `factura-electronica-sfep.md` | invoices or takes payment from Panamanian customers |
| `ley-45-consumidor.md` | sells to consumers — pricing, checkout, subscriptions, T&C, ads |
| `tier-2-sectoriales.md` | is fintech/credit, health, public-sector, telecom, or ships third-party code |
| `tier-3-tramites.md` | **always, at the end** — the filings the code can never satisfy |

## Workflow

1. **Scope the system.** Stack, who the users are, what data is collected, where it's stored (in Panama? abroad?), whether there are Panamanian customers/employees, sector, public vs. private, B2C vs. B2B. Sector and audience decide which laws even apply — get this before grepping.
2. **Load the reference files the router selects.**
3. **Audit code against each `What to grep` block.** Trace real flows: where data enters, where it's stored, who can read it, when it's deleted.
4. **Verify every cited number against source** (above).
5. **Report code findings** in the format below, ranked Critical → Low.
6. **Emit the trámite checklist separately** from `tier-3-tramites.md` — task, trigger, owner, where it's filed. Not findings; to-dos for a human.
7. **Implement only after the user approves the report.** Generate against the framework already installed — never add a compliance SDK for what a table and three endpoints cover. Leave one runnable check per non-trivial piece (a test that a deletion request actually deletes, that consent is recorded before first use).

Do not auto-fix before showing findings. A "fix" that silently changes what data the app keeps is a data-loss incident.

## Finding format

```
SEVERITY | Ley/Decreto + article (or "⚠ PIN — unverified") | file:line
Exposure:  what a regulator, a data subject, or a plaintiff would do with this
Fix:       the concrete change
```

Severity, by exposure not by tidiness:

- **Critical** — processing with no lawful basis at all, sensitive data unprotected, no way to honor a rights request, invoicing outside the SFEP where it's mandatory.
- **High** — rights request can't be met in time, no breach-detection path, undisclosed cross-border transfer, no custodio contract for a live processor.
- **Medium** — incomplete privacy notice, retention with no defined limit, weak consent evidence.
- **Low** — wording, placement, documentation gaps.

## What this skill will not do

- Draft or file legal instruments (contratos de custodio, avisos to ANTAI, terms of service) as final text. Produce a **draft marked for counsel review**, never something presented as filing-ready.
- Assert that a system "is compliant." Report what was checked, what passed, what's open, and what needs a lawyer.
- Guess at penalties. Fine ranges are ⚠ PIN, always.
