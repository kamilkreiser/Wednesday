STARTABLE: YES (after the stamp; Q1 is STOP-class and needs Tuesday's answer in words at S4; Q4 recommends launching after kit B1912's lane lands)

# B1916 DRAFTER REPORT | lane C (seat Datasec/OXPd2-X30): rule R6's two quoted-value shapes and the Dockerfile digest pin

Kit: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-22_B1916_SEAT-X30_oxpd2-c-r6-shapes-and-digest-pin.md` (62278 bytes, sha256 `16452c071b92855be4a84f3f8119dec65726f59b838e509c39aa626daaf922d0` at writing; 8 unfilled slots, the last line `READ-WHOLE-BY-TUESDAY: ____`). Sidecar `.measured` beside it: 183 claims, 183 measured, `stamp_check.py <kit>` rc 0. Scratch and every program behind a number: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s310/d1916/` (`gate/` = the seat's `<src>`, `logs/`, `scratch/`). Drafted 20:16 to 20:40 AEDT 2026-11-22 (clocks by `date`).

## BLUF
- A three-file lane: `build/repo_rules.py` (R6 gains two refusals), `build/tests/test_repo_rules.py` (seven rows in two EXISTING planted controls), `packaging/linux/Dockerfile` (FROM by digest). All frozen as three patches applied byte for byte; prototyped red then green in the drafter's clones at `bf6b441e`.
- **The commission's default (sketch (i)) was NOT taken: the prototype shows it fails one of the ticket's cells.** With (i)+(ii) the suite printed `FAILED (failures=1)`: the flow mapping hidden inside an expression in a key (`env${{: {x: {permissions: write-all}}`), which the ticket lists among its cells, stays unrefused. Sketch (iii) (an expression marker before the line's first colon and blank is a finding) closes shape 1 AND that cell; with (iii) in place (i) adds nothing (DERIVED). Default: (iii)+(ii). This is Q1, STOP-class.
- **No new test case, so `ci.yml` is untouched.** `test_pipeline_controls.py:95` requires FLOOR to EQUAL the count of indented `def test_` lines; any new case would force `FLOOR=112` in `ci.yml`, which the commission forbids. The seven rows go into existing tables: `Ran 111 tests` before and after; the ticket's "count of tests equals the floor" holds as 111 = 111.
- Digest `sha256:12b1135f5f8b3c0a214f2a680ff2033dff4f684f445d6c697d9524ceeb303586`, read by GET from three hosted linux logs (2026-11-20 and two of 2026-11-22, the newest 09:12Z), identical in all three; no registry call, no docker.

## FACTS RE-MEASURED (instrument, control)
- Origin (gh api -X GET, 20:16:10): main `bf6b441e30900127487145c3b65b29d8cc9eb5ea`, 0 open PRs, 19 branches incl. `b1912/f13-test-race`, no `b1916`; `.private` true, `.permissions.push` true. Blob ids of the three owned files on origin main equal the drafter's clone (contents API vs rev-parse).
- Ticket OXPD2-25 read by key (GET `/rest/api/3/issue/OXPD2-25`, no JQL, credentials in-process, 20:16:46): Backlog, 0 comments; acceptance and sketches quoted in the kit as RELAYED.
- BASE suite (through heavy.py): `Ran 111 tests`, `OK`; `repo_rules.py` `RULES: clean (500 files)`.
- RED (patch 1 alone): `Ran 111 tests`, `FAILED (failures=5)`, `^ERROR:` 0 (control `^FAIL:` 5), `AssertionError: 0 != 1` 5.
- GREEN (patches 1+2): `Ran 111 tests`, `OK`; `RULES: clean (500 files)` on the real workflow; 111 lines ` ... ok` with `-v`.
- Mutants, each killed: drop (ii) failures=2; drop (iii) failures=3; (ii) on the raw line failures=1 (kills via a new quiet row); (iii) without the colon failures=4. Alternative sketch (i)+(ii): failures=1 (the brace).
- libyaml 0.2.1 (`/usr/bin/ruby -ryaml`) reads every red shape prototype as VALID with the hidden quoted keys as real keys (so the cells are real holes, not only line-reader artefacts). GitHub's parser: UNMEASURED.
- Patches applied to a second fresh clone from BASE: apply rc 0 x3, cmp rc 0 x3, second apply-check of the fix rc 1 (control).
- numstat 25/6, 7/1, 2/1; ASCII-only (0 lines outside `[ -~]`); `words.py` `WORDS: clean (2 files)` with `CONTROL FIRED: 13 of 13`; gitleaks 8.30.1 `no leaks found` over the seven files under neutral names, planted control rc 1 (moved to `_quarantine/`).

## D-DECISIONS (all Tuesday's defaults as coordinator, each a Q in the kit)
D1 (iii)+(ii), not (i) | D2 accept (ii)'s cost | D3 rows into existing controls, no new case | D4 digest from hosted logs with one comment line | D5 one commit, red state local only.

## Q-QUESTIONS FOR TUESDAY (each with its default)
- **Q1 STOP-class:** (iii)+(ii) [default] vs the commission's (i)+(ii) with the brace a named limit, or all three with (i) a survivor.
- **Q2:** accept the named over-refusals [default]: outside a block scalar R6 now refuses `run: echo "hello"`, `if: github.event_name == 'push'`, `name: a 'b'` (sketch (ii)), and a quoted value holding an expression then a colon, `- "a ${{ x }}: b"` (sketch (iii) on the raw line). Measured `[1]` green / `[]` BASE each; today's ci.yml holds none. A later ci.yml edit has to write such values inside `${{ }}` or a block.
- **Q3:** pin by digest [default]. Cost: base-image patches stop flowing until this line moves.
- **Q4:** launch after B1912 lands [default]. While main holds the F13 race the linux leg can go red, and a red test step SKIPS the `container image` step, so the pin would go unproved; the kit makes a red F13 a STOP, never a re-run.
- Q5: root `README.md:29` (names the tag) unchanged [default]: still true; README is "no lane" tonight.
- Q6: Opus by project CLAUDE.md:7 [default]. Q7: READY +90, push +60, pane X30, gate G1 Opus.

## CHAIN INPUTS
Printed in the kit's CHAIN INPUTS table: every step's input exists at BASE (the three files, the origin, the tools folder) or comes from an earlier step. Step 5's digest compare uses Step 1's `hosted-base` log, or a named GET when BASE's linux leg was red.

## UNMEASURED
GitHub's YAML parser on the shapes; how the hosted builder words a digest-pinned `FROM` in its log (Step 7(e) PREDICTED, worded as "never treat a wording difference as a finding"); whether the digest is the multi-platform index or one manifest (it is the reference the builder printed); the run_step neutral scan on a commit of this lane (NEVER RUN, marked); the hosted run of any head of this lane (NEVER RUN, marked); a valid-YAML hiding form of shape 2 after a sequence dash (two prototypes refused by libyaml, one left the key visible; said so in H3).

## OUTSIDE-THE-FENCES DISCLOSURE
- Read-only toward the project: no write in `<project>` (`.tools/` holds no `b1916` and no lock folder, measured 20:39:45); every git write verb ran only in my own clones under `fleet/state/s310/d1916/` (clone from kit B1912's local clone, push URL `invalid://no-push`). Three hook refusals of mine (twice a `$S/clone` variable on a git write verb, read by the hook as outside the tree; once a zsh `======` separator), each re-run with literal paths; nothing ran outside the fences.
- GitHub: `gh api -X GET` only, under the project GH_CONFIG_DIR (repo, refs, branches, pulls, contents, runs, jobs, three job logs). Jira: two GETs by issue key (OXPD2-25, OXPD2-8); no JQL, so the parentheses rule had nothing to apply to; no token printed. No HTTP to any other host, no registry, no docker, no az, no ssh.
- Heavy lock: 10 unit-test jobs through the round's unchanged `heavy.py` (lock waits 0 to 17 while other holders had it; I never broke a lock). No dotnet job. Load1 ran 5.04 to 6.92 while I worked.
- Read sweep B1913 scratch file names only (its `jira/` listing) and its kit text; I did not read `fleet/briefs_staged/`, the scoreboard, `_ledger.md`, any WEDNESDAY/FRIDAY tree, `Source_Documents/`, a key folder, or another drafter's (B1914/B1915/B1917) files. No `decision_queue.sh` call. No port block (none assigned; the kit starts no listener).
- One unneeded background grep over `tuesday/briefs/` (looking for the word libyaml in older kits) was started and stopped by me before it printed anything.
- No name of a person or a card id in the kit's commit message or added lines (`words.py` clean); the kit cites rulings by C-number and date.
