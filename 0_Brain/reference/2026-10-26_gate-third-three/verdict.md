# QA gate, tier 2 batch: three Secuura Platform K PRs (#1700 round 2 of 2, #1706, #1707)

Gate: Sonnet, findings-only. Nothing pushed, merged, commented or fixed; no `!CODING` checkout touched; no Docker; no stack. Linear read-only (KS-1649, KS-1714, KS-1636; comments first:50 sorted client-side; key sourced per command, never printed).

Develop readings (`git ls-remote origin`): start 07:26:59Z (18:27 AEDT) `fee13f25d574cdbac32601cbe0176f7b6622fa57`; end 07:45:08Z `1f2ec373bdade7298b5c29c4d144d0bddf92861f`. **Develop MOVED mid-session** (five merged PRs, #1701 to #1705). I ran the main work on the `fee13f25d574` merge and then re-ran the load-bearing legs on the new develop (section "Develop moved"). The three PR heads were identical at start and end (ls-remote in the same action as the fetch, and again at the end). No STOP on any PR.

## BLUF

| PR | Ticket | Head (verified, start = end) | Verdict | One line |
|---|---|---|---|---|
| #1700 | KS-1649 | `99720932a7f8abbdedcc999c0337113484ee691f` | GO WITH NOTES | Both round-1 Majors are CLOSED: 3,000 is now stated as the default with bounds 1 to 10,000 and pre-change keys at 1,000, and "on every response" is gone. Red/green re-run: 10 cells green, round-1 text turns 8 red, 7 further mutants each caught by name. Minor: "keys minted before that change" has no antecedent a portal reader can resolve. |
| #1706 | KS-1714 | `2c2aadbdccb2a84f662a151e2e3f66c74143b9ec` | GO WITH NOTES | Rebuilt fake-`cp`: develop rc 0, head rc 1 in BOTH suites after a failed restore, stash kept with the sentinel, clean runs rc 0 with 28/0 and 17/0 unchanged, bash 3.2.57. Note: no committed cell holds the new behaviour; it is proven only by an instrument that lives in the builder's evidence folder. |
| #1707 | KS-1636 | `b2afedf42a2e1415cf36dc7faa2f203fc26b491b` | GO | Census over the three files 3 to 0, twin 2 to 2, nonsense token 0 to 0; nothing outside the three files changed; ks781 diff is comment-only (non-comment lines hash-identical); packages/shared 1031 tests same set before and after. |

**Round-2 closure for the #1700 class (cap bookkeeping):** instance R-1 (3,000 stated as a fixed fact) CLOSED; instance R-2 ("on every response") CLOSED. Nothing remains open from round 1. One new Minor (M-1 below) and Notes; if Wednesday or Kam rates M-1 a Major, this round would read as NO GO with that single instance remaining, and per the cap it would ship as ticketed residue, not a round 3. My severity is Minor (reason below).

**Merge order I recommend:** #1707, then #1706, then #1700. The three touch disjoint files (pairwise overlap of changed files: 0), `git merge-tree --write-tree` against both `fee13f25d574` and the new develop `1f2ec373bdad` returns rc 0 for all three, and real `git merge` into each (rc 0, three-parent-word merge commit) was tested. The order is only a risk ordering: #1707 is docs plus one comment, #1706 is test scaffolding, #1700 goes last so that, if Wednesday wants M-1 reworded first, nothing else waits on it.

---

## #1700 KS-1649, round 2 of 2: `99720932a7f8`: GO WITH NOTES

Round 1 report: `/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-10-26_gate-r2-nine/verdict.md` (head `4f951814deb3`, NO GO, R-1 and R-2 Majors). The head now contains develop `fee13f25d574` (merge-base of head and that develop is `fee13f25d574` itself), so the head tree IS the merged tree for that develop. Builder's round-2 evidence folder (Seat R 2nd): **not on disk** at this time (`5_Project_History/` has only `2026-10-26_seatR-1st`, which predates round 2), so I could not read the builder's own red/green numbers and re-derived everything; the "8 to 10 cells, 4 mutants" figures below are mine.

### FOUND

The changed cell, `developer-portal.html:564` (diff of head vs `fee13f25d574`: that line plus one new test file, 84 lines):

> `<td>1,000 req/hour by default; Platform S connector keys are minted at 3,000 req/hour by default (an operator can set it between 1 and 10,000; keys minted before that change keep 1,000 until rotated)</td>`
> `<code>X-RateLimit-Limit</code> (the key's ceiling; sent on responses the rate limiter handles), <code>X-RateLimit-Remaining</code>, <code>X-RateLimit-Reset</code>`

Each sentence against the code, quoted in the same read (`services/api-gateway/src/routes/platform.ts`, `middleware/rateLimitEnforce.ts` at head):

| Sentence in the portal | Code line, quoted | Reads as |
|---|---|---|
| "3,000 req/hour **by default**" | `platform.ts:156` `const CONNECTOR_RATE_LIMIT_DEFAULT = 3000;` and `:192` `if (raw === undefined \|\| raw.trim() === '') return CONNECTOR_RATE_LIMIT_DEFAULT;` | TRUE, and it says default. R-1 part (a) CLOSED. |
| "an operator can set it between 1 and 10,000" | `:158` `const CONNECTOR_RATE_LIMIT_MIN = 1;` `:159` `const CONNECTOR_RATE_LIMIT_MAX = 10000;` `:190` `raw: string \| undefined = process.env.PLATFORM_S_CONNECTOR_RATE_LIMIT,` `:195` `if (!Number.isInteger(n) \|\| n < CONNECTOR_RATE_LIMIT_MIN \|\| n > CONNECTOR_RATE_LIMIT_MAX) {` ... `:202` `return CONNECTOR_RATE_LIMIT_DEFAULT;` | TRUE: whole numbers 1..10,000 are honoured; anything else falls back to the default (the sentence does not claim otherwise). R-1 part (b) CLOSED. |
| "keys minted before that change keep 1,000 until rotated" | `:142` `// hour, tunable by env; new keys only", with the detail "existing keys keep` / `:143` `// 1,000 until rotated".` and `:146-148` "This value travels on the key MINT ... which inserts a row and never updates one" | TRUE for keys minted before KS-1195. See M-1: "that change" is ambiguous. |
| "1,000 req/hour by default" (per key) | `services/security/src/index.ts:666` (read in round 1) `.default(1000)` | unchanged, TRUE for a key minted without `rateLimit`. |
| "X-RateLimit-Limit (the key's ceiling; sent on responses the rate limiter handles)" | `rateLimitEnforce.ts:289` `res.setHeader('X-RateLimit-Limit', limit.toString());` inside `if (outcome) {` (`:284`); `:275` `logger.error('[rateLimit] in-memory fallback ALSO failed — request allowed unlimited', {` then `:279` `outcome = null;`; `:297-300` `} catch (writeErr) {` ... `logger.error('[rateLimit] could not write the rate-limit headers or the 429 — request allowed unlimited', {`; `:159` `if (!user \|\| !MACHINE_AUTH_METHODS.has(user.authMethod)) {` then `next(); return;` | TRUE. The header is sent only when the limiter produced an outcome and the write did not throw; the sentence says exactly that, and "on every response" is gone. R-2 CLOSED. |

MEASURED AT RUNTIME for every test claim below; the text-versus-code legs above are READ ONLY (no gateway stood up, no key minted, no response header observed; same limit as round 1).

**Findings**
- **M-1 (Minor): the antecedent of "that change" is unresolvable for a portal reader, and its natural reading is wrong.** Oracle: Comprehensibility/Claims (FEW HICCUPPS: Purpose, World). In `(an operator can set it between 1 and 10,000; keys minted before that change keep 1,000 until rotated)` the nearest antecedent is the operator setting it. Read that way it is false: a key minted at 3,000 and then followed by an operator change stays at 3,000 (`:146-148`, the value is fixed at mint), not 1,000. The true reading (before KS-1195 raised the connector default) names an event the portal never mentions. Severity Minor: the figure is correct under its intended reading and no developer would be misled about the current default, but it is the same shape as round 1's R-1 (a number stated without the condition that makes it true). Fix-shape for the owner to author: "...; keys minted before the 3,000 default shipped keep 1,000 until rotated, and a key keeps the ceiling it was minted with". Regression test: assert the row does not contain `before that change` (or contains the word "minted" next to "keeps" with a stated event). EVIDENCE CLASS: READ ONLY (text against `platform.ts:142-148`).
- **N-1 (Note, pre-existing, outside the diff): the same file contradicts itself.** `developer-portal.html:262` `<p>Default: 100 requests per minute per API key. Contact us to increase limits for production use.</p>` sits under the quickstart `<h3>Rate Limits</h3>` (`:261`), while `:564` now says 1,000 req/hour by default. The runtime fallback for a key with no allowance is indeed 100/60 s (`rateLimitEnforce.ts:66-67` `DEFAULT_MACHINE_RATE_LIMIT = 100`, `DEFAULT_MACHINE_RATE_WINDOW = 60`; `middleware/auth.ts:248-249` `data.rateLimit || 100`), so neither line is the whole story. Unchanged by this PR and was true before it. KS-1649 is the natural home if Wednesday wants it. EVIDENCE CLASS: READ ONLY.
- **N-2 (Note): the header is documented as the key's ceiling, but for a machine caller whose `user.rateLimit` is falsy the limiter reports the fallback**: `rateLimitEnforce.ts:183` `const limit = user.rateLimit \|\| DEFAULT_MACHINE_RATE_LIMIT;` and sends that as `X-RateLimit-Limit` (`:289`). Reachable only by a misconfigured key (the code warns at `:177-182`). The portal sentence is true for every configured key. READ ONLY.
- **N-3 (Note): the qualifier "(...sent on responses the rate limiter handles)" is attached to `X-RateLimit-Limit` only, while `X-RateLimit-Remaining` and `-Reset` are written in the same three lines (`:289-291`) under the same conditions.** Not false; slightly under-stated. READ ONLY.
- **N-4 (Note): a code comment now disagrees with the code and the portal**: `rateLimitEnforce.ts:288` `// Set rate limit headers on ALL responses`, directly above the `if (outcome)` guard and the two paths that omit them. Not in the diff; a later reader could re-introduce the round-1 text from it. READ ONLY.
- **N-5 (Carried, round 1 N-2)**: OAuth apps have no `rate_limit` column, so the shared "1,000 by default" row is loose for them. Unchanged, not in this diff.
- **Ticket check (KS-1649 read whole, comments first:50):** the ticket body itself says `X-RateLimit-Limit` "already reports the actual ceiling on every response" (this is where round 1's "on every response" came from). The ticket's "Timing" paragraph says make the change only after #1613 lands; #1613's code (`platform.ts:156`) is in develop at both readings, so the timing precondition holds.

### TESTED / HOW (with controls)

FAIL conditions stated before each arm: a cell is a detection only if it fails for the named cell on the mutated tree and passes on the pristine head.
1. **Green arm.** The new file alone on the head tree, vitest run with `--root` (the file reads by `__dirname`, so cwd does not matter): **10 passed, 0 failed** (R1 to R6, C1, C2, D1, D2).
2. **Red arm, round-1 text.** The `developer-portal.html` from `4f951814deb3` dropped into the head tree (landed: differs from head; restored with `git checkout --`, clean status asserted): **8 failed, 2 passed**. Failing: R1, R2, R3, R4, R5, R6, D1, D2. Passing: the two controls C1, C2. So the new test is RED on exactly the round-1 defect and its controls hold.
3. **Seven further mutants, each with an anchor-count assertion before and a landed assertion after, restore + clean status after each:**

| Mutant | Cells that went red |
|---|---|
| B: "3,000 req/hour by default" to "3,000 req/hour" (the round-1 fixed-fact error) | R1, R2, D1 (3 failed) |
| C: qualifier replaced by "on every response" | R5, R6 |
| H: qualifier replaced by "always sent" | R5, R6 |
| D: `CONNECTOR_RATE_LIMIT_DEFAULT` 3000 to 2500 in `platform.ts` | D1 |
| E: `CONNECTOR_RATE_LIMIT_MAX` 10000 to 20000 in `platform.ts` | D2 |
| F: html "between 1 and 10,000" to "between 1 and 100,000" | R3, D2 |
| G: html "keep 1,000 until rotated" to "keep 1,000" | R4 |

   The unmutated control before the first mutant and after the last: both 10 passed.
4. **Suite counts.** Full `services/api-gateway`, run with cwd = the service dir, json reporter, by-name set arithmetic: develop `fee13f25d574` 1176 tests passed 0 failed, head 1186 passed 0 failed; 0 vanished, 10 new (exactly the ten KS-1649 cells), 0 regressed. Re-run on the NEW develop `1f2ec373bdad` merged with the head (real `git merge`, rc 0): 1190 passed, 0 failed.
5. **Blind spot of the new tests (so they are not over-credited):** they pin prose substrings. They do not catch M-1 (wording that is true on one reading), and R6 forbids `every response|all responses|always` anywhere in the row, which would also trip on an unrelated true use of "always" (fail-loud, acceptable).

---

## #1706 KS-1714: `2c2aadbdccb2`: GO WITH NOTES

### FOUND
- Diff vs merge-base `28e2d27de337` (read whole): two files, +16/-2. In each suite's `restore()`: `local rc=$?` as the first statement, and the failed-restore branch's bare `return` becomes `if [ "$rc" -eq 0 ]; then exit 1; fi; exit "$rc"` (`pre_suite.test.sh:127-143`, `quarantine_call_sites.test.sh:95-113` at head). Message and kept stash are unchanged. Matches the ticket's ask (both suites exit non-zero after a failed restore) and its note that `return` inside an EXIT trap leaves the status as it was. No product code.
- Ticket read whole (KS-1714: body is the DA3 round-1 measurement; builder comment 06:59Z). Builder's claims challenged, not trusted.
- **N-1 (Note): the behaviour is held by no committed cell.** The PR changes two test scripts and adds no test of them; the only proof is the fake-`cp` instrument kept under `5_Project_History/2026-10-26_seatU-1st/evidence/ks1714/instrument/`. A later edit that puts `return` back would go green everywhere. Fix-shape (owner authors): a third small suite that runs each of the two suites against a copied `generated/` with a fake `cp` first on PATH and asserts rc != 0 plus the kept stash (the instrument below is the template). EVIDENCE CLASS: READ ONLY for "no committed cell" (census of the diff: two files).
- **N-2 (Note, named by the builder, confirmed unchanged): the `snapshot_ok != 1` branch still `return`s** (`pre_suite.test.sh:129-135`, `quarantine_call_sites.test.sh:98-104` `return`). Same shape as the defect, outside the ticket; builder says it is named in the PR. Not tested by me (I did not fake a failing snapshot copy). KS-1735 (third copy in `support/generated_guard.sh`) is the builder's filing; not read or tested by me.
- **N-3 (Note, measured, favourable): the `$?`-first placement matters and is right.** See mutant LateRc below: in `quarantine_call_sites.test.sh` the line before it is `kill ... ; wait "$STUB_PID"`, and `wait` on a killed stub returns 143, so reading `$?` after it turns a clean suite with a failed restore into exit 143, not 1.

### TESTED / HOW
I rebuilt the instrument from nothing (`.../scratch/g1706/fakebin/cp`, `drive.sh`, `matrix.sh`): a `cp` placed first on PATH that exits 1 only when its last argument ends in `/generated/` and otherwise `exec /bin/cp "$@"`. **Controls, run on the instrument itself:** copying a file to an ordinary directory: rc 0 and the file arrived; copying to `.../generated/`: rc 1, nothing arrived; the suite's own form `cp -R src/. dest/generated/`: rc 1, nothing arrived. Every fake run also records that the fake was actually called with a `/generated/` destination (`fakecalls_to_generated=1`), so a run where the fake never fired would show 0 and be discarded. Sentinel file seeded in `systemTest/fixtures/generated` of MY worktree copy before every run (the real `generated/` of any checkout was never touched). Shell: `/bin/bash` 3.2.57(1) on this host, node v26.8.1. Loads at start 4 to 6.

FAIL conditions: head must exit non-zero after the FAILED message with the stash kept and containing the sentinel; develop must exit 0 there (else the instrument cannot see the defect); clean runs must exit 0 with the unchanged counts.

| Tree | Suite | no fake | fake `cp` (failed restore) |
|---|---|---|---|
| develop `fee13f25d574` | pre_suite | rc 0, 28/0, sentinel restored | **rc 0** (the defect), FAILED msg, stash kept with sentinel, `generated/` empty |
| develop | quarantine_call_sites | rc 0, 17/0 | **rc 0** (the defect), same |
| head `2c2aadbdc` | pre_suite | rc 0, 28/0 | **rc 1**, FAILED msg, stash kept with sentinel, `generated/` empty |
| head | quarantine_call_sites | rc 0, 17/0 | **rc 1**, same |
| head merged into `fee13f25d574` (`87fe5a94c`) | pre_suite / quarantine | rc 0, 28/0 / 17/0 | rc 1 / rc 1, both with stash+sentinel |
| head merged into NEW develop `1f2ec373bdad` (`d1ca39cb9`) | pre_suite / quarantine | rc 0, 28/0 / 17/0 | rc 1 / rc 1, both with stash+sentinel |

- Pass counts unchanged on clean and failed-restore runs: pre_suite 28 passed 0 failed, quarantine 17 passed 0 failed, on develop, head and both merged trees (so the 16 added lines changed no cell).
- **SIGTERM mid-run** (suite killed after 3 s, then 4 s settle): rc **143** on develop and on head, both suites, with and without the fake (8 runs). With the fake the FAILED message appears and rc stays 143 on head. This confirms the "keeps the suite's own status" half, but note it is NOT discriminating (develop gives 143 too, since `return` leaves the status); it only shows the fix does not force 1 over a signal.
- **Mutant LateRc** (moved `local rc=$?` below the `kill`/`wait` line in the head's `quarantine_call_sites.test.sh`; anchor count 1, landed asserted, restored by `git checkout --`, clean status asserted): fake run exits **143** instead of 1, 17 passed. So the first-line read is load-bearing in that suite; the PR has it right.
- Not just one reading: I did not re-derive "the runner scores it FAILED" through `scripts/run-shell-suites.sh` (see NOT TESTED).
- Kept stashes from my fake runs were moved, not deleted, into `.../scratch/_quarantine_20261026/kept_stashes/` (14 dirs).

---

## #1707 KS-1636: `b2afedf42a2e`: GO

### FOUND
- Diff vs merge-base `28e2d27de337` (read whole): three files, +5/-6. `CLI-AGENT-INSTRUCTIONS.md:420` deleted (`- GET /api/documents/:id/verify`); `docs/TEST_IMPROVEMENTS.md:67` deleted (`- ✅ /api/documents/:id/verify - Document verification`), the certifications twin on the following line stays; `ks781-p3-3-body-parser-order.test.ts` comment only. Matches the ticket's table row for row. Ticket and builder comment read whole.
- The successor is still listed where the PR says it is: `CLI-AGENT-INSTRUCTIONS.md:422` `- POST /api/verification/verify`; source: `services/originate/src/routes/verification.ts:841` `'/verify',` under `verificationRouter.post(`, proxied by `services/api-gateway/src/routes/proxy.ts` `router.use('/api/verification', proxy('originate', ...))` (READ ONLY; not called).
- The new comment's "5 routes" is correct: `grep -c 'router.post(.*mockBodyParser'` over `services/api-gateway/src/routes/verification.ts` on the head tree returns 5 (`:332` certifications verify, `:413`, `:478`, `:613`, `:660` workflow routes). Same 5 on the merged tree with NEW develop.
- **N-1 (Note, outside the ticket): other live comments still name the retired route**, e.g. `services/api-gateway/src/routes/verification.ts:115`, `:297`, `:402`. They are in files other tickets own (KS-1628/#1589); the ticket's census explicitly scoped to the three. Repo-wide count of lines naming `documents/:id/verify`: 26 in 20 files before, 23 in 17 after (exactly the 3 lines this PR removes). READ ONLY.

### TESTED / HOW
- **Census** (`git show <ref>:<file> | grep -c -F`, summed over exactly the three files; base `28e2d27de337` vs head): `documents/:id/verify` **3 to 0**. Positive control, the certifications twin `certifications/:id/verify`: **2 to 2** (stays). Nonsense token `documents/:id/ks1628-never-existed`: **0 to 0**. Extra control, `verification/verify` (the successor): 5 to 5. So the instrument discriminates (hits where expected, zero where nothing exists, twin untouched).
- **Dated records byte-identical:** `git diff --name-status base head` lists exactly the three files; `git diff --stat` excluding them is empty (0 lines). Repo-wide the twin count is 18 and 18.
- **ks781 comment-only:** the only changed lines are the doc-comment lines (` * parser at :535...` etc.). With every comment-leading line (`*`, `/*`, `//`) stripped, the file's `shasum` is identical before and after (`28bda807286e` both): no code or assertion line changed. The suite proves it independently below (the ks781 file: 242 cells passed on both).
- **packages/shared suite count unchanged:** run with cwd = `packages/shared` (json reporter, set arithmetic by test name):
  - Base `28e2d27de337` vs head: **1031 tests, 1031 tests**; failing on base: `parameteriseMintPolicy (Phase 2) returns different policy IDs for different seed` (load timeout class) and `verifyMessageSignature ... KS-278 accepts a valid wallet signature`; on head only the wallet-signature one. 0 vanished, 0 new, 0 regressed, 1 "fixed" (the threadToken timeout, which passed on head at load1 about 4: a load flake, not caused by the PR: the PR touches no code).
  - Develop `fee13f25d574` vs develop+head: **1035 vs 1035**, 1 failed on both (wallet-signature), 0 vanished/new/regressed/fixed. New develop `1f2ec373bdad` + head: 1035, the same 1 failure.
  - The wallet-signature failure is pre-existing on base, develop and head (KS-1727 per round 1).

---

## Develop moved (07:26:59Z to 07:45:08Z)

`fee13f25d574` to `1f2ec373bdad`: #1701, #1702, #1703, #1704, #1705 merged (files changed: 20, none of `systemTest/`, `developer-portal.html`, `platform.ts`, `rateLimitEnforce.ts`, `CLI-AGENT-INSTRUCTIONS.md`, `TEST_IMPROVEMENTS.md`, or the ks781 test). Re-run on the new develop merged with each head (three fresh worktrees, real `git merge`, rc 0 each, `git merge-tree` rc 0 each): api-gateway full suite 1190/0 (#1700), packages/shared 1035 with only the pre-existing wallet-signature red (#1707), fake-`cp` matrix both suites (#1706, results in the table). A GO is a statement about the head SHA named in the table; if any head moves, it expires.

## NOT TESTED (first-class)

- #1700: no gateway stood up, no connector key minted via `register-connector`, no response header observed; every text-versus-code row is READ ONLY. `PLATFORM_S_CONNECTOR_RATE_LIMIT` was exercised only through `resolveConnectorRateLimit` in the builder's unit cells and my mutants, not in a deployed environment. The PR body and GitHub check-runs were not read (`gh` not logged in); I judged the head's published text.
- #1700: builder's round-2 evidence folder was not on disk; I could not compare my 10/8/7 numbers with the builder's "8 to 10 cells, 4 mutants".
- #1706: only bash 3.2.57 (the host's `/bin/bash`); no bash 5. Not run through `scripts/run-shell-suites.sh` (leg 14), so "the runner scores a failed restore as FAILED" is the builder's claim, not mine. The `snapshot_ok != 1` branch was not driven. The real cause of a failed copy (full disk, permissions) was not reproduced; the fake stands in. The real `generated/` of a checked-out project was never touched (my own worktree copies only). KS-1735 and `support/generated_guard.sh` were not examined.
- #1707: the three docs' other content was not re-read for staleness beyond the retired route; `RUNBOOK.md:263` and the other holders of the retired path (dated records, e2e callers, gateway comments) are other tickets' scope and were not edited or tested. The successor route was read, not called.
- No pre-push hook run, no preflight legs 3, 4, 8, no platform suites, no Docker, no push.
- No Linear or GitHub write of any kind.

## My own instrument errors (reported in the open)

1. **First packages/shared run was invalid.** I ran vitest with `--root <dir>` from a different cwd, so seven repo-walking guard files (including the very ks781 file this PR edits) failed at collection with "could not locate the Dev root from /Volumes/DevMASTER/WEDNESDAY", giving 619/623 tests instead of 1031/1035. I noticed the count disagreed with the builder's 1031 and the prior gate's, read the collection errors, and re-ran all six suites with cwd = the package dir (`subprocess` `cwd=`, no shell `cd`). Every shared and api-gateway figure in this report is from the second set; the invalid set was never used for a verdict. The #1700 targeted file does not depend on cwd (it uses `__dirname`), and I re-ran the full api-gateway suite under the correct cwd anyway.
2. **A `sed -i` rename of my own comparison script failed on BSD sed** (extra characters at end of command); I noticed the output still named the old files, and redid it with a Python replace before reading any number.
3. **zsh/hook slips, no effect on results:** a `echo ======` separator and a `git -C $VAR` write verb were refused by the fleet hooks; write steps then ran from script files with absolute literal paths.
4. **Develop moved under me.** I did not re-pin the develop ref during the main work; I caught it at the end ls-remote and re-ran the legs on the new develop (section above). The main matrix for #1706 and the counts for #1700/#1707 were originally on `fee13f25d574`.
5. **TERM cell was non-discriminating** (develop also gives 143); I report it as a "does not force 1" check only, not as a detection.
6. No finding of mine was retracted.

## Left on disk (not deleted)

`/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/cache/work/gate_third_three_20261026/`: clone `repo` (shared with `.../cache/src`, refs `refs/gate/*` added there by my fetch), worktrees `dev`, `base28`, `h1700`, `h1706`, `h1707`, `m1706`, `m1707`, `n1700`, `n1706`, `n1707` (node_modules cloned with `cp -c -R` from the earlier gate's `dev`), and `scratch/` (logs, json reports, `g1706/` instrument, `_quarantine_20261026/kept_stashes/` with 14 moved stash dirs). Node_modules copies are APFS clones; the dir can be quarantined at wrap.
