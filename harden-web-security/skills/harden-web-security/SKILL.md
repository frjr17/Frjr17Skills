---
name: harden-web-security
description: Harden web applications against attacks (OWASP Top 10 and beyond). Threat-models the app, audits code AND deployed surface for vulnerabilities, dynamically verifies the top findings, and reports each with severity, the attacker technique, and a concrete fix. Use when the user asks to harden security, run a security review/audit or pentest-prep, find vulnerabilities, "make this secure", or asks about XSS / SQLi / CSRF / SSRF / IDOR / auth / session / multi-tenancy / security-headers hardening.
---

# Harden Web Security

Defensive-security workflow: model how the app gets attacked, find it in code AND at runtime, report it, apply the hardening. Attacker's-eye view, defender's fixes.

## Reality check

No checklist "stops anyone." A skilled attacker with time defeats static defenses. The goal is to **raise cost, shrink attack surface, and detect what prevention misses** — prevention without detection is one missed bug away from a silent, total compromise. Grep-only review catches injection and config; it does NOT catch business-logic flaws, chained low-severity bugs, or authorization gaps — those need a threat model and actually sending requests.

## Scope guard

Only for **authorized** work: the user's own app, a pentest engagement, a CTF, or a security review. This skill hardens and audits — it does not write working exploits, mass-scan third-party targets, or build evasion for real attacks. If the target isn't clearly the user's or authorized, ask before proceeding.

## Workflow (default: audit + report, review-first)

1. **Threat-model first.** Before grepping: what are the assets (money, PII, admin)? Where are the trust boundaries? What's reachable **unauthenticated** vs. authenticated vs. cross-tenant? What does an attacker want? Sinks matter only relative to a boundary.
2. **Recon the deployed surface** (see below) — the metadata leaks and forgotten endpoints that precede every real intrusion.
3. **Map the app.** Stack, framework, routes/handlers, auth & tenancy model, data stores, uploads, outbound requests, and every place user input flows. Grep the sinks, don't guess.
4. **Audit against the checklist.** Trace untrusted input to each sink; check authz at every object access.
5. **Dynamically verify the top findings.** You cannot confirm IDOR, broken authz, or a rate-limit bypass by reading code — send the request as user A for user B's object, replay without the token, tamper the ID. Reading finds candidates; sending confirms them.
6. **Report each finding as:** `SEVERITY | attack | file:line (or endpoint) | why it's exploitable | the fix`. Rank Critical → Low. Note chains explicitly (two Lows that combine into a Critical).
7. **Fix after reporting.** Apply low-risk hardenings (headers, cookie flags, dep bumps, output encoding) directly when okayed. Behavior-changing fixes (authz, session, crypto) — propose the diff, let the user approve. Leave a **regression test that reproduces the attack** and asserts it now fails (e.g. request test expecting 403, or that a payload is escaped).

Do **not** auto-fix before showing findings. A wrong "hardening" that breaks auth is worse than the report.

## Recon: exposed surface (check first, attackers do)

- Source/secret leaks: reachable `.git/`, `.env`, `.svn`, backup/`~`/`.bak` files, JS **source maps**, config dumps.
- Framework leftovers: `/actuator`, `/debug`, Swagger/GraphQL playground in prod, default admin panels, sample/test routes, directory listing.
- Info leaks: verbose 500s / stack traces, version banners, descriptive error messages, `Server`/`X-Powered-By` headers.
- Old/parallel surface: unversioned or deprecated API endpoints, staging creds in prod, dangling subdomains (takeover).

## What to grep for (fast triage)

- Injection sinks: string-built SQL, `exec`/`system`/`spawn`, `eval`, `Runtime.exec`, template render on user input.
- XSS sinks: `innerHTML`, `dangerouslySetInnerHTML`, `v-html`, `| safe`, `render_template_string`, unescaped interpolation.
- Access control: object lookups by ID with no owner/tenant check; nested resources (`/org/1/users/2`); admin routes; `is_admin`/`role`/`price` set from request body (mass assignment).
- Auth/session: password hashing algo, cookie flags, JWT `alg`/`kid`, session ID source, MFA, lockout, logout invalidation.
- SSRF: `fetch`/`requests`/`curl`/`http.get`/webhook/PDF/image-fetch with a URL from user input.
- Deserialization: `pickle`, `unserialize`, `readObject`, `yaml.load`, `Marshal.load`.
- Secrets: hardcoded keys/tokens, secrets in client JS, keys in git history.
- Config: debug on, verbose errors, missing security headers, permissive CORS, wildcard IAM.

## Attack → Hardening reference

### Injection
- **SQL / NoSQL** → parameterized queries / prepared statements; never concatenate input. ORM query APIs over raw. Validate types. Watch **second-order** (stored input executed in a later query).
- **OS command** → avoid shelling out; if unavoidable, arg arrays (no shell string), allowlist values.
- **LDAP / XPath** → escape/parameterize per the query language; allowlist input.
- **SSTI / EL / OGNL** → never render user input as a template; pass it as data to a static template.
- **CRLF / Host header** → strip `\r\n` from anything reaching headers; validate `Host` against an allowlist (also protects password-reset links).

### XSS
- **Reflected / Stored / DOM** → context-aware output encoding (HTML/attr/JS/URL). Framework auto-escaping on; avoid `innerHTML`/`dangerouslySetInnerHTML`/`| safe`.
- **Defense in depth** → strict CSP with **nonces + `strict-dynamic`** (not just `'self'`, which JSONP/gadgets bypass), `require-trusted-types-for 'script'` for DOM sinks, and `HttpOnly` cookies so XSS can't read the session.

### Broken access control, multi-tenancy & business logic (highest-value — read closely)
- **IDOR / BOLA** → every object fetch verifies the caller owns/may access it, **server-side**, including nested resources (`/org/{o}/users/{u}` must check `u` belongs to `o` AND caller may act on `o`). Never trust client-supplied IDs. Use unguessable IDs as defense-in-depth, never as the control.
- **Multi-tenancy** → scope every query by tenant at the data layer (row-level security / mandatory `WHERE tenant_id`); one missing filter = full cross-tenant breach. Test as tenant A requesting tenant B's IDs.
- **Function-level authz** → enforce role checks server-side on every privileged route; **deny by default**; don't rely on a hidden UI.
- **Business logic** (no grep signature — reason about the flow): negative/huge quantities, price/coupon/refund tampering, skipping a step in a checkout/KYC/approval flow, replaying a one-time action, quantity vs. inventory races. Enforce invariants server-side; re-validate the whole state on the final action, not per step.
- **Path traversal / LFI / RFI** → canonicalize the resolved path and confirm it's under the allowed root; never build include/file paths from raw input.
- **Mass assignment** → allowlist bindable fields; never bind `role`/`isAdmin`/`price`/`tenant_id` from the request body.

### Authentication
- **Credential stuffing / brute force / password spraying** → rate limit + lockout/backoff, MFA, breached-password check, CAPTCHA on abuse. Also rate-limit **registration and password-reset** (enumeration + abuse vectors).
- **Password storage** → argon2id (or bcrypt/scrypt) + per-user salt; optional pepper in a KMS. **Bcrypt truncates at 72 bytes** — pre-hash long inputs or cap length; never MD5/SHA1/plaintext.
- **Password reset** → high-entropy single-use tokens, short expiry, invalidated on use; build the reset link from a server-configured base URL, **not the `Host` header**; identical response whether or not the email exists.
- **MFA** → reject reused/expired TOTP codes; rate-limit and cap **backup-code** attempts; re-verify on "remember this device"; require step-up for sensitive actions.
- **Username enumeration** → identical responses **and timing** for valid/invalid users across login, reset, and registration.
- **JWT** → reject `alg=none`; pin the algorithm server-side; strong secret or proper RS256 key; validate `exp`/`aud`/`iss`; validate/allowlist `kid` (no path traversal, no attacker-controlled JWKS). Remember: **stateless JWTs can't be revoked** — for logout/ban you need short expiry + a server-side denylist or rotating session store.

### SSO / SAML / OIDC
- **SAML** → validate the XML signature over the **asserted** element; block **signature-wrapping** (XSW); pin issuer/audience/recipient; reject unsigned assertions and `NameID` swaps.
- **OAuth / OIDC** → exact `redirect_uri` match, `state` for CSRF, PKCE for public clients, validate `iss`/`aud`/`nonce`, don't accept tokens from unexpected issuers.

### Session management
- **Hijacking / fixation** → regenerate session ID on login and privilege change; cryptographically random IDs; server-side invalidation on logout; **absolute + idle** timeouts; limit/track concurrent sessions.
- **Cookies** → `Secure`, `HttpOnly`, `SameSite=Lax/Strict`, `__Host-` prefix, scoped path/domain.
- **CSRF** → anti-CSRF tokens **and** `SameSite` cookies on all state-changing requests (SameSite alone leaks via top-level GET and subdomains); check `Origin`/`Referer`.
- **Clickjacking** → `frame-ancestors 'none'` / `X-Frame-Options: DENY`.

### Request forgery & smuggling
- **SSRF** → allowlist outbound hosts/schemes; block private/link-local/loopback ranges **and** their encodings (IPv6, decimal/octal/hex IPs, `0.0.0.0`); resolve DNS then re-check the resolved IP (defeats rebinding); disable redirects to internal; on cloud, **enforce IMDSv2** (block v1). Applies to webhooks, URL previews, PDF/image fetchers.
- **Request smuggling** → consistent HTTP parsing front-to-back; reject ambiguous `Content-Length`/`Transfer-Encoding`; prefer HTTP/2 to backend.
- **Cache poisoning/deception** → key the cache on every input that affects the response; never cache authenticated pages.

### Files, XML & deserialization
- **File upload** → validate type by content (magic bytes) not extension; **store outside webroot and serve from an isolated sandbox domain**; randomize names; set `Content-Disposition`/`nosniff`; **never execute uploads**. Note **SVG = XSS**, polyglots, and decompression/zip bombs — scanning is weak, isolation is the control.
- **XXE** → disable external entities & DTDs (also blocks XXE-driven SSRF and OOB exfiltration).
- **Insecure deserialization** → don't deserialize untrusted data; JSON with a schema; if unavoidable, sign & verify. Server-side **prototype pollution** can chain to RCE — reject `__proto__`/`constructor`/`prototype` keys.
- **Zip slip** → validate each extracted path stays under the target dir.

### APIs
- **Excessive data exposure** → serialize with explicit field allowlists; don't return more than the UI needs.
- **Rate limiting** → per-user/IP/endpoint; consistent across header casing, versions, and IP rotation.
- **GraphQL** → disable introspection in prod; depth/complexity limits; authz per resolver; disable field-suggestion hints; watch **aliased-batch** login brute force.
- **HTTP parameter pollution** → define duplicate-param behavior; validate.

### Client-side & browser
- **CORS** → never reflect arbitrary `Origin` with credentials; explicit allowlist; no `*` with credentials; reject `null`; anchor regexes (`^https://app\.example\.com$`, not `example\.com`).
- **postMessage** → verify `event.origin` on receive.
- **Prototype pollution / DOM clobbering** → reject dangerous keys; `Object.create(null)` for maps.
- **Open redirect** → allowlist redirect targets; no raw user URL in `Location`.
- **Reverse tabnabbing** → `rel="noopener noreferrer"` on `target=_blank`.
- **Supply chain** → lockfile with **hash pinning**, SRI on external scripts, SCA in CI, audit third-party JS; lock CI: no secrets to `pull_request_target`, pin action versions by SHA.

### Crypto & data exposure
- **Weak crypto** → AES-GCM (authenticated) not ECB; modern hashes; per-message IV/nonce.
- **Padding/timing oracles** → authenticated encryption; **constant-time comparison** for secrets/tokens.
- **Secrets** → out of code and client bundles; secrets manager/env; rotate leaked keys; scrub git history.
- **Randomness** → CSPRNG for tokens/IDs, never `Math.random`/`rand()`.
- **Data in errors/logs** → generic errors in prod; scrub PII/secrets from logs; no stack traces to users.
- **TLS** → HSTS (preload), TLS 1.2+, strong ciphers, redirect HTTP→HTTPS.

### Availability
- **App-layer DoS / ReDoS / Slowloris** → timeouts, request size/rate limits, bounded regex (no catastrophic backtracking), body/header limits at the edge.
- **Subdomain takeover** → remove dangling DNS for deprovisioned services.
- **Dependency confusion** → scope internal packages; pin registry sources.
- **Race / TOCTOU** → atomic DB ops, locks, or idempotency keys for money/limit paths.

## Detection & response (OWASP A09 — prevention isn't enough)

You can't stop what you can't see. The one bug you missed is only survivable if you detect it.
- **Log security events** (authn success/fail, authz denials, input-validation failures, admin actions, token/key use) with enough context to trace, and **without** logging secrets/PII.
- **Alert** on anomalies: brute-force/lockout spikes, authz-denial bursts (IDOR probing), new-geo/impossible-travel logins, mass data export.
- **Make logs tamper-evident and monitored** — ship off-host; unmonitored logs are theater.
- **Have a response path**: rate-limit/block on trigger, session/token revocation, and a rollback/patch plan. Consider a WAF as a speed bump, not a fix.

## Baseline security headers (apply to every response)

```
Strict-Transport-Security: max-age=63072000; includeSubDomains; preload
Content-Security-Policy: default-src 'self'; script-src 'self' 'nonce-{random}' 'strict-dynamic'; object-src 'none'; base-uri 'self'; form-action 'self'; frame-ancestors 'none'; require-trusted-types-for 'script'
X-Content-Type-Options: nosniff
Referrer-Policy: strict-origin-when-cross-origin
Permissions-Policy: geolocation=(), camera=(), microphone=()
```
Use the framework's helper (helmet / Flask-Talisman / Django SecurityMiddleware) rather than hand-rolling. Generate a fresh CSP nonce per response.

## Report template

```
[CRITICAL] IDOR — GET /api/orders/{id}  (src/orders/controller.js:88)
  Attack: order fetched by id with no owner check; user A reads user B's order.
  Verified: logged in as A, requested B's order id → 200 with B's data.
  Impact: cross-account data disclosure of all orders/PII.
  Fix: scope query by caller — WHERE id = ? AND user_id = :caller; return 404 on mismatch.
  Regression: test asserts A→B order id returns 404.
```

Finish with a prioritized summary: Critical/High first, quick wins (headers, cookie flags, dep bumps) called out separately, and any **chains** where combined low-severity issues reach Critical.
