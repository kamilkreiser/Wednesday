From Friday (laptop seat), Datasec / MPS Commercial Calculator. Replies to friday-laptop-agent@agentmail.to (no mail key in this project: your STATUS file is the wrap).
# BRIEF B39 · SEAT-R — record gate B38's findings and notes in BACKLOG, post the three B37 "advances, not Done" Jira comments, record one unrecorded card ruling as C-22, fold `records/b37` + `records/b39` into records main
**Written:** @NOW@. **Pane:** `Datasec/MPS-R`. Your commission is the newest file in `Briefs/` containing `_SEAT-R_`.
(Launcher check, read by the draft writer: `Launch_Claude.command:107` sets `SEAT` from a pane name matching `*MPS*-?`; `:111` says the commission is "the NEWEST brief in 1_Project_Definition/Briefs/ whose file name contains _SEAT-${SEAT}_ (NOT simply the newest file)". At drafting, 1 file in `Briefs/` contains `_SEAT-R_`: B34, which is finished: its STATUS ends `READY FOR REVIEW — records main @ 76d735c086715167a9b15f7a1a401fa150f66f57`.)
**Seat:** Seat R (Claude records seat). **RECORDS ONLY: no product code.** One records branch, the fold, three Jira comments, your STATUS. Nothing else.
**Report:** `1_Project_Definition/Briefs/2026-10-12_B39_STATUS.md`. Its last line is exactly one of:
- `RECORDS DONE: <one line: records main @ <sha from git rev-parse main after the fold>, rows N, C-22 y/n, Jira 3/3 read back>`;
- `STOPPED: NEEDS FRIDAY` and ONE question.

## AUTHORITY
- **Friday commissions this round.** The BACKLOG rows are the gate's own findings (`Briefs/2026-10-11_B38_STATUS.md`, B38 seat E) and the rows B37 seat B already wrote on `records/b37`. The Jira lines are Friday's wording, below. None of this needs Kam's word.
- **C-22 records a ruling Kam already made** (card text quoted in ITEM 3 from Friday's decision queue). Do not compose any wording inside a quote.
- **Who writes Jira here, as measured:** the project `CLAUDE.md` does not reserve Jira for Friday; `Launch_Claude.command` tells every seat to record progress in "the Jira ticket(s) the brief names", and seats have posted every MPS comment so far (B01–B03 per `JIRA.md`; B09/B17/B18 comments 39263, 39306, 39315, 39319, 39321; B34's 39326–39332). B37's "Jira comments are Friday's" was that brief's rule only. **This brief names three tickets, so you post them** (ITEM 2).

## READ WHOLE FIRST
- The project `CLAUDE.md`, `JIRA.md`, `BACKLOG.md` **as it stands on `records/b37`** (`git show records/b37:BACKLOG.md`; 388 lines at drafting), and `1_Project_Definition/CLARIFICATIONS.md` on records `main` (ends at C-21).
- `Briefs/2026-10-11_B38_STATUS.md`: `## Findings` (L-1…L-4), `## Notes` (N-1…N-8), `## Post-deploy check items` (P-1…P-3), `## NOT TESTED`.
- `Briefs/2026-10-11_B37_STATUS.md`: `## RECORDS`, `## needs-Friday`, `## UNMEASURED`.
- `Briefs/2026-10-11_B34_SEAT-R_board-reconcile-and-records.md` and `Briefs/2026-10-11_B34_STATUS.md` (the records route you repeat, and its precedent B21/B30).

## THE RECORDS ROUTE (measured by the draft writer, read verbs only, `--no-optional-locks`)
Friday's rule (ledger, 2026-10-11): *"a records instruction names the repo by reading where BACKLOG.md lives and whether it has a remote"*.
- `BACKLOG.md` lives at the **project root**, so the records repo is the **project-root** git repo (not `2_Project_Files`).
- `git -C <root> remote -v`: **empty** (rc 0). **No remote: nothing is pushed in this round.** Commit only.
- Records `main` = `76d735c086715167a9b15f7a1a401fa150f66f57` (B34's fold).
- `git branch --no-merged main` = **`records/b37` only**. `records/b12`, `b21`, `b25`, `b30`, `b34` are all merged (B34 folded them).
- `records/b37` = `d458b38be4f1a1307f4a7f3d434b50fd05244216`, in worktree `.tools/wt-B37-records`; `rev-list --left-right --count main...records/b37` = `0 3`; `merge-base --is-ancestor main records/b37` = yes. Its 3 commits: `e8521d4` (gate B36 rows), `a0f522c` (`[B37-G1-LOAD]`), `d458b38` (that row's count corrected). `git diff --stat main records/b37`: `BACKLOG.md` +64, nothing else.
- Root `git status --porcelain --untracked-files=no`: **empty**. Untracked: 118 (mostly `Briefs/`); leave them all.

## ITEM 1 — BACKLOG rows (one commit on `records/b39`)
**Branch:** `git -C <root> worktree add .tools/wt-B39-records -b records/b39 records/b37` (`chmod 700`). Build on `records/b37`, so B37's five rows `[B36-K6]`, `[B36-N4]`, `[B36-N10]`, `[B36-K2-purchase]`, `[B37-G1-LOAD]` ride along into main (they are **not** on main today: `git show main:BACKLOG.md | grep -c -i 'B36-K6'` = 0 at drafting; on `records/b37` = 1). Do not rewrite them.

**First check:** `grep -n -i '<row id>'` on `records/b37:BACKLOG.md` for every id below. If one is already there, skip it and say where.

**Shape:** B37's rows under `## Deferred problems` (e.g. `[B36-N4]`): `- [ ] **[ID]** (origin; **Severity**) one-line summary`, then `Where` / `Symptom, the gate's words` (verbatim, `*"…"*`, cited `B38_STATUS.md` + section) / `Fix shape` (B38's HOW, verbatim) / `Why deferred` / `Discovered`. **Summaries are the B38 heading text, verbatim**; quote, never reword. `Discovered:` *found by gate B38, 2026-10-11 (`B38_STATUS.md` <id>); recorded by B39 seat R, 2026-10-12*. `Why deferred:` *round 2 of 2 of the B36/B37/B38 cycle; the gate ruled GO WITH NOTES and left ticketing to Friday (B38 BLUF: "Friday decides what ships and what is ticketed (round 2 of 2: no round 3)")*.

| Row id | Source (B38 STATUS) | Severity / origin | Must also carry |
|---|---|---|---|
| `[B38-L1]` | `### L-1` | Minor, INTRODUCED BY B37 | the `[3,5,5]` TESTED line verbatim |
| `[B38-L2]` | `### L-2` | Minor, INTRODUCED BY B37 + PRE-EXISTING | the line *"**The hosted count is UNKNOWN** (P-1). If P-1 finds any, Friday may want to raise this before deploy."* and the P-1 item verbatim from `## Post-deploy check items`. Plus the hold below. |
| `[B38-L3]` | `### L-3` | Minor, INTRODUCED BY B37 | cross-reference `[B38-N3]` (negative overrides) |
| `[B38-L4]` | `### L-4` | Minor, RESIDUE of K-5 | the line *"Today no generic type is defined under `src/` (grep 0; control 1), so **nothing leaks at head**"* |
| `[B38-N2]` | `N-2` | Note, PRE-EXISTING | cross-reference `[B38-L2]` |
| `[B38-N3]` | `N-3` | Note, PRE-EXISTING; a pricing question | — |
| `[B38-N4]` | `N-4` | Note, PRE-EXISTING | — |
| `[B38-N5]` | `N-5` | Note, a K-5 judgement ("a view, not a ruling") | the gate's *"My view: worth doing; Friday's call."* verbatim |
| `[B38-N6]` | `N-6` | Note: a **measurement addendum to `[B37-G1-LOAD]`**, not a new problem | say so in the summary line; do **not** edit the `[B37-G1-LOAD]` row |
| `[B38-N7]` | `N-7` | Note, **no action** (the gate: *"It relies on the frozen clock on purpose and hides no write."*) | — |
| `[B38-N8]` | `N-8` | Note, **no action** (the gate: *"Expected, not a change."*) | — |

N-1 (a comment-only cross-row hunk) is not commissioned: do not record it.

**The P-1 hold (under `## Holds on the hosted site`, after the B25 HOLD, same shape):**
- Heading text: `HOLD (B39, Friday, from gate B38 P-1 / L-2; recorded 2026-10-12): before any hosted MPS deploy of a main that contains B37's K-3 refusal (f48edf0, merged as main 44374606):`
- Body: the P-1 item, verbatim, then: *"The hosted count of quotes with repeated fleet line numbers is UNKNOWN (B37 UNMEASURED; B38 NOT TESTED). Lifted only by a brief that records the count."* (this sentence is Friday's wording; it is not a quote from the gate, so do not put it in `*"…"*` as one; mark it *Friday's words*).
- Hosted today runs `db8edfd` (C-21), which does not contain K-3: say so as fact, cited C-21.

Commit message: `Records: gate B38 rows [B38-L1…L4], [B38-N2…N8] and the hosted P-1 hold (B39)`.

## ITEM 2 — Jira: three "advances, not Done" comments (no transition)
**Credentials (names only):** `4_Credentials/.env` holds `JIRA_BASE_URL`, `JIRA_EMAIL`, `JIRA_API_TOKEN` (B34 used them). A small scratch helper reads the file and sends Basic auth. **Never print, log or write the token**, never on a command line.

**Merge facts, measured before any write.** In `2_Project_Files` (`fetch` and read verbs only):
1. `git fetch origin` rc 0; `git ls-remote origin refs/heads/main`. At drafting: **`44374606f49bc5c5498ad7fbd19230de487d85c2`**.
2. `git rev-parse 44374606^{tree}` must equal `2c1fd884bd833bddd76ea622a05b1d2a80d5f74f`, and so must `git rev-parse f48edf0^{tree}` (draft writer read the latter: equal; the former was **not readable** at drafting because the local clone had not fetched it).
3. `git log -1 --format=%s 44374606` names PR **#26** (draft writer could not read it: unfetched, and no `gh`).
If main moved past `44374606`, use the main you measured only if `44374606` is its ancestor, and say so. If (2) or (3) fails, **post nothing** and STOP: NEEDS FRIDAY.

**Per key:** (1) re-read (`GET …?fields=status,comment`): at drafting all three were `Backlog`, newest comments 49 → 39310, 33 → 39321, 47 → 39319, none mentions B37. If a newer comment already carries this text, SKIP and quote its id. (2) POST the line below verbatim, one ADF paragraph, no person named. (3) read the comment back by id, byte for byte. **No transition, no field, label, link or issue.**

- **MPSCALC-49:** `B37 (gate B36 K-1, K-4): a proposal GET whose quote save fails now records no event in memory or on disk (500, no proposal); the suite now kills E-04 on a moving clock. Merged as PR #26 → MPS main 44374606 (tree 2c1fd884 = gated head f48edf0). Deltas gate B38: GO (K-1, K-4). Not deployed: hosted runs db8edfd. Advances, not Done.`
- **MPSCALC-33:** `B37 (gate B36 K-2, K-3): a rental override re-sent at another decimal scale is no change; a draft whose fleet line numbers repeat is refused 400 (create, PATCH, duplicate). Merged as PR #26 → MPS main 44374606 (tree 2c1fd884 = gated head f48edf0). Deltas gate B38: GO WITH NOTES (BACKLOG [B38-L1], [B38-L2], [B38-L3]). Purchase half of K-2 is BACKLOG [B36-K2-purchase]. Before any hosted deploy: count stored quotes with repeated fleet numbers (BACKLOG hold, B38 P-1). Advances, not Done.`
- **MPSCALC-47:** `B37 (gate B36 K-5): the allow-list guard is transitive; 16 nested DTO types listed, 105 fields NotShown (INTERNAL_ONLY); M4 is now red. Merged as PR #26 → MPS main 44374606 (tree 2c1fd884 = gated head f48edf0). Deltas gate B38: GO WITH NOTES (BACKLOG [B38-L4]: a generic solution DTO type is not walked; none exists today). Advances, not Done.`

If (3) of the merge facts shows a PR number other than #26, replace `#26` with the measured number in all three lines and say so; change nothing else.

## ITEM 3 — CLARIFICATIONS C-22 (one commit on `records/b39`)
**Measured by the draft writer:** `decision_queue.sh list ruled | grep -i mpscalc` = 23 ruled MPS cards; each card id grepped (`-i -c`) in `main:CLARIFICATIONS.md` (control `mpscalc-cost-rounding` = 1). **22 are recorded. One is not: `mpscalc-azure-login-for-hosting-1010` (0 hits; also 0 for `a6b8fe11`, `budget alert`).** No MPS card was ruled after C-21's (`2026-10-11T10:23:20`). (`datasec-90pct-gates-wait-for-fresh-account-1001` is a scheduling card about the fleet's usage, not an MPS product ruling: do not record it.)

**First check:** `git show records/b39:1_Project_Definition/CLARIFICATIONS.md | grep -i -c 'azure-login-for-hosting'`; if ≥ 1, skip and say where.

**C-22 — card `mpscalc-azure-login-for-hosting-1010`** (shape: C-14's; heading = the card title verbatim; card id and timestamps on every entry). Source: FRIDAY decision queue (outside this project; **do not open it**: the lines you need are here).
- title: *"Sign the MPS project into Azure once, so it can be hosted for Monday"*
- `ruled_choice` **a**, `ruled_ts` `2026-10-10T09:33:47.981206+11:00`. Board-log line: **none found** (`grep -rn -i azure-login-for-hosting Briefs/` hits only `B14_SEAT-C_infra-ci-deploy-demo.md:184`, which names the card, not the tap). Say so.
- option a: *"Done: I have signed in"*: *"The infra seat creates the new resource group mpscalc-showcase-rg, one B1 App Service (about A$21 a month) and a budget alert, and deploys after the QA gate."*
- `delivered_artefact`: *"MPS 4_Credentials/.azure: az account show = kamil@datasec-rd.com, tenant ec01829b, sub a6b8fe11 (read 09:34)"*, `delivered_ts` `2026-10-10T09:33:59.302515+11:00`.
- **Do not copy the card's step text** (it holds a login command line and a full tenant id). Write no full tenant or subscription id.
- Note as fact: it predates C-13 and is recorded late; C-13 cites the resulting hosted showcase.

Commit message: `Records: C-22 (Kam's 2026-10-10 Azure sign-in card, recorded late) (B39)`.

## ITEM 4 — Fold `records/b37` and `records/b39` into records `main`
1. After ITEMS 1 and 3 are committed: root `git status --porcelain --untracked-files=no`. If it lists any path in `git diff --name-only main records/b39`, **STOP: NEEDS FRIDAY**. Never stash, checkout, switch, reset, `update-ref`, or `fetch . x:main`.
2. If `main` is an ancestor of `records/b39` (expected: `main` = `76d735c`, an ancestor of `records/b37`): `git -C <root> merge --ff-only records/b39`.
   Otherwise: `git -C <root> merge --no-ff records/b39 -m "Records: fold records/b37, b39 into main (B39)"`. A conflict in `history.md` only may be resolved by keeping **both** sides' entries, newest at top, no word changed. Any other conflict: `git merge --abort`, then **STOP: NEEDS FRIDAY**.
   **Never rebase, never force, never cherry-pick.**
3. Read back: `git rev-parse main`; `merge-base --is-ancestor records/b37 main` and `records/b39 main` = yes; `git branch --no-merged main` = empty; `main:CLARIFICATIONS.md` `### C-` count (`grep -i -c`) = 23 if C-22 written (22 on `76d735c`, the control); `main:BACKLOG.md` holds the 5 B37 ids and your new ids (count each, `-i`); root tracked status is what it was before step 2.
4. **Delete no branch and remove no worktree.**

## Ports
None needed: **bind nothing**. (Reserved for B39 only if a tool insists: 6920–6929; `grep -rhoE '\b6[5-9][0-9]{2}\b' Briefs/` names nothing in 6920–6949 at drafting.)

## Leak + secret scan
Run B34's records scan (`.tools/qa-B34/tools/leak26.py` + `adjud.py`, copied into `.tools/qa-B39/`; lists read-only by path; counts only, a positive control that fired) over `git diff 76d735c..records/b39`, the commit messages, the three Jira texts, and this STATUS before its last line. Plus `gitleaks` with a planted control.
- Expected, to adjudicate, not to hide: `kamil@datasec-rd.com` in C-22's delivered artefact (already in CLAUDE.md and C-13); the year `2026`; the HTTP status `400`/`500`; `@example.test` if a quoted gate line carries one. **Never print an avoid list.**

## STATUS sections
BLUF · ITEM 1 (ids written, skipped + where) · ITEM 2 table (key · re-read · comment id · read-back equal) with the merge facts as measured · ITEM 3 · ITEM 4 (commands, before/after `main`, ancestry, root status before/after) · UNMEASURED · `## NOT DONE / NOT COVERED` · needs-Friday · Leak + secret scan · processes started/stopped · worktrees and files left.

## UNMEASURED (by the draft writer)
- **`44374606`'s tree and PR number:** the object is not in the local clone (no fetch at drafting; no `gh`). ITEM 2 (2)–(3) closes it.
- **Whether Friday or another seat writes `records/*` or main before you run:** re-measure `git branch --no-merged main` first and fold anything new only if Friday's brief names it; otherwise list it under needs-Friday.
- **Whether any of the three Jira lines was posted by Friday after drafting:** ITEM 2 step (1) closes it.

## HOLDS
- Datasec only; no other client's names, tickets or paths.
- No product code; `2_Project_Files`: `fetch` and read verbs only. No checkout, switch, commit, branch or push there. CodeQL policy unchanged (this round pushes nothing).
- No deploy, no Azure, no setting change. **Nothing to any human**: the three Jira comments are the only outbound writes, and they name no person.
- **Own worktree:** `.tools/wt-B39-records` only. Do not commit in `wt-B37-records` or any other seat's worktree.
- **Never delete; quarantine** to `.tools/_quarantine/2026-10-12_B39_<what>/` (0700) and say so. No `branch -d/-D`, `worktree remove`, `gc`, `prune`.
- **Records:** write only `records/b39` (ITEMS 1, 3), the fold of `main` (ITEM 4) and your STATUS. `CLAUDE.md`, `JIRA.md` and `history.md` are Friday's: do not edit them. Existing BACKLOG rows are not edited; you only add.
- **Processes:** kill by port + cwd, never by name. Stop everything you started before the last line.
- **Instruments:** verdicts are ratios with denominators; every scanner zero has a positive control that fired; every grep for a phrase is `-i`.

## End
The last line of `Briefs/2026-10-12_B39_STATUS.md` is exactly one of:
- `RECORDS DONE: <one line>`;
- `STOPPED: NEEDS FRIDAY` and ONE question.
