# SMOKE-1 arms-selfpath — make the absence-check arms find their checker relative to themselves

File: `2_Project_Files/tests/absence_claim_check_arms.sh`
Tip: `15189f1f37c316603d7c4f87d5d5d42dc024da39`
Runner: `bash`

Written 2026-09-23 14:25 AEST from the SHA above, file read whole (17 lines).

## The mode — read this twice

CODE-ONLY. Your diff touches EXACTLY 1 file: the one on the File: line, modified in place. You never touch `2_Project_Files/tools/absence_claim_check.sh` or any other file.

## What is wrong (one paragraph)

Line 3 sets `C` to an absolute path on a drive (`/Volumes/DevMASTER/WEDNESDAY/...`) that does not exist on this machine, so every arm calls a missing script and the arms exit 1 (measured at the tip: rc 1, three arms print FAIL with rc=127). The checker lives one directory up, in `tools/`, beside this `tests/` directory. Line 3 must locate it relative to the arms file itself. Nothing else in the file changes.

## The exact change

Edit 1 — line 3, replacement.
Context: line 2 is `# Arms for tools/absence_claim_check.sh. Each prints PASS/FAIL; exit 1 if any fail.`, line 4 is `arm(){ # name, text, expect_flag(yes/no)` — copy both as context.

```
-C=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/tools/absence_claim_check.sh; F=0
+C="$(dirname "$0")/../tools/absence_claim_check.sh"; F=0
```

**Do NOT touch** lines 1-2 and 4-17, the `arm()` function, any arm line, or any other file.

## The test

File: `2_Project_Files/tests/absence_claim_check_arms.sh` (the file itself is the test; there is no separate test file).
Run from the repo root: `bash 2_Project_Files/tests/absence_claim_check_arms.sh`.

## Cells and controls

- `arms` = the whole script's exit code   ← RED (rc 1) before the change, GREEN (rc 0, 9 PASS) after
- `A4` = `A4 a positive claim does NOT flag` ← control: must print PASS after the change

## The failing case (the "tamper")

Reverting Edit 1 is the tamper: with line 3 back to the absolute path the arms exit 1. The replaced line is byte-unique in the file (literal count = 1).

## Premises (each one measured, with where)

- Line 3 text at the tip — read at `2_Project_Files/tests/absence_claim_check_arms.sh:3`; literal count 1 (`grep -c -F`).
- Arms at the tip exit 1 — ran `bash 2_Project_Files/tests/absence_claim_check_arms.sh` in a clone at the tip.
- With exactly this replacement the arms exit 0 with 9 PASS, 0 FAIL — ran on a copy of the two files.

## UNMEASURED — stated rather than glossed

Behaviour when the arms file is invoked through a symlink (not exercised). The Studio, where `/Volumes/DevMASTER` exists, was not run.

## Collision

No other in-flight work on this file. First round for this brief.

## Scope

Fixes this one arms file. Two other arms files in `tests/` hardcode the same drive (`friday_seat_tools_arms.sh`, `note_entry_typed_clock_arms.sh`); they are NOT in this brief.

## Output

Exactly ONE fenced diff block, nothing outside it. Paths exactly as the File: line gives them. Every `+` line on its own physical line. Every context line keeps its leading space.
