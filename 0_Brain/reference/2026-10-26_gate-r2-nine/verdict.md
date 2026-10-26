# QA gate, tier 2 batch, round 1 of 2 under the cap: nine Secuura Platform K PRs from Seat R (Spark patches)

Gate: Sonnet, findings-only. Nothing pushed, merged, commented or fixed; no `!CODING` checkout touched; no Docker run.
Develop read: `28e2d27de33734c3ad7d2909c3019a9f530d4629` (`git ls-remote origin`, 05:29:24Z start, 06:37:36Z end). All ten refs identical at start and end (diff of the two ls-remote outputs is empty), and every PR head equals the READY mail's head. No STOP on any PR.

## BLUF

| PR | Ticket | Head (verified) | Verdict | One line |
|---|---|---|---|---|
| #1689 | KS-1716 | `b3a063dd33b95bcea382aa1ab1ea4a73a743b482` | GO WITH NOTES | Fix proven through the REAL pre-push hook (red on develop, green on head, malformed refused, clean passes). Minor: the same script has a sibling `printf \| grep -qxF` at line 874 with the same defect, shown through the real hook as a wrong "(NOT in this push)" label. |
| #1692 | KS-1560 | `6bb63146affd0079020924a94691e1208dbd39f8` | GO WITH NOTES | Behaviour proven on a simulated jq-not-in-/usr/bin host (develop 4 passed 1 failed, head 5/0). Minor: the census oracle is a substring, blind to a comment (mutant B survives). |
| #1693 | KS-1391 | `0b880d125964e3cece4bb29c431297e7b6ead446` | GO | `npm test -w frontend/issuer`: rc 1 Missing script on develop, rc 0 with 15 passed on head; planted failing spec turns it red. Item 1 of the ticket only. |
| #1694 | KS-1289 | `048b9d5fa48ba05712bcee73dbc9831655d58c8f` | GO WITH NOTES | Static-only: no Dockerfile or build step I could find needs a path the new line excludes. Docker semantics and the ticket's own rebuild measurement are NOT done. The 3 reported failures are pre-existing / load, not the PR. |
| #1695 | KS-1513 | `716e26290155975a4b97fda68cf597413c0e8e98` | GO WITH NOTES | 22/0 with a SKIP line without install; 38/38 with install, 0 SKIP. Minor: the suite's own verdict line does not carry the skipped denominator. |
| #1697 | KS-1527 | `6e45c854a46fe8cb406d8798cc0406fe5fc87bb0` | GO | Both mutants caught by name with no compiler; unmutated control clean; sibling 38 to 39 with install. |
| #1698 | KS-1548 | `073289640d6367f0dff74e7a41b7999dcd2e2046` | GO | 2x2 reproduced exactly: the old test is blind to the mutated guard (18/18), the new test is not (1 failed). Covers m2 only; m1, m3 and the nit stay open. |
| #1699 | KS-1524 | `c189e242a37791005b1cff60ab4860d6df6332f4` | GO | 2x2 reproduced for both `err.stack` and `String(err)` mutants. Covers (b) only; (a), (c), (d), (e) stay open. |
| #1700 | KS-1649 | `4f951814deb376a92024e05100b30a752636c2cc` | NO GO | Published text is unsafe as worded: "are minted at 3,000" reads as a fixed fact (code: default, env-tunable 1..10000, existing keys stay 1,000) and "on every response" has code-proven exceptions. Two Majors, cheap fix. |

Counts: GO x4 (#1693, #1697, #1698, #1699), GO WITH NOTES x4 (#1689, #1692, #1694, #1695), NO GO x1 (#1700). The "published portal text" class has had no earlier NO GO, so this is its round 1 of 2.

Merge order I recommend (all pairwise conflict-free; the only shared file is #1695/#1697):
1. #1698, #1699 (test-only, mechanism measured), 2. #1692, #1693, 3. #1695 then #1697 (see below), 4. #1689, 5. #1694 (last of the shippable ones, because it changes the build context of every image and carries the only unmeasured runtime semantics), 6. #1700 only after its text is fixed and re-gated on the new head.
#1698 and #1699 are one PR behind develop (#1690); their product file `routes/platform.ts` is byte-identical to develop's (empty `git diff --stat`), and I ran their cells as develop plus the PR's test file, which is the merge result.

Merge-tree, `git merge-tree --write-tree refs/gate/develop refs/gate/pr<n>`: all nine rc 0, no conflict. #1695 and #1697 merged in BOTH orders (real `git merge`, rc 0 each): the two resulting trees are byte-identical (`521a71b75228ccd22c398c875d5b13617ecc7640`), no conflict markers. Order does not change the result; I recommend #1695 first because it removes the 9 environment false-reds that make #1697's no-install tally hard to read.

## Method notes that apply to all nine

- Runner: `spark_gate.sh` is pytest-only (`pyproject.toml` lookup, junit), so it does not fit any of these PRs (shell suites, vitest, a script, an html file). I ran every suite directly: `bash <suite>` for shell, `npx vitest run` for vitest. Said once here, not per PR.
- Environment: my own worktrees under `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/cache/work/gate_r2_nine_20261026/` (`dev` = develop with `npm ci --ignore-scripts` + `npm run build --workspace=packages/shared`, `dist/index.js` asserted; `pr<n>` = each head; `combA`/`combB` = the two merge orders). Substrate source = the repo's own lockfile (`npm ci`), same as the hook and the preflight use.
- Every mutation was preceded by an anchor-count assertion and followed by a "mutant landed" read (counts printed in the logs), and every restore was `git checkout --` plus a clean `status`; pristine copies were kept.
- Load: the vitest and install runs started at load1 8.0 to 8.8 (my `waitload` gate waited for under 9); load1 drifted up to 18 during the session from the other seats. The shell-suite, hook and sandbox runs were light and ran at load 12 to 18. I never ran two heavy things at once.
- Evidence class: everything below is MEASURED AT RUNTIME unless marked READ ONLY.
- Logs: `.../gate_r2_nine_20261026/scratch/` (`o*.txt`, `full_*.txt`, `chain1.log` to `chain3.log`). Scripts: the session scratchpad.

---

## #1689 KS-1716 `b3a063dd33b9`: GO WITH NOTES

**FOUND**
- Diff vs merge-base `28dac5c12ba5` (read whole): one product line, `systemTest/scripts/check-package-format.sh:730`, `grep -q "^systemTest/${p}/"` becomes `grep "^systemTest/${p}/" > /dev/null`, plus a new 7-cell suite. Matches the ticket's fix shape (the form it measured).
- Minor M-1 (the class, same file, same trigger): `check-package-format.sh:874`, `printf '%s\n' "$changed_paths" | grep -qxF "$full"`, is the same early-exit reader under the same `set -uo pipefail` (`:190`). It is inside the `| while read` that labels a red file "(in this push)" or "(NOT in this push - inherited red)". On a list over 64 KiB the pipeline fails and a file that IS in the push is labelled "NOT in this push - inherited red", the exact blame misattribution KS-998 introduced `-qxF` to prevent. The gate decision (rc 1) is still right; only the label lies. ORACLE: Product/Purpose (the line's own comment at `:869-872` says the label "is a literal statement about this push"). Fix-shape: same read-to-EOF form, `grep -xF "$full" > /dev/null`. Regression test to add: the existing fixture with `abc` red and the big list; assert the output contains `(in this push)`. Not in the ticket's literal ask (the ticket names line 730), so this is a Minor follow-up, not a blocker. No other `| grep -q` on a list exists in the script or in `.githooks/pre-push` (`grep -i` census, hook has no `pipefail` and no `grep -q`).
- Note: this push ran no preflight leg, as the PR says. Real hook on the real PR range (merge-base `28dac5c12ba5`..head, two systemTest paths, neither under a package dir): `git hook run pre-push` rc 0, empty output. The fix is therefore proven only by the legs below, not by the push itself.

**TESTED / HOW (controls)**
1. New suite on head: 7 passed 0 failed. On develop's gate script (`PACKAGE_FORMAT_GATE_SH` aimed at `git show develop:...` copy, `cmp` rc 1 proves the two scripts differ; the only diff is line 730): 4 passed 3 failed, exactly the builder's 3 (`aaa first`, `red first`, `zzz only`). Controls inside the suite: cell 0 asserts the list is over 65536 bytes, cell 3 small list green on both.
2. Siblings before/after (base = develop `systemTest/__tests__` via `git archive`): ks998_format_gate_stdin_isolated 9/0 -> 9/0, ks998_format_gate_push_label_is_literal 8/0 -> 8/0, package_format_gate 435/0 -> 435/0.
3. THE REAL HOOK PATH, `.githooks/pre-push` byte-identical (`cmp` rc 0) on develop and head, driven by `git -c core.hooksPath=.githooks hook run --to-stdin <ref line> pre-push -- origin <url>` in scratch clones. The hook computes the changed set at `pre-push:~255-262` (`all_changed`), finds the gate at `:310` (`_fmt_gate`), and pipes the list into it at `:365` (`printf '%s\n' "$all_changed" | FORMAT_GATE_TREE=... bash "$_fmt_gate"`). Synthetic commit: `systemTest/akto/src/a.ts` (sorts first) plus 2200 files under a non-package dir `systemTest/zzzbulk/gen/` so the path list is 187,025 bytes; `origin/develop` ref set to the base. `akto` node_modules symlinked read-only from the main checkout (no write there).
   - H3 develop script, big list, malformed akto file: **hook rc 0**, only output `line 730: printf: write error: Broken pipe`. The malformed package was NEVER judged: the defect reproduced through the real hook.
   - H1 head, big list, malformed: **hook rc 1**, `systemTest/akto - format:check FAILED`, `1 package(s) checked, 0 skipped, 1 failed`. Planted control proves refusal. (It also printed `line 874: printf: write error: Broken pipe` and the wrong label: M-1 through the real hook.)
   - H2 head, big list, clean akto file: rc 0, `1 package(s) checked, 0 skipped, 0 failed`.
   - H4/H5 head, small list, malformed / clean: rc 1 with label "(in this push)" / rc 0 (the small-list control for both directions).
4. Mutant of M-1 control: the small list prints "(in this push)" (control), the big list prints "(NOT in this push)" for the same file (`scratch/o1689b_*.txt`).

## #1692 KS-1560 `6bb63146affd`: GO WITH NOTES

**FOUND**
- Diff read whole: `tenant_isolation_stderr_own_file.test.sh` resolves `JQ_BIN` once (`command -v jq`) and `ln -sf "$JQ_BIN" "$root/bin/jq"` into each fixture's stub dir; new census suite `ks1560_private_path_suites_link_jq.test.sh`. Covers M1 of the ticket. M2 (ks1347 probe brittleness) and M3 are not in this PR and the ticket stays open.
- Minor M-2: the census decides "links jq" with `grep -qF 'bin/jq' "$f"` (substring anywhere in the file). Mutant B below: delete the real `ln -sf` line, leave the words `bin/jq` in a comment, and the census stays GREEN. The census is the instrument that is supposed to catch a fifth copy. Fix-shape: match the link statement (`ln .*jq.* "\$root/bin/jq"`), or better, run each census suite's subject under a jq-less PATH. Regression test: mutant B must go red.
- Census completeness (counted from the cause, not from the census's own list): my independent predicate (any `*.test.sh` mentioning `\bjq\b` AND a PATH ending `:/usr/bin:/bin`, any variable name) over the 72 suites returns the same four suites (three trivy + tenant_isolation). No fifth.

**TESTED / HOW**
- New suite on head 3 passed; copied onto develop's directory it goes 2 passed 1 failed naming `tenant_isolation_stderr_own_file.test.sh` (RED on the defect). Siblings: tenant_isolation 5/0 on develop and 5/0 on head.
- Behaviour, not just the census: a simulated host whose jq is not in /usr/bin (`sandbox-exec` denying exec and read of `/usr/bin/jq`, a re-signed copy of jq on the outer PATH; control: the copy runs in the sandbox rc 0, `/usr/bin/jq` is refused rc 71). tenant_isolation suite: **develop 4 passed 1 failed, head 5 passed 0 failed**.
- Mutant A (delete the `ln -sf` line, `bin/jq` count 0): census goes RED (2 passed 1 failed). Mutant B (as above plus a comment): census GREEN (M-2).

## #1693 KS-1391 `0b880d125964`: GO

**FOUND:** one line, `frontend/issuer/package.json` `"test": "vitest run"`, plus a 3-cell pin. Item 1 of the ticket's "Suggested shape" only; items 2 to 4 (posture for the other frontends, `--if-present`, `__mocks__`) stay open, so the ticket must not close on this PR. Note: the root `"test": "npm run test --workspaces"` (`package.json:17`) still fails for the five frontends without a script; unchanged by this PR and called out in the ticket.
**TESTED / HOW**
- `npm --prefix <Dev> run test -w frontend/issuer`: develop rc 1 `Missing script: "test"`; head rc 0, 3 files 15 tests passed. Issuer suite before (direct vitest on develop) 12 passed in 2 files; after 15 (+3).
- New file copied onto develop: R1 RED (`expected undefined to be 'vitest run'`), 1 failed 2 passed. Mutant `"test": "echo ok"` (landed, grep count 1): R1 RED `expected 'echo ok' to be 'vitest run'`. KS-1391 acceptance control: a planted failing spec in issuer's `src/__tests__` turns `npm test -w frontend/issuer` red (rc 1, `Test Files 1 failed | 3 passed`). Planted file moved to quarantine.
- Note: the pin asserts the string, not that the script reaches the specs; the rc/15-passed run above is what proves reachability.

## #1694 KS-1289 `048b9d5fa48b`: GO WITH NOTES

**FOUND**
- Diff: one line `Blockchain/Dev/.dockerignore` `**/__tests__` (after `tests`, before the `!connectors/whatsapp-bot` re-include, so last-match-wins ordering is preserved) plus a 4-cell pin. 745 tracked `__tests__` files under Blockchain/Dev at head (744 at base + the new test) leave the context: services 616, packages/shared 55, `scripts/__tests__` 71 `.sh`, `migrations/__tests__` 1, frontend/issuer 2.
- Note N-1, build-context enumeration (READ ONLY; Docker not run). 35 Dockerfiles tracked under Blockchain/Dev; compose builds 31 with `context: .` (docker-compose.yml, `context: .` x31) and 2 with their own subdir context (pgbouncer, nginx-gateway, unaffected). Also built from the same context: `deployment/azure/deploy.sh:409-411,464-466` and `deploy-all.sh:189-191` (`az acr build ... .`), `.github/workflows/security-scan.yml:303` (`CONTEXT=Blockchain/Dev`; Actions retired), `scripts/build-docker.sh:77,100`, `scripts/docker-build.sh:189`. Facts that make the exclusion safe: (1) no `COPY`/`ADD` source in any Dockerfile names a test, `__tests__`, spec or fixture path (260 COPY/ADD lines extracted and filtered; whole-directory copies are `services/<x>/`, `packages/shared/`, `frontend/shared/`, `connectors/whatsapp-bot/`); (2) no `package.json` `build/prebuild/postbuild/prepare/postinstall` script in any service, package, frontend or connector mentions test/`__tests__`; (3) no non-test source file mentions `__tests__`; (4) every service/package/frontend `tsconfig.json` already excludes `src/__tests__` (28 tsconfigs listed in the log), so `tsc` never read these files; billing's Dockerfile rewrites its own exclude (`services/billing/Dockerfile:52`) the same way; (5) `connectors/whatsapp-bot` has 0 tracked `__tests__` files; (6) no repo file other than the new test mentions `.dockerignore`. Image-side effect expected as ticketed: tests no longer ship in runtime images and the cache key stops depending on them.
- **Could not establish:** (a) BuildKit/classic-builder matching of `**/__tests__` against nested paths and the interaction with the later `!connectors/whatsapp-bot` negation (documented semantics, not measured; no Docker run by instruction); (b) the ticket's own acceptance, "rebuild after a shared-test-only change and show the rebuilt set shrinks", is NOT done (needs Docker); (c) `services/vc-issuer/.dockerignore` (a second tracked ignore file) is only honoured for a build whose context is that directory; compose uses the Dev root, so I treated it as unaffected, not measured; (d) `scripts/__tests__` and `migrations/__tests__` also leave the context; I found no COPY of those directories, but I did not read every `run-migrations.sh` consumer at image runtime (originate copies the single file `scripts/run-migrations.sh`, `services/originate/Dockerfile:47`).
- The three failures the builder reported: PRE-EXISTING / LOAD, not the PR. packages/shared full suite: merge-base `28dac5c12ba5`: 994 tests, **2 failed** (wallet-signature "accepts a valid wallet signature over the message", `expected false to be true`; threadToken "returns different policy IDs for different seeds", 60,785 ms timeout). Head: 998 tests (+4), **1 failed** (wallet-signature only). Develop `28e2d27de337`: 1031 tests, 1 failed (wallet-signature only). The ks879 timeout the builder saw did not reproduce on any of my three runs at load1 about 8. wallet-signature fails identically on base, develop and head (deterministic; KS-1727); the timeouts are load. Nothing is caused by this PR (it adds one file read and one `.dockerignore` line).

**TESTED / HOW:** new suite copied onto develop: R1 RED (`expected [ ...(39) ] to include '**/__tests__'`), 1 failed 3 passed; head 4 passed. Mutant (delete the line from head's `.dockerignore`, 0 matches after): R1 RED, 1 failed 3 passed; restored by `git checkout --`.

## #1695 KS-1513 `716e26290155`: GO WITH NOTES

**FOUND**
- Diff read whole: the real-checker block of `preflight_test_types_ratchet_leg.test.sh` is wrapped in `if bash scripts/preflight/deps-present.sh ...; have_install=yes; else ...; printf 'SKIP - workspace install absent ...'; fi`; the wiring cells above and the stub cells below stay outside it, exactly the scoping the ticket's own 2026-10-12 comment asked for. The `SKIP` line matches the runner's convention (`run-shell-suites.sh:369`, `^[[:space:]]*SKIP[[:space:]]*[-—]`); the runner scores a suite with rc 0 plus that line as one counted skip, and rc != 0 takes precedence (`:365-368`), so a failing stub or wiring cell is still a FAIL.
- Minor M-3: with no install the suite's own last line reads `22 passed, 0 failed` with the SKIP line far above; the denominator (the 9 real-checker cells that were not run) is not on the verdict line. Standing line "a verdict line prints the ratio". Mitigated because the runner counts the whole suite as skipped, so the PR-evidence line does carry it. Fix-shape: print `N passed, 0 failed, M real-checker cells not run` when `have_install=no`.
- Note: ks1513's cell 5 matches the substring `a failing leg-16 script FAILS the run` of a cell title; a retitle breaks it loudly (control line shows 1), acceptable.

**TESTED / HOW**
- No install (these worktrees): sibling suite develop 25 passed 9 failed; head 22 passed 0 failed with 1 SKIP line. New ks1513 suite: head 5/0; aimed at develop's sibling (`RATCHET_LEG_SUITE_SH`) 2 passed 3 failed (cells 1 to 3 RED, stub/wiring controls still ok).
- With a real install (`dev` worktree, `deps-present.sh` OK): sibling on develop 38/0, on head 38/0, SKIP lines 0 (no behaviour change when the install is present); ks1513 5/0.
- Ticket's "a tamper that deletes the precondition must turn the first cell red": the develop suite IS that tamper (no precondition) and turns cells 1 to 3 red.

## #1697 KS-1527 `6e45c854a46f`: GO

**FOUND:** stub now appends its whole argv (`process.argv.slice(2).join(' ')`, one line in the sibling suite), one new rc-1 wording cell, and a new suite that builds two mutants of the real leg by `sed` (X4 `--update`, R1text) and requires the NAMED stub cell among the FAIL lines with no compiler (`DEPS_PRESENT_ROOT` at a missing dir). Cell 0 asserts both mutants differ from the real leg by `cmp`, so a sed that stops matching goes red rather than silently green. Covers (a) and (b) of the ticket; nothing left open on it.
**TESTED / HOW**
- Head: ks1527 4 passed 0 failed. Aimed at develop's sibling (stub without argv, no wording cell): 2 passed 2 failed (X4 and R1text cells RED), control cells ok.
- Sibling with no install: develop 25p/9f, head 26p/9f (+1 cell, the same 9 environment reds); with install: 38/0 -> 39/0.
- Unmutated-leg control inside the suite: 0 and 0 failing for the two named cells.

## #1695 + #1697 combined tree (both edit `preflight_test_types_ratchet_leg.test.sh`)

Both orders merged by real `git merge` onto develop `28e2d27de337`, rc 0, no conflict markers, **identical trees** (`521a71b75228`). Combined, no install: sibling 23 passed 0 failed (22 + 1 new rc-1 cell), ks1513 5/0, ks1527 4/0. Combined, with install (merge commits `ff18b3aaa63d`, `ff387f94ef11`): sibling 39/0, ks1513 5/0, ks1527 4/0, 0 SKIP, 0 FAIL lines. Recommended order #1695 then #1697 (no technical difference; see merge-order paragraph).

## #1698 KS-1548 `073289640d63`: GO

**FOUND:** one test line: cell M gains `calls.length !== 1 ? ... : ''` (`ks1512-...clamp.test.ts:254`). Product file untouched and identical to develop's. It pins m2 only ("no window starts once nothing is left", `routes/platform.ts:481-482`); m1 (stalled body), m3 (post-deadline answer) and the nit (cell G's second assertion, `:214`) remain open, so KS-1548 must stay open.
**TESTED / HOW (2x2, one product-line mutant; guard line count 1 before, 0 after = landed)**
| | unmutated product | mutated (guard `if (remaining <= 0) throw ...` deleted) |
|---|---|---|
| old test (develop) | 18 passed | **18 passed** (the gap) |
| new test (head) | 18 passed | **1 failed** 17 passed (cell M, 2218 ms) |
Full api-gateway suite (`npx vitest run`): develop 121 files 1175 passed; head 121 files 1175 passed (same count, one assertion edited).

## #1699 KS-1524 `c189e242a377`: GO

**FOUND:** one new cell L5 (Error thrown, assert the log is `{ error: <message> }` exactly) in `ks1510-document-lookup-logs-the-thrown-error.test.ts`. Pins (b) only; (a) guard the log call, (c) null throw, (d) cap, (e) deployed limiter key stay open, so KS-1524 stays open. Cosmetic: the id `L5` sits between L2 and L3.
**TESTED / HOW (2x2 with two mutants of `routes/platform.ts` document-lookup catch, unique anchor `document-lookup)', { error: err instanceof Error ? err.message :` count 1; the shorter anchor appears twice, so I used the longer one)**
| | none | `String(err.stack)` | `String(err)` |
|---|---|---|---|
| old test | 8 passed | **8 passed** | **8 passed** |
| new test | 9 passed | 1 failed 8 passed (L5) | 1 failed 8 passed (L5) |
Full api-gateway suite: develop 1175 passed, head 1176 passed (+1).

## #1700 KS-1649 `4f951814deb3`: NO GO (round 1 of 2 for this class)

**FOUND (the changed text, `developer-portal.html:564`, against the code):**
The new cell: `<td>1,000 req/hour by default; Platform S connector keys are minted at 3,000 req/hour</td>` and `X-RateLimit-Limit (the actual ceiling for the key, on every response)`.

| Claim in the text | Code | Verdict |
|---|---|---|
| "1,000 req/hour by default" | `services/security/src/index.ts:666` `rateLimit: z.number().int().min(1).max(10000).default(1000)`, `:667` `rateLimitWindow ... .default(3600)` | TRUE for a key minted without `rateLimit`. Caveat (READ ONLY): the gateway substitutes 100 per 60 s if the validate response carries no rateLimit (`auth.ts:248-249` `data.rateLimit \|\| 100`, `rateLimitWindow \|\| 60`). Not what the sentence says; not in the diff. |
| "Platform S connector keys are minted at 3,000 req/hour" | `routes/platform.ts:156` `CONNECTOR_RATE_LIMIT_DEFAULT = 3000`; it is a DEFAULT: `:190` `process.env.PLATFORM_S_CONNECTOR_RATE_LIMIT` overrides it, bounds `:158-159` MIN 1 / MAX 10000 (`:196` out-of-range falls back to 3000); window `:170` 3600; mint call `:848-849`. "New keys only": `:142` "existing keys keep 1,000 until rotated". | **MAJOR R-1**: stated as a fixed fact, it is wrong for (i) every Platform S key minted before the change (still 1,000) and (ii) any deploy that sets `PLATFORM_S_CONNECTOR_RATE_LIMIT`. This is Wednesday's gate note ("3,000 is the DEFAULT, bounds 1..10000"); the text does not carry it. |
| "X-RateLimit-Limit (the actual ceiling for the key, on every response)" | Set only inside the limiter: `rateLimitEnforce.ts:289`. Skipped when the caller is not a machine caller (`:159-161`, JWT/human users get the global limiter and no header) and when the limiter's own bookkeeping fails: `:275-279` (in-memory fallback also failed, `outcome = null`, "request allowed unlimited") and `:297-305` (header write throws). | **MAJOR R-2**: "every response" is false at those lines; the table row is about API keys, so the machine-caller case is in scope of the sentence only if read loosely, but `:275-279` and `:297-305` are the exception Wednesday's second note named. A developer who builds on "always present" gets a missing header exactly when the limiter is broken. |
| OAuth apps share the 1,000 default (pre-existing words, unchanged) | `oauth_apps` table has no `rate_limit` column (`startup-migrations.ts:517-531`); `oauth_app` callers take `user.rateLimit` from the token, else the 100/60 s fallback (`rateLimitEnforce.ts:183-184`) | Note N-2, READ ONLY, outside the diff, not blocking; worth a follow-up since the same sentence now claims to be careful. |

Minor M-4: the new cells pin prose substrings only (`row.toContain('... 3,000 req/hour')`); nothing ties "3,000" to `CONNECTOR_RATE_LIMIT_DEFAULT`, so a later change of the constant leaves the doc and a green suite disagreeing. Fix-shape: export the constant and assert the doc contains its formatted value.

Fix-shape for the text (for the owner to author, not applied by me): "1,000 req/hour by default; Platform S connector keys are minted at 3,000 req/hour by default (an operator can set it between 1 and 10,000; keys minted before that change keep 1,000 until rotated)" and "X-RateLimit-Limit (the key's ceiling; sent on responses the rate limiter handles)". Regression tests to add: the row contains "by default" next to 3,000 and does not contain "on every response"; plus the drift guard from M-4. Severity only; whether the two notes were meant for the published text or only for the PR body is Wednesday's call (priority), and the PR body could not be read by me (gh not logged in), so I judged the head's text as published.

**TESTED / HOW:** new test on develop's html: 2 failed 2 passed (R1, R2 RED, C1/C2 controls pass); on head 4 passed. Full api-gateway suite: develop 121 files 1175 -> head 122 files 1179 (+4), 0 failed. Text-vs-code legs are READ ONLY (no key was minted; no deploy, no stack).

---

## NOT TESTED (first-class output)

- Docker: no build, no context transfer, no `**/__tests__` matcher run (#1694); the ticket's rebuild-set measurement is owed by someone who may run Docker. Static enumeration only (#1694 section).
- The ticket's #1694 runtime semantic of the `!connectors/whatsapp-bot` negation after `**/__tests__` (documented, not measured).
- Preflight legs 3, 4, 8 and the full pre-push preflight on any head (no local stack, as the builder). The real hook was run on #1689 only, with `git hook run` and a synthetic ref line, not a real `git push`; no push, no network write.
- The four platform suites and the repo-wide vitest run: not run (only packages/shared, services/api-gateway and frontend/issuer, listed per PR). `ks879` and `threadToken` timeouts: threadToken reproduced once on the old base under load; ks879 did not reproduce; neither tied to the PRs.
- #1692: the F-4 behaviour was measured on a sandbox-simulated host only, not on a real homebrew host; trivy suites were not re-run under the sandbox.
- #1700: no running gateway, no key minted, no response header observed; every claim is READ ONLY against the source. Shipped text in `developer-portal.html` outside line 564 was grepped for rate-limit words only.
- PR bodies, GitHub mergeability/UNSTABLE rows, check-runs and the ticket comments on GitHub: not read (`gh` is not logged in here; Linear tickets were read read-only, comments first:50 sorted client-side). I claims-tested the code, not the bodies.
- No Linear or GitHub write of any kind.
- `STANDING_LINES.md` and the charter, template and learning were read whole.

## My own instrument errors (reported in the open)

1. **#1692 sandbox first try was invalid.** I copied the arm64e `/usr/bin/jq` into a scratch dir; the OS killed the copy (rc 137), so BOTH develop and head read "1 passed 4 failed" and I briefly had a number that meant nothing. Corrected by ad-hoc `codesign -f` of the copy and a control (copy runs inside the sandbox, `/usr/bin/jq` refused rc 71). The valid reading is develop 4p/1f, head 5/0. The invalid reading was never used.
2. **#1689 hook run, first try.** `git add -A systemTest` also committed my `node_modules` symlink into the synthetic commit, which produced an `ln: ...node_modules/node_modules: File exists` line from the gate in tree mode. Re-ran all five hook cases with the symlink excluded; the outcomes (rc 1 / 0 / 0 / 1 / 0) are the re-run's.
3. **Load gating.** My first background chain was set to give up waiting for load1 under 9 after 15 minutes; I killed it before it ran anything and restarted it with a longer wait. The vitest and install runs then started at load1 8.0 to 8.8. The sub-9 rule was honoured at start, not through the run.
4. **Shell slips, no effect on results:** a `PIPESTATUS` print in my mutant-A echo was meaningless (I read the result from the printed `1 failed`); zsh did not word-split a quoted spec argument once (the script died with "unbound variable" before doing anything and was re-run); `git -C $VAR` write verbs are refused by the fleet hook, so write steps ran through script files with absolute literal paths.
5. **#1699 anchor.** My first mutation anchor matched two lines (`count 2`); I switched to a longer unique anchor with an `assert count == 1` before any run. The earlier "anchor count 2" line in `chain2.log` is that discovery, not a result.
6. I did not retract anything: no finding of mine was found wrong.

## Left on disk (not deleted)

`.../spark/cache/work/gate_r2_nine_20261026/` (worktrees `dev`, `pr<n>`, `combA`, `combB`, and `scratch/` with clones and `_quarantine_20261026/` holding the moved copies); `.../spark/cache/src` gained refs `refs/gate/*` and worktree metadata. Wednesday or the next wrap can quarantine the work dir (about 2 GB with the install).
