PR 2122: GO WITH NOTES; PR 2123: GO WITH NOTES; PR 2124: GO WITH NOTES

Gate 282, tier 2 batch. QA gate, findings only. Posted nothing, mailed nothing, pushed nothing. 2026-11-09 about 14:45-14:52 AEDT.

## Pins (ls-remote at start 14:45 and again at end 14:50): NONE MOVED
develop 4d6b7bb17fd3; PR 2122 f5a9a878ef43; PR 2123 3e8265bae0a1; PR 2124 b2853fcf9274. No PR numbered above 2124 exists.

## Q1 Files and stop line (every file is under Blockchain/Dev/scripts; NO product byte in any PR)
- PR 2122: `__tests__/ks1547_preflight_step_header_denominator.test.sh` +5 (test). Tier 2.
- PR 2123: `__tests__/check_akto_container_names_flags.test.sh` +19 (test); `check-akto-container-names.sh` +2 (one comment, one PATTERN+= line; dev/ops guard, tier 2). That guard is called from run-code-guards.sh / check-stack-safety / preflight, so a wider pattern changes what the pre-push gate flags; it is still a tooling script, not a service.
- PR 2124: `__tests__/smoke_test_honours_smoke_base_url.test.sh` +12 (test); `smoke-test.sh` +2 -1 (operator script, tier 2).
No NEEDS TIER 1.

## FOUND / TESTED / HOW
Instrument: blobless clone /private/tmp/g282 + one detached worktree per head + one at develop; /bin/bash 3.2, BSD grep and sed (no GNU). Mutants applied in my worktrees by python replace on the exact line, restored with `git checkout --` and the sha compared to the start sha each time (every restore matched).

### PR 2122 (KS-2130, +5 test)
- Suite: develop 26/26, PR 27/27.
- My mutants of preflight.sh line 246 (patched suite): "are not checked." -> "are checked." RED (only the new cell); "cannot read" -> "can read" RED; wrong example `:17` -> `;17` RED; trailing period dropped RED. Each prints exactly one FAIL, the new KS-2130 cell. Line 245 changed ("a closing parenthesis" -> "...X"): stays green (scope claim true, line 2 not pinned, the body says so). Same shape on develop's suite stays green for the first mutants (the seat's claim; I confirmed develop's suite is 26/26 only for the unmutated script).
- Control for the pin: my own mutant that APPENDS " BUT ACTUALLY THEY ARE." after the sentence: suite stays 27/27 (see G282-2122-1).
- Sibling suites: ran 3 of the 12 (gateway_slot 15, leg4_sweep_not_run 5, failure_verdict_keeps_ratio 8) on develop and on the PR head: output byte-identical (cmp), rc 0. The PR touches one file, so the other 9 are untouched by construction.
- Cell names: "RED KS-2130 ... states the whole sentence" is true of the sentence, but the cell is a `grep -F` substring, not a whole-line compare.
- Merge tree on develop: rc 0 (f739aca5fe73). Note its merge base is e028786a0921, one commit behind develop; clean.

Findings
- G282-2122-1 (low): the cell and the PR/ticket words call it "the whole third line"; it is a substring (`grep -q -F`). An inversion made by APPENDING text to the sentence or the line (planted: " BUT ACTUALLY THEY ARE.") passes 27/27. The listed plants (change inside the sentence) are all caught; the appended class is not. Wording "whole line" in the PR body summary and ticket BLUF is wider than the cell.
- G282-2122-2 (info): the seat's 334 vs 338 sibling-cell gap was not investigated by me (NOT TESTED); it is the seat's own declared UNMEASURED and sits outside the PR.

### PR 2123 (KS-1902, +2 script, +19 test)
- Suite: 12/12 at head. Red-first: not re-run as a script-hunk reversal, but my mutants cover it: dropping the whole value group turns exactly the 4 red cells red (-u root, -e FOO=1, --tail 5, -it -u root), as READY states.
- My mutants of the added PATTERN line (restore sha checked): value group's `?` removed -> only `-it -u root` red; outer `+` -> single -> only `-it -u root` red; `logs` dropped -> only the logs cell red; `exec` dropped -> 3 red; `akto-` broken -> 4 red; value-word class `[^-[:space:]][^[:space:]]*` shortened -> 3 red. SURVIVORS (no cell goes red): `[[:punct:]]?` removed (quoted name after flag+value untested); value first char allowing `-`; dropping `restart` from the verb list. Probes show inspect, cp, kill, stop, rm, restart and quoted names after a flag-with-value are all newly flagged by the PR and none has a cell; only exec and logs do.
- Probes (develop vs PR rc, rc 1 = flagged, fixture tree per case): `-u root "akto-mongo"` 0->1; `inspect -f x`, `cp -a f`, `kill -s KILL`, `stop -t 5`, `restart -t 5`, `--env-file .env -u root`, `logs -f --tail 5 --since 1m` all 0->1 (correct). Clean controls stay 0: `-u root other-mongo mongosh akto-x`, AKTO_PREFIX forms (bare and quoted), comment line.
- Over-flags (new): `docker exec -it other-container akto-x` 0->1 (declared by the seat, no cell); `docker exec -u root _akto-x` 0->1 (NOT declared). Remaining false negatives: `-u "a b" akto-mongo`, `-u root $(echo akto-mongo)` stay 0 (not asked by the ticket).
- ReDoS: 3000 repeats of `-a b ` and 20000 of `-a ` with no akto name: 23 ms and 30 ms, rc 0. No catastrophic backtracking on BSD grep.
- Real tree: the script over the PR's systemTest/akto: rc 0, and rc 0 on develop. GNU grep: NOT TESTED (BSD only, as the seat says).
- Is the script change exactly what the ticket asks? Yes: one added alternation allowing one value word after each dash-token (the ticket's own "consume a value token" fix shape), nothing else. The comment added in the script claims `[[:punct:]]?` "stands for the optional quote": it matches ANY punctuation character, not just a quote (G282-2123-2).
- Merge tree: rc 0 (5ab7539d1821), base = develop tip.

Findings
- G282-2123-1 (low): the PR body summary says "six cells now say it for the value-taking spellings plus two clean controls", which reads as 8 cells. The diff has 6 cells: four red (c7-c10) and two controls (c11, c12). The tier line (+19, six cells) is right; the summary sentence is wrong.
- G282-2123-2 (low): `[[:punct:]]?` (and the comment saying it is the optional quote) is wider than the original `[\"'\`]?`. Measured: `docker exec -u root _akto-x` is newly flagged. Harmless in practice but undeclared and the comment is inaccurate. The old first alternative used a quote class.
- G282-2123-3 (low): test coverage thinner than the surface the change moves. Survivors above: six verbs (inspect, cp, kill, stop, rm, restart) and the quoted-name form were widened and none has a cell; two of three of my survivor mutants (quote, `restart`) flip real behaviour. The PR body claims only the cells it has; nothing false, but "the guard now flags ... a docker flag" is a claim about all eight verbs.
- G282-2123-4 (info): the declared over-flag (`docker exec -it other-container akto-x`) is true and is stated in the body and ticket comment as the seat says. Because the guard runs in the pre-push preflight, a false positive would block a push; no line in the real tree trips it.

### PR 2124 (KS-1794 item 3, +2/-1 script, +12 test)
- Suite: 8/8 at head. Red-first: the PR's suite on develop's smoke-test.sh: 6 pass, 2 FAIL (the two RED cells), matches the READY. Three sibling suites that drive the script (degraded_warns 5, counters_survive_errexit 6, direct_ports_follow_the_target 25): output byte-identical against develop.
- My mutants of the echo line (restore sha checked): `\1` dropped -> scheme lost: cell 2 red; scrub removed (print $GATEWAY) -> cells 1 and 2 red; `[^/@:]` -> both red; replacement text X -> cell 2 red. The seat's control (request goes to full base) is the third new cell and I did not need to touch it. SURVIVORS: scheme class without digits, anchor `^` removed, scheme class without `+`, and a FIXING mutant `[^/]*@` (greedy to the last @) passes 8/8: no cell pins either gap as a limit.
- THE KEY QUESTION, all three gaps verified by fixture with a stub curl first on PATH and an `.invalid` host (script never run against a real host; quick and full mode):
  1. Skip warnings: CONFIRMED. `direct_skip` (SKIP++ at line 46, warn at line 47) and `local_skip` (SKIP++ at 55, warn at 56) both print `a run against $GATEWAY`. 15 call sites (12 direct_skip + 3 local_skip, lines 284-433), all inside the `else` of the `--quick` branch (the branch ends at line 176/177). Fixture, full run, `SMOKE_BASE_URL=https://alice:s3cr3t-token@smoke-target.invalid:9999`: 15 output lines contain `s3cr3t-token`; the Smoke target line is clean. In `--quick` the output has 0 secret lines.
  2. Raw @ in a password: CONFIRMED. `https://alice:p@ssw0rd-tail@host` prints `Smoke target: https://ssw0rd-tail@host` (the tail of the password).
  3. Scheme-less URL: CONFIRMED. `alice:s3cr3t-token@host:9999` prints unchanged.
  Does the body's NOT-covered statement state ALL of them? It states all three the seat measured, truly (the skip warnings and 15 call sites, GNU sed, raw @, no-scheme; also "left for the board" and "item 2 not in this PR"). It does NOT state a fourth shape I measured: a secret carried in the query string (`https://host:9999/?token=s3cr3t-token`) is printed unchanged on the Smoke target line and in all 15 warnings (G282-2124-2). Its line citations (46 and 55) are the SKIP increment lines; the warn lines are 47 and 56 (G282-2124-3).
- Merge tree: rc 0 (7e5bc1106e38).

Findings
- G282-2124-1 (medium): the stated purpose (a token in SMOKE_BASE_URL is not written to a terminal or CI log) is NOT met on a full run, which is the run RUNBOOK 2.2 prescribes (ticket item 2, still open). 15 warnings leak the full credentialed URL on every non-local full run. This is disclosed in the body, ticket comment, and `didnot` list, so it is not a hidden defect, and the PR says Refs and leaves the ticket open; but the one-line script comment the PR adds ("so a token in SMOKE_BASE_URL is not written to a terminal or a CI log") states the full claim unqualified, in the code future readers see. Ruling for Kam/Wednesday: take the PR as a partial fix (GO WITH NOTES) or require the 15 warnings to print the scrubbed value in the same PR. A one-variable change (`GATEWAY_SHOWN` used by the three printing sites) would close gaps 1; widening the sed to `[^/]*@` also closes gap 2 (mutant passes the suite).
- G282-2124-2 (low): the body's NOT-covered statement is complete for the three gaps the seat measured but names fewer than exist: query-string secrets (`?token=`, `?api_key=`) are also printed unchanged, in the target line and in the warnings. Also the script comment's "a token in SMOKE_BASE_URL" is wider than the userinfo-only scrub.
- G282-2124-3 (info): body cites "line 46 and line 55" for the warnings; at the head the warn lines are 47 and 56 (46/55 are the SKIP increments).
- G282-2124-4 (low): no cell pins the two known limits (raw @, scheme-less); a mutant that fixes the raw-@ gap passes 8/8, so the suite would not notice a regression or a fix either way. The new cells run `--quick` only, so they cannot see the 15 warnings (the body says so).

## Q5 Merge trees on develop 4d6b7bb17fd3 (git merge-tree --write-tree)
- 2122 alone: rc 0, tree f739aca5fe73
- 2123 alone: rc 0, tree 5ab7539d1821
- 2124 alone: rc 0, tree 7e5bc1106e38
- all three (2122 then 2123 then 2124): rc 0, tree f38f4284da34; diff against develop is exactly 5 files, +40 -1.
Shared paths with each other: NONE (five distinct paths, planted overlap not needed; the diff-of-union equals the sum). With open PRs: from the seat's saved census (50 open PRs, REST GET, E8 pre-push; planted positive PR 2102 found by `baseline-api-gateway`, my re-read of the JSON gave the same planted hit and: 2122's suite path only in PR 2122 itself; nothing for the akto script, its suite, smoke-test.sh or its suite). I did NOT redo the census live (gh is not logged in for this account on this machine; GET via the seat's record only). No PR above 2124 exists per ls-remote.

## Q6 Words
Read the seat's saved copies (pr_spec.json bodies, ticket comment templates, READY bodies, KS-1794 and KS-1902 ticket text): live PR bodies and the comments 9ee4e4c6, e96bc82f, 6d565175 were NOT read live (NOT TESTED live: gh not authenticated here; Linear not reachable). Against the heads: true except G282-2122-1 ("whole line"), G282-2123-1 ("six cells plus two controls"), G282-2124-2 and -3. Everything else I checked held: the cell counts (27, 12, 8), the red-first FAIL lines for 2124, the 3 sibling suites identical, the real-tree rc 0 for the guard, the over-flag statement, 15 call sites, and "the request still goes to the full base".

## NOT TESTED
GNU grep/sed (all measures BSD); shellcheck; the pre-push hook legs; the 334 vs 338 count; 9 of the 12 sibling suites of PR 2122 (3 run); the live PR bodies/ticket comments; a live open-PR census; smoke-test.sh against any real host (never done); a GNU/Linux CI run of the akto guard.

## My conduct
No git write verb in any !CODING checkout. Clone only in /private/tmp (git writes there only: clone, fetch, worktree add, merge-tree/commit-tree objects, checkout of tracked files after mutants). No cd. No smoke-test.sh run except with a stub `curl` first on PATH, `.invalid` host. Two early commands were refused by the harness hooks (zsh word-splitting; an `rm` of my fixture dirs): redone in bash heredocs and without rm. Load1 peaked at 7.7 at start (just under 8), 5.3 at end. DevMASTER df: 106 Gi free at start and at end (unchanged).
Clone sizes at the end (not removed; no rm allowed by the hooks): /private/tmp/g282 194M; worktrees /private/tmp/g282w2122, g282w2123, g282w2124, g282wdev 354M each (about 1.6 GB total); fixture dirs /private/tmp/g282_fx.* and g282_smk.* (small); scratch fx.sh in the session scratchpad.
