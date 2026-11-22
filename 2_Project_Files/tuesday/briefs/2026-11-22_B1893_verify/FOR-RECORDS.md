# B1893 FOR RECORDS: lane I refuse round (kit B1892) at head a9dc8cd on main e1e8043d (verdict NO GO, round 3; landing on the card's option a)

The verdict stands as written (VERDICT.md). This file was rewritten after Tuesday relayed the card's ruling (datasec-oxpd-ci-guards-round3-nogo-1122, choice a, ruled_ts 2026-11-22T14:58:00, label verbatim "Merge now, the two shapes ticketed as known limits"). The landing texts in this folder follow from that label. None of them says anyone approved the code.

## The merge (measured for head a9dc8cd ONLY; `evidence/merges3.log`)
| Merge | Tree | Rules | `build/tests` | Files |
|---|---|---|---|---|
| main e1e8043d + a9dc8cd | `458df92f03ab0e0f8240e65f8b65d6c64458e5f2` (both orders) | `RULES: clean (478 files)` | `Ran 111`, OK | 478 (476 + the lane's 2 new files) |

- Main's own push run 44964415576 was read by me by GET (`evidence/hosted-main.log`): linux 1524/1520/4, windows 1524/1505/19, GUARD 10 and 11, rules `Ran 60`, `RULES: clean (476 files)`. PASS.
- The merge-ref and the after-merge push run should read: total 1524 on both legs (skipped 4 and 19), `RULES: clean (478 files)`, `Ran 111`, floor 111, GUARD 10 and 11, the hardened secret-scan lines. These are DERIVED from equal merge inputs; the lane adds no .NET test.

## Both readers' findings (this round)
| Reader | # | Severity | Inside the three refusals? | Finding | State |
|---|---|---|---|---|---|
| B1893 | G1 | MAJOR (parser-dependent) | yes, refusal 2 | An open quote after `${{` in a plain key (`a${{: "b }}`) is not refused, because the expression removal takes the opening quote. Measured rc 0 through the whole program; libyaml valid with a hidden job | follow-up ticket (below) |
| B1893 | G2 | records | no (R6 flow rule) | The same removal hides a `{` on that line (`a${{: {b: "}}"}`) | follow-up ticket (below) |
| B1893 | G3 | Minor (cells) | yes, refusal 2 | No cell has an expression before the quote; the tab subTest is also caught by refusal 1 | follow-up ticket |
| B1893 | G4 | records | no | n1 and n2 (tab shapes) survive in the unit suite but are equivalent through the whole program | records |
| B1893 | G5 | records (conduct) | no | Two of my commands were refused by hooks before they ran: a stray `cd`, and a write verb on a variable path | records |
| B1893 | G6 | records (conduct) | no | B1894's r4: my session scratchpad was shared with B1894's. My `head2/repo_rules.py` (byte-equal to HEAD2's file) and two programs (`probes/x3full.py`, `probes/x3spec.py`) landed in folders B1894 also used. Its own record says no run of its reads them and nothing was deleted. Later work of mine (the P1 reproduction) went into `b1893only/` | records |
| B1894 | P1 | MAJOR (parser-dependent) | yes, refusal 2 | A quote inside a plain key (`k "x: "a`, then `  b: |`, then `    "`) is paired by `yaml_scan` with the value's real opener, so the open value is not refused. Variants: single quotes, mixed, column 0, a sequence entry, and two through expression removal. **Reproduced by me** (`evidence/p1repro.py`, `evidence/p1repro.log`): `p1-dq` and `p1-sq` rc 0 `RULES: clean (1 files)`, libyaml valid with hidden `runs-on` and an unpinned `uses`; the control without a quote in the key rc 1 R6 :220 | follow-up ticket (below) |
| B1894 | m11 | Minor (cells) | no | 3 of its 21 round-2 mutants survive (`n-yaml-hash-anywhere`, `n-r8-comment-any-word`, `n-g3-cpio-binary-one-order`) | records (RELAYED) |
| B1894 | r3, r4 | records | n/a | `x85_probe.py` prints `R6 []` by design; the shared-scratchpad incident (G6) | records (RELAYED) |

Refusals 1 and 3 hold for both readers: B1894 found 167 of 167 byte shapes refused and 12 more quoted-attribute shapes refused (RELAYED); I found 21 more shapes refused.

## THE FOLLOW-UP TICKET (text for Tuesday to file; no key exists yet)
**Title:** CI guards: the open-quote refusal of R6 misses two quoted values spread over lines (expression in a plain key; quote inside a plain key)

**Body:**
- **What:** R6 refuses a line outside a block scalar that leaves a quoted value open at its end. Two shapes leave a value open in YAML while `yaml_scan` reads the line as closed, so the next lines are read as YAML and a continuation line ending `: |` opens a phantom block that hides the rest of a job from R3, R4 and R6.
  1. **An expression in a plain key:** `a${{: "b }}` (or `'b }}`). The `${{ ... }}` removal (`R6_EXPRESSION`, non-greedy, blind to quotes) runs before `yaml_scan` and removes the opening quote. Measured rc 0 through the whole program at a9dc8cd; libyaml valid, with job-level `permissions: write-all`, an unpinned `uses` and a flow mapping hidden.
  2. **A quote inside a plain key:** `k "x: "a` (also single quotes, the two mixed, column 0, after `- `). `yaml_scan` opens a quote at any token start, also inside a plain scalar, and pairs the key's quote with the value's opener. Measured rc 0 by both readers; libyaml valid with hidden keys.
- **Both are parser-dependent:** each needs a continuation line indented less than its mapping (YAML 1.2 forbids it; libyaml accepts it). GitHub's parser is UNMEASURED. For shape 1 GitHub probably refuses an unclosed `${{` in a key (DERIVED, unmeasured). Both existed before the refusal commit (rc 0 at ff1defac).
- **Backstop today:** `REVIEWED_WORKFLOW` holds the whole workflow file, so any edit of `ci.yml` is red until a person reads it and moves the fingerprint, and `ci.yml` is the only workflow file allowed.
- **Fix sketches, measured in readers' scratch only:**
  - (i) Also take the open-quote reading on the raw line: `if left_open or yaml_scan(line)[1]:`. This closes shape 1. B1893 measured `Ran 111` OK, `RULES: clean (412 files)`, shape 1 rc 1.
  - (ii) A quote outside a block that is not the first character of a value (the line's first non-blank, after `- `, or after `: `) is an R6 finding. This closes shape 2. B1894's census: 0 such lines in today's `ci.yml`.
  - (iii) Alternative to (i), covering G2 too: refuse any `${{` before a line's first `: ` (an expression in a key). Census UNMEASURED.
- **Cells to add:** shapes 1 and 2 in double and single quotes, each with a hidden quoted key that must fire; the expression-hidden `{` (G2); mutants dropping (i) and (ii).
- **Also carry:** B1890 F2 / H39 (`key: ${{ x }} |`, invalid YAML); B1891 m9, m10 and B1894 m11 (surviving mutants and G3 formats); G3 above.

## Records items (carried)
- The kit's named limits this round: H32 (a non-workflow file under `.github/` is not byte-bound), H34 (a workflow file's name), H35 (CRLF fails closed), H39, H42 (untracked attribute sources). The costs: no unclosed quote in a plain scalar outside a block; no quoted `.gitattributes` pattern.
- Round 2's named limits H17, H19, H20, H23, H26 to H29 and D25 records, and round 1's FOR RECORDS (`SETUP_RUNBOOK.md` item 4 to name `build/squash_scan.py`; `BACKLOG.md` lines 120 to 148; NOT DECIDED 1 to 3) stand.
- Unchanged against the yardstick:
  - my 22 round-1 mutants: 17 killed, m12 survived as the named equivalent, 4 re-made and killed;
  - my 8 round-2 mutants: 6 killed, n1 and n2 survived;
  - `mutants3.py`: 13 of 13 killed;
  - CodeQL: 0+0 at the head, 3+3 at the control;
  - hosted run 44980825061: PASS with `--unit 111 --floor 111` (control `--unit 108` FAIL 2).
- Landing texts: words2 `WORDS: clean (4 files)`; gitleaks over the title and body rc 0; `squash_scan.py` on the placeholder subject and the body `SQUASH-SCAN: clean` (`evidence/squash-scan.log`). The subject with the real number must be scanned again before the merge (landing.txt step 5).
