# B1890 FOR RECORDS: lane I fix round (kit B1882) at head ff1defac on main ca94ed96 (verdict NO GO, round 2 of 2)

## The merges (measured for head ff1defac ONLY; `evidence/merges2.log`)
| Merge | Tree | Rules | `build/tests` | Files |
|---|---|---|---|---|
| main ca94ed96 + ff1defac | `9a1e42a23551ca4d8f87946dd9536451b17cae2a` (= Tuesday's S3 tree) | `RULES: clean (446 files)` | `Ran 108`, OK | 446 |
| main ca94ed96 + ff1defac + lane G edaa1b70 | `f82bc8949772cd1e6db7840456c07dbbb3729f3f` | `RULES: clean (478 files)` | `Ran 108`, OK | 478 |

- After a landing at this head, a pull-request merge-ref run on main ca94ed96 reads `--rules 446 --unit 108 --floor 108` (DERIVED from equal merge inputs).
- Lane G (edaa1b70, now on main ca94ed96, ahead 5 and behind 0, 476 files, `FLOOR=60` on its own branch) touches nothing under `build/`, `.github/` or `README.md`, and no `.gitattributes`. Its merge-ref run after this lane lands reads `--rules 478 --unit 108 --floor 108`.
- **A fix round for F1 moves `Ran` and `FLOOR` past 108 (one cell or more). Re-measure both rows on that head.**

## For the fix round's kit (if the product owner's card sends one)
- **F1 (MAJOR).** Refuse a line outside a block whose `yaml_structure` leaves a quote open (a multi-line quoted scalar).
  - Measured in my scratch copy only: the suite `Ran 108`, OK; `RULES: clean (412 files)`; today's `ci.yml` holds 0 such lines, so no fingerprint moves; the phantom shape gives rc 1.
  - Cells: an open `"` and an open `'` whose continuation line ` x: |` sits below its key, each with a quoted key under it that must fire. Add a mutant that drops the open-quote test.
  - Correct the R6 docstring and kit D15's "its rest is never read as YAML".
- **F2.** Read the block start on the YAML with its `${{ }}` expressions kept, or name `key: ${{ x }} |` (invalid YAML) as a limit.
- **F3.** Cells for a `#` after a tab (`jobs:\t# x: |`, which fires at the head) and for a quote after a tab.
- **F4.** `"x"#: |` is invalid YAML (Psych): a record, not a hole.

## Records items (RELAYED, still open)
- Round 1's FOR RECORDS stand: `SETUP_RUNBOOK.md` item 4 to name `build/squash_scan.py`; `BACKLOG.md` lines 120 to 148; NOT DECIDED 1 to 3.
- The kit's D25 records stand: PKCS7 PEM or `x5c` JSON; a lone CR in a squash message; `'a''b':`.
- The kit's named limits H17, H19, H20, H23 and H26 to H29 stand.
- The seat's deviation (the neutral-copy glob) is ruled ACCEPTED in VERDICT.md.
- **Q14 and Q26 hold as built.** Round-1 F1 is closed (`p1full` rc 1 on both shapes). My 22 round-1 mutants give 17 killed, m12 survived (equivalent), and 4 re-made, all killed.
- Local CodeQL: head 0+0, control 3+3. The hosted run 44961377381 PASSes with `--unit 108 --floor 108 --rules 412`.
