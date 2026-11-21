STARTABLE: NO - both MPSCALC-422 and MPSCALC-423 claims are no longer true at code main 28d8d31b (pull request 222 already delivered the attribute read, the whole-dollar tokens, the exact-leaf no-new-word check and the committed priced capture compare); the kit is a held, stopped kit that ends in Questions.

# B1875 drafter report (lane M-2, seat M171), 2026-11-21, drafter for Tuesday (Sonnet), 23:08 to about 23:20 AEDT

## BLUF
- Main read by `gh api -X GET` at 23:08:55 and again at 23:14:14: `28d8d31b73c6475b33921c679499b0777fdf0448`; open pull requests 0; `matching-refs/heads/b1875` 0 rows.
- The read owed first (commission, M-2): each ticket's claim against `web/src/proposal/unpriced.test.tsx` at main (blob `eb3f7e7bdbea2127253c5f0542b0583616698bc5`, 1135 lines). Verdicts, with the lines, are in the kit's section THE READ OWED:
  - 422 "never reads an attribute value": NO LONGER TRUE (`scanText` `:112`-`:126`, attribute line `:115`; control cells `:400`-`:410`).
  - 422 "never looks for an integer part alone": NO LONGER TRUE for 3-digit-and-up whole figures (`wholeDollarForms` `:128`-`:135`, the rule written at `:129` and `:132`; cells `:412`-`:429`); what stays unread (rounded or abbreviated figures, 1 or 2 digit integer parts) is a limit the file states at `:5`-`:6`: PARTLY, as a stated limit, not the ticket's claim.
  - 422 optional tidy: PARTLY TRUE, the one residue (three `console.log` lines at `:284`, `:756`, `:941`; cell titles still lead with build labels).
  - 423 "admits any part of a priced text": NO LONGER TRUE (`unexplainedLeaves` `:240`-`:244`, U10 `:366`-`:373`, one named exception that must be the last sentence of a priced leaf; cells `:584`-`:611`).
  - 423 "no committed check sees a priced markup change beyond the column heads": NO LONGER TRUE (`pricedUnchanged.test.tsx`, 77 lines, 8 captures compared byte for byte; the priced short-form `<col>` widths are in the capture; its rule for regenerating is written at its lines 5 and 6).
- Per the commission, a claim no longer true STOPS the kit for that ticket with a Question. The kit therefore freezes no build. Its first action for any seat launched on it by mistake is a STATUS ending `STOPPED: NEEDS TUESDAY ...`.
- What changed between the tickets and main: both were written at `565ba142` (blob `1e4e81af`, 29 tests); #222 (`debb5e28`, merged 2026-11-20T04:55:54Z per the pull request, RELAYED from `gh api -X GET .../pulls/222`) rewrote the file and added `pricedUnchanged.test.tsx`. Its own body says so (lines 25 and 38). Main `28d8d31b` differs from `debb5e28` by 5 files, none under `web/src/proposal` (`gh api -X GET .../compare/...`).

## Files
- Kit: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-21_B1875_SEAT-M171_mps-unpriced-test-followups.md` (21838 bytes).
- Sidecar: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-21_B1875_SEAT-M171_mps-unpriced-test-followups.md.measured` (65 lines, 14152 bytes; `stamp_check.py <kit>` exits 0; 65 claims, 65 measured). Three sidecar lines (two ` and ` fragments and one `), no ` fragment) measure artifacts of backtick pairing in the kit text, and the sidecar says so on those lines; they assert no output.
- Scratch (all under `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s307/d1875/`): `main.tgz` and `src/` (tarball of main, read only, nothing run from inside), `jira_get.py` (GET-only, credentials by name in-process, never printed), `tickets.txt`, `t426.txt`, `pr222.txt`, `claims.txt`, `measure.py`, `kit.measured.first-init` (the first sidecar skeleton, moved aside with `mv`, not deleted).

## Facts re-measured with instruments
| Fact | Instrument | Result |
|---|---|---|
| main sha | `gh api -X GET .../git/ref/heads/main --jq .object.sha` under the project `GH_CONFIG_DIR` | `28d8d31b73c6475b33921c679499b0777fdf0448` (twice) |
| test file blob | `git hash-object` over the tarball copy | `eb3f7e7bdbea2127253c5f0542b0583616698bc5`, 1135 lines, 61899 bytes (equals the sweep's `eb3f7e7b`) |
| `pricedUnchanged.test.tsx` blob | same | `9f2aa36e49957a9222b2d8783b6c3fa90cd0d82e`, 77 lines (equals the sweep's `9f2aa36e`) |
| cells in `unpriced.test.tsx` | `/usr/bin/grep -c -E '^[[:space:]]+(it\|test)(\.each\(.*\))?\('` | 79; column-1 pattern 0 (control in sidecar); loop-expanded runtime = 79 + 7 + 1 + 1 = 88, DERIVED arithmetic, UNMEASURED by a run |
| commits touching the two files at main | `gh api -X GET .../commits -f path=...` | `unpriced.test.tsx`: 2 rows (#221, #222); `pricedUnchanged.test.tsx`: 1 row (#222) |
| captures | `ls -l`, `grep -o -E '<col [^>]*>'` | 8 files; `onepager-s4.html` holds 4 priced `<col>` (control `<colXX ` prints 0) |
| tickets | Jira GET at 23:09:09 | both Backlog, 0 comments, 0 links, last updated 2026-11-20 |

## Census of tests that pin the OLD behaviour
By program, frame `web/src` and `web/e2e` (`.ts`, `.tsx`): **0 in `unpriced.test.tsx`** (each old limit has its opposite cell: `:400`, `:412`, `:592`, `pricedUnchanged.test.tsx:50`). 14 test files import `OnePager` or `ProposalDocument` (listed in the kit); only `unpriced.test.tsx` (2 lines) and `pricedUnchanged.test.tsx` (5 lines) name `priced={`; `OnePager.test.tsx` has 9 lines reading `innerHTML` or `outerHTML`, `ProposalDocument.test.tsx` 1. Nothing is edited, so nothing must stay green untouched; there is no lane.

## What lies outside the frame (rule 7, three shapes; each also in the kit)
1. An amount split across elements: found when the two text nodes are adjacent (marks stripped at `:220`), not found with another node between: named limit (DERIVED).
2. A currency other than dollars, or a rounded, abbreviated, computed or in-words figure: digit forms of the contract's own leaves are found with any symbol removed; anything else is not a leaf and is not found; the file states it at `:6`: named limit; any change is a NEW behaviour, a Question (Q3, default: no).
3. A number in an `aria-*` or `title` attribute: COVERED. Not covered: an attribute name (pinned by the cell at `:408`) and a style element's body (`:114`): named limits.

## D-decisions of the drafter
- D1: applied the commission's STOP rule to both tickets, because every claim in both is contradicted by lines at main; I did not freeze the optional tidy, since with no main change it is a change of its own and a retitle is new behaviour (Q2).
- D2: wrote the kit in the held form (Stamp slots as four underscores, launch line marked HELD, `BRIEF_SEAT_LEVEL=sonnet` inside the quotes per routing row C2 at `model-routing.md:92`; model id `claude-sonnet-5-5` at `models_latest.json:23`), so a stamped kit can be launched only if Tuesday's S5 line names a lane.

## Questions for Tuesday (each with a default; all are in the kit)
- Q1: both claims no longer true: launch no lane; the next MPS records pass comments on 422 and 423 with these lines and moves them by the project's Done rule (or narrows 422 to the tidy).
- Q2: the optional tidy of 422 (three `console.log` lines, cell titles): default do not build.
- Q3: extend the oracle for its stated limits: default no.
- Q4: add a clause "re-read the ticket's claim against the file at main" to the next sweep's predicate.
- Q5: gate G2, level sonnet, only if a lane is named.

## Corrections to the commission and to the sweep's row (plainly)
- The commission's lane table and the sweep's M-2 row treat both tickets as buildable ("still true at main"). Neither is. The sweep's row printed the post-#222 blob `eb3f7e7b` and kept the pre-#222 claims.
- The sweep row says 423's committed priced-markup check would be `pricedUnchanged.test.tsx` or `OnePager.test.tsx` / `ProposalDocument.test.tsx`, "the builder picks": the first already exists and is that check (its blob is in the sweep's own list).
- The commission says the tickets were written "before pull request 222 ... changed `unpriced.test.tsx`": correct, but #222 also added the file `pricedUnchanged.test.tsx`, which the commission does not name.
- The tickets' pointers are stale (`visibleText` `:77` not `:75`; `OnePager.tsx` priced widths `:223`-`:226`, four `<col>`, not `:222`-`:224`; `OnePager.tsx` blob `9d02239f` not `dc40558b`).
- MPSCALC-426 (read at 23:10:50, text says a build kit "is being drafted") is already built by #222, as the sweep itself says: a records pass should cover 422, 423 and 426 together.
- Commission line 20 says pull requests 223 and 224 are merged; I measured main and open pull requests (0) but did not read 223 and 224 individually.

## Reading load
Kit 21838 bytes. The kit names no READ WHOLE list beyond itself (a stopped kit); so the load for a seat is 21838 bytes. If Tuesday answers Q2 yes and a successor kit is cut: add `unpriced.test.tsx` 61899 + `pricedUnchanged.test.tsx` 4476 + the project `CLAUDE.md` 8103 = 74478, for about 96316 in all; well under 300 kB.

## UNMEASURED
- Every red or green statement (a planted attribute or whole-dollar fragment turns U1/U2 red; a changed priced width turns `pricedUnchanged.test.tsx` red; a planted phrase turns U10 red) is DERIVED from reading; I ran no test, build or install. The oracle's controls at `:400`-`:429` run over synthetic elements, not over the rendered documents; nobody has run a plant on the real documents at main.
- The runtime test count of the file (88) is arithmetic over the loops, not a run.
- Whether the full proposal and short form hold any style-element CSS content that prints an amount: not read.
- Whether `RentalDocument.test.tsx` imports the documents through `OnePager` or `ProposalDocument` or through another route: the import grep matched it; its cells were not read.
- Check of the kit never run on a real seat output: the REFUSE paragraph (a seat writes a STATUS ending `STOPPED: NEEDS TUESDAY ...`) is a stated action, not a check with a pass predicate; no STOP-severity check is claimed.

## Not read, and outside-the-fences disclosure
- Not read: `Source_Documents/`, `.local/`, any price book, HPSM-POC, any other client, any card store, `0_Brain/learnings/_ledger.md`, `fleet/briefs_staged/`, `scoreboard.md`.
- Read beyond the named files: the project's `CLARIFICATIONS.md` by one `grep -n` for `MPSCALC-422`, `MPSCALC-423`, `C-188` and `C-189` (read-only, first 10 hits only; the output printed C-51 and unrelated rows, so it told me nothing about these tickets); the sweep's JOB 2 rows, STOP list and QUESTIONS; `model-routing.md` rows C1 to C10 by `grep -n`; `brief_seat.sh` line 31; `models_latest.json` line 23; `stamp_check.py` header; MPSCALC-426 by Jira GET (for the sweep's "already built (#222)" line only).
- No git write, no `cd`, no deletion (the first sidecar skeleton was moved with `mv`), no hosted call but `gh api -X GET` (main ref, tarball, commits, compare, pulls/222) and Jira GET. One in-place `sed -i` edit and one Python temp-file-then-`os.replace` edit were made to my own kit only.
- Hook advisories received (not blocks): case-sensitive grep, `cut` after grep, `$?` after a pipeline. None changed a result: I printed lines, not absences, and the one `echo rc=$?` I ran followed a pipeline whose rc I did not use; `stamp_check_rc=0` was re-run alone and printed 0.
