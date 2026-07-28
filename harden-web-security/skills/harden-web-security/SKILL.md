---
name: harden-web-security
description: Harden web applications against attacks (OWASP Top 10 and beyond). Audits code for vulnerabilities and reports each finding with severity, the attacker technique, and a concrete fix. Use when the user asks to harden security, run a security review/audit, find vulnerabilities, "make this secure", prep for a pentest, or asks about XSS / SQLi / CSRF / SSRF / auth / session / security-headers hardening.
---

# Harden Web Security

Defensive-security workflow: find how an app can be attacked, report it, and apply the hardening. Attacker's-eye view, defender's fixes.

## Scope guard

Only for **authorized** work: the user's own app, a pentest engagement, a CTF, or a security review. This skill hardens and audits — it does not write working exploits, mass-scan third-party targets, or build evasion for real attacks. If the target isn't clearly the user's or authorized, ask before proceeding.

## Workflow (default: audit + report, review-first)

1. **Map the app.** Identify stack, framework, entry points (routes/controllers/handlers), auth model, data stores, file uploads, outbound requests, and where user input flows. Grep for the sinks, don't guess.
2. **Audit against the checklist below.** For each surface, trace untrusted input to the sink.
3. **Report each finding as:** `SEVERITY | attack | file:line | why it's exploitable | the fix`. Rank Critical → Low.
4. **Fix only after reporting.** Apply low-risk hardenings (security headers, cookie flags, dependency bumps, output encoding) directly when the user okays it. Anything that changes behavior (authz rewrites, session model, crypto) — propose the diff, let the user approve.
5. **Leave a check behind.** For non-trivial fixes, add one runnable test that fails if the vuln returns (e.g. a request test asserting a 403, or that a payload is escaped).

Do **not** auto-fix without showing findings first. A wrong "hardening" that breaks auth is worse than the report.

## What to grep for (fast triage)

- Injection sinks: string-built SQL, `exec`/`system`/`spawn`, `eval`, `Runtime.exec`, template render on user input.
- XSS sinks: `innerHTML`, `dangerouslySetInnerHTML`, `v-html`, `| safe`, `render_template_string`, unescaped interpolation.
- Access control: object lookups by ID with no owner check; admin routes; `is_admin`/`role` set from request body (mass assignment).
- Auth/session: password hashing algo, cookie flags, JWT `alg`, session ID source, MFA, lockout.
- SSRF: `fetch`/`requests`/`curl`/`http.get` with a URL from user input.
- Deserialization: `pickle`, `unserialize`, `readObject`, `yaml.load`, `Marshal.load`.
- Secrets: hardcoded keys/tokens, `.env` in repo, secrets in client JS.
- Config: debug mode on, verbose errors, missing security headers, permissive CORS.

## Attack → Hardening reference

### Injection
- **SQL / NoSQL** → parameterized queries / prepared statements; never string-concatenate input. ORM query APIs over raw. Validate types.
- **OS command** → avoid shelling out; if unavoidable, use arg arrays (no shell string), allowlist values.
- **LDAP / XPath** → escape/parameterize per the query language; allowlist input.
- **SSTI / EL / OGNL** → never render user input as a template; pass it as data to a static template.
- **CRLF / Host header** → strip `\r\n` from anything reaching headers; validate `Host` against an allowlist.

### XSS
- **Reflected / Stored / DOM** → context-aware output encoding (HTML/attr/JS/URL). Framework auto-escaping on; avoid `innerHTML`/`dangerouslySetInnerHTML`/`| safe`.
- **Defense in depth** → strict `Content-Security-Policy` (no `unsafe-inline`, nonces/hashes for scripts), `HttpOnly` cookies so XSS can't read the session.

### Broken access control
- **IDOR / BOLA** → every object fetch checks the caller owns/may access it, server-side. Don't trust client-supplied IDs.
- **Function-level authz** → enforce role checks on the server for every privileged route; deny by default.
- **Path traversal / LFI / RFI** → resolve to a canonical path and confirm it's under the allowed root; never build include/file paths from raw input.
- **Mass assignment** → allowlist bindable fields; never bind `role`/`isAdmin`/`price` from the request body.

### Authentication
- **Credential stuffing / brute force** → rate limit + account lockout/backoff, MFA, breached-password checks, CAPTCHA on abuse.
- **Password storage** → argon2id (or bcrypt/scrypt) with per-user salt; never MD5/SHA1/plaintext.
- **Username enumeration** → identical responses & timing for valid/invalid users.
- **JWT** → reject `alg=none`; pin the algorithm server-side; strong secret or proper RS256 key; validate `exp`/`aud`/`iss`.
- **OAuth/OIDC** → exact `redirect_uri` match, `state` for CSRF, validate issuer/audience.

### Session management
- **Hijacking / fixation** → regenerate session ID on login; cryptographically random IDs; short expiry + idle timeout.
- **Cookies** → `Secure`, `HttpOnly`, `SameSite=Lax/Strict`, scoped path/domain.
- **CSRF** → anti-CSRF tokens (or `SameSite` cookies) on all state-changing requests; check `Origin`/`Referer`.
- **Clickjacking** → `frame-ancestors 'none'` (CSP) / `X-Frame-Options: DENY`.

### Request forgery & smuggling
- **SSRF** → allowlist outbound hosts/schemes; block private/link-local ranges (incl. `169.254.169.254`); resolve DNS and re-check; disable redirects to internal.
- **Request smuggling** → consistent HTTP parsing front-to-back; prefer HTTP/2 to backend; reject ambiguous `Content-Length`/`Transfer-Encoding`.
- **Cache poisoning/deception** → key cache on all inputs that affect the response; don't cache authenticated pages.

### Files, XML & deserialization
- **File upload** → validate type by content not extension; store outside webroot; randomize names; never execute uploads; scan.
- **XXE** → disable external entities & DTDs in the XML parser.
- **Insecure deserialization** → don't deserialize untrusted data; use JSON with a schema; if you must, sign/verify payloads.
- **Zip slip** → validate each extracted path stays under the target dir.

### APIs
- **Excessive data exposure** → return only needed fields; serialize with explicit allowlists.
- **Rate limiting** → per-user/IP/endpoint limits; consistent across casing/versions.
- **GraphQL** → disable introspection in prod; query depth/complexity limits; authz per resolver.
- **HTTP parameter pollution** → define behavior for duplicate params; validate.

### Client-side & browser
- **CORS** → never reflect arbitrary `Origin` with credentials; explicit allowlist; no `*` with credentials.
- **postMessage** → verify `event.origin` on receive.
- **Prototype pollution** → reject `__proto__`/`constructor`/`prototype` keys; `Object.create(null)` for maps.
- **Open redirect** → allowlist redirect targets; no raw user URL in `Location`.
- **Reverse tabnabbing** → `rel="noopener noreferrer"` on `target=_blank`.
- **Supply chain** → pin/lock deps, Subresource Integrity (SRI) on external scripts, audit third-party JS.

### Crypto & data exposure
- **Weak crypto** → AES-GCM (authenticated) not ECB; modern hashes; per-message IV/nonce.
- **Padding/timing oracles** → authenticated encryption; constant-time comparisons for secrets/tokens.
- **Secrets** → out of code and client bundles; use a secrets manager/env; rotate leaked keys.
- **Randomness** → CSPRNG for tokens/IDs, never `Math.random`/`rand()`.
- **Data in errors/logs** → generic error pages in prod; scrub PII/secrets from logs; disable stack traces.
- **TLS** → HSTS, TLS 1.2+, strong ciphers, redirect HTTP→HTTPS.

### Availability
- **App-layer DoS / ReDoS / Slowloris** → timeouts, request size/rate limits, bounded regex (no catastrophic backtracking), body/header limits at the edge.
- **Subdomain takeover** → remove dangling DNS records for deprovisioned services.
- **Dependency confusion** → scope internal packages; pin registry sources.
- **Race/TOCTOU** → atomic DB operations, locks, or idempotency keys for money/limit paths.

## Baseline security headers (apply to every response)

```
Strict-Transport-Security: max-age=63072000; includeSubDomains; preload
Content-Security-Policy: default-src 'self'; object-src 'none'; frame-ancestors 'none'; base-uri 'self'
X-Content-Type-Options: nosniff
Referrer-Policy: strict-origin-when-cross-origin
Permissions-Policy: geolocation=(), camera=(), microphone=()
```
Use the framework's helper (helmet / Flask-Talisman / Django SecurityMiddleware) rather than hand-rolling.

## Report template

```
[CRITICAL] SQL Injection — src/users/repo.js:42
  Attack: `SELECT ... WHERE id = ${req.query.id}` — id is user-controlled.
  Impact: full DB read/write, auth bypass.
  Fix: parameterized query — db.query('SELECT ... WHERE id = ?', [id]).
```

Finish with a short prioritized summary: Critical/High first, quick wins (headers, cookie flags, dep bumps) called out separately.
