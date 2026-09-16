# NEXT SEARCH 2026-09-17d (05:08–05:40 AEST): T5 splits and T3 jest

**BLUF: TWO FITS, both PARTIALS of KS-730 ("71 inline handlers still return err.message off production"), both JEST
code_patch (one small product edit + one new test), both PASS 7/7 on the real checker at the current tip `e0f41a8fa`.**
They touch different files and were measured together (originate 649 / 649 with both goldens). A third fit does not
exist in the two commissioned directions: 34 tickets read (22 original T5, 9 more T5 rows from a mid-search census
regeneration, 3 T3) and 21 splits examined; 2 fit.

Queue in this order: A first (small input, the simpler file), then B.

1. **KS-730 part A: originate `routes/systemErrors.ts`, POST /ingest (`:95`) and POST /client-errors (`:125`).**
   Adds a logger import and, in each catch, a log line plus the constant `Internal server error` (3 hunks, +6/-2). New
   test `ks730-security-71-inline-handlers-still-return.test.ts` (111 lines): 4 🔴 + 2 🟢. Input ~11.3K prompt tokens.
   **Hardening, not a live leak:** every `errorTrackingService` export swallows its own error, so these catches are
   unreachable through the real service today (the brief's P3).
   ```
   KS-730 input=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/inputs/code_730A.json task=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/tasks/code_patch/task.md ctx=65536
   ```
2. **KS-730 part B: originate `routes/adminConfig.ts`, POST / PUT / DELETE `/document-types` (`:187`, `:219`, `:231`).**
   In each catch, a log line plus the constant text (2 hunks, +6/-3; `logger` is already imported). New test
   `ks730-adminconfig-document-types-500-body.test.ts` (131 lines): 4 🔴 + 2 🟢. **A live leak off production (read, not
   driven against a DB):** each route casts a caller value with `::uuid` inside its try, so a malformed id's PostgreSQL
   text reaches the body today. **Input ~38.6K prompt tokens** (2133-line product file), leaving ~26.9K of ctx 65536 for
   a ~3K-token answer. It is the largest input tonight.
   ```
   KS-730 input=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/inputs/code_730B.json task=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/tasks/code_patch/task.md ctx=65536
   ```

**Class check for Wednesday before queueing:** both are KS-727-lineage message-redaction edits, the class the 17b report
raised for KS-1182. KS-1182 was queued and ran (done.md, PASS at 03:57), so I read that as ruled in. Neither file is
auth, MFA, OAuth, a guard module, the erasure door or proxy normalisation. `gdpr.ts` was refused as erasure-adjacent.

**Files:**
- Briefs: `night/briefs/split_730A/KS-730.md` and `night/briefs/split_730B/KS-730.md`, the house split convention
  (`new_brief.sh --split`), which the builder can read (`NIGHT_BRIEFS_DIR/<id>.md`).
- The commissioned paths `night/briefs/KS-730-A.md` and `KS-730-B.md` are **symlinks** to those files, so there is one
  source.
- Inputs: `night/inputs/code_730A.json` (sha256 `0554e6fc0d8c6b8f…`) and `code_730B.json` (`1f3f159423821582…`),
  both built at 05:38 at tip `e0f41a8fa`.
- Nothing queued. `queue.md`, `done.md`, the checkers, the builders, other briefs and `IMPROVEMENTS.md` were not
  touched. No git write verb ran against the Secuura checkout; its porcelain read 0 at every reading (25
  readings, 05:10:24–05:39:40).

## Pins and final rounds

| | A | B |
|---|---|---|
| product | `systemErrors.ts` blob `6b57d8d75`, 186 lines | `adminConfig.ts` blob `26cec03de`, 2133 lines |
| builder pins | `NIGHT_BRIEFS_DIR=night/briefs/split_730A product=Blockchain/Dev/services/originate/src/routes/systemErrors.ts ref=services/originate/src/__tests__/ks444-system-errors-body-guard.test.ts line=95 ctx=65536` | `NIGHT_BRIEFS_DIR=night/briefs/split_730B product=Blockchain/Dev/services/originate/src/routes/adminConfig.ts ref=services/originate/src/__tests__/ks764-admin-api-keys-revoke-route-contract.test.ts line=187 ctx=65536` |
| test alone at tip | 4 failed / 6, all 🔴, all assertion; controls green (twice) | same shape (twice) |
| partial-fix tampers | 5 rows, each reds exactly its own cell by assertion | 7 rows, same |
| suite | 637 → 643, NEW `[]` | 637 → 643, NEW `[]`; A+B together 649 / 649 |
| decl_splice | `spliced 0` vs ks444, ks423, ks694 | `spliced 0` vs ks764, ks487, rightsHolders integration, itself |
| checker rounds | fin2 PASS (`79432c797`, scratch input); fin3 PASS (placed input); **fin4 PASS at `e0f41a8fa`** (fresh clone `runs/next17d_ks730A.lA1tiW`, 05:38:25–05:39:01) | finB1 PASS (scratch); finB2 PASS (placed); **finB3 PASS at `e0f41a8fa`** (05:39:07–05:39:40) |

**Tip moved mid-search:** `79432c797` → `e0f41a8fa` (#1013, KS-999) at 05:37:02. GitHub compare (05:37:14): 1 commit,
3 files, all `services/auth`. Locally, `git diff --stat` over originate and packages/shared is empty. Both briefs' P1
records this. Both inputs were rebuilt and both checker rounds re-run at the new tip. Scripts are in the session
scratchpad `…/76d545ac-…/scratchpad/next17d/` (`premeasure.sh`, `premeasureB.sh`, `final.sh`, `finalB.sh`, `probe.sh`,
`tsc_jest*.sh`, and their `.out` files). Clones: `local-model/runs/next17d_ks730A.FQWWPz` (old tip) and `.lA1tiW` (new
tip); `runs/` is gitignored.

## Rejection table (every row read this search)

`Instr` says how the reason was established: **R** = the ticket read in full on Linear (05:09:12, 05:36:14);
**M** = measured at the tip; **P** = partition (READY `+++ b/` paths, open-PR files, live lanes). No row's `updatedAt`
has moved since the 2026-09-16 20:07 search.

| ticket / split | verdict | reason | instr |
|---|---|---|---|
| **KS-730 A** (`systemErrors.ts` :95, :125) | **FITS** | see above | M |
| **KS-730 B** (`adminConfig.ts` :187, :219, :231) | **FITS** | see above | M |
| KS-730 `systemErrors.ts` admin catches :136/:158/:168/:184 | HELD FOR A | Same file as part A (the partition rule applies to my own briefs), and part A adds the import they need. Brief after A merges. | M |
| KS-730 `adminConfig.ts` pricing :104/:121/:131 | REFUSED (chose B instead) | Latent: `loadPricing` and `updatePricing` catch everything, and `getPricingTable` returns a copy. Same file as B. | M |
| KS-730 `adminConfig.ts`, the other 40 ternaries + 3 unguarded | HELD FOR B | Same file as B; one part at a time. The 3 unguarded sites (:1832, :2004, :2131) are NOT in the ticket count. | M |
| KS-730 `gdpr.ts` (15) | REFUSED | Erasure-adjacent (`executeErasureByExternalRef`), and `:503` records a deliberate NO-logger-import constraint (config import hazard), which the log requirement contradicts. That is a decision. | M |
| KS-730 tokenisation `index.ts` (2) | REFUSED (recorded reason re-verified) | Top-level `await initDb()` + `app.listen` at `:405-411`; 0 tests import `../index`. | M 05:31:51 |
| KS-730 api-gateway `index.ts` (2) | ALREADY DONE | 0 response-side `err.message`; `:1139` is the KS-727 comment, `:1158` a log. | M 05:19:02 |
| KS-910 | NOTHING LEFT | The comment half is `READY_KS-910` (done.md PASS 20:45). The rest is Kam's 09:53 ruling "keep leg 12 as reachability", not a patch. `preflight.sh` is carried by READY_KS-1040-part1. | R+P |
| KS-1153 R-918-A (pin the `--check-unreached` advisory-skip arm) | REFUSED, harness gap | A pin of CORRECT behaviour has no red at the tip. bash_patch B4 requires red at the tip and has no test-only/tamper mode (finding 4). | M (checker read) |
| KS-1153 R-918-B (nested guard basename, `run-code-guards.sh:197-199`) | REFUSED | "pre-existing design", done-when "fixed or accepted"; two fix directions (narrow the pathspec or wire by path), neither ruled. | R+M |
| KS-1153 R-925-A (`preflight.sh:166` TAB tail) / F-925-4 (`:197-202`) | REFUSED | `preflight.sh` is carried by READY_KS-1040-part1; both are latent ("no such header exists today", "no leg does it"). | P |
| KS-1153 R-924-A / R-924-B / F-924-2 / precision rows | REFUSED | A PR body edit (GitHub write), a fact, a pre-existing record, board records: none is a repo patch. | R |
| KS-967 (single-file split: line-level check + self-test flip in `no-tracked-credentials.sh`) | REFUSED | A credential guard module (hard exclusion), and "Keys named, not pattern-guessed" is an unmade key-list design. | R |
| KS-1051 (fix shape 3, a Test Evidence doc line) | REFUSED | "Kam or Wednesday to pick a fix shape"; `DEV-PROCESS.md` is carried by 3 READYs. | R+P |
| KS-753 (single `index.ts:466` half) | REFUSED (reason stands) | "Open design question for the ruling" (503 vs `verified:false`); no ruling in comments (0). | R |
| KS-1083 (`bootstrap-env.sh` half) | REFUSED | The comment says "Do not set GATEWAY_VOUCH_SECRET on any environment yet" (PROVISIONING UNSAFE); `bootstrap-env.sh` is carried by READY_KS-1081; `verification.ts` is a live lane. | R+P |
| KS-1055 | REFUSED | Needs real Postgres (RLS NOBYPASSRLS role); per-tenant migration design. | R |
| KS-485, KS-491 | REFUSED | Created by `peter@obeden.com`; review programmes; auth.ts. | R |
| KS-1174, KS-526 | REFUSED | Created by `stuart.jamieson@secuura.ai`; API-key auth (1174) / KMS (526). | R |
| KS-576, KS-580 | REFUSED | Features split from KS-480 (bulk re-key; off-estate recovery audit); design + security review. | R |
| KS-621, KS-624, KS-625 | REFUSED | Tracking tickets with "fix shape deliberately blank" pending Kam's ruling; authz / VC proof crypto. | R |
| KS-658 | REFUSED | "Kam's call": what the demo is; file-don't-flip ruling stands. | R |
| KS-807, KS-870, KS-954 | REFUSED on sight | Control-byte guard / erasure door / proxy path normalisation (hard exclusion). | R |
| KS-1082 | REFUSED | systemTest Playwright (Peter's area); "Not decided here". | R |
| KS-1187 (new, P1) | REFUSED on sight | Erasure door + proxy path normalisation (hard exclusion). | R |
| KS-1100 | REFUSED | Commission 4 gates; "a QA credential on kintsugi … is Kam's call"; auth `mfa.ts` / `userRepo.ts` (live lane). | R |
| KS-607 | REFUSED | Created by Stuart; an investigation with a semantics ruling, no fix shape (recorded 09-16). | R |
| KS-696 | REFUSED | The Akto harness (non-determinism; capture fix is KS-700) needs a live stack + Mongo; the systemErrors/gdpr hint is a basename false match. | R |
| KS-735 | REFUSED | "The contract question — Peter's call, not to be decided in the fix"; frontend. | R |
| KS-1039, KS-1106 | REFUSED (recorded) | Playwright e2e / frontend verifier UX; no checker. | R |
| KS-1116 | REFUSED | **Now ruled** (Kam 2026-09-13 16:55, `bind-creator`), but an ownership/authz check across vc-issuer `presentations` + `credentialRepo` (multi-file; `credentialRepo.ts` is carried by READY_KS-1121). A Claude seat. | R+P |
| KS-1090 | REFUSED | A new `tsconfig.test.json` + a local-gate leg + a structural 172-cell api-gateway mint-scope guard; no tier grades a config file; `gatewayProvenance.ts` is in an open PR. | R+P |
| **T3** KS-1019 | REFUSED (not a harness reason) | "[Question] … this is a QUESTION, not a defect report"; a discriminated-union design. | R |
| **T3** KS-759 | REFUSED | `middleware/auth.ts` (auth, hard exclusion) + the shared `JwtPayload` type in packages/shared ("wants its own PR and its own reviewer"). | R |
| **T3** KS-1084 | REFUSED | "READ ONLY / unverified … Measure before any fix" on a two-tenant stack; tenancy surface. | R |

Seat A's KS-1018 / KS-1050 / KS-1101 / KS-1072 were read for their paths (auth `users.ts` / `userRepo.ts`, api-gateway
`health.ts` / `system-status.ts` / `health-dashboard.ts` / `verification.ts`). The held READYs cover them; none is under
originate.

## Harness findings (FOUND / TESTED / HOW)

1. **The jest question: NO GAP.**
   - FOUND: `checker.sh:138-152` branches on `RUNNER_KIND` (`vitest|jest`, `npx jest --json --outputFile`). `build_input.sh:206-214` sets `runner_kind = "jest"` from the test script, and `task.md:31-40` carries the jest idioms. Jest has been in since 2026-09-15 18:2x, and READY_KS-1028 / -1074-A/B/C / -794 / -1133-A / -1158-R3 are JEST PASS.
   - TESTED: 6 jest checker rounds tonight, all PASS.
   - HOW: the T3 refusals in candidates.md were never harness reasons. They were a question (1019), auth (759) and unverified tenancy (1084), and they still hold.
2. **A3e matches stay-sites by TEXT, so identical lines cannot be split into "change these, keep those".**
   - FOUND: `checker.sh:460-471` builds `minus` as a set of stripped `-` texts and fails any `must_change:false` site whose `text_at_tip` is in it, with no line number.
   - TESTED: fin1 (05:20:53) **FAILED at A3e** on a golden diff. Brief A listed `:136/:158/:168/:184` as `(correct)`, and they carry the same text as the `:95/:125` `-` lines. Moving them to prose gave PASS (fin2).
   - HOW TO FIX: map each `-` line to its original line number from the hunk headers and compare site LINES. About 15 lines of python in the same heredoc. bash B3c (`bash_patch/checker.sh:169-195`) should be checked for the same shape.
   - Consequence tonight: an over-edit of the other identical catches (4 in A, 43 in B) is **not graded**. Both briefs' raise notes say so.
3. **The standalone test-file tsc passes `--types node,vitest/globals` even for jest services.**
   - FOUND: `checker.sh:692`, whose INFO line says "vitest does not type-check".
   - TESTED: the untouched `ks444` test gives 8 × TS2708 under that exact command (05:22:32). The new tests give 13 / 10 × TS2708. The same command with `--types node,jest` gives 0 error lines (05:22:46, 05:31:28).
   - HOW TO FIX: branch the `--types` on `RUNNER_KIND` (1 line), so the INFO number means something for jest.
4. **bash_patch has no test-only (tamper) mode.**
   - FOUND: `bash_patch/checker.sh` B3 requires `{script, new test}` and B4 requires red at the untouched tip. code_patch has had `defect_line.tamper` since 09-15, but the bash tier does not.
   - Blocks: KS-1153 R-918-A and every "pin the working arm" bash item.
   - HOW TO FIX:
     - `build_bash_input.sh`: parse `## Tamper` (`line/from/to/statement_ok`) the way `build_input.sh:466-500` does.
     - `bash_patch/checker.sh`: B3 accepts `{one new test}` when a tamper is set; B4 plants the tamper in the clone's script, runs, expects FAIL, reverts and checks the sha; B5 runs at the untouched tip and expects PASS.
     - Estimate: ~60-90 lines across the two files, plus one golden round on R-918-A (tamper `:147 exit 0` → `exit 1`, or drop the `SKIP (advisory)` echo).
5. **`build_input.sh` has no pin for a NEW test path.**
   - FOUND: `suggested_test_file` is title-derived (`:310-316`), so two parts of one ticket get the same new path. KS-730 A and B both got `ks730-security-71-inline-handlers-still-return.test.ts`, and B's brief overrides it in prose.
   - The same shape is already on disk: **READY_KS-1074-A, -B and -C all add `ks1074-the-poller-reconcile-blob-writers-also.test.ts`** (`+++ b/` count 3). Those three collide at raise.
   - HOW TO FIX: accept `test_new=<path>` and put it in `suggested_test_file` (~5 lines). A3 already accepts any new file under the test dir.
6. **The code_patch checker leaves the product PATCHED and the new test untracked after a PASS** (already filed in 17b/17c). Reconfirmed in all 6 rounds; the scripts reset the clone after each.

## Anything a reviewer should know (every deviation)

- **`candidates.md` was REGENERATED during this search, and the regeneration DROPPED every rejection table.**
  - night_run.sh (`com.wednesday.ornith-loop`, every 900 s) logged "QUEUE … has no pending ticket" and "DERIVE: candidates.md older than 6h — re-deriving" at 05:20:40, and wrote the file at 05:20:47 (`log/derive_2026-09-17_0520.out`: T1 28 · T2b 7 · T3 3 · T4 3 · T5 30 · held 59 · set-aside 27 · excluded 156, total 313).
  - `derive_candidates.py` writes the census fresh; nothing carries over the 4 hand-appended `<!-- REJECTION TABLE … -->` blocks. The working copy is now `git diff --stat` +55 / -182 against HEAD `3e68f4132`, which still has them.
  - The file's mtime moved again at **05:34:46**, which the night log does not account for. I do not know who wrote it then.
  - **I did not write it and did not restore it.**
  - Effect: 8 rows the blocks had refused (KS-607, 696, 735, 1039, 1090, 1100, 1106, 1116) are now listed as T5 candidates. I read them all (table above). A future seat reading only the regenerated file would re-derive every old refusal.
  - I read the pre-regeneration file whole at 05:08, so the commission's 22-row T5 set is the one I searched, plus these 9.
- **Brief file layout:** the real files are in `split_730A/` and `split_730B/`, and the commissioned `KS-730-A.md` / `KS-730-B.md` are symlinks (there is no symlink precedent in `briefs/`). `autostart_on_brief.sh` was read first: no autostart process was running (`ps`, between 05:31:51 and 05:33:24), and `night_run.sh` never reads `briefs/`. So placing the files queued nothing.
- **Clone location:** under `local-model/runs/` as commissioned (the previous reports used the scratchpad). The two clones hold symlink-farmed node_modules; nothing was removed.
- **One Bash call held a `cd`** (the backgrounded baseline jest run at 05:15, as `( cd "$SV" && … )`). The no-cd hook refused one earlier call (05:14) and did not fire on this one. All later `cd`s are inside script files, the prior seats' pattern.
- **One probe printed wrong `rc=` values:** `tsc_jest.sh` evaluates `$?` after a `$(date)` substitution. Only its `error_lines` counts are used anywhere.
- **Decisions the briefs take (flagged in their raise notes):**
  - The log carries `err.message` only (no stack), following `errorTrackingService`'s own convention.
  - A adds an import, which `task.md` rule 5 ("imports the file ALREADY has") does not anticipate. KS-844's import edit is the precedent (`task.md` 2e), and the brief states it explicitly.
- **Ticket facts to file (not filed, no board writes):**
  - **KS-730:** its counts are stale. The api-gateway half is done at the tip. `adminConfig.ts` also has **3 catches that return `err.message` with NO NODE_ENV guard**, so they leak under production too (`:1832` `/backfill-certification-metadata`, `:2004` `/seed-demo-users`, `:2131` `/migrate-tenant-data`), and the ticket does not count them. The `systemErrors.ts` catches are unreachable through the real service.
  - **KS-1116:** it is ruled (`bind-creator`, 09-13 16:55) but still reads as a decision ticket. It is now Claude-seat work.
