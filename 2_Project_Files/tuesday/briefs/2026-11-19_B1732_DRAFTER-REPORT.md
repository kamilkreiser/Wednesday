STARTABLE: YES - after Tuesday stamps the 8 slots; stamp_check.py exits 0 (73 claims, 73 measured); one lane, one path, one sentence of one line; words frozen from printed code lines; predicted blob measured on a scratch copy.

# B1732 DRAFTER REPORT (kit: 2026-11-19_B1732_SEAT-M162_mps-lane-mf-importer-doc.md)
Drafted 2026-11-19 about 11:17 to 11:25 AEDT (clock reads by `date`: 11:18:09, 11:19:16, 11:23:34, 11:24:11).

## BLUF
MPSCALC-415 at MPS main b65a7f3b716bb79a1ddd229caaba1bbc1c9aa475 (squash of #216; 0 open PRs). One sentence of `docs/IMPORTER.md:17` (``so `prove` counts them and compares the governed options only.``) is replaced by a frozen sentence read word by word against `ParityProof.cs`. Base blob e37fac255f92a9fee34798b9fa7de1b0eb477ad3 (= the ticket's e37fac25); predicted head blob 4dd6130fde2ef7e4e0cc6dddd74ad662a1a7b1bb; diff shape measured by `git diff --stat` on a scratch repo: 1 file, 1 insertion, 1 deletion (numstat `1 1`), `diff --check` rc 0, line 17 1718 -> 1865 characters, file 146 lines both sides, non-ASCII bytes 86 -> 86. Ruled by Tuesday: developer doc under C-109 (b), gate G2, Sonnet. No dotnet in this lane (no program reads the document; census in FACT 5).

## Kit
`/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-19_B1732_SEAT-M162_mps-lane-mf-importer-doc.md` (110 lines, 34138 bytes at the stamp_check run; one later one-clause edit of the drafting-clock sentence), sidecar `.measured` 73 lines.

## Facts re-measured (instrument -> result)
- main: `gh api -X GET .../git/ref/heads/main` under the MPS GH_CONFIG_DIR (gh auth status: github.com account kamilDatasec; the kit's refuse rule tests for "the Datasec account") -> b65a7f3b...; `pulls` -> 0; `matching-refs/heads/b1732` -> 0 (control `heads/b1706` -> 1); main's subject is the #216 squash.
- MPSCALC-415 whole by my own GET-only Jira helper (scratch, in-process credentials, never printed): Backlog, label records-pass-1119, updated 2026-11-19T00:22 (+1100), 0 comments; control MPSCALC-361 reads Done.
- `docs/IMPORTER.md` at main: 146 lines, 0 CR, 86 non-ASCII bytes (python), blob e37fac25; the old phrase is on exactly 1 line of docs, src, tests, .github (control `any mapped model sheet` on the same line, 1).
- ParityProof.cs (509 lines): every cited line printed by awk (:89-94, :112-115, :148-149, :175-203, :270-328); IMPORTER.md:86-95 printed; PriceBookImporter.cs:150 already carries the #215 sentence.
- Edit applied by python to a copy in a scratch git repo (`fleet/state/s292/d1732/gs`): other lines equal, prefix and suffix of line 17 equal, new sentence ASCII (248 bytes), `any mapped model sheet` still 1, `does not re-read the book` 1 -> 2 lines, old phrase 1 -> 0, name-only grep -c -v -x -> 0 (control 1).
- Census of readers: `IMPORTER.md` is named on 12 lines of 9 files; none reads the real file's words (OutputGuardTests uses a synthetic one; `test_demo_doc.py` reads DEMO.md).
- Model: `models_latest.json:23` claude-sonnet-5-5; row L1 `model-routing.md:80`; G2 `:109`; `brief_seat.sh:31` defaults to opus (launch line carries the level).

## Corrections to the commission's facts
1. The sentence is NOT "the last sentence of the cell" (ticket and sweep both say so): one more sentence follows it (` On Q4_26 v1a: 80 rows, 50 SKUs, 4 sheets; ...`). The kit replaces only the sentence the ticket names by its words and leaves the trailing one.
2. The old words `compares the governed options only` are themselves narrower than the code: `CompareRecords` (`ParityProof.cs:270-328`) compares devices, supplies and software too. The frozen sentence therefore drops that clause rather than restating it (Q3). The ticket's own recommendation does not ask for it.
3. The sweep and ticket cite main b65a7f3b; that is still main now (not 51ed36eb of the B1721 lane).
4. DRAFTER_RULES.md names `/Volumes/Laptop-DEV/...` paths (rules 9, 75, 68); this machine is `/Volumes/Datasec_DEV/...`, and the kit uses the latter.
5. The commission calls the project's own helpers "read helpers"; none was needed (own GET-only helper in scratch).

## D-decisions (mine)
- D1: no dotnet build or test in the seat's work; marked NOT RUN with the reason (census), left to hosted CI. B1721's heavy-lock block is dropped for the same reason.
- D2: the frozen sentence keeps the old words `They are not in the approved workbook, so `prove`` and does not use "governed" at all.
- D3: READY target Step 0 + 20 minutes (docs-only, no build).
- D4: Edit-tool-only, with a bytes-level program proof (4(a), 4(e)) because the file holds 86 non-ASCII bytes.
- D5: the hand-built line-17 text contains the words "any mapped model sheet" (MPSCALC-207's cite); the kit makes it a check.

## Inputs table (rule 4: each input is produced by an earlier step or exists at BASE)
Step 1 clone and base: exist at origin. Step 2 predictions: from this kit. Step 3: files at base. Step 4: Step 3's counts, the edited file. Step 5: Step 4's head sha. No step needs a file a later step makes.

## Q-questions for Tuesday (each with a default)
- Q1 words as frozen. Q2 only the named sentence replaced, the trailing sentence untouched. Q3 "governed options only" clause dropped (alternative: keep it and have the G2 gate read it against :270-328). Q4 L1 on Sonnet, gate G2. Q5 no dotnet.

## Slots Tuesday must stamp (recommended values)
- S0 COMMISSION: Tuesday's 2026-11-19 sweep (SWEEP-1115 lane M-F) and ruling item 1 (developer doc, C-109 (b), built as written, G2); the product owner has said nothing on MPSCALC-415 (0 comments as the drafter read it; the seat re-reads).
- S1 STAMP: `STAMPED <time> AEDT 2026-11-19 by Tuesday (s292)`, plus only what Tuesday actually read and re-printed (suggested re-prints: blob e37fac25 of docs/IMPORTER.md at main, the head blob 4dd6130f from a scratch copy, ParityProof.cs :89-94, :112-115, :175-203, :270-328 against FACT 4, C-109 at CLARIFICATIONS.md:2716/:2720, the `.measured` spot checks, stamp_check rc 0).
- S2 BASE: b65a7f3b716bb79a1ddd229caaba1bbc1c9aa475 (re-read at the stamp; it is main now).
- S3 STATE: open PRs 0; main b65a7f3b; `^b1732` branches 0; mps panes 0 (re-read live); no `.tools/.heavy-lock*` needed.
- S4 Q-ANSWERS: the defaults (Q1 as frozen, Q2 named sentence replaced, Q3 clause dropped, Q4 L1 Sonnet G2, Q5 no dotnet).
- S5 LAUNCH WINDOW: to the hard stop; load1 at the stamp (it read 6.45 at 11:19); live seats beside you (NexusAI N-S lane in another project: shares nothing); one waiter.
- S6 HARD STOP: an absolute latest start (suggest the same night cut as B1721, 02:00 Friday 2026-11-20, weekday by `date -j`); READY target = Step 0 + 20 minutes.
- Last line: `READ-WHOLE-BY-TUESDAY: DONE by Tuesday (s292) <time>: ...` only after Tuesday reads the kit whole.

## UNMEASURED
No build or test run (none needed). gitleaks exists at /opt/homebrew/bin/gitleaks but was not run (canary and range runs are the seat's). Hosted CI and CodeQL not run. The ban-list scan is by reference to GATE-VERIFIER-STANDARD step 7 (list read there: Kam, Kamil, Kreiser, Steve, Peter, Paul, Blanchard, Inch, Waite). I did not read each of the eight sibling kits that name `docs/IMPORTER.md` for what it grants (word-boundary counts only; open PRs 0 and no pane live).

## Outside-the-fences disclosure
Read-only: Jira GETs (MPSCALC-415 and -361) with the project's `.env` in-process, never printed; `gh api -X GET` (ref, pulls, matching-refs, commit subject, tarball, search/issues, commits?path=, pulls?state=all) under the project GH_CONFIG_DIR; one `gh auth status` (prints a masked token line); tarball of main unpacked in my scratch; `ls -d` and `tmux list-panes`; `command -v gitleaks`; `df -g`; `date`. I read the MPS project's CLARIFICATIONS.md by line numbers 2716 and 2720 and CLAUDE.md lines 50-52, and `git config --local --get user.email` as a count only. I created a scratch git repo with a scratch identity under `fleet/state/s292/d1732/gs` (not a Datasec repo). Two Bash calls were refused by hooks (a `=====` separator word, and `git -C $VAR init` for a path held in a variable); both were re-issued with literal paths. I read no card, no briefs_staged, no scoreboard, no ledger. I read the `.pre-stamp`-free B1721 kit, its sidecar and report, B1706's `IMPORTER.md` lines by grep, and the first 12 lines of the B1730 commission for form only. Writes: the kit, its `.measured` sidecar, this report, and scratch under `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s292/d1732/` (including `.measured.todo-old`, a superseded skeleton moved aside).
