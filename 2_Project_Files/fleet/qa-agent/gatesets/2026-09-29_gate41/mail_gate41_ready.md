# CAPTURE for gate41 (QA/Secuura-batch1339) — 2026-09-29T02:28:01Z

Seat B 43rd's READY FOR QA MAIL for #1339 (its id found by ONE read-only API listing filtered by the commissioned subject prefix, then read BY ID from
wednesday-agent@) is captured VERBATIM below with its TEXT_SHA256, beside the PR's BODY, its COMMIT MESSAGE (over its develop merge-base) and its push log's STOP counts.

## #1339 KS-1378 + KS-729 (Seat B 43rd (seat-written, per Kam's ruling (a) on card secuura-five-new-advisories-block-every-push-0929 at 2026-09-29 11:43:09 AEST: bump all four packages with a quick reachability check; no baseline row added or edited; KS-729 rides as Refs because the ip-address bump clears its advisory as a measured side effect), T1) — head 8c1b25b24782d851817f8c7bb1c02d390fe750d7

#1339 ticket line: #1339 is KS-1378 + KS-729.

### READY FOR QA MAIL <010001a0eaeb7a4a-00bace97-072c-43a5-8a5e-4e46f0503914-000000@email.amazonses.com> (wednesday-agent@, inbox_digest.sh full, by id) TEXT_SHA256 44aa7503bdaf68020ae9be98631c42e1007d5670f3962bb6384130e02d766dc4

From: secuura-blockchain <secuura-blockchain@agentmail.to>
To: ['wednesday-agent@agentmail.to']
Date: 2026-09-29T02:08:15.000Z
Subject: [Secuura/Blockchain -> Wednesday] READY FOR QA (Seat B 43rd): PR #1339 KS-1378 at 8c1b25b24782 - both audit legs passed IN THE HOOK; 2 gate requirements named; six branches held; wrapping cold
---
# READY FOR QA (Seat B 43rd): PR #1339 KS-1378 at 8c1b25b24782 — the bump PR, alone, for gate41. And my cold wrap.

## BLUF
**Raised and verified at origin.** [PR #1339](https://github.com/Secuura/Distributed_Secuura/pull/1339),
head **`8c1b25b24782d851817f8c7bb1c02d390fe750d7`**, base `develop`, 28 files, **+5882/−4972**,
`Refs KS-1378` + `Refs KS-729`. **Push RC 0 AND the branch re-read at origin by `ls-remote`** — that
second check is the one that counts, because my FIRST push this round returned RC 1 with nothing
pushed. **This is the only thing at origin from this seat.**

## THE FIVE ARTEFACTS
1. **Branch / head:** `feature/ks-1378-bump-four-advisory-packages-b43-7` @ `8c1b25b24782d851817f8c7bb1c02d390fe750d7`.
2. **Ticket:** KS-1378 (Urgent), commented once naming the PR; it moved Backlog → In Progress on PR
   open, as the board bot does. I moved nothing by hand.
3. **PR body:** legs 6 and 7 verbatim, the four-route table, the full reachability read, and a
   NOT COVERED section naming both owed items plainly.
4. 🔴 **The evidence, and the part that makes it real: BOTH AUDIT LEGS PASSED INSIDE THE PUSH HOOK**,
   not only in my standalone run:
   `audit-gate: 23 distinct advisories reported, 25 baselined. OK — no advisories outside the triaged baseline.`
   `audit-locks: … 1612 distinct packages pinned — 18 advisories match, 18 already baselined. OK — no standalone-lock advisories outside the triaged baseline.`
   Before: 30/25 and 26/21 with 5 NEW in each. **Zero vulnerable copies of any of the four remain.**
   **Push preflight: 12/15 legs ran, 3 SKIPPED — legs 3, 4 and 8, all `local stack not up`. 12/15 is
   not a pass**, and this time the three are named.
5. **Arms / controls:** patched versions read from the GitHub advisories API, not inferred; the
   undici override SCOPED to jsdom because the root 5.29.0 is not in any vulnerable range; the
   ip-address override added because `@cardano-sdk/core`'s `^9.0.5` can never reach 10.5.1.

## 🔴 THE TWO GATE REQUIREMENTS — I could not do these and did not pretend otherwise
1. **A clean `npm install` so nodemailer 10.0.x is what RUNS.** The locks say 10.0.12; this
   worktree's `node_modules` still holds **9.1.1** (the install errored EOVERRIDE — passing
   `morgan@1.12.1` explicitly duplicates the override this PR adds; a plain `npm install` is rc 0).
   **So `services/auth`'s 77 files / 836 tests passed against 9.1.1.** That is a READ of the call
   surface, not a RUN of the new major.
2. **`services/originate`'s suite green.** It does not load in this worktree: 93 files, "no tests",
   `Cannot find module '../routes/anchors'`. **PRE-EXISTING** — the diff touches ZERO non-manifest
   files, both modules exist in source, and auth passes off the same install. The gate should
   confirm it reds the same way at the BASE.

## COLD WRAP — this is my last mail
**Seven branches. ONE at origin (#1339). Six still committed-not-pushed**, deliberately: nothing
lands on an unproven bump. The handover (344 lines) names the successor's order of work:
**#1339 through gate41 alone → merge → rebase the six onto the post-bump `develop` → push.**
**Keep `worktrees/s-b43-ks1371` and its `node_modules`** — the successor pushes from it, and it holds
all seven branches plus a built `packages/shared`.
**Follow-up, NOT this PR:** leg 6 now advises removing two baseline rows no longer reported
(`GHSA-v2v4-37r5-5v8g`, `GHSA-mwp4-54f8-5fhr` = KS 729's). **#1339 edits no baseline row.**

**Hygiene:** shared checkout still `3bad652d17cf`, `.git/config` sha256 `4fc905a40a16e572`,
porcelain 17 — unchanged all session. **Total fetches ONE.** Lock taken and released four times,
every release with the pid the JSON holder file records; **none remains**. No `--no-verify`, no
force push, no baseline edit, no deploy, no `az`. KS-1374's comment stands as posted, verbatim.
**Eleven of my own instruments were wrong this round and all eleven were caught** — the four in
ITEM 3 and the bump are in the handover as traps.

🔴 **STILL KAM'S: the audit fuse — 21.9 h, computed 2026-09-29T02:08Z.** It needs his own DKIM mail to
`secuura-blockchain@agentmail.to`; none arrived all session. If it lapses before #1339 merges, all
seven branches are blocked again by the second wall.



### PR BODY (gh_body_1339.md) TEXT_SHA256 4c45d076570bde981c21d8065ab275c2f0877690121f49ab84038c39d7043d71

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



### EVERY COMMIT MESSAGE IN THE CHAIN over 8af6ab8216007462e596daed6b0adcd1e87e34ee (oldest first) TEXT_SHA256 96c0122db4f3fb8681d25f1fa9f9ae92426a0602eecf75aa40a25a0ae5e151fc

--- commit 8c1b25b24782d851817f8c7bb1c02d390fe750d7
KS-1378: bump morgan, nodemailer, ip-address and undici off five advisories

The push preflight FAILED legs 6 and 7 on develop's own dependencies, so NO push
on this repo succeeded. Five newly published advisories were absent from
scripts/audit/audit-baseline.json -- verified ABSENT at develop 8af6ab82 itself,
so not caused by any open branch.

Kam ruled card secuura-five-new-advisories-block-every-push-0929 = (a) on the
live board at 2026-09-29 11:43:09 AEST, verbatim:
  "Bump all four packages, with a quick reachability check in the same round."
No baseline entry for any of the five.

THE PROOF, both legs now green, verbatim:
  audit-gate: 23 distinct advisories reported, 25 baselined.
  OK - no advisories outside the triaged baseline.                      [rc 0]
  audit-locks: 43 standalone lockfiles ... 1612 distinct packages pinned
  - 18 advisories match, 18 already baselined.
  OK - no standalone-lock advisories outside the triaged baseline.      [rc 0]
Before: leg 6 read "30 distinct advisories reported, 25 baselined" with 5 NEW,
leg 7 "26 match, 21 already baselined" with the same 5. Measured across every
lock afterwards: ZERO vulnerable copies of any of the four remain.

FIRST PATCHED VERSIONS read from the GitHub advisories API, not inferred:
nodemailer 10.0.2 - morgan 1.12.1 - ip-address 10.5.1 - undici 6.28.1/7.29.1/8.10.2.

THE ROUTES ARE NOT UNIFORM, and two of them are not what the preflight implies:
- nodemailer: a lock refresh CANNOT fix it. The highest published 9.x IS 9.1.1,
  exactly what was pinned, and the fix lands in 10.0.2. MAJOR bump, declared in
  the root and in services/auth and services/originate.
- morgan: all ten declarers said ^1.10.0 and 1.12.1 is inside it, but a refresh
  keeps an already-satisfying tree. Declarations bumped to ^1.12.1 so it is
  explicit and reviewable rather than resolution-dependent.
- ip-address: @cardano-sdk/core asks ^9.0.5 and 9.x has NO fix, so only an
  override reaches 10.5.1. Added at the root and in packages/shared and
  services/anchoring, which have no root overrides to inherit.
- undici: the ROOT undici 5.29.0 (via @connectrpc/connect-node) is NOT vulnerable
  at all - every vulnerable range starts at 6.25.0. Only jsdom's nested 7.29.0 is.
  The override is therefore SCOPED to jsdom; a blanket one would have dragged a
  working 5.x runtime dependency to 7.x for no security gain.

A MEASURED BONUS, not claimed when the ticket was filed: leg 6 now reports
  CLEANUP (advisory): 2 baseline entries are no longer reported - remove:
    - GHSA-v2v4-37r5-5v8g (ip-address, KS 470)
    - GHSA-mwp4-54f8-5fhr (ip-address, KS 729)
  (the tool prints those two keys hyphenated; de-hyphenated here so this commit
   attaches only its own ticket. Otherwise the two lines are its output verbatim.)
so the ip-address bump also cleared KS 729's separate advisory. The ticket said
that "may also satisfy it; a bonus, not this ticket's claim" -- it is now measured.
Those two baseline rows should be removed in a follow-up; this PR does not edit
the baseline at all.

HOW THE LOCKS WERE REGENERATED, because it is not obvious and cost me four tries:
host npm 11.5.1 dies with "Cannot read properties of null (reading 'edgesOut')"
-- and it does so even on a bare package.json in an empty temp dir, so it is the
host npm build, NOT the workspace layout. Regenerated in node:24-alpine
(npm 11.19.0), each package.json resolved in an isolated directory inside the
container: 13 of 13 ok, 0 failed.

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
- Legs 6 and 7: rc 0 each, lines quoted verbatim above. That is the proof the
  ruling asked for.
- services/auth: 77 files / 836 tests, ALL PASSED, in this worktree.
- Zero vulnerable copies of any of the four across the root lock and all
  standalone locks, re-measured after the regeneration.
- `npm install --package-lock-only` at the root: rc 0, "up to date".

## NOT COVERED - stated, not papered over
- 🔴 **nodemailer 10 was NOT exercised at runtime.** The locks and declarations
  name 10.0.12, but node_modules still holds 9.1.1: my attempt to install it
  errored EOVERRIDE (passing `morgan@1.12.1` explicitly duplicates the override
  this PR adds -- a gotcha, not a defect; a plain `npm install` is rc 0). So the
  auth suite above passed against nodemailer 9.1.1. The call surface is two
  calls per service (`createTransport`, `sendMail`) and node >= 20 is satisfied
  (we run v24.7.0), but THAT IS A READ, NOT A RUN. A full install and re-run of
  both suites is owed before this merges.
- 🔴 **services/originate's suite does not load in this worktree**: 93 files
  failed with "no tests", on `Cannot find module '../routes/anchors'` and
  '../services/provenance'. PRE-EXISTING and not caused here: this diff touches
  ZERO non-manifest files, both modules exist in source, and services/auth's 836
  tests pass in the same worktree off the same install. Named because originate
  is one of the two nodemailer services and so its suite is owed too.
- The root `morgan` override is redundant now that all ten declarers say ^1.12.1.
  Kept as a guard against a future service declaring an older range; it is why
  `npm install morgan@<ver>` reports EOVERRIDE.
- No baseline entry added or removed. No --no-verify. Nothing deployed.

Refs KS-1378

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>



### PUSH LOG STOP COUNTS (READ, bounded region; /private/tmp/claude-501/-Volumes-DevMASTER--CODING-Secuura-Blockchain/f77d1935-dcce-45e9-85f6-265f00171214/scratchpad/push1378.out)

```
{
 "log": "/private/tmp/claude-501/-Volumes-DevMASTER--CODING-Secuura-Blockchain/f77d1935-dcce-45e9-85f6-265f00171214/scratchpad/push1378.out",
 "lines": 1349,
 "pre_push_hook_base": "28/0",
 "fixture_guard": "6/0",
 "run_shell_suites_region": "49/0",
 "run_shell_suites_prefixed": "49/0",
 "shell_suites": "60 passed, 0 failed, 0 skipped (of 60)",
 "CONTROL_absent_header": "NOT FOUND",
 "rc_line": "RC=0",
 "fixture_build_failed_lines": 0,
 "verdict_line": "PREFLIGHT INCOMPLETE — 12/15 legs ran, 3 SKIPPED. Nothing failed.",
 "preflight_ran": true,
 "rc": "?",
 "start": "?",
 "end": "02:06:10Z"
}
```

## SEAT RECORD /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/HANDOVER-seatB43-2026-09-29.md TEXT_SHA256 0d1d7bbb14299bebdd002bfbfeb476b83d4f4336f96775595d96a287f9b714d5

# HANDOVER — Seat B 43rd, Secuura/Blockchain, round 39

**Pane** `Secuura/Blockchain` (unsuffixed, tmux `fleet:main.1`). **Token** `b43`. **Tools** `*39`.
**Lock** `.push-lock-39`. **Gate** gate41 (never convened). **Window** 2026-09-29 00:34Z → 01:3xZ.
**Record folder** `5_Project_History/2026-09-29_seatB-43rd/`.
**Brief** Wednesday, `2026-09-29T00:34:23Z`, `[Wednesday -> Secuura/Blockchain] LAUNCH BRIEF (Seat B 43rd): 4 Spark raises + KS-1375 fail closed + N-1332-5, gate41`.

## STATE AT HANDOVER — this is final
🔴 **NOTHING IS AT ORIGIN AND NOTHING MERGED. Zero `-b43-` refs**, re-read by `ls-remote` after every
commit and after the failed push. **develop is untouched at `8af6ab8216007462e596daed6b0adcd1e87e34ee`.**

**ALL SIX ITEMS ARE COMPLETE AS BUILD WORK — six branches, committed, none pushed.** The four
Spark patches first:

ITEM 1 IS COMPLETE AS BUILD WORK: all four Spark patches applied, measured, green and COMMITTED —
and blocked from pushing by something that is not mine.** All four live in ONE worktree,
`worktrees/s-b43-ks1371` (named for the first branch; it carries all four), each on its own branch
off `8af6ab82`:

| ticket | branch | commit | diffstat | brief predicted |
|---|---|---|---|---|
| KS-1371 | `feature/ks-1371-unrevoke-refuses-negative-index-b43-1` | `4df536b5689bfba5fdb1dd0536d4ab8a55087970` | +21/−2 | +21/−2 |
| KS-1359 | `feature/ks-1359-platform-audit-log-refuses-bad-bounds-b43-2` | `c084f6cb2e25ec77051c55cde735d2f720f5ef2c` | +89/−0 | +89/−0 |
| KS-1369 | `feature/ks-1369-onproxyreq-skips-header-writes-once-sent-b43-3` | `3aeebf2cf09bb471b801c8dc9f2576bdd2da2f13` | +65/−0 | +65/−0 |
| KS-1360 | `feature/ks-1360-session-delete-carries-success-b43-4` | `b874efb05cae4b8c108443f287c54ded38119956` | +76/−1 | +76/−1 |

**Every count names the tree it was measured on — base `8af6ab82`:**

| | baseline | RED (test half ALONE) | GREEN | whole suite | tsc delta | eslint |
|---|---|---|---|---|---|---|
| KS-1371 vc-issuer | 16 f / 146 | **2 failed / 9** (U1,U2) | 9/9 | **16 f / 150** | ZERO | rc 0, 0 lines |
| KS-1359 api-gateway | 88 f / 795 | **4 failed / 7** (B1–B4) | 7/7 | **89 f / 802** | ZERO | 1 warning, PRE-EXISTING |
| KS-1369 api-gateway | 88 f / 795 | **2 failed / 3** (H1,H2) | 3/3 | **89 f / 798** | ZERO | 4 warnings, ALL PRE-EXISTING |
| KS-1360 wallet-connector | 7 f / 45 | **1 failed / 3** (D1) | 3/3 | **8 f / 48** | ZERO | rc 0, 0 lines |

Every README-predicted figure matched. Each patch was SPLIT product/test with the split proved
byte-exact against its canonical BEFORE applying (so the bytes verified are the bytes applied), and
each test half applied ALONE with the product file asserted unchanged — that is what makes the reds
attributable to the product rather than the harness. eslint warnings proved pre-existing by LINE
SHIFT, not asserted: KS-1359's :983 -> :989 (+6, the lines the patch adds), KS-1369's :684/:710 ->
:686/:712 (+2), same rule and message; the new test files report ZERO.

**Arms — two per patch, product file restored by BYTE COPY and sha256-verified equal after each.**
Each second arm discriminates something the first could not:
- KS-1371 A1 remove `< 0` -> 2 failed/9. 🔴 **A2 revert the MESSAGE only -> 9/9 STILL GREEN: the new
  message string is UNPINNED.** In that PR's NOT COVERED.
- KS-1359 A1 neuter `badInt` -> 4 failed/7. **A2 offset minimum 0->1 reds the offset-0 control: the
  MINIMUM is load-bearing, not merely the presence of a guard.**
- KS-1369 A1 guard removed -> 2 failed/3. **A2 guard MOVED below the first setHeader -> 2 failed/3:
  its POSITION is load-bearing.**
- KS-1360 A1 remove `success: true` -> 1 failed/3. **A2 `success: false` (key present) -> 1 failed/3:
  D1 pins the VALUE, not the key's presence.**

## ✅ KS-1378 IS RAISED — PR #1339, THE FIRST AND ONLY THING AT ORIGIN THIS ROUND
🔴 **READ THIS FIRST — it changes what "nothing at origin" means elsewhere in this file.**
**PR [#1339](https://github.com/Secuura/Distributed_Secuura/pull/1339)**, head
**`8c1b25b24782d851817f8c7bb1c02d390fe750d7`**, base `develop`, 28 files, **+5882/−4972**,
`Refs KS-1378` + `Refs KS-729`. **Push RC 0 and the branch VERIFIED at origin by `ls-remote`**, which
is the check that matters — my first push this round returned RC 1 with nothing pushed.
**Both audit legs passed INSIDE THE PUSH HOOK**, not only in my standalone run. Push preflight
**12/15 legs ran, 3 SKIPPED — legs 3, 4 and 8, all `local stack not up`. 12/15 is not a pass.**
**THE SUCCESSOR'S ORDER OF WORK:**
1. **PR #1339 goes to gate41 ALONE and must MERGE FIRST.** Nothing else may land on an unproven bump.
2. 🔴 **Its two owed items are gate requirements, not optional:** a **clean `npm install`** so
   nodemailer **10.0.x** is what actually runs (this worktree still holds **9.1.1** — auth's 836
   tests passed against the OLD version), and **both** `services/auth` and `services/originate`
   suites green on it. originate's suite does not load here at all (93 files, "no tests",
   `Cannot find module '../routes/anchors'`) — **pre-existing**, since the diff touches ZERO
   non-manifest files and auth passes off the same install.
3. **Then rebase the SIX held branches onto the post-bump `develop` and push them.** They are the
   six listed above, all still committed-not-pushed in `worktrees/s-b43-ks1371`.
4. **Follow-up, NOT this PR:** leg 6 now advises removing two baseline rows that are no longer
   reported — `GHSA-v2v4-37r5-5v8g` and `GHSA-mwp4-54f8-5fhr` (KS 729's). **PR #1339 edits no
   baseline row.** The ip-address bump cleared KS 729's advisory as a measured side effect.

## ✅ THE BLOCKER IS FIXED — KS-1378, and BOTH AUDIT LEGS NOW PASS
🔴 **This supersedes the section below, which described the blocker while it was open.**
Kam ruled the card **(a)** at 2026-09-29 11:43:09 AEST: *"Bump all four packages, with a quick
reachability check in the same round."* Ticket **KS-1378** filed (Urgent); branch
`feature/ks-1378-bump-four-advisory-packages-b43-7`, commit
**`8c1b25b24782d851817f8c7bb1c02d390fe750d7`**, 28 files, **+5882/−4972**.
**THE PROOF, both legs rc 0:** `audit-gate: 23 distinct advisories reported, 25 baselined. OK — no
advisories outside the triaged baseline.` and `audit-locks: … 1612 distinct packages pinned — 18
advisories match, 18 already baselined. OK — no standalone-lock advisories outside the triaged
baseline.` (Before: 30/25 with 5 NEW, and 26/21 with the same 5.) **Zero vulnerable copies of any of
the four remain**, re-measured across the root lock and every standalone lock.
**Patched versions read from the GitHub advisories API, not inferred:** nodemailer 10.0.2 · morgan
1.12.1 · ip-address 10.5.1 · undici 6.28.1/7.29.1/8.10.2.
**Two corrections to the preflight's framing, both measured:** the ROOT `undici@5.29.0` is **not
vulnerable at all** (every range starts at 6.25.0) so the override is SCOPED to jsdom; and
`@cardano-sdk/core` asks ip-address `^9.0.5`, a range that can NEVER reach 10.5.1, so only an
override closes it.
**A measured bonus:** leg 6 now prints a CLEANUP advising removal of two baseline rows —
`GHSA-v2v4-37r5-5v8g` and `GHSA-mwp4-54f8-5fhr` (KS 729's separate ip-address advisory). The bump
cleared KS 729's too. **This PR edits no baseline row**; that removal is a follow-up.
🔴 **HOW THE LOCKS WERE REGENERATED — it cost four failed attempts and the next seat should not
repeat them.** Host **npm 11.5.1 dies with `Cannot read properties of null (reading 'edgesOut')`**,
and it does so **even on a bare package.json in an empty temp dir** — so it is the HOST NPM BUILD,
not the workspace layout, and `--no-workspaces` does not help. Regenerated in **node:24-alpine
(npm 11.19.0)**, each package.json resolved in an isolated dir inside the container: **13 of 13 ok**.
⚠ Mount the repo at `/src`, NOT `/dev` — mounting over `/dev` clobbers the container's `/dev/null`
and the container dies `rc 127` before it starts.
🔴 **TWO THINGS OWED BEFORE IT MERGES, stated in the commit body:** (1) **nodemailer 10 was NOT
exercised at runtime** — the locks say 10.0.12 but node_modules still holds 9.1.1 (my install
errored EOVERRIDE because passing `morgan@1.12.1` explicitly duplicates the override this PR adds;
a plain `npm install` is rc 0). auth's 836 tests passed against **9.1.1**, so that is a READ of the
call surface, not a RUN. (2) **services/originate's suite does not load in this worktree** — 93
files, "no tests", `Cannot find module '../routes/anchors'`. **PRE-EXISTING**: this diff touches
**zero** non-manifest files, both modules exist in source, and auth passes off the same install.

## 🔴 THE BLOCKER — NOT MINE, AND IT BLOCKS EVERY PUSH ON THIS REPO
The push preflight **FAILED on legs 6 and 7**, `RC=1`, `PREFLIGHT FAILED on leg(s) 6 7 … (12/15 legs
ran)`. Five newly published advisories are **absent from `scripts/audit/audit-baseline.json` at
`8af6ab82` itself** — verified, not assumed — and none is reachable from my two vc-issuer files:
`GHSA-rpw4-54j3-4h4q` + `GHSA-2vr4-cq9g-pvrc` (**ip-address**, SSRF/trust-boundary, 3 locks incl.
`packages/shared`) · `GHSA-9f6g-j8ch-79g4` (**morgan**, log injection, **10 service locks**) ·
`GHSA-6vj9-mwq6-2f5v` (**nodemailer**, cross-tenant SMTP credential disclosure, auth + originate) ·
`GHSA-3wwx-pv8p-q78v` (**undici**, WebSocket DoS, frontend/issuer).
**I did not touch the baseline and did not use `--no-verify`.** Escalated; Wednesday carried it to Kam
as card `secuura-five-new-advisories-block-every-push-0929`, recommending (a) bump all four, with
(b) split and (c) baseline-all as alternatives. **Default at 12:30 AEST if he is silent: nothing is
accepted and pushes stay blocked.**

🔴 **THE CHEAP ROUTE DOES NOT EXIST FOR THE WORST ADVISORY. Measured:**
- **nodemailer — a lock refresh CANNOT fix it.** The highest published 9.x **IS `9.1.1`**, exactly
  what is pinned; `^9.0.3` is at its ceiling and latest is `10.0.12`. It needs a **MAJOR** bump in
  `services/auth` and `services/originate`. That is the most expensive of the four and it is the
  credential-disclosure one.
- **morgan — cheapest.** `^1.10.0` in 10 services, pinned 1.12.0, **1.12.1 is inside the caret**.
- **ip-address — partly.** `packages/shared` declares `^10.2.0` and 10.7.2 is inside it; the
  `@cardano-sdk/*` nested 10.4.0 copies and a 9.0.5 are TRANSITIVE (override or parent bump).
- **undici — transitive only**, under `jsdom` (a test dep) plus a 5.29.0.
**So option (a) is not one uniform bump: two are a lock refresh, one is a major, one is an override.**
Whoever takes it: it is Wednesday's stated NEXT ITEM and goes FIRST, on its own gate, before these four.

## 🔴 THE THREE SKIPPED PREFLIGHT LEGS, NAMED — B 42nd could not name them
`12/15` = 12 ran + **2 FAILED (6, 7)** + **3 SKIPPED: legs 3, 4 and 8** — Spec-auth conformance, Path
resolvability, Served-spec consistency. All three print `SKIP — local stack not up on
http://localhost:6882`. It is a local-stack gap, not a mystery. **12/15 is still not a pass.**

## ITEMS 2 AND 3 — BOTH SUBSEQUENTLY COMPLETED (this heading replaces "UNRAISED, HANDED OVER WHOLE")
🔴 **ALL SIX ITEMS OF THE BRIEF ARE BUILT, MEASURED AND COMMITTED. NOTHING IS UNRAISED.** This
section twice said otherwise, and both times that was a mis-read of my own budget — I read the
`<total_tokens>` session counter as though it were the context window. Wednesday read the pane
statusline instead (`ctx:44%`, then `ctx:49%`) and cleared me to continue on each occasion. The two
entries below are kept as corrections in place rather than overwritten, because a handover that
quietly rewrites its own history teaches a successor nothing.
**The lesson for the next seat: the pane statusline is the ONLY context instrument. The token
counter is a session budget and is not the window. Do not estimate it — ask.**

- 🔴 **ITEM 2, KS-1375 is DONE — this CORRECTS the line that stood here.** It read NOT STARTED,
  stopped on the ~65% budget line. That was a MIS-READ OF MY OWN BUDGET: I estimated context from the
  session-token counter, which is a session budget, instead of the pane statusline, which is the only
  context instrument. Wednesday read `ctx:44%` off my pane and told me to resume. I did.
  **Commit `e55010bcbef83bb5fc0f457a26261881afd82ed4`, branch
  `feature/ks-1375-verify-fails-closed-on-no-issuer-record-b43-5`, 3 files, +213/−9.**
  vc-issuer 16 f/146 → **17 f/155, 0 failed** · `packages/shared` **48 f / 945, 0 failed** · new cells
  **4 failed / 9** at the tip → **9/9** · tsc delta **ZERO on BOTH** packages · eslint rc 0, 0 lines.
  Both verify routes driven; the presentations route asserted through `credentialResults[]`, which is
  per-credential and therefore not confounded by `presentationProofValid`.
  **The refusal sits in the verifier's stored arm in `packages/shared`**, inside the existing
  `if (this.config.storedRecordResolver)` guard, so a consumer that never wired the arm is untouched.
  Arms (each REBUILT `shared` — it is consumed as built dist; an unrebuilt tamper is invisible and
  reads as inert): A1 refusal removed → all four RED cells; A2 reason reworded → the same four, so
  the card's exact wording is **PINNED, not decorative**; 🔴 **A3 refusal moved OUTSIDE the guard →
  C4 ALONE reds**, which is what proves that guard load-bearing.
  🔴 **The re-pin was EXACTLY ONE CELL, and it is the one KS-1368's own text names: C2.** Measured,
  not assumed — with the fix in and C2 untouched the suite read **154 passed / 1 failed** and the one
  failure was C2. Its **TITLE moved with its assertion**; F0/R1/R2/R3/C1 byte-unchanged and the diff
  holds exactly one changed `it(` line.
  🔴 **The cost is NARROWER than the card's wording.** The vc-issuer suite already runs DB-less, and a
  credential issued IN THE SAME PROCESS still verifies from the memory store (both controls, both
  routes). So it is "a DB-less stack refuses every credential IT DID NOT ITSELF ISSUE", not "every
  credential". Exactly one existing cell assumed otherwise: C2.
  🔴 **NOT COVERED, found while building:** `determineStatus` (`verifier.ts:562`) maps
  `!checks.status -> 'revoked'` UNCONDITIONALLY, so a no-record refusal still reports
  `docStatus: 'revoked'` — the exact mislabel KS-1368 option 2 chose its wording to avoid. The reason
  string achieves the distinction; the docStatus cannot without widening the published status enum.
  **The scoping notes below are what made this build cheap; kept for the record.**
- 🔴 **ITEM 3, N-1332-5 is DONE — this CORRECTS the NOT STARTED line that stood here.** Wednesday read
  `ctx:49%` off my pane and cleared it. **Commit `b2d84ffdcb59951f05dec68a5562409a85f1fb23`, branch
  `feature/ks-1054-deploy-scripts-read-startupmigrations-b43-6`, 4 files, +201/−0.** `Refs KS-1054`.
  **At the tip: 0 passed / 11 failed. With the change: 11 passed / 0 failed.** `bash -n` clean on all three.
  **Shape:** the rule lives in ONE new predicate, `deployment/azure/check-startup-migrations.sh`, which
  both deploy scripts call — that is what lets each caller be pinned SEPARATELY. **Arms: A1 removes the
  call from `deploy-all.sh` only → C1 alone reds; A2 from `deploy.sh` only → C2 alone reds; A3 neuters
  the failure branch → P2 and P3 red.** All three files restored by byte copy and `cmp`-verified.
  **Keyed on `failed`, never `error`** (gate39 N-G39-2 served `failed: 3` with no `error`); cell P3 pins it.
  **`/health` is untouched** — still 200 and healthy, no Dockerfile HEALTHCHECK change, no service code
  in the diff at all. The DEPLOY STEP is what fails, per Kam's option (a).
  **ABSENT field PASSES and warns loudly.** Reason, and the second one decides it: absence of the field
  is absence of evidence, not evidence of failure; and failing closed would block a ROLLBACK to an older
  image — the operation you need exactly when a deploy has gone wrong.
  🔴 **TWO defects caught here, both mine, both would have shipped:**
  (a) the predicate's first draft conflated "no argument" with "an EMPTY argument" (`BODY="${1-}"` then
      an emptiness test), so `check-startup-migrations.sh ""` fell through to `cat` and **BLOCKED ON
      STDIN FOREVER** — in a deploy that is a HUNG deploy, not a failed one, which is worse because
      nothing reports it. Cell P7 found it by hanging the suite. It now decides on argument COUNT and
      never reads a terminal.
  (b) 🔴 **`core.filemode` is FALSE in this repo, so git recorded the new helper as `100644`.** Both
      deploy scripts invoke it directly, so on a fresh clone the deploy would die on Permission denied;
      it only worked locally because my worktree carried the bit on disk. Caught by comparing against a
      known-executable sibling (`deploy.sh`, `100755`) rather than trusting the local `-x` test. Fixed
      with `git update-index --chmod=+x`; the amend changed the SHA, which is why it is `b2d84ffd` and
      not the `c9c07cc6` my first commit printed. **Any successor adding a script here must check the
      RECORDED mode, not the on-disk one.**
  The test file stays `100644`, matching `check_no_latest_tags.test.sh`; the runner invokes suites via
  `bash <path>` and that directory's convention is genuinely mixed.

### What ITEM 2 needs, already measured by me so the successor need not re-do it
- **Wednesday ANSWERED both open questions (2026-09-29T00:41:59Z), and both REVERSE the brief:**
  **Q1 — KS-1369 is TIER 1**, not T2 (it shipped as T1, reasons in that commit body).
  **Q2 — the KS-1375 PR carries `Refs KS-1375` AND `Refs KS-1368`**, because KS-1368's own option 2
  is Kam's card (b) verbatim, reason string included.
- 🔴 **KS-1368's ticket text NAMES THE RE-PIN FOR YOU:** "Cell `C2` … asserts that an id with no
  stored record still verifies true, so option 1 cannot be changed by accident — whichever option is
  chosen, that cell is the one to edit." I located it:
  `services/vc-issuer/src/__tests__/ks1352-revoked-credential-fails-verify.test.ts:166`
  `it('C2 control: an id with NO stored record still verifies true (Q1 ruling (b), pass-through)')`
  -> `:172` `expect({verified, statusCheck}).toEqual({verified: true, statusCheck: true})`.
  The file is **174 lines, 6 `it()` cells**: F0 fixture-health, R1, R2, R3, C1, C2.
  🔴 **ITEM 2 moves exactly ONE existing cell — C2 — and its TITLE must move with its assertion:**
  the title still reads "(Q1 ruling (b), pass-through)", the policy the change supersedes. A re-pin
  that flips the assertion and leaves the title is a cell that lies about itself.
  **R1/R2/R3 and C1 must stay byte-unchanged and that must be proved.**
- Kam's card `secuura-ks1352-unknown-id-policy-after-gate38` => **b**, `ruled_ts`
  2026-09-29T08:06:25.830535+10:00. Quote it verbatim; reason string exactly `'no issuer record'`.
- Anchors re-read at `8af6ab82`: `packages/shared/src/vc/verifier.ts` blob `5ec0953eb136`, `:478`
  `storedRecordResolver(credential.id)`, `:486` the ABSTAIN comment, `:397`/`:399` the structural-only
  and production branches; `services/vc-issuer/src/services/revocationResolvers.ts:54-57`;
  both routes wire it at `routes/credentials.ts:346` and `routes/presentations.ts:293`.
- ⚠ **`packages/shared` MUST be rebuilt after every edit** (`npm run build -w @secuura/shared`) — see
  the trap below. It is already built in the handed-over worktree.

## THE WORKTREE — REUSE IT, DO NOT DELETE ITS node_modules
`worktrees/s-b43-ks1371` on DevMASTER (523 GB free). It holds **all four branches**, a completed
`npm ci` (1936 packages) and a BUILT `packages/shared/dist`.
🔴 **I deliberately did NOT remove its `node_modules` at wrap, although the brief permits removing my
own regenerable leftovers.** That permission is conditioned on "AFTER your merges are verified" and
**nothing merged**: the next seat must push these four branches, the push preflight runs INSIDE the
pushing worktree, and a fresh worktree costs an `npm ci` plus a shared build. Deleting it would have
destroyed the only thing that makes the handover cheap. **Reuse this worktree.**

## TRAPS — EIGHT OF MY OWN INSTRUMENTS WERE WRONG, ALL CAUGHT
1. 🔴 **A census regex that could NEVER match.** `\b([A-Z][A-Z_]*38_?)\b` — after `_?` eats the
   underscore of `MERGE38_SCRATCH`, the required `\b` sits between `_` and `S`. It reported SEVEN
   ALL-CAPS prefixes and silently dropped the four largest (`PUSH38_` 5, `WATCH38_` 7, `MERGE38_` 4,
   `NAMECHECK38` 1 — **17 live occurrences**). The brief REQUIRES `MERGE38_* -> MERGE39_*`; from that
   census `MERGE39_` would not exist and the set-equals-read assertion would have had nothing to read.
   Corrected regex gives ELEVEN, which is also B 42nd's own count. **Keep the broken one as the control.**
2. 🔴 **`git checkout-index -a -f` SILENTLY REVERTED A PATCH I HAD JUST APPLIED.** It restores file
   CONTENT from the index, not only modes. `git apply` had printed "applied"; afterwards porcelain was
   0 and the new cells were gone. The brief says "restore the disk modes from the index after every
   git apply" — **that command is the wrong tool for it.** `.githooks/pre-push` is executable from the
   worktree checkout anyway; assert `test -x` and move on.
3. 🔴 **MY ARMS STACKED, and arm 2's reading was garbage.** The restore was a reverse text
   substitution guarded by uniqueness — but the KS-1269 original line **also exists in the revoke
   handler**, so after arm 1's tamper it occurs TWICE, the guard refused, the tamper stayed, and arm 2
   measured arm 1's damage. **Restore by BYTE COPY from a pristine file, never by reversing the edit.**
   A reverse anchor is not guaranteed unique even when the forward one is.
4. 🔴 **A patch splitter that returned ONE section for a two-file patch.** It split on `^--- a/`; a
   NEW file's section opens `--- /dev/null`. It would have made me apply a "test half" that was the
   whole patch, and the red-first proof would have been vacuous. Fixed to accept both — and the fix
   PROVED ADDITIVE: KS-1371's split is byte-unchanged by it.
5. 🔴 **A `git apply --check` control that mutated an ADDED line.** Added lines are not matched against
   the file, so the "mutated" patch applied cleanly and the control passed while proving nothing.
   **Only context lines (leading space) and removed lines gate `--check`.** Mutate one of those.
6. 🔴 **`timeout 300 npx vitest` -> rc 127.** macOS has no `timeout`. The suite never ran and a
   careless read is "the suite failed". (`gtimeout` is also absent here.)
7. **`--reporter=basic` was removed in vitest 4** — it fails with `loadCustomReporterModule` /
   `ERR_LOAD_URL`, rc 1, ZERO cells run. A harness fault that reads exactly like a product red.
8. **`${PIPESTATUS[0]}` is empty in the Bash tool** (it runs zsh). Write rc-dependent logic in a
   bash script FILE, or capture the inner rc explicitly.
Plus, from the brief and confirmed live: 🔴 **carry 7 is real** — `@secuura/shared` must be BUILT or
**11 of vc-issuer's 16 files fail to load with "(0 test)"**, which reads as 11 product failures and is
a fixture fault. `Cannot find package '@secuura/shared/vc'` is the tell; `npm ci` does not build it.

## THE `*39` TOOL GENERATION — 21 tools, at `2026-09-29_seatB-43rd/raise/`
Pass run ONCE at `2026-09-29T00:47:13Z`: **20 files, 205 LIVE lines rewritten, 50 prose preserved**,
then 20 renamed `*38 -> *39` (0 clobbered). `rekey38.py` quarantined FIRST into
`_b42_artefacts_NOT_MINE/` with B 42nd's three `merge38-1338*` records, its
`inbox_match38.TAMPER-no-b41st.py` and its five `s-b42-ks1370-*` push records — **10 files, each
sha256 proved equal against the ORIGINAL in B 42nd's folder, and the equality test shown able to FAIL
on a deliberately mutated copy.** `_pre_rekey_snapshot/` holds the 20 as they arrived.
- **NAMECHECK39** 7 checks / 0 bad, **21/21 controls fired**, 3 positives OK. C20 proves `b4` reads
  FOREIGN and not mine; the positives prove `-b43-` branches do not fire — **the prefix trap proved
  BOTH ways**. **C21 ADDED BY HAND for `b42`** — and the inherited prose at `:77` and `:300` already
  NAMED a C21 that did not exist in the list, a dangling reference; this is it. `ADOPTIONS` stays EMPTY.
- **BANNERCHECK39** CLEAN, **17 checked / 0 stale**, CONTROL A 17 stale over B 42nd's folder, CONTROL B
  17 stale asking my own folder for generation 40. Both PASS.
- **REKEY_CHECK39** MY COPIES **932 hits / 0 DEFECT-LIVE**; CONTROL A **1077 hits** on the originals;
  8/8 B, 4/4 C, 6/6 D, 4/4 E, 5/5 F controls behaved. THEIRS censused from disk (21 names).
- 🔴 **TRAP 4, EIGHTH GENERATION, PROVED ON REAL MAIL** (`trap4-eighth-generation-proof.txt`): with
  `b 42nd` present, 9 real subjects, 0 mismatches; **without it FIVE flip and B 42nd's real GO —
  "merge 1338 on gate40" — classifies FOR ME.** I would have acted on my predecessor's merge
  instruction. Subjects taken from the AgentMail API: **B 42nd's real GO carries NO ", signed" suffix**
  although Wednesday's staged header does.
- 🔴 **AN INHERITED FIXTURE DEFECT, THIRD GENERATION:** `watchproof39.sh:82` and `:161` asserted
  `LAUNCH BRIEF (Seat B 43rd): KS-1370 both halves + KS-1371 raise` — B 42nd's TOPIC with my seat
  number re-keyed in. **That subject has never existed.** B 41st recorded this exact shape one
  generation ago. Both re-pointed at my real subject, with B 42nd's real GO and plan ANSWER added
  beside them as FOREIGN fixtures.
- 🔴 **`lock39.sh`'s release was BROKEN and I fixed it.** `$REC` was unguarded, so a call without a
  record dir wrote to `/lock-released.txt` on the read-only root — **and that write sat inside the
  release's `&&` chain, so it printed `RELEASE FAILED` AFTER the lock had already released.** A false
  verdict on a successful release. Now: `$REC` required and checked, and the verdict depends on the
  release alone. Proved both ways (no recdir REFUSED, missing dir REFUSED, real take/release OK).
- **The hex guard is INERT this generation and I say so** rather than counting it as evidence: `b43`
  and `b42` occur ZERO times in any digit-bearing hex run across the 20-file set, my session uuid and
  all ten SHAs I pin. The fixture uuid carries `b41`, which is not a key of mine. Kept as the PATTERN.
  ⚠ **The brief's "7 `b41` hex runs" is 2 in the working set + 5 in the quarantined `rekey38.py`** —
  same measurement, different denominator. A count names the tree it was measured on.

## A CORRECTION TO MY OWN CORRECTION
I told Wednesday the README's "five header writes" for `onProxyReq` was wrong and there are seven plus
a body write. **Right about the file, wrong to call the README wrong.** The control cell's expected
list is `['set X-Request-ID','set Authorization','set Content-Type','set Content-Length','write']` —
the calls a LOGIN request actually triggers; the vouch and two policy headers are conditional.
**Seven is a property of the source, five of the fixture.** A correction is a claim like any other.

## REFUSED AND DISCLOSED
The launcher's boot pull/fetch on the shared checkout (`git status` + `ls-remote` only) · the
SessionStart hook's `POST /api/seen` (`EXTRANET_ME=kam` — it clears **Kam's** flags) · the boot
prompt's "CC Kam on every email" · its rule-7 extranet to-do. **Preflight NOT clean: `[F-02] No SSH
identity available for git`** — it did not bite; the repo-local `core.sshCommand` carried the attempt.
The file's `# launch 2026-09-29T00:34:29Z` equals my own session start to the second, so it is MINE.

## SHARED CHECKOUT — the ONE refresh, PLUS one config write I must disclose
🔴 **CORRECTION to my own READY mail, which said `.git/config` was unchanged all session.** It is
`4fc905a40a16e572` at boot and **`4f624a213933d54b` at wrap**. The cause is MINE: `git push -u`
sets upstream, and for a WORKTREE branch that upstream is written to the SHARED `.git/config`.
Exactly three lines added at :1114-:1116,
`[branch "feature/ks-1378-bump-four-advisory-packages-b43-7"]` + `remote` + `merge`. **HEAD, local
`develop` and porcelain are all unchanged.** Left in place deliberately: the successor pushes that
branch and wants its upstream. **A successor using `push -u` from a worktree should expect this.**

HEAD and local `develop` stayed `3bad652d17cf111c1e2e1bed1ae7686894637487` all session; `.git/config`
sha256 `4fc905a40a16e572` unchanged across the fetch; porcelain 17 `??` / 0 tracked, before and after.
**Total fetches: ONE**, taken under `.push-lock-39` (`origin/develop` `0de108577e61` -> `8af6ab821600`,
`8af6ab82` went `fatal` -> `commit`, control bogus sha `fatal` both sides, tree `4d2c269e3381` =
gate40's declared END). Receipt: `2026-09-29_seatB-43rd/tracking-ref-refresh.txt`.
Lock taken and released **three times**, every release with the pid the JSON holder file records
(52790). **No `.push-lock-*` remains.**

## 🔴 STILL KAM'S, AND ON A CLOCK
1. **The five advisories** (card `secuura-five-new-advisories-block-every-push-0929`). Until he rules,
   **no push on this repo succeeds** — mine or anyone's.
2. **The audit fuse `2026-09-30T00:00Z` — 22.4 h at this wrap** (computed 2026-09-29T01:35Z with my
   shell). It needs **his own DKIM mail** to `secuura-blockchain@agentmail.to`; a Wednesday relay and
   a prompt line are both machine text. **Zero mail from him all session.** After it, every
   Blockchain/Dev push and merge is refused fleet-wide — so the four branches above have TWO walls in
   front of them, and the second one is on a timer.


## SEAT RECORD /private/tmp/claude-501/-Volumes-DevMASTER--CODING-Secuura-Blockchain/f77d1935-dcce-45e9-85f6-265f00171214/scratchpad/leg6.out TEXT_SHA256 db89ae72858368c32d93d725d8fa2110cb17436ccfe7dbf1da47bf4edbaeb094

audit-gate: 23 distinct advisories reported, 25 baselined.

CLEANUP (advisory): 2 baseline entries are no longer reported — remove:
  - GHSA-v2v4-37r5-5v8g (ip-address, KS-470)
  - GHSA-mwp4-54f8-5fhr (ip-address, KS-729)
OK — no advisories outside the triaged baseline.


## SEAT RECORD /private/tmp/claude-501/-Volumes-DevMASTER--CODING-Secuura-Blockchain/f77d1935-dcce-45e9-85f6-265f00171214/scratchpad/leg7.out TEXT_SHA256 32a435040b9618c3419c5531a90f3566545ea21f6d6858bb36b66d1201ef00a1

audit-locks: 43 standalone lockfiles (45 tracked, minus the Blockchain/Dev/package-lock.json workspace root which audit-gate covers, minus 1 declared out of scope = 45 - 1 - 1 = 43; reproduce the tracked count with `git ls-files '*package-lock.json' | wc -l`; out of scope: Blockchain/Dev/mobile/secuura-app (KS-769, expires 2026-10-19: React Native app tree, not built by any compose file (0 references against a control of 2 for services/originate) or by any workflow (0 against a control of 3 referencing services/). 81 advisories (2 critical, 45 high) pending their own triage rather than 81 unmeasured baseline rows.)), 1612 distinct packages pinned — 18 advisories match, 18 already baselined.
OK — no standalone-lock advisories outside the triaged baseline.


## SEAT RECORD /private/tmp/claude-501/-Volumes-DevMASTER--CODING-Secuura-Blockchain/f77d1935-dcce-45e9-85f6-265f00171214/scratchpad/nmtest.out TEXT_SHA256 9732c5271a5e8cbf0e91ac11d5ed4c3411f25a0a223b7c0c56a35ea8e987224b

--- installing nodemailer@10 + morgan@1.12.1 into the worktree tree so the suites test the REAL new deps ---
npm error code EOVERRIDE
npm error Override for morgan@1.12.1 conflicts with direct dependency
npm error A complete log of this run can be found in: /Users/kam_code/.npm/_logs/2026-09-29T01_55_24_003Z-debug-0.log
install rc=0
nodemailer now: 9.1.1
--- auth suite ---
 Test Files  77 passed (77)
      Tests  836 passed (836)
--- originate suite ---
 Test Files  93 failed (93)
      Tests  no tests


## SEAT RECORD /private/tmp/claude-501/-Volumes-DevMASTER--CODING-Secuura-Blockchain/f77d1935-dcce-45e9-85f6-265f00171214/scratchpad/ovtest.out TEXT_SHA256 b9e24d8b651e0b1adcde243ff1864bead6c833183ca923c0c5b3bcc2d7b39b63


up to date in 698ms


## SEAT RECORD /private/tmp/claude-501/-Volumes-DevMASTER--CODING-Secuura-Blockchain/f77d1935-dcce-45e9-85f6-265f00171214/scratchpad/reachability.md TEXT_SHA256 b3dabba9bcd03eba78c010b200bf3c85d8d014b32b6cba724d65d7ae93cd248d

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


## SEAT RECORD /private/tmp/claude-501/-Volumes-DevMASTER--CODING-Secuura-Blockchain/f77d1935-dcce-45e9-85f6-265f00171214/scratchpad/pr1378-body.md TEXT_SHA256 f4bc7c10b73b696c3b5f6b1d3f984a47b65a5a45cac5d66c416af518f0ddfb37

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


## SEAT RECORD /private/tmp/claude-501/-Volumes-DevMASTER--CODING-Secuura-Blockchain/f77d1935-dcce-45e9-85f6-265f00171214/scratchpad/push1378.out — TAIL (last 40 of 1349 lines); the WHOLE file's TEXT_SHA256 c209080ffdf8091d2187b530170987d952ba6918ec3a6b161d7d2c11d6224799

ok   hermetic-env leaves bash's own OLDPWD alone
ok   hermetic_strip_except keeps the named variable and strips the rest
ok   a wrapper that cannot be measured is FATAL (exit 2), never an empty strip
ok   CONTROL: without the strip a sourced shell redirects the cell to slot 2's gateway (http://localhost:6982) — the leak is real
ok   with the strip the cell resolves the closed port it named, not the sourced slot

slot_target: 119 passed, 0 failed

shell suites: 60 passed, 0 failed, 0 skipped (of 60)
shell suites wall-clock: 291s

=== 15/15  Every check-*.sh guard must have a HOME, and the wired ones must pass (KS-926) ===
OK — all 21 tracked guards accounted for (21 buckets entries).
OK — no inline event handlers in connector JS.
OK — all 35 Dockerfile(s) drop root for runtime.
OK — all resource-group references are in the allowed set.
OK — no hardcoded *123 password literals.
check-no-latest-tags: examined 5 of 5 advertised file(s).
OK — no :latest tags found in production-bound configs.
OK — no Math.random() in security-relevant paths.
OK — no PII store file is tracked by git.
OK — no string-concatenated SQL found.
OK — no TS-strictness flips found in Dockerfiles or build scripts.
production-guard coverage: 23 / 23 services
OK — 7 portability rules hold across 102 shell scripts (KS-666).
OK — 100 shared-stack safety invariants hold (KS-666).
[L7] test-wallet.env not present — nothing to check
OK — 13 code guards passed.

PREFLIGHT INCOMPLETE — 12/15 legs ran, 3 SKIPPED. Nothing failed.
  legs 3 4 8 — local stack not up; you can clear this by starting it.
  This is NOT a pass. Do not quote it as one — say which legs ran.
remote: 
remote: Create a pull request for 'feature/ks-1378-bump-four-advisory-packages-b43-7' on GitHub by visiting:        
remote:      https://github.com/Secuura/Distributed_Secuura/pull/new/feature/ks-1378-bump-four-advisory-packages-b43-7        
remote: 
To github.com:Secuura/Distributed_Secuura.git
 * [new branch]          feature/ks-1378-bump-four-advisory-packages-b43-7 -> feature/ks-1378-bump-four-advisory-packages-b43-7
branch 'feature/ks-1378-bump-four-advisory-packages-b43-7' set up to track 'origin/feature/ks-1378-bump-four-advisory-packages-b43-7'.
RC=0

