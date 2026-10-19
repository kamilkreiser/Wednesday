# B303 drafter report (MPS lane-e price book), 2026-10-20 08:2x-08:3x AEDT

Brief: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-20_B303_SEAT-K4_mps-lane-e-price-book.md`. Read verbs only. Nothing fetched, checked out, deployed, mailed or published. Jira GETs through the project's JIRA_* read by name inside `python3 -I`, never printed.

## Classification (all 12 tickets read whole: description, labels, links, every comment)

| Key | Pri | Class | One line of evidence |
|---|---|---|---|
| MPSCALC-140 | High | D | Merged: PR #74 `ed726068` + PR #78 `f1d5641a`; comments 39572, 39638 (deployed on hosted at e6f92a5f). `PriceBookImporter.cs:526` `ImportCarePacks`. Status still Backlog (project rule: merge does not move a ticket). |
| MPSCALC-141 | High | D | Merged: PR #65 `a5cbbf81`, comment 39538. Coverage table at `docs/IMPORTER.md:~104-130`. |
| MPSCALC-142 | High | D | Merged: PR #76 `0217044e`, comments 39573, 39639. `web/src/screens/inventory/InventoryScreen.tsx:23` `carePack: 'Care pack'`. |
| MPSCALC-143 | Low | D | Merged: PR #52 `e59fa18f`, comment 39524. `InventoryScreen.tsx:20` `supply: 'Supplies'`. |
| MPSCALC-147 | Med | D | Merged: PR #69 `3478ff43`, comment 39547. `SynnexBook.cs:282` `PanelRows`; `InventoryScreen.tsx:18` `option: 'Customisation'`. Calc-register row still "PROPOSED" (BACKLOG [B164-R25]): records seat's, not code. |
| MPSCALC-155 | Med | D + C | Class built: PR #76, `InventoryScreen.tsx:24` `staging: 'Staging'`, ENGINE.md X-31. Remainder ("prices come from the reviewer's staging details when they arrive", comment 39574) waits for a client human. |
| MPSCALC-182 | Low | D | Merged: PR #66 `de808f51`, comment 39539. `PriceBookImporter.cs:237,:250` `SydneyDate`. Follow-up is MPSCALC-191 (not in the sweep list). |
| MPSCALC-231 | Med | D | Merged: PR #83 `21c2aec7` (= main), comment 39646. Rides the next hosted card. |
| MPSCALC-200 | Med | A-conditional, held out (Q1) | Docs fix needing counts from the real price book (`.local/`, confidential). Partly stale: "294 SKUs in common" no longer appears in `IMPORTER.md` at main (`grep -i 'in common\|all three\|294'` = 0; control: `262` hits at `:122`), so the contradiction half may be fixed by #78; the A3 23-vs-8 and A4 25-vs-22 gap explanations are still not in the table (`:~108-109`). |
| MPSCALC-206 | Med | A (tier 1) | No comments, no hold label. Unbuilt at main: `SynnexBook.cs:300-303` ends the section at a non-SKU-shaped cell with no issue; no commit after #69 touches the file. Buildable as a staff-only Warning; NEW WORDS listed for a later deploy card (the #83 precedent). |
| MPSCALC-207 | Med | A (tier 2) | No comments. Unbuilt: `ParityProof.cs` `CheckPanels` (`:111-150`) has no records = SKUs x devices check; `IMPORTER.md:17` still says "an A3 model sheet's". The ticket's path `tools/MpsCalc.ImportCli/ParityProof.cs` is stale; the file is `src/MpsCalc.Import/Parity/ParityProof.cs`. Two acceptance alternatives; the brief picks the assertion with a docs fallback. |
| MPSCALC-227 | Med | A (tier 2) | No comments. Unbuilt: `B104CarePackApiTests.cs:31` `Assert.All(...StartsWith(care_))` over `?class=carePack`; the file's only commit is #78. Test-only. |

No class B rows (no Kam ruling or customer-facing words needed; -206/-207 words are staff-only importer/prove output). No class C row except 155's remainder. **The three High rows are all already built and merged, so no High row is in the brief.**

Findings for Tuesday's records seat (not seat work): -140, -141, -142, -143, -147, -182, -231 are merged and (for -140/-142/-155/-231) deployed or riding the next card, but still read Backlog. The sweep's "160 buildable" count for MPS counted label-based, and 8 of these 12 were already built.

## Measurements (command, time)

- Main = `21c2aec71e66f7f6af63817134c66b8f54e97720`: `gh api repos/datasecau/MPS-Commercial-Calculator/git/ref/heads/main --jq .object.sha` (08:23) and `git -C <project>/2_Project_Files --no-optional-locks ls-remote origin refs/heads/main` (08:2x). `gh auth status` = `kamilDatasec` (GH_CONFIG_DIR = project's).
- Open PRs: `gh api 'repos/datasecau/MPS-Commercial-Calculator/pulls?state=open'` = empty (0); control `?state=all&per_page=1` -> `83`.
- `b303*` refs: `git ls-remote origin 'refs/heads/b303*'` = 0; control `'refs/heads/b172*'` = 1 (`e0c8c4ad…`).
- Jira: `project = MPSCALC AND key > MPSCALC-231` = 0 rows (no newer ticket); `labels = lane-e AND statusCategory != Done` = 15 rows (the 12 + -144 needs-ruling, -215, -219 outside the sweep list).
- Port block: `lsof -nP -iTCP:7330-7339 -sTCP:LISTEN | wc -l` = 0; `lsof -nP -iTCP:7330-7339 | wc -l` = 0 (08:26).
- Load: `uptime` 5.59 (08:23), **8.24 (08:26)**: already over the 8 limit; the seat must wait before any heavy run.
- Panes: `tmux list-panes -a -F '#{pane_id} #{session_name}:#{window_index} #{pane_title}'` = %0 TUESDAY, %1 fleet monitor, %56 NexusAI, %103 HPSM-POC import failure path. No Composer or NexusAI test-code pane seen.
- Heavy slots: `ls -d <project>/.tools/heavy-slot-*` = no match (none held); `ls <project>/.tools/_quarantine | grep -i heavy` = `2026-10-17_B161_orphaned-heavy-slot-2`.
- Launch card: `bash decision_queue.sh show datasec-80pct-band-build-lanes-1020` = `choice='c'`, `ruled_ts=2026-10-20T08:21:03.782293+11:00` (the 08:20:44 tap is the commission's, RELAYED).
- Tool presence: `ls -l /opt/homebrew/bin/gitleaks` -> 8.30.1; `ls -d <project>/.tools/dotnet` and `.tools/b172/jira.py` exist. `git config core.sshCommand` is repo-local (deploy key `3_Access_Keys/github_deploy_rw`).
- Status folder: `1_Project_Definition/Briefs/` exists and holds `2026-10-18_B172_STATUS.md`.
- Code reads: `gh api -H 'Accept: application/vnd.github.raw' repos/datasecau/MPS-Commercial-Calculator/contents/<path>?ref=21c2aec7…` for SynnexBook.cs, PriceBookImporter.cs, ParityProof.cs, B104CarePackApiTests.cs, PanelOptionImportTests.cs, IMPORTER.md, InventoryScreen.tsx, ci.yml; commit history by `…/commits?sha=<main>&path=<file>` (none of the 206/207/227 files changed since #69/#78).
- Heavy-slot rules found in `Briefs/2026-10-16_MPS-LANES_ADDENDUM-3/-5/-6` (the brief combines them with the commission's load1 < 8).

## Open questions for Tuesday (recommended answer after each)

1. MPSCALC-200 needs counts from the real price book (`.local/pricebooks`, Synnex-confidential). May a seat open it, counts only? **Recommend: not in this wave.** Hold it for a separate later seat once you say yes; the contradiction half may already be fixed, so first re-read `IMPORTER.md` at main.
2. One tier-1 branch carries a tier-2 test-only ticket (-227) and a tier-2 ticket (-207) with -206 (tier 1), so all three wait for the gate. **Recommend: keep one branch** (shared files, your instruction), commits in order 227, 206, 207; if the gate is slow, -227 and -207 could be cherry-picked, but do not pre-split.
3. -206 adds a staff-only importer Warning; -207 adds staff-only prove lines and singular forms. I could not measure whether any screen shows import findings. **Recommend: build, merge, list as NEW WORDS for the next hosted card** (the #83 / R-3 precedent); do not deploy on this branch.
4. -206 design: the brief picks the "Warning" alternative so no imported row or price changes (C-33 says panel costing is confirmed as built). **Recommend: keep.** The "keep scanning" alternative changes imported rows and needs its own review.
5. The sweep gave a 12-ticket list but only 3 are work. Ask the sweep author to filter "merged but Backlog" rows out of the lane list. **Recommend: have the records seat transition -140/-141/-142/-143/-147/-182/-231 only if you want the board to match main** (project rule today: merge does not move tickets).
6. Load is 8.24 at 08:26 with B300 and S101O live. **Recommend: launch K4 only after load1 stays under 8 for a read or two**; the brief makes the seat wait, but it will sit idle.
7. -155's remainder and -147/-142's calculation-register row (BACKLOG [B164-R25]) are not seat work. **Recommend: leave -155 open for the reviewer's staging details; send the register row to the records seat.**

## Not established

- `dotnet --version`, any baseline test count, and whether the CI line is green at main (nothing run).
- Whether `AGENTMAIL_API_KEY` is set in the MPS `4_Credentials/.env` (not opened; the brief tells the seat to test by name and fall back to `STOPPED`).
- Whether import findings appear on any screen (so whether -206/-207 words are "screen words" under C-32).
- How the reference-store document records mapped devices per sheet (decides -207's assertion versus the docs fallback).
- Whether a Composer or NexusAI test-code seat exists; the real book's behaviour under -206 (never opened by design); the content of gate B162's instrument files (cited, not opened).
- Whether -200's "294 SKUs" contradiction was removed by #78 or by another edit (the `git log -S` was not run; only the absence at main was measured).
