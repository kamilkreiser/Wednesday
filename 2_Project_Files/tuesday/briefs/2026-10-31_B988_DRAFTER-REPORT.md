STARTABLE: yes, after the stamp, with one timing caveat: `Analyze (csharp)` on the new head was still in progress at 14:47, so the gate will spend its CodeQL wait (up to 40 min) before it can finish. Q-1 to Q-6 below have defaults; nothing blocks the launch.

# B988 drafter report (read-only; Sat 31 Oct 2026 14:47-14:58 AEDT)

**BLUF.** Kit `2026-10-31_B988_SEAT-G240_mps-133-v4-engine-gate-tier1-round2.md` (29 lines, same shape as B980): Opus tier-1 gate, ROUND 2 OF 2 on class "V4 engine: page basis and rental projection", PR #133 at head `30ea76dab66179bcebeeb048f94844e8cb303666`, three commits. It re-judges the whole PR, proves B980-1 closed with the gate's own harness under InputHash's options AND ApiJson (purchase result alone and whole, no strip, expected 0 of 13 differing files, control reproducing 12 of 13 at `1d49328`), proves the B980-3 row dies under N8, re-runs hand cases, projection, N1-N10 and MU1-MU6, adds N11-N13 for the new fix, writes the CI line with TMPDIR outside git (probe required), reads CodeQL at the new head, and states in the kit that a NO GO is NO GO 2 of 2, the round cap, to the product owner. Nothing was built, run, fetched or sent.

## Measured (gh -X GET under the project GH_CONFIG_DIR; git ls-remote; tmux; uptime)
- `pulls/133` 14:47: open, draft false, head `30ea76da...`, base `1a2a0294...`, commits 3 (`790e224b`, `1d493283`, `30ea76da`), +731 -22, 9 files, mergeable_state blocked. Files numstat: ENGINE.md 3/0, PurchaseCalculator 16/9, QuoteCalculator 64/7, PurchaseInput 4/1, QuoteInput 17/1, CalculationResult 33/2, PurchaseResult 8/2, RecurringProjectionTests 193/0, VolumeBasisTests 393/0. Compare `1d49328...30ea76d`: 4 paths, ENGINE 1/1, PurchaseCalculator 1/1, PurchaseResult 4/1, VolumeBasisTests 45/1 (+51 -4); `compare main...head` ahead 3 behind 0.
- `ls-remote` branch = head; main `1a2a0294...` (equal to `git/ref/heads/main`). Open PRs 133, 121, 120.
- Commit 3 message read whole (one trailer, `Co-Authored-By: Claude Opus 5.5`, unverified). Builder STATUS 214 lines, last line READY FOR QA at the new head.
- Check-runs on the head at 14:47: CodeQL completed/neutral; python completed/success; Analyze actions, python, javascript-typescript completed/success; **Analyze (csharp), dotnet, web in progress**; workflow runs `ci` and `PR #133 dynamic` in progress. Analyses on `refs/pull/133/head`: 7 rows (3 on the new head, 4 on `1d49328`; no csharp on the new head yet), results_count 0 each. Open code-scanning alerts on the PR ref: 0 (no positive control, said in the kit). ci.yml blob sha equal at head and main (`212b0da1...`). Squash settings `COMMIT_OR_PR_TITLE` / `COMMIT_MESSAGES`.
- PR title unchanged. PR body unchanged since round 1 (read whole): stale sentences are "9 files change, +684 -22", "Two commits, one per ticket", "Tests (...on 1a2a0294): Engine 451 ... 16 new tests", "6 of 6 planted defects", the byte-equal sentence, and the emoji line; "the purchase result is unchanged" was false at `1d49328` and is true at the head. The kit lists these for Tuesday.
- Round count: `Briefs/*_STATUS.md` 285 files; first lines starting `GATE VERDICT` 65; naming `#133` or `b974`: 1 (`2026-10-31_B980_STATUS.md`, NO GO, round 1 of 2). Control: the loop listed that file by name. So NO GO 1 of 2 before this gate; this is round 2 of 2.
- Routing: G1 `model-routing.md:108`, G-cap `:111`; `models_latest.json` opus `claude-opus-5-5`.
- Ports: none needed; fallback block 9550-9559: `lsof -nP -iTCP:9550-9559 -sTCP:LISTEN` empty (rc 1; control not run, so a zero is a suspect only for the fallback, which is unused); word-boundary scan of the Oct 30-31 SEAT kits for `955[0-9]` 0 files.
- Panes 14:47: `%0` tuesday, `%103`, `%102`, `%101`, `%93` (MPS builder, parked), `%1`; no `Datasec/MPS-G240`. `G240` and `B988` in earlier briefs: 0 files (last G in use G239, last B in use B987). load1 7.07 (above the gate threshold, the launcher's wait handles it).
- TMPDIR probe: `/private/tmp/claude-501/probe-b988`: `git rev-parse --show-toplevel` -> "not a git repository" (rc 128); the project root prints its top level (control). So `/private/tmp/b988-seat-tmp` is a valid shape; the kit makes the gate re-probe.
- Kit: 0 non-ASCII bytes (`tr -d` count 0); four-underscore lines 8; last line bare `READ-WHOLE-BY-TUESDAY: ____`; no decision-card id; no person name.
- Read whole: DRAFTER_RULES, B980 kit and report, B980 STATUS (166 lines), B974 STATUS (214), ADDENDUM-1 and -2. Not read: engine source, evidence sources (the kit points the gate at them).

## D-decisions made
- D-1 Hand cases: the gate may READ the round-1 gate's hand-case sources (text in `B980_evidence/`) and re-run them in its own mutant tree, but must write the B980-1 and quantity-0 rows BEFORE reading the builder's V and Z. Reason: kit item "re-run the round-1 hand cases" needs the source; the new rows keep independence.
- D-2 The builder changed its own row G (PerDevice -> null on a purchase line); the round-1 gate's file probably asserts PerDevice too. The kit pre-classifies a red caused by that single assertion as a ROW TO UPDATE, not a defect, and requires the gate to name it.
- D-3 Two serializers, separate passes (InputHash's options write nulls, which is why the fix needs `JsonIgnore`); a record dropped by an ApiJson spy is an instrument limit, counted and said.
- D-4 N11 (JsonIgnore removed), N12 (round-1 defect restored), N13 (fix inverted) added; N8 surviving the builder's rows is Major (B980-3 not closed).
- D-5 CodeQL: csharp at the new head still absent after the wait is reported PENDING, not a Blocker, not a pass (matches round-1 Note list).
- D-6 Rental result still gains new JSON members: out of scope by ADDENDUM-2, a Note.

## Questions for Tuesday (each with a default)
- Q-1 Round and class: round 2 of 2 on "V4 engine: page basis and rental projection", NO GO 1 before. Default: yes.
- Q-2 May the gate read B980's evidence text (hand-case sources) as data? Default: yes (D-1); `.tools/b980/` stays forbidden to run or copy.
- Q-3 TMPDIR location: `/private/tmp/b988-seat-tmp` (outside any git tree, outside the project folder). Rule 1 says project writes stay in the project; a temp dir is not project state. Default: yes, with the probe; fall back to the session scratchpad.
- Q-4 If the quantity-0 choice (B980-2) still differs from per-device quantity-0: Note. Default yes.
- Q-5 Squash text: explicit `--subject` and `--body`, ASCII, no person, no B-number, one trailer, ticket keys allowed in the subject. Default yes. The body edit (stale sentences) is Tuesday's, before landing.
- Q-6 Launch timing: `Analyze (csharp)`, `dotnet`, `web` were still running; launching now costs the gate an extra wait. Default: launch after they complete if load1 is still above 7; otherwise launch (the gate can wait up to 40 min).

## Stamp values suggested
S1 `STAMPED <time> AEDT 2026-10-31 by <seat>`; S2 until 2026-11-01 02:00 AEDT, one waiter at load1 below 7, MPS pane M52 parked beside; S3 Q-1..Q-6 answered, round 2 of 2; S4 the product owner's 2026-10-16 merge-once-tested grant and the 11:55 live-board words, YES to the one in-clone fetch, scratch mutant tree, own harness build, own gitleaks run; S5 target 3 h, hard stop 5 h after the Step-0 date; S6 read at the stamp (head, main, all Analyze statuses); S7 model receipt and load1.

## UNMEASURED
Whether the gate's ApiJson spy will compile against `MpsCalc.Api` in its tree (the builder's did); whether the round-1 hand-case file asserts PerDevice on a purchase line (assumed, from the B980 STATUS row text); whether `/private/tmp` survives a reboot mid-run; CodeQL csharp at the new head; the dotnet job result at the new head.

## Outside the fences
None: only `gh api -X GET` under the project GH_CONFIG_DIR, `git ls-remote`, tmux/lsof/uptime reads, reads of briefs and the project STATUS files, one `mkdir` and `rmdir` of an empty probe dir under `/private/tmp/claude-501/` (not the scratchpad; harmless, removed), and writes only to the two output files. No decision_queue, no ledger, no fleet/briefs_staged, no scoreboard read.
