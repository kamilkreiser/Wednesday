# Spark operator o145 report (Secuura/Blockchain), Mac mini, 2026-11-12 00:41-01:07 AEDT. The BASH tier and multi-file test-only
(Saved to disk by Wednesday from the operator's returned text, 2026-11-12 ~01:1x: the subagent's Write was refused. Content verbatim.)

Develop cb46c28eef6f6aa761111f4737e53f3de1e43d74 by ls-remote at 00:41, 00:44, 00:55, 01:01 (unchanged). I fetched the Spark cache clone to it by its literal path, as round.sh does. The Secuura checkout saw only ls-remote; every file was read from the cache clone. Tunnel UP.

Load1 at round starts was 5.3, 4.8, 5.2 and 4.6, all under 8. One real run rose to 8.0 at its end. The tier checkers run their whole-sibling legs inside every round, and there is no targeted-only leg.

Counts: 2 tickets briefed (KS-2160 O145 P1, KS-1163 O145 P2), 2 PASS, 2 READY held, 0 model FAIL. That is 3 real rounds of 6; KS-1163 needed a re-run after a harness refusal.
- Both goldens are mine.
- The model's output was BYTE-IDENTICAL on KS-2160 and TREE-IDENTICAL on KS-1163. For KS-1163 it omits the `diff --git` lines, as in o140.
- `--control` with my golden ran first on each.
- Both tickets are Backlog, so no `started_ok` pin.

## Exclusion measure was wrong, now fixed (important)
o139-o144's meas.py read held READY paths only from `diff --git a/..` lines. test_only_bash READYs and other Spark patches in `---/+++` form have no such line, so those files were invisible.
- The positive control proved it: `ks1560_private_path_suites_link_jq.test.sh` read NOT held while READY_KS-2141-O140-P1 holds it.
- I fixed my scratch meas.py to also parse `+++ b/`. Held paths went from 286 to 434. There are 87 open PRs touching 331 files and 362 READYs.
- Earlier operators' "no READY names this file" claims for bash suites may be false. Re-check any held bash suite before raising it.
- preflight.sh and the ks1547 suite also sit in old held READYs (KS-1040, 1209, 1261, 1547, 1613, 2130). All are merged and their text is at the tip. I treated them as spent, not live. Wednesday, please confirm.

## 1. KS-2160 O145 P1: test_only_bash, PLANT shape
Fault: the `RED KS-2130 the abort text states the whole sentence...` cell used `has()` = `grep -q -F`, a substring test.
Change: one hunk. The `has "..."` line becomes `grep -q -x -F -- "  so a doubled ... are not checked." "$tmp/out.txt"`, a whole-line match with two leading spaces. The label is unchanged, so no `## Renames`.
Plant: in the brief only, never in the diff. It appends ` BUT ACTUALLY THEY ARE.` at preflight.sh:246.
Hand proof first: the old cell stayed 27/27 under the plant, which is the ticket's blind spot. The new cell went 26 passed / 1 failed under the plant and 27/0 at the tip.
Rounds: control PASS in 13 s. Real PASS 10/10 legs, 42 s round, 30 s model, 22992+357 tokens.
HELD: `night/READY_KS-2160-O145-P1_spark-dsv4flash_BRIEFED-TESTONLYBASH-ks1547 abort sentence cell pinned as the whole line-PASS-10of10_2026-11-12.diff.md`. The prefix is not doubled.
UNMEASURED: GNU `grep -x -F`; a prefix on the line (caught by `-x`, not planted); the other abort lines stay substring-checked.

## 2. KS-1163 O145 P2: bash_patch2 (script plus 2 RED suites)
Kam ruled option (a), "Wait for all five", on 2026-09-22 in a ticket comment marked "recorded, not built". There has been no READY or PR since.
Script: `Start_Up/start-secuura.sh` gains five names in `EXPECTED_SUFFIXES`: demo-service, mcp-server, pgbouncer, tenant-provisioning, tokenisation. The count comment goes from 27 to 32 (2 hunks).
Suites: `start_secuura_expected_services.test.sh`: the five KNOWN_UNWAITED lines are deleted, plus one comment clause on the stack-marker line. `start_secuura_slot_names.test.sh`: typed `EXPECTED_COUNT=27` becomes 32.
By hand: suite 1 alone 3 pass / 2 FAIL, with the script 5/0. Suite 2 alone 15 pass / 8 FAIL, with all three files 23/0.
Real round: PASS 10/10, 191 s, 43.2 s model, 25852+815 tokens.
HELD: `night/READY_KS-1163-O145-P2_spark-dsv4flash_BRIEFED-BASHPATCH2-start-secuura.sh waits for the five unwaited services-PASS-10of10_2026-11-12.diff.md`.
Design calls by me: the typed 32 (not derived from the script), and the added comment clause.
UNMEASURED: the five healthchecks on a real stack start (an unhealthy one now holds start-secuura.sh to MAX_HEALTH_WAIT); `--status` and the timeout text; slots 3-4.

## Bash tier verdict
The tier ran end to end twice: the plant shape in test_only_bash, and bash_patch2 with a script. Everything that broke was brief or harness; nothing was the model.
1. KS-1163's first control was REFUSED because the builder rejects `test_file == ref`. I had copied a pin whose ref was the suite itself, and moved ref to `stack_env.test.sh`.
2. The control then FAILED B6. The sibling leg caught `start_secuura_slot_names.test.sh` going from 23 passed to 15 passed / 8 failed when only the script changed, because it types the count. A real gap in my first brief, found by the harness. I declared the sibling as a second RED suite.
3. The first real PASS was refused by hold_ready (B3x unmeasured=1). A test hunk made only of `-` lines has no `+` line to byte-compare, so a pure deletion cannot be held. Fix: give every declared file at least one `+` line. Re-brief, control and real run was the third real round.
4. hold_ready on a re-run needs the `-r2` run dir, because round.sh suffixes it. My hold.sh assumed no suffix, so I held by hand.
5. hold_ready still prints "golden: not compared" on bash_patch2 although the round said TREE-IDENTICAL.

## Screen
Linear Backlog+Todo read-only: 645 issues, 124 naming a .sh. Filter dropped Peter's and Stuart's tickets and any whose files are in an open PR or held READY by the corrected measure.
RUN: KS-2160 and KS-1163.
Skipped: KS-2159 (pre-push banner deliberate per the hook's KS-2127 comment lines 369-372, wording is the owner's call, needs a failing-git-diff fixture); KS-1759, 1764, 1755 (no fix proposed or undecided; preflight.sh and pre_push suites held); KS-2154 (earlier brief FAILED A2 at a drifted tip 0d286210; ks1560 suite held by KS-2141 O140 P1); KS-2139, 2135, 2128, 2075, 2047, 2039, 1988 (a held READY or open PR names the script; KS-2128 also needs GNU grep); KS-2140 (.mjs runner is node:test, harness lacks it); KS-2067 (empty-DB behaviour is a decision, needs Postgres); KS-1932 (awk scanner, six shapes); KS-1977 (four items + docker compose); KS-951, 948, 1088, 1138, 2069 (design question or unmeasured cause).
Multi-file test-only screen (26 hits), none briefable: KS-2100 (open tenant question); KS-1761, 1775, 2108 (no fix proposed, very large files, one in a held READY); KS-2026 (comment-count fix, no red proof); KS-1895 (intermittent); KS-1712 (needs Postgres).
Candidate 3 (second-opinion review) not run: candidates 1 and 2 produced two rounds.

## Faults (mine)
1. The ref pin, the missed sibling suite and the pure-deletion hunk cost one control and one real round.
2. Hooks refused an unquoted `======` and an `rm` of a scratch file. Nothing deleted; used a third scratch tree.
3. `show.py` first matched PS- tickets of the same number; fixed to KS-.
4. `git fetch` ran in the Spark cache only.
5. No push, PR, board or Linear write, or mail. Tokens in-process, never printed. Heredocs quoted, no npm/npx, Secuura checkout saw only ls-remote. Harness not changed.

## Left
- 2 held (none by Wednesday yet), 3 real rounds spare, Spark idle again.
- Owed: raise-seat addendum rows for O145 P1 (KS-2160: one test file, one hunk, plant on preflight.sh) and O145 P2 (KS-1163: 3 files; read the + lines; ruling cited).
- Briefs: `night/briefs/ks_2160_o145_p1_*/` and `ks_1163_o145_p1_*/`.
- Scratch: /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-12_spark-operator-o145/scratch/ (corrected meas.py, lin.py, show.py, rr.sh, hold.sh, x/ and t1163/ trees, control and real outputs, backlog.json, prs.json, held.json).
