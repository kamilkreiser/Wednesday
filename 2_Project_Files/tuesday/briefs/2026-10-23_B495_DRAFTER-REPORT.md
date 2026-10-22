# B495 drafter report (Tuesday s145 drafter, 2026-10-23 about 04:4x AEDT)

Brief: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-23_B495_SEAT-G51_hpsmpoc-b493-gate-tier2.md` (48,841 bytes, ASCII only, 8 slot lines with the pattern, 0 at-sign tokens).
Seat `Datasec/HPSM-POC-G51` (tmux showed tuesday, K1, G50, J2, fleet-monitor: G51 free). Model row G2, sonnet. Ports 8430-8439 (lsof 8420-8449 empty; 843x tokens in the briefs folder are only lsof range checks). Locks by path `.tools/.git-lock` (ref writes) and `.tools/b495/heavy.lock`.

## Measured by the drafter (read-only GitHub GET, ls-remote, tmux, lsof)
- main 4daa4054 (#188 squash); b493 head 52b6b26a; compare: ahead 2, behind 0, files 45+0 and 34+8.
- b490 head moved to 6708ac6b (round 2; B494 live in G50).
- pulls 177 (b409), 178 (b418), 185 (b472), 188 (b489): all closed, merged true.
- Full patch read; apiq.sh matcher run on five canned ps lines: dotnet test and testhost exec lines printed, bash decoy, dotnet build and a b495-owned run not printed.

## Relayed (builder STATUS): all counts, kill lists, 22 of 22, 1901/13/0 -> 1904/13/0, challenge texts, delay cells.
## Unmeasured: open-PR list and check-runs of the head, package owner of the error_description wording (drafter's reading: the JwtBearer handler, not IdentityModel), P4 outcome.

## Departures from the ask
- Over the 40 KB target (48.8 KB): the eight minus-line proofs, 15 new mutants and the queue rule take room.
- Api-suite rule is a script (`apiq.sh`, first-word match on dotnet test, dotnet exec testhost.dll, testhost) with canned-line, live decoy and live positive controls.
- New mutants beyond three: N1 (skew 29), N2 (life >=), N3 (exp < iat), N4/N4b (iat bracket), N5/N5b (structural), N6/N6b (Names), c3 equivalent control, probes P1-P4. P4 (offset rows life 61 or 0 may let a second clause shadow the labelled one, unpinned) is the drafter's own candidate gap.
- Error_description capture uses a pin set to ZZZ so the red message prints the real challenge (no probe).

## `____` slots (Tuesday)
Stamp time, stamped by, launch authority, hard stop, main at launch, head at launch, model receipt and load1, plus the last line READ-WHOLE-BY-TUESDAY.
