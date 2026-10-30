STARTABLE: YES (after your stamp; read D-1 first, I recommend NO merge, which differs from your default)

# B951 drafter report (Sonnet 5.5, 2026-10-30 about 16:35 to 16:55 AEDT)
Kit: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-30_B951_SEAT-H73_hpsmpoc-251-round2-non-bool-if-row.md` (145 lines; 9 four-underscore lines = 8 slots + the last line; 0 non-ASCII). Read-only: `gh api -X GET`, `ls-remote`, one function-level probe on scratch copies (no suite or test run), no write, no cd.

## BLUF
Seat `Datasec/HPSM-POC-H73` (Sonnet) adds ONE commit on `b933/hpsmpoc-403-404-infra-test-extensions` (child of `a8b9e81a`), one path, a pure insertion of ONE new test method (3 conditions x 2 branch orders, all expecting the existing "read in dev, uat, demo, can take a branch" message). Shown: m16 alive on the unedited head, red through the new row only, green without the mutant. Counts 130 -> 131 and 308 -> 309.

## Facts re-measured
- Branch tip = a8b9e81a; main = 37bc6323; PR #251 open, clean, +143 -14; open PRs 252 251 250 248 245. File blob `000e676a...`, 2743 lines, sha256 `ac55fe11...`; 130 methods; m16 line 1195 (anchor count 1); existing `if` row 1898; green row 1912 (insertion anchor).
- Compare e21d8044...37bc6323: 38 files, 0 under infra/, 0 ci.yml, 0 for the two web tests (control 1).
- Branch protection strict = false (5 contexts); ruleset strict false. The push recomputes the merge ref; so required contexts run on the new base without a merge.

## Probe (six plants, original and m16)
Conditions `parameters('flag')` (Symbolic), `concat('a','b')` ('ab'), `createArray('a')` (tuple). Scoped branch FIRST: original RED, m16 GREEN. Scoped branch SECOND: original RED, m16 RED. **Only the 3 scoped-first entries kill m16**; the gate's "both branch orders" is kept for the message pin, but the kit says plainly which entries kill (D-2). Predicted m16 + row: Ran 131, failures=3.

## D-decisions (default)
- D-1 NO merge (your default was YES). Reasons: 0 guarded paths either way; a merge adds a second commit and 38 web files to the delta the gate must reproduce; the push alone recomputes the merge ref (Condition B943-8 answered); up-to-date not required. The YES path is written in the kit in one paragraph.
- D-2 which entries kill: scoped-first. D-3 one new method, not subtests (the counts 131/309 need it). D-4 B943-2..-7 stay out (records seat).

## Q (default)
- Q-1 reuse the three read-only b916 helpers, with `-I` changed to `-I -B`. YES.
- Target READY 90 / hard stop 150 minutes (drafter's suggestion; Tuesday's call).

## Slot recommendations
STAMP / KEYS (HPSMPOC-403 and -404) / LAUNCH WINDOW (load1 was 21.95 at 16:35: launch_when_cool) / Stamped by / Launch authority (the usual grants) / Hard stop 90+150 / Head a8b9e81a, main 37bc6323, no b951 ref / receipt line given in the Stamp paragraph.

## Wrong at source in the gate or builder STATUS
- None in the gate's findings: B943-1 reproduced by my probe. Small: the gate's "both branch orders" implies both kill; only scoped-first does. The builder's "20 of 20 killed" is already refuted by the gate.
- Note: the ruleset's `required_status_checks` list is empty; the 5 required contexts live in classic branch protection (strict false). Not wrong, just where they are.

## Reasons not to launch now
None blocking. Load is heavy (21.95): expect the heavy lock to wait. 8 listeners exist on 9700-9999 (other seats); the kit needs none.

## UNMEASURED
The row inside the file, the whole-file runs, 309, the merge-ref recompute, CI/CodeQL on the new head.
