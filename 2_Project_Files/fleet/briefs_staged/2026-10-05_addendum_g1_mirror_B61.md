To Seat B 61st only (pane `Secuura/Blockchain`, %29). From Wednesday. This ADDENDUM changes no GO and no ruling on PR A (KS-1388). Apply it BEFORE your next ref write. Per STANDING_LINES :399, LIST the inbox by API after your current action, so this mail is not lost behind a wall-clock SINCE.

## BLUF
Two new pushing seats are launching:
- **Seat G 1st**: pane `Secuura/Blockchain-G`, token `g1`, lock `.push-lock-g1`. Script-tooling lanes: `run-shell-suites.sh`, `preflight.sh` + `run-code-guards.sh`, `scripts/audit/*.mjs` + `scripts/preflight/lockfile-cleanroom.sh`.
- **Seat D 8th**: pane `Secuura/Blockchain-D`, token `d8`, lock `.push-lock-d8`. KS-1404 anchor wiring: `docker-compose.yml` timestamping env + the timestamping `Dockerfile`.

Today your tools read both locks as UNATTRIBUTED (**rc 11**). That is a correct STOP, but it would freeze you mid-push. **Both become WAITs, in ONE change, so you re-prove once.** Your `lock56.sh`/`push56.sh` have **only TWO WAIT slots**, so you must ADD a third AND a fourth. Neither new seat takes ANY lock until Wednesday quotes your ACK to it.

## The change (both files, every `_CHK` twin, byte-identical order)
1. **Add `OTHER_LOCK3` = `"$(dirname "$LOCK")/.push-lock-g1"` and `OTHER_LOCK4` = `"$(dirname "$LOCK")/.push-lock-d8"`** in `lock56.sh`, hand-wired after `:287` (`OTHER_LOCK2` = `-e4`). Add **`OTHER_LOCK3_CHK` = `"$_LOCKPARENT/.push-lock-g1"` and `OTHER_LOCK4_CHK` = `"$_LOCKPARENT/.push-lock-d8"`** in `push56.sh`, after `:165`. Use the same literal style as your `:274`/`:287` lines: your 08:31Z ACK records a regex patch that missed one of those quote forms. Match the literal, then re-verify that take and re-check agree.
2. **Wire BOTH new slots into EVERY site that reads slots 1-2.** Model the wiring on Seat E 4th's three-slot build (`locke4.sh:283/:345/:385/:437`, `pushe4.sh:168/:201`). The sites:
   - `lock56.sh:268`: the env refusal;
   - `:352-:353`: KNOWN, so that a live `-g1`/`-d8` is no longer rc 11;
   - `:384`: the take/re-check loop;
   - `:393-:420`: the per-name bounded wait and stale check (via `OTHER_LOCK_CUR`);
   - `push56.sh:157`: the env refusal;
   - `:187`: KNOWN;
   - `:212`: the re-check loop;
   - `:220`: the message.

   **Grep every `OTHER_LOCK2` occurrence in both files and show that each one has slot-3 AND slot-4 siblings.** A slot the take reads but the re-check does not is the mid-window hole.
3. STOP stays at your 16 (`55 e2 f2 e3 f1 e1 54 c21 d2 d3 d4 d5 d6 53 52 51`). `-d7` (D 7th, WRAPPED, no lock), `-c24` and anything unknown stay caught by your catch-all (rc 11).
4. FOREIGN: namecheck56 already has `g1`/`seatg1` and inbox_match56 already has `g 1st`/`seat g 1st` (your ACK, 08:31:22Z). **Add `d8`/`seatd8` (segment-anchored, `-d8-\d+$`, `s-d8-`, `.push-lock-d8`) and `d 8th`/`seat d 8th`.** Attribute D 8th's ref by EXACT name only (`feature/ks-1404-tsa-anchor-wiring-d8-1`): `d8` is a hex digraph, and 111 `refs/heads` contain it raw. `feature/ks-539-g1-split-ruling` stays FOREIGN to everyone. Show a tamper per new constant that fires at least one arm.

## ACK required
Send STATUS **`mirror g1 d8 ACK (Seat B 61st)`**, with `twolock56.sh` re-run against an EMPTY scratch dir, never the real `worktrees/`. It must show:
- **live `-g1` → WAIT (rc 8)** and **live `-d8` → WAIT (rc 8)**: lock NOT taken, planted lock still present. Also, one slot-3 and one slot-4 RE-CHECK arm: the lock injected between take and re-check → you RELEASE and your file is gone;
- **slots 3 and 4 now SET**: the four WAIT names extracted from `lock56.sh` AND `push56.sh`, side by side → IDENTICAL, plus a control comparison that correctly says NO;
- **nothing else changed**:
  - `-f3`, `-e4` still rc 8;
  - each of the 16 STOP still rc 10;
  - `-d7`, `-c23`, `-c24` and an unknown `-zz9` still rc 11;
  - stale is still a STOP;
  - nothing planted → rc 0;
- **CHECKED counts**: your tool enforces its arm count (23 at 08:31Z). State the NEW enforced count with its breakdown (−1 UNATTRIBUTED `-g1`, +2 WAIT, +2 re-check), and the KNOWN-names count (17 → 19);
- **take and re-check byte-identical**: the WAIT and STOP sets of both files, in the same order;
- the real `worktrees/` lock population before and after (unchanged), and the sha256 of `lock56.sh`/`push56.sh` before and after (before = `e13c12ea01dde441…` / `dd58f55d7ef54d8a…`).

PROVENANCE:
- B 61st has 2 WAIT slots, `-f3`/`-e4`. Sites: `lock56.sh:274/:287`, loop `:384`, KNOWN `:352-:353`, env refusal `:268`; `push56.sh:157/:162/:165/:187/:212/:220` | `grep -n` + `sed -n` | read 2026-10-05T08:50Z.
- `-g1` = rc 11; arm count 23; KNOWN 17; g1 FOREIGN entries | B 61st's STATUS `mirror e4 f3 ACK (Seat B 61st)` | read 2026-10-05T08:31:22Z.
- `d8` appears 0 times in `lock56.sh`; 111 raw `d8` refs | D 8th brief P13/P15 (`/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-10-05_seatD8_ks1404_wiring.md:17-:19`) | read 2026-10-05T08:43-08:47Z.
- Three-slot model: `locke4.sh:283/:345/:385/:437`, `pushe4.sh:168/:201` | read 2026-10-05T08:50Z.
- Hashes: `shasum -a 256` of `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-10-05_seatB-61st/raise/{lock56,push56}.sh` (mtime 08:28Z) | read 2026-10-05T08:50Z.
- New seats' identity and lanes: `…/briefs_staged/2026-10-05_seatG1_scripts_lane.md` + `…_seatG1_AMENDMENT.md` W1-W5; `…_seatD8_ks1404_wiring.md` + `…_seatD8_AMENDMENT.md`.
