STARTABLE: YES (after your stamp; one live-coordination wait: heavy-slot-1 held by B645 at 10:27, load1 6.47)

# B654 DRAFTER-REPORT (topic `mps-325-walk-caps`; drafter claude-sonnet-5-5, 2026-10-25 10:22-10:37 AEDT; `date` 10:26:53 and 10:27:45)

## BLUF
- Kit: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-25_B654_SEAT-M21_mps-325-walk-caps.md` (136 lines, 0 non-ASCII bytes, 8 stamp-slot lines). Seat `Datasec/MPS-M21`, ports 9320-9329, Sonnet row C2 (`model-routing.md` line 92), model `claude-sonnet-5-5` (`models_latest.json` line 23), gate after TIER 1 Opus (row G1, line 108), round 1.
- Lane M-A2 = MPSCALC-325. Apply the parked patch + its 8 rows to CURRENT main `dd0ce36d` (not to #110), add the one approved `docs/API.md` sentence, run the mutant battery B614 did not run, the `QuoteApiTests` family, and the CI line. One commit, 4 paths, NEW branch `b654/mps-draft-validation-walk-caps`, ends READY FOR QA; Tuesday opens the PR.
- Overlap with PR #110 (open, clean, base `93e1cab5`, head `650ddfb7`, 5 files): 0 shared paths. One real coupling: the new rows call `PatchRaw` and `Errors`, `private static` helpers declared in #110's own file `tests/MpsCalc.Api.Tests/QuoteRefusalOrder.cs` (already on main, identical in its first 40 lines at the #110 head). Kit: read-only dependency, STOP if they change.

## FACTS RE-MEASURED (instrument; control)
- Main `dd0ce36dc1083266bf89c55d9ddab4aa9efb4c85`, #110 head `650ddfb7`: `git ls-remote` + `pulls/110` GET (state open, clean). No `b654*` ref (`matching-refs/heads/b6`: b60, b603, b614, b62, b630, b69).
- Name `MPS-M21`: free. Word-boundary scan of non-`.pre-` SEAT kits of 10-24/10-25 for `MPS-M21|SEAT-M21|M21`: only Composer kits B623/B626/B627 hit, on `M21` as a MUTANT id, not a seat. Live panes (`tmux list-panes -a`): tuesday, NexusAI-M9, Security-Composer-G109, MPS-G107, Security-Composer-J13, fleet-monitor. No B65x brief existed before B654 except B650.
- Ports 9320-9329: `lsof` printed nothing (rc 1; no positive control run). Word-boundary scan hits SIX non-`.pre-` SEAT kits, all from yesterday: B582 (its own block 9320-9329, HPSM-POC, finished, no pane), B585 and B589 (allocation lists naming it as B582's), B607/B608/B609 (digits inside a commit sha `...bb9328bdf`). Control: scan finds 9320-9329 in B582 itself; a scratch `9325` line reads 1. No live seat holds the block.
- Parked patch (`.tools/_quarantine/2026-10-25_B614_325-parked/`): `325-src.patch` sha256 `6e41acac...1067` (62 lines), `QuoteWalkCaps.cs` `9c987430...2cce` (105 lines, equals `.moved-from-fix`). `patch -p1 --dry-run` on scratch copies of the two files from main: rc 0; with `-F0` rc 0; control (one context line changed, `-F0`): rc 1, "1 out of 3 hunks failed". (My first control, default fuzz, passed and was a bad control; replaced.) `PurchaseValidation.cs` blob `230fe63d` and `QuoteEndpoints.cs` blob `3bde33c4` equal the patch's `index` pre-images.
- `docs/API.md` at main: the sentence is at line **274** (card said 275); `one error per repeated number, e.g.` count 1, control `zzz-no-such-string-7f3a` 0; `docs/api/openapi.json` count of "one error per repeated" 0 (control: API.md 1).
- Tree at main: 729 entries, 645 blobs, not truncated; `QuoteWalkCaps.cs` absent; docs/API.md and both src paths present; made-up path absent. (An earlier grep of a saved path list gave a false zero for known-present paths; I re-fetched the tree as JSON and checked membership with controls. The false zero came from the saved list, not the tree.)
- MPSCALC-325: Jira GET via an in-process helper reading the MPS `.env`; JQL `project = MPSCALC AND ( key = MPSCALC-325 )` returns it, Backlog, labels lane-d / tier-1; 1 comment (B583). Ticket notes the supplies-null site was not measured; not in this lane.
- CI: `ci.yml` lines 42-43 (`dotnet build MpsCalc.slnx -c Release`, `dotnet test ... --no-build`); `Directory.Build.props` `TreatWarningsAsErrors` true. Main's last commit: 8 check-runs success (dotnet, web, python, package, 4 CodeQL). Landing rule: squash with head pinned, `CLARIFICATIONS.md:809` and project `CLAUDE.md:50`; quoted in the kit.
- Existing rows that assert these walks: `QuoteApiTests.B102Audit.cs:58`, `QuoteApiTests.GateB36.cs:109`, one entry each (read at main).
- B645 (gate of #110) kit: judges `34ccb02...650ddfb7` by tree ids; fences no repo path; ports 9960-9969. `heavy-slot-1` holder `B645 10:26:26 m-mut-N1-narrow`; load1 6.47 6.76 8.12 at 10:27.

## D-DECISIONS (override at the stamp)
- D1. Base is main `dd0ce36d`, not #110's branch: lane independent of #110, either can land first.
- D2. One commit, 4 paths; keep the file name `QuoteWalkCaps.cs` (sweep + B614 name) so the parked proof is byte-identical.
- D3. Add ONE row (x2 hosts) in the same new file proving the control-character cap is SHARED across the text fields (25 bad fleet sites + 25 bad hardware optionSkus gives exactly 20 entries, fleet first). Reason: B614 STATUS line 172 item 4 says no row covers the shared cap; a tier-1 gate would find it. Droppable only with a measurement.
- D4. Branch name carries `b654/` per repo convention (b614/, b630/); the template's rule 4 bans a brief number in code, comments, commit message, file names, and I read a ref name as outside it. Strike at the stamp if you disagree.
- D5. No provider matrix; DevStub + Entra-test host classes only.
- D6. Docs: one sentence only; `openapi.json` is the MPSCALC-290 lane.
- Mutants: B614 named C1-C7 but never wrote their definitions, so the kit defines them (C1 BOM guard removed, C2 `.Take` removed on control chars, C3 Take-before-Where, C4 `.Take` removed on repeated numbers, C5 cap 21, C6 cap 19, C7 BOM cap counts the whole list) plus drafter-added C8 (per-field cap) and cw-weak. Predictions are my reading, not runs.
- Sequencing: M-FEEDBACK (MPSCALC-176) shares `docs/API.md`; kit says it starts after this lane lands.

## Q-QUESTIONS FOR TUESDAY (each with a default)
- Q1. Are you content that kit text names a branch `b654/...`? Default: yes, keep (repo convention).
- Q2. The kit lets the seat open exactly one folder of another seat's quarantine (B614's parked folder), copy-only. Default: yes; the sweep names it as the source of the patch.
- Q3. Launch ordering: heavy-slot-1 is held by the B645 gate; this lane is light until the first build. Default: launch with the single waiter at load1 below 7; M-A2 can run beside the gate (0 shared paths, different ports 9960 vs 9320).

## UNMEASURED
- Nothing built or run: that the 8 parked cases are green on `dd0ce36d` (proved only at `93e1cab5` by B614; src blobs are byte-equal), the D3 row's exact list (sketch from reading lines 1425-1440), all mutant outcomes and C3/C8 buildability at 0 warnings, test-count baselines at main, CI Linux behaviour for the 100,000-line bodies, any CodeQL result (no PR exists), `lsof` positive control, org-level state beyond the GETs above.
- The helper dependency was compared for lines 1-40 of `QuoteRefusalOrder.cs` between main and #110 head only.

## OUTSIDE-THE-FENCES DISCLOSURE
- Wrote only the kit and this report. Scratch files in the session scratchpad (fetched read-only copies, a Jira GET helper reading the MPS project `.env` in-process, never printed). I read the parked folder (patch, rows, red/green logs) as the task told me. Jira: one GET search + issue + comments, JQL with parentheses. `gh api -X GET` under the MPS `GH_CONFIG_DIR` only. No git write verb: one attempt of `git -C <scratch> apply` was refused by a hook (not run), then used `patch --dry-run` on scratch copies. Did not run `decision_queue.sh list`; `show` once on the exact id. Did not read staged briefs, scoreboard, the ledger, or any WEDNESDAY/FRIDAY tree. No HTTP to any hosted host. One advisory about case-sensitive greps was noted; counts that matter were paired with controls.
