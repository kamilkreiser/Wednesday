# DRAFTER REPORT: Seat J 16th, lane A (auth) -- 2026-11-05 ~16:25 AEDT

**BLUF.** Brief: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-11-05_seatJ_laneA_auth.md`. Seat J, ordinal **16th** (max numbered J heading in history.md = 15th; one UNNUMBERED J entry at history.md line 6892, 2026-10-26, KS-1717: if Wednesday counts it, this seat is the 17th; the brief tells the seat the launch mail wins). Model `claude-opus-5-5`, row C3 (+ G1 for the gates). Develop tip at drafting `5fc5569ed96a`. Six of seven tickets are in; **KS-1407 is in but is a stop-and-ask item (its remaining work is outside the auth family) and KS-1585 is EXCLUDED (readers are in services/security + packages/shared).** The seat was NOT sent anything; no repo, Linear or mail write was made by the drafter.

## Tickets included, in order, with the scope sentence quoted
1. **KS-1150** (High) -- "Three pre-existing gaps on ONE logical path ... `POST /api/oauth/token` ... One test pass, one fix on one file, three items". R-1 delivered (PR 987); brief commissions **R-2 + R-3 as one PR (a narrowing, stated)**. Measured open at develop: `denylistRefreshJti(` 0 in oauth.ts (control 2 in auth.ts); `ServiceUnavailable` 0 in oauth.ts; catch at lines 1118-1127 answers 500.
2. **KS-1407** (High, unassigned) -- "Left open: N-1382-2 and gate note N1". **Measured:** N1 is ALREADY on develop (commit `21e2ffd20`, KS-1692 PR 1669, ancestor of develop; try/catch at users.ts:1012-1030 and auth.ts:909-924), so the ticket's last comment is stale on N1. N-1382-2 is the e2e spec `Blockchain/Dev/tests/e2e/tests/security-bad-actor.prelaunch.spec.ts` lines 1155/1182 -- outside services/auth and in no lane of lanes.md. Brief: seat re-verifies N1, sends one QUESTION (`ks1407 outside family`), continues with KS-1460. It is not told which route the e2e should call.
3. **KS-1460** (Medium) -- "Left open: the six remaining discarding callers in `routes/auth.ts` that comment 73f91c88 names." Measured six at develop: auth.ts lines 561, 616, 1385, 1389, 1471, 1475. The comment says converting all six is "not right"; the per-caller design is left to the seat with a QUESTION (not pre-answered).
4. **KS-1968** (High) -- "Left open: B2, change-password." Brief commissions **B2 only** (narrowing stated: admin/create and OpenAPI 422 descriptions not commissioned). PRs 1796/1798 (the stated wait) ARE merged and ancestors of develop. **B2's file is `routes/users.ts:975`, not `routes/auth.ts`** as lanes.md inferred (users.ts imports no `isPasswordBreached`; B1 already in auth.ts).
5. **KS-1804** (Medium) -- "Left open: note 1 is not done." Measured (plan said UNMEASURED): `services/passwordLoginGate.ts` const at line 69, last import at line 72; remedy "move the const below the last import". Note 2 delivered (PR 1826). Product file, so not under the no-deploy-surface addendum; the brief asks the seat to prove zero behaviour change and propose tier 1.
6. **KS-1858** (Medium) -- "Left open: gate note G67-F3, a whitespace-only token, passes the new guard on all four adapters." Measured: google:88, facebook:83, linkedin:86, microsoft-personal:88 still test only `=== ''`. Whether github.ts joins is left as a seat question; KS-1917 (error-field parity, Backlog) stays out.
7. **KS-1797** (Low) -- "Left open: the POST half is not covered by either PR." Description leaves open "whether POST should refuse an array `state` or coerce it"; the brief does NOT pre-decide it (QUESTION `ks1797 post array`). Placed last (shares oauth.ts with KS-1150).

Queue order is Wednesday's, which honours the same-file note (auth.ts: 1460 then 1968; oauth.ts: 1150 then 1797); it differs from lanes.md row order (1968 before 1460). Given the B2 finding the auth.ts constraint does not actually bind 1968, but the order is kept.

## EXCLUDED
- **KS-1585**: Kam's card `secuura-ks1585-scope-rows-on-admin-change-1105` = b (ruled 2026-11-05 16:09:46 +11:00, "Keep them; readers apply a row only while the user is still ADMIN", read at source by exact id). The readers live in **services/security** (`adminScope.ts`, `index.ts`) and **packages/shared** (`src/security/keyRevokePolicy.ts`); `git grep admin_organisation_scopes` at develop finds 10 files, none under services/auth. Belongs to lane E (security service). Named in the brief as excluded.
- Not included by design: KS-1690 (refresh-token session binding, same grant as KS-1150 R-2; the brief tells the seat to stop and ask if R-2 forces that decision), KS-1692 PR 2 (session.ts half), KS-1917.

## UNMEASURED (each is conditional in the brief)
- Whether any OPEN PR touches these files (no GitHub PR list read; only `ls-remote --heads` by key, which shows old merged branches for 9 keys).
- Contents of the tools to copy (names only read).
- Whether `docs-fragments.mjs` usage is unchanged since the E 36th brief.
- Location of the OpenAPI 422 descriptions (KS-1968 extras).
- Staged ANSWER mails to Blockchain-J since its last brief (section 6 carries only rulings read from the S 20th exemplar and the traps file).
- Seat's pane id; no live behaviour on any box (none contacted).
- `human_owned.md` is not a complete list: KS-1098 (said by SUMMARY to be Peter's) has 0 hits in it; the Linear creator/assignee read (all ours; KS-1407 unassigned) is the primary evidence, positive control KS-256 = 1 hit.

## Things that looked wrong in the lane plan
1. lanes.md put KS-1968 B2 in `routes/auth.ts`; it is `routes/users.ts`.
2. KS-1407 "file UNMEASURED": it is a test file outside every lane, and half its remaining scope (N1) is already delivered by KS-1692 (a stale ticket comment, and its board state could be corrected by Wednesday or the close-out seat).
3. KS-1797 summary reads "answers 400 invalid_request, not 500" for POST; the ticket says POST arrays do not 500 and leaves refuse-vs-coerce open.
4. KS-1585 sits in no lane A file at all (lane E).
5. Branch names for six of the keys already exist on origin (merged work); the brief says to cut new branches from develop.
6. SUMMARY's "KS-1098 is Peter's" is not in human_owned.md.

## Gates run on the brief
Scope-claim words (send_brief.sh:434 regex): 0 hits. Gate literals present at line start: `RULED BY KAM, NOT YET IN AN ARTEFACT` (line 117), `PROVENANCE:` (134), `SELF-CHECK: re-read end-to-end for contradictions | <stamp>` (152). `self_check_view.sh` was run once; Wednesday should re-run it after any amendment.

/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-11-05_seatJ_laneA_auth.md
/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-11-05_seatJ_laneA_auth_DRAFTER-REPORT.md
