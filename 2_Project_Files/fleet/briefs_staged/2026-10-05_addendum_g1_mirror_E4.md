To Seat E 4th only (pane `Secuura/Blockchain-E`, %34). From Wednesday. This ADDENDUM changes no GO and no ruling in your queue. Apply it BEFORE your next ref write. Per STANDING_LINES :399, LIST the inbox by API after your current action.

## BLUF
Two new pushing seats are launching:
- **Seat G 1st**: pane `Secuura/Blockchain-G`, token `g1`, lock `.push-lock-g1`, script-tooling lanes.
- **Seat D 8th**: pane `Secuura/Blockchain-D`, token `d8`, lock `.push-lock-d8`, KS-1404 anchor wiring in compose + the timestamping Dockerfile.

Your brief's hand-fix 2 (`:117`) built `OTHER_LOCK3`/`OTHER_LOCK3_CHK` EMPTY "until Wednesday's addendum names `-g1`". **This is that addendum.** It also adds a FOURTH slot for `-d8`, in ONE change, so you re-prove once. Today both locks read UNATTRIBUTED (your **rc 15**). Neither new seat takes ANY lock until Wednesday quotes your ACK to it.

## The change (both files, byte-identical order)
1. `locke4.sh:283`: `OTHER_LOCK3="${OTHER_LOCK3:-}"` → **`OTHER_LOCK3="${OTHER_LOCK3:-$(dirname "$LOCK")/.push-lock-g1}"`**, and a NEW **`OTHER_LOCK4="${OTHER_LOCK4:-$(dirname "$LOCK")/.push-lock-d8}"`** after it.
2. `pushe4.sh:168`: `OTHER_LOCK3_CHK="${OTHER_LOCK3:-}"` → **`OTHER_LOCK3_CHK="${OTHER_LOCK3:-$_LOCKPARENT/.push-lock-g1}"`**, and a NEW **`OTHER_LOCK4_CHK="${OTHER_LOCK4:-$_LOCKPARENT/.push-lock-d8}"`**.
   🔴 **Set the IN-FILE default, not an env var.** `pushe4.sh` is called BARE. A value set only in the env would leave the take waiting on a slot that the pre-push re-check does not check. That is the take/re-check disagreement B 61st caught in its own tools at 08:31Z.
3. **Wire slot 4 wherever slot 3 is wired:**
   - KNOWN `:345` (counted only when SET);
   - the take loop `:385`;
   - the post-take presence re-check `:437`;
   - `pushe4.sh:201`.
   
   Grep every `OTHER_LOCK3` occurrence in both files and show that each one has a slot-4 sibling. Slot 3 is already wired at those sites. Prove it, do not assume it.
4. Nothing else changes. WAIT = `-56`, `-f3`, `-g1`, `-d8`. STOP stays at your 16 (`-e3`, `-f2`, then the 14). `-d7` (D 7th, WRAPPED, no lock), `-c24` and anything unknown stay caught by the catch-all (rc 15).
5. FOREIGN: `g1`/`seatg1` and `d8`/`seatd8`, segment-anchored (`-g1-\d+$`, `-d8-\d+$`, `s-g1-`, `s-d8-`, the two lock names). `feature/ks-539-g1-split-ruling` is FOREIGN. D 8th's ref goes by EXACT name only (`feature/ks-1404-tsa-anchor-wiring-d8-1`): `d8` is a hex digraph, with 111 raw hits in `refs/heads`. inbox_matche4 already has `g 1st` and `blockchain-g]` (your 08:45:39Z STATUS, finding 3). Add `d 8th`/`seat d 8th`. `blockchain-d]` carries D 7th's mail too, so key on the seat ordinal. Show a tamper per new constant that FIRES at least one arm, on a REAL full-length `(Seat D 8th)` subject once one arrives.

## ACK required
STATUS **`mirror g1 d8 ACK (Seat E 4th)`**, with `twolocke4.sh` re-run against an EMPTY scratch dir (never the real `worktrees/`) and with NO `OTHER_LOCK3`/`OTHER_LOCK4` in the environment. It must show:
- **Live `-g1` → WAIT and live `-d8` → WAIT.** The lock is NOT taken and the planted lock is still present. For each of the two: injected between take and re-check → you RELEASE and your file is gone (the `:437` site).
- **Slots 3 and 4 are now SET.** Extract the four WAIT names from `locke4.sh` AND from `pushe4.sh` → IDENTICAL, plus a control comparison that says NO. Your "slot empty → `-g1` rc 15" arm now inverts: state its new expectation.
- **Nothing else changed.** `-56` and `-f3` still WAIT. Each of the 16 STOP locks keeps its rc. `-d7`, `-c24` and an unknown `-zz9` → rc 15. Nothing planted → taken.
- **CHECKED counts:** arms and KNOWN names, before and after, with the breakdown.
- **Take and re-check byte-identical:** the WAIT and STOP sets of both files, in the same order.
- The real `worktrees/` lock population before and after (unchanged), and the sha256 of `locke4.sh`/`pushe4.sh` before and after (before = `65e56969ec063d0e…` / `e8207df863249641…`).

PROVENANCE:
- Slot 3 is EMPTY and env-overridable; there is no slot 4: `locke4.sh:277-:283`, KNOWN `:345`, loops `:385`/`:437`; `pushe4.sh:163/:166/:168/:201` | `grep -n` + `sed -n` | read 2026-10-05T08:50Z.
- `-g1` = rc 15; hand-fix 2 is EMPTY until the addendum: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-10-05_seatE4_successor.md:117` and E 4th's STATUS (HF2) | read 2026-10-05T08:45:39Z.
- `d8` appears 0 times in `locke4.sh`; 111 raw `d8` refs | D 8th brief P13/P15 (`…/briefs_staged/2026-10-05_seatD8_ks1404_wiring.md:17-:19`) | read 2026-10-05T08:43-08:47Z.
- Hashes: `shasum -a 256` of `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-10-05_seatE-4th/raise/{locke4,pushe4}.sh` (mtime 08:40:02Z) | read 2026-10-05T08:50Z.
- New seats: `…/briefs_staged/2026-10-05_seatG1_scripts_lane.md` + `…_seatG1_AMENDMENT.md` W1-W5; `…_seatD8_ks1404_wiring.md` + `…_seatD8_AMENDMENT.md`.
