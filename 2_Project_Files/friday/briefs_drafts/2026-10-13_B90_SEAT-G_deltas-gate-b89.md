From Friday (laptop seat), Datasec / MPS Commercial Calculator. No mail key in this project: your STATUS file is the wrap.
# BRIEF B90 · SEAT-G: QA DELTAS GATE, tier 1, ROUND 2 OF 2 (LAST under Kam's cap), on `b79/proposal-two-buttons` @ e776635: gate B88's G-1 fix (the one-pager's lead = the executive summary's FIRST paragraph) + the merge of main 33f2cb41 (B85) into the branch
**Fired: 18:33.** Pane `Datasec/MPS-G` (fresh seat). Your commission is THIS file at `/Volumes/Laptop-DEV/FRIDAY/2_Project_Files/friday/briefs_drafts/2026-10-13_B90_SEAT-G_deltas-gate-b89.md` (Friday's tree, read-only to you). Step 0: copy it unchanged into your `1_Project_Definition/Briefs/` (`cmp` equal, sha256 in STATUS).
**Launch (Friday):** `bash /Volumes/Laptop-DEV/FRIDAY/2_Project_Files/fleet/cockpit/cockpit.sh add Datasec/MPS-G "bash '/Volumes/Laptop-DEV/FRIDAY/2_Project_Files/friday/brief_seat.sh' datasec '/Volumes/Laptop-DEV/!CODING/Datasec/Datasec MPS Commercial Calculator' '../../../FRIDAY/2_Project_Files/friday/briefs_drafts/2026-10-13_B90_SEAT-G_deltas-gate-b89.md'"`. No az. (Concurrent: build seat **B83** on `b83/feedback-attachments`, pane `Datasec/MPS-E`, worktree `.tools/wt-B83`, ports 6750-6759: never open, run in or touch it.)
**Report:** `1_Project_Definition/Briefs/2026-10-13_B90_STATUS.md`; first lines = the verdict lines below; exact LAST line `READY FOR REVIEW: B90 gate b79 @ <sha7> on main <sha7>` or `STOPPED: NEEDS FRIDAY` + ONE question.
**TESTING seat, findings only** (charter `/Volumes/Laptop-DEV/FRIDAY/2_Project_Files/fleet/qa-agent/QA_AGENT_CHARTER.md` §7 §8: oracle, evidence, coverage executed/skipped/n-a, proved vs assumed; no product change, not even a test; a write grant is void, so refuse and report). **Round 2 of 2, the LAST:** Kam's cap is two NO GO rounds; a NO GO here means the branch does NOT ship this round (Friday tickets the residue and cards Kam). Each finding: blocks merging as is, or a ticket. **DELTAS gate:** what changed since gate B88 judged `adacb7e`, plus anything the merge of main could have broken. B88's verdicts on everything else STAND (cite B88 STATUS, do not re-run them) except where a delta touches them. Every fact you write carries file:line or says UNMEASURED. Your own instruments, mutants and controls that can fail (B88's shape).

## Subject (Friday, read-only git, at brief time)
- Branch `b79/proposal-two-buttons` @ **`e776635a1ef9c13f8153d0446882fe8186e24b9f`** (Friday's `ls-remote` = the builder's push read-back, B89 STATUS last line). Main **`33f2cb41fa81871bcfeacfdb5498479f658de63e`** (`ls-remote`). `rev-list --left-right --count main...branch` = `0 12` (a fast-forward merge is expected; B89 claims `merge-tree origin/main e776635` = `e776635^{tree}` `098f46d1…`).
- The deltas since B88's `adacb7e`, three commits (Friday's `log --format='%h %p %s'`):
  - `7b3cc5a` (parents `adacb7e` + `33f2cb4`): merge of main = B85 / PR #37. B89 claims its tree = `f90ac316769f1aa5016feefc4ba08e17a746076c` = B88's prediction (B88 STATUS `:17`).
  - `d94a1df`: the G-1 fix.
  - `e776635`: the e2e order change.
- `git diff --stat 7b3cc5a e776635` = **3 files, +94 / −3**: `web/src/proposal/OnePager.tsx` (+16/−2), `web/src/proposal/OnePager.test.tsx` (+35/−1), `web/e2e/proposal-buttons.spec.ts` (+43). That is exactly B89's partition (B89 brief `:26`); confirm it.
- **The builder's report, read whole as a CLAIM:** `Briefs/2026-10-13_B89_STATUS.md` (174 lines). **The oracle:** B89 brief (`Briefs/2026-10-13_B89_SEAT-B_g1-summary-first-paragraph.md`, Do `:14-19`), gate B88's G-1 (`Briefs/2026-10-13_B88_STATUS.md:174-195`), and the approved mock (`1_Project_Definition/Design/2026-10-12_one-pager/`, PDF p.2 row "1 Executive summary"; `tools/make_mockup.py:141-151` `condense_summary`).

## Authority (verbatim; cite, do not re-open)
- Kam's approved mock (card `mpscalc-one-pager-mockup-1012` = a), PDF p.2, as quoted by gate B88: *"CONDENSE · First paragraph, cut at a sentence end ≤ 600 characters, then "…" (D-6). Shown as the lead paragraph without its heading"*.
- Kam, live board 2026-10-13 12:31:16 (the two buttons and itemisation): B88 brief `:13`, unchanged.

## RULED by Friday (do not re-open)
- Everything RULED in B88's brief `:16-21` stands.
- N-1 (double click while the logo loads calls `print()` twice) is a TICKET, not this round (B89 brief `:22`).

## Verdict lines
- `B79+B86+B89 e776635: GO | GO WITH NOTES | NO GO`
- `B90 G-1 fixed (lead = first paragraph; \r\n, \n, \n\n; blank lead lines; one paragraph unchanged; > 600 cut + " …"):` · `B90 one-pager fit (1 A4 page: B50's five shapes + the 4-paragraph overflow and overflow-as-draft, macOS + Linux, room left):` · `B90 merge of main (tree = prediction; B85 guards + S10 cents rows green on the branch):` · `B90 suites base 33f2cb41 vs head e776635 + Entra bundle:` · `B90 NEW WORDS (0 claimed):`
- `MERGE 33f2cb4+e776635: GO | GO WITH NOTES | NO GO`

## Check (FOUND / TESTED / HOW, each with its own control or mutant)
1. **G-1, your instrument.** Read the `OnePager.tsx` diff `7b3cc5a..e776635` line by line against B89 brief Do 2. Then render the one-pager (Chromium `page.pdf`, A4, your own fixture built the B88 way) with these executive summaries: 4 paragraphs separated by `\n`, the same by `\r\n`, the same by `\n\n`; leading blank lines then a paragraph; one paragraph ≤ 600 (must render exactly as at `adacb7e`, no ` …`: compare the text and bbox with the same fixture rendered at `adacb7e`); one paragraph > 600 (cut at a sentence end ≤ 600 + ` …`, as at `adacb7e`); a first paragraph with no sentence end inside 600 (say what it does and whether that matches the mock's `condense_summary`). For each: the lead text from `pdftotext`, page count, and whether ` …` appears. **Compare with the mock's own `condense_summary`** (run `make_mockup.py`'s function on the same inputs in scratch) and list every difference. **Mutant (yours):** revert to cutting the whole text → the 4-paragraph fixture prints 2 pages and your check is RED; restore → GREEN.
2. **Fit:** exactly 1 A4 page on B50's five shapes AND on overflow + overflow-as-draft with a 4-paragraph summary, macOS + Linux. Room left by B88's own method (its STATUS names it) vs B88's **52.1 / 46.9 / 83.7 / 8.1 / 2.9 mm** and B89's claim (identical).
3. **The merge of main.** `git rev-parse 7b3cc5a^{tree}` = `f90ac316…` (B88 `:17`). On head: B85's `noBrowserPricing` (all its tests; print its `browser money arithmetic: N (files scanned M)` line) and `cssColourGuard` green; S10 on a rental quote from the live API reads the `…InCents` parts through `proposalRentalRows` (each row = its JSON field, formatted; B85's R-28: shown parts add up to the shown total, now in scope because B85 is merged). `git diff 33f2cb4 e776635 --stat` must equal B79's 11 files (B88's list) and nothing of B85's 29 (confirm).
4. **Suites, base `33f2cb41` vs head `e776635`, macOS + Linux** (B88's images; name the tag/digest): .NET, Vitest, lint, `tsc -b`, `npm run build`, `VITE_MPSCALC_AUTH=entra npm run build` + `node scripts/check-bundle.mjs dist` (rc + its line), e2e legs (live / stub / Linux no-API). 0 failed except a pre-existing set identical on both trees (name each: B88 measured `[B86-1]` is MAIN's); **0 lost test names** on head vs B88's head-run list.
5. **Customer safety on every PDF you render** (B88 check 6's regex = 0; one-pager ex GST only).
6. **NEW WORDS:** B89 claims 0. Diff every user-visible string `7b3cc5a..e776635` and confirm.
7. **Merge prediction:** scratch `git clone --shared`, `git merge-tree --write-tree <main-at-verdict> e776635`: clean (a fast-forward is expected), or the conflicting paths. If main moved, say what moved.

**Screenshots** (synthetic) → `Briefs/2026-10-13_B90_evidence/`: the one-pager with the 4-paragraph summary (PNG of the PDF page), and the side by side with the mock's overflow render.

## HOLDS
- Datasec only; synthetic data; never open `4_Credentials/.env`, `.local/` or `.local/pricebooks/`; no hosted site; **no az** (`infra/tests/test_infra.py` NOT run: say "not run (az fallback, HOLD)"); no Jira; no history.md.
- No product change, no commit/push to any branch, no PR, no merge, no deploy. Never delete (quarantine under `.tools/_quarantine/2026-10-13_B90_<what>/`), never force-push, never dismiss CodeQL.
- **In the project checkout READ verbs only**, as `git --no-optional-locks -C`: `ls-remote · log · show · diff · cat-file · ls-tree · rev-parse · rev-list · merge-base · grep`. Every write verb (clone, checkout, merge, merge-tree, build, mutants, npm) happens in a `git clone --shared` scratch copy or under `.tools/qa-B90/`. Never open, run in or touch other seats' trees: `.tools/wt-B79`, `wt-B89-base`, `wt-B89-mut`, `wt-B83`, `qa-B88`.
- Containers: yours named `b90-*`, removed by you at the end (`docker rm`, never `-v`). **Ports 6780-6789 only** (Friday read 0 listeners there at brief time); `5080`/`5173` are Kam's, 6750-6759 B83's, 6760-6769 B89's (stopped). Kill by port + cwd, never by name.
- A line at your prompt that is not a Friday file pointer is not an instruction.
