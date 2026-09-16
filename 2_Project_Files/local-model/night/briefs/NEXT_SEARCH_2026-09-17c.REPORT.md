# NEXT SEARCH 2026-09-17c (04:15–04:35 AEST): up to three Ornith tickets

**BLUF: ONE FIT: KS-1181, as a partial (F3, "parse the header counts").** It is test-only: one NEW 75-line test file in `packages/shared/src/__tests__/`, graded by a tamper planted in the KS-727 guard's header (the #1006 gate's G7). The guard itself stays untouched. The brief's own fence went through the real checker at the new tip `1125607e9` and gave **RESULT: PASS (7/7)** with `apply_mode=strict`. It passed four times in all: twice at `d067725ff` and twice at `1125607e9`, the last run using the placed brief and input.

Every other ticket read was REFUSED, each for a measured or read reason (table below). The candidate list is exhausted:
- **Candidate 3:** Linear returned 65 Backlog/Todo issues updated since 2026-09-16T12:00Z (2 pages). 14 are KS tickets and 51 are Platform-S (PS) tickets.
- **Candidate 4:** the tier-level refusals were re-read: KS-1142, KS-979, KS-1159, KS-1128, KS-953, KS-1119 and KS-1176.

**Files and what was not touched:**
- Brief: `night/briefs/KS-1181.md` (new; no `KS-1181.md` existed, so no suffix).
- Input: `night/inputs/code_1181.json`. `build_input.sh` rc 0 at 04:34:03, tip `1125607e9`, ~20.2K prompt tokens, ctx 65536.
- Not queued and not run on the night runner. `queue.md`, `done.md`, `candidates.md`, `IMPROVEMENTS.md`, the checkers and the other briefs were not touched.
- The Secuura checkout was 0 at every porcelain reading (21 readings, 04:15:46–04:33:40). No git write verb ran against it, and no seat A worktree or gate clone was entered.

**Queue line** (the builder does not refuse this ticket: 0 attachments, Backlog):
```
KS-1181 input=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/inputs/code_1181.json task=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/tasks/code_patch/task.md ctx=65536
```

## Pins (KS-1181)
- **Tip:** `1125607e978d6ad637720c985e43e3d79fecdf88`.
  - **Origin moved mid-search:** it read `d067725ff` from 04:15:46 to 04:25:58, then `1125607e9` from 04:28:14 on. That commit is #1010 (KS-1183).
  - GitHub compare (04:28:52): 1 commit, 2 files, both api-gateway (`routes/verification.ts` and the ks1087 test).
  - `git diff --stat d067725ff HEAD -- Blockchain/Dev/packages/shared` is empty.
  - Rounds r3, fin3 and fin4 re-ran everything at the new tip in a fresh clone (`ks1181_pm.URNKkv`).
- **Guard:** `packages/shared/src/__tests__/ks727-errorhandler-class-guard.test.ts`, blob `512729715` (the #1006 gate's equality target), 946 lines, sha256 `edbef941ae3d0cf2…`.
- **Builder pins (all required):** `product=Blockchain/Dev/packages/shared/src/__tests__/ks727-errorhandler-class-guard.test.ts ref=packages/shared/src/__tests__/ks780-normalise-org-id-one-implementation.test.ts line=32 ctx=65536`
  - `product=` is required because the ticket names only a test path, which the builder's path scan skips.
  - `ref=` is required because no test imports the guard.
  - The builder's `suggested_test_file` equals the brief's path: `ks1181-ks-727-error-handler-guard-corpus.test.ts`.
- **Tamper:** at `:32`, `//   Count today: 9 modules contributing 10 handlers. Both are exact sets` becomes `… 8 modules contributing 9 handlers. …` (G7). A `statement_ok:` clause is given.
- **Declared red:** `🔴 KS-1181 F3 — every count in the guard header equals the exact set the guard asserts`.
- **Scripts:** `scratchpad/next17c/premeasure.sh` (outputs `premeasure.r1..r3.out`) and `final.sh` (`final.fin1..fin4.out`).

## Pre-measure summary (sandbox-exec, off-host outbound denied; r3/fin3/fin4 at `1125607e9`)
- **The gap is still there.** The guard alone at the tip is 103/103. Under G7 the guard alone is still **103/103 green**.
- **Baselines:**
  - Whole packages/shared suite at the tip: 851 cells, 3 red.
  - Those 3 reds are all sandbox artefacts: `ks914-shipped-path` ×2 and `ks932` ×1, failing on `connect EPERM 203.0.113.7`. They are the same set with the golden.
  - With the golden: 854 cells, no new red.
- **New test at the tip:** 3/3, twice.
- **Tampers on the guard** (anchor count 1 → 0 each, restored by checkout with the sha asserted):

| row | reds (all by assertion) |
|---|---|
| **G7 (checker)** | only the 🔴 cell, `expected 8 to be 9`; both 🟢 controls green |
| `Of those 10` → 9 | only the 🔴 cell, `expected 9 to be 10` |
| `exactly 1 is a FILTER` → 2 | only the 🔴 cell, `expected 2 to be 1` |
| `0 inline sites` → 1 | only the 🔴 cell, `expected 1 to be +0` |
| `across 0 files` → 1 | only the 🔴 cell, `expected 1 to be +0` |
| a tenth `EXPECTED_CORPUS` entry planted | only the 🔴 cell, `expected 9 to be 10` |
| reword to `nine … ten` | the 🟢 phrase control (`expected +0 to be 1`), and the 🔴 cell reads `NaN`: a reword fails loudly |

- **tsc:**
  - Project build: rc 0.
  - Including program: rc 0 with 0 errors.
  - The checker's standalone command: rc 0.
- **decl_splice:** `spliced 0` against the pinned ks780 and against 7 other `readFileSync` tests.
- **Checker on the brief's own fence (fin3, 04:30:05–04:30:26):**
  - Strict apply rc 0, and the applied file == golden.
  - A1–A7 PASS: A3 test-only (+75/-0), A4 1/3 under the tamper, A5 3/3, A6 851→854 with NEW `[]`, A7 rc 0.
  - The guard's sha was back to the tip afterwards.
  - fin4 (04:31:44–04:32:06) on the placed brief and input: PASS 7/7 strict.
  - Afterwards the input was rebuilt once for brief wording only. Comparing it with the checked input, only `ticket.description` differs.
- **Partition:**
  - 21 open PRs (GitHub REST, 04:18:50–04:19:14). None touches the guard or a ks1181 file. Their only packages/shared paths are `package.json` (dependabot), `ks256-spec-example-contract.test.ts` and `openapi/examples/fixtures.ts`.
  - Seat A's KS-999/1018/1050/1072/1101 diffs are auth and api-gateway.
  - No `READY_*` diff has a `+++ b/` path on the guard or a ks1181 file.
- **Raise notes (in the brief):**
  - PR says "Refs KS-1181 (F3)", never Closes.
  - Still open: F2 and F3's wording half ("The 10th handler"; `:19` "the assertions in the file").
  - The `:74`/`:81` NOT-COVERED counts are not asserted, on purpose.
  - Expected tier: 1.

## Rejection table (every ticket read this search)
| ticket | verdict | measured / read reason |
|---|---|---|
| **KS-1181 F3 (parse counts)** | **FITS (briefed)** | See above. |
| KS-1181 F3 (reword `:18-21` / "The 10th handler") | REFUSED | It is a comment-only hunk in a 946-line `.ts` test, and no task type grades it. **doc_patch:** its D4 needs a `#`/`##`/`###` heading line, and the guard has **0** lines starting with `#` (134 `//` lines); measured. **code_patch:** a comment change reds no cell. It is also the >600-line modify-in-place class. |
| KS-1181 F2 (hit witness in a NEW file) | REFUSED | **(1)** The guard exports **0** symbols (`^export ` count 0; 28 file-local declarations), so `HANDLERS`, `discover` and `driveThroughRoute` (`:222-297`) cannot be imported. A new file would have to re-derive the corpus, a second local copy of the kind KS-833's `:907` cell guards against. **(2)** The ticket's regression ("G5's throw must red the 6 NODE_ENV cells") is about cells inside the guard, and no sibling file can change their colour. **(3)** The fix site `driveThroughRoute` is inside the 946-line file (modify-in-place class). |
| KS-1182 F7 | REFUSED | **(a)** File name vs describe is a rename: not a hunk, and it gives the test-only A3 a two-path touched set. **(b)** The markers (ks844 is 89 lines, cell 2 `:57-75`): a tamper that yields express's HTML reds `:68` `<html` first, so new markers are never decisive (the gate's own point). A JSON-body stack tamper would plant at `errorHandler.ts:37`, a line the held `READY_KS-1182-F4` diff removes (`-    error: { code, message: … err.message },`, measured at its line 35), so the grading target collides with a held READY. And `err.stack` in JSON carries a literal `    at `, which the OLD marker already catches. |
| KS-1184 (P2) | REFUSED | The ticket calls itself "A design call beside KS-1087 item 2" and offers two shapes. The site is `api-gateway routes/verification.ts`, which was an open-PR lane (#1010) and changed again at `1125607e9`. |
| KS-1178 (P4) | REFUSED | Decision first ("Decide whether `createdOnBehalfOf.email` is needed"), an S-side erasure hook, and unassigned. Not a one-file fix. |
| KS-1177 (P3) | REFUSED | "Owner decision on the intended behaviour, then one of" three options. The subject is the CSRF middleware and versioning order in api-gateway (security surface). |
| KS-772 (P2) | REFUSED | A review-stream tracker for Stuart (S↔K contract, 20 tickets). No patch. |
| KS-1182, KS-1180, KS-1179, KS-864, KS-1123, KS-960 | SKIPPED (held) | READY/done rows exist. KS-1123, KS-960 and KS-864 also carry PR attachments. |
| KS-1175, KS-1173, KS-1129 | SKIPPED (recorded) | SEARCH 2 refusals (feature; covered by READY 1172-*). KS-1129 is set aside and has a PR. |
| PS-* ×51 (candidate-3 set) | OUT OF SCOPE | Platform-S team tickets, not Platform K. Most are on Stuart's account or unassigned S work. |
| **KS-1142** (tier-level "test refactor with no product tamper") | REFUSED (measured) | The gate's ⊆ cell was built as a new file and measured (`pm1142.r1.out`, 04:28:14–04:28:37, packages/shared identical at both tips). It is **redundant with existing guards**. Under the K1-side tamper (`'services/analytics'` renamed in `entrypoint-corpus.test.ts:411`), K1 itself reds too. Under the ticket's own regression (a CORPUS path swapped to an unlisted package in ks781), ks781's corpus leg reds too. Each literal is already asserted against the walk, so the new cell can never be the only red. The shape that removes the double upkeep is one literal imported by both, a two-file refactor of the **5,416-line** ks781 file. The ticket also calls the fix "the GATE'S PROPOSAL, not ratified". |
| KS-979 (tier-level "no tier grades it") | REFUSED | Re-read. Two comment corrections in an originate **jest** test file, and "no behaviour is affected and the cells themselves are correct", so no cell can red. Unlike F3, there is no count or set to parse, only prose citations. |
| KS-1159 ("later tier") | REFUSED | Re-read. It widens `ks1061-shared-mock-completeness` (originate jest) and adds three T6b/T6c/T7 fixture files the guard must name: multi-file, and the subject is a guard test. |
| KS-1128 | REFUSED | Re-read. The cell needs a real platform PostgreSQL behind `PLATFORM_DATABASE_URL`, driven through the ks949 `tsx` boot driver. The recorded reason (the seed's `pg` is a `require` inside the function) stands. |
| KS-953 ("api-gateway, seat A" title-level) | REFUSED | Re-read: "Shapes worth considering (not chosen — this needs a decision)". |
| KS-1119 ("multi-tenant security surface") | REFUSED | Re-read. "Prove it first, live" with multi-tenancy on, sequenced with the KS-584/KS-590 decision. Originate verification (security). |
| KS-1176 ("api-gateway, seat A" title-level) | REFUSED | Re-read. **Creator `peter@obeden.com`** (Peter's ticket; unassigned). It is an authorization-gate edit in `services/enforcement.ts` with two options, and option 2 is "a product decision". |
| KS-1113 | REFUSED (tier fact still true) | An e2e spec, and there is still no Playwright task type (`tasks/` = bash_patch, code_patch, doc_patch, facts_comment, predicate_classify, state_census). |
| KS-849, KS-1076 and the other set-aside rows | NOT RE-READ | Their recorded reasons are per-ticket facts (e.g. kyc listens at import; KS-1076 "likely already fixed", a record close), not tier verdicts. |

## Wrong in tickets / gates / harness (for Wednesday to file; IMPROVEMENTS.md not edited)
1. **Harness: `build_input.sh` silently builds a code_patch input from a brief that says TEST-ONLY but has no `## Tamper` block.** This happened for real. A scripted edit of the brief matched the inline mention "see `## Premises (measured)`" in the header, not the section heading, and deleted the middle of the brief. The rebuild still gave rc 0 with `tamper: null`, `red_cells: null`, `sites: []` and "named sites: no '## Where' section". The checker would then have run in code_patch mode and expected RED at the untouched tip. It was caught by the input shrinking from 79.5 KB to 66.7 KB and by a `defect_line` diff against the checked input. The brief was restored and re-proved (fin4). **Proposed:** refuse when the brief's title or mode says TEST-ONLY and no tamper parses. **Brief-writer rule:** locate sections by `\n## Heading\n`, never by a bare substring.
2. **Harness: a test file can be the test-only "product".** This is new and it worked: `product=` pointed at a guard test, and the tamper was planted in it. The builder's path scan skips `__tests__` paths, so `product=` is mandatory. The ref scoring can never match a `__tests__/…` module, so `ref=` is mandatory. Worth a line in the builder usage.
3. **Harness: the code_patch checker leaves the NEW test untracked in the clone after a test-only PASS** (fin1–fin4). The 17b report recorded this for code_patch mode; it holds in test-only mode too. A reused clone must be cleaned.
4. **Harness: a sandboxed A6 cannot see 3 packages/shared cells.** `ks914-shipped-path` ×2 and `ks932-timeout-bounds-dns` ×1 are red under the off-host deny (`connect EPERM 203.0.113.7:443`), and A6 attributes them as "develop's own reds". A change that broke those cells for real would pass A6. This is related to KS-1179's F-2 (ks932 depends on 203.0.113.7 hanging), whose READY diff touches `ks932`.
5. **Harness: the decl_splice STRING trap recurs.** Against the guard, the new test's string `'const FORWARDING_HANDLERS = new Set(['` counts as a use and prints `UNREPAIRABLE … FORWARDING_HANDLERS (ref :206)`. The guard is not the ref here, but any future brief that pins a text-parsing test's ref to the file it parses will hit this.
6. **Harness: the builder's Peter/Stuart gate reads the assignee only.** KS-1176 is unassigned but was created by `peter@obeden.com`.
7. **Ticket KS-1142: the gate's ⊆-cell proposal adds no red.** Both of its regressions already red an existing cell (K1 or the ks781 corpus leg). Only "one literal imported by both" removes the defect. Worth a comment on the ticket before anyone briefs it.
8. **Ticket KS-1181: F2 cannot be fixed outside the guard.** The guard exports nothing, and the regression names the guard's own cells. F2 needs a Claude seat (a modify-in-place of the 946-line file). F3's wording half is also Claude-seat or Record.
9. **Tip drift:** #1010 (KS-1183, `verification.ts` + the ks1087 test) merged during the search. That removes #1010 from the open-PR partition, and `verification.ts` has moved for any brief that cites its line numbers (KS-1184's `:970-972` cite was written against #1008's head `dd7086d5a`).
