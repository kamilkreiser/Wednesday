STARTABLE: YES (one path, no open PR, no live branch on it, ports 9840-9849 free; the shared jest lock is FIFO behind B855 and B856, a wait and not a refusal)

# B862 drafter report (SEAT-M52, NexusAI, RD-895, lane N2)

## BLUF
Kit written: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-28_B862_SEAT-M52_nexusai-rd895-tamper-control-cell.md` (105 lines, same shape as B855/B856). One test-only commit in `__tests__/rd407-concurrent-settings-writers.test.js` lines 366-385; no count moves (37 tests stay 37), so the counts file is not in the diff. Red-proof by mutants of the helper in the clone (MT-3 and a throw-only double go red; MT-1/MT-4 stay red; MT-2 stays green; old assertion restored goes green under MT-3 and MTB0). Model Sonnet `claude-sonnet-5-5` (models_latest.json), routing C2 line 92, gate G2 line 109 tier 2 round 1 of 2. Unstamped copy: 9 lines with the slot pattern, 0 `@X@` tokens, 0 non-ASCII bytes (controls run: planted accent reads 1).

Measured by me (read-only): main `f4ea31c9` (ls-remote); 0 open PRs; test file blob `c27c1501` (674 lines, equal to the content API sha), helper `2e0f5208` (102 lines), `backend/jsonStorage.js` `bba3742b`, counts file `d3c0021b` (5220 / 310); assertion at line 383; refusal text built at `backend/jsonStorage.js:3262`; Jira RD-895 whole (To Do, Low, no comments); gate B838 finding B838-1, section C7 and its two run files; ports 9840-9849: lsof empty, kit scan hits only closed 10-25/10-26 seats; lock tool hash equals the stamp value of B855. Nothing was run (no clone, no jest).

## D (decisions I made in the kit)
- D-1: `detected` = `torn + lost + finalLost + refusals > 0`; `thrown` stays in the printed object but is not counted. Source: the ticket Recommendation.
- D-2: `refusals` is counted from the helper's `firstErrors` (first 5 per child, message cut to 240 characters) by an anchored regular expression on the product's refusal text, because the helper (not this lane's) reports only a total error count otherwise. Any refusal is a detection and `torn` carries the cell on the committed double (gate: min 1854), so the limit is recorded, not fixed.
- D-3: mutants live in the HELPER (the tamper double is its `RD407_TAMPER` branch), applied in the clone, hash-restored to `2e0f5208`; the committed diff stays the one test file.
- D-4: 6 standard plus 16 isolated green runs (the gate's 22), counters read by a temporary stderr print that must be absent from the commit (hash-proved).
- D-5: added MT-5 (a double that throws the exact refusal text), expected GREEN by the ticket's own rule, recorded as the one spoofable channel (informational, not a red target); added MT-6 (old loose assertion restored, under MT-3 and MTB0, must read green) as the tamper control of the new line, the same device as B856's MS9.
- D-6: no new cell; a new cell moves the counts file B855 owns, so it is a STOP.
- D-7: whole-file mutant runs only for MT-3 and MTB0 (one each); all other mutants run on the cell alone (`-t`), as the gate did.

## Q (each with its default, all taken in the kit)
- Q-1: should `refusals` be derived from `firstErrors` (cap 5) given the helper is out of lane? Default: yes, record the limit; no helper change.
- Q-2: match the refusal by message only, or message plus `code` `STORE_UNREADABLE`? Default: message only (the ticket speaks of the message); builder records the code option under DESIGN.
- Q-3: ports 9840-9849. Default: taken.
- Q-4: ordering against B855 (counts file) and B856: none; four distinct paths; branch stays on the stamp base.
- Q-5: gate tier 2 round 1 of 2 with the full plain verify (5220 / 310). Default: taken.
- Q-6: pane `Datasec/NexusAI-M52` (no kit names it; live panes are M49, M50, J29, H48). Default: taken; recheck at launch.

## Points for Tuesday at stamping
- Heavy file: 16 storms of 2 child processes per whole-file run; the kit says run alone under the lock and never beside another storm file. Suggested: launch after B855/B856 have finished their jest-heavy steps if load1 rises (the gate pre-stagger note in the sweep).
- Landing order: if B855 lands first the counts pair on main moves; this branch stays on its base and its verify reads 5220 / 310 on its own base (kit REFUSE already says not a stop).
- Kit cites CLARIFICATIONS by line (2067-2068, 2412 read at my time; both lines confirmed) and its STANDING LINE 1 grep pattern includes the same entry ids B855 uses; no person names appear.
- Unmeasured and said so in the kit: every red/green, the counters on node 24 Linux, CodeQL on the new head.
