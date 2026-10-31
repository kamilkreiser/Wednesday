STARTABLE: YES (main 1a2a0294, 2 open PRs touch web/package-lock.json only, 0 live branch on the engine files, no pane M52 live, no .tools/b974, ports 9700-9709 free and not needed; load1 was 7.69 on one read and 2.65 on the next, so the waiter handles it)

# B974 drafter report (SEAT-M52, MPS Commercial Calculator, MPSCALC-254 + MPSCALC-256)

## BLUF
Kit written (79 lines, B861 shape): `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-31_B974_SEAT-M52_mps-254-256-v4-volume-basis-annual.md` (unstamped copy beside it as `.pre-stamp`, 8 lines with the four-underscore pattern). One builder, one branch `b974/mps-254-256-v4-volume-basis-annual`, two commits (254 then 256), engine files + `docs/ENGINE.md` + Engine.Tests only, tier-1 gate after. Model: Opus (`claude-opus-5-5`), row C3 (model-routing.md:93). Both tickets are startable with no ruling; no visible word is needed unless the builder finds one (then STOP).

## Measured (read-only, all at 2026-10-31 ~12:0x AEDT)
- main `1a2a02947db076aa01af494056724d4a10fd3f07` (2026-10-27 19:01Z). Open PRs #121, #120: each lists only `web/package-lock.json`. 155 branches compared to main: 24 touch engine/ENGINE.md/Engine.Tests paths, all squash-landed and 20+ commits behind (nearest 20); the 8 branches within 10 behind touch none. No `heads/b974`.
- Jira GET: MPSCALC-254 and -256 read whole, Backlog, 0 comments, 0 links, labels lane-v4 / tier-1 / calc-register; control MPSCALC-99999 = HTTP 404. -254: purchase GROUP path waits for -252; rental and deal-usage path starts now. -256: no dependency.
- The "calculation register" the tickets name is `docs/ENGINE.md` (rule map; highest R-28, highest X-32); the workbook register in the project folder is workbook-derived and the kit does not edit it. Build-plan fixture 503 + 3,692 x 60 = 251,700 is a page-count test input (cited in the plan, not a price file).
- Harness found: ReplicaDifferentialTests (60 rental), PurchaseReplicaDifferentialTests + purchase_bom_scenarios.json (1,000), ItemisedComponentsTests (5,000 seeded), DealUsageTests, V13Fixture*Tests, QuoteReconciler (already has annual GP = monthly x 12). No frozen result-JSON golden exists, so the kit makes the builder dump one at the base and byte-compare after each commit; it also asserts InputHash equality.
- Trap flagged in the kit: `InputHash` hashes the whole input JSON, so a new input member must be omitted when unset (precedent `PurchaseInput.cs:123`, `WhenWritingNull`).
- `tmux list-panes`: tuesday, Datasec/HPSM-POC-R94, Datasec/HPSM-POC-H79, fleet-monitor (no M52). Pane form follows B861: `Datasec/MPS-M52`. Ports: `lsof` 9700-9709 empty (also 9710-9739 empty). 9700-9709 was G95's block on 10-25 (long finished). `LC_ALL=C uptime`: 12:02 load 7.69/3.78/2.67, 12:06 2.65/3.97/3.17.
- Local SDK `.tools/dotnet/dotnet --version` printed 10.0.401; `gh auth status` under the project config reads logged in; no heavy-slot or git-lock present.
- Kit scan: 0 non-ASCII bytes, 8 four-underscore lines, 0 person names; MPSCALC keys are in the kit text for the builder's STATUS only, and the kit forbids them in code and commit messages.

## Questions with defaults (Tuesday decides at the stamp)
- Q-1 Model: Opus by C3 (money-design surface) rather than Sonnet by C2. Default: Opus. Alternative: Sonnet under C2 if you read the surface as "spelled-out"; the plan and rulings are given, but the multiply-once rule is the money step.
- Q-2 Register location: new rows in `docs/ENGINE.md` (R-29 / X-33 or next free), not the project-folder workbook register. Default: ENGINE.md only.
- Q-3 Scope of -254: rental fleet line and purchase deal-usage line only; the purchase GROUP path is left to -252. Default: as the ticket says.
- Q-4 -256 measures: six measures in the acceptance sentence; any the engine cannot already derive is a STOP, not an invented figure. Default: STOP with the list.
- Q-5 Seat name: M52 was used by a finished NexusAI seat on 10-28 (pane `Datasec/NexusAI-M52`, not live). Default: keep `Datasec/MPS-M52` as asked.
- Q-6 Gate: tier 1, round 1 of 2 on the PR (money figures). Default: yes, Opus gate per G1 (:108).
- Q-7 Timing: target READY 3 h, hard stop 5 h after Step 0 (larger than B861's 1.5 h / 3 h because of the byte-equal harness). Default: as drafted.

## Stamp values to fill
- Expected main `1a2a02947db076aa01af494056724d4a10fd3f07`; no `refs/heads/b974*`; open PRs #121 and #120 only.
- Model receipt: `model: claude-opus-5-5 -- C3 money-design surface (model-routing.md:93) -- Opus first, no override -- gate G1 tier 1 (:108) -- gauge <n>%`.
- Launch: line is in the kit's Stamp section (`launch_when_cool.sh Datasec/MPS-M52 "... BRIEF_SEAT_LEVEL=opus ..."`).
- Not run by the drafter: any build, test, mutant or compile.
