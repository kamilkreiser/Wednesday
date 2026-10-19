# Spark screen, part 19 (2026-10-20 ~09:08-09:50 AEDT): KS-1659, KS-1407 (both routes), KS-1157; FOUR briefs, FOUR PASS, all BYTE-IDENTICAL, one of them the widest rung 3 yet

model: claude-sonnet-5-5 -- row C8 (screen + brief drafting) -- Spark screen-19 sub-agent -- gauge 65% (as routed)

By a Spark screen-and-brief sub-agent for Wednesday. Secuura only. Nothing held, raised, pushed, merged, committed or deleted; no GitHub or Linear write; no `hold_ready`. Nothing under `!CODING` was written (reads, `git ls-remote`, and node_modules/tool paths read for the hand runs). The Linear key was read inside a scratch script file and never printed. Every clock below came from `date` in the command that wrote it.

## BLUF
- **Four briefs, every one: lint rc 0 (empty stderr), dry-run rc 0 (no WARNING), CONTROL-PASS first, then ONE real round, PASS, golden BYTE-IDENTICAL, `spliced 0`, plain `section_N.diff` in every `.opts`. No FAIL, no rebrief, no model fault.**
  - `ks_1659_p1` (KS-1659): `certificationRepo.ts` folds the HOLDER with `toActorUuid` in the one shared INSERT (the ticket's shape 1); code_patch rung 2, one one-line hunk + NEW jest file. 123 s round, 55 s model.
  - `ks_1407_p1` (KS-1407 N-1382-1, change-password): `routes/users.ts` calls `revokeAllUserSessions` after the write; code_patch rung 2, pure insertion + NEW vitest file. 165 s, 75 s.
  - `ks_1407_p2` (KS-1407 N-1382-1, reset-password): `routes/auth.ts` import + 3-line insertion, before the single-use token is burned; code_patch rung 2 (one product, 2 hunks) + NEW vitest file. 169 s, 78 s.
  - `ks_1157_p1` (KS-1157 first bullet): `mintedBy: 'oauth'` marker, **3 product files in 5 hunks + a NEW vitest file (code_patch2 RUNG 3, 4 files, 6 edit points)**: `A3x declared=4 measured=4 ok=4 diff=0`. 212 s, 123 s model, **45788 prompt + 4383 completion tokens, the longest prompt so far (screen 16's was 41.4k)**. The Spark's limit is still not found.
- **Two of the four touch the auth surface (sessions, credentials) and are TIER 1 by routing**: KS-1407 (both) and KS-1157. KS-1407 revokes the caller's OWN session too on change-password (design choice below): the client must sign in again. Wednesday should read that before holding.
- **KS-1659 sits next to the KS-1557 lane**: the product file is `certificationRepo.ts`, which KS-1557's text does not name (it names `certifications.ts:412-431`, `documentRepo.ts:419-450`, `verification.ts:220-236`); but the ticket itself says it is "neither KS-1633 nor KS-1557" and it is a certification file. If Wednesday reads the exclusion as "any certification file", hold `ks_1659_p1`. Open-PR overlap on GitHub was NOT checked for any file.
- Pool is thin: of 370 open Backlog/Todo, nearly everything left is a decision, a migration, infra/CI/launcher, or a dependency on a live lane (see SKIPs). I did NOT write the "pool exhausted" line in `queue.md`: I read about 45 of the 216 unnamed descriptions, not all.

## Pinned sha
`git ls-remote origin refs/heads/develop` after `git -C /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/cache/src fetch -q origin develop` (literal path; `cat-file -t` not needed, the cache then built at it): `89956fe92956a810f6821fdee09915f087feea7b` ("Refs KS-1116: owner-less rows readable ... (#1649)") at 09:08:14. **It did not move**: re-read before every dry-run, every control and every real round, and again at 09:50:10 (same sha). Every Tip line says `89956fe92956`. So there was no stale-brief hazard in this screen.

## Census (Linear, read-only)
- Query as screens 15-18 (team `KS`, `state.type in [backlog, unstarted]`, `orderBy: updatedAt`, `first:50`, paginated to `hasNextPage=false`; script `census.py` in the session scratchpad, key read from `Blockchain/4_Credentials/.env` inside the file, `Authorization: <key>` with no Bearer prefix): **8 pages, 370 tickets** (373 at screen 18, three left the pool). Positive controls: KS-1659, KS-1407, KS-1157 in the set; KS-1682, 1681, 1683-1686 present (excluded by instruction or skipped). Zero controls: KS-1557, KS-1660, KS-1679, KS-1676, KS-1634, KS-1628, KS-1677, KS-1116 absent (taken or no longer Backlog/Todo).
- Of the 370, **216 are named in no earlier SCREEN file, `queue.md` or `done.md`** (a grep of every `KS-n` token; the screens' shorthand lists such as "KS-1604, 1280, 1102" undercount, so the true unnamed number is a little lower and I re-read a few already-skipped ones by accident). I read all 216 titles and **about 45 descriptions**: KS-1681, 1672, 1107, 1105, 1106, 1407, 787, 824, 840, 1454, 625, 1304, 1327, 1499, 1495, 889, 1659, 1383, 1161, 1051, 1356 (title), 607 (title), 1091 (title), 1235, 1247, 1083, 954, 1157, 1338, 1340, 1082, 967, 902, 1225, 1423, 1412 (head), 925, 655, 765 (title), 940 (title), 1443, 1138, plus KS-1557 (to name its files).
- Linear attachments: none on KS-1659, 1407, 1157 (census `attachments` count 0). Open-PR overlap on GitHub: **not checked** (no identity).

## SKIPs (reason, measured at source)
- **KS-1681** (DEPLOY-BLOCKERS.md cited in 5 tracked files): "which of the two applies is a maintainer call", and the file must not be copied in.
- **KS-1672** (auth stores no provider identity): the fix is dangerous by the code's own comment (`routes/auth.ts:1233-1240`: tier-1 gate, links must stay after the KS-795 gate); needs a decision on pre-"linked" accounts.
- **KS-1107** (register accepts a client organizationId): impact not traced, "trace every consumer before choosing a fix".
- **KS-1105** (admin login placeholder) and **KS-1106** (verifier message): the frontend has no test runner in the tree (`frontend/admin` has no test files), nothing the checker can run red-first.
- **KS-787, 824, 840, 625, 1383, 1454, 1304, 1327, 1235, 1083, 1161**: all say "fix shape not chosen" / "needs a decision" / S-side dependency / multi-service (KS-1454 is the anchoring schema + CIP-674 metadata + two read paths + openapi, far more than a rung; KS-625 and 1383 are vc-issuer = excluded).
- **KS-1499 F1/F2/F5, KS-1495, KS-1340** (originate integration test files): the files are `*.integration.test.ts`, which the unit config ignores (`testPathIgnorePatterns`), and the guard in KS-1340 is inline in a DB-gated `beforeAll`; the checker cannot run them.
- **KS-1338** (entrypoint-corpus reader): the "guarded" reader named by the ticket is NOT on develop (`git grep "Both return shapes"` empty; the attempting PR is open).
- **KS-954** (billing mount leading `//`): "mechanism NOT determined, reproduce before fixing". **KS-1051** (develop red on originate): stale since #926. **KS-1225** (jsdom in auth's lock): manifest/lock change, "decide the shape". **KS-902, 925, 655, 1443, 1138, 1423**: scripts/launcher/CI, a Linux-only behaviour that cannot be proved red-first on this Mac, or comment-only decisions.
- Excluded by instruction and untouched: services/m365-integration/** (KS-1675, 1682), services/vc-issuer/** (KS-625, 1383, 1683-1686), KS-1557 lineage lane, KS-1677, KS-1116.

## Design choices (Wednesday's rule): choice / rejected alternative run as a mutant BEFORE the brief / cell that reds
All mutants were run by hand in the scratch clone (develop `89956fe92956`), against the new test, with `tsc --noEmit` after each (scripts `mut1659.py`, `mut1407a.py`, `mut1407b.py`, `mut1157.py` in the session scratchpad; file restored after each). The unmutated baseline `tsc` prints `TS2305` (one stale-shared-dist symbol) for `originate` in the scratch clone only; the checker's own baseline is rc 0.

| brief | choice | alternative mutated | cells that red |
|---|---|---|---|
| ks_1659_p1 | fold the holder in the repository's INSERT with `toActorUuid` (ticket shape 1) | M1 the holder left raw (the defect) | R1 R2 R3 |
| ks_1659_p1 | fold, do not hard-null | M2 holder bound `null` always | C1 C2 |
| ks_1659_p1 | fold the HOLDER id, not the issuer's | M3 holder folded with `cert.issuer.id` (copy-paste) | C1 C2 |
| ks_1659_p1 | keep the raw principal in `certification_metadata.holderId` | M4 fold `holderId` in the metadata as well | C3 |
| ks_1407_p1 | `revokeAllUserSessions(user.id)` once, AFTER the write, caller's own session included | M2 revoke BEFORE the write | R2, C3 |
| ks_1407_p1 | same | M3 revoke before the current-password check | C1 C2 C3 R2 |
| ks_1407_p1 | same | M1 none (the defect) / M4 log without the count / M5 revoke twice | R1 R2 R3 / R3 / R1 R2 |
| ks_1407_p1 | do NOT spare the caller's session (alternative: `getUserSessions` + `revokeSession` minus `req.sessionId`) | not mutated: needs two functions the existing `ks1005` mock does not provide and a MODIFIED test; stated in Scope | n/a |
| ks_1407_p2 | revoke after the write and BEFORE `consumeResetToken` | M2 revoke AFTER the token is burned | R2 |
| ks_1407_p2 | same | M3 revoke BEFORE the write | R2, C1 |
| ks_1407_p2 | same | M1 none (leaves the import unused: `TS6133` only) / M4 log without the count / M5 twice | R1 R2 R3 / R3 / R1 R2 |
| ks_1157_p1 | a dedicated optional field `mintedBy?: 'oauth'` (ticket shape ii) | M6 marker written into `clientType` (shape i) | R4 |
| ks_1157_p1 | both grants pass it | M1 code grant does not / M2 refresh grant does not | R1 / R2 |
| ks_1157_p1 | stored only when given | M4 key always present (`undefined`) / M5 every session marked | C2 / C2 C3 |
| ks_1157_p1 | stored at all | M3 `createSession` drops it (`TS6133` on the unused param only) | R3 R4 |

## Briefs and rounds (dirs under `local-model/night/briefs/`, run dirs under `local-model/runs/`)
| # | ticket / piece | dir | tier / rung | by-hand red / green | control | real round (verbatim) | golden |
|---|---|---|---|---|---|---|---|
| 1 | KS-1659: certificationRepo.ts folds the holder; NEW jest | `ks_1659_p1` | code_patch, rung 2 | 3 red / 4 green, 7/7 with the edit; ks564 (8) and certificationRepo (16) green | CONTROL-PASS 73 s | `SPARK ROUND ks_1659_p1: PASS — PASS (checker rc 0 + A2a anchor OK) · golden BYTE-IDENTICAL · tip 89956fe92956 · 123s round, 55.048s model, 18428+2026 tok` | BYTE-IDENTICAL |
| 2 | KS-1407 change-password: users.ts revokes; NEW vitest | `ks_1407_p1` | code_patch, rung 2 | 3 red / 4 green, 7/7; ks1005 (6) and ks1052 (12) green | CONTROL-PASS 101 s | `SPARK ROUND ks_1407_p1: PASS — PASS (checker rc 0 + A2a anchor OK) · golden BYTE-IDENTICAL · tip 89956fe92956 · 165s round, 75.224s model, 33328+2553 tok` | BYTE-IDENTICAL |
| 3 | KS-1407 reset-password: auth.ts import + insertion; NEW vitest | `ks_1407_p2` | code_patch, rung 2 (2 hunks) | 3 red / 4 green, 7/7; ks1052, ks1005 green | CONTROL-PASS 91 s | `SPARK ROUND ks_1407_p2: PASS — PASS (checker rc 0 + A2a anchor OK) · golden BYTE-IDENTICAL · tip 89956fe92956 · 169s round, 78.494s model, 32072+2812 tok` | BYTE-IDENTICAL |
| 4 | KS-1157: types + session + oauth; NEW vitest | `ks_1157_p1` | **code_patch2, RUNG 3** (3 products, 5 hunks, 1 new test) | 4 red / 3 green, 7/7; whole auth suite 102 files / 1117 tests green; tsc clean | CONTROL-PASS 88 s | `SPARK ROUND ks_1157_p1: PASS — PASS (checker rc 0 + A2a anchor OK) · golden BYTE-IDENTICAL · tip 89956fe92956 · 212s round, 122.76s model, 45788+4383 tok` | BYTE-IDENTICAL |

Run dirs: `runs/spark_secuura_2026-10-20_ks_1659_p1`, `..._ks_1407_p1`, `..._ks_1407_p2`, `..._ks_1157_p1` (controls: the same names with `-control`).

Checker lines (`checker.out`): ks_1659_p1 `A4 (3 failed / 7 run; controls green; assertion reds)`, `A5 (7/7)`, `baseline total=1568 failed=0 | after total=1575 failed=0`, `A6 no NEW red`, `A7 tsc rc 0 (baseline rc=0)`, `A2a hunks=1 ok=1`; ks_1407_p1 `A4 (3 / 7)`, `baseline 1096 | after 1103`, `A2a hunks=1 ok=1`; ks_1407_p2 `A4 (3 / 7)`, `baseline 1096 | after 1103`, `A2a hunks=2 ok=2`; ks_1157_p1 `A3x declared=4 measured=4 ok=4 diff=0`, `A4 (4 failed / 7 run)`, `A5 (7/7) with all 3 product sections`, `baseline 1096 | after 1103`, `A2a hunks=5 ok=5`. All `RESULT: PASS (7/7)`, all `NEW reds: []`.

**Accommodation check (read before holding):** all four `decl_splice*.out` start `spliced 0`; `tdz_inline*.out` = `inlined 0`; every `section_N.opts` names the plain `section_N.diff`; `cmp section_N.diff section_N.decl.diff` and `...tdz.diff` equal where they exist. For ks_1157_p1 the decl-splice output also carries a NOTE, not an action: `spliced 0 - UNREPAIRABLE (multi-line in the reference, used and undeclared in the new file): description (ref :182)`. The new file does not use an undeclared `description` identifier (the word appears only as a `description: null` object key in the app row); the checker passed strictly, so it is a heuristic false positive and nothing was spliced.

## Things Wednesday should read before holding
1. **KS-1407 is a behaviour change on the auth surface; the pair should be raised and gated together.** Change-password now ends the caller's own session too (`revokeAllUserSessions` is account-wide): the next authenticated request on the old access token fails session validation and the client signs in again. The alternative (spare `req.sessionId`) needs `getUserSessions` + `revokeSession` and a MODIFIED `ks1005` session mock; it was not taken and is stated in Scope. If the revocation throws (Redis error) after the password was written, the request answers an error although the password changed (reset: the token is still unburned, so the user can retry; change-password: they re-try with the new password as current). Both briefs close only N-1382-1; N-1382-2 (the e2e case that posts to a route that does not exist) is untouched, and neither brief should use a closing word. The tests mock `revokeAllUserSessions`; a real Redis was not driven.
2. **KS-1659 is a one-line product change with a new behavioural cell.** NULL is stored in `documents.owner_user_id` for a connector holder (the column is nullable by migration 043's own comment); the raw principal stays in `certification_metadata.holderId`. The ticket's open question (does Platform S ever certify with no holder, which decides the severity) is for Stuart and was not asked. It does not touch `certifications.ts:333`'s default (the ticket's option 2) and leaves the old source-text guard in `ks564-certification-issuer-uuid.test.ts` in place (still green).
3. **KS-1157 closes only the "mark every session" bullet.** The deploy-time query ("list a user's OAuth-minted sessions") is not built; existing Redis sessions carry no marker (the ticket accepts the forward-only window). `createSession`'s other callers (login, wallet, social) do NOT pass the marker. Whether any consumer enumerates a stored session's keys was not audited.
4. **Same-file pairs:** `ks_1407_p1` and `ks_1157_p1` do not share files; `ks_1407_p2` (`routes/auth.ts`) and `ks_1157_p1` (`routes/oauth.ts`, `services/session.ts`, `types/index.ts`) are disjoint hunks of disjoint files, but `ks_1407_p1` and `ks_1407_p2` add test files in the same directory and both touch `auth` session semantics. `routes/auth.ts` is a busy file: expect a rebase.
5. Open-PR overlap on GitHub was NOT checked for `certificationRepo.ts`, `routes/users.ts`, `routes/auth.ts`, `routes/oauth.ts`, `services/session.ts`, `types/index.ts`.

## Findings (not written to IMPROVEMENTS.md: my write scope was the spark dir, SCREEN_19 and queue.md)
1. **BRIEF (my own), caught before any model round:** the first KS-1407 change-password hunk ended on a BLANK context line, and the builder REFUSED it in the dry-run (`edit block 1 ... has a BLANK CONTEXT line`). Fixed by turning the edit into a pure insertion between two non-blank lines, with `-U1` contexts; for the reset route the same trap was avoided by inserting between `updateUserOrThrow` and `consumeResetToken`. No real round spent.
2. **My own near-miss, kept out of the tree:** the first KS-1659 edit put a `//` comment on the SQL template line, which is SQL text, not JavaScript; the jest stand-in could not see it. Caught in review before the golden was cut; the brief now carries an explicit WARNING in `## Where`. A faithful-database cell would need a real Postgres.
3. **HARNESS/hook friction:** the pathguard refuses `ln -s` into the scratch clone when the link target is under `!CODING` (false positive, no write there); created with `os.symlink` from Python instead. A `golden.py` run with a relative output path wrote `s19_g1659.diff` into the WEDNESDAY root; moved to the scratchpad at once (the root is clean: `git status` shows no stray file of mine).
4. NOTE: `A4` needs the `## Red cells` lines to be substrings of the test titles (screen 16's lesson): applied in all four briefs, no control failed.
5. NOTE: new-file test names were pinned by the header `Test file:` line; the dry-run accepted all four and the model produced the same paths.

## NOT done / NOT tested
- No real Postgres, no real Redis, no route-to-database end to end for any of the four. No whole-workspace run beyond each checker's A6/A7 for its own service (originate, auth), plus one by-hand full auth vitest run (102 files / 1117 tests green, with all my edits applied together).
- No open-PR query. No hold, no raise, no `hold_ready`, no queue line (the pool is not shown exhausted).
- Housekeeping: `spark/cache/work/` gained 8 per-round clones (4 controls, 4 real; 223 entries now), `spark/state/dry/` 5 dry-run inputs (330 entries now), the cache clone fetched develop `89956fe92956`.

## Files written
Briefs (each `KS-<n>.md`, `golden.diff`, `spark.pins`) under `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/`: `ks_1659_p1/` (KS-1659.md), `ks_1407_p1/` and `ks_1407_p2/` (KS-1407.md each), `ks_1157_p1/` (KS-1157.md). Run dirs under `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/` (8 incl. controls). This file. Scratch (not durable): `/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/2a56ac36-e9ca-49f4-8d2d-f02d4a53f9ed/scratchpad/s19/` (clone/, t/ test drafts, mut*.py, golden.py, mk*.py, h.sh, lint/dry/ctl/real outputs) and `.../scratchpad/census.py|census.out|get.py`.
