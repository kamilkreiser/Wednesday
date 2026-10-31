# QA GATE 50: Secuura/Blockchain tier-2 batch, PRs #1842, #1847, #1851, #1852 (all by our seats), Round 1
Sonnet 5.5, findings-only. Nothing was fixed, pushed, commented or merged; Linear was read only.

**Heads gated** (each re-pinned with `git ls-remote` and a fetch of `refs/pull/<n>/head` at 14:4x, all four OPEN, none moved since R 66th's READY):

| PR | Ticket | Head gated | Base |
|---|---|---|---|
| #1842 | KS-1534 | **23af54d655de7749d63c4c05ab25fd9c12f5ead8** | develop, merge-base a8c554659cb3 |
| #1847 | KS-1579 | **731df241e3338aa9242140d47606c2917aed7258** | same |
| #1851 | KS-1866 | **1c73d6ea5d3992d28e2192afd2a3f48403f097b0** | same |
| #1852 | KS-1544 | **2d28a3496bf51ba154a7fc66846734804918b610** | same |

Develop tip now is 9e1eb55fde53, 15 commits past the merge-base. None touches any product or test file of these four PRs (the only scripts change is `check-no-sql-injection.sh`, a sixth script that #1851 does not touch).
**#1842 head is the SAME head the Spark shadow of 10-30 ran on (23af54d6).** Nothing changed on the PR since, so I re-gated the head as it stands, not a delta (see the calibration note: Spark's verdict on this identical head changed from NO GO to GO WITH NOTES, which is a checklist change, not a PR change).

## VERDICTS

| PR | Verdict | Fix before merge? |
|---|---|---|
| #1842 KS-1534 | **GO WITH NOTES** | no |
| #1847 KS-1579 | **GO WITH NOTES** (docs hold only) | no |
| #1851 KS-1866 | **GO WITH NOTES** | no (F-851-1 and F-851-2 want a follow-up ticket or a one-line fix, the seat's choice) |
| #1852 KS-1544 | **GO WITH NOTES** | no |

No Major finding anywhere. All four PRs conflict with develop in the two `Projects Documents/*.html` files and merge clean in code; per the docs-fragments transition that is NOTED ONLY (F-D below).

---------------------------------------------------------------------------------------------------

## #1842 (KS-1534): a source-text pin that the info reader and the create path carry one allow-list guard. TEST ONLY, zero product bytes.

| File | Change | Gated |
|---|---|---|
| api-gateway/src/__tests__/ks1534-allow-list-guards-are-the-same-executable-code.test.ts | new, +57, 5 cells G1-G5 | yes |
| Projects Documents/*.html (2 files) | +18 / +20 | conflict noted only |

- **Against the ticket.** KS-1534 item (a) offers two options: one shared helper (edits the create path, needs its own gate) or "a source-level cell asserting the two guards are the same executable code ... compare the code, not the text". This PR takes the second. It reads both files, drops whole-line comments, and compares the guard condition with the variable name normalised. The guard lines exist where the PR says (`health.ts:98`, `verification.ts:810`; the ticket's `:1307` is stale). The PR says "Refs", not "Fixes", and its ticket comment says the helper option and item (b) are not done. Honest.
- **Spark deterministic:** head 5/5; on base product code 5/5. That is expected for a test-only PR (it pins something already true), so "red on base" cannot be shown that way. The red proof is by tamper, below.
- **Tamper / mutants** (copy of `health.ts` and `verification.ts` saved, restored, sha256 equal; `probes/mut1842.txt`):
  - M1 drop `&& !Array.isArray(...)` in health.ts (the PR's own claim): G1, G2 RED, 2 of 5. Reproduces.
  - M2 same drop in verification.ts: G2, G3 RED.
  - M3 guard line commented with `//`: RED. M4 `!= null` rewrite (same meaning, different text): RED (a false alarm that forces a deliberate update, acceptable).
  - M5 change the 403 text in health.ts: still 5/5 GREEN (not this test's job; ks1232 owns the text).
  - M6 guard wrapped in `if (false)`: still GREEN. Inherent to any text pin; the behavioural ks1232 cell is the net.
  - **M7 guard disabled by a multi-line `/* ... */` block whose inner lines do not start with `*`: still 5/5 GREEN** (F-842-1).
- Suite at head: api-gateway whole 131 files, **1326/1326**, matches the PR (develop 1321). `eslint` on the new file 0; `tsc --noEmit -p` api-gateway 0 errors (I did not reproduce the PR's "27 baseline errors in other test files": under the service tsconfig I see 0; not a defect, same as gate 47 F2).

**Findings**
- **F-842-1 Minor (instrument: tamper M7, then the existing behavioural cell as the net).** `executableLines` only drops lines that START with `//`, `/*` or `*`. A guard disabled inside a block comment whose inner lines have no leading `*` is still counted, so G1 and G2 stay green. The file's own header says "a guard that survives only in a comment is not a guard"; G4 proves that only for a `//` line. Net risk is low: the existing `ks1232-info-reader-refuses-a-non-array-allow-list.test.ts` goes RED (2 of 5) on the same mutant. Fix when convenient: strip `/* ... */` spans before splitting lines, plus a G4-style control for it.
- **F-842-2 Note (read).** The pin compares the guard condition only. It does not look at the 403 body or the code in the block (M5 passes). Those are covered by ks1232 / ks1204 behavioural cells, so no gap overall, but the file name "are the same executable code" claims a little more than "the same `if` line".
- **F-842-3 Note (ticket scope).** KS-1534 stays open for the helper option and item (b); the PR says so.

---------------------------------------------------------------------------------------------------

## #1847 (KS-1579): the erase-connector header comment and one cell title state what the code does. Product change is comments only.

| File | Change | Gated |
|---|---|---|
| originate/src/services/connectorOrganisationErasure.ts | +3 -2, comment lines only | yes |
| originate/src/__tests__/ks695-ask3-erase-connector-refusals.test.ts | +1 -1, one `it()` title | yes |
| originate/src/__tests__/ks1579-erase-connector-comment-and-title-state-the-truth.test.ts | new, +43, 6 cells T1-T6 | yes |
| Projects Documents/*.html (2 files) | +19 / +21 | conflict noted only |

- **Against the ticket** (items 3 and 4 of the 5-item checklist): item 4 header sentence, item 3 stale title. Items 1, 2, 5 are left open and the PR says so ("Refs ... only").
- **The new comment is true.** Read against the code: the collision `SELECT` (`connectorOrganisationErasure.ts:359`) and the ownership `SELECT` (:149) have no `is_active` predicate, so inactive keys are seen; security's `retirePriorStatement` (index.ts:215-218) is an `UPDATE svc_api_keys SET is_active = false` / shorten expiry; the revoke route sets `apiKey.isActive = false` and never deletes. So only a DELETED key escapes the guard. "rotated away" occurs nowhere else in the tree (develop 0; the one HTML hit is the PR's own docs entry quoting the old phrase).
- **Comment-only claim, re-measured:** whole-line-`//`-stripped product file hash is identical at base and head (364 lines both, 3857e3c75eae09ca), and a planted one-token code change gives a different hash (control). Only comment lines differ.
- **Spark deterministic:** head 40/40 (the new file 6 + the refusals file 34); base product code 38/40, the 2 fails are T1 and T2 (the header cells). T3 and T4 are about the test file's own title, so they only go red against the OLD test file; that is why the PR says "4 of 6 red" and the harness shows 2. Consistent, not a discrepancy.
- Suite at head: originate whole **153 suites, 1866/1866**, matches the PR (develop 1860). `eslint` on the 2 test files 0; `tsc --noEmit -p` originate 0.
- Red-proof: the product-only revert goes RED on T1, T2 (Spark gate, base product). The title cells T3/T4 are text-presence checks of one string each; I did not mutate them separately.

**Findings**
- **F-847-1 Note (read).** T2 and T4 pin the exact wording of a comment and a title, so any later rewording of either fails the test. This is what a prose pin does and the PR calls the cells "source-text"; just be aware that it makes the comment hard to edit.
- No code or behaviour finding. Items 1, 2, 5 of KS-1579 remain open as stated.

---------------------------------------------------------------------------------------------------

## #1851 (KS-1866): five `check-*.sh` guards answer correctly on the cases they exist to catch

| File | Change | Gated |
|---|---|---|
| scripts/check-dockerfile-non-root.sh | 1 line: `\s` -> `[[:space:]]`, `|| true` on the pipeline | yes |
| scripts/check-no-strictness-patches.sh | `--exclude-dir=node_modules` | yes |
| scripts/check-connector-xss.sh | `--exclude-dir=node_modules` | yes |
| scripts/check-no-pii-store.sh | 2 lines: `--exclude-standard=false` -> `--exclude-standard`; `; true;` ends the warning group | yes |
| scripts/check-akto-container-names.sh | verb alternative now allows `([[:space:]]+-[^[:space:]]+)*` between verb and name | yes |
| scripts/__tests__/check_*.test.sh | 5 new suites (+61, +85, +70, +84, +76) | yes |
| Projects Documents/*.html (2 files) | +19 / +22 | conflict noted only |

- **Spark deterministic:** the 5 suites at head 23/23; on base product code 13 pass / 10 fail (files all red). That is the ticket's 2+2+1+2+3 = 10. Matches.
- **Real-tree behaviour:** `check-dockerfile-non-root.sh` on the real tree: "all 35 Dockerfile(s) drop root"; `check-no-pii-store.sh`: OK; `run-code-guards.sh` **13/13 guards pass**, matching the PR. The existing akto suite is **17/17**.
- **Mutants: 7 of 7 killed** (`probes/mut1851/`; each suite takes the subject through its own env override, so no tree file was touched): A drop the `true;` (PII cell 2 RED), B restore `=false` (2 RED), C drop the flag group (3 RED), D put `\s` back into the sed (3 RED on this BSD userland), E drop `|| true` (1 RED), F drop `--exclude-dir` in xss (1 RED), G drop it in strictness (2 RED).
- **Akto pattern false-positive and cost probe** (`probes/akto_probe.txt`): `docker exec -it ${AKTO_PREFIX}-mongo`, `"$AKTO_MONGO"` and `secuura-mongo` still pass; a 3000-flag line takes 5 ms (no backtracking blow-up).
- Shell suites whole: `run-shell-suites.sh` at head in my worktree: **101 passed, 1 failed, 2 skipped (of 104)**. The one failure, `blockchain_testing_target_base_follows_the_slot.test.sh`, stops with "FATAL: tsx not installed" (my worktree has no `Dev/node_modules`; the cell's own earlier checks all pass), so it is my set-up and not the PR; it touches none of the changed scripts. The second skip, `preflight_test_types_ratchet_leg`, is also environment. So I could NOT reproduce the PR's "103 of 104" exactly (UNMEASURED); every one of the five new suites and the akto suite passes in it.
- The XSS suite proves the `--exclude-dir` argument is on the grep command line using a stub grep (PR says so). That is an argument-text pin, which fits a cost-only change (the verdict is unchanged because the post-filter stays).

**Findings**
- **F-851-1 Minor (instrument: pattern probe, 15 lines).** The new flag group only matches flags with NO separate value. `docker exec -u root akto-mongo ...`, `docker exec -e FOO=1 akto-mongo ...` and `docker exec -it -u root akto-mongo ...` still PASS the gate, although they target slot 1. It is the same class as `docker logs --tail 5 akto-testing`, which the ticket and PR name as "not fixed", but `-u` and `-e` are far more common than `--tail N`, and they are not in the "not fixed" list. Not a regression and outside "flags with attached values". Add them to the KS-1866 "not fixed" list or widen the group (for example allow a following non-akto token).
- **F-851-2 Minor, pre-existing (instrument: fixture run of the script, `nr.sh`).** `check-dockerfile-non-root.sh` compares the last USER to `root` and `0` exactly. `USER root:root`, `USER 0:0` and `USER ROOT` all pass with rc 0 and "OK". The PR fixes the "USER root read as USERroot" fault and the no-USER silent exit, but the guard still has this hole. Separate ticket. Also: if one of the five scanned directories is missing, `find ... | sort` under `set -e` + `pipefail` still exits silently (my first fixture hit it; the real tree has all five, so no effect today).
- **F-851-3 Note (read).** `check-no-pii-store.sh:57-58` still carries the comment "--exclude-standard=false still honours .gitignore", about the option the PR just removed. The second sentence of that comment (why the `find` leg exists) is still right; the first is stale.
- **F-851-4 Note (instrument limit).** The Dockerfile cell 2 ("final USER root exits 1") is only red on a BSD/macOS userland (the file says so). On the GNU/Linux CI image, base is green for that cell, so it is a regression guard there, not a red-first proof. Not run on Linux (UNMEASURED).
- **F-851-5 Note.** The PR text says it hand-edited one Spark-authored suite (two printf fixtures spelled the banned flip) and asserted equal bytes. I confirmed the strictness suite is red at base (2 fail) and passes at head, so the edit did not neutralise it.

---------------------------------------------------------------------------------------------------

## #1852 (KS-1544): eleven more paged lists end their ORDER BY in the primary key

| File | Change | Gated |
|---|---|---|
| originate/src/services/errorTrackingService.ts | 5 `system_errors` reads: `, id DESC` | yes |
| originate/src/routes/adminConfig.ts | 2 `audit_logs` (`, id DESC`), 2 `rights_holders` (`, id ASC`) | yes |
| staking/src/routes/rewards.ts | `svc_reward_claims` `, id`; `svc_revenue_distributions` `, id` | yes |
| originate/src/__tests__/ks1544-class-originate-paged-lists-order-in-a-total-order.test.ts | new, +61, 6 cells | yes |
| staking/src/__tests__/ks1544-class-staking-rewards-paged-lists-order-in-a-total-order.test.ts | new, +56, 6 cells | yes |
| Projects Documents/*.html (2 files) | +20 / +23 | conflict noted only |

- **Count and schema.** 5 + 2 + 2 + 2 = 11 clauses, as claimed. `id` is the primary key of all five tables: `system_errors` (migrations/040, UUID), `audit_logs` (001, UUID), `rights_holders` (docker/init/07, UUID), `svc_reward_claims` and `svc_revenue_distributions` (migrations/002, TEXT). All reads are single-table `SELECT *`, so `id` is not ambiguous. No other paged read is left in these two services except `staking/src/routes/stake.ts:458` (below).
- **Against the ticket.** KS-1544 names `platform_audit_log` (merged in #1600). This PR applies the same class elsewhere and says "Refs", ticket stays open.
- **Spark deterministic (one call per package):** originate 6/6 at head, base product 3 fail / 3 pass; staking 6/6, base 3 fail / 3 pass. Matches "3 of 6 red in each file".
- **My red proof:** originate file under jest at head 6/6, with the two product files restored to base 3 FAIL (T1, A1, A2); staking at head 6/6, base `rewards.ts` 3 FAIL (T1-T3). Files restored and `git status` clean each time.
- Suites at head, `--maxWorkers=2`: originate whole **153 suites, 1866/1866**; staking whole **72/72**. Both match the PR. `eslint` 0, `tsc --noEmit -p` 0 in both services.
- The originate file has no `import` from vitest and is run by jest (the package has `jest.config.js`); run under vitest it is "no tests", which is not a PR defect.

**Findings**
- **F-852-1 Note (read; the PR names it).** `staking/src/routes/stake.ts:458` `ORDER BY stake_date LIMIT $1 OFFSET $2` on `svc_stake_positions` is the same class and is untouched. Fold it into KS-1544 or a new ticket.
- **F-852-2 Note (UNMEASURED, reasoned only).** `ORDER BY created_at DESC, id DESC` with a tenant filter may no longer be served in index order by an index on `(tenant_id, created_at DESC)` alone. Plans were not measured by the PR or by me. KS-1544 already lists the query-plan check as owed.
- **F-852-3 Note.** Both tests are source-text and scan only `LIMIT ${limit} OFFSET ${offset}` (originate) and `LIMIT $n OFFSET $m` (staking) shaped clauses; the exact-count cells (5, 4, 2) catch an added query that follows the same shape, and a differently shaped paged read would escape. No paging behaviour was run against a real table (as the PR states).

---------------------------------------------------------------------------------------------------

## F-D (all four PRs, NOTE ONLY: docs conflict)
`git merge-tree --write-tree` of each PR head into develop 9e1eb55f reports conflicts only in `Projects Documents/API_Security_Functional_Testing_Architecture_Flow_Diagrams.html` and `Projects Documents/QA_Tool_Cheat_Sheet_Secuura_API_Testing.html`. All code and test files merge clean. The docs-fragments transition handles it; I did not read the entries beyond confirming each PR's own section exists (and, for #1847, that it quotes the old phrase on purpose).

## UNMEASURED
- Any real PostgreSQL: paging behaviour with tied rows (#1852), query plans or index use (#1852), the KS-695 R-cells (#1847 items 1, 2, 5 of the ticket).
- A GNU/Linux userland for #1851 (grep/sed behaviour, the Dockerfile cell 2 as a CI guard). Everything shell was run on macOS (BSD grep/sed, bash 3.2/5 mix as installed).
- The PR's whole-shell-suite figure 103/104 (my run: 101 + 1 env failure + 2 skips, see #1851).
- Node 24, the other platform suites, a running stack, Akto/Schemathesis/Playwright/k6, deploy.
- The HTML docs content beyond conflict detection.
- `tsc` with the test files in the program (the PR's "27 baseline errors"): my `tsc --noEmit -p` under each service tsconfig reports 0.
- Spark's staking run was a separate `spark_gate.sh` call; `spark_review.py` takes one `--facts`, so #1852's review saw only the originate facts (see calibration).

## SPARK CALIBRATION (pilot evidence)

**Deterministic half (`spark_gate.sh`): 4 of 4 matched my own runs exactly.**
#1842 5/5 (base 5/5, test-only); #1847 40/40 (base 38/40); #1851 23/23 (base 13 pass, 10 fail); #1852 originate 6/6 (base 3/3), staking 6/6 (base 3/3). Instrument faults on my side, not the tool's: the first vitest runs hit "Cannot find module vitest/config" because `--node-modules` symlinks ONE directory and vitest is hoisted at the monorepo root, so I built merged node_modules dirs (service + root) and re-ran; originate needs jest, which the harness picks itself.

**Review half (`spark_review.py`, shadow, one request at a time, 31-90 s each, 1 retry on #1851 after a repetition abort):**

| PR | Spark verdict | Mine | Match | Spark findings | True and useful | False positive / misread | Instrument-gap "unmeasured in facts" | I found, Spark did not |
|---|---|---|---|---|---|---|---|---|
| #1842 | GO WITH NOTES | GO WITH NOTES | yes | 4 Notes | 2 (regex only matches a one-line guard; only the condition is compared, not the 403 body) | 1 (says the test is "not red on base": true fact, wrong inference for a test-only pin) | 0 | F-842-1 block-comment gap (Minor, with a reproducing mutant) |
| #1847 | GO WITH NOTES | GO WITH NOTES | yes | 8 Notes | 1 (T2 pins wording) | 0 (the "2 of 6 vs 4 of 6" note is correct arithmetic, not a defect) | 4 (suite, tsc, eslint, comment-only) + 1 (HTML over size cap) | none; I verified the comment's claims against the code and the comment-only hash |
| #1851 | GO WITH NOTES | GO WITH NOTES | yes | 8 Notes | 2 (both ticket-acknowledged: `--tail 5`, digit var names) + 1 trivial (stub grep is more permissive) | 2 (says Dockerfile cell 1 and PII cell 2 do not prove the fault: both do, and mutants A and E are killed) | 2 (run-code-guards, shell suites) | F-851-1 `-u/-e` flag values (Minor), F-851-2 `USER root:root / 0:0` (Minor), F-851-3 stale comment |
| #1852 | GO WITH NOTES | GO WITH NOTES | yes | 7 Notes | 1 (PK claim unverified; I verified all five) | 2 (says the regexes "may pass vacuously": disproved, the count cells plus RED 3/3 on base) | 3 (staking run, tsc/eslint, whole suites) + 1 (staking base not recorded) | F-852-1 `stake.ts` sibling (PR states it), F-852-2 index/plan, F-852-3 shape-limited scan |

Totals: 27 Spark findings; 6 true and useful, 5 false or misread, 11 instrument-gap notes (a Note that says a PR number is not in `facts.json`; true of the facts, not of the PR, and all of them were measurable and I measured them), 5 trivial or non-findings. Verdict match 4 of 4. Spark found no Major and I found none, so there was nothing for it to miss at Major.

**What the pilot shows.**
1. The deterministic half is trustworthy and saves real time (it reproduces red-first and the head/base counts without me). Its limits are in set-up: one `--node-modules` dir per call (needs a merged dir for vitest in this monorepo) and one `--facts` per review (a two-package PR gets only one package's facts, which caused two of #1852's notes).
2. The review half is a competent checklist reader, not an investigator. It repeated what the ticket and PR already say, flagged "claim not in facts.json" for every figure the facts file does not hold (11 of 27), and twice declared a test "vacuous" or "not proving" without running a mutant. It found none of my five Minor findings, all of which came from running something (a mutant, a probe line, a fixture) rather than reading.
3. **Same head, two verdicts.** On #1842 head 23af54d6 the 10-30 Spark review was NO GO with two Major (fragile regex; "PR does not share the predicate"); today's, on the identical head, is GO WITH NOTES. `REVIEW_CHECKLIST.md.pre-1030-pinprs` shows the checklist changed in between (pin-PR guidance), so that is a rule change, not noise, but it means a Spark verdict is only comparable within one checklist version. The old NO GO's second Major (the ticket offers a pin as an option) was a misread of the ticket, which the new rule fixed.
4. Net: use Spark as the facts step and as a free first reader for tier-2; do not let it substitute for the mutant and probe step, which is where every actionable finding here came from.

## HOW
- Clone: `git clone --shared --no-checkout` from gate 48's clone into the non-existent `repo/` under this folder, toplevel asserted, origin set to Secuura/Distributed_Secuura with the Blockchain deploy key as `core.sshCommand` and push URL `no_push_qa_gate`. Fetched the four PR refs and develop into `refs/qa/p<n>`; the heads above were read from GitHub by `ls-remote` and by the fetch, both equal.
- Spark gate: `spark_gate.sh` once per PR (twice for #1852), work dirs in the session scratchpad, `--node-modules` set to merged dirs; then `spark_review.py` once per PR, sequentially, with the Linear ticket text (the fetch worked this time) and the head commit message as the PR body (the Blockchain `gh` config is not logged in, so the PR bodies themselves were not read; the ticket comments carry the same text).
- My runs: two detached worktrees (`wt`, `wt2`) of the clone; mutants and base swaps by copying the file aside and restoring it, with sha256 equal and `git status` clean afterwards; #1851 mutants use the suites' own env override so no tree file changed. Suites one at a time with `--maxWorkers=2`.
- Instrument faults: (1) the first vitest runs failed on missing modules (merged node_modules fixed it); (2) my first api-gateway whole run showed 8 failures in two ks1543 eslint-running files because the worktree had no `Dev/node_modules` for `@eslint/js`; I linked it and the rerun is 1326/1326, so those 8 are my set-up, not the PR; (3) my first Dockerfile fixture omitted four of the five scanned directories and the script died silently, which led to the second half of F-851-2; (4) the hook refused `$VAR` path forms for git write verbs, so those calls went through script files with literal paths.
- No git write verb was run in /Volumes/DevMASTER/!CODING. Every process I started has exited. Files live in this folder: `repo/`, `wt/`, `wt2/` (worktrees, safe to remove), `probes/` (tickets.txt, mut1842.txt, mut1851/, akto_probe.txt, suites.log, lint_tsc.txt).
