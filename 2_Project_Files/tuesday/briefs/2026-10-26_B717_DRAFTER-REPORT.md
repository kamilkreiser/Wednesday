STARTABLE: YES (after the stamp; one wait: the machine sits at the load1 line of 7 and `heavy-slot-1` is held by the live #118 gate)

# DRAFTER-REPORT B717 / SEAT-M29 (MPS PR #117 fix round, round 2 of 2), drafted 2026-10-26 08:48-08:55 AEDT (clock = `date`)

Kit: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-26_B717_SEAT-M29_mps-117-round2-rows.md` (141 lines; 8 slot lines, `/usr/bin/grep -c -E '_''_''_''_'` printed 8; last line `READ-WHOLE-BY-TUESDAY: ____`).

## BLUF
- The fix is ONE new commit on `6e34f07a` of `b686/mps-null-class-edge-rows`, fast-forward push, test rows only, appended to the PR's own file (existing 261 lines byte-equal, `+N -0`). Sonnet, model row C2 (`model-routing.md:92`), ports 9840-9849, pane `Datasec/MPS-M29`.
- "The 3 rows" read as three test row SHAPES (the gate's own count): E1 costed device, link + one trailing space; E2 costed device, one leading tab + link (both kill H3); E3 a second included supply group differing only in case, document validates (kills H4). Default 9 cases (4+4+1). B700-3 is a PR-title matter (Tuesday's squash text), not a row.
- Main moved by 3 commits since the branch point (#116 `110ebecd`, #115 `f5a27af0`, #112 `1ac8ab8a`; main now `1ac8ab8a`): none touches #117's path, the validator or the two older GovernedNull files. The kit forbids rebase and merge of main (fix-round rule, quoted with sources).
- Open PR #118 (`b711/mps-parity-multiset` @ `39e51272`, Import Parity paths) is named in PARTITION with its live Opus gate `Datasec/MPS-G135` (B715), which holds `heavy-slot-1` ("B715 08:44:47 mutants"). 0 shared paths.
- Round count: the round-2 gate counts as "NO GO 1 of 2 on the class 'a surviving mutant on the null-class refusal of ReferenceDocumentValidator'" (read from B700 STATUS `:1`, `:80`, `:56`); that class had 2 of 2 on PR #110's cycle; the B700 kit made this lane a stricter new cycle (same-class NO GO goes to a card). Tuesday states the count at the stamp.

## Questions for Tuesday
- **Q-1 (which three rows).** Gate text, B700 STATUS `:49` "Fix shape: two rows in the new file (costed device, link = real link + one space; + leading tab) ... same one CPP_INCONSISTENT list"; `:50` "Fix shape: one row, expected pass"; `:51` B700-3 "title-only"; `:56` "ONE new commit on the same branch (3 rows, test-only) fixes both; B700-3 needs no commit." My reading: three test rows (2 for B700-1, 1 for B700-2), not the three findings. **Default: the three row shapes.** The kit says the stamp may read it otherwise.
- **Q-2 (case count).** A "row" is a shape; E1 and E2 run on devices 0-3 as the round-1 rows do. **Default: 9 cases (4+4+1).** If you want exactly three data cases: device 0 only for E1 and E2 (fewer kills for per-device mutants, none of which the gate named).
- **Q-3 (sweep extras).** The next gate builds a fresh battery against the same two lines. **Default: the seat runs a sweep (group key `.Trim()`, `ToLowerInvariant()`, comparer at `:183`, `rows` join variants, no-break-space padding, `<= 1`) and adds a row only for a reachable survivor, capped at 4 extra cases, each named as beyond the ruled three; over the cap or unkillable by a test row: STOP.** I judged the group-key `.Trim()` variant the likeliest extra survivor (the gate did not test it). If you hold strictly to "3 rows", set the cap to 0 and the sweep to report-only.
- **Q-4 (append vs second file).** D1 appends to the PR's file so the PR stays one path and removed lines stay 0. Alternative: a second new file (PR becomes two paths). **Default: append.**

## D-decisions (in the kit, override at the stamp)
D1 append, new member names, no edit of the closed builder/expected switches (they throw on unknown shapes); D2 sweep extras cap 4; D3 own mutants, the gate's evidence folder and `.tools/b700` not opened; D4 base is the PR head, no rebase, no merge of main; D5 one commit, never an amend; D6 narrow filters (`~GovernedNullClassEdges`, `~GovernedNull`); D7 no provider matrix; D8 the property (no one-edit variant of the link lookup `:200-224` or the supply-group key `:181-193` survives every committed row) then the closed list H3, H3a, H3b, H4 plus the sweep, "any other shape: prove it meets the property or STOP".

## Facts re-measured (instrument, control)
- ls-remote (git read verb): main `1ac8ab8aca9573aacf022860b3963e867e559fb1`; branch = `refs/pull/117/head` = `6e34f07acecf5ddf42a1b72f6861e69672a2c5a0`; `refs/pull/118/head` `39e51272b6b2733d50764e4277f8f0158e8f0794`; no `b717*` (control: the same call listed `b711/...`).
- `gh -X GET api pulls/117`: open, not draft, 1 commit, 1 file, +261 -0, mergeable_state "unknown"; commit parent `a85f8bd5` (not the host's base field `110ebecd`). `compare main...6e34f07a`: diverged, ahead 1, behind 3, merge-base `a85f8bd5`.
- Compare `a85f8bd5...1ac8ab8a`: 3 commits, 7 files (list in the kit). Path program over the list: Edges.cs 0, validator 0, GovernedNullClass.cs 0, GovernedNull.cs 0; controls StoreFirstUseAbsent.cs 1, `zzz-no-such` 0. Note: the task said "#112 landed just now as `1ac8ab8a`, #113-#116 earlier": measured, #113 and #114 are older than the branch point, #115 and #116 landed after it, none overlaps.
- Open PRs and files: #117 (the one path), #118 (ParityProof.cs, PanelParityMultisetTests.cs).
- Raw reads at the head: Edges.cs 261 lines, blob `dd2c19ba`, sha256 `4352255e...3ad`; validator 229 lines, blob `e7c6f862`; counts in the kit (`:207` 1, `:184` 1, `StringComparer.Ordinal` 6, control 0). `TreatWarningsAsErrors>true` 1; `InvariantGlobalization>true` 1; `global.json` 10.0.100.
- Ports: `lsof -nP -iTCP:9840-9849 -sTCP:LISTEN` empty, rc 1; positive control (python bound 9840) listed, rc 1 after free. Word-boundary scan of the 107 non-`.pre-` SEAT kits of 10-25/10-26 for `984[0-9]`: hits B634 (claimant, finished, pane `Datasec/MPS-M20` not live), B630, B643, B645, B647, B690, B693 (prose about B634's claim); control `979[0-9]` fires on 9 files. Hits reported in the kit. Live panes: tuesday, NexusAI-M14, HPSM-POC-G136, MPS-G135, NexusAI-G134, Security-Composer-J19, Security-Composer-G133, fleet-monitor; `MPS-M29` count 0.
- Model: `model-routing.md` line 92 C2 ("1st" Sonnet), 108 G1, 109 G2, 111 G-cap; `models_latest.json` line 23 `claude-sonnet-5-5`, checked 2026-10-26 07:42:13.
- CI step read (`ci.yml` lines 30-43 on main): `dotnet build MpsCalc.slnx -c Release` then `dotnet test MpsCalc.slnx -c Release --no-build`, ubuntu-latest, 20-minute cap; predicate written in the kit.
- Heavy slot: `heavy-slot-1/holder` "B715 08:44:47 mutants"; `LC_ALL`-default `uptime` 6.85 6.76 7.34 at 08:51.
- Fix-round rule: project `CLAUDE.md` has no such line (grep hit only a history entry, line 78); quoted from `CLARIFICATIONS.md:1090` ("no rebase, no merge of main. Not a stop.") and the B672 kit line 20 ("the PR branch is NOT rebased and main is NOT merged into it ... would void the gate's pin").
- Landing rule: `CLARIFICATIONS.md:809` (squash with the head pinned, `--match-head-commit`) and `CLAUDE.md:50-52` (CodeQL), quoted in the kit.

## Things Tuesday should know
- The PR body still says "42 new test rows" and the title/squash subject carries the key only in the title (B700-3): Tuesday's squash text; the kit says so.
- `pulls/117` mergeable_state is "unknown" (main moved); the round-2 gate must re-run its CI line on a fresh combined tree (#112 added since the old one).
- The round-1 gate lost time to `uptime` under a German locale (decimal commas read as a load of 300); the kit tells the seat `LC_ALL=C uptime`.
- The gate's scratch Api forcing rows (`B700ApiForce.cs`) sit in `.tools/b700/quarantine`; the kit does NOT let the builder open them (independence, as B686 did for B645's evidence).

## UNMEASURED
No build, test, mutant or C# compile was run. Supply-row JSON property names and which sheet the four devices use (E3 needs a sheet a device links to); the head's exact answers for a padded link and for E3; per-mutant red counts (8/4/4/1 are predictions); whether the group-key `.Trim()` variant survives; Jira state of MPSCALC-336 (not read by me; RELAYED Backlog, 0 comments from the gate); a combined tree with the three newer commits; CodeQL on the new head.

## Outside-the-fences disclosure
Wrote only the kit and this report. Read-only: DRAFTER_RULES, the B686 and B700 kits and B700 STATUS, the B672 kit, B711/B715 kits (a few lines), the project `CLAUDE.md` and `CLARIFICATIONS.md` lines, `gh -X GET` only under the project `GH_CONFIG_DIR`, `git ls-remote` and `git config --get`-style read of `core.sshCommand` (key path elided), `lsof` plus one 6-second python loopback bind on 127.0.0.1:9840 as the positive control (freed; no hosted host touched), `tmux list-panes`, `uptime`, a scratchpad copy of three raw files (edges.cs, val.cs, gnc.cs) and a compare list. A 'cd /dev/null' was typed once in a combined command and refused by the hook (nothing ran); no `decision_queue.sh`, no `briefs_staged`, no scoreboard, no `_ledger.md`, no other project, no Jira call, no fetch.
