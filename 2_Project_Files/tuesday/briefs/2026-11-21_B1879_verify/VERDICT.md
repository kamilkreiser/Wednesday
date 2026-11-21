GATE B1879: NO GO @ 782b379 on main 5bb1418

# B1879 VERDICT: whole-lane reader, OXPd 2 lane I (kit B1861, seat X26), G1 round 1 of 2

Reader: B1879 (Opus 5.5), 2026-11-21, 23:19 to about 23:45 AEDT. Evidence under `evidence/` in this folder. Every number below was printed by a program in this session. I typed or printed no planted value: the programs cut it from the workflow's two halves. A program scan of this folder found it in 0 of 15 files, and the same scan found it in a planted control file. I ran no `--source-documents`, no dotnet and no lock. I wrote nothing in the OXPd_2 project folder. I made no push, opened no pull request and sent no mail.

## The NO GO, in one line
**MAJOR F1: R6 can be blinded by a plain YAML comment.** A comment that ends in `: |` or `: >` opens a block scalar that does not exist. R6 then judges every more-indented line below it as block text, for BASH_ENV only. R6's own stated property ("outside a block scalar, no line holds a quoted mapping key, an explicit key, a backslash or a `{` ...") covers these shapes. Measured through the whole program (`evidence/p1full.log`):
```
control: quoted job-level permissions key, no comment: (1, ['RULES: R6 .github/workflows/ci.yml:16'])
plain job-level permissions key (R3 control): (1, ['RULES: R3 .github/workflows/ci.yml:16'])
the same under a comment line ending ': |': (0, ['RULES: clean (1 files)'])
the same under a trailing comment ending ': >': (0, ['RULES: clean (1 files)'])
```
So a job-level `"permissions": write-all` gets past both R3 and R6 when a line `# the jobs: |` sits under `jobs:`. The YAML is valid and GitHub honours a quoted key. Cause: `build/repo_rules.py:91`. `R6_BLOCK_START` is matched against the raw line, and the alternative `:\s+[|>]...(?:#.*)?$` matches inside a comment. `check_spellings` (`:211` to `:239`) then sets `block_key` from that line. What lessens it, without clearing it: `ci.yml` is held by the whole-file fingerprint, so a reader still sees the edit. But R6 exists because a reader should not have to spot these spellings, and the commission grades "a guard that lets through a shape its own stated property covers" as a NO GO.
**The fix-round default I propose:** test for a block start only on the line with its YAML comment removed (a `#` at the start of the line or after white space, outside quotes). Add an R6 cell for `# x: |` on a line of its own and for `key: v # x: >`, each with a quoted key below it that must fire. Add a mutant that skips the comment removal.

## What I re-ran (all at head 782b3795 in my own clone, draft mode, push URL `invalid://no-push`)
- Suite: `Ran 84 tests`, `OK` (`evidence/suite-head.log`). `repo_rules.py` without `--source-documents`: `RULES-NOTE: R5 hash half NOT RUN`, `RULES: clean (412 files)`, rc 0. `git ls-files` 412.
- `prove.py` (kit tools, sha256 21 of 21 equal to THE TOOLS) against BASE 5bb1418c: `PROVE: PASS (49 rows)`, 34 `killed`, 0 SURVIVED or DIFFERENT (`evidence/prove.log`).
- `scan_faults.py`: all 6 rows `as wanted`, porcelain EQUAL, `SCAN-FAULTS: PASS`, listing 1004 (`evidence/scan_faults.log`).
- Hosted run 44902762994 of 782b3795 by GET (`hosted2.py ... --total 1335 --rules 412 --skipped-linux 4 --skipped-windows 19 --unit 84 --floor 84 --hardened-scan`): `HOSTED 782b3795737cd34e527eee1a07b90d12f2cbb801: PASS`. Control: the same with `--unit 60 --floor 60` gives `FAIL 2` on exactly the two `rules` rows. The runner's shell is `/usr/bin/bash --noprofile --norc -e -o pipefail {0}` (the job log), so the step's pipelines fail the step.
- Local CodeQL 2.27.4 (`codeql_py.py`): control `28d2852d` `6 results (code-scanning 3, security-extended 3)`, rc 1. Head `0 results (code-scanning 0, security-extended 0)`, rc 0, 7 of 7 Python files and 1 of 1 Actions files.
- Squash scan with the real gitleaks: clean LF and clean CRLF messages `SQUASH-SCAN: clean`; the planted value in the body (LF), in the body (CRLF) and in the subject: `FINDING in the message`, rc 1; a non-UTF-8 byte: rc 2 `cannot read an input` (`evidence/s3probe.log`).

## Rule on 1: scope by property
`compare 5bb1418c...782b3795`: ahead 5, behind 0, 9 files, 7 M and 2 A, numstat equal to FACT 5. Nothing under `src/`, `tests/`, `packaging/`, `contracts/` or `build/denylist/`, and no solution, package or lock file. Per commit: C1 `README.md` 2/2 (lines 72 and 73 only); C2 ci.yml (FLOOR 60->71), README, repo_rules.py, test_pipeline_controls.py, test_repo_rules.py; C3 ci.yml (FLOOR 71->76), README, the two new files; C4 ci.yml (the secret-scan step), README, test_pipeline_controls.py; C5 ci.yml (FLOOR 76->84), README, release_guard.py, test_release_guard.py. Every commit matches THE OWNED PATHS table. **HOLDS.**

## Rule on 2: each commit against its ticket and the D-decisions
- C1 (OXPD2-20): the two phrases and nothing else in C1. HOLDS.
- C2 (OXPD2-23): D2 to D5 are built as written, but **F1 (MAJOR)** above applies. Also F2 and F3 below. D3 `R7_LISTED = ()`. D4 any `filter` word. D5 `REVIEWED_WORKFLOW`, both job fingerprints kept, the one-workflow case.
- C3 (OXPD2-21): D10 is built (control first, at least 2 findings, `--cleanup=verbatim`, no global or system configuration, `--no-verify`, scratch outside the checkout). It is cut from the workflow by program.
- C4 (OXPD2-22): D6 (55 / 43008 / tree rule, `NEUTRAL-EXPORT`), D7 (`NEUTRAL-SCAN-REACH`), the listing counted by lines read. D8 and D9 are not built. HOLDS.
- C5 (OXPD2-24): D11 and D12 are built. Release mode refuses 0 fingerprints and any deny-list but the tracked file. Default mode on today's publish folders is unchanged on the hosted legs (`GUARD: clean (10 files)` / `(11 files)`). HOLDS, with the limits in F5.
- No text says the product owner decided anything about these guards (commit messages, docstrings and README read in full; a grep for `product owner|decided|ruled|approved` over the four product files gives 0).

## THE REQUIRED SECTION, H1 to H14, with my own inputs (`evidence/r6probe.log`, `evidence/s3probe.log`, `evidence/p1full.log`)
| # | My input | Result |
|---|---|---|
| H1 | `- "name": checkout` after a dash; `|+2`; `Bash_Env` inside a block | each fires (lines 17, 20, 21) |
| H1 | `'runs''on': x` (single-quoted key with a doubled quote) | QUIET: **F3 (Minor)**. The regex `(?:(?!\1).)*\1` stops at the doubled quote. The key cannot name a GitHub key (it holds a `'`), so it cannot hide a meaningful key |
| H1 | `env: [X: one]`, `x: ["k": v]` (flow pairs inside a flow sequence, no brace) | QUIET: **F2 (Minor)**. The ticket says "refuse ... any flow mapping". R6's stated property and D2 test only `{`. A YAML flow pair is a single-pair flow mapping, so `steps: [run: x]` makes a valid step with no brace |
| H2 | a comment ending `: |` or `: >`, on its own line or after a value | **F1 MAJOR** (above) |
| H3 | `run: | # it's` (block with a comment) | quiet, correct |
| H4 | `!!str runs-on:` | quiet: the named limit holds as stated |
| H5 | R7: a symlink whose target holds a NUL; a NUL as the last byte | fires (the rule reads the work tree and follows the link); my mutants m2 and m17 are killed |
| H6 | R8: CRLF line, tab separator, quoted pattern `"a b.bin" filter=lfs`, `x/.GitAttributes` | each fires; `*.bin binary` quiet; mutant m1 killed |
| H7 | gap rows | 7 of 7 as wanted in my `prove.py` run |
| H8 | six step faults | 6 of 6 as wanted in my `scan_faults.py` run |
| H9 | git notes | named limit, unchanged in README S1 |
| H10 | planted value in the subject, in the body, in a CRLF body | each `FINDING in the message`, rc 1 |
| H11 | `TMPDIR` inside the checkout | not run (named limit, as the kit says) |
| H12 | UTF-16LE PEM with no BOM | fires |
| H12 | UTF-16LE PEM at an odd offset inside a binary; the library name in UTF-16BE inside a binary; a v7 tar (no `ustar` at 257) | each `GUARD: clean`: **F5 (Minor, name as limits)**. The docstring says "ASCII or UTF-16LE" and tar "by ustar at 257", but README G1 says "the name inside any file that holds a NUL byte" without the LE qualifier, and README G3 says "tar" without the magic |
| H13 | brotli, single-file bundle | not built; named limit / UNMEASURED, as the kit says |
| H14 | the new awk on Ubuntu | the hosted run printed both `NEUTRAL-EXPORT ... wrong 0` lines and `NEUTRAL-SCAN-REACH ... 0`, and `rules` `Ran 84`. Which awk the runner uses was not printed |
| S3 (i) | a gitlink plus a symlinked `.gitattributes` | the gitlink's empty folder is `RULES: R0 sub:0` (refused, loud). For the symlinked `.gitattributes`, R8 reads the link's target; git itself does not honour a symlinked `.gitattributes` (it warned "unable to access"). A limit, not a hole |
| S3 (ii) | ZIP nested 4 deep; a ZIP holding the library inside a tar | `G3 a.zip!b.zip!c.zip!d.zip`; `G1 a.tar` and `G3 a.tar`. Fails closed |
| S3 (iii) | CRLF subject and body; a non-UTF-8 byte | CRLF: scanned with the CR bytes kept, clean when clean, a finding when planted; non-UTF-8: rc 2. Fails closed |

## Rule on 3: my mutants on product code (each in its own export of the head; a pristine export after them: `Ran 84`, OK)
22 mutants (`evidence/mutants.log`, `evidence/mutants2.log`). **10 killed by assertion** (FAIL, 0 ERROR):
m1 R8 first attribute skipped; m2 R7 last byte unread; m9 cab magic dropped; m10 PEM-embedded DER not searched; m14 the step's 43008 check removed (killed by the three fingerprint cells); m15 base name case kept; m16 unopened formats in release mode only; m17 one NUL allowed; m20 tar magic at 256; m21 the UTF-16LE library name unseen.
**12 survived. The suite is green on each:**
- R6, a hiding hole if mutated: **m3** (`>` becomes `>=`: an "empty" block takes the next sibling key as its first line); **m18** (a quoted key after `- ` missed); **m22** (greedy `${{ .* }}` hides a `{` between two expressions). D2 names each of these behaviours, and none has a cell. **F4 (Minor, test gap)**.
- R6, fails closed (stricter, so a false red is the worst case): m4 (`- |` not a block start), m5 (`>` blocks not seen).
- Guard: **m6** (JCEKS magic dropped: D12 names Java key stores; only JKS has a cell); **m7** (UTF-16 PEM only with a BOM); **m8** (release mode takes any file named `dev_ca_sha256.txt`: the cell's other list has another name). F4.
- Squash: m11 (message judged by exit code only) and m12 (the copy count): equivalent in practice, because `neutral_export` fails the run itself on a wrong count. **m13** (leading blank lines of the body stripped) and **m19** (multi-line subject allowed): untested input handling. F4.

## Rule on 4: suite, rules, hosted, CodeQL
`Ran 84`, `OK`; `RULES: clean (412 files)`; `HOSTED 782b3795...: PASS` (1335 / 1335, skipped 4 / 19, unit 84, floor 84, hardened scan: listing 996, wrong 0, reach 996 / 0); CodeQL head 0+0, control 3+3. **HOLDS.**

## Rule on 5: the merge, and the lanes behind it (`evidence/merges.log`)
- `git merge-tree --write-tree 5bb1418c 782b3795`: rc 0, tree `1638e9c22e64515fb4a9610a74fbb84a4628301f`, which equals the head's tree. **HOLDS.**
- Lane E 610bb7d2 and lane G 8efae983 both branch at 8ae5e08c (before this lane and before PR 12). Each merges clean with this head. Neither touches this lane's paths or any `.gitattributes`, and neither adds a NUL-byte file. The merged `ci.yml` equals this head's, so the whole-file fingerprint holds. `repo_rules.py` on the merged tree is clean, and `build/tests` gives `Ran 84`, OK. The full table is in FOR-RECORDS.md. **It is valid for THIS head only**: a fix round adds cells and moves `FLOOR` and `Ran` past 84.

## Rule on 6: the seat's deviations
1. **CONFIRMED.** I rebuilt the red stage myself: the C2 tree with C1's `repo_rules.py`. It gives `Ran 71`, `FAILED (failures=16)`, 0 `ERROR:`. The distinct FAIL names are exactly the kit's eight: 3+3+1+1+3+1+1+3 subTests (`evidence/red-c2.log`). The C5 red, rebuilt the same way, gives `FAILED (failures=8)`, exactly the eight names, 0 ERROR (`evidence/red-c5.log`). The kit's `failures=8` at C2 was a count of names. The seat's reading is right.
2. **CONFIRMED.** By GET, `matching-refs/heads/b1861` holds one row at 782b3795, and pull requests whose head starts `b1861` number 0. In the seat's clone, the reflog of `refs/remotes/origin/b1861/...` holds ONE entry, `update by push`, `0000000 -> 782b3795`. The quarantined second clone (read only) has porcelain 0, a HEAD reflog with one `clone` entry, `refs/heads/main` at 5bb1418, and no b1861 ref of any kind. A push from it would have left a remote-tracking ref. No push came from it.
3. **ACCEPTED.** S2 voids FACT 6. The FACT 5 sha256 and numstat match, and I confirmed the numstat by my own diff.
4. **CONFIRMED.** The head equals the drafter's code: `prove.py` re-applies the kit's diffs to BASE, and my scope diff equals FACT 5's numstat. There is no fix commit.

## Findings
| # | Severity | Finding | Where |
|---|---|---|---|
| F1 | **MAJOR** | A YAML comment ending `: |` / `: >` opens a phantom block, so R6 skips every more-indented line: quoted keys, flow mappings, backslashes, `? ` and `|2` all pass, and a quoted job-level `"permissions": write-all` passes R3 and R6 together | `build/repo_rules.py:91`, `:234`-`:238` |
| F2 | Minor | A flow pair inside a flow sequence (`[k: v]`, `["k": v]`) is a flow mapping by YAML with no `{`. The ticket says "any flow mapping"; R6 and D2 test `{` only. Fix: refuse a value or entry that opens with `[` (`: [` / `- [`). This is not a bare `[`: today's `ci.yml:7` holds `'b[0-9]*/**'`. Otherwise name it as a limit | `repo_rules.py` R6 |
| F3 | Minor | `'a''b':` (a doubled quote) is not seen as a quoted key. It cannot name a GitHub key | `repo_rules.py:92` |
| F4 | Minor (test gaps) | 12 surviving reader mutants, 8 of them behaviour that D2, D10 or D12 names: m3, m18, m22 (R6), m6, m7, m8 (guard), m13, m19 (squash) | test files |
| F5 | Minor (text/limits) | The guard misses a UTF-16 PEM at an odd offset inside a binary, the library name in UTF-16BE, and a v7 tar. The docstring is exact, but README G1 and G3 claim more than the code does | `README.md:66`, `:68` |
| F6 | records (reader incident, mine) | While making my clone I ran `git switch --detach 782b3795` in a clone I did not own, `scratchpad/clone` (it holds `GateB1878Probes.cs`, so it is probably reader B1878's). The pre-existing clone was in the session scratchpad. Its HEAD stood at 782b3795 for about one minute near 23:20 AEDT before I switched it back to `b1849/wp12-oxpd2-adapter` (610bb7d2). Its untracked probe file and ignored bin/obj were untouched. **Tuesday: tell B1878 in case a run of theirs fell in that minute.** | session scratchpad |

## What I did NOT test
Anything on Windows, and `mawk` locally (none on this machine). The `TMPDIR`-inside-checkout refusal of `squash_scan.py`. A real .NET single-file bundle, and brotli. The release guard over a real local publish folder: I relied on the hosted legs' `GUARD: clean (10/11 files)`. CodeQL on the pull request (none exists). A YAML parser's view of my R6 probes (none on this machine): their validity is DERIVED from the YAML spec, and GitHub's acceptance is not measured. Lane E's and lane G's dotnet totals (not this lane's). B1880's adversarial depth on the second scan's export and on the fingerprint (I re-ran the kit's rows only).

On a NO GO I write no landing texts. FOR-RECORDS.md holds the later-lanes table for this head and the records items.
