# Ley 45 de 2007 — Protección al Consumidor y Defensa de la Competencia

> Last verified against source: never — written 2026-07-28 from model knowledge. Every ⚠ PIN value is unconfirmed.

Consumer protection and competition. Enforced by **ACODECO** (Autoridad de Protección al Consumidor y Defensa de la Competencia). Applies to B2C sales — including a foreign-hosted site selling into Panama.

Load this whenever there's a checkout, a subscription, pricing, advertising claims, or terms of service shown to consumers.

Most of this is UI and copy, which makes it easy to audit and easy to have gotten wrong without noticing.

## What to audit

**Price display.** The price the consumer sees must be the price they pay. Audit for: taxes and mandatory fees revealed only at the final step, currency ambiguity (B/. vs USD — they're at parity but label it), per-unit vs. total confusion, and struck-through "was" prices that were never charged. ⚠ PIN whether ITBMS must be shown inclusive or may be added at checkout, and the current rate — this drives the finding either way.

**Pre-contract disclosure.** Before the consumer commits: total price, product identity and characteristics, seller identity and physical contact details, delivery terms and timeframe, and cancellation/return terms. Grep the checkout flow for what's actually rendered before the confirm button, not what's in a footer link.

**Cláusulas abusivas.** Unfair terms in adhesion contracts are attackable regardless of acceptance. Read the T&C for: unilateral modification without notice, blanket liability waivers, forcing foreign jurisdiction on a Panamanian consumer, waiving statutory warranty, automatic renewal buried in a clause. A clicked "I agree" does not save an abusive clause.

**Warranty and returns.** Statutory warranty exists independent of what the T&C says. Grep for a returns flow that's shorter or narrower than the statutory minimum. ⚠ PIN the minimum warranty period and return rights.

**Advertising.** Claims must be truthful and substantiable. Check marketing copy for absolute claims ("the fastest", "100% secure", "guaranteed"), fake urgency (a countdown that resets on reload, "only 2 left" that's hardcoded), and fabricated social proof.

**Dark patterns and subscription traps.** The highest-risk area for a modern app: cancellation that's harder than signup, free trials that auto-convert without a clear pre-charge disclosure, pre-ticked add-ons, confirmshaming, hidden unsubscribe. **Cancellation must be at least as easy as subscription** — audit both paths side by side and compare step counts.

**Receipt.** The consumer gets a valid fiscal document → `factura-electronica-sfep.md`.

**Complaint channel.** A reachable one, and awareness that ACODECO adjudicates consumer complaints.

## What to grep for

- price rendering and tax computation — where is ITBMS added, and at which step does it first appear on screen?
- checkout step components: what's disclosed before the final confirm
- `terms`, `tos`, `terminos`, `condiciones` — read them, don't just confirm the file exists
- subscription code: `trial`, `auto_renew`, `cancel_at_period_end` — then find the user-facing cancel path and count the clicks
- countdown timers, stock counters, "X people viewing" widgets — trace to a real data source or flag as fabricated
- hardcoded jurisdiction/governing-law clauses naming a non-Panamanian forum for consumer contracts
- marketing superlatives and guarantees in landing copy

## Implementation spec

**Show the all-in price early**, with tax and fees itemized at the first price display, not the last.

**Disclosure block** rendered before the confirm action: total, seller identity, delivery window, cancellation terms. One component, reused on every checkout surface.

**Symmetric cancellation**: if signup is N clicks in-app, cancellation is ≤ N clicks in-app. No email-only, no phone-only.

**Trial-to-paid**: explicit pre-charge notice and a clear conversion date shown at signup and before the first charge.

**T&C draft** ⚠ marked for counsel review — never presented as filing-ready.

## Cobranza — collecting debts and sending payment reminders

**Applies when** the system tracks what consumers owe (installments, contracts, loans, subscriptions in arrears) and contacts them about it — reminders, overdue notices, collection messages by WhatsApp, SMS, email or calls. Collection practices toward consumers are regulated; ⚠ PIN the governing articles of Ley 45 and any ACODECO resolution on gestión de cobro before citing any rule below as law. Treat the list as *what to check*, not as settled requirements.

Audit:
- **Who is contacted** → only the debtor (and a guarantor where the contract names one). Messages to relatives, employers, references or group chats disclose the debt to third parties — a consumer issue **and** a Ley 81 disclosure.
- **When and how often** → sending windows (no late-night or very early sends), a cap on reminders per period, and no repeat sends after the debtor has paid or disputed. ⚠ PIN any statutory hours or frequency limit; absent one, the app should still enforce a configurable window and cap.
- **What the message says** → identifies the creditor, the amount and due date accurately, and how to pay or dispute; no threats, no false legal consequences ("legal action today", "you'll be reported" when nobody will), no shaming, no tone implying an authority that isn't there.
- **Accuracy** → the amount shown matches the ledger at send time (payments applied, partial payments reflected); a reminder for an already-paid installment is a finding.
- **Dispute and stop path** → the debtor can say "already paid" or dispute, the reply reaches a human, and reminders pause while it's open.
- **Evidence** → every message logged (to whom, when, content/template version, channel), so the creditor can show what was and wasn't sent.

Grep: reminder schedulers/cron/queues, message templates and their variables, send-window or rate-limit logic (often missing), contact fields beyond the debtor's own (`referencia`, `familiar`, `contacto_alterno`), and what happens to scheduled reminders when a payment is registered.

Implementation spec: send window + per-debtor cap enforced in the scheduler (not the UI); reminders cancelled or recomputed on payment; a `paused` state on dispute; a send log keyed to template version. Template copy ⚠ drafted for counsel review.

Cross-reference: debtor data, phone numbers and messaging providers → `ley-81-datos-personales.md`.

Cross-reference: consumer data collected at checkout → `ley-81-datos-personales.md`.
