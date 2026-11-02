STARTABLE: YES (commit 1 now; commit 2 behind a stamp slot, default HELD)

# B1116 drafter report (drafted 2026-11-02 10:59 to 11:02 AEDT by `date`)
**BLUF.** Kit is 10,134 bytes. Both tickets re-read at source (Jira GET, 0 comments, Backlog, 0 links). The sweep's NM1 and NM2 claims hold, with one catch on NM2: the ticket is labelled `needs-ruling`, its acceptance says "The product owner decides the sentence", and the 04:42 daily-note line (`daily_tuesday/2026-11-02.md:80`) records only "MPSCALC-345 accepts the gate's docs wording as earlier docs sentences were settled, a one-line docs lane" and does not quote the wording. The wording itself is in the ticket (from the gate, "proposed by the gate and not approved"). So the call is Tuesday's own, not the product owner's.

## Facts re-measured (instrument)
- Code main `19d084fa8018094bf7ea9360433d0d87f8720e45` (`gh api git/ref/heads/main` and `ls-remote` agree). Local checkout lacks the object (stale), so every file was read by `gh api` raw at the pin.
- Lines (cat -n / grep -n on the raw files): IMPORTER.md 141 lines, wording at :89-90; model :19 :23 :57 :63; severalDevices.test 413 lines, :104 row (c), :308, :343; QuantityAudit.test 237 lines, :20 helper (one fleet line), :51 row. The ticket's `:308/:343/:20/:57` pointers still hold at the new main although it cites an older main (b7cf1ad0).
- Overlap: b1093 (M74's branch, head 717da6f) vs main: 14 paths, 0 shared. B1103 kit names bom paths `BomClassColumn.test.tsx`, `bomModel.ts`, `PurchaseBomEditor*`: 0 shared. B1106 kit: 0 hits for my paths. B1094 (M73): 0 hits. B1115 kit does not exist yet (0 files), so its paths are unread; M74's branch only touches the API/Templates/docs-API tree. Open PRs: #121, #120 (dependabot).
- Ports: none needed (vitest, eslint, tsc). Panes: `Datasec/MPS-M75` absent; live MPS panes %49 G277, %51 G278, %52 G279. load1 9.75 at 11:01.
- Landing: squash (#137, #138 per the B1087 kit line 24).

## D-decisions (mine, override at stamp)
- D1: 13/12 row goes in severalDevices.test (ticket's item 1 Where), as a committed row with hand-written literals, not an oracle rewrite (ticket allows either; row is smaller).
- D2: rental row goes in QuantityAudit.test with its own two-fleet draft; the helper at :20 is left alone.
- D3: red proof by two mutants in a separate detached worktree (MA remainder-1 tolerance, MB `fleet.length < 2`), plus controls c0/c1.
- D4: branch `b1116/mps-366-345-quantity-audit-rows`, one push, no PR; commit 2 skipped unless the RELEASE slot says RELEASED.

## Q-questions for Tuesday
- Q-1 (the one you asked about): is commit 2 a docs correction or the product owner's word? The ticket says the latter, twice, and is `needs-ruling`. **Default: HELD** (kit carries the COMMIT-2 RELEASE slot; seat stops at commit 1 and says HELD). Release it only if you hold that the 04:42 call settles it, as earlier docs sentences were; the daily note line does not quote the sentence, so the slot should cite the ticket text.
- Q-2: gate G2 tier 2, round 1, on the one branch (both commits) or gate commit 1 alone and send commit 2 later? Default: one gate, one PR, whichever commits exist.
- Q-3: Sonnet (C2, `model-routing.md:92`; id `claude-sonnet-5-5`), launch via `launch_when_cool.sh`, one waiter. Default yes.

## Contradictions
- Sweep says the 04:42 call "accepts the gate's wording"; the note line says only "accepts the gate's docs wording"; the wording string exists in the ticket (from the gate B740, `B740_STATUS.md:178` as cited by the ticket), not in the note.
- Ticket 345 cites main 1137f119 (141 lines); main 19d084fa also has 141 lines with the same words at :89-90.

## UNMEASURED
No npm, test, lint or mutant run. Accessible names for `rowOf` in the two-fleet draft not tried. Five old branches (`b03/importer`, `b104/mpscalc-140-care-packs`, `-141-coverage-audit`, `-147-customisation`, `-147-customisation-r2`, `-182-sydney-date`) list QuantityAudit or IMPORTER paths in a compare against main; state (merged or live) not read. B1115's paths unread. Plants: none used (mutants instead).

## Outside the fences
None. Only `gh api -X GET`, read-only git, a Jira GET with the project `.env` sourced in-process (token never printed), `date`, `lsof`, `tmux list-panes`, `uptime`. Scratch copies of the fetched files sit in the session scratchpad only.
