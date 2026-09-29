#1339 KS-1378: bump morgan, nodemailer, ip-address and undici off five advisories
head 8c1b25b24782d851817f8c7bb1c02d390fe750d7

## BLUF
The push preflight **FAILED legs 6 and 7** on develop's own dependencies, so **no push on this repo
succeeded**. Five newly published advisories were absent from `scripts/audit/audit-baseline.json` —
verified ABSENT at develop `8af6ab82` itself, so not caused by any open branch.

Kam ruled card `secuura-five-new-advisories-block-every-push-0929` = **(a)** at 2026-09-29 11:43:09
AEST, verbatim: *"Bump all four packages, with a quick reachability check in the same round."*
**No baseline row is added or removed by this PR.**

## THE PROOF — both legs now green, rc 0 each, verbatim
```
audit-gate: 23 distinct advisories reported, 25 baselined.
OK — no advisories outside the triaged baseline.

audit-locks: 43 standalone lockfiles (45 tracked, minus the workspace root which audit-gate covers,
minus 1 declared out of scope), 1612 distinct packages pinned — 18 advisories match, 18 already baselined.
OK — no standalone-lock advisories outside the triaged baseline.
```
**Before:** leg 6 `30 distinct advisories reported, 25 baselined` with 5 NEW; leg 7 `26 match, 21
already baselined` with the same 5. **After: ZERO vulnerable copies of any of the four remain**,
re-measured across the root lock and every standalone lock.

**First patched versions, read from the GitHub advisories API rather than inferred from "latest":**
nodemailer **10.0.2** · morgan **1.12.1** · ip-address **10.5.1** · undici **6.28.1 / 7.29.1 / 8.10.2**.

## The routes are NOT uniform — and two are not what the preflight implies
| package | route | why |
|---|---|---|
| **nodemailer** | **MAJOR 9 → 10** | the highest published 9.x **IS 9.1.1**, exactly what was pinned; the fix lands in 10.0.2. A lock refresh can never reach it. |
| **morgan** | declaration `^1.10.0` → `^1.12.1` | 1.12.1 was already inside the caret, but a refresh keeps an already-satisfying tree. Explicit beats resolution-dependent. |
| **ip-address** | **override `^10.5.1`** | `@cardano-sdk/core` asks `^9.0.5`, a range that can **never** reach 10.5.1. Root + `packages/shared` + `services/anchoring` (which inherit no root overrides). |
| **undici** | **override SCOPED to jsdom** | 🔴 the root `undici@5.29.0` is **NOT vulnerable at all** — every range starts at 6.25.0. Only jsdom's nested 7.29.0 is. A blanket override would have dragged a working 5.x runtime dep to 7.x for no security gain. |

## A measured bonus, not claimed when this was filed
Leg 6 now prints:
```
CLEANUP (advisory): 2 baseline entries are no longer reported — remove:
  - GHSA-v2v4-37r5-5v8g (ip-address, KS 470)
  - GHSA-mwp4-54f8-5fhr (ip-address, KS 729)
```
So the ip-address bump **also cleared KS 729's separate advisory**. The ticket said that "may also
satisfy it; a bonus, not this ticket's claim" — it is now measured. **Removing those two baseline
rows is a follow-up, not this PR.**

## How the locks were regenerated — it is not obvious and cost four attempts
Host **npm 11.5.1 dies with `Cannot read properties of null (reading 'edgesOut')`** — and it does so
**even on a bare `package.json` in an empty temp dir**, so it is the **host npm build**, not the
workspace layout, and `--no-workspaces` does not help. Regenerated in **node:24-alpine (npm 11.19.0)**,
each `package.json` resolved in an isolated directory inside the container: **13 of 13 ok, 0 failed**.
⚠ Mount the repo at `/src`, **never `/dev`** — mounting over `/dev` clobbers the container's
`/dev/null` and it dies `rc 127` before it starts.

## Reachability read — one line per advisory (FOUND / TESTED / HOW)
This informs the gate. It does NOT replace the bump: all four are bumped regardless, per the ruling.

**`GHSA-9f6g-j8ch-79g4` morgan — log injection via an unescaped quote in a quoted field.**
FOUND: **REACHABLE.** All three call sites use the `'combined'` preset
(`services/queue/src/index.ts:31`, `services/guardian/src/index.ts:31`,
`services/demo-service/src/app.ts:55`), and `combined` quotes the referrer and user-agent fields.
Those are attacker-controlled headers. TESTED: read only — no custom format string and no
`morgan.token`/`morgan.format` call exists anywhere in `services/` (measured, zero hits), so the
exposure is exactly the preset's two quoted fields and nothing wider. HOW: `grep` for `morgan(`
and for custom-format APIs across `services/**/*.ts`, excluding `node_modules`.

**`GHSA-6vj9-mwq6-2f5v` nodemailer — process-global DNS cache reuses TLS `servername` across transports.**
FOUND: **NOT REACHABLE as written.** The vulnerable path needs **two or more transports with
DIFFERENT servernames in one process**. Both services create exactly **one** transport, memoised:
`let transporter … | null = null;` then `if (transporter) return transporter;` before the single
`nodemailer.createTransport(...)` (`services/auth/src/services/email.ts:73,78,95`;
`services/originate/src/services/email.ts:75,78,97`). One `createTransport` call site per service,
measured. HOW: `grep -c createTransport` per file across both services' `src/`.
⚠ This is a property of TODAY'S code, not a guarantee: anyone adding a second transport (a second
SMTP provider, a per-tenant relay) re-opens it. That is the reason to take the bump anyway.

**`GHSA-rpw4-54j3-4h4q` + `GHSA-2vr4-cq9g-pvrc` ip-address — isLinkLocal `fe80::/64` vs `/10`, and no NAT64 classifier.**
FOUND: **NOT REACHABLE through our code.** We never call the library's classifiers: zero imports of
`ip-address` and zero calls to `isLinkLocal`/`Address6` anywhere in `services/` or `packages/`.
Our SSRF guard classifies NAT64 **itself**, in our own code — `packages/shared/src/security/ssrf-guard.ts:119`
("Embedded IPv4 tail, e.g. ::ffff:127.0.0.1 or 64:ff9b::192.0.2.1") and `:173` ("(64:ff9b::a.b.c.d)
all reach an IPv4 destination — classify the inner v4"), with its own cell at
`packages/shared/src/__tests__/ssrf-guard.test.ts:117` (`https://[64:ff9b::10.0.0.1]/x`,
'NAT64-wrapped RFC1918'). So the two advisories describe gaps we do not depend on the library to
close. The package is transitive, under `@cardano-sdk/*` and `@modelcontextprotocol/sdk`.
HOW: `grep` for `isLinkLocal|64:ff9b|Address6|ip-address` across `services packages --include='*.ts'`.

**`GHSA-3wwx-pv8p-q78v` undici — DoS via unhandled error in WebSocket permessage-deflate.**
FOUND: **NOT REACHABLE in runtime.** No `permessage-deflate` and no WebSocket client construction
anywhere in our source; every hit for "undici" is a COMMENT about its bad-port behaviour in tests
(e.g. `services/originate/src/__tests__/ks520-anchor-fail-closed.test.ts:26`). The vulnerable copy is
`jsdom`'s nested 7.29.0 — and **jsdom is a test-only dependency**, so it is not in any runtime image.
🔴 A measured correction to the preflight's framing: the ROOT `undici@5.29.0`
(via `@connectrpc/connect-node`) is **NOT vulnerable at all** — every vulnerable range starts at
6.25.0. Only the jsdom-nested 7.29.0 needs to move, which is why the override is SCOPED to jsdom
rather than applied package-wide. A blanket `undici` override would have dragged a working 5.x
runtime dependency to 7.x for no security gain.
HOW: `grep` for `permessage-deflate|new WebSocket|undici` across `services packages frontend`;
advisory ranges read from the GitHub advisories API, not inferred from "latest".

## Test evidence
**Touched:** 28 files — manifests and lockfiles only. **Zero non-manifest files in this diff.**
- **Legs 6 and 7: rc 0 each**, lines verbatim above. That is the proof the ruling asked for.
- **services/auth: 77 files / 836 tests, ALL PASSED** in this worktree — ⚠ see NOT COVERED (1).
- Zero vulnerable copies of any of the four, across the root lock and all standalone locks.
- `npm install --package-lock-only` at the root: **rc 0, "up to date"**.

**Migrations + config:** none. No migration, no env var, no service code.

## 🔴 NOT COVERED — the two things this PR cannot prove, stated plainly
1. **nodemailer 10 was NOT exercised at runtime.** The locks and declarations name 10.0.12, but
   `node_modules` in this worktree still holds **9.1.1** — the install errored `EOVERRIDE` because
   passing `morgan@1.12.1` explicitly duplicates the override this PR adds (a gotcha, not a defect:
   a plain `npm install` is rc 0). **So the 836 auth tests above passed against nodemailer 9.1.1.**
   The call surface is two calls per service (`createTransport`, `sendMail`) and node >= 20 is
   satisfied (we run v24.7.0) — **but that is a READ, not a RUN.** A clean install and a re-run of
   both services' suites is owed and should be a gate requirement.
2. **services/originate's suite does not load in this worktree** — 93 files, "no tests", on
   `Cannot find module '../routes/anchors'` and `'../services/provenance'`. **PRE-EXISTING and not
   caused here:** this diff touches **zero** non-manifest files, both modules exist in source, and
   `services/auth`'s 836 tests pass in the same worktree off the same install. Named because
   originate is the other nodemailer service, so its suite is owed too.
3. The root `morgan` override is now redundant (all ten declarers say `^1.12.1`). Kept as a guard
   against a future service declaring an older range; it is why `npm install morgan@<ver>` reports
   `EOVERRIDE`.
4. No baseline row added or removed. No `--no-verify`. Nothing deployed, no `az`.

Refs KS-1378
Refs KS-729

🤖 Generated with [Claude Code](https://claude.com/claude-code)

