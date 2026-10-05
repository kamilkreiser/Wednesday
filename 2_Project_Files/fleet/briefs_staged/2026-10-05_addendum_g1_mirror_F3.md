To Seat F 3rd only (pane `Secuura/Blockchain-F`, %35). From Wednesday. This ADDENDUM changes no GO and no ruling on #1383. Apply it BEFORE your next ref write. Per STANDING_LINES :399, LIST the inbox by API after your current action.

## BLUF
Two new pushing seats are launching:
- **Seat G 1st**: pane `Secuura/Blockchain-G`, token `g1`, lock `.push-lock-g1`. Script-tooling lanes.
- **Seat D 8th**: pane `Secuura/Blockchain-D`, token `d8`, lock `.push-lock-d8`. KS-1404 anchor wiring in compose + the timestamping Dockerfile.

Your brief's hand-fix 2 (`:98`) built `OTHER_LOCK3`/`OTHER_LOCK3_CHK` EMPTY "until Wednesday's addendum names `-g1`". **This is that addendum.** It also adds a FOURTH slot for `-d8` in the same change, so you re-prove once. Today both locks read UNATTRIBUTED (your **rc 12**). Neither new seat takes ANY lock until Wednesday quotes your ACK to it.

## The change (both files, byte-identical order)
1. `lockf3.sh:328`: change `OTHER_LOCK3=""` to **`OTHER_LOCK3="$(dirname "$LOCK")/.push-lock-g1"`** (the exact form your `:328` comment names). Add a NEW **`OTHER_LOCK4="$(dirname "$LOCK")/.push-lock-d8"`** after it.
2. `pushf3.sh:195`: change `OTHER_LOCK3_CHK=""` to **`OTHER_LOCK3_CHK="$_LOCKPARENT/.push-lock-g1"`**. Add a NEW **`OTHER_LOCK4_CHK="$_LOCKPARENT/.push-lock-d8"`**.
   🔴 **Edit the literals. Never pass an env var.** `lockf3.sh:298-:302` REFUSES (exit 2) when `OTHER_LOCK`, `OTHER_LOCK2` or `OTHER_LOCK3` arrives SET. **Add `OTHER_LOCK4` to that refusal** (and to `pushf3.sh`'s equivalent, if it has one).
3. **Wire slot 4 into every site that already handles slot 3:**
   - KNOWN `:387`;
   - loops `:414`/`:431`;
   - `pushf3.sh:214`.

   Grep every `OTHER_LOCK3` occurrence in both files and show that each one has a slot-4 sibling. Slot 3 is already wired at those sites; prove it, do not assume it.
4. Nothing else changes. WAIT = `-56`, `-e4`, `-g1`, `-d8`. STOP stays as your set, with `-f2` and `-e3` first. `-d7` (D 7th, WRAPPED, no lock), `-c24` and anything unknown stay caught by the catch-all (rc 12).
5. FOREIGN:
   - `g1`/`seatg1` and `d8`/`seatd8`, segment-anchored (`-g1-\d+$`, `-d8-\d+$`, `s-g1-`, `s-d8-`, the two lock names).
   - `feature/ks-539-g1-split-ruling` stays FOREIGN.
   - D 8th's ref is matched by EXACT name only (`feature/ks-1404-tsa-anchor-wiring-d8-1`). `d8` is a hex digraph: 111 raw hits in `refs/heads`.
   - inbox_matchf3 gets `g 1st`, `seat g 1st`, `blockchain-g]`, `d 8th` and `seat d 8th` where absent. `blockchain-d]` also carries D 7th's mail, so key on the seat ordinal.
   - Show a tamper per new constant that FIRES at least one trap-4 arm, including REAL full-length `(Seat G 1st)` and `(Seat D 8th)` LAUNCH BRIEF subjects → FOREIGN.

## ACK required
STATUS **`mirror g1 d8 ACK (Seat F 3rd)`**, with `twolockf3.sh` re-run against an EMPTY scratch dir, never the real `worktrees/`. The ACK carries:
- **WAIT on both new locks:** live `-g1` → WAIT and live `-d8` → WAIT, lock NOT taken, planted lock still present. For each, a lock injected between take and re-check → you RELEASE and your file is gone.
- **Slots 3 and 4 now SET:** the four WAIT names extracted from `lockf3.sh` AND `pushf3.sh` → IDENTICAL, plus a control comparison that says NO. Your "slot empty → `-g1` rc 12" arm now inverts; state its new expectation.
- **Nothing else changed:**
  - `-56` and `-e4` still WAIT;
  - each STOP keeps its rc;
  - `-d7`, `-c24` and an unknown `-zz9` → rc 12;
  - the env-SET refusal still exits 2 (now also for `OTHER_LOCK4`);
  - nothing planted → taken.
- **CHECKED counts:** arms and KNOWN names before and after, with the breakdown.
- **Take and re-check byte-identical:** the WAIT and STOP sets of both files, in the same order.
- **Before/after evidence:** the real `worktrees/` lock population (unchanged), and the sha256 of `lockf3.sh`/`pushf3.sh` (before = `525745e17fc2af44…` / `4cc6502357e819a7…`).

PROVENANCE:
- Slot 3 is an EMPTY literal, with no slot 4 and an env refusal: `lockf3.sh:298-:302/:304/:322/:328`, KNOWN `:387`, loops `:414`/`:431`; `pushf3.sh:187/:190/:195/:214` | `grep -n` + `sed -n` | read 2026-10-05T08:50Z.
- `-g1` = rc 12, and hand-fix 2 stays EMPTY until the addendum: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-10-05_seatF3_successor.md:98`.
- `d8` appears 0 times in `lockf3.sh`; 111 raw `d8` refs | D 8th brief P13/P15 (`…/briefs_staged/2026-10-05_seatD8_ks1404_wiring.md:17-:19`) | read 2026-10-05T08:43-08:47Z.
- Hashes: `shasum -a 256` of `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-10-05_seatF-3rd/raise/{lockf3,pushf3}.sh` (mtimes 08:30:54Z / 08:32:11Z) | read 2026-10-05T08:50Z.
- New seats: `…/briefs_staged/2026-10-05_seatG1_scripts_lane.md` + `…_seatG1_AMENDMENT.md` W1-W5; `…_seatD8_ks1404_wiring.md` + `…_seatD8_AMENDMENT.md`.
