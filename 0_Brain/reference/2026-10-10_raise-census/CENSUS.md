# RAISE CENSUS — the 8 held READYs against develop `613070f29112` (2026-10-10 ~04:1x AEDT = 2026-10-09T17:0xZ)

Drafted by a Sonnet sub-agent for Wednesday. Nothing here was sent, launched, written to Linear or to GitHub. Every claim names its instrument; anything not measured says UNMEASURED.
Scratch (instruments, outputs): `/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/ce91ac93-c45e-4849-a76b-deff4ef72ffc/scratchpad/raisecensus/` (`census.sh`, `census.out`, `trees.sh`, `seq.sh`, `stack.sh`, `heads.txt`, `pulls.txt`).

## 0. Base
- develop = `613070f29112a40a0d8d9684cd50c7c2ae54592c` — `git ls-remote git@github.com:Secuura/Distributed_Secuura.git refs/heads/develop` rc 0, with the project's `core.sshCommand`; the commit object is present in the scratch clone (`cat-file -t` = commit). 772 heads, 1,361 `refs/pull/*/head` lines, highest pull **1440**.
- Open/merged since the READYs' tips (`ae9bf6828f88`, 3 behind develop; `81d2e5f4c415` 16 behind; `0a6177ea5482` 18 behind; `69f2045af2a4` 57 behind): `rev-list --count tip..develop`.
- Pulls above 1437, by fetching their head SHAs by SHA into the scratch clone: #1438 and #1439 are ANCESTORS of develop (`merge-base` = the head itself, ahead 0) = already merged; **#1440** (KS-1448, `feature/notification-bola-marker-cites-live-owner`) is 1 commit ahead of its merge-base and touches 2 files, both under `systemTest/schemathesis/tests/` (`git diff --stat`): 0 overlap with any file below. Its OPEN/MERGED state is UNMEASURED (no GitHub API); "ahead 1 of develop" is all `rev-list` can say.
- Instrument for every apply check: a TEMP INDEX (`GIT_INDEX_FILE` + `read-tree 613070f2…` + `git apply --cached --check`, never a worktree) in the scratch clone, each `section_<k>.diff` of the canonical `out.md.checker/`, strict first, then `--recount --ignore-whitespace`, then `-R`.

## 1. The census table (per READY)

| # | READY (night/) | canonical run | forward strict | forward lenient | reverse `-R` | verdict at 613070f2 |
|---|---|---|---|---|---|---|
| 1 | KS-998 FORMATGATESTDIN-1 (bash, 2 files) | `spark_secuura_2026-10-09_KS-998-format-gate-npm-stdin` | rc 0 both sections | rc 0 | rc 1 (new file absent; hunk absent) | **RAISE** |
| 2 | KS-937 (bash, 2 files) | `2026-10-08_ks937-omlx-ornith-1.5-35b-a3b-mlx-8bit-night` | rc 0 both | rc 0 | rc 1 | **RAISE** |
| 3 | KS-1346 APIGWFAIL500TYPES-1 (rung 3, 4 files) | `spark_secuura_2026-10-10_KS-1346-apigw-fail500-type-and-field-names` | rc 0 all 4 | rc 0 | rc 1 | **RAISE** |
| 4 | KS-1410 AUDITEXPORT502-1 (rung 4 LOOSE, 2 files) | `spark_secuura_2026-10-10_KS-1410-apigw-audit-export-502-loose` | section 1 **rc 128 `corrupt patch at line 15`**; section 2 rc 0 | section 1 rc 0 (`--recount --ignore-whitespace`) | -R rc 128; -R recount rc 1 | **RAISE**, lenient apply for section 1 only |
| 5 | KS-1410 TRANSFERPROCEXPIRED-1 (rung 1, 2 files) | `spark_secuura_2026-10-10_KS-1410-transfer-process-expired-500` | rc 0 both | rc 0 | rc 1 | **RAISE** |
| 6 | KS-1432 KS-1432-1 (held 2026-10-07, 2 files) | `spark_secuura_2026-10-07_KS-1432-apigw-ks529-guard-real-predicate` | rc 0 both (tip was 57 behind) | rc 0 | rc 1 | **RAISE if the hold is lifted** (Q-1432HOLD) |
| 7 | KS-1345 LIST-1 (2026-10-05) | `spark_secuura_2026-10-05_KS-1345-list` | **rc 1** `patch failed: …/originate/src/routes/webhooks.ts:187` and the test `:4` | rc 1 | **rc 0 both sections** | **ALREADY ON DEVELOP — DROP** |
| 8 | KS-1345 WEBHOOKS-DELIVERIES-1 (2026-10-10, LOOSE rung 6, 2 files) | `spark_secuura_2026-10-10_KS-1345-originate-deliveries-failed-query-500` | section 1 **rc 128 `corrupt patch at line 27`**; section 2 rc 0 | section 1 rc 0 | -R rc 128 / recount rc 1 | **RAISE**, lenient for section 1 |

**DROP evidence for #7** (two independent instruments): (a) `apply -R --check` rc 0 for both sections = the reverse applies = the change is present; (b) `git log` on develop: `f01c1da5717f` "KS-1345: a failed webhooks list query answers 500, not 200 with an empty list" (2026-10-05, ancestor of develop by `merge-base --is-ancestor` rc 0), whose body says "Test evidence is in PR #1381" and names the merge ("Merged by Seat B 61st on Wednesday's signed GO … merge 1381 on gate57"). The flow block `13.` / cheat section "Webhooks list failure — KS-1345" already exist in both docs (Python read of the blobs). Branch `feature/ks-1345-webhooks-list-500-b60-2` still exists at origin (`82e6bfa9de85`, NOT an ancestor: squash-merged). The READY's own tip `2d85b84e` is older than that merge. **Do not re-raise; move the READY to a dated quarantine folder, recorded (never delete) — Wednesday's act.**

Patch identity: `wc -c` + `shasum -a 256` of each `patch.diff` equals its READY header (KS-998 5,136 B `8c2bd29b5ae4010a`; KS-937 4,914 B `49f69f7d29a4f628`). The rest (drafter's measure, not in the READY headers): KS-1346 8,497 B `e21ce6406079b6cc`; KS-1410 audit-export 6,920 B `7b7fea05b2511d2e`; KS-1410 transfer 6,181 B `a9b70cd45a25fd92`; KS-1432 2,412 B `b94af8557c45087d`; KS-1345 deliveries 6,425 B `1a70f75e281f8d76`. NOTE the two lenient patches' whole `patch.diff` does NOT strict-apply (the READY says so); apply PER SECTION.

Resulting tree at develop per payload (`write-tree` of the temp index, base tree `cf10edb0b9f8`): KS-998 `6ea89a172011` · KS-937 `e19cb788c6a7` · KS-1346 `c30b64d30fa7` · KS-1410-ae `ceca1f2e401a` · KS-1410-tr `007affad1d70` · KS-1432 `3cd4cc0ab2ea` · KS-1345-del `78202c558cc6`.

## 2. (2) Existing branch / PR for the same ticket+change
Instrument: `ls-remote --heads` (772 lines, saved) grepped `ks-?(998|937|1346|1410|1432|1345|1402)`; PR STATE (open/merged) is **UNMEASURED** — `gh` / the GitHub API is not available to this drafter.
- KS-998: `feature/ks-998-format-gate-push-label-literal-ra9-3` (`3be1a5317735`) = the EARLIER change (develop has `7bcc2ed54` "the format gate reads its in-this-push label literally"); not this one. No branch for the stdin change.
- KS-937: **no** branch. (Earlier KS-937-family commits on develop are 2026-09; not this change: reverse check rc 1.)
- KS-1346: six branches, all other routes: `…adminconfig…-b36-1`, `…gdpr…-b32-6`/`-b35-3`, `…systemerrors…-b32-5`/`-b35-2`, `…webhooks…-b36-2`; develop has KS-1346 A, B, C, D (`1d6e903be`, `2be9f7e4d`, `acb045d6a`, `5c847ab3a`). **No api-gateway KS-1346 branch.**
- KS-1410: `feature/ks-1410-apigw-500-never-answers-err-message-ra19-1` (`5ed875dcb60a`) = R 19th's PR, landed as develop `eb19d99d3` "10 of 28 sites" (notifications/batch/audit-export `fail500`s). This audit-export 502 site and `transfer/delegations.ts` are the NOT-yet-done remainder (the reverse checks prove it).
- KS-1432: no branch (PR-vs-ticket trap: `#1432` in the seat files is a PR NUMBER, merged 2026-10-09; the ticket KS-1432 has 0 commits on develop by `git log --grep "KS-1432\b"`).
- KS-1345: only the already-merged list branch (#7 above); none for deliveries.

## 3. (3) Files, tests, docs, MUSTs

| READY | product file(s) | test file(s) | lines (`numstat.out`) |
|---|---|---|---|
| KS-998 | `systemTest/scripts/check-package-format.sh` (100644, 216 lines on develop) | NEW `systemTest/__tests__/ks998_format_gate_stdin_isolated.test.sh` (+93; siblings there are 100755 — the seat reads the committed mode) | +4/-1 (hold_ready count) / +93 |
| KS-937 | `Blockchain/Dev/scripts/check-shared-relink.sh` (100755) | EDIT `Blockchain/Dev/scripts/__tests__/check_shared_relink.test.sh` (100755) | +6/-2 / +66/-1 |
| KS-1346 | `Blockchain/Dev/services/api-gateway/src/routes/{notifications,batch,audit-export}.ts` (1/1 each) | NEW `…/api-gateway/src/__tests__/ks1346-apigw-fail500-logs-type-and-field-names.test.ts` | 3×(+1/-1) / +132 |
| KS-1410-ae | `…/api-gateway/src/routes/audit-export.ts` (+2/-1) | NEW `…/api-gateway/src/__tests__/ks1410-audit-export-502-never-answers-err-message.test.ts` | +132 |
| KS-1410-tr | `Blockchain/Dev/services/transfer/src/routes/delegations.ts` (+4/-2) | NEW `…/transfer/src/__tests__/ks1410-delegations-process-expired-500.test.ts` | +116 |
| KS-1432 | `…/api-gateway/src/routes/verification.ts` (+11/-2) | EDIT `…/api-gateway/src/__tests__/ks529-non-object-body-guard.test.ts` (+20/-4) | |
| KS-1345-del | `Blockchain/Dev/services/originate/src/routes/webhooks.ts` (+6/-1) | EDIT `…/originate/src/__tests__/ks1341c-webhooks-500-never-answers-err-message.test.ts` (+40/-6) | |

**Docs: EVERY raise edits BOTH platform-k HTML docs** — `Projects Documents/API_Security_Functional_Testing_Architecture_Flow_Diagrams.html` (blob `a23ec16bb0a0`, 311,353 B at develop) and `Projects Documents/QA_Tool_Cheat_Sheet_Secuura_API_Testing.html` (blob `8af4daa33385`, 293,022 B). Authority: `secuura-test-discipline` SKILL §4 "Every test change updates its platform's two HTML docs, in the same commit… Both files, every time… Never cross platforms." "Test change" there includes backend unit and systemTest tests, so it covers the shell suites (KS-998, KS-937) as well. Doc tails at develop (Python read of `git show` blobs; positive controls: flow number `44` and cheat key `KS-1402` found): flow 40 numbered `<h2>`, 0 dups, max 44, numbers `32 33 34` ABSENT, `45`+ absent; cheat 29 `<h2>`, 0 dups, tail `… KS-1139, KS-1449, KS-1171, KS-808, KS-1355, KS-1328, KS-1402`. **Existing blocks for tickets re-raised here:** KS-998 (flow 29 / cheat), KS-1345 (flow 13 / cheat), KS-1410 (flow 36 / cheat) — a second block under the same cheat key is a duplicate by the project's key-uniqueness rule (R 19th brief `Q-N5`): Q-KEYDUP. KS-937, KS-1346, KS-1432: no block yet (0 mentions).

**MUSTs a raise touches (named):**
- SKILL §1 Plan before you touch; **review authority**: platform-k base code = Kamil, **`systemTest/` = Peter** (KS-998 is under `systemTest/`: Peter's call decides its test design; "seek their input before settling a test's expectations" — via Wednesday's batch, never this seat).
- SKILL §4 two HTML docs in the SAME commit + the timings MUST (a changed tier timing must appear in both docs, a measurement with date and host; for these changes no timing is expected to move — UNMEASURED, the seat says so with its instrument). `html_docs_matrix.test.sh` 12/0 is NOT evidence a block is well-formed (STANDING_LINES `:442`).
- SKILL §5b every fix proven by a test RED on the broken code and GREEN after (+ `systemTest/CLAUDE.md:838` "A fix is proven only by a red→green transition (MUST — ALL tests)").
- SKILL §5c no god files (400, excl. blanks/comments) — **scope systemTest only**: applies to KS-998; 937 and the services are out of its scope.
- **SKILL §5d "Every changed line carries a comment saying WHY it changed and the Linear ticket number"**: measured gap on the canonical diffs — KS-1346 (3 changed lines), KS-1410-ae (2), KS-1410-tr (3) carry NO ticket comment on the changed lines (read from the `section_*.diff` text); KS-998, KS-937, KS-1345-del carry them; KS-1432 carries it on the new function, not on the one changed call-site line. Precedent for the fix: R 19th's `Q-5D1139 (a)` (payload byte-for-byte, then ONE WHY line in the SAME commit).
- SKILL §5e CLAUDE.md diff audit (no branches/merges/MD files/tickets unless instructed; Zod/UTC rules — none apply to these diffs: UNMEASURED beyond a read of the hunks).
- SKILL §5f a runtime-behaviour change is not done on offline green: "live run owed", the ticket does not move to Done (api-gateway 500/502 bodies, transfer 500 body, originate deliveries 500: all runtime; KS-998/937 are push-path scripts: the hook itself is the runtime — UNMEASURED live).
- `systemTest/CLAUDE.md`: MUST 1-8 (branch first, unit tests, docs, CLAUDE.md, clean design, no god files, ALL docs) for KS-998; `:663` "The gate must be TRUTHFUL" (KS-998 changes a gate); `:909` no links to other organisations' issues/PRs in git metadata (every lane).
- Repo `CLAUDE.md` lines carried from R 19th's brief (`:255-256` ticket URL in PR, `:285` Test Evidence, `:296` never push to develop, `:167-175` no foreign links, `:209-226` slot MUSTs): NOT re-read by this drafter.

## 4. (4) File-family collisions (measured)
- **`api-gateway/src/routes/audit-export.ts`: KS-1346 (`fail500` line, `@@ -22,6` ≈ :25) and KS-1410-ae (catch block `@@ -170`, :170-175).** Hunks are 145 lines apart: both orders apply (rc 0 each, `seq.sh`), and **both orders give the IDENTICAL tree `c3ae1044cdb0`** (`write-tree`); re-applying KS-1346's section 3 on the stack is REFUSED (rc 1, `patch failed: …/audit-export.ts:22`) = the control that the stack is not vacuous.
- **The content collision is not textual — it is the RULING:** KS-1410-ae's new line `logger.error('Audit export could not reach the security service (GET /api/admin/audit/export)', { error: err instanceof Error ? err.message : String(err) })` uses the PRE-ruling `String(err)`; KS-1346's `+` line is the ruled expression (Kam 2026-09-27 16:31/16:32, card `secuura-ks1346-logging-thrown-objects-leaks-secrets` => a, "type + field NAMES only"; the line is `cmp`-identical to `originate/src/routes/adminConfig.ts:104`, which is at develop line 104 by `git grep`). Wednesday's 00:19 raise note (daily 2026-10-10 line 30): "the second to land takes the KS-1346 ruled expression". Drafted as Q-RULEDEXPR.
- **`originate/src/routes/webhooks.ts`:** KS-1345 LIST-1 (:187) and DELIVERIES (:404) are 217 lines apart, but LIST-1 is already on develop (DROP), so the pair is moot; DELIVERIES alone touches webhooks.ts.
- KS-1346 vs KS-1432 (both api-gateway): different files (`routes/{notifications,batch,audit-export}.ts` vs `routes/verification.ts`), different tests: 0 shared paths. KS-1410-tr (`transfer/`) shares nothing with the others.
- **All seven stacked at develop** (one temp index, each section with its recorded options): every section applies, **15 changed paths, 0 path touched twice except `audit-export.ts`** (the pair above) → code-level the seven are disjoint. Stack tree `f0d7afd79f13`.
- Shared by ALL seven: the two HTML docs (§5).

## 5. PARTITION by directory, and the shared-docs question

Directory map (measured from the `+++` headers):
`api-gateway/src/routes` (KS-1346 ×3 files, KS-1410-ae, KS-1432) · `transfer/src` (KS-1410-tr) · `originate/src` (KS-1345-del) · `systemTest/` repo-root (KS-998) · `Blockchain/Dev/scripts` (KS-937).

- **Maximal partition the code allows: 5 directory groups** (apigw, transfer, originate, systemTest, Dev/scripts); inside apigw the KS-1346/KS-1410-ae pair MUST share a seat (same file), KS-1432 is file-disjoint from them.
- **Recommended: 3 seats**, grouped by file FAMILY so each lands on an existing lineage and its toolkit:
  1. **R 28th — api-gateway** (R 19th raised KS-1410 api-gateway in this lineage): KS-1346, then KS-1410-ae, then KS-1432 if released. File-lock: the colliding pair in one seat.
  2. **G 6th — services (originate + transfer)**: KS-1345-del, KS-1410-tr. G 5th's handover names G 6th as its successor (`HANDOVER-seatG5-2026-10-08.md`); `transfer/` has no lineage of its own and is directory-disjoint from originate.
  3. **F 7th — scripts**: KS-998 (`systemTest/`), KS-937 (`Blockchain/Dev/scripts`). F 6th's handover names F 7th; F's lane is the shell-script/guard family (KS-808, KS-1355, KS-1328).
- Why not 5: R 19th's own evidence is "expect 1-2 raises per seat" before the 45% ctx line; the three seats above each carry 2 PRs (R 28th a conditional 3rd). A 4th/5th seat adds one more ITEM 0 + toolkit re-key + a doc keep-both for ≤1 PR each. Splitting is possible with no file conflict if Wednesday wants it: carve KS-1410-tr out of G, or KS-937 out of F.
- **Shared docs: they DO NOT force one seat.** Each raise appends ONE flow block and ONE cheat section at the tail of the same two files; N PRs from N seats all append at the same tail, so the second and later merges hit a textual "both added" conflict at the tail — resolved keep-both (each block is self-contained) at merge time, by the merge seat (R 19th's brief: "keep-both merge-ins at merge time are EXPECTED and Wednesday's to sequence"; precedent: 7 rows of gate77 landed this way, #1437 is the latest). What it costs: one merge-in per PR after the first. What it does NOT force: a shared checkout of the docs (each seat edits its own worktree copy). What WOULD force one seat: a rule that numbers ascend (R 19th's `Q-N5` says ascending is NOT asserted, uniqueness is) — so allocate numbers up front (`Q-NUM`) and N seats are safe. **A collision on a NUMBER is a STOP.**
- Proposed allocation (drafter's proposal, for Wednesday to rule; free at develop: 32 [reserved KS-1432 in earlier briefs], 33, 34 [reserved KS-591 / KS-1364 in earlier briefs, E 12th, their PR state UNMEASURED], 45+): KS-1432 `32.` · KS-1346 `45.` · KS-1410-ae `46.` · KS-1410-tr `47.` · KS-1345-del `48.` · KS-998 `49.` · KS-937 `50.`. Cheat keys: as the ticket, with Q-KEYDUP for KS-1410 ×2, KS-998, KS-1345.
- Tiers (drafter's defaults; READY headers say only "AT LEAST tier 2 — the gate decides"; tier definitions from `learnings/2026-09-05_qa-gate-tiers-and-the-two-nogo-cap.md`): KS-1346 **tier 1** (secrets/PII-in-logs class: gate30T1 NO-GO'd KS-1346 A/B for exactly that on 2026-09-27) · KS-1410-ae and KS-1410-tr **tier 1** (R 19th's brief tabled KS-1410 as TIER 1; 500/502 body disclosure) · KS-1432 tier 2 (behaviour-preserving extraction of a guard predicate) · KS-1345-del tier 2 (follow-up to #1381's gated mechanism, plus a new UUID pre-check branch the gate reads) · KS-998 tier 2 · KS-937 tier 2 **with a mandatory WIDEN cell** (it relaxes a push guard; the READY says "the QA gate must prove the guard still refuses what it exists to catch"). Wednesday rules.

## 6. UNMEASURED / UNSURE (this census)
- PR open/merged state for anything (no API). Branch presence only.
- Whether R 28th / G 6th / F 7th are free names: tmux shows only `%0` Wednesday, `%18` K 3rd, `%1`; the staged-file listing shows R 27th and K 3rd as the last tonight. R 20th-R 27th were MERGE seats; whether R 28th should be a raise or the next merge seat is Wednesday's (Q-LANE).
- Linear state, assignee and newest comment for every key (no Linear access): the briefs make the seat read them (ITEM 0 (g)).
- Why KS-1432 was "held": READY headers use "HELD for QA" for every file (hold_ready's word), but R 19th's brief (2026-10-08) lists KS-1432 as "REVIEW-held, in NO seat" and reserves flow `32.`. Not resolved here: Q-1432HOLD.
- A stray `/tmp/x.err` file was written by `fetchprs.sh` (outside the scratchpad, ~one line of fetch output). Not deleted (never delete); harmless; flagged.
- Lint/prettier on KS-1346's very long single line (the checker ran vitest + `tsc --noEmit` only; `grep` for `max-len|printWidth` in the Dev eslint/prettier config paths I tried returned nothing, which proves only that those file names are not where it lives).
- The 15 changed paths and "0 touched twice" count are from the temp-index stack with the recorded options; nothing was built, no test was run by this drafter.
