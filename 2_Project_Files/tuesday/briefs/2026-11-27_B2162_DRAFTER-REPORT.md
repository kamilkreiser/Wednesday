STARTABLE: YES (once Tuesday stamps it; the B2157 lock at launch is an expected wait, not a bar)

# B2162 DRAFTER REPORT: narrow revision of kit B2153 (seat X82), rev1

Read-only drafter (Opus), commissioned by Tuesday s334. First `date`: Fri 27 Nov 2026 17:49:30 AEDT; this report written at 17:53:00 AEDT (by `date`).

## BLUF
- New kit: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-27_B2162_SEAT-X82_oxpd2-lane-c-kit2-part2-rev1.md` (233 lines; B2153 had 232 by `wc -l` plus the new first line).
- Sidecar: `...-rev1.md.measured`. `stamp_check.py <kit>` prints `156 claims, 156 measured, 0 not measured` and returns rc 0 (output saved at `fleet/state/s334/d2162/stamp_check.out`).
- Diff: `...-rev1.diff`, made by `diff -u` B2153 against rev1. It has 8 hunks, 11 `+` lines and 8 `-` lines (the new first line plus ten changed lines).
- B2153 itself is NOT edited. No `<src>` seat-tool was touched. Nothing was written in the OXPd project.
- The kit was built by a program, not by hand: `fleet/state/s334/d2162/make_rev1.py` makes 12 exact replacements, each OLD text found exactly once, then prepends the first line.

## Every changed line (new line number; old = B2153 line - 1)
1. **New line 1 (added).** `SUPERSEDES kit B2153 (narrow revision B2162: the one-seat rule narrowed to build and gate panes; the records precondition removed). Every other line is B2153's.`
2. **Line 2 (old 1), header.** OLD: "One OXPd seat at a time: this kit launches only after the records seat of pull request 58 (kit B2146, seat R339) has ended READY (Stamp S3 ...), with no OXPd pane live ... (the folders `.tools/b2138` and `.tools/b2146` among them)". NEW: "One OXPd BUILD or GATE seat at a time". It refuses no other pane holding `OXPd2-X` or `OXPd2-G`. A records pane (`OXPd2-R`) is not a bar and may run beside it, for example kit B2161, seat R341 or the seat its kit names, which supersedes B2146/R339 (never launched). The records seat writes only record files outside the repository. X82 writes none of them and reads `BACKLOG.md` for 137, 138 and 121 only. The NOT-yours folders now include `.tools/b2161`, plus the records seat's actual folder if its kit names another.
3. **Line 126 (old 125), FACTS 7.** Keeps the B2146 sentence and adds:
   - B2146 is SUPERSEDED by B2161, never launched (RELAYED from this commission).
   - A records seat may run beside X82, and what it touches.
   - The lock as measured: owner B2157, written 17:40:20, "max 100 min".
   - "A lock held by B2157 at your launch is EXPECTED: it is never broken, and HEAVY's waits cover it."
4. **Line 136 (old 135), PRIOR-WORK CHECK (1).** OLD: "The records pass of pull request 58 has ended: the STATUS named in Stamp S3 ends with its READY line (print it);". NEW: "Your three owed items are open (a records seat may be live beside you; revision B2162 dropped the wait for its READY line):". The BACKLOG startswith check (137, 138, 121 exactly 1 each; control 122 [x]) is unchanged.
5. **Line 148 (old 147), PARTITION (c).** It now reads "kit B2161, seat R341 or the seat its kit names; it supersedes kit B2146, never launched), which may run BESIDE you".
6. **Line 175 (old 174), CHAIN INPUTS row 0.** "S3 the records seat's READY" becomes "S3 the records seats live or not". I changed this row although the commission named only row 1, because slot S3 changed.
7. **Line 176 (old 175), CHAIN INPUTS row 1.** The records seat's STATUS is gone as an input. NEW input: the live `BACKLOG.md`, its three lines only (a records seat may run beside you: you write none of its record files). NEW source: `<project>/BACKLOG.md` exists; a records seat beside you may change its other lines, and no records pass ticks these three.
8. **Line 196 (old 195), REFUSE AT ONCE.** The clause "or Stamp S3 does not name the records seat's STATUS ... `READY `" is dropped. The pane refuse becomes "Any pane but yours whose name holds `OXPd2-X` or `OXPd2-G`", with "a pane whose name holds `OXPd2-R`, a records seat, is NOT a refuse: revision B2162". "A held lock is NOT a refuse" was already there.
9. **Line 213 (old 212), Q6.** The default launch condition is now: no other OXPd build or gate pane live. A records seat (`OXPd2-R`, B2161, which supersedes B2146) may run beside it, under the same touch rule.
10. **Line 225 (old 224), slot S3.** It now names "the records seats live or not at the stamp, by pane name, no READY line required; the live `Datasec/OXPd2` panes, none but this seat's named `OXPd2-X` or `OXPd2-G` at launch".
11. **Line 231 (old 230), launch line.** The rule text matches Q6. **The kit path in the launch command now points at the rev1 file.** The commission did not list this change, but without it the launch would run B2153 unchanged (D1).

## Facts re-measured (instrument, clock by `date`)
- **main:** `gh api -X GET repos/datasecau/OXPd_2/commits/main` (project `GH_CONFIG_DIR`) at 17:49:50 printed `760e1a644ce9a419cf1b9132d0776e9e5eac1cac`, tree `8e3985c1...`. This equals B2153's BASE, so no BASE number changes. Open pull requests: 0. `matching-refs/heads/b2153`: 0.
- **Panes:** `tmux list-panes -a -F '#{@cockpit_name}'` at 17:52:27 listed `tuesday` plus two unnamed panes. Counts of `OXPd2-X`, `OXPd2-G` and `OXPd2-R` were all 0 (control `tuesday`: 1).
- **Lock:** `cat .tools/wave1-heavy.lock.d/owner.txt` at 17:51:58 printed `B2157 | pid 92618 | parallel-heavy-build experiment, re-commission (Tuesday s334), max 100 min, ... | 2026-11-27 17:40:20`, so it is held until about 19:20 at most.
- **BACKLOG:** sha256 is `74800003...`, 1212 lines, unchanged from B2153's read. An in-process startswith check found 137, 138 and 121 open, 1 each; control `122. - [x] `: 1.
- **Lane folders:** `ls -d` found no `.tools/b2146`, no `.tools/b2153` and no `.tools/b2161` (all three: No such file or directory). The B2161 kit is not yet in briefs, so the seat id R341 is RELAYED from its commission.
- **Waiter:** `launch_when_cool.sh` and `brief_seat.sh` have no OXPd one-seat check of their own (grep for `oxpd|cockpit_name` found only a model comment in brief_seat.sh line 32). The narrowed rule therefore lives in the kit alone.

## The sidecar
- Every line B2153 did not change moved down by one, so every claim id changed (the id hashes the line number).
- 136 claims carry B2153's measurement unchanged, with a new id and `(kit line N+1)`. Each sits on a line byte-equal to B2153's line N.
- 20 claims sit on changed lines:
  - 4 are freshly measured: `OXPd2-X`, `OXPd2-G`, the lock's `owner.txt`, and `137. - [ ] `.
  - 16 are literals B2162 did not change. Each is marked "carried (clause rewritten by B2162)" with B2153's measurement.
- Two B2153 claims dropped out because their wording window changed (`.tools/b2138` and `.tools/b2146` on line 1). Both folders are still named.
- Programs: `fleet/state/s334/d2162/map_sidecar.py` and `write_sidecar.py`.
- Unfilled slots: 9 four-underscore lines, the same as B2153 (S1 to S8 plus the last line). Non-ASCII bytes: 0.

## D-decisions (mine, within the commission)
- **D1:** The launch line's kit path changed to rev1. Otherwise the launch would run B2153.
- **D2:** CHAIN INPUTS row 0 also changed (S3's meaning), to keep the kit consistent.
- **D3:** The STATUS, HANDOVER, branch, lane and READY names stay `B2153`, as "every other byte unchanged" requires. The seat still writes `2026-11-27_B2153_STATUS.md` and ends `READY B2153: <sha40>`.
- **D4:** Line 29 (old 28) is left as is: "the records pass of pull request 58 will change it: re-read your three items". It does not name B2146 and is still true. The commission did not list it.

## Questions for Tuesday (each with a default)
- **Q1:** Should `OXPd2-Z` (Azure boundary seats) and any non-X/G/R OXPd pane also be a refuse? Default: NO. The commission's pattern is followed exactly; such panes take no OXPd heavy lock role here.
- **Q2:** If B2161's seat id is not R341, should the kit be re-drafted? Default: NO. The kit says "R341 or the seat its kit names" and refuses on pane prefix only.
- **Q3:** Should the STATUS and READY names stay B2153 (D3)? Default: YES. Tuesday's stamp and gate read B2153 names.

## UNMEASURED
- B2161's kit, its actual seat id and its lane folder (not yet written).
- Whether B2157 releases the lock before X82's first heavy job. HEAVY's waits apply (30 minutes per job, about 60 in all), then `BLOCKED: lock held`.

## Outside the fences
None. I wrote only these four files under `tuesday/briefs/` plus scratch under `fleet/state/s334/d2162/`. Everything else I only read: GitHub (GET), tmux, the lock's owner.txt and `BACKLOG.md`. I read nothing in `Source_Documents/`, `4_Credentials/` or any key folder, and typed no `cd` (one attempt was refused by the hook before it ran).
