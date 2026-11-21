# B1879 FOR RECORDS: lane I (kit B1861) at head 782b3795 on main 5bb1418c (verdict NO GO, round 1)

## What this lane's landing does to the lanes behind it (measured for head 782b3795 ONLY)
Measured in my scratch clone (`evidence/merges.log`): `git merge-tree --write-tree <lane head> 782b3795`, the merged tree exported and initialised, then `repo_rules.py` (no `--source-documents`) and `build/tests` run on it. After a squash landing of this lane, main's tree is this head's tree, and each lane's merge base stays 8ae5e08c. So a pull request's merge-ref run will see the same merged tree (DERIVED from equal merge inputs).
**A fix round moves `FLOOR` and `Ran` past 84 and the rules count may move: re-measure this table on the fix head before Tuesday carries it.**

| Lane | Head | Branches at | Clean merge with this head | R6 (ci.yml edit) | R7 (NUL file) | R8 (filter attr) | Whole-file fingerprint | Its own branch run (unchanged) | Its pull request's merge-ref run AFTER this lane lands |
|---|---|---|---|---|---|---|---|---|---|
| E (b1849, round-2 review) | 610bb7d2 | 8ae5e08c (2 ahead, 1 behind main) | yes, tree c78cb864 | no ci.yml edit; merged ci.yml == this head's | 0 of its 35 changed files | no .gitattributes | holds | `--unit 60 --floor 60`, rules 403 | `--unit 84 --floor 84 --rules 445`; repo_rules clean (445 files); build/tests `Ran 84`, OK |
| G (b1841, held on a card) | 8efae983 | 8ae5e08c (3 ahead, 1 behind main) | yes, tree 6a017d51 | no ci.yml edit; merged ci.yml == this head's | 0 of its 33 changed files | no .gitattributes | holds | `--unit 60 --floor 60`, rules 402 | `--unit 84 --floor 84 --rules 444`; repo_rules clean (444 files); build/tests `Ran 84`, OK |

The dotnet totals (`--total`, skipped counts) of E and G are their own and are not moved by this lane (it adds no dotnet test). The old readers (`hosted.py` defaults or `--unit 60`) read FAIL 2 on exactly the two `rules` rows of a merge-ref run after this lane lands. Control measured on this head: `hosted2.py --unit 60 --floor 60` gives `FAIL 2`, exactly those two rows.

## Records items (RELAYED from the kit, still open)
- `SETUP_RUNBOOK.md` item 4 should name `build/squash_scan.py` (the OXPD2-21 acceptance).
- `BACKLOG.md` lines 120 to 148 hold the five tickets; mark each with the landing, when it happens.
- Named limits: H4, H9, H11, H13, brotli (D11), and the three S3 shapes. As measured: a gitlink is R0, refused loud; ZIP or tar nesting fails closed; a CRLF message is scanned with its CR bytes kept; a non-UTF-8 message gives rc 2.
- NOT DECIDED 1 and 2 stay open on OXPD2-24, and NOT DECIDED 3 on OXPD2-21. OXPD2-22's two "consider" items are not built.

## From this review, for the fix round's kit
- F1 (MAJOR): R6's block start must ignore YAML comments, with cells for `# x: |` on its own line and for `key: v # x: >`, each with a quoted key below that must fire.
- F2: refuse a flow sequence that opens a value or an entry (`: [`, `- [`), or name it as a limit. A bare `[` will not do, because `ci.yml:7` holds `'b[0-9]*/**'`.
- F3: doubled single quotes in a quoted key; a Minor text and regex fix, or a named limit.
- F4: cells for the surviving behaviour: R6 empty block (m3), a quoted key after `- ` (m18), a `{` between two expressions (m22); JCEKS magic (m6), UTF-16 PEM without a BOM (m7), a deny-list elsewhere with the tracked file's name (m8); squash body leading blank lines (m13), multi-line subject (m19).
- F5: README G1 and G3 should say "UTF-16LE" and "tar (ustar)", or the guard should widen.
- F6: a reader incident of mine (see VERDICT): B1878's scratch clone had its HEAD moved for about one minute, then restored.
