# Spark operator o146 report (Secuura/Blockchain), Mac mini, 2026-11-12 01:08-01:25 AEDT. Second-opinion review round, then the re-screen with the corrected held-path measure.
(Saved to disk by Wednesday from the operator's returned text, 2026-11-12 ~01:2x: the subagent's Write was refused. Content condensed only in layout; every figure verbatim.)

Develop by ls-remote 01:08 and 01:10: c1f3d66e7720bf71fde0f410bf61f51fbb43a5dc (moved one commit from the commission's cb46c28e: PR 2172, one test file, not the operator's). Secuura checkout: ls-remote only. Review ran on the Spark cache clone at 2e998b8d (the READY's own tip). Tunnel UP, load1 4.9-5.6.
Counts: 0 tickets briefed, 0 READYs held, 2 Spark review requests (1 real, 1 planted-defect control), 0 failures. Nothing written under !CODING; no push, PR, board, Linear write or mail.

## Held-path measure (o145's corrected meas.py)
01:09: 87 open PRs / 334 files, 363 non-.pre READYs, 437 held paths (434 + o145's two READYs). Positive controls: ks1560_private_path_suites_link_jq.test.sh HELD; demo-service/src/routes/persona.ts HELD (KS-1927 O144 READY). Spent per Wednesday's ruling (KS-1040, 1209, 1261, 1547, 1613, 2130): four paths held only by spent READYs, none in an open PR: scripts/preflight/preflight.sh, preflight_state_is_initialised.test.sh, preflight_verdict_names_real_failures.test.sh, preflight_leg4_sweep_not_run.test.sh.

## 1. Second-opinion review: KS-1927 held READY (O144 P1) against gate 311 (PR 2176: GO WITH NOTES, 1 Minor + 5 Notes)
Inputs: spark_review.py, REVIEW_CHECKLIST.md as system prompt unchanged; ticket description (no comments); the 136-line diff; both touched files at head, line-numbered; facts.json carried from the Spark checker's artefacts, labelled carried (2 of 5 red-first, suite 103 -> 108, tsc rc 0). Head = base 2e998b8d + the READY's patch.diff (apply --check passed) in scratch/revclone. No PR body, drafted comment or CI supplied.
Real run: valid JSON, 22.0 s, 7045+478 tokens, GO WITH NOTES, 4 findings, 4 of 4 evidence quotes found in the input.
| Reference finding (G311-2176) | Spark real run | Planted control |
|---|---|---|
| -1 Minor: !res.headersSent guard not pinned by any cell | Caught as a Note (finding 3, persona.ts:90 quoted exactly); no mutation run; severity one step low | Caught (finding 4) |
| -2 Note: unconditional removeHeader killed by the ks1868 test | Not raised (needs a mutant run) | Not raised |
| -3 Note: removeHeader('Set-Cookie') removes every Set-Cookie value | Missed | Planted widening caught, as a Note |
| -4 Note: the cookie cannot be taken back once the head is written | Caught, merged into -1 | Caught |
| -5 Note: PR body says Backlog vs Linear In Progress; RED cell names | n/a (no body); correctly raised "PR body MISSING" | Same |
| -6 Note: every checkable READY statement reproduced | n/a | n/a |
Recall on the 3 substantive items (-1, -3, -4): 2 of 3, severity under-called on -1. Verdict match: yes (GO WITH NOTES both; zero Majors both).
False positives checked at source: real finding 2 vacuous Note; real finding 4 true as a limitation (test line 24), mild (C1 lines 54-58); real finding 1 self-inflicted (no body supplied); no false claim in the real run. Planted-run finding 5 FALSE (R1/R2, test lines 76-98, cover a throw after the cookie): the one false positive, control run only.
Planted control: persona.ts line 90 changed to remove every response header (passes every cell). GO WITH NOTES, 33.3 s, 7062+949 tokens; widening seen but filed as a Note. Planted code never held or run (scratch/revclone commit d478f793, scratch/review1927_planted/).
Reading: useful as a cheap first read (unpinned-property and stated-limitation issues; found the reference's one Minor and its post-head Note; 8 of 8 quotes real across 2 runs); cannot reproduce gate-style mutant findings; under-calls severity; does not replace a Claude gate. ONE sample on one ticket.

## 2. Re-screen of Backlog/Todo with the corrected measure (644 issues, read-only)
Freed (holds were spent only): preflight.sh. No ticket naming it passes the kit predicate: KS-1764, KS-1755 (no fix proposed; delete-or-keep decision); KS-2047 (three items on a 920-line shared push gate, conditional item; not Spark-sized); KS-1146 (new leg = design); KS-630 (undecided); KS-1149 (ssh keepalive); KS-1611 (intermittent); KS-1389, KS-1162, KS-1398, KS-1051 (design, or not preflight changes).
Still live (skip unchanged): KS-2154 (ks1560 suite: READYs KS-1560, KS-2141); KS-1759 (pre_push_hook_base.test.sh: READY KS-910); KS-2139 (check-stack-safety.sh: PR 2052 + 3 READYs); KS-2135 (smoke-test.sh: PR 2124 + 4 READYs); KS-2128 (check-package-format.sh: READYs KS-1716, KS-998); KS-2039, KS-1988 (run-migrations.sh: READY KS-1988); KS-2075 (READY KS-2075 exists; PR 2052 holds docker-compose.yml); KS-1743 (routes/documents.ts: open PR 2161 + READY KS-2107).
KS-1553, KS-937, KS-851, KS-1031 no longer in Backlog/Todo (not re-read).
The corrected measure changes the status of exactly 4 paths; no skip becomes briefable. Spark idle, 4 rounds spare.

## Faults (operator's)
1. Hooks refused three commands (unquoted `======`, a cp through $VAR/../.., a git write verb with a variable path); re-issued with literal paths. 2. Called spark/spark_status.py at a wrong path; used tunnel.sh check. 3. facts.json assembled from checker artefacts, not spark_gate.sh (needs a PR ref and node_modules); the reference gate also had the PR body and ran mutants, so the comparison is review-only; a fairer re-run adds --pr-body-file from PR 2176. 4. revclone left in place, never deleted.

## Left
No READY owed to a raise seat. Artefacts: scratch/ in this folder (meas.py, lin.py, cmp.py, holders.json, prfile.json, facts_1927.json, rev_1927.diff, ticket_KS-1927.txt, review1927/, review1927_planted/, preflight_tip.sh, revclone/).
