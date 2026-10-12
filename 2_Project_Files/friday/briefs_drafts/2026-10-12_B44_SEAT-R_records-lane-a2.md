From Friday (laptop seat), Datasec / MPS Commercial Calculator. Replies to friday-laptop-agent@agentmail.to (no mail key in this project: your STATUS file is the wrap).
# BRIEF B44 · SEAT-R — record lane A2 (PR #27 → main b28c95eb): history entries for B40–B43, BACKLOG rows for gate B43's residues, three Jira tickets (Q-1, Q-2, Q-3), three "advances, not Done" comments, fold `records/b42` (which carries `records/b40`) into records main
**Written:** @NOW@. **Pane:** `Datasec/MPS-R`. Your commission is the newest file in `Briefs/` containing `_SEAT-R_`.
(Launcher check, read by the draft writer: `Launch_Claude.command:107` sets `SEAT` from a pane name matching `*MPS*-?`; `:111` says the commission is "the NEWEST brief in 1_Project_Definition/Briefs/ whose file name contains _SEAT-${SEAT}_ (NOT simply the newest file)". At drafting, 2 files in `Briefs/` contain `_SEAT-R_`: B34 and B39. Both are finished: B39's STATUS ends `RECORDS DONE: records main @ 564f86d624e0a04bf74fd326f5cf516d73d02134, rows 11 (+ the P-1 hold), C-22 y, Jira 3/3 read back`.)
**Seat:** Seat R (Claude records seat). **RECORDS ONLY: no product code.** One records branch, the fold, three Jira tickets and three Jira comments, your STATUS. Nothing else.
**Report:** `1_Project_Definition/Briefs/2026-10-12_B44_STATUS.md`. Its last line is exactly one of:
- `RECORDS DONE: <one line: records main @ <sha from git rev-parse main after the fold>, history 4/4, rows N, tickets <keys>, Jira comments 3/3 read back, C-23 n>`;
- `STOPPED: NEEDS FRIDAY` and ONE question.

## AUTHORITY
- **Friday commissions this round.** The history facts are the four seats' own STATUS lines. The BACKLOG rows are gate B43's own findings (`Briefs/2026-10-12_B43_STATUS.md`, seat E). The Jira lines and the ticket shape are Friday's, below. None of this needs Kam's word.
- **`history.md` is written in this round, by commission.** B39's hold called it Friday's; this brief names it (ITEM 3b). Only the four entries named here; no other entry is edited.
- **Who writes Jira here, as measured:** `Launch_Claude.command:96` tells every seat to record progress in "the Jira ticket(s) the brief names"; seat B39 posted 39333–39335 (`B39_STATUS.md:11`). B40 and B42 left draft lines for Friday (`B40_STATUS.md:622-625`, `B42_STATUS.md:732-738`); those were those briefs' rules only. **This brief names MPSCALC-50, -53, -55 and three new tickets, so you write them** (ITEMS 2 and 4).
- **No C-23.** Measured by the draft writer: `bash …/FRIDAY/2_Project_Files/tools/decision_queue.sh list ruled | grep -i -c mpscalc` = **23**; the newest MPS ruling is `mpscalc-b30-new-words-hosted-deploy-1011` (`2026-10-11T10:23`), already C-21 (`main:1_Project_Definition/CLARIFICATIONS.md:287-288`); `### C-` count on records main = **23** (C-0…C-22, C-22 at `:298`). No MPS card was ruled after it; the only non-ruled MPS card is `[withdrawn] mpscalc-codeql-javascript-web-1009`. **Write no CLARIFICATIONS entry.** Gate B41 N-10 (FR-ADM-009, a draft calculated on a now-Superseded set may be approved) is an **open** question, not a ruling: do not record it (B42 `:731-733` left it to Friday).

## READ WHOLE FIRST
- The project `CLAUDE.md`, `JIRA.md`, `1_Project_Definition/CLARIFICATIONS.md` on records `main`, and `BACKLOG.md` **as it stands on `records/b42`** (`git show records/b42:BACKLOG.md`; **616 lines** at drafting, against 468 on `main`).
- `5_Project_History/history.md` on records `main`: newest entry is `## 2026-10-11 — B33 SEAT-C …` (`:3`). Copy its entry shape.
- The four STATUS files, whole: `Briefs/2026-10-12_B40_STATUS.md` (679 lines), `B41_STATUS.md` (686), `B42_STATUS.md` (788), `B43_STATUS.md` (537).
- `Briefs/2026-10-12_B39_SEAT-R_records-b37-b38.md` and `Briefs/2026-10-12_B39_STATUS.md` (the records route you repeat, and B39's Jira helper method: `B39_STATUS.md:51-69`).

## THE RECORDS ROUTE (measured by the draft writer, read verbs only, `--no-optional-locks`)
Friday's rule (ledger, 2026-10-11): *"a records instruction names the repo by reading where BACKLOG.md lives and whether it has a remote"*.
- `BACKLOG.md` lives at the **project root**, so the records repo is the **project-root** git repo (not `2_Project_Files`).
- `<root>/.git/config` holds **0** `remote` lines. **No remote: nothing is pushed in this round.** Commit only.
- Records `main` = **`564f86d624e0a04bf74fd326f5cf516d73d02134`** (B39's fold, `B39_STATUS.md:93`).
- `refs/heads/records/*` (`for-each-ref`): `b12 b21 b25 b30 b34 b37 b39` are ancestors of `main` (`merge-base --is-ancestor` rc 0 each). **Not merged: `records/b40` and `records/b42` only.** There is **no `records/b41` and no `records/b43`** (gates B41 and B43 wrote no records: `B41_STATUS.md:4`, `B43_STATUS.md:4`).
  - `records/b40` = `80a5abb95b657ec8f79e9a0e54930f19bd563bd8` (worktree `.tools/wt-B40-records`); `rev-list --left-right --count main...records/b40` = `0 3`: `1c2b659` (rows `[B40-R1]`…`[B40-R7]`), `118ab1c` (`[B40-R8]`), `80a5abb`.
  - `records/b42` = `0b792fc778612703681490679ccb76576e55f11e` (worktree `.tools/wt-B42-records`); `main...records/b42` = `0 4`; `merge-base records/b40 records/b42` = `80a5abb` = `records/b40`, so **`records/b42` contains all of `records/b40`** plus `0b792fc` (rows `[B42-L1]`…`[B42-L7]`, `[B42-R1]`, dated lines on `[B40-R5]`, `[B40-R7]`, `[B40-R8]`).
  - `git diff --stat main records/b42`: `BACKLOG.md` +148, nothing else.
- Root `git status --porcelain --untracked-files=no`: **empty** (rc 0). Untracked: 132; leave them all.

## ITEM 1 — Merge facts (measured before any write)
In `2_Project_Files` (`fetch` and read verbs only):
1. `git fetch origin` rc 0; `git ls-remote origin refs/heads/main`. At drafting: **`b28c95eb0f73ed0ce7ae410791feefc8b1a059ea`**.
2. `git rev-parse b28c95eb^{tree}` must equal **`2826f02744a28e7ffd5689bd1885e2b03cad68b6`**, and so must `git rev-parse ab8fdf1^{tree}` (gate B43's head tree, `B43_STATUS.md:33`, `:56`). The draft writer could **not** read `b28c95eb` (the local clone has not fetched it: `rev-parse` fatal; `origin/main` = `4437460` locally).
3. `git log -1 --format='%H %P%n%s' b28c95eb` names PR **#27** (UNMEASURED at drafting; Friday's own note records *"MERGED MPS PR #27 (lane A2: B40 + B42): … main b28c95eb, tree 2826f027"*). Record its parents, and `merge-base --is-ancestor 44374606 b28c95eb` and `… ab8fdf1 b28c95eb` as facts (either merge style is fine; only the tree decides).
If main moved past `b28c95eb`, use the main you measured only if `b28c95eb` is its ancestor, and say so. If (2) or (3) fails, **write nothing anywhere** and STOP: NEEDS FRIDAY.

## ITEM 2 — Jira: board search, then three tickets (Q-1, Q-2, Q-3)
**Credentials (names only):** `4_Credentials/.env` holds `JIRA_BASE_URL`, `JIRA_EMAIL`, `JIRA_API_TOKEN` (B34 and B39 used them). A small scratch helper (B39's `jira39.py` method, new copy in the session scratchpad) reads the file and sends Basic auth. **Never print, log or write the token**, never on a command line.

**2a. Search first (read only).** JQL `project = MPSCALC AND text ~ "<term>"` for each of: `SourceLifecycle`, `registry.json`, `IsEmptyStore`, `EngineRead`, `SourceDocumentChecks`, `ReadRegistry`. Record each count and every key returned. Control: `text ~ "MPSCALC"` or a term you know is on MPSCALC-50 (e.g. `"FR-ADM-012"`) must return ≥ 1. Also read `GET /rest/api/3/issue/MPSCALC-50?fields=status,comment,issuelinks,parent` and list its links. If any returned issue already describes one of Q-1, Q-2 or Q-3 (same file and same symptom), **do not file that one**: name the key and use it in ITEMS 3–4 instead.
**2b. Read the create rules (read only):** `GET /rest/api/3/issue/createmeta/MPSCALC/issuetypes` and, for the chosen type, its fields. Use issue type **`Bug`** if offered, else **`Task`** (say which). Priority **`Low`** if the field is on the screen and offers it; if not, create without a priority and say so (do not pick another value). Link type **`Relates`** if `GET /rest/api/3/issueLinkType` lists it; if not, STOP: NEEDS FRIDAY before creating.
**2c. Create, one per residue** (`POST /rest/api/3/issue`, then `POST /rest/api/3/issueLink` type `Relates` to **MPSCALC-50**). No assignee, label, sprint, parent or transition. Description: ADF paragraphs and a bullet list, built only from the lines below; gate text inside `"…"` is copied from `B43_STATUS.md` byte for byte (no paraphrase, no ellipsis that changes meaning). No value, no person, no full path outside the repo.
| Residue | Summary (Friday's words, exact) | Description must carry |
|---|---|---|
| Q-1 | `Source version store: three on-disk store shapes refuse the start without words (gate B43 Q-1)` | first line `Severity: Minor (gate B43). RESIDUE of M-2, PRE-EXISTING at base.`; the `### Q-1` heading's file:line text (`:281`); the FOUND bullets (`:282-285`); the HOW (`:290`); `Found by gate B43 (Briefs/2026-10-12_B43_STATUS.md, Q-1) on b42/gate-b41-fix-round @ ab8fdf1, merged as PR #27 → main b28c95eb. BACKLOG [B43-Q1].` |
| Q-2 | `Source version store: a reference-only store that loses registry.json re-initialises silently (gate B43 Q-2)` | `Severity: Minor (gate B43). RESIDUE of M-2, PRE-EXISTING at base.`; FOUND (`:293`); the two-lists collision (`:297`); Gate's view (`:299`); HOW (`:300`) **including** *"This needs a rule choice from Friday on what "empty" means."*; the same found-by line with `BACKLOG [B43-Q2]`. |
| Q-3 | `Source document checks: catch-alls report an engine bug on a valid document as a document refusal, with no log line (gate B43 Q-3)` | `Severity: Minor (gate B43). INTRODUCED BY B42.`; FOUND (`:303`); the P4 probe results (`:304-308`); Gate's view (`:309`); HOW (`:310`); the same found-by line with `BACKLOG [B43-Q3]`. |

(Line numbers in `B43_STATUS.md` are the draft writer's reading: `### Q-1` `:281`, `### Q-2` `:292`, `### Q-3` `:302`, `## Notes` `:312`. Re-read them; if a line moved, cite the line you read.)
**2d. Read back** every created issue by key (`GET …?fields=summary,issuetype,priority,issuelinks,description`): summary byte-equal; the `Relates` link to MPSCALC-50 present; then re-run the 2a searches and show each new key appears once. A comparator control that fires (1-byte file ⇒ unequal), as B39 did (`B39_STATUS.md:68`).

## ITEM 3 — Records (commits on `records/b44`)
**Branch:** `git -C <root> worktree add .tools/wt-B44-records -b records/b44 records/b42` (`chmod 700`). Build on `records/b42`, so B40's 8 rows and B42's 8 rows (and B42's dated lines) ride along into main unchanged. Do not rewrite them.

**3a. BACKLOG rows — dedupe first.** Measured by the draft writer, each id `grep -c -i` on `records/b42:BACKLOG.md` (vs `main`):
| Commissioned id | On `records/b42`? | Line | Action |
|---|---|---|---|
| `[B40-R1]` per-type staging + raw upload | yes (2 hits; 0 on main) | `:475` | **skip, already written** |
| `[B40-R2]` expire (Q-10) | yes (2; 0) | `:483` | **skip** |
| `[B40-R4]` overlay measure (lane A3) | yes (1; 0) | `:496` | **skip** |
| `[B40-R6]` admin screens | yes (2; 0) | `:514` | **skip** |
| `[B42-L2]` N-2 log line, needs Program.cs | yes (1; 0) | `:558` | **skip** |
| `[B42-L7]` N-11 markups source-set field | yes (1; 0) | `:596` | **skip** |
| `[B43-Q1]`…`[B43-Q6]` | **no** (`B43`, `IsEmptyStore`, `ReadRegistry`, `ReadCapped`, `reference-only`: 0 hits each) | — | **add** |
Re-run that check on your branch before writing (`grep -n -i '<id>'`); if anything changed, say where.

**Rows to add (six), under `## Deferred problems` after `[B42-R1]`**, in `[B42-L1]`'s shape (`records/b42:BACKLOG.md:548-556`): `- [ ] **[ID]** (gate B43 Q-n) summary`, then `Where` / `Symptom (gate's words)` (verbatim, `*"…"*`, cited `Briefs/2026-10-12_B43_STATUS.md` + section) / `Fix shape` (B43's HOW, verbatim) / `Why deferred` / `Jira` / `Discovered`.
- **Summaries are Friday's ticket summaries above without the `(gate B43 Q-n)` tail** for Q-1…Q-3; for Q-4…Q-6 the gate's own lead sentence (`:313`, `:319`, `:320`), verbatim.
- `Why deferred:` *round 2 of 2 of the B40/B41/B42/B43 cycle; the gate ruled GO WITH NOTES (B43 BLUF: "No Blocker and no Major, so the closed rows ship once CodeQL is green. Each residue gets a ticket under the two-NO-GO cap.")* (`B43_STATUS.md:44`; copy the line to its end).
- `Discovered:` *found by gate B43, 2026-10-12 (`B43_STATUS.md` Q-n); recorded by B44 seat R, 2026-10-12*.
| Row id | Source | Severity / origin | Jira line | Must also carry |
|---|---|---|---|---|
| `[B43-Q1]` | `### Q-1` `:281` | Minor, RESIDUE of M-2, PRE-EXISTING | the Q-1 key | B43's *"Mutant G13 … proves the fix shape"* line (`:289`) |
| `[B43-Q2]` | `### Q-2` `:292` | Minor, RESIDUE of M-2, PRE-EXISTING | the Q-2 key | *"This needs a rule choice from Friday on what "empty" means."*; cross-reference B43 `Q-10` (`:324`, the `.DS_Store` refusal) as one line |
| `[B43-Q3]` | `### Q-3` `:302` | Minor, INTRODUCED BY B42 | the Q-3 key | cross-reference `[B42-R1]` (both name `EngineRead`) |
| `[B43-Q4]` | `Q-4` `:313` | Note, INTRODUCED BY B42 | `none (Note)` | *"Only an Administrator gets that far, because the role check runs before the body read."* |
| `[B43-Q5]` | `Q-5` `:319` | Note, reachable only by mutant | `none (Note)` | *"No production path throws there"* sentence, verbatim |
| `[B43-Q6]` | `Q-6` `:320` | Note, test coverage (B42's tests) | `none (Note)` | the G1/G3/G15 counts, verbatim |
Q-7…Q-13, the N-20 gate correction and the N-2/N-8 measures (`:321-330`) are **not commissioned**: do not record them (list them under needs-Friday as "not recorded").

Commit message: `Records: gate B43 rows [B43-Q1…Q6] with Jira keys (B44)`.

**3b. history.md — four entries, newest at top, above the B33 entry**, in start-time order (B40 started first; B43 last), so the file reads B43, B42, B41, B40 from the top. Shape: B33's (`main:5_Project_History/history.md:3-12`): `## 2026-10-12 — B<n> SEAT-<x>: <one line> — <the STATUS last line>` then 3–7 bullets. **Every bullet is a fact copied from that STATUS, with its line cited at the bullet's end as (`B4n_STATUS.md:NN`)**; no new adjective, no claim the STATUS does not make. Start order proof: cite each STATUS's first timestamp or, where none, the brief file's mtime as `stat` prints it (draft writer read mtimes 06:02:28, 07:26:23, 08:10:36, 09:55:31 for the B40…B43 briefs; B42's brief was written while B41 ran, and B42 `:30` records read-only preparation until B41 finished).
| Entry | Heading's last part | Facts each entry must carry (source) |
|---|---|---|
| B40 SEAT-A | `READY FOR GATE: b40/source-lifecycle-admin-api 70c8172…` (`:679`) | base `4437460` (`:3`); DevStub only, off by default (`:7`); Items 1–5 DONE / NARROWED / API half (`:12-23`); suites 946 → 990, web 325 (`:24-25`); NOT DONE rows `[B40-R1]`…`[B40-R8]` (`:591-604`); records on `records/b40` (`:605-616`); branch pushed, main untouched (`:676-677`) |
| B41 SEAT-E | `READY FOR REVIEW` (`:686`), verdict `overall: NO GO` (`:684`) | M-1 Blocker, M-2 Major (`:7-9`); M-3, M-4 Minor (`:222`, `:229`); closure lines for -50 / -53 / -55 (`:25-29`); merge verdict NO GO (`:683`); no records, no Jira (`:4`) |
| B42 SEAT-B | `READY FOR GATE: b42/gate-b41-fix-round ab8fdf1…` (`:788`) | M-1…M-4, N-4, N-20 DONE; N-11 words DONE / field LEFT; N-2 moved to LEFT (`:13-21`); suites 990 → 1049 (`:24`); push of the branch only, 09:44:35 (`:85-87`); Entra-fake arm NOT DONE (`:695`); records on `records/b42` (`:718-728`) |
| B43 SEAT-E | `READY FOR REVIEW` (`:537`), verdict `overall: GO WITH NOTES` (`:19`) | M-1…M-4, N-4, N-20, N-11 words CLOSED (`:21-33`); Q-1, Q-2, Q-3 Minor and Q-4…Q-6 Notes (`:39-42`); MERGE fast-forward, merged tree `2826f027…` (`:18`, `:33`); B41 HELD re-sampled GO (`:16`) |
Add **one line to the B43 entry**, as Friday's and marked *(B44 records, from ITEM 1)*: `Merged as PR #27 → MPS main b28c95eb (tree 2826f027 = B43's merged tree); not deployed. Tickets <Q-1 key>, <Q-2 key>, <Q-3 key>.` with the values you measured. No other entry is touched; the entries missing for B34–B39 are **not** this round's (needs-Friday, one line).

Commit message: `Records: history entries B40–B43 (lane A2, PR #27) (B44)`.

## ITEM 4 — Jira: three "advances, not Done" comments (no transition)
**Per key:** (1) re-read (`GET …?fields=status,comment`): record status and the newest comment id; at drafting Friday has read none of these keys, so **all three values are UNMEASURED**. If a comment already carries this text (or names PR #27 / b28c95eb), SKIP and quote its id. (2) POST the line below verbatim, one ADF paragraph, no person named, with `<Qn>` replaced by the ITEM 2 keys (and `#27` / `b28c95eb` replaced only if ITEM 1 measured different values; say so). (3) read the comment back by id, byte for byte. **No transition, no field, label or link.**

- **MPSCALC-50:** `B40 + B42 (lane A2; gates B41 NO GO, B43 GO WITH NOTES): governed source versions, DevStub only and off by default: stage (one whole store document) → validate → atomic activate → rollback to a Superseded version; approved history unchanged; gate B41 M-1…M-4 fixed in B42. Merged as PR #27 → MPS main b28c95eb (tree 2826f027 = gated head ab8fdf1). Not deployed: hosted runs db8edfd. NOT DONE: per-type staging and raw upload [B40-R1], expire (Q-10) [B40-R2], hosted switch-on [B40-R3], importer checks in validate [B40-R7], a cross-process lock [B40-R8]; gate B43 residues <Q1>, <Q2>, <Q3>. Advances, not Done.`
- **MPSCALC-53:** `B40 + B42: the API half: GET /api/v1/admin/sources with real states and type/state filters, GET …/{versionId}, the lifecycle routes and GET /api/v1/admin/source-events, Administrator only; a value-free 500 backstop (SOURCE_LIFECYCLE_FAILED) on the seven source routes. Gates: B41 219/219 authZ cells, B43 re-sampled 219/219. Merged as PR #27 → MPS main b28c95eb (tree 2826f027). Not deployed. NOT DONE: the admin console screens [B40-R6]; template and audit admin are not in this lane. Advances, not Done.`
- **MPSCALC-55:** `B40 + B42: source-governance events (registered, staged, validated, failed-validation, activated, superseded, rolled-back) with actor, persona, roles, time, version and prior Active version; server-written, persisted, Administrator-only read. A store with documents but no registry.json now refuses the start instead of silently dropping them (B42 M-2; gate B43 CLOSED); a reference-only store still re-initialises (<Q2>). Merged as PR #27 → MPS main b28c95eb (tree 2826f027). Not deployed. NOT DONE: commercial and configuration change events beyond B35's; a cross-process lock [B40-R8]. Advances, not Done.`

(Sources for the wording: B40 `:12-23`, `:591-604`, `:623-625`; B41 `:7-29`; B42 `:13-21`; B43 `:10`, `:16`, `:25`; hosted `db8edfd` per C-21 and the B33 history entry `main:5_Project_History/history.md:3`.)

## ITEM 5 — Fold `records/b44` (= `records/b40` + `records/b42` + yours) into records `main`
1. After ITEM 3 is committed: root `git status --porcelain --untracked-files=no`. If it lists any path in `git diff --name-only main records/b44`, **STOP: NEEDS FRIDAY**. Re-measure the not-merged list (`for-each-ref` + `merge-base --is-ancestor` per `records/*`): if anything other than `records/b40`, `b42`, `b44` is unmerged, do not fold it; list it under needs-Friday. Never stash, checkout, switch, reset, `update-ref`, or `fetch . x:main`.
2. If `main` is an ancestor of `records/b44` (expected: `main` = `564f86d`, an ancestor of `records/b42`): `git -C <root> merge --ff-only records/b44`.
   Otherwise: `git -C <root> merge --no-ff records/b44 -m "Records: fold records/b40, b42, b44 into main (B44)"`. A conflict in `history.md` only may be resolved by keeping **both** sides' entries, newest at top, no word changed. Any other conflict: `git merge --abort`, then **STOP: NEEDS FRIDAY**.
   **Never rebase, never force, never cherry-pick.**
3. Read back: `git rev-parse main`; `merge-base --is-ancestor` rc 0 for `records/b40`, `records/b42`, `records/b44` against `main`; every `records/*` an ancestor of `main`; `main:BACKLOG.md` holds B40's 8 ids, B42's 8 ids and your 6 (count each `**[id]**`, `-i`: 1 each); `main:5_Project_History/history.md` holds 4 new `## 2026-10-12 — B4` headings (control: 0 on `564f86d`); `main:1_Project_Definition/CLARIFICATIONS.md` `### C-` count still **23**; root tracked status is what it was before step 2.
4. **Delete no branch and remove no worktree.**

## Ports
None needed: **bind nothing**.

## Leak + secret scan
Run B39's records scan (`.tools/qa-B39/tools/leak26.py`, `leakscan.py`, `qalib.py`, `adjud.py`: present at drafting; copy into `.tools/qa-B44/`, sha-equal; lists read-only by path; counts only; a positive control that fired) over `git diff 564f86d..records/b44`, the commit messages, the three ticket descriptions, the three Jira comment texts, and this STATUS before its last line. Plus `gitleaks` (present at `/opt/homebrew/bin/gitleaks`) with a planted control.
- Expected, to adjudicate, not to hide: the year `2026`; HTTP statuses `400`/`403`/`409`/`500`/`503`; `219/219`, `990`, `1049` and other counts; `Permission denied` in Q-1's quote. **Never print an avoid list.**

## STATUS sections
BLUF · ITEM 1 (merge facts as measured) · ITEM 2 (search table: term · count · keys; createmeta choices; created keys; links; read-back) · ITEM 3a (ids written; skipped + where) · ITEM 3b (four headings, start-order proof) · ITEM 4 table (key · re-read · comment id · read-back equal) · ITEM 5 (commands, before/after `main`, ancestry, root status before/after) · UNMEASURED · `## NOT DONE / NOT COVERED` · needs-Friday · Leak + secret scan · processes started/stopped · worktrees and files left.

## UNMEASURED (by the draft writer)
- **`b28c95eb`'s tree, parents and PR number:** not in the local clone (`origin/main` = `4437460` locally). ITEM 1 closes it.
- **Jira:** none of MPSCALC-50/-53/-55 was read at drafting; the board search was not run; the next free key, the issue types, the `Low` priority and the `Relates` link type are UNMEASURED. ITEM 2 and ITEM 4 step (1) close them.
- **Each seat's start time:** the B40 and B42 STATUS files carry no start clock; brief mtimes are a proxy only. ITEM 3b records what you read.
- **Whether Friday or another seat writes `records/*` or main before you run:** ITEM 5 step 1 re-measures.

## HOLDS
- Datasec only; no other client's names, tickets or paths.
- No product code; `2_Project_Files`: `fetch` and read verbs only. No checkout, switch, commit, branch or push there. CodeQL policy unchanged (this round pushes nothing).
- No deploy, no Azure, no setting change. **Nothing to any human**: three Jira tickets, their three links, and three Jira comments are the only outbound writes, and they name no person.
- **Own worktree:** `.tools/wt-B44-records` only. Do not commit in `wt-B40-records`, `wt-B42-records` or any other seat's worktree.
- **Never delete; quarantine** to `.tools/_quarantine/2026-10-12_B44_<what>/` (0700) and say so. No `branch -d/-D`, `worktree remove`, `gc`, `prune`.
- **Records:** write only `records/b44` (ITEM 3), the fold of `main` (ITEM 5) and your STATUS. `CLAUDE.md`, `JIRA.md` and `CLARIFICATIONS.md` are not touched. Existing BACKLOG rows and existing history entries are not edited; you only add.
- **Processes:** kill by port + cwd, never by name. Stop everything you started before the last line.
- **Instruments:** verdicts are ratios with denominators; every scanner zero and every Jira search zero has a positive control that fired; every grep for a phrase is `-i`.

## End
The last line of `Briefs/2026-10-12_B44_STATUS.md` is exactly one of:
- `RECORDS DONE: <one line>`;
- `STOPPED: NEEDS FRIDAY` and ONE question.
