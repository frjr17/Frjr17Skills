# Ley 51 de 2008 — Documentos y Firmas Electrónicas

> Last verified against source: never — written 2026-07-28 from model knowledge. Every ⚠ PIN value is unconfirmed.

Defines and regulates electronic documents, electronic signatures, technological document-storage providers, and certification service providers; adopts provisions for e-commerce. Amended by **Ley 82 de 2012** (⚠ PIN the amendment scope). Oversight sits with the **Dirección Nacional de Firma Electrónica** of the **Registro Público de Panamá**.

Load this when the system e-signs anything, accepts signed documents, or keeps documents as legal records.

## The distinction that decides everything

Not all electronic signatures are equal under Panamanian law. A **firma electrónica calificada** — backed by a certificate from a certification service provider (PSC) **registered with the Dirección Nacional de Firma Electrónica** — carries the legal equivalence to a handwritten signature. A plain electronic signature (a typed name, a drawn squiggle on a canvas, a checkbox, an `signed_at` timestamp) does not automatically get that equivalence.

Consequence: an app that "signs" contracts with a base64 canvas image and a boolean has, in a dispute, an evidentiary artifact — not a signature with statutory equivalence. Whether that matters depends on what's being signed and what the counterparty will contest. Flag it as a finding with that framing; do not overclaim that it's void.

⚠ PIN before asserting: the exact terminology and tiers in the current text, which acts require a qualified signature, and any excluded document types (some instruments are typically carved out — verify rather than assume).

## What to audit

- **Signature mechanism.** What actually produces the signature? A registered PSC's certificate, a foreign e-sign SaaS (DocuSign/Dropbox Sign/etc.), or homemade? A foreign provider is not automatically a registered PSC in Panama — check the register at `firmaelectronica.gob.pa`.
- **Certificate validity at signing time.** Was the certificate valid, unrevoked, and unexpired *when signed*? Verify at signing and store the verification result — not just the signature blob.
- **Integrity binding.** The signature must bind to the exact document content. Grep for signatures stored separately from an immutable document hash — if the document can be edited after signing and the signature still "validates," it binds nothing.
- **Evidence retention.** Signed document, signature, certificate chain, timestamp, and validation evidence kept together, immutably, for the document's legal life.
- **Technological storage (almacenamiento tecnológico).** If the system holds documents as the authoritative record, storage-provider rules may apply. ⚠ PIN whether the operation needs registration.
- **Consent to transact electronically.** Recorded, not assumed.

## What to grep for

- `signature`, `firma`, `signed_at`, `canvas`, `toDataURL`, `sign(` — trace to what actually validates
- e-sign SDKs: `docusign`, `dropbox-sign`/`hellosign`, `adobe sign`, `zapsign`, `autentic`, local PSC SDKs
- crypto signing paths: `crypto.sign`, `pkcs7`, `pkcs12`, `.p12`, `.pfx`, `x509`, `pades`, `cades`, `xades`
- absence of hash-binding: a signed record with no `document_hash`
- documents in mutable storage (an S3 object with versioning off, an editable row) presented as signed originals
- certificate expiry handling — a job that renews, or silent failure at expiry

## Implementation spec

**Signature record**: document id, `document_hash` (content-addressed), signer identity, certificate serial + issuer, signing timestamp, validation result captured at signing time, signature blob. Immutable.

**Validation at signing, not at read.** Verify chain, revocation status, and validity window when the signature is created, and persist the outcome. Re-validating years later against a since-expired certificate produces false negatives; the captured evidence is what stands up.

**Storage**: append-only or versioned with deletion protection. If a signed document can be silently overwritten, the signature is decorative.

Cross-reference: signed documents almost always contain personal data → `ley-81-datos-personales.md` (retention rules interact — a legal-retention duty can override a deletion request; state that interaction explicitly rather than letting one job delete evidence the other requires).
