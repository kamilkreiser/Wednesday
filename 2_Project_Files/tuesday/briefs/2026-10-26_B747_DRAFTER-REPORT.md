STARTABLE: YES (after Tuesday fills the 7 stamp slots and the last line; nothing in the start depends on #223 landing, on CI, or on a live seat; the one ordering fact is that the verdict covers a STACK, see D-1)

# B747 DRAFTER REPORT (kit `2026-10-26_B747_SEAT-G150_hpsmpoc-343-held-values-gate-tier1.md`, 117 lines)
Drafted Mon 26 Oct 2026 from 15:37 AEDT (clock from `date`), read-only, by the Sonnet drafter. Shape cloned from the round-1 tier-1 gate kit B729 (115 lines, read whole) and the CI-pause grading of the tier-2 kit B738 (129 lines, read whole). Builder kit B739 (138 lines, with its stamp) and its STATUS (282 lines) read whole as CLAIMS.

## BLUF
- Tier 1 (routing row G1, `model-routing.md` line 108; G-cap line 111; I read lines 105-111), Opus `claude-opus-5-5` (`models_latest.json` line 17), launch line carries `BRIEF_SEAT_LEVEL=opus`. Brief B747, seat G150, ports **9610-9619** (the in-process test hosts bind none).
- Round 1 of 2 on the builder-confirmed class "allowance for an unchanged stored value in a hidden-character refusal, and screening of AI narrative output". Frame re-measured: 407 STATUS files, 77 start `GATE VERDICT`; no verdict line names this class (B729, #223 itself, is GO WITH FINDINGS on a different class and is where the subject finding came from).
- **Stacked-head rule written into the kit:** the subject is `bcb359f8..66bf9aa8` (3 commits, 6 paths); #223 is not re-gated; #223's head moving = NOT GATED (base moved); #223 landing = not a refuse; the combined tree on current main is an informational merge prediction (no PR exists, so no merge ref to compare); the verdict does NOT cover the re-landed commits, which need their own short check, whose predicate the gate must write under FOR TUESDAY (six blobs equal, `git diff` byte-equal, CI/CodeQL read at the re-landed head). No `gh pr merge` command is stated for this branch.
- **The security heart (C2/C3):** the gate rebuilds the allowance as "exactly unchanged": all 212 scalars as STORED values (the builder pinned 3, middle only) times variants V0-V17 (one-character edits, case, whitespace, normalisation forms, CRLF, other row, other field, older disposition row, removed item, clean-when-stored, three JSON encodings), against its own oracle, with the parent as the control that must refuse every V0 (B729-1 reproduced), plus the order/equality-oracle differential.
- Under the CI pause and with no PR, GO is not reachable; best verdict `GO WITH FINDINGS (conditional: CI not started, paused; CodeQL not scanned at 66bf9aa; UNMEASURED-ON-SQLSERVER)`.

## Facts re-measured (instrument, control)
| Fact | Instrument | Control / note |
|---|---|---|
| Branch `b739/...` @ `66bf9aa84684f0d355c6ca89fe0f05ac733023af`, the only b739 ref | `gh api -X GET git/matching-refs/heads/b739` | list shows 1 ref |
| Delta ahead 3 behind 0, 6 files, +12/-6, +5/-1, +8/-1, +8/-3, +1/-1, +713/-0 | `gh api compare bcb359f8...66bf9aa8` (files and commits) | matches the builder's numstat; commits `c8e28b55`, `a64216e8`, `66bf9aa8`, all `unsigned` |
| main `1523cd2db09fd49f26da46af5155432de17fa2a3`, one file vs `b069274c` (the Assessment csproj) | `matching-refs/heads/main`, `compare` | #225 landed; shared with your six: 0 |
| #223 open, head `bcb359f8`, `mergeable_state` blocked; open PRs 224, 223, 222, 221 | `pulls/223`, `pulls?state=open` | no PR has head b739 |
| Tree of `bcb359f8` = `7a142ebd...`, head tree `60b34ece...` | `git rev-parse <c>^{tree}` on the shared clone | `cat-file -t 66bf9aa8` = commit |
| Six blobs parent -> head and line counts (kit "The six files"); unchanged blobs `dd298a537fd2`, `ad23fab94867`, `8f9709616ca2` identical both sides | `rev-parse <c>:<path>`, `cat-file -p | wc -l` | parent line counts derived from numstat (414/180/1173/272) |
| `HasControl(` lines ActionPlan 2/2, Finding 0/0, Reporting 2->3, Requests 7/7; `StringComparison.Ordinal)` lines ActionPlan 0->2, Reporting 10->11, Requests 2->4, Finding 0/0 | `cat-file -p` + `/usr/bin/grep -c` at both commits | a first attempt printed zeros because of a zsh `$c:` modifier mistake (path built wrong, git said "Not a valid object name"); redone with `${c}:` and the counts above are from the second run |
| `check-runs` at the head 0; analyses at `refs/heads/b739/...` 0; main analyses control returns 3 (per_page=3); base `bcb359f8` has 20 check-runs (17 success, 3 failure) and 4 analyses (csharp, js-ts, python, actions) | `gh api -X GET` | zero is a suspect: control fired (main rows) |
| No HPSM-POC pane live; panes: tuesday, MPS-M33, MPS-M32, NexusAI-M15, Security-Composer-J22, -G149, MPS-G148, fleet-monitor | `tmux list-panes -a -F '#{pane_id} #{@cockpit_name}'` at 15:37:50 | H36 is gone; `.tools/b739` and `wt-b739-*` exist (read-forbidden in the kit) |
| 9610-9619 and the whole 9600-9659 free | `lsof -nP -iTCP:... -sTCP:LISTEN` rc 1 | control: bound AND listened on 9611, `lsof` listed it, rc 0, then rc 1 after exit |
| Port scan: zero 26 Oct hits for `961x`; three finished 25 Oct kits hit (B665, B673, B685); frame 137 non-.pre SEAT `.md` kits (42 from 26 Oct) | python `-I` word-boundary regex `(^|[^0-9a-f])961[0-9]([^0-9a-f]|$)` | control: `956` hits B738, B739, B741, B744; `955` hits B739, B741, B744; `960x` hits B746 (a live NexusAI seat), so I did not take it |
| `B747`/`G150` unused: no `*B747*` in `tuesday/briefs/` (before writing) and none in the HPSM-POC `Briefs/` (`ls | grep -c` 0) | `ls` | `.tools` has no `b747`/`wt-b747-*` |
| Frame for the round count: 407 `*_STATUS.md`, 77 start `GATE VERDICT`; builder STATUS first line is `PROGRESS B739...` | python `-I` over line 1 | control: the B739 file is not counted as a verdict |
| `CLARIFICATIONS.md:138` is the only squash/match-head line; **no line records the 13:31 ruling** (`Land #223|Leave CI|13:31` count 0) | `/usr/bin/grep -n -i` / `-c` | the ruling is relayed in the builder kit's lane table and stamp lines; a records branch was not given |
| `dn.sh` line 4 holds `B=` and line 19 holds `grep -v b514` | `sed -n 1,40p | grep -n` | matches the kit's token instructions |
| Words: failed-narrative sentence is `web/src/content/narrative-failure.ts:23` at the head (no `web/**` path in the delta); design-pack `05_ai-narrative-pipeline.md:67` names `schema-invalid` for the validator; no records file rules the sentence | `git grep -n -E 'schema-invalid|narrative-failure' <H> -- web/src`; `grep -n` over the pipeline doc | the kit tells the gate to trace the origin with `git log -S` and to say "ruled in <file:line>" or "code-owned, no ruling found" |

## Things the builder's STATUS does not say (found by reading the diff and a `git grep`; the kit makes them checks)
1. A second pipeline caller: `Showcase/ShowcaseSeeder.cs:246` calls `seedNarratives.GenerateAsync` and stores the outcome; it is NOT behind the new screen (C5 census, grade Note unless a model text can reach it).
2. The failed-row `fallback` echoes an EARLIER approved or edited narrative's `NarrativeText` in the 201 view (`ReportingEndpoints.cs` ~223-250): a stored text surfaced, not a write; a held scalar could surface there (Note).
3. `PutDisposition` now reads `Dispositions.CurrentAsync(db, assessment!.AssessmentId, ...)` BEFORE the shape (a second read, not a hoist). The kit makes two checks of it: whether `assessment` is provably non-null on every path that reached the shape at the parent (a 500 where the parent answered 400/403/404 is a Blocker), and whether it opens an equality oracle across assessments (C3).
4. The builder's wording "two commits" is wrong in its own kit; there are THREE (builder Correction 1). `main` also moved during its build (#225 landed).
5. S9 (Paragraphs/Caveats not cleared on a hit) is the builder's one survivor; the gate must judge it by a run with a decorator carrying a scalar in Paragraphs/Caveats, not by the builder's grep.

## D-decisions (mine; Tuesday accepts or overrides at the stamp)
- **D-1 The verdict covers the stack, not the re-landed commits.** The re-land is a different commit set; the kit makes the gate write its check predicate and does not run it. Alternative (gate the re-land too) is impossible: it does not exist yet.
- **D-2 Merge prediction is informational** (`merge-tree --write-tree` in the gate's own clone; expected 7 changed paths against main: #223's five + `FindingEndpoints.cs` + the new test file; a build of that tree only if Q-2 is YES). GitHub gives no merge ref for a branch without a PR.
- **D-3 Best verdict `GO WITH FINDINGS (conditional ...)`**, as B738 grades a paused CI, plus the B729 rule that nothing says GO until the 61 new rows are read `Passed` on a SQL Server shard. Neither can happen before the re-land PR's CI runs.
- **D-4 Allowance tested as the property "ordinal-equal, as sent, same field of same row"**, with all 212 scalars as stored values (middle for all, edges for one per class plus every .NET white-space scalar), 18 variants, cross-row, cross-field, older-disposition-row and removed-item cells, three JSON encodings, parent as the control. The builder's 3-character middle-only plants are reported as what they pin.
- **D-5 S12 (screen narrowed to the builder's three characters) is expected to survive the builder's rows** and be red in the gate's matrix; graded Note while all call sites call the shared function (same logic as B729's Y11b).
- **D-6 Words:** zero tolerance; the gate traces the origin of the failed-narrative sentence and treats the builder's question (is it the right words for a model reply that held a hidden character) as a Note for the product owner via Tuesday.
- **D-7 Mutant battery:** one switch build for the guard family, literal-edit builds for structural ones, the builder's A/B/S names plus B11-B14 and S10-S12 of the gate's own, seed `747101`; priority order puts C2/C3/C5/C7 before the mutants and never cuts the base-vs-head control, the order cells, S9, the CodeQL read or the moved-head/base checks.
- **D-8 Ports 9610-9619, none expected to be bound** (in-process hosts). 9610-9619 was assigned in a finished 25 Oct kit (B665, "tentative", pane gone) and two others mention it; 9630-9639 has the same count; nothing in 26 Oct kits.
- **D-9 Hygiene:** the kit says "the product owner's 2026-10-26 13:31:40 ruling" and "the 12:35 ruling"; no person's name and no decision-card id or card slug appears in it (grep for a name list and for `decision-card` shapes: the only matches are the kit's own prohibition sentences).

## Questions for Tuesday (each with a default)
- **Q-1** May the gate add scratch variants of the four product files and its own plant class in `.tools/wt-b747-mut` (never committed, restored byte-equal)? Default **YES** (C2, C5 and C10 need it; NO caps the verdict).
- **Q-2** May the gate make ONE `git commit-tree` object write (no ref) inside its own clone to build the merge-prediction tree? Default **YES** (NO makes the prediction tree-only and the combined build NOT TESTED).
- **Q-3** Round-count statement: "NO GO 0 of 2 on this class". Default **confirmed** (frame 407/77 at my read; no verdict names the class).
- **Q-4** Port block 9610-9619. Default **accept** (none expected to be bound).
- **Q-5** Hard stop and target verdict. Default: target verdict 4 h and HARD STOP 5 h 30 m after the gate's Step-0 date (about 40 mutant builds under a load of 8-9), absolute at Step 0, and not past whatever outer bound Tuesday sets.
- **Q-6** Launch before #223 lands? Default **YES** (nothing depends on it; a landed #223 is handled by the stacked-head rule, a moved #223 head is NOT GATED).
- **Q-7** Does the product owner want the failed-narrative words (`narrative-failure.ts:23`) reviewed for a model reply that held a hidden character? Default: **leave it as the gate's Note**, raised by Tuesday with the verdict.

## UNMEASURED (by me)
No dotnet, clone, fetch, worktree, build, mutant or run. Not measured: the reach of the allowance and the screen over the 212 scalars; S9; whether `assessment` can be null at the new read; the equality oracle; whether the builder's 61/33/28 and 2089/0/13 reproduce; the seven-path merge prediction (`merge-tree` forbidden to me) and whether a cherry-pick applies cleanly; SQL Server, CI and CodeQL at the head (nothing ran); a browser round trip changing CR LF; hosted UAT/demo data; the 3 failing check-runs of the base `bcb359f8` (names not read); the 13:31 ruling's record outside the builder kit (no records file holds it); load at the gate's start (15:41 load averages 8.13 8.97 9.31).

## Outside-the-fences disclosure
- My first Bash call contained a `cd` and the hook refused it (nothing ran); every later call used absolute paths.
- A second call with an unquoted `======` was refused by the zsh hook; nothing ran.
- I ran `grep -rl` (list only) over `1_Project_Definition/Content`, `Registers`, `Design`, `Governance` and `Architecture` for `schema-invalid` and related words (it matched only three `Architecture/design-pack` files; file names only were printed), and `ls` of `1_Project_Definition` and of `Content` and `Registers` at the top level. I opened no file under `Content/`, `Source_Documents/`, `HP Reporting and Docs/` or `inbound/`; the kit tells the gate not to touch `Content/` or `Source_Documents/`.
- I read `Briefs/2026-10-26_B739_STATUS.md` and the line 1 of every `*_STATUS.md` (python `-I`, first line only).
- I listed `.tools/` of HPSM-POC (names only) and read `.tools/b514/dn.sh` lines 1-40; opened nothing else under `.tools/`.
- One loopback listener on 9611 for about 6 seconds (the `lsof` control). Scratch scripts `scan.py` and `frame.py` in my session scratchpad (`/private/tmp/claude-501/-Volumes-Laptop-DEV-TUESDAY/a4b8b0d7-c5c4-4870-a000-03dec8ba3ee1/scratchpad/`); no file written in any project tree except the two outputs.
- I did not use `decision_queue.sh`, Jira, mail, any Artifact/Docs tool, or `gh` beyond `-X GET`; no HTTP to a hosted host.
