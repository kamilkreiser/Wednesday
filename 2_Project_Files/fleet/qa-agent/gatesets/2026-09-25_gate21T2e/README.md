# Gateset 2026-09-25_gate21T2e — README for Wednesday

The drafter launched nothing, sent no mail, tapped no pane and committed nothing. It wrote only under
`/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/d384786a-4d7e-451d-a78b-40a06ef20e21/scratchpad/gate21T2e/`.

This kit is ONE tier-2 gate over ONE PR, and it is the LAST round (round 2 of 2):
- **#1241** KS-1226 item 2, `b4427d416592b40eb5ddb8727b2d6c31f3c7d067` (Seat B 27th, READY 11:41:29Z).
- It is a fast-forward of the round-1 head `e2d0518df` (gate21T2d ruled NO GO).
- **ROUND 2 OF 2 is the cap. A NO GO ships nothing, and the gate describes a residue ticket for you to file.**

Routing `QA/Secuura-batch1241r2`. GO string: `GO: merge #1241 batch`.

## 1. BLUF: the gate will most likely rule NO GO (READ ONLY, strong)
The head's reader returns NULL whenever vitest prints no `passed` segment. The seat believes vitest always prints one ("`passed` emitted
unconditionally"). vitest 4.1.11 has two `getStateString` functions (read from `npm pack vitest@4.1.11`):
- `index.UpGiHP7g.js:3059`: `passed` IS unconditional. It serves the SummaryReporter window, which DefaultReporter never builds when stdout is not a
  TTY (`:3094 if (!this.isTTY) this.options.summary = false;`). This is the function the seat quoted, and round 1's report quoted it too.
- `utils.BS4fH3nR.js:91`: `passed ? … : null` is CONDITIONAL. It serves `BaseReporter.reportTestSummary` (`:2457`), which prints the final `Tests`
  line of every PIPED run, and childSuiteCounts' child is piped.

So, predicted:
- a fail-only run prints `Tests  1 failed (1)` and readSuiteCounts returns NULL;
- skip-only and todo-only runs return NULL the same way;
- the five shapes the seat captured all read correctly.

Corroboration from the seat's own record: its red runs print ` Test Files  1 failed (1)`, which is the same conditional renderer on the Test Files line
(`raise/b27-1226-red-round1.out`, `b27-1226-red-read.out`). Under your rule, NULL on any real shape = NO GO. The gate measures it (S6/S8/S9). In
practice the failure is a loud throw ("could not read the child vitest summary" plus the output tail), not a silent wrong count (§6 decision 1).

## 2. Pins (measured: predict_2.out at 11:50:32Z; re-read by repin_dryrun_2.out at 12:16Z)
- **BASE:** `aa600af94d69ad59db279d32cbbd7596931a739b`. Head's parent = `e2d0518df`, whose parent = BASE. That is 2 commits, squashed as one.
  merge-base(develop, head) = BASE.
- **Develop:** `33ccff807eb2bb0a43c5d03ceb88d877b86950e1` (#1242), 11 ahead of BASE.
  - Since round 1's develop `e68e2f0e8`, develop moved by exactly 1 commit (#1242, originate). That commit touches no systemTest/performance path.
  - Develop's blob of the file = BASE's `e4225f1e…`.
- **The merge (base-invariant):**
  - Merged tree = END_TREE `c0f0e7c91b2efd8c754becb341185ddd871874cd`.
  - diff(develop, merged) == the one path at head blob `6a52943284318375a9f7bff936769b0542355155` (100644).
  - numstat 123/3 == BASE..head. The move ∩ the path = EMPTY.
  - A second instrument (`apply --cached`) agrees.
- **Item 1 out of scope:** the matrix cell, SLOT_SENSITIVE_FILES and vitest.unit.config.ts are byte-identical from BASE to head.
- **GitHub:** compare `develop...head` → diverged, ahead 2, behind 11, 1 file. `mergeable` True (11:47:50Z and 12:16Z).
- **Instruments:**
  - `ls-remote` from the Secuura checkout (a read verb).
  - A scratch clone at `_sp/g21e_sp/clone.git`, made with `git clone --bare --no-local`. It has NO alternates file, so it never borrows from the
    shared store. The fetch from origin went into it.
  - The GitHub REST API (GET), and Linear (queries only).
  - The shared checkout was the same before and after: `count-objects` 2361 loose, HEAD `3bad652d17cf`.

## 3. What the gate owes (the prompt, `2026-09-25_secuura-1241-r2-t2.prompt.txt`, 40953 bytes)
- **LIVE-SHAPE, through the real function.**
  - L1 captures 10 piped shapes: S1–S5 are the seat's shapes, S6 is fail-only, S7 is multi-file (the C2 shape), S8 is skip-only, S9 is todo-only, and
    S10 is 2 failed + 3 passed.
  - L2 is an in-file GATE-PROBE plant that calls the module-private `readSuiteCounts` on each capture. It is restored by blob.
  - L3 plants `it.skip`, `it.todo`, `it.fails` and a failing `it` into `fixturesSlot.test.ts`, then calls `childSuiteCounts({})` end to end.
  - L4 compares the cell strings byte for byte with the captures.
  - Rule: NULL, a throw or wrong counts on ANY real shape = NO GO.
- **Red proofs:**
  - R-A: round 1's reading placed in readSuiteCounts. Predicted: R1–R4 and C2 go red, which matches the seat's "5 cells RED".
  - R-D: develop's reading. Predicted: the same five go red.
  - R-B = T-103: tamper :93 alone. Predicted: R2, R3, R4 and C1 go red, and R1 and C2 stay green because their counts are 1/1 (the seat's "4 cells RED").
  - R-C = T-CALL: tamper the call site at :157/:161. Predicted: all 10 cells stay GREEN, so the result is NOT-PINNED CALLSITE, and C6's comment
    overclaims.
  - R-E: the head untampered.
- **Package suite:** predicted BASE 1085, head 1095, develop 1089, merged 1099, each with the one pre-existing PRESUITE-URLPATH red.
- **Typecheck:** the seat's `tsc -p tsconfig.json` is vacuous, because tsconfig excludes `tests`. The gate runs a per-file typecheck.
- **Leads:** (b) renderer, (c) callsite, (d) symmetric fixtures, (e) first-match, (f) stale PR title/body (round 1's), (g) no raw captures in the seat
  record, (h) the seat's disclosures, including "There is no N-4".
- **Fleet STOP:** NOT claimable. The push was format gate only, which the gate confirms by READ. No standalone suite run.
- **No Docker and no DB.**

## 4. The routing line is NOT written by the drafter. Add it FIRST (`PROPOSED_inbox_routing_line.txt`)
    QA/Secuura-batch1241r2|coagent@agentmail.to|yes
The drafter's read: `QA/Secuura-batch1241r2` is ABSENT (0), and round 1's `QA/Secuura-batch1241` is present (1). Without the new line, repin step 0
refuses with rc 1. Controls R4 and R4b prove this; R4b shows that round 1's line alone does not satisfy step 0.

## 5. THE ONE LAUNCH COMMAND (copy to gatesets/ + re-pin + launch; run it in a shell that can reach tmux)
    /usr/bin/rsync -a --exclude '_sp' /private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/d384786a-4d7e-451d-a78b-40a06ef20e21/scratchpad/gate21T2e/ /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-25_gate21T2e/ && /bin/bash /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-25_gate21T2e/repin_and_launch_gate21T2e.sh /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-25_gate21T2e/launch_qa_secuura_1241-r2-t2.sh <your session scratchpad under /private/tmp/claude-501/>

Step 0b sees a MOVED KIT and re-runs predict and fill at the new home in the same action. Both re-read origin and refuse on any disagreement. Predict
makes a fresh `--no-local` clone under `<scratchpad>/g21e_sp` (about 20 s) and runs `npm pack vitest@4.1.11` there. Controls R6 and F1 prove the moved
kit works.

The steps and their refusal codes:
- 0 routing (1)
- 0b moved kit: predict + fill (8)
- 1 ls-remote (2)
- 2 pulls API + `mergeable` (3)
- 3 head == pin on both instruments, open, not `mergeable:false` (11)
- 3b develop moved → predict + fill, then develop re-read (10)
- 4 usage gate (12)
- 5 `--check` (13)
- 6 `cockpit.sh add QA/Secuura-batch1241r2` (14), then a pane census

**Rehearsal:** append `--dry-run` to rehearse steps 0–3. `repin_dryrun_1.out` and `repin_dryrun_2.out` both ended rc 0, the second at 12:16:05Z.

## 6. Decide or know before launching
1. **The predicted NO GO is a loud misattribution, not a silent wrong count.**
   - A fail-only child makes childSuiteCounts throw with the output tail. In the matrix (7 files, >100 tests) a fail-only summary needs every test to fail.
   - Your rule, as carried in the prompt, makes it NO GO anyway, and at round 2 that ships nothing.
   - If you would rather rule a loud refusal on fail-only / skip-only / todo-only as acceptable, change THE RULE in the prompt before launching and
     re-fill. The launcher's exit 40 anchors on the sentence `NULL, a throw, or wrong counts on ANY real shape is NO GO for #1241 (blocking)`.
   - The drafter recommends launching as drafted. The measurement costs minutes, and the residue ticket then carries MEASURED lines.
2. **"There is no N-4" is wrong by READ.** The round-1 report.md:188 lists `N-4 (Minor, standing) INTEGRATION-UNWIRED` for #1242, a TICKET-class
   finding marked SHIPS-WITH. The seat asked you to send it if it exists. That answer is yours to give; the gate only confirms it.
3. **The PR title and body are round 1's.** The title reads "…regex accepts an optional skipped segment". The body says vitest prints skipped
   between failed and passed, and that the cells scrape the source. The gate proposes a squash subject from the round-2 bytes. Whether the seat must
   edit the body is yours to decide.
4. **The seat record has no raw fixture captures** for its five "CAPTURED" lines (lead g). The gate's own captures are the evidence.
5. **`mergeable: null` policy**, as in gate21T2d: null is reported after 3 reads, not refused. `false` refuses.

## 7. Controls: `controls_gate21T2e.sh <scratchpad> [--invert]`
- **controls_1.out: 91 OK / 0 MISMATCH of 91**, rc 0, to 12:06:25Z.
- **controls_2.out (`--invert`): 0 OK / 91 MISMATCH of 91**, rc 1, to 12:15:17Z. Every control can fail.
- Covered:
  - launcher: P, C, C2 (the round-1 head pinned), D, V, O, G, U, H20, T, I, I2, K, B, B2, S, S2, X, X2, F, F3, Y–Y3, Hh, H2, Q–Q3, R, R2, CAP, Z,
    IT1, A, E, J, W, N, N2, M;
  - repin: R1–R6 and R4b;
  - predict: P1 (a FOREIGN edit of the PR's own file over develop → refuses) and its twin;
  - fill: F2 (refuses SIM pins) and F1 (moved-copy re-fill + `--check`).
- Every doctored arm has a pristine twin through the same override. The doctored arms are pinned to the launcher's develop.
- `predict_simforeign1241_1.out`: rc 1, with 8 hard fails (the negative control at home).

## 8. Files
- COMMISSION.md · README.md · PROPOSED_inbox_routing_line.txt
- The pins:
  - predict_gate21T2e.py and predict_1.out (rc 1). The one hard fail was the drafter's own check matching a comment line, and it was fixed.
  - predict_2.out (rc 0, the pinned run) and predict_simforeign1241_1.out (rc 1).
  - pins_gate21T2e.json and its SIM file.
- The prompt and launcher:
  - prompt_gate21T2e.TEMPLATE.txt and launcher_gate21T2e.TEMPLATE.sh.txt;
  - fill_gate21T2e.py with fill_1.out (a seat-item wrap refusal, fixed), fill_2.out and fill_3.out (rc 0);
  - the rendered prompt;
  - the launcher `launch_qa_secuura_1241-r2-t2.sh` (`bash -n` rc 0; the `.pre-215844` file is its pre-fix fill);
  - launcher_check_1.out and launcher_check_2.out (rc 0).
- The repin and controls: repin_and_launch_gate21T2e.sh with repin_dryrun_1.out and _2.out (rc 0); controls_gate21T2e.sh with controls_1.out and
  controls_2.out.
- The captured reads:
  - mail_gate21T2e_ready.md and mail_seatB27th_ready_1241r2.md (verbatim; TEXT_SHA256 `68d332d2…`; the round-1 report's sha256 `ef04788f…`,
    41708 B), from capture_mail_gate21T2e.py;
  - gh_read_gate21T2e.py with gh_read_1.out, gh_body_1241.md and gh_comments_1241.md;
  - linear_reads_gate21T2e.py with linear_reads_1.out and linear_KS-1226.md.
- The `launch_1205xx/1214xx.routing.out` files are control R4/R4b artefacts.
- `_sp/`: the scratch clone, the vitest tarball and the control workdirs. The launch command excludes it.

## 9. NOT done / NOT measured by the drafter
- No launch, mail, tap, commit, push or routing-conf write.
- The Secuura checkout was touched only by read verbs: ls-remote, show, diff, cat-file, config --get, count-objects, and `clone --no-local` reading it
  as a source. The seat record was read as plain files.
- The inbox was read only in the one permitted form (`inbox_digest.sh full wednesday-agent@agentmail.to '<id>'`).
- UNMEASURED:
  - every live vitest shape, including whether fail-only really prints without `passed`;
  - every red arm, T-CALL, the package counts and the typecheck;
  - the usage gate and the machine load at launch;
  - the real launch path (step 6).
- Not controlled: exit 16 (it needs a TTY), the repin's `mergeable=False` refusal, and step 4–6.
