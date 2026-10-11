From Friday (laptop seat), Datasec / HPSM-POC. Replies and wraps go to friday-laptop-agent@agentmail.to.

# BRIEF B222 (SEAT G): HPSM-POC RECORDS: one catch-up branch for 10-11/10-12 (four open records branches, ~18 briefs' files on no branch), Kam's twelve unrecorded 10-11 rulings as C-entries, the owed BACKLOG rows, two flake tickets
**From:** Friday (laptop seat), @NOW@ AEDT 2026-10-12. **Seat:** Datasec/HPSM-POC-G. Your commission is the newest `Briefs/` file containing `_SEAT-G_` (launcher `Launch_Claude.command:110`). The previous one, B199, is finished: `Briefs/2026-10-11_B199_STATUS.md` ends `RECORDS DONE`. Datasec / HPSM-POC only. Report to `Briefs/2026-10-12_B222_STATUS.md` (BLUF · FOUND · TESTED · HOW · NOT TESTED · PRIOR WORK · Records). **The last line is exactly `RECORDS DONE: <one-line>` or `STOPPED: NEEDS FRIDAY` followed by ONE question.**
**Tier:** records + Jira only. **No product code, no deploy, no setting, nothing on Azure, no hosted access.** Nothing pushed to any `main`.

**Records route (the B199 shape; read it yourself first).** The records repo is the project root: origin `git@github.com:datasecau/HPSM-POC-analysis.git`. `CLARIFICATIONS.md` is at `1_Project_Definition/CLARIFICATIONS.md`; `BACKLOG.md` is at the root; history is `5_Project_History/history.md`, newest at top. Work in your OWN worktree (`.tools/wt-b222`) built from a freshly fetched `origin/main`. Every ref write goes under the shared lock (`.tools/b198/lock.sh <cmd>`). Push ONE branch, `records/b222-catchup`, plainly (never force), and read it back with `ls-remote`. **Friday opens the PR and merges it after CodeQL and the checks.** (Precedent: `records/b199-catchup` landed as squash PR #111, then #112. origin/main = `47565b8` at drafting.)

**The root checkout is not yours.** The root is on local `main` = `76bb8ba`, which is 111 commits behind origin/main. It holds UNCOMMITTED edits to `BACKLOG.md` (+31 lines) and `5_Project_History/history.md` (+285 lines, measured against that stale base), and the untracked files listed in §4. Read them with plain reads (`cat`, `diff`, `git --no-optional-locks status`). Never run a git verb that writes there, and never edit, move or delete anything in it.

## 1. CLARIFICATIONS: Kam's 10-11 rulings that no C-entry records yet
**C-numbers (Friday's scan at drafting, `git show <ref>:1_Project_Definition/CLARIFICATIONS.md` on all 125 `refs/heads/records/*` plus main):** main ends at **C-83**. `records/b210` adds **C-84**. `records/b221` adds **C-85** and **C-86**. No ref holds C-87 or higher. **Next free = C-87.** Re-scan EVERY origin ref just before your commit. If any number from C-87 up has been taken, STOP (a duplicate is a stop, not a renumber).

**Already cited as AUTHORITY inside a deploy entry (write no new entry; name them in the STATUS table so Friday can mark them):** `hpsmpoc-tuesday-hosted-deploy-1011` (C-84, C-85) · `hpsmpoc-page-frame-names-for-demo-1011` (C-85) · `hpsmpoc-hosted-preview-shows-no-sample-data-1011` (C-86) · `hpsmpoc-hosted-reset-confirm-count-1011` (C-86). All four entries sit on unmerged branches (§4).

**Not in any CLARIFICATIONS on any ref.** Friday counted each card id with `grep -ci` on main, b210, b214, b217 and b221: every count was 0. `grep -ci alias` on main = 0. Write ONE C-entry per card, in ruled-time order: **C-87 … C-98**. Use the shape of C-84 (heading with the date, then `Authority, verbatim, as relayed in Friday's Briefs/2026-10-12_B222_SEAT-G_records-catchup-1011.md`).
- **Channel:** Kam's live decision board, as read by Friday from his decision register (`decision_queue.sh show <id>`, read at drafting).
- **Time:** the register's `ruled_ts`. Friday's reconcile writes it, and it can trail Kam's click by up to ~30 s. Friday's daily note logs "live board 12:49:46–12:50:09" for the first three. Quote the `ruled_ts`.
- **Quote** the title and the chosen option's label + detail exactly as below.
- **Where it was BUILT or DEPLOYED:** cite a file:line in the STATUS or CLARIFICATIONS that shows it. If none shows it, write "not established". Never claim more than that file shows.

| C | card id | ruled_ts (AEDT) | title, verbatim | choice: label, verbatim / detail, verbatim |
|---|---|---|---|---|
| C-87 | `hpsmpoc-ranges-vs-exact-1011` | 2026-10-11T12:49:38 | "Organisation size and device count: store exact numbers or ranges only?" | **a** "Keep exact, show ranges to HP" / "Derive ranges for anything HP sees; cheap, loses nothing." |
| C-88 | `hpsmpoc-device-identifiers-1011` | 12:50:15 | "Device serials, IPs and MACs from the SM/FTA imports vs HP's anonymisation principles" | **b** "Drop or hash identifiers at import" / "Keep firmware version, model and counts; before any real customer upload." |
| C-89 | `hpsmpoc-customer-names-alias-1011` | 12:50:18 | "HP says avoid storing customer company names: keep names, alias them, or replace them?" | **a** "Keep names; alias wherever data leaves the partner" / "ORG-nnnnn on anything HP or an export sees." (This is "the standing ruling" that gate B220 N-5 measures against.) |
| C-90 | `hpsmpoc-revenue-source-1011` | 12:50:22 | "Where would attributed revenue come from, and how is a masked customer joined to HP's records?" | **b** "Partners report their own wins" / "Easy to build, low trust as a measure of influence." |
| C-91 | `hpsmpoc-attribution-demo-tuesday-1011` | 12:50:47 | "Show anything for attribution at Tuesday's HP review (13 Oct)?" | **c** "A live dashboard on seeded data" / "More work, and breaks the freeze." (Shaped by C-95.) |
| C-92 | `hpsmpoc-attribution-phase-1011` | 12:51:21 | "Steve's revenue attribution (Paul's five metrics): this POC or the next phase?" | **a** "Next phase; roadmap now" / "The map becomes the roadmap entry; nothing built." (Shaped by C-95.) |
| C-93 | `hpsmpoc-industry-prioritise-1011` | 12:51:24 | "Should the customer's industry change scoring or priorities, or only be shown?" | **a** "Display only for now" / "As built; revisit after HP's review." |
| C-94 | `hpsmpoc-industry-words-1011` | 12:52:28 | "Industry list wording: HIPAA for Australian healthcare, and which other industries name a framework?" | **a** "Keep as built" / "HIPAA and PCI DSS only; the rest blank; the hint as written." (The card recommended b. Record that Kam chose a.) |
| C-95 | `hpsmpoc-tuesday-dashboard-vs-next-phase-1011` | 12:54:08 | "Two of your rulings meet: a live attribution dashboard for Tuesday, but attribution itself is next phase. Which shape?" | **b** "Preview plus the keys" / "As (a), and the engagement id, partner id and revenue category added to the data model now (no revenue yet)." Option (a)'s detail, which (b) includes, verbatim: "A separate page labelled 'Preview: next phase', on seeded data; no new data model; real attribution stays next phase." |
| C-96 | `hpsmpoc-import-kept-files-identifiers-1011` | 14:20:10 | "Uploaded import files still hold device identifiers: what should be stored?" | **b** "Store a cleaned copy instead (recommended)" / "The stored CSV has the identifier cells blanked, so a file is still kept as evidence but holds no identifier. Needs a second hash column (or a redefined hash) and a one-line contract change. One build round plus a gate, before any real customer upload." |
| C-97 | `hpsmpoc-made-before-the-keys-customers-1011` | 16:30:59 | "Customers created before today's change will show 'No alias' until the demo data is reset" | **c** "Leave it; the note explains it" / "HP may see 'No alias (made before the keys)' rows." **Superseded in effect** by `hpsmpoc-hosted-preview-shows-no-sample-data-1011` = a (20:51:35), whose card says *"you ruled 'leave them' (c) at 16:30:34 … on a card whose text did not say the preview would show no sample data; this card corrects that premise."* Record both: supersede, never delete. C-84 already paraphrases this ruling as "Kam's ruling (c)" without the card id. |
| C-98 | `hpsmpoc-demo-names-beyond-the-frame-1011` | 20:51:31 | "After the frame alias, a Demo login still sees customer names in page headings and the executive PDF" | **b** "Alias the headings AND the executive PDF for Demo (recommended)" / "As (a), plus the PDF a Demo user downloads names the customer only by alias, in its pages and its file name. The PDF is the clearest case of data leaving the partner; it is a bigger round." |

The register shows no HPSM-POC card ruled on 2026-10-12, and no other HPSM-POC card ruled on 10-11. **STATUS:** a table with card id → C-number (or "cited in C-8x"), so Friday can mark each card `--delivered`.

## 2. BACKLOG rows (`BACKLOG.md` on `records/b222-catchup`; one row each in the file's own shape: Where / Symptom / Why deferred / Discovered, plus the source file:line)
Copy each gate's own wording; do not paraphrase. Friday's line numbers are from the root's untracked files, read at drafting. Re-read them yourself.
- **Gate B211 (of B206), the notes still open:** N-3 (`B211_STATUS.md:80`) and N-4 (`:87`). Gate B218 says *"N-3 and N-4 (B211's) are open by design this round"* (`B218_STATUS.md:275`). N-1, N-2 and N-5 were built by B213 Row 2 (`B218_STATUS.md:7`): name them as DONE, and add no row for them. Also note B205 N-1 (log capture), which B211 says is *"still open"* (`B211_STATUS.md:285`). Search BACKLOG and Jira for it first.
- **Gate B212 (of B208), N-1 (`B212_STATUS.md:49`) and N-2 (`:55`).** Gate B220 item 7 reports both re-made after B215: w5 (B212 (e)) went 3 red, w4 (B212 (h)) went 1 red (`B220_STATUS.md:106-107`). If that holds when you read it, record them as rows already ticked `[x]` with that evidence. If it does not, record them as open rows.
- **Gate B218 (of B213):** m-1 (`B218_STATUS.md:94-100`: Row 1's upper bound absorbs product-caused delay inside an injected wait) and N-4 (`:123-128`). For N-4, use the gate's own fix-shape: a brief that grants contract prose also grants `web/src/api/contract-drift.test.ts`, or says "no version bump for prose".
- **Gate B220 (of B215 + B219):**
  - M-1 (`B220_STATUS.md:40`, the Demo PDF name check matches the WHOLE name only)
  - M-2 (`:47`, a refused Demo copy reaches the person as raw JSON or a silent failed download)
  - N-1 (`:54`) and N-2 (`:55`), surviving mutants g2 and ord
  - N-3 (`:56`)
  - N-4 (`:57`, partners see "Customer" for a moment). It is marked "for Kam's eye".
  - N-5 (`:58`, `getAssessmentResult` names the customer to Demo). Record it as a disclosure against C-89.
  - N-6 (`:59`, the four 409 reasons are missing verbatim from B215's NEW WORDS)
  - S-N2 (`:63`, 90 s does not cover an EF retry of the whole reset)
  - Friday's addition: S-N1 (`:62`), from the same file.
- **B217 / B221 OPEN items:**
  - **(a) Possible orphan PDF in Blob** from the rolled-back reset (`B217_STATUS.md:126`, and `:12`). Still open per `B221_STATUS.md:162` and `:179`. It is a NEW row. `records/b217`'s first row mentions it only inside a symptom.
  - **(b) The "It may still finish, so reload the page in a minute" wording** is false for the reset. B217 already has a row (`records/b217` BACKLOG). Add to it, do not duplicate: gate B220 found the sentence still on the B219 head (`B220_STATUS.md:162`, `AppShell.tsx:63` + `client.ts:288`).
  - **(c) Event 3211 at cold start.** B221 already has a row (`records/b221` BACKLOG). Add nothing beyond a link to the flake ticket from §3.
  - `records/b217`'s first row (the reset cannot finish inside 30 s) was answered by B219's 90 s (#142), deployed in C-85, and the reset then completed in 9,788 ms (C-86). Tick it `[x]` with that evidence. Never delete it.
- **The two `HostedDemoSlowFirstLoginTests` timing flakes:**
  - (i) `A_first_read_whose_retry_also_times_out_warns_once_after_exactly_one_retry`: red on main CI run 38148442673, attempt 1 (`B221_STATUS.md:18`). Its row is already on `records/b221`.
  - (ii) `Only_a_first_login_that_timed_out_is_retried`: red once in B213's base load copy, *"Expected: -2 Actual: 258"* (`B213_STATUS.md:102`). This is a NEW row, and B221's row already names it as the same class.
  - Each row cites its §3 ticket key.
- **Rows that exist only in the root's uncommitted `BACKLOG.md`:** "Follow-ups from B202 (Seat B, 2026-10-11)" and "Follow-ups from B208 (Seat A, 2026-10-11)". Origin main's BACKLOG ends with B199's rows. COPY those two sections in verbatim. The root's B221 section should equal `records/b221`'s. Confirm that with a diff and copy it only once.

## 3. Jira (seats write the tickets their brief names: `Launch_Claude.command:95`, B199 precedent). Read-only searches first; quote every query and its count in the STATUS.
- **Flakes:** `project = HPSMPOC AND text ~ "HostedDemoSlowFirstLogin"` = **0**, and `… "HostedDemoSlowFirstLoginTests"` = **0** (Friday, at drafting). `… "Only_a_first_login_that_timed_out_is_retried"` = 1, HPSMPOC-207. That ticket is the seed-lock / start-up retry ticket, which names this test as a guard. Read its 6 comments, then say whether any of them treats it as a flake. If all searches are still 0 and 207 does not treat it as a flake, **file ONE HPSMPOC ticket per flake**, as Friday's brief asks: two, linked to each other and to HPSMPOC-207. Use BLUF · Recommendation · Detail, and quote the test name, the run, and the verbatim error from the STATUS files above. Do not loosen any bound and do not suggest a number. B221's row says the test's owner must find the cause first.
- **Comments on work closed or advanced:** `text ~ "B208"`, `"B213"`, `"B215"`, `"B219"` = **0 each** (Friday, at drafting). No B208, B215 or B219 brief or STATUS names a ticket (`B208_STATUS.md:182`, `B215_STATUS.md:226`, `B219_STATUS.md:10`). B213's brief names HPSMPOC-232, -238, -246 and -247 only as search results that are "not this test" (`B213_SEAT-D…md:53-55`). So: **post a comment only on a ticket the work's own brief or STATUS ties it to**, BLUF-first: what merged (PR number), what was deployed (C-85), and what was measured. Where no ticket exists, post nothing and create nothing. Put the one-line comment you would have written in the STATUS for Friday. Read each ticket's newest comments before you post, and do not duplicate them.

## 4. Fold the open records into `records/b222-catchup`
**Open records branches (Friday's `ls-remote` + `rev-list`, at drafting; behind = 0 on origin/main `47565b8`, so no merged PR yet):**

| branch | commit | what it adds |
|---|---|---|
| `records/b210` | `f51f927` | C-84, B210 files, history |
| `records/b214` | `d95ecff` | B214 files, history; no C |
| `records/b217` | `4fad607`, `946300d`, `33eada9` | saved records, B217 files, BACKLOG, history |
| `records/b221` | `cbae1c4` | C-85/C-86, B221 files, BACKLOG, history |

Every other `records/*` branch is behind main and was landed by squash (B199 classified them up to b198). **Gates B211, B212, B218 and B220 have NO records branch.**

**Files on no branch (untracked in the root, `git --no-optional-locks status`; 0 hits on `ls-tree origin/main` for B200–B209):** brief + STATUS + evidence (+ addenda) of **B200, B201, B202, B203, B204 (incl. `B204_R2_STATUS.md`), B205, B206, B207, B208, B209, B211, B212, B213, B215, B216, B218, B219, B220**. That is about 1,100 files and ~45 MB; Friday found none over 5 MB. Also included: `B200_ADDENDUM-1…`, `B204_ADDENDUM-1…`, `B207_ADDENDUM-1…`, `B215_SEAT-A_ADDENDUM-1…`, `B210_ADDENDUM-1…` (b210 already has the last). Check each against the branches before copying: same blob = skip it, and name it.

**Do:**
1. Cherry-pick, in this order: b210, b214, b217 (three commits), b221. Resolve conflicts ADDITIVELY:
   - `CLARIFICATIONS.md`: C-84 → C-85 → C-86, each once. b210 and b221 both insert at line 935, so the conflict is certain.
   - `history.md`: keep every entry, newest at top. All four branches insert at the same top hunk (`@@ -1,5`). Order the entries by their heading's start time: B221 01:45 (10-12) · B217 ADDENDUM-1 22:55 · B217 22:14 · B214 21:09 · B210 17:10.
   - `BACKLOG.md`: both sections (B217's, B221's), each once.
   - Nothing a branch added is dropped.
2. COPY (never move) the no-branch files above into the same paths.
3. Merge the root's uncommitted `history.md` entries. Compare them against the folded file by HEADING, not by diff: the root diff is against the stale `76bb8ba`, so most of its "+" lines are already on main. Add only the headings that are missing (Friday expects B200–B209, B211–B213, B215, B216, B218–B220), each verbatim, in start-time order.
4. Then add §1's C-87…C-98, §2's rows, and your own history entry.
5. Before pushing:
   - gitleaks on every staged path, with a random canary that must be caught.
   - A content check for the HOLD below. Print counts only, never the matched text.
   - Assert that every source branch's added files are present and blob-equal on your branch, or name the ones that differ.
   - Then push `records/b222-catchup` only.
6. **Never delete a branch, a worktree or a file.** The four source branches stay on origin.

## HOLDS
- **No HP Restricted document (the executive deck, the financial model, anything HP marks Restricted) is given to ANY AI tool without HP's written approval (signed SOW §4.1.4(c)).** If a no-branch evidence folder holds one, leave it out, name it in the STATUS, and STOP.
- Datasec only. No other client's names, tickets or paths anywhere.
- CodeQL policy: push your branch only. Never push to main, never dismiss an alert, never ask for a bypass.
- **Nothing to HP or any human.** No mail except your wrap to Friday. Jira comments are BLUF-first and say what was measured and how.
- Never delete; quarantine. **Never edit a running script.** Use your own worktree. Processes you start are stopped by PID, after a cwd check.
- If a measurement contradicts this brief, the measurement wins. Say so in the STATUS, and STOP if it changes what you would do.
