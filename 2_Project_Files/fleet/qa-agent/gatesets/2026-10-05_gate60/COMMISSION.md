# gate60 — the commission (Wednesday -> kit drafter, 2026-10-05 ~07:24Z / 18:24 AEDT), as received

You are a QA-gate KIT DRAFTER for Wednesday (Kam's coordinator agent). Build ONE gate kit folder:
`/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-10-05_gate60/` for **gate60**: a tier-1 (T1, auth/security surface)
QA gate on Secuura/Blockchain **PR #1384 (KS-1210)**: OAuth apps — scopes become a closed vocabulary (the nine AVAILABLE_SCOPES),
`{admin:read, admin:write}` only for platform roles (a local copy of users.ts:192's four-role list + a drift cell), and owner-or-admin 404 on
the four by-id routes (gate on `OAuthApp.createdBy`, users.ts:439's six-role list), in `Blockchain/Dev/services/auth/src/routes/oauth.ts`, a
NEW test `…/__tests__/ks1210-oauth-app-scopes-and-ownership.test.ts` (24 cells), two sibling test fixes (ks431, ks451), and block `18.` in
both platform-k docs.

FACTS (Wednesday's ls-remote 07:23:10Z): develop `46c3e20cfbd21acee0c67d544180c33deaa4c8ef`; `refs/pull/1384/head` == branch
`feature/ks-1210-oauth-app-scopes-and-ownership-e3-1` == `852fc927632095fb603583cb543050d5edd66111`; author's END_TREE
`632b07492c9501ad4e36bd5f20b62e4240b7394e` (its head tree; single parent == develop). Other open PRs ruled to land BEFORE it: #1381 (KS-1345,
head 82e6bfa9de85, doc block 13.), #1382 (KS-1005, head 80bafc849a54, doc block 19., touches auth routes/users.ts — NOT oauth.ts). KS-1210
conflicts with each of them on the two docs only (author-measured).

INPUTS: the READY at `fleet/briefs_staged/2026-10-05_seatE3_READY_1384.txt` (whole); the author's brief
`fleet/briefs_staged/2026-10-05_seatE3_successor.md` (row 1 + Q-1210 rulings: nine scopes; admin pair platform-only; owner-or-admin 404;
`certifications:write`/`webhooks:manage` deliberately NOT privileged); the Q-1210 ruling context in Seat E 2nd's brief
`fleet/briefs_staged/2026-10-05_seatE2_successor.md`; the SHAPE to copy: `fleet/qa-agent/gatesets/2026-10-05_gate59/` (the latest T1 auth gate,
same lane) and `…/2026-10-05_gate57/`; the QA charter + `fleet/qa-agent/BRIEF_TEMPLATE.md`.

ROWS (gate59 naming): C1 PIN (ls-remote + API, single parent, 6 paths, END_TREE, 0 trailers with control `bf277eead268` 55 bytes, subject ≤92
no `(#`, one `Refs KS-1210`, other keys de-hyphenated); C2 HUNK vs ticket + the class hunt (every route that writes/reads OAuth app scopes or
loads an app by id: are all gated? `services/oauth.ts` getAppById/updateApp are id-only — the gate must be in every by-id handler); C3 red-first
(cells red at develop, green at head), full auth suite before/after (known pre-existing ks949 timeout flake: name it, prove the file is
byte-identical base/head), tsc with a planted control, `npm run check:openapi`; C3b SECURITY PROBE: tenant/role matrix — owner, other-tenant
user, same-tenant non-owner, tenant admin, platform admin, connector principal — on create (scopes in/out of vocabulary, admin pair by role),
list, get/update/delete/rotate by id; scope-escalation attempts (case, whitespace, duplicates, NUL, unicode look-alikes, `admin:*`); existing
apps that already hold a now-refused scope (named NOT migrated — measure what they can still do); C4 docs (block 18., number order, predicted
merge-in after #1381 and #1382 computed in the gate's OWN scratch clone); C5 PR text (Test Evidence, NOT COVERED incl. live sweep owed, the
gateway has no role gate for /api/oauth/apps, existing apps not migrated); C6 NOT COVERED. A Q-M rule for a later merge-in head (gate59 shape;
develop's advance path-disjoint from auth `routes/oauth.ts`, `services/oauth.ts`, the ks1210/ks431/ks451 tests). GO string:
`GO (Seat E 3rd): merge 1384 on gate60`.

HARD RULES: write ONLY inside that kit folder and `/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/4633ab20-117b-4d2e-a571-ce5d0598b988/scratchpad/g60/`;
do NOT edit `inbox_routing.conf` (put the exact routing line in the README, gate59 shape); `!CODING` is READ-ONLY (git
show/log/ls-tree/cat-file/ls-remote with the project's sshCommand); clones only via `git clone --shared` into the scratchpad; never run the
suites yourself (that's the gate's job) — only your scripts' `--selftest` on synthetic input; never `cd`; never delete; rc on its own line
(zsh, no PIPESTATUS); every check prints how many items it CHECKED.

Reply with: folder path, file list, exact routing line, exact launch command (gate59 README shape), selftest results, and up to 8 doubts
(D1..D8) for the gate, most important first.
