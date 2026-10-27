STARTABLE: YES

# B821 DRAFTER-REPORT (Sonnet drafter, 2026-10-27 13:0x-13:3x AEDT) - M-WALK, MPSCALC-355

Kit: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-27_B821_SEAT-M47_mps-355-walk-cap-rows.md` (101 lines, 8 four-underscore lines, all Stamp slots plus the last line left blank for the stamp).

## BLUF
The seat's Step 1 is the measurement of g01..g07 at main `32b09108`; a row is written only for a survivor, and if none survives it ends `NO BRANCH:` with no push. By reading the source and the committed rows (nothing run), the drafter predicts **six of seven are already killed by rows at main and g07_ccDistinct survives**, so the likely outcome is ONE new `[Fact]` (a rental draft with fleet numbers 1, 1, 2, control-character sites, asserting `fleet[1].site` twice, `fleet[2].site`, then the repeat entry). The prediction is UNMEASURED and the kit says so and tells the seat not to trust it.

## Facts re-measured with instruments
- main `32b09108a5c476249498d22229debe3e73c8a5d6`: `git ls-remote` (control: matches the ticket's sha). `refs/heads/b821*` 0 (`gh -X GET matching-refs/heads/b821 --jq length` 0; control: `heads/b80` lists 3). Open PRs: 121 and 120, both `web/package-lock.json` only; PR 128 `merged_at` 2026-10-26T23:11:47Z.
- Ticket MPSCALC-355: Jira GET through the project `.env` in process, 0 comments, Backlog; contains g01..g07 and the claim "UNMEASURED at main".
- Product code at main (raw): `PurchaseValidation.cs` 366 lines, BOM loop `:128-171`, `MaxWalkEntriesListed = 20` count 1, `sectionIdListed += errors.Count - before;` count 1; `QuoteEndpoints.cs` 1611 lines, text walk `:1434`, `Take(PurchaseValidation.MaxWalkEntriesListed)` count 2 (so the g07 anchor must use the `.Select(t => $"{t.Name} contains` text), `errors.AddRange(PurchaseValidation.Errors(draft));` count 1, `HasControlCharacter` is `internal static` at `:1561` (usable by a g01 mutant). Control: `zzz-no-such` prints 0.
- Reading of rows at main (QuoteWalkCaps.cs, 736 lines): `:478` (100,000 lines numbered <=0, every check bad) kills g03/g04/g06 by reading; `:634` (both full fleet walks plus 25 all-checks-bad lines) kills g01/g02 (and g03, g04, g06); `:574`/`:615` kill g05 (expected list order). g07: no committed row repeats a control-character fleet number inside the first 20 entries (`:268` and `:574` repeat from the 24th line), so `Distinct` before `Take(20)` cannot change any expected list.
- CI predicate: `ci.yml` at main lines 31-43: job `dotnet (build Release, 0 warnings; test)`, ubuntu-latest, timeout 20, `dotnet build MpsCalc.slnx -c Release` then `dotnet test MpsCalc.slnx -c Release --no-build`; `Directory.Build.props` TreatWarningsAsErrors count 1.
- SDK: `dotnet` not on PATH; the repo-local `.tools/dotnet/dotnet` exists, `--version` prints `10.0.401` (the B789 template uses the same). Exists, not exercised beyond `--version`.
- Ports 7620-7629: `lsof -nP -iTCP:7620-7629 -sTCP:LISTEN` printed nothing; python `\b762[0-9]\b` scan of 256 non-`.pre-` `.md` kits dated 26/27 Oct: 0 hits (control: `\b968[0-9]\b` 6 files).
- Seat name `M47`: 0 hits in those 256 files (control: `M39` 7 files); panes listed: tuesday, Security-Composer-R62, HPSM-POC-D38, NexusAI-M21, fleet-monitor.
- Load: `LC_ALL=C uptime` 6.55 / 5.38 / 4.22 at 13:05, near the limit of 7; the kit says wait, do not hurry.
- Model: L6 line 85, C2 line 92, G2 line 109, G-cap line 111 (printed by `sed -n`); `models_latest.json` line 38 `claude-sonnet-5-5`.
- Template: B789 kit read (headings, walk-cap group, lines 108-174). No B789 DRAFTER-REPORT exists (its Stamp says it was not saved).

## D-decisions
- D1: Seat name `M47`, pane `Datasec/MPS-M47`, branch `b821/mps-walk-cap-rows`. Default if overridden: any unused name.
- D2: Row cap 6 added NAMES (the DevStub and Entra legs double the names, so 3 facts list as 6). The expected single g07 fact lists 2. A 7th name is a STOP.
- D3: Gate round per the coordinator's 2026-10-27 13:0x ruling (CC1 option a): round 1 of 2 on this PR, tier 2 (line 109); a further NO GO is a STOP to Tuesday.
- D4: Ending with no survivor is its own marker (`NO BRANCH:`) because the commission says the seat ends without a branch; the watcher must learn that marker (Q-1).
- D5: REFUSE "main moved" is limited to the three paths read (the test file and the two product files), not the whole tree, so unrelated merges do not stop the seat.

## Q-questions for Tuesday
- Q-1: Does the status watcher accept `NO BRANCH: ...` as a final marker? Default: yes, treat it as a terminal state like READY (the records seat then comments on MPSCALC-355).
- Q-2: Hard stop and target READY: suggested 1.5 h / 3 h after Step 0 (smaller than B789's 2.5 h / 4 h, one file, one expected row, but 7 mutant builds). Default: those.
- Q-3: Sibling kits B819/B820 did not exist at the read, so the seat name `M47` and ports 7620-7629 are unchecked against them; re-check at the stamp. Default: if a collision, rename the seat only.

## UNMEASURED
No build, test, mutant, compile or probe was run. The six-of-seven kill prediction, the g07 survivor and the row's expected list are readings. Not checked: other `QuoteApiTests` partial files for a row that already kills g07 (only `QuoteWalkCaps.cs` was read); that each mutant anchors once and builds warning-free; the `--list-tests` counts; the Jira ticket after the read.

## Outside the fences
None crossed. Read-only: Jira GET (MPSCALC-355, project `.env` in process, no token printed); `gh -X GET api` under the MPS `GH_CONFIG_DIR`; `git ls-remote`; raw files saved to the session scratchpad; `lsof`, `tmux list-panes`, `uptime`; one invocation of the repo-local `dotnet --version`. No card, no scoreboard, no ledger, no briefs_staged, no other client tree read. Writes: only these two files and scratchpad copies.
