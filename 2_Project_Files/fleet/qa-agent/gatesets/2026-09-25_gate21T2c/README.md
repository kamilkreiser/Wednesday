# Gateset 2026-09-25_gate21T2c — README for Wednesday

The drafters launched nothing, sent nothing, tapped nothing, committed nothing, and wrote nothing outside the kit directory. This kit was started by a drafter whose parent session rotated (source, read-only: `/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/fa11cd0d-1030-4620-83ac-40d313b499eb/scratchpad/gate21T2c/`) and finished by a second drafter in this directory (`cp -Rp` of the source; the source is untouched).

This is ONE tier-2 batch gate: round 21, the THIRD tier-2 batch, over EIGHT PRs (FROZEN at eight — COMMISSION.md). Routing: `QA/Secuura-batch1218`. GO string: `GO: merge #1218, #1219, #1223, #1233, #1235, #1236, #1237, #1238 batch`.

## 1. The eight PRs and the pin

The heads were re-read at 07:43:01Z by `git ls-remote origin` (read-only, from the Secuura checkout). They were read again in predict_7.out (ls-remote + a fetch into a scratch clone FROM ORIGIN), in fill_5.out (ls-remote), and at 08:13:30Z in repin_dryrun_2.out (ls-remote + the GitHub pulls API; all `open`, `mergeable True`). **All eight equal COMMISSION.md, and none moved.**

| PR | ticket | tier | head | commits past BASE |
|---|---|---|---|---|
| #1218 | KS-897 + KS-896, ROUND 2 | T2 | `d971aa4f24665bb192765a0c6e82f719996efb92` | 3 |
| #1219 | KS-1277 | T3 | `5d5129a03af0bf1586c26403a453ce283ae0be2f` | 1 |
| #1223 | KS-1118, ROUND 2 | T2 | `2892e528630d93a5b1b1482efa6978edce4211f1` | 2 |
| #1233 | KS-1133 (+KS-1229 R-a) | T2 | `6892124d9304ae014c52f7ea08a17e9468d411bf` | 1 |
| #1235 | KS-1140 GF-1 | T2 | `1c899947ea31e7a6628f5256174c1c353e6587af` | 1 |
| #1236 | KS-1110 A+B | T2 | `4296ba6d090c212d0849f488f882d00a2985245e` | 2 |
| #1237 | KS-1229 | T2 | `cfa16eb70ba28c5833101e39e4e1cb1680b8dd6c` | 1 |
| #1238 | KS-1158 | T3 | `0f3ffbb0947a82b7ec1c2866fd1a82ff4c94b2c1` | 1 |

**Pins:**
- BASE: `6ab9d5021e96ea1481cb6c6ff2d6d33b414aecb7`.
- Launch develop: `d9515f4a06e0db0396a059ccd8c76b610f22a22b`, 18 past BASE. Re-read unmoved at 08:13:49Z (ls-remote).
- END_TREE: `15dfe75db96e0816e2280ce70d2b4e1f83e33b73`. It agrees in three distinct orders and with `apply --cached` as a second instrument. Shortstat: `11 files changed, 396 insertions(+), 44 deletions(-)`.
- Merge-bases: every head's merge-base with develop is BASE, measured two ways:
  - `git merge-base` in the scratch clone;
  - GitHub compare `develop...head` in launcher_check_3.out, which shows ahead 3/1/2/1/1/2/1/1, behind 18, and each PR's files list == its own paths by name.
- Disjointness: the 11 paths are pairwise disjoint across all 28 pairs (predict_7.out (d)).

**Develop moved twice after the first drafter's last pin (cf3de2c4c):**
1. **17:32–17:33 AEST** — the five tier-2b squashes #1225 1ded2f817, #1227 7f06f3d40, #1229 ab7826afb, #1231 b83f986fd and #1232 aa600af94. This is why the first drafter's controls_3.out REFUSED: every arm hit exit 17.
2. **07:45:31Z** — **#1240 KS-789 (tier 3, NOT in this kit)**, squashed as d9515f4a0. It touches `Blockchain/Dev/CONTRIBUTING.md` only, which is disjoint from all eight PRs.

## 2. The one thing Wednesday must rule on: a SECOND declared overlap (#1225 × #1219)

**#1225 KS-1291 DEADGUARD (squash 1ded2f817) edits `Blockchain/Dev/services/originate/src/routes/documents.ts`, which is #1219's only file.** The first re-measurement over aa600af94 therefore FAILED base-invariant checks (3) and (1) for #1219 (predict_6.out, rc 1, 2 hard fails). The repin script's own rule is that a move touching a PR's own paths is re-predicted BY HAND. Here is that measurement, taken in the scratch clone (instruments: `merge-tree --write-tree`, `diff -U0`, `diff --numstat`, `rev-parse`):

- **The hunks are textually disjoint:**
  - #1225 has hunks at :610-611 and :841-849 (numstat 8+/11-, net −3 lines).
  - #1219 has the docblock at :61-67 and the /revoke PLACEMENT comment at :2332-2345.
- **Develop's blob equals #1225's squash blob.** Develop's blob at that path is `8331f626cd82b977204da3c5193c64df91908ce7`, the same as #1225's squash blob, and no other develop commit touches the file since BASE.
- **The merge is clean, and #1219's diff survives intact.** #1219 merges clean over develop to merged tree `edc74a8475e2944da4b4741752a63c9a76e8018a`. The 18 +/- lines of diff(develop, merged) are byte-identical to diff(BASE, #1219 head), and numstat 11/7 == 11/7.
- **#1219's claims still hold on the merged file.**
  - checkOnBehalfOf has 4 call sites, at [1612, 1971, 2160, 2345], on routes transfer-custody / version / share / revoke.
  - recordOnBehalfOf has 4 call sites.
  - #1219's comments cite no line numbers, so #1225's −3 shift stales nothing it adds.
- **Negative control:** a simulated FOREIGN edit of documents.ts over develop REFUSES on #1219 (predict_simforeign1219_d384.out, rc 1). The existing #1221 foreign control still refuses on #1237 (predict_simforeign_d384.out, rc 1).

**I encoded this as a second exact-shape declared overlap, the same way the first drafter handled #1221 × #1237:**
- predict `OVERLAP['1219']`;
- a new prompt paragraph, "THE DECLARED OVERLAP (#1225 × #1219)";
- the launcher's exit-34 rule, which now also requires that paragraph and the 8331f626 blob sentence;
- a new control, B3.

**Accepting it is your call.** If you refuse it, #1219 comes out of the batch or has to be rebased, and the kit must be re-predicted.

## 3. Controls — `controls_gate21T2c.sh` on the final kit, in controls_4.out: **43 OK / 0 MISMATCH** (rc 0, 07:5x–08:13:17Z)

The controls run both ways:
- **Positive arms:** P `--check` rc 0, R1 repin dry-run rc 0, R6 moved-kit dry-run rc 0 (MOVED KIT ×1).
- **Negative arms (40):** each plants one fault and must hit its own exit code: C 6, D 17, V 10, G/U 8, O 30, T 32, I 7, L 33, B/B2/B3 34, K–K5 35, X 36, F–F4 37, Y/Y2 38, H 39, W 40, Q/Q2 41, J 42, Z 43, S2 44, A 26, E 25, S 23, N 21, M 2, R2 11, R3 10, R4 1, R5 9.

The first drafter's controls_3.out showed 12 arms as MISMATCH (rc 17). That was develop moving under the run, not the rules; all 12 pass now.

**Changes I made to the controls:**
- **Added B3**, which doctors the #1225 blob sentence; want 34.
- **Changed R4.** It used to do a REAL repin run against the live inbox_routing.conf and rely on the routing line being absent. If you had added the line mid-run, that "control" would have gone on to `cockpit.sh add`. R4 now runs a copy of the repin script whose ROUTING names an empty scratch file, and it asserts that the copy names no real routing file. It stops at step 0 by construction.

**Not controlled:**
- exit 16 (needs a TTY; a faulty arm would exec claude);
- the repin's `mergeable=False` refusal (no override);
- the real launch path;
- the step-3b re-pin run end to end.

**Known fragility, NOT changed:** unlike gate21T2b, the doctored arms do not pin `QAB1218_CUR_DEV`. A develop move during a controls run masks them as exit 17, as controls_3 shows. Re-run the controls if that happens.

## 4. Routing line — NOT WRITTEN. Add it FIRST (`PROPOSED_inbox_routing_line.txt`)

    QA/Secuura-batch1218|coagent@agentmail.to|yes

My read at 07:5xZ (grep -c): batch1218 = 0, and the control batch1224 = 1. Without the line, the repin script's step 0 refuses with rc 1.

## 5. The ONE launch command (copy to gatesets/ + re-measure + re-fill there + re-pin-and-launch; run from a shell that can reach tmux)

    /usr/bin/rsync -a --exclude '_sp' /private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/d384786a-4d7e-451d-a78b-40a06ef20e21/scratchpad/gate21T2c/ /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-25_gate21T2c/ && python3 /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-25_gate21T2c/predict_gate21T2c.py <your session scratchpad under /private/tmp/claude-501/> && python3 /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-25_gate21T2c/fill_gate21T2c.py <same scratchpad> && /bin/bash /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-25_gate21T2c/repin_and_launch_gate21T2c.sh /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-25_gate21T2c/launch_qa_secuura_batch1218-t2.sh <same scratchpad>

**Why predict + fill run before the repin script:** the repin script re-fills a MOVED kit at step 0b. That fill refuses (rc 8) if develop moved since the last predict, and 0b runs BEFORE the step-3b re-pin. Running predict + fill at the new home first makes the chain self-healing against a develop move. Step 3b still catches any move between fill and launch.

**If predict refuses:** a new develop commit touched an own path outside the two declared overlaps. STOP and re-predict by hand.

**Repin steps (exit codes in brackets):**
- 0 routing (1)
- 0b home (8)
- 1 ls-remote (2)
- 2 pulls API (3)
- 3 heads == pins, open (11)
- 3b develop moved → predict + fill (10)
- 4 usage gate (12)
- 5 `--check` (13)
- 6 `cockpit.sh add QA/Secuura-batch1218` (14)

**Rehearsal:** append `--dry-run` to the last command to rehearse steps 0–3. repin_dryrun_2.out: **rc 0** at 08:13:37Z, both instruments agree with all eight pins, develop unmoved.

## 6. Files changed by the finishing drafter (each original kept as `.pre-d384`)

- **predict_gate21T2c.py:**
  - the second overlap, `OVERLAP['1219']` with blob 8331f626;
  - the `--simulate-develop foreign1219` negative control;
  - (h) now also checks #1219's claims on the MERGED file;
  - overlap messages generalised.
- **fill_gate21T2c.py:** the overlap-status wording names both overlaps.
- **prompt_gate21T2c.TEMPLATE.txt:**
  - "the TWO declared overlaps / exceptions";
  - the new #1225 × #1219 paragraph;
  - check (a) now points at the newest predict_N.out and names both overlaps.
- **launcher_gate21T2c.TEMPLATE.sh.txt:** exit 34 requires the new paragraph and the blob sentence.
- **controls_gate21T2c.sh:** B3 added; R4 made unable to reach a launch.
- **Re-rendered by fill_5:** `2026-09-25_secuura-batch1218-t2.prompt.txt` (72776 B, 275 lines) and `launch_qa_secuura_batch1218-t2.sh` (21129 B, `bash -n` rc 0). The previous renders are kept as `.pre-074951`-style copies.
- **New records:** predict_6.out (rc 1, the overlap found) · predict_7.out (rc 0) · predict_simforeign1219_d384.out / predict_simforeign_d384.out (rc 1, controls) · fill_5.out · launcher_check_3.out · controls_4.out · repin_dryrun_2.out · pins_gate21T2c.txt / devlog_gate21T2c.txt (over d9515f4a0).
- **`_sp/`:** scratch clones, about 3.5 GB. The launch command excludes it.

## 7. NOT done / UNMEASURED

- No launch, mail, tap, commit, push or routing-conf write. The Secuura checkout was touched with `ls-remote` / `config --get` only; every git write verb ran in scratch clones FROM ORIGIN under `_sp/`.
- **Not re-read by me:** the READY capture, the gh bodies/comments and Linear. They are the first drafter's (16:1x–16:3x AEST); the heads are unchanged, so the capture still names every head (fill_5 asserts it).
- **Not pre-run (the gate's job):** any suite, tsc, red proof, AST equivalence, stack, or legs.
- **UNMEASURED:**
  - whether a Docker stack or slot is free at launch;
  - the usage gate's state;
  - machine load;
  - the step-3b re-pin run end to end;
  - whether #1239 (tier 1, not in the batch) lands before #1219 (prompt item (j)).
