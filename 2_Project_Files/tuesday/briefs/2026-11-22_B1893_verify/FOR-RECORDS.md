# B1893 FOR RECORDS: lane I refuse round (kit B1892) at head a9dc8cd on main e1e8043d (verdict NO GO, round 3)

## The merge (measured for head a9dc8cd ONLY; `evidence/merges3.log`)
| Merge | Tree | Rules | `build/tests` | Files |
|---|---|---|---|---|
| main e1e8043d + a9dc8cd | `458df92f03ab0e0f8240e65f8b65d6c64458e5f2` (both orders) | `RULES: clean (478 files)` | `Ran 111`, OK | 478 |

- If this head lands as it is, a merge-ref run on main e1e8043d should read `--rules 478 --unit 111 --floor 111` (DERIVED from equal merge inputs). Its hosted Linux and Windows totals are UNMEASURED; main's own push run read `--total 1524` (RELAYED from the kit's Stamp S2).
- A fix for G1 with two cells moves `Ran` and `FLOOR` to 113. Re-measure the row on that head.

## For a fix of G1 (if the product owner's card sends one)
- **Default:** in `check_spellings`, judge the open quote on the raw line as well: `if left_open or yaml_scan(line)[1]:`.
  - Measured in a scratch export only: `Ran 111`, OK; `RULES: clean (412 files)`; both G1 shapes `rc 1`; no fingerprint moves (`ci.yml` is untouched).
  - Cells: `a${{: "b }}` and `a${{: 'b }}` under `env:`, each followed by ` x: |` / `  y` plus its quote, then a quoted key that must fire.
  - Mutant: drop the raw-line test.
- **Alternative (a plain refusal):** R6 refuses any `${{` before a line's first `: ` (an expression in a mapping key). This also covers G2 (`{` hidden behind the same removal). The census of today's `ci.yml` for such keys is UNMEASURED.

## Records items
- G2: `a${{: {b: "}}"}` hides a flow mapping from the `{` check on its own line. libyaml reads it as valid. It sits under R6's older flow rule, outside the three refusals.
- G3: the open-quote cell lacks an expression-before-quote shape. Its tab shape is also caught by refusal 1.
- G4: n1 and n2 (tab shapes) survive in the unit suite, but they are equivalent through the whole program because refusal 1 refuses a tab.
- G5: reader conduct. Two of my commands were refused by hooks before they ran: a stray `cd`, and a write verb on a variable path. Neither changed any state.
- Round 2 B1890 F2 / H39 (`name: ${{ github.sha }} |`, Psych INVALID) is still quiet, as the kit says. F4 (`"x"#: |`) is still quiet and invalid YAML.
- Refusals 1 and 3: no hole found in 21 extra shapes through the whole program (`evidence/x3full.log`).
- Unchanged against the yardstick: my 22 round-1 mutants (17 killed, m12 survived as the named equivalent, 4 re-made and killed), my 8 round-2 mutants (6 killed, n1 and n2 survived as above), `mutants3.py` 13 of 13, CodeQL 0+0 at the head and 3+3 at the control, and hosted run 44980825061 PASS with `--unit 111 --floor 111` (control `--unit 108` FAIL 2).
- Round 1 and round 2 FOR RECORDS stand. So do the kit's named limits H32, H34, H35, H39 and H42.
