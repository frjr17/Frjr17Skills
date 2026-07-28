# Factura Electrónica — SFEP (DGI)

The **Sistema de Facturación Electrónica de Panamá**, run by the **Dirección General de Ingresos** (DGI/MEF). The most mechanically checkable obligation in this skill: the output is an XML document that either validates against DGI's rules or doesn't.

Load this when the system invoices or takes payment from Panamanian customers.

## Applicability

Electronic invoicing is the valid method of issuing fiscal receipts for taxpayers in scope; **newly incorporated companies have been required to adopt it since January 2022**. Rollout has proceeded in waves by taxpayer category. ⚠ PIN the current in-scope population, any remaining fiscal-printer (equipo fiscal) alternative, and effective dates from `dgi.mef.gob.pa/_7FacturaElectronica` — this schedule has moved repeatedly.

## The two channels — pick correctly, this is a live 2026 trap

1. **Facturador gratuito (free DGI tool)** — as of **1 January 2026**, restricted to taxpayers meeting **both** conditions simultaneously: annual gross income up to **B/.36,000** *and* a maximum of **100 electronic documents per month**. ⚠ PIN both figures before stating them.
2. **PAC (Proveedor Autorizado Calificado)** — a DGI-authorized provider, required for everyone above that ceiling.

Audit finding to look for: a business on the free tool that has grown past either limit, or is projected to cross it. Crossing it means invoicing capacity stops — a revenue-blocking outage disguised as a compliance issue. Check actual volume against the ceiling, don't take the user's word for the tier.

## What to audit

- **Channel fit** — free tool vs. PAC against real invoice volume and income (above).
- **Digital certificate** — electronic documents must be backed by a certificate from a PSC registered with the Dirección Nacional de Firma Electrónica (Ley 51 de 2008). Check expiry handling: an expired cert stops invoicing entirely. → `ley-51-firma-electronica.md`
- **CUFE** — the unique fiscal code identifying each electronic document. Stored, unique, immutable, and reproducible on request.
- **CAFE** — the auxiliary printed/visual representation delivered to the customer, including the QR/verification path. Check it's actually generated and delivered, not just the XML.
- **Authorization flow** — the document is only valid once DGI (or the PAC) authorizes it. Grep for code that marks an invoice `paid`/`issued` locally without awaiting authorization; that's a divergence between books and DGI.
- **Contingency mode** — what happens when DGI/PAC is unreachable. There is a defined contingency procedure with a window to transmit afterward (⚠ PIN the window). No contingency handling means sales halt during any DGI outage.
- **Cancellation / nota de crédito** — corrections go through the proper document type. Grep for `DELETE FROM invoices` or mutation of an authorized invoice — an authorized fiscal document cannot be edited or deleted.
- **ITBMS** — tax correctly computed, itemized, and displayed. ⚠ PIN current rates and exempt categories; a wrong rate is both a tax and a consumer-protection issue → `ley-45-consumidor.md`.
- **Schema version** — DGI updates the XML schema; pin the version in use and check it's current.
- **Retention** — electronic documents retained for the statutory fiscal period. ⚠ PIN the number of years. This retention duty **overrides** a Ley 81 deletion request for the invoice record; say so explicitly.

## What to grep for

- `factura`, `invoice`, `cufe`, `cafe`, `sfep`, `dgi`, `itbms`, `pac`, `nota_credito`
- PAC SDKs/HTTP clients and their base URLs — verify prod vs. sandbox endpoint per environment
- XML builders/templates for the fiscal document; hardcoded schema versions
- `.p12` / `.pfx` certificate files, and where their passwords live (a fiscal cert password in the repo is a Critical for `harden-web-security` too)
- retry/queue logic around the authorization call — its absence is the contingency gap
- any `UPDATE`/`DELETE` reaching an authorized invoice row

## Implementation spec

**Invoice state machine**, explicit: `draft → submitted → authorized → (cancelled via nota de crédito)`. Nothing is deliverable to the customer before `authorized`. No transition out of `authorized` except by issuing a corrective document.

**Durable queue for submissions** with retry and a contingency branch — DGI outages are routine, and a dropped submission is an unrecorded sale.

**Certificate expiry alarm** ahead of expiry, not on failure.

**Store the complete DGI response** (CUFE, authorization timestamp, raw payload) alongside the invoice. That response is the evidence.
