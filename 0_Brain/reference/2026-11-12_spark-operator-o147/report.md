# Spark operator o147 report (Secuura/Blockchain), Mac mini, 2026-11-12 01:46-02:05 AEDT
(Saved by Wednesday 02:0x from the operator's returned text: its own Write was refused. Content verbatim in substance; Wednesday's source-read verdict appended at the foot.)

Develop 4f85ca04c622f29099d184bc45de2faa61fb4af0 by `ls-remote origin` at 01:46, before each round and at 02:03, unmoved. (ls-remote on the checkout path alone reads the local branch 0e6479d7, not origin.) Only the Spark cache clone was fetched to the pin; the Secuura checkout saw only `ls-remote origin`. Tunnel UP; load1 3.4-4.5 at round starts, 7.2 at 02:03.
Exclusions re-measured (corrected `+++ b/` + `diff --git` measure): 88 open PRs / 336 files; 363 non-.pre READYs / 437 held paths. R 100th's rows 38/40/41/42 + PR 2183 touch none of these files. The only READY on exportService.ts (KS-1922 O128 P2) is merged and its text is at the tip (98d7a21cf): spent.

## Verdict per candidate
- KS-2167: briefable, briefed, PASS, held (save first, then log inside a try; new vitest file copied from ks1922's harness).
- KS-2168: briefable, briefed, PASS, held (one doc sentence; route fact read at the tip, metering.ts 119-125 answers 400 BAD_REQUEST; expect_absent = the old sentence).
- KS-678: skip, HARNESS LIMIT, after a full hand build. The ask is clear (URL host rule; the board seat's 11-09 comment narrowed it). Hand proof: E10 on a scratch copy of the guard gives 0 findings on the real spec (422 example blocks) and 1 on a planted `webhookUrl: https://example.secuura.io/resource`. The builder refuses: "scripts/ product scripts/spec-examples/check/rules-example.mjs is admitted ONLY as a test-only tamper target". Subdomains of a reserved name passing is the operator's design call. Brief + golden kept for a Claude seat or a harness widening.
- KS-967: skip. The ticket says "keys named, not pattern-guessed" but names none; 32 tracked *.env.example files hold ~45 non-empty credential-shaped placeholder values; which keys and placeholders is a policy choice; the demo123 allow-list is the screen's, not the ticket's.
- KS-987: skip. Runbook additions with no absent text (pure addition; o141 precedent).
- KS-1486: skip. services/auth/src/routes/wallet.ts is in open PR 2099 (KS-2060); also an auth file needing a tier-1 gate.
- KS-668: skip. Flips ALLOW_DEFAULT_SEED_PASSWORDS and forwards 11 credential vars: credential surface, demo frozen by Kam's card; docker-compose.yml also in open PR 2052.
- KS-2051: skip. o143/o144's reason holds: authorisation design; the ticket says "for the owner to decide".
- KS-2093: skip. Rule choice ("possible shape (mine, not a decision)"); governanceService.ts also in open PR 2099.

## Rounds (3 real model rounds of 6; 2 controls passed, 1 control caught a brief defect)
1. KS-2167 O147 P1, code_patch2 (one product hunk + a new 5-cell test file, R1-R3 red). --control with the golden PASS 36 s, golden byte-identical. Real round PASS A1-A7 + A2a, golden BYTE-IDENTICAL; 74 s round, 42.7 s model, 13719+1557 tokens. A4 3 failed of 5; A5 5/5; A6 no new red in the whole analytics suite (123 -> 128); A7 tsc rc 0.
2. KS-2168 O147 P2 round 1, doc_only: control FAIL and real FAIL, cause = the BRIEF (a third expect_present already held at the tip, so A4/A7 failed). Model output TREE-IDENTICAL to the golden: no model fault.
3. KS-2168 round 2 (rebrief, that line dropped): control passed first; real PASS, 9 legs, TREE-IDENTICAL; 23 s round, 13.8 s model, 6646+389 tokens.
Builder refusals before the first control were brief faults (a moved line made a + and - identical: comment reworded; a blank context line: -U2).

## READYs held (2)
- local-model/night/READY_KS-2167-KS-2167-O147-P1_spark-dsv4flash_BRIEFED-CODEPATCH2-analytics failed-export catch saves the failed row before it logs, a throwing logger is swallowed-PASS-7of7_2026-11-12.diff.md (strict apply OK at 4f85ca04c622; red 3/5, green 5/5).
- local-model/night/READY_KS-2168-KS-2168-O147-P2_spark-dsv4flash_BRIEFED-DOCONLY-metering usage doc: a repeated from answers 400-PASS-9of9_2026-11-12.diff.md (operator note: round 1 was a brief defect).
Both tickets Backlog (no started_ok pin); prefixes not doubled; KS-2168 held from the -r2 run dir.

## For the raise seat
- KS-2167 behaviour change to state: the failed row is saved before the log line; a throwing logger or an unreadable error.message is swallowed in that one catch; createExport's un-awaited processExport gets no .catch, so a throw from dbSaveExport itself stays unhandled. Operator's choices: the try-wrap and reorder, plus cell R3 (a throwing message getter). UNMEASURED: whether any consumer reads the old order; vitest's unhandled-rejection report at the tip.
- KS-2168: Refs only; KS-1875 stays open (its piece 1, 500 on an impossible date, is still true in the doc).
- Neither READY needs a tier-1 gate on its face; both use Refs, never closing words.

## Proposed card text (NOT filed)
- KS-2051 / KS-2093, one card each: "Who may create a sub-delegation under a parent (KS-2051: only the parent's delegatee, plus document owner for a top-level one?) / who may execute a queued governance proposal (KS-2093)?" Options [a] mirror cancelProposal's guard (proposer or committee); [b] a named role set; [c] same-tenant only. Recommended [a] for KS-2093 (the sibling route already refuses the same callers with 403); KS-2051 needs Kam's rule on the delegatee check. Sequence after open PR 2099 (governanceService.ts).
- KS-967: "Which keys does the env-example guard name, and what values are placeholders?" [a] named keys only (ADMIN_USER_PASSWORD, TEST_ADMIN_PASSWORD, DEMO_*; demo123 allowed); [b] every credential-shaped key with a placeholder-shape allow-list (change-me, <...>, sk_..., your-...); [c] leave it to the ks949 cell. After a ruling: a Spark bash task.

## Left
Spark idle, 3 rounds spare. Briefs under local-model/night/briefs/: ks_2167_o147_p1_failed_export_catch_saves_before_it_logs, ks_2168_o147_p2_metering_usage_doc_repeated_from_answers_400, ks_678_o147_p3_spec_examples_guard_e10_url_host (builder-refused, never run). Scratch: 0_Brain/reference/2026-11-12_spark-operator-o147/scratch/ (meas.py, rr.sh, hold.sh, g2167/, g2168/, g678/ incl. the hand-proved golden and both scratch guard trees, control and real outputs). Hooks refused a variable-path git apply and an rm (re-issued with literal paths; nothing deleted). .env values read in-process only, never printed. No push, PR, board, Linear write or mail beyond the Spark cache fetch.

## Wednesday's source read (02:0x, 2026-11-12)
Every +/- line of both READYs read. KS-2167: the hunk's '-' lines equal develop 4f85ca04c622 exportService.ts 165-169 (read from the Spark cache clone, which holds the pin; the shared checkout does not); the new order (set status, set constant reason, save, THEN log inside try/catch) is the ticket's fix; test file 105 lines, 3 RED + 2 controls, real ExportService with stand-ins. ACCEPTED, tier 2; the PR body must state the three behaviour points above. KS-2168: the new sentence quotes metering.ts:123 at develop verbatim ('from and to may each be given once', BAD_REQUEST). ACCEPTED, tier 2 (docs). Both become R-lane rows.
