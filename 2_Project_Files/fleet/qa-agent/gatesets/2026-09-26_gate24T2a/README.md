# Gateset 2026-09-26_gate24T2a — README for Wednesday

The drafter launched nothing, sent no mail, tapped no pane and committed nothing. It wrote only under
`/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/d384786a-4d7e-451d-a78b-40a06ef20e21/scratchpad/gate24T2a/`.

This kit is ONE tier-2 BATCH gate over FOUR PRs from ONE seat (Seat L6), WIDENED to four and FROZEN by your message:
- **#1243** KS-1117 + KS-1300 items 2-4, `0c89e2b503d9333829c277c50ad3b1a33f03cb96` (READY 13:27:44Z) — 5 files, systemTest/performance.
- **#1244** KS-1111, `146b620fda53f008b3384334a474b06a16235af3` (READY 13:35:31Z) — 2 files, systemTest/performance.
- **#1245** KS-1313, `1700b5ae7dd56ad3e30602a40b20ae6469c35350` (READY 13:52:45Z) — 1 file, systemTest/performance. #1241 NOT graded.
- **#1248** KS-1143 GF-2, `2b4960172644b5ef0414b94d46d11974012c2007` (READY 14:10:18Z) — 1 file, Blockchain/Dev/packages/shared.

Routing `QA/Secuura-batch1243`. GO string: `GO: merge #1243, #1244, #1245, #1248 batch` (or the subset).

## 1. BLUF
- **Kit: READY to launch** once you add the routing line (§4). Every head re-read at 14:22:43Z on two instruments; `mergeable` True on all four.
- **#1245 — predicted NO GO under your rule as written (drafter's LIVE capture through a LIFTED reader — a PREDICTION, the gate measures):**
  - Every MANDATED shape reads correctly (fail-only {0,1}, skip-only {0,0}, todo-only {0,0}, expected-fail+pass {1,0}, fail+pass+skip {1,1},
    pass-only {1,0}, multi-file {1,1}); so do all-failed, every-label, orientation, beforeAll-throw, ctx.skip and an unexpected it.fails pass. The
    label-set + sum design is right, and vitest 4.1.11's renderer (READ) confirms the seat's label and sum claims.
  - BUT the new LAST-line rule reads `${stdout}\n${stderr}`, and vitest prints failure detail and console.error on STDERR, after the summary. Two
    real piped outputs read WRONG, silently, hiding a failure:
    - S17: a test `console.error`s `      Tests  5 passed (5)`, plus one failing test → **{5,0}** (real summary `1 failed | 1 passed (2)`).
    - S18: NO console output — one ordinary failing `toBe` between two strings sharing a `Tests  9 passed (9)` line (vitest prints the diff context on
      stderr) → **{9,0}**.
  - The last-line rule came from the t2e report's own residue fix-shape and KS-1313's text ("Take the LAST Tests line"); the gate names that slip.
  - Reach today: probably none (the seven slot files had 0 console writes at t2e); the gate measures it. See §6 decision 1.
- **#1243 — predicted GO WITH FINDINGS:** the BOM strip is one correct line; findings MULTILINE-IMPORT (a multi-line or split `from` import evades
  `parserImportSites`, port), CANARY-IN-PACKAGE (a scratch dir inside the package root, un-ignored), T2C-ROUTING-HOME (t2c's original ROUTING finding
  is not what KS-1300 item 3 now says).
- **#1244 — predicted GO WITH FINDINGS:** the fallthrough fixes all seven QA-961-1 argvs (port), the name set is byte-identical; finding
  UNROWED-SIBLINGS: L01/L04/L05/L07 with a secret name leak at BASE and are masked at head, and no row pins them. The seat's "placeholder NAME, so
  clear is correct" does not survive a secret name.
- **#1248 — predicted GO WITH FINDINGS if T-2 reds W8** (the seat's A1 did; the gate re-runs it FIRST). It is a faithful cherry-pick of L3's
  `a40cb9eea049` (patch-id and blob equal). The push log (READ, anchored) carries 28/0, 6/0, 60 of 60 and `PREFLIGHT INCOMPLETE — 12/15`, with legs
  3/4/8 skipped. Lead CONT-DEFERRED (a guard defined but never called in the continuation reads true; pre-existing, unsafe direction).

## 2. Pins — measured by predict_4.out at 14:21:02Z; re-read by repin_dryrun_1.out at 14:22–14:23Z
- **BASE:** `6e2a00bfed577528de1ee02b41cb5a0e99172b35`. Every head is ONE commit whose parent is BASE.
- **Develop:** `77c6426b96d9e48a758e68fa56e9138dc8509aa8`, 2 ahead of BASE. It moved TWICE while drafting:
  - #1246 `14cc526d1` (KS-1312): originate files.
  - #1247 `77c6426b9` (KS-1294 HOOKPROSE): `.githooks/pre-push` +7/-2. Every changed line is a comment (READ), and it landed after #1248's push.
  - The move ∩ every PR's paths = EMPTY. No systemTest/performance path moved.
- **Merged trees over 77c6426b9** (from the pins file, re-derived at 14:21Z): #1243, #1244, #1245 and #1248 each merge clean; checks (1)-(3) hold for all four.
- **END_TREE `c647fd4349b89094fcf337c348730fcbfe261069`:**
  - identical in all 24 merge orders;
  - `apply --cached` agrees;
  - 9 files over develop, every blob == its head blob.
- **PAIRWISE PATH-DISJOINT:** all 6 pairs are EMPTY.
  - The only co-residence is at DIRECTORY level: `tests/unit/utils/` holds both #1243's yamlRedaction.test.ts and #1245's file. It is not an overlap.
  - The merged-blob target of every path is its head blob.
- **#1241:** `b4427d4165` unchanged; it CONFLICTS with the END_TREE (merge-tree rc 1). Context only, not graded.
- **GitHub:** compare develop...head → merge_base BASE, ahead 1, behind 2, files == own paths (launcher --check). `mergeable` True ×4 at 14:23Z.
- **Instruments:**
  - `ls-remote` from the Secuura checkout (a read verb);
  - a scratch clone at `_sp/g24a_sp/clone.git` (`git clone --bare --no-local`, NO alternates), fetched from origin;
  - REST GET;
  - Linear queries only;
  - the seat record read as plain files;
  - `npm pack` of vitest / @vitest/runner 4.1.11;
  - an `npm ci` of the #1245 head's own lockfile under `_sp/pkg` for the drafter's live captures.

## 3. What the gate owes (the prompt `2026-09-26_secuura-batch1243-t2.prompt.txt`)
- **#1245 LIVE-SHAPE, through the real function:**
  - L1 captures S1-S18: the seven mandated shapes, eight more real shapes, and three LOOKALIKE shapes, with the streams kept SEPARATE.
  - L2 is a GATE-PROBE in-file that calls `readSuiteCounts` on `${stdout}\n${stderr}`.
  - L3 plants E1-E5 through `childSuiteCounts({})`. E5 is the stderr lookalike inside the real child.
  - L4 compares byte for byte against the CAPTURED literals and the seat's archived captures.
  - THE RULE is yours: NULL or wrong on ANY real shape = NO GO. The prompt states that the lookalike shapes fall under it (§6 decision 1).
- **Red proofs, per PR, in the tester's own clone:**
  - #1243: A-0 (develop's yaml.ts → B1+B2 red), A-1, A-2, K-1..K-4, an indented-import plant over develop (green) vs head (red), and a MULTILINE plant
    (predicted green).
  - #1244: M-0 (develop's k6_docker.ts → exactly L02, L03, L08), T-1, T-6, T-5, and UNROWED-SIBLINGS probes.
  - #1245: R-D (develop's reading → 10 red, port), T-103 at :210 (4 red + the matrix), T-FIRST, T-NOSUM, T-DUPOK, T-CALL (i)/(ii)/(iii), and R-E.
  - #1248: **T-2 FIRST** (W8 must red, else NO GO), then A-2, A-3, A-4, the RED-AT-BASE plant of W7/W8 over develop, REAL-TREE-DELTA and
    CONT-DEFERRED.
- **Suites, serial:**
  - systemTest/performance: BASE 1089, heads 1097 / 1096 / 1107, END 1122 (predicted), with the PRESUITE-URLPATH red in a spaced path.
  - packages/shared: 928 → 930.
  - `npm run lint` (both tsconfigs + eslint), prettier, knip delta.
- **Fleet STOP:** CLAIMABLE ONLY FOR #1248, BY READ of its push log. The other three pushes were format-gate only. No standalone runs.
- **No Docker, no DB.** Time-box 180 min.

## 4. The routing line is NOT written by the drafter. Add it FIRST (`PROPOSED_inbox_routing_line.txt`)
    QA/Secuura-batch1243|coagent@agentmail.to|yes
The drafter's read: `QA/Secuura-batch1243` is ABSENT (0 lines). Without it, repin step 0 refuses with rc 1 (controls R4 and R4b prove it).

## 5. THE ONE LAUNCH COMMAND (copy to gatesets/ + re-pin + launch; run it in a shell that can reach tmux)
    /usr/bin/rsync -a --exclude '_sp' /private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/d384786a-4d7e-451d-a78b-40a06ef20e21/scratchpad/gate24T2a/ /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-26_gate24T2a/ && /bin/bash /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-26_gate24T2a/repin_and_launch_gate24T2a.sh /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-26_gate24T2a/launch_qa_secuura_batch1243-t2.sh <your session scratchpad under /private/tmp/claude-501/>

Step 0b sees a MOVED KIT and re-runs predict and fill at the new home, in the same action. Both re-read origin and refuse on any disagreement. Predict
makes a fresh `--no-local` clone under `<scratchpad>/g24a_sp` (about 20 s) and runs `npm pack vitest@4.1.11` there. Controls R6 and F1 prove that the
moved kit works.

The steps and their refusal codes:
- 0 routing (1)
- 0b moved kit: predict + fill (8)
- 1 ls-remote (2)
- 2 pulls API + `mergeable` (3)
- 3 heads == pins on both instruments, open, not `mergeable:false` (11)
- 3b develop moved → predict + fill, then develop re-read (10)
- 4 usage gate (12)
- 5 `--check` (13)
- 6 `cockpit.sh add QA/Secuura-batch1243` (14), then a pane census

**Rehearsal:** append `--dry-run`. `repin_dryrun_1.out` ended rc 0 at 14:23:35Z.

## 6. Decide or know before launching
1. **#1245 and the LOOKALIKE shapes.**
   - As drafted, the prompt carries your rule literally: S16-S18 and E5 are real vitest output, so wrong counts there = NO GO for #1245.
   - The drafter predicts the gate will measure {5,0} and {9,0}. A NO GO would be ROUND 1 OF 2 for #1245: it goes back to the seat, and the
     fix-shape is to read stdout alone, or the `Tests` line after vitest's own ` Test Files` line.
   - If you would rather grade the lookalike class by REACH (as t2e ruled its mirror-image FIRST-MATCH, Minor), edit that sentence in the prompt
     TEMPLATE before launching, and re-fill. The launcher's exit 40 anchors on `The LOOKALIKE shapes S16-S18 and E5 are REAL vitest output and fall
     under THE RULE as written`, so change that anchor in the launcher template too.
   - The drafter recommends launching as drafted. The measurement is minutes, and the silent direction (a failing child read as green) is the one the
     three attempts exist to kill.
2. **#1248's preflight is 12/15.** Legs 3/4/8 SKIPPED (local stack not up). The seat asks whether 12/15 with nothing failed is acceptable for a
   packages/shared test-only change, or whether it should start the stack and re-push. The gate reports the legs as NOT run; the call is yours.
3. **Two titles fail MG-11 as squash subjects.** #1243 is 102 chars and #1245 is 96. The gate proposes subjects from the bytes.
4. **The seat's environment-gap question** (packages/shared has no own vitest dependency; `npm ci` in the member exits 127): the seat asked "Do you
   want a ticket?". The gate grades it (lead l), never blocking.
5. **Develop moved twice during drafting** (#1246, #1247). Step 3b re-pins in the launch action if it moves again. A move that touches a PR's own
   path refuses and must be re-predicted by hand.
6. **`mergeable: null` policy**, as in gate21T2d/e: null is reported after 3 reads, not refused. `false` refuses.

## 7. Controls: `controls_gate24T2a.sh <scratchpad> [--invert]`
CONTROLS_SUMMARY

## 8. Files
- COMMISSION.md (with the §2a LEGITIMATE SHAPES tables) · README.md · PROPOSED_inbox_routing_line.txt
- **Pins:**
  - predict_gate24T2a.py;
  - predict_1.out (the 3-PR draft, rc 0), predict_2.out (rc 1: the drafter's own check hit an 8-space `walk(body);`; fixed), predict_3.out
    (rc 0, over 14cc526d1), predict_4.out (rc 0, the pinned run, over 77c6426b9);
  - predict_simforeign<n>_1.out (the negative controls at home);
  - pins_gate24T2a.json and its SIM files.
- **Prompt and launcher:**
  - prompt_gate24T2a.TEMPLATE.txt and launcher_gate24T2a.TEMPLATE.sh.txt;
  - fill_gate24T2a.py with fill_1.out (rc 1: develop had moved, a correct refusal), fill_2.out, fill_3.out and the later fills (rc 0);
  - the rendered prompt `2026-09-26_secuura-batch1243-t2.prompt.txt`;
  - the launcher `launch_qa_secuura_batch1243-t2.sh` (`bash -n` rc 0);
  - launcher_check_*.out (rc 0). `.pre-*` files are earlier fills.
- **Repin and controls:** repin_and_launch_gate24T2a.sh with repin_dryrun_*.out; controls_gate24T2a.sh with controls_*.out.
- **Captured reads:**
  - mail_gate24T2a_ready.md and mail_seatL6_ready_<n>.md (verbatim; TEXT_SHA256 per READY; prior-report sha256s), from capture_mail_gate24T2a.py;
  - raw_ready_*.txt (the drafter's first reads, the same form);
  - gh_read_gate24T2a.py with gh_read_1/2.out, gh_body_<n>.md and gh_comments_<n>.md;
  - linear_reads_gate24T2a.py with linear_reads_1/2.out and linear_KS-*.md.
- **Drafter's live shapes (PREDICTION only):** drafter_liveshape_g24a.sh, liveshape_1.out, liveshape_2.out, liveshape_lift_2.out.
- `_sp/`: the scratch clone, the npm packs, the `npm ci` package, the live fixtures and the control workdirs. The launch command excludes it.

## 9. NOT done / NOT measured by the drafter
- No launch, mail, tap, commit, push or routing-conf write.
- The Secuura checkout was touched only by read verbs (ls-remote, config --get, and `clone --no-local` reading it as a source). The seat records were
  read as plain files.
- The inbox was read only in the one permitted form (`inbox_digest.sh full wednesday-agent@agentmail.to '<id>'`).
- UNMEASURED:
  - every live shape through the REAL `readSuiteCounts` (the drafter's reads went through a LIFT);
  - L3 through `childSuiteCounts`;
  - every red arm of every PR, and T-2 on #1248;
  - the package counts, lint, knip and prettier;
  - #1248's REAL-TREE-DELTA and CONT-DEFERRED probes;
  - the reach greps;
  - the usage gate and the machine load at launch;
  - the real launch path (steps 4-6).
- Not controlled: exit 16 (it needs a TTY), the repin's `mergeable=False` refusal, and steps 4-6.
