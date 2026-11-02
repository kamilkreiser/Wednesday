STARTABLE: YES (after Tuesday stamps the seven slots; nothing blocks it at 05:06 AEDT: no pane, listener, branch or earlier NO GO in the way)

# B1178 drafter report (routing row C8, `model-routing.md:98`), drafted Tue 3 Nov 2026 04:59 to about 05:10 AEDT

Kit: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-03_B1178_SEAT-G306_hpsmpoc-437-gate-tier2.md` (88 lines, 75 KB). Shape copied from the tier-2 gate kit B1036 (read whole) and the charter. Pane `Datasec/HPSM-POC-G306`, Sonnet, `BRIEF_SEAT_LEVEL=sonnet` inside the quotes, through `launch_when_cool.sh`, ports 9620-9629.

## BLUF
A bounded tier-2 Sonnet gate. Its weight is on proving that the one product-file hunk changes nothing (three independent instruments: emitted JavaScript, string-literal sequence, and the shipped `checkEntry` run over 2000+ entries in both trees), on the gate's OWN hashed plants for the order pin (per state, per evidence shape), and on the rename census. Slot count: 8 lines with four underscores (7 slots + last line), checked by grep; 0 non-ASCII, 0 at-sign markers, 0 person names.

## Facts re-measured (instrument; control)
- Branch ref `212fbda1...` and main `2a770988...` (`gh api -X GET git/ref`; compare `2a77098...212fbda1` ahead 1 behind 0, total_commits 1; control `matching-refs/heads/b1175` 1, `b1178` 0). Open PRs 0; PRs for the head 0 (control `pulls?state=closed` lists 278, 277).
- Files +/-: store +1 -1, test +35 -3, register +3 -3; blobs equal the raw `git hash-object` of what I read (706f4877, 0c53005e, 5aa677b9; base 19789782, db418738, 96a27122). Head tree 6cf13e7d. `ci.yml` cmp-equal head/base (679 lines). Check-runs: head 0, main 19 (control).
- `diff -w` of store base vs head empty; `diff` shows exactly line 33. Register diff = 3 lines (2, 3, 121). Test diff: header 1-2, 3 `node:` imports, title 29, new describe from head line 215 (two hunks by diff alignment).
- Anchors for plants in head `remediation-store.ts`, each `grep -c -F` = 1 (`:47`, `:48`, `:49`, `:29`, `:30`, `:46`), zero control 0.
- Round count: 145 gate lines over 586 `*_STATUS.md` first lines; filter `remediation|checkEntry|remediation-store` = B1156 only (GO WITH FINDINGS, different class); control filter `B1156` 1; zero control 0. So NO GO 0 of 2 on this class.
- Landing line: analysis repo main `4f48008c`, 5463 lines, line 3617 starts "The landing form is a head-pinned squash" (106 `head-pinned` lines; absent-string control 0).
- Ports 9620-9629: lsof 0, control listener on 9629 seen then gone; word-boundary scan of 104 non-`.pre-` SEAT kits of 11-02/11-03 found none (control 9610: 1 kit, the builder's). Older 962x kits are 10-25 (finished). Panes: tuesday, fleet-monitor, NexusAI-G303, MPS-G305, MPS-M84, Security-Composer-C82; no HPSM-POC pane.
- Model ids: `models_latest.json` line 23 `claude-sonnet-5-5`; routing rows G1 108, G2 109, G-cap 111, C2 92, C8 98; `brief_seat.sh:24` defaults to opus.
- Ticket HPSMPOC-437 read once through the project helper: Backlog, 0 comments, items and Done-when as quoted in the kit.
- Head commit author and committer email hosts both end in `localdomain` (2 of 2 fields; main 0; message 0). Not in the builder's brief to the gate, but it matters for landing: the kit makes the squash-commit check explicit.

## D-decisions (mine)
- D-1 INDEPENDENCE ORDER: the builder STATUS plant bullets (lines 41-48) and READY line (80), and the commit message (its last paragraph states every plant count), are withheld until the gate's predictions are hashed. Your brief asked for hashed independent plants; the message leak was not obvious and is the reason for the `--jq` instruction.
- D-2 Three-instrument proof for "no behaviour of remediation-store.ts changed": emitted JS equality (ts.transpileModule), literal sequence, and a scratch file that runs the shipped `checkEntry` over 2000+ entries in base and head. `git diff -w` is the fourth, as asked.
- D-3 Plants beyond the brief's list: qE (empty-evidence-only reversal) and qZ (invisible-only reversal) test whether the four-case table is needed; qU, qXm, qMf, qD cover the real-date rows and the sentence; qR is an EQUIVALENT refactor that I predict turns only the source-reading row red (a Note: that row couples the test to the source text). Cap 20 runs.
- D-4 The source-reading row (`:237`) reads `remediation-store.ts` via `import.meta.url`; the kit asks the gate to run it from `web/` and from the repo root and to classify it as test-support.
- D-5 Frame: the two files plus every other file importing `remediation-store` or rendering `RoadmapScreen`, found by `git grep` (I did not enumerate importers; the gate does).
- D-6 Consumers of old titles: whole tree, not only `web/src`, plus `-t`/`testNamePattern` selectors in package.json, ci.yml and scripts. The builder grepped `web/` only.
- D-7 Landing files only on GO / GO WITH FINDINGS; trailer `Claude Sonnet 5.5` as you specified. Counts 3881 -> 3892 (267 files, builder's claim; the gate re-measures).
- D-8 Hard stop 90/150 minutes (same as B1036), fewer plant runs but a smaller frame.

## Q-questions for Tuesday (each with a default)
- Q-1 The extra plants qE, qZ, qU, qXm, qMf, qD, qR beyond the order, evidence and sentence plants. Default: yes.
- Q-2 The C1 (e) (iii) scratch file run in `wt-b1178-base` as well as `mut`. Default: yes.
- Q-3 May the PR title and squash subject carry `HPSMPOC-437`? Default: yes (precedent from the part-B PR title).
- Q-4 Both audits (prod and dev). Default: yes.
- Q-5 Ports 9620-9629, pane G306. Default: yes.
- Q-6 Round statement "0 of 2 before, round 1 of 2 on class remediation register tests and titles". Default: yes.
- Q-7 The independence order (plant lines and commit message withheld until hash). Default: yes. If you decline, the gate is no longer independent on the plants.
- Q-8 The squash author: the head commit's author host is `localdomain`; if GitHub carries it into the squash commit, who decides (amend is forbidden to the seat)? Default: the check is in the kit (C6), Tuesday decides at landing.

## UNMEASURED
Every test outcome and count (rows, 3881/3892, 130/119) is the builder's claim until the gate runs it; the importers of `remediation-store`; any consumer of the old titles outside the three files (I did not clone or grep the tree); the branches naming the three paths since PR 277 (builder found 4 stale ones; I did not re-run the 293-branch scan); my predicted row counts for plants (hypotheses from reading the diff, not runs); hosted CI and CodeQL; whether `import.meta.url` resolves the same under the gate's cwd choices; the drafter's expectation that qR turns only the source row red.

## Outside the fences
None. Read-only: `gh api -X GET` under the project config dir (refs, compare, commits, contents, trees, check-runs, repo settings, the analysis repo's raw `CLARIFICATIONS.md`), the project's Jira helper once (output to the session scratchpad only, no token printed), local reads of the briefs, status files and charter, `lsof`, `tmux list-panes`, `uptime`. A temporary python listener on 9629 for the port control (4 s, then gone). One command of mine contained a stray `cd` inside `bash -c` (the hook did not block it; it changed nothing). Scratch files only under the session scratchpad. No clone, fetch, install, card read, mail or publish.
