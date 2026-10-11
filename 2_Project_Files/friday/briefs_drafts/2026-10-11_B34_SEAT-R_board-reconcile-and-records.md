From Friday (laptop seat), Datasec / MPS Commercial Calculator
# BRIEF B34 · SEAT-R — apply the board reconcile (8 Done moves), fold the records branches into records main, record Kam's 2026-10-11 rulings as C-14 onward
**Written:** ~16:5x AEDT 2026-10-11 (draft; Friday times it at firing). **Pane:** `Datasec/MPS-R`. Your commission is the newest file in `Briefs/` containing `_SEAT-R_`.
(Launcher check, read by the draft writer: `Launch_Claude.command:107` sets `SEAT` from a pane name matching `*MPS*-?`, and `:111` tells the seat its commission is "the NEWEST brief in 1_Project_Definition/Briefs/ whose file name contains _SEAT-${SEAT}_". At drafting, 0 files in `Briefs/` contain `_SEAT-R_` (`ls | grep -c`; control `_SEAT-B_` = 9), and `tmux list-panes -a` shows no MPS pane.)
**Seat:** Seat R (Claude records seat). **No product code.** One records branch, Jira writes as listed, nothing else.
**Report:** `1_Project_Definition/Briefs/2026-10-11_B34_STATUS.md`. No mail key in this project, so your STATUS file is the wrap.
Its last line is exactly one of:
- `READY FOR REVIEW — records main @ <sha>`, with `<sha>` read back by `git rev-parse main` in the records repo after the fold;
- `STOPPED: NEEDS FRIDAY` and one question.

## AUTHORITY
- **Friday commissions this round** from the reconcile `2026-10-11_mpscalc_board_reconcile.md` (Friday's drafts; its text that you need is quoted below, so you do not need the file). Friday's reconcile is not a Kam ruling. The Jira moves are housekeeping of shipped work: no ticket in this brief needs Kam's word.
- The C-entries record rulings Kam already made. Their verbatim text is quoted in ITEM 3 from Friday's board file. **Do not compose any wording inside a quote.**

## READ WHOLE FIRST
- The project `CLAUDE.md`, `JIRA.md`, and `1_Project_Definition/CLARIFICATIONS.md` **as it stands on `records/b30`** (`git show records/b30:1_Project_Definition/CLARIFICATIONS.md`). The root working copy is behind it (it ends at C-11; reconcile, Notes).
- `Briefs/2026-10-11_B30_STATUS.md` § ADDENDUM-2 (how the last records seat used a records branch with no remote) and `Briefs/2026-10-10_B21_*` records precedent.
- `Briefs/B31_ADDENDUM-1_approver-upn-domain.md` (the approver-account name, C-20).

## ITEM 1 — Jira: apply the reconcile's 8 Done transitions
**Keys (8):** MPSCALC-21, -22, -37, -38, -39, -56, -86, -89. At drafting, all 8 read `status=Backlog` (Jira REST `GET /rest/api/3/issue/MPSCALC-<n>?fields=status`, read-only, ~16:4x AEDT).

**Credentials (measured, names only):** `4_Credentials/.env` holds `JIRA_BASE_URL`, `JIRA_EMAIL`, `JIRA_API_TOKEN` (read by the draft writer with `sed -E 's/=.*//'`; values not read into any file). `JIRA.md` records that every earlier MPS seat (B01–B03) used these three. Use them through a small helper that reads the file and sends Basic auth. **Never print, log or write the token**, and never pass it on a command line.

**Evidence check at origin main, before any write.** In `2_Project_Files`: `git fetch origin`, then `git ls-remote origin refs/heads/main`. At drafting it was `db8edfd5082e49f9a1a1b3c23feeb02b36834b21` (ls-remote, and `friday_as.sh datasec gh api …/commits/main`, ~16:4x AEDT). For each key, the evidence **holds** only if all its rows below pass at the main you measured; otherwise **SKIP that key** and say which row failed.

| Key | Evidence rows to re-measure (all must pass) |
|---|---|
| 21 | `merge-base --is-ancestor 7be7e37 <main>`; `git grep -c FleetLineResult <main> -- src/MpsCalc.Engine` ≥ 1 |
| 22 | `7be7e37` ancestor; `git grep -c MonthlyFinance <main> -- src/MpsCalc.Engine` ≥ 1 |
| 37 | `7be7e37` ancestor; `git grep -c SoftwareLine <main> -- src/MpsCalc.Engine` ≥ 1 |
| 38 | `7be7e37` ancestor; C-10 present on `records/b30` CLARIFICATIONS |
| 39 | `7be7e37` ancestor; `git grep -n 'AUTH MANAGER REQUIRED' <main> -- src/MpsCalc.Engine/Calculation/WorkbookRules.cs` (drafting: `:47`) |
| 56 | `9fe66dc` and `98d829f` ancestors |
| 86 | `7be7e37` ancestor; `git grep -n 'Release1' <main> -- src/MpsCalc.Engine/Currency/CurrencyRegistry.cs` (drafting: `:28`) |
| 89 | `774b82d` ancestor |
| all | `db8edfd` is `<main>` or an ancestor of it (the comments name `db8edfd`); `Briefs/2026-10-11_B33_STATUS.md` still carries `DEPLOYED: db8edfd5082e49f9a1a1b3c23feeb02b36834b21 live-check 0` |

Drafting read (`merge-base --is-ancestor … db8edfd`, `--no-optional-locks`): 7be7e37, 9fe66dc, 98d829f and 774b82d are all ancestors of db8edfd; every grep above hit.

**Per key, in this order:** (1) re-read the issue (`GET …?fields=status,comment,summary`); if it is already Done, or a newer comment says "not Done" for a reason the reconcile did not see, SKIP and quote that comment's id; (2) post the comment below, **verbatim, one line, no mention of any person**; (3) `GET /transitions` and apply the transition whose target status is `Done`; (4) read back the status and the comment by its id. Record all four results per key in STATUS.

Comment text, verbatim from the reconcile (do not edit):
- **MPSCALC-21:** `Reconcile 2026-10-11: SHIPPED. R-04…R-15 in QuoteCalculator.FleetLineResult, PR #1 (7be7e37), in main db8edfd, deployed (B33 STATUS: DEPLOYED db8edfd live-check 0).`
- **MPSCALC-22:** `Reconcile 2026-10-11: SHIPPED. Annuity R-09 (MonthlyFinance) and recommended base R-10, PR #1 (7be7e37), in main db8edfd, deployed (B33).`
- **MPSCALC-37:** `Reconcile 2026-10-11: SHIPPED. Term-SKU resolution S-01/S-02 (QuoteCalculator.SoftwareLine), PR #1, in main db8edfd, deployed (B33).`
- **MPSCALC-38:** `Reconcile 2026-10-11: SHIPPED. Software sell/cost S-03/S-04, PR #1; margin treatment ruled C-10 (parity, keep MARGIN REVIEW); in main db8edfd, deployed (B33).`
- **MPSCALC-39:** `Reconcile 2026-10-11: SHIPPED. AUTH MANAGER REQUIRED rule S-05 (WorkbookRules), PR #1, in main db8edfd, deployed (B33).`
- **MPSCALC-56:** `Reconcile 2026-10-11: SHIPPED. Entra SSO API PR #11 (9fe66dc) + web PR #12 (98d829f); hosted showcase signs in with Entra (B14 ADDENDUM-7); in main db8edfd, deployed (B33).`
- **MPSCALC-86:** `Reconcile 2026-10-11: SHIPPED. Currency model per ADR-001, AUD only (CurrencyRegistry.Release1), PR #1 (7be7e37), in main db8edfd, deployed (B33). FX and next currencies stay on MPSCALC-87/-88.`
- **MPSCALC-89:** `Reconcile 2026-10-11: SHIPPED. Importer rules merged as PR #3 (774b82d), so the "not Done until merged" condition of the 2026-10-01 comment is met; hosted reference store read-back MATCH (B33).`

**Not in scope (do not touch):** the six UNSURE rows (18, 20, 51, 52, 54, 57), the close-candidates 66, 81, 84 (Kam's), every epic, and every other key. Create no issue. No other comment, field, label or link.

## ITEM 2 — Records: fold `records/b12`, `b21`, `b25`, `b30` into records `main`
The records repo is the **project-root** git repo (not `2_Project_Files`).

**Measured by the draft writer (read verbs only, `--no-optional-locks`):**
- `git remote -v`: **empty** (rc 0). No remote: nothing is pushed anywhere in this item.
- `main` = `7773456843aa5a96406066209d93f2bc967af3ab`. Branches: `records/b12` `0857d54`, `records/b21` `7d13ba0`, `records/b25` `e8b1973`, `records/b30` `e9db892`, each checked out in its own worktree `.tools/wt-B{12,21,25,30}-records`.
- `merge-base --is-ancestor main records/bNN` = yes for all four. `git log --oneline main..records/b30` = exactly 4 commits, one per branch, in a line: main → b12 → b21 → b25 → b30. So **one fast-forward of main to the tip carries all four.**
- `git diff --stat main records/b30` = 3 files: `1_Project_Definition/CLARIFICATIONS.md` (+47), `5_Project_History/history.md` (+13), `BACKLOG.md` (+146 −2).
- **The blocker:** `main` is checked out in the **root** worktree, and the root holds **uncommitted** work: `M 5_Project_History/history.md` (`git diff --stat main -- 5_Project_History/history.md`: +329), plus 104 untracked files (mostly `Briefs/`). The fold changes `history.md` too, so a fast-forward in the root would collide with that edit.

**PRECONDITION — RULED BY FRIDAY AT FIRING:** Friday does not write into a project tree (hard rule 1), so YOU settle it, as your FIRST records step. Read `git -C <root> diff main -- 5_Project_History/history.md` whole. If it holds only history entries from earlier seats (no secret: run `gitleaks` on the diff with a positive control, no non-history text), commit exactly that file on `main` as its own commit, unchanged, with the message `Records: commit pending history entries left uncommitted by earlier seats (B34)`. Then fold. The 104 untracked files stay untouched. If the diff holds anything else, STOP and say what.

**Steps:**
1. `git worktree add .tools/wt-B34-records -b records/b34 records/b30` (`chmod 700`). ITEM 3 commits go here.
2. After ITEM 3 is committed, in the **root**: `git status --porcelain --untracked-files=no`. If it lists any path in `git diff --name-only main records/b34`, **STOP: NEEDS FRIDAY**. Never stash, checkout, switch, reset, `update-ref`, or `fetch . x:main`.
3. If `main` is an ancestor of `records/b34`: `git -C <root> merge --ff-only records/b34`.
   Otherwise (Friday committed on main first): `git -C <root> merge --no-ff records/b34 -m "Records: fold records/b12, b21, b25, b30, b34 into main (B34)"`. A conflict in `history.md` only may be resolved by keeping **both** sides' entries, newest at top, with no word changed. Any other conflict: `git merge --abort`, then **STOP: NEEDS FRIDAY**.
   **Never rebase, never force, never cherry-pick.**
4. Read back: `git rev-parse main`; `merge-base --is-ancestor records/bNN main` = yes for b12, b21, b25, b30, b34; `git show main:1_Project_Definition/CLARIFICATIONS.md | grep -i -c '^### C-'` (expect 14 at b30 plus the new ones; control: the same count on `records/b30`); `git status --porcelain --untracked-files=no` in the root is what it was before step 3, except the merged paths.
5. **Delete no branch and remove no worktree.**

## ITEM 3 — CLARIFICATIONS C-14 onward (on `records/b34`)
**First check:** `git show records/b30:1_Project_Definition/CLARIFICATIONS.md | grep -i -c '<card id>'` for each card id below. If one is already recorded, skip it and say where. At drafting the file ends at **C-13** (`grep -i '^### C-'`: C-01…C-13 and C-06a), and the reconcile found none of these recorded.

**Shape:** C-13's: a `### C-NN — <title>` heading, then the source line, the verbatim quote(s), and a line marked **Friday's reading, not Kam's words** only where one is quoted below. The heading text is the card's `title`, verbatim. Every entry carries its **card id** and **timestamp**.

**Source, read by the draft writer:** FRIDAY `0_Brain/dashboard/data/decisions.json` (a Friday file outside this project; **do not open it**: the lines you need are quoted here). Fields used: `id`, `title`, the ruled option's `key`, `label` and `detail`, `default_action`, `ruled_choice`, `ruled_ts`, and `delivered_artefact` where present. The **board-log** time (the moment Kam tapped, as relayed in an MPS brief's AUTHORITY) is a few seconds earlier than `ruled_ts`; record both, as below.

Order: by board-log time.

**C-14 — card `mpscalc-new-words-hosted-deploy-1011`**
- title: *"Ship last night's calculator fixes to the hosted site? Approve the new wording first"*
- `ruled_choice` **a**, `ruled_ts` `2026-10-11T06:49:22.071844+11:00`; board-log 06:48:47 (`Briefs/2026-10-11_B31_SEAT-C_…:23`, verbatim: *"Decision mpscalc-new-words-hosted-deploy-1011: a — Approve the wording and deploy"*).
- option a: *"Approve the wording and deploy"*: *"A deploy seat ships main 4f27f55 to the same hosted URL, code only. Friday runs the gates' post-deploy checks herself and tells you the result."*
- `delivered_artefact`: *"hosted showcase runs main 4f27f55 (B31 PART A: deploy + check rc 0; Friday's live check 07:0x)"*, `delivered_ts` `2026-10-11T07:14:33.463652+11:00`.

**C-15 — card `mpscalc-new-quote-form-1010`**
- title: *"'New quote' makes a record straight away: add a short form first?"*
- `ruled_choice` **a**, `ruled_ts` `2026-10-11T06:49:24.114409+11:00`; board-log 06:48:56 (`Briefs/2026-10-11_B30_SEAT-B_…:14`).
- option a: *"A short form first (type, term, customer)"*: *"Web only; no record exists until you fill it in."*
- default action: *"a: Friday's seat builds the form through a QA gate; nothing deployed until you have seen it."*

**C-16 — card `mpscalc-markup-precedence-1010`**
- title: *"When a catalogue item has its own markup, which markup wins?"*
- `ruled_choice` **b**, `ruled_ts` `2026-10-11T06:49:26.214451+11:00`; board-log 06:49:01 (B30 brief `:15`).
- option b: *"Keep the order, show it before calculating"*: *"Each line shows its effective markup and where it comes from (catalogue or section) before you calculate."*
- default action: *"b: Friday's seat builds it through a QA gate; no pricing rule changes; nothing deployed until you have seen it."*
- **Friday's reading, not Kam's words** (B30 brief `:17`, verbatim): *"Friday's reading of G-4 "before calculating": shown after the draft is SAVED and before Calculate is pressed, with a pending marker for unsaved edits (below). This is Friday's reading, told to Kam; his word corrects it."*

**C-17 — card `mpscalc-accessory-fits-device-1010`**
- title: *"Accessories: show which device each one fits, and flag a wrong one?"*
- `ruled_choice` **b**, `ruled_ts` `2026-10-11T06:49:28.359754+11:00`; board-log 06:49:08 (B30 brief `:16`).
- option b: *"Picker + a warning on the quote"*: *"As (a), plus a review warning when a line's accessory fits no device in its section. Engine + contract change, gated like everything else."* Option a, which b includes: *"The picker shows 'Fits <model>', lists each option once, and offers the section's device options first. A wrong pick can still print."*
- default action: *"b: Friday's seat builds it and it goes through a QA gate; nothing is deployed until you have seen the new words and screens."*

**C-18 — card `mpscalc-second-approver-for-kam-test-1010`**
- title: *"Your test quote cannot be approved by you alone: add a second approver account?"*
- `ruled_choice` **a**, `ruled_ts` `2026-10-11T06:49:30.463186+11:00`; board-log 06:49:15 (`Briefs/2026-10-11_B31_SEAT-C_…:28`).
- option a: *"Friday's seat creates a second sign-in account with the Approver role only"*. Record **only the label**: the card's `detail` names an example address that B31 ADDENDUM-1 calls *"Friday's drafter's composed value, not Kam's"*; C-20 records the real name.

**C-19 — card `mpscalc-hosted-edit-survives-restart-1010`**
- title: *"Prove a catalogue edit survives a restart on the hosted calculator"*
- `ruled_choice` **b**, `ruled_ts` `2026-10-11T06:50:23.886832+11:00`; board-log 06:49:56 per the B30 brief `:18` (that line paraphrases, so cite it as a time, not as a quote).
- option b: *"Let your test quote on Monday cover it"*: *"Your full test quote will include price edits; tell me when you have done them and I restart and check then."*
- Not settled: persistence on the hosted site is still unproven until that check (record this as fact, not as Kam's words).

**C-20 — the B31 approver-account name (Friday's answer under C-18, not a Kam ruling)**
- Source: `Briefs/B31_ADDENDUM-1_approver-upn-domain.md`, Friday, 07:08 AEDT 2026-10-11, verbatim: *"Create the account as `mps-approver@kamildatasecrd.onmicrosoft.com`, everything else exactly as the brief says (Approver role only; …)"* and *"The `datasec-rd.com` UPN was Friday's drafter's composed value, not Kam's: his ruling (06:49:15) is "a second sign-in account with the Approver role only" and names no domain. Your `GET /domains` read is the authority for the domain."*
- Card `mpscalc-second-approver-for-kam-test-1010` `delivered_artefact`, verbatim: *"Entra user mps-approver@kamildatasecrd.onmicrosoft.com (0cc6dece…), exactly 1 assignment = Approver (B31 ADDENDUM-2, assignment zt7GDL…); password in MPS 4_Credentials 0600"*, `delivered_ts` `2026-10-11T07:14:35.113189+11:00`.
- Mark the heading clearly as **Friday's determination**. Write no password, no full object id, and no other mailbox.

**C-21 — card `mpscalc-b30-new-words-hosted-deploy-1011`**
- title: *"Your three new calculator features passed QA: approve their wording and put them on the hosted site?"*
- `ruled_choice` **a**, `ruled_ts` `2026-10-11T10:23:20.966418+11:00`; board-log 10:22:57 (`Briefs/2026-10-11_B33_SEAT-C_…:7`, verbatim: *"Decision mpscalc-b30-new-words-hosted-deploy-1011: a — Approve the wording and deploy"*).
- option a: *"Approve the wording and deploy"*: *"A deploy seat ships main db8edfd to the same link, code only; Friday checks it live and tells you."*
- `delivered_artefact`: *"hosted showcase runs main db8edfd (B33: check rc 0, 48/48; Friday's live check 10:4x)"*, `delivered_ts` `2026-10-11T10:36:27.250887+11:00`.

One commit on `records/b34` for all of ITEM 3. Message: `Records: C-14…C-21 (Kam's 2026-10-11 card rulings; B31 approver-account name) (B34)`.

## ITEM 4 — BACKLOG B27-H1…H4: suggested Jira homes (a list for Friday; nothing created)
These four rows are on `records/b30` `BACKLOG.md` (`grep -n -i 'B27-H[1-4]'`: `:224`, `:242`, `:255`, `:274`; the hosted-path HOLD is at `:17`). They are not on the board (reconcile lane A3). For each, give in STATUS: the row id, its one-line summary (quoted from BACKLOG, not reworded), the **parent epic** it would sit under (the reconcile's lane A3 implies MPSCALC-11 or -14: say which and why), and whether an existing key already covers it. **A new key's number is assigned by Jira when it is created**, so any `MPSCALC-9x` you write is a guess and must be labelled as one. **Create nothing on Jira; edit no BACKLOG row.**

## Ports
**6640–6649**, reserved for B34 only. This round needs no listener: **bind nothing**. Friday checked at ~16:4x: `lsof -nP -iTCP -sTCP:LISTEN` shows 5000, 7000, 7768, 42050 and five ports at 49152 or above (none in 66xx/67xx); `grep -rhoE '\b6[5-7][0-9]{2}\b' Briefs/` names 6581, 6590, 6593, 6599 and 6600–6609 only (0 in 6610–6799).

## Leak + secret scan
Run the B30 ADDENDUM-2 records scan (lists read-only, counts only, positive control that fired) over `git diff records/b30..records/b34`, the commit message, and this STATUS file before you write the last line.
- Expected and to adjudicate, not to hide: the `kamildatasecrd.onmicrosoft.com` address in C-20 (the e-mail class fires once). Never print an avoid list.

## STATUS sections
- BLUF;
- ITEM 1 table: key · evidence result · comment id · transition id · status read back (or SKIP + why);
- ITEM 2: the commands run, before/after `main`, the ancestry read-back, and the root status before and after;
- ITEM 3: C-numbers written, and any skipped (already recorded);
- ITEM 4 list;
- UNMEASURED;
- `## NOT DONE / NOT COVERED`;
- needs-Friday;
- Leak + secret scan;
- processes started / stopped;
- worktrees and files left.

## UNMEASURED (by the draft writer)
- **Jira transition ids** and whether `Done` is reachable in one step from `Backlog` on this board (`GET /transitions` closes it).
- **Whether Friday has settled the root `history.md` edit** before firing (the PRECONDITION).
- **Whether `main` moves past `db8edfd`** before the seat runs (the seat's `ls-remote` closes it).
- **The C-19 board-log second:** 06:49:56 is from the B30 brief's paraphrase, not from a verbatim board line. The draft writer found no verbatim line for it in the MPS briefs (grep `hosted-edit-survives` in `Briefs/`: 0 hits).

## HOLDS
- Datasec only; no other client's names, tickets or paths.
- CodeQL policy: push your branch only; never push to main; never dismiss an alert; never ask for a bypass. (This round pushes nothing: the records repo has no remote, and no code branch is made. Friday opens any PR.)
- No deploy, no Azure write, no setting change; nothing to any human. The Jira comments name no person.
- Never delete; quarantine.
  - Quarantine to `.tools/_quarantine/2026-10-11_B34_<what>/` (0700) and say so.
  - No `branch -d/-D`, `worktree remove`, `gc` or `prune`.
- **Processes:** kill by port + cwd, never by name. Stop everything you started before READY.
- `2_Project_Files`: read verbs and `fetch` only. No checkout, switch, commit, branch or push there.
- **Records:** write only `records/b34` (ITEM 3), the fold of records `main` (ITEM 2), your STATUS, and the Jira writes in ITEM 1. `CLAUDE.md`, `BACKLOG.md`, `JIRA.md` and `history.md` are Friday's: do not edit them, beyond what the fold carries in.
- **Instruments:** verdicts are ratios with denominators. Every scanner zero has a positive control that fired.

## End
The last line of `Briefs/2026-10-11_B34_STATUS.md` is one of these:
- `READY FOR REVIEW — records main @ <sha>`;
- `STOPPED: NEEDS FRIDAY` and one question.
