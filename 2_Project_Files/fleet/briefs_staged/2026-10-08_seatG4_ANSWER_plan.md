## BLUF
Plan **CONFIRMED** (Seat G 4th), and your two slugs are ACCEPTED as written:
- G-A `feature/ks-593-not-a-server-error-originate-three-passes-g4-1`
- G-B `feature/ks-1171-b1-absent-boundary-is-inclusive-g4-2`

Key namecheck's row tables once, on these. **ctx 26%** (Wednesday read your pane %96 statusline at 06:14:48Z). Proceed: phase-2 re-key + namecheck and trap4 arms → `STATUS: raise base` → hold for acceptance by name → G-A → G-B, each to READY FOR QA.

## One thing you did not have: develop's objects
**Seat R 18th measured develop `0a6177ea5482`'s objects ABSENT from the shared store** (`cat-file -e` with a positive control on `ddea005553bf`). R 18th performs ONE objects-only transfer under ITS lock `.push-lock-d8`. **Do NOT transfer yourself.** Two seats writing the same objects into one store is exactly the shared-resource collision the parallel block warns about. At your RAISE_BASE, measure `cat-file -e` on develop's tip with the same positive control:
- **Present:** your Q-OBJ is a recorded no-op; say whose transfer put the objects there.
- **Absent:** mail `QUESTION: objects (Seat G 4th)` and wait. Do not transfer.

## Your six items
1. `reseat_g4.py` written fresh instead of running `reseat_g3.py` with G 3rd's and G 2nd's scratch UUIDs: right.
2. **`WED_USAGE_STOP` absent in your shell is expected.** It is a launch-time knob read by Wednesday's launch tools (`brief_and_launch.sh` → `usage_gate.sh`), and your seat launches nothing. The brief's "launches with" described the launch, not your environment.
3. **No independent re-key auditor:** accepted and recorded. Say so in any mail that rests on a re-key, as you did.
4. Flow 30 (NEW reader) vs 25 (SAME): noted; your reading agrees with the brief.
5. A7: correct handling. A merge GO addressed to you in this round is a mismatch: mail it, act on nothing.
6. Your two self-caught instrument faults: good; both go in your handover.

Peter's newest KS-593 comments (auth `wallet/verify`) are outside your three passes: agreed, no scope change. KS-593 stays OPEN.
