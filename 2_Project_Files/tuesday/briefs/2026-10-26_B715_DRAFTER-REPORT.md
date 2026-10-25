STARTABLE: YES (needs your stamp, Q-1 answer, and a launch at load1 below 7; PR #118 checks were still in_progress at drafting, so the gate polls them)

# B715 DRAFTER-REPORT: SEAT-G135, MPS gate of PR #118 (MPSCALC-302), tier 1, Opus, round 1 of 2

Drafted 2026-10-26 08:20-08:3x AEDT, clock from `date`. Kit: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-26_B715_SEAT-G135_mps-118-parity-multiset-gate-tier1.md` (99 lines).

## BLUF
- Tier-1 gate kit built from the B700 shape, raised: 9 checks (C1-C9), 6 named mutants plus 10 of its own (Q1-Q10), 8 forcing rows (F1-F8), 12 false-refusal cases (L1-L12), a three-seed set, and a Blocker grade for any false refusal on a legitimate store.
- Pins: head `39e51272...`, main `f5a27af0...`, merge ref `19759df3...`; ports 9820-9829 free; no `Datasec/MPS-*` pane live; no heavy slot held.
- Model: Opus `claude-opus-5-5` (row G1, `model-routing.md:108`); launch line carries `BRIEF_SEAT_LEVEL=opus`.
- Round count: NO GO 0 of 2 on the class (no earlier NO GO on the parity panel check).
- CI was still running at drafting: the head has 1 of 4 CodeQL analyses; the kit expects 4 of 4 before a GO.

## Facts re-measured (instrument, control)
- `ls-remote` (retry-free, first try): main `f5a27af0a4994a884c739e7892181b71ae0e4b72`; branch and `refs/pull/118/head` `39e51272b6b2733d50764e4277f8f0158e8f0794`; `refs/pull/118/merge` `19759df31bb2f01848d2fcc639abf1b394ad32a7`; #117 head `6e34f07a`, #112 head `f2102e35` unchanged; `refs/heads/b715*` none (control: `b711*` lists the builder branch).
- `gh api -X GET pulls/118`: open, not draft, 1 commit, 2 files, +158 -2 (`ParityProof.cs` 9/2, new test file 149/0), mergeable true, state blocked (checks pending). Title and body carry the key and one `Co-Authored-By: Claude Opus 5.5` line.
- Check-runs at the head: umbrella CodeQL `neutral`, the other 7 `in_progress`. `code-scanning/analyses` for the PR head: 1 row (actions); main returns 4 per commit (control). Open alerts 0 at PR head and main (no positive control for a zero; the kit says so). Ruleset thresholds re-read: errors / high_or_higher.
- `ci.yml` at main: dotnet job line 30, build line 42, test line 43, timeout 20, no SQL step (`grep -c -i sql` filter control `dotnet` > 0 in the same read). `TreatWarningsAsErrors` count 1 in `Directory.Build.props` at the head.
- Product hunk read whole (`git show 39e51272 -- src`): the 2 old lines replaced by `owed` / `have` sorted lists and `SequenceEqual`; refusal line untouched. Fixed callers of `ParityProof.Run` (`git grep -F`): 5 test files plus `tools/MpsCalc.ImportCli/Program.cs:112` (the `prove` command); none in `src/MpsCalc.Api`.
- Ports 9820-9829: `lsof` rc 1; bind control (python on 127.0.0.1:9820) listed 2 lines rc 0, freed, rc 1 again. Word-boundary scan of the 104 non-`.pre-` SEAT kits of 25-26 Oct: 5 hits (B632, B689 NexusAI finished lanes; B658, B662 only in their own control sentence; B655 a false hit inside a sha256 string); zero live kits (B710-B713). Control: `978[0-9]` on B711 fires 4 lines.
- Panes (`tmux list-panes -a`): tuesday, NexusAI-M14, Security-Composer-J19 and G133, HPSM-POC-H28 and H29, fleet-monitor. No MPS pane. `ls -d` of `.tools/heavy-slot*` and `.tools/b715*`: no matches.
- Load: `uptime` 5.44 8.17 8.40 at 08:21; 9.00 9.19 8.75 at 08:20. Kit says the gate waits for load1 < 7 per heavy job.
- Model id: `models_latest.json` `levels.opus.model_id` = `claude-opus-5-5` (sonnet `claude-sonnet-5-5` at line 23 for contrast). Row G1 is at `model-routing.md:108`, G-cap at `:111` (G1 line confirmed by grep; G-cap by position after G2 `:109` and G3 `:110`, read from the table order, not re-grepped).
- Round count frame: first line of 245 `Briefs/*_STATUS.md`; 49 open with `GATE VERDICT` (control: B700 matches); 4 name panel/parity (B305, B324, B348, B365), all GO WITH FINDINGS, none a NO GO on this mechanism.
- Fact marks and `CLARIFICATIONS.md:809` landing line quoted from the template's quotation, and re-read: the line holds "squash with the head pinned (`--match-head-commit`, the MPS convention, entry 04:52 above)".

## Corrections to the brief's framing (a contradiction wins)
- The task text says the gate checks "the workbook-derived owed set". In the product the owed set is derived from the STORE (block SKUs, mapped devices, held pairs), not from the workbook; the workbook is the other side only for the governed records. The kit says so and frames C3 around importer output.
- "A non-synthetic fixture if one exists": none exists in the repo. `ls-tree -r --name-only` at the head matched no `.xlsx`, `.xlsm` or store sample (control: it matches `purchase_bom_synthetic.json`). Real books are confidential and forbidden by the rules, so the kit marks the real-book `prove` run NOT TESTED, product owner's, and gives the command location.
- Test file is +149 (not stated in the task): total +158 -2.

## D-decisions
- D1: Opus model, tier-1 weight: mutants Q1-Q10 target the new comparison and the inputs it inherits (device placement from panel records, un-deduplicated `b.Skus`, first-block-wins), and F1-F8 force count-preserving tampers the committed rows do not name.
- D2: False refusal (C3) is an Escalation and a Blocker, because the change from a count to a multiset is exactly where a legitimate store could newly be refused.
- D3: The kit keeps the builder's P6 credit on an old row as a Note, and asks the gate to re-measure it.
- D4: Hard stop slot text: 150 min target, 4 h hard stop (Tuesday fills absolute times).
- D5: Seeded edits use `random.Random(715101)` (not any earlier gate seed listed in the kit).

## Q-questions for Tuesday
- Q-1 (stamp slot): may the gate build mutants and scratch rows in `.tools/wt-b715-mut`? Default: YES (C2 and C3 need it).
- Q-2: Should the gate wait for the PR's `dotnet` / CodeQL runs to finish (poll up to 30 min after its last heavy job), or give a conditional verdict earlier? Default: poll, as written; `CI pending` is conditional.
- Q-3: Launch order against the three open PRs: #117 and #112 may land first and move main; the kit's main-moved rule (STOP only if an Import, parity-test, CLI, docs/IMPORTER or CI path moves) handles it. Default: as written.

## UNMEASURED
Everything the gate will run: builds, tests, mutants, the 187/2972 counts, Linux behaviour, CodeQL results (not yet scanned for 3 of 4 languages), whether F3/F4/F8 are refused, whether any legitimate store is newly refused, and the real-book `prove` result. The kit's predictions (Q1-Q10, F1-F8, L1-L12, GO WITH FOLLOW-UPS) are source readings.

## Outside-the-fences disclosure
Read-only throughout. Wrote only the two files. One loopback bind on 127.0.0.1:9820 for a few seconds as the `lsof` control (a python socket, freed). Git in the project repo: `ls-remote`, `show`, `grep`, `ls-tree` only, with `--no-optional-locks`. `gh` `-X GET` under the project `GH_CONFIG_DIR`. No decision-queue tool, no scoreboard, no ledger, no Jira call (the Jira facts are the builder's, RELAYED). One shell mistake (a `sed` with a path holding spaces inside `$(basename $f)`) printed errors but touched nothing; I re-ran the scan with python. Two hook refusals (`cd` once, zsh word-splitting once) fixed by absolute paths and `bash` heredocs. Four-underscore slot count of the kit: 8 (seven slots and the last line); at-sign pattern 0; non-ASCII 0; person names 0.
