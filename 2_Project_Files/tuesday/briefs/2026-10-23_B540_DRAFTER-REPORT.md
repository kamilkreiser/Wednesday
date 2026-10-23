# DRAFTER REPORT · B540 (HPSM-POC records R25, afternoon round)

Drafted 2026-10-23 16:28 to about 16:55 AEDT by Tuesday's read-only drafter (Sonnet 5.5, row C8). Wrote only: the brief, its byte-identical `.pre-stamp` (`cmp` IDENTICAL), and this report. B540 was free (`ls | grep B54` showed nothing at start; the folder later shows B539 as highest before mine).

## Files
| File | Lines | Unstamped lines (four-underscore pattern) |
|---|---|---|
| `2026-10-23_B540_SEAT-R25_hpsmpoc-records-1023-pm.md` | 116 | **8** = STAMP, LAUNCH WINDOW, Stamped by, Launch authority, Hard stop, Heads at launch, Model receipt, plus last line `READ-WHOLE-BY-TUESDAY: ____` (`grep -c` printed 8 on both the brief and the `.pre-stamp`) |

TRANSITIONS and CATCH-UP are not slots here (you listed 7 + 1): they are fixed as defaults in the brief (transitions none, new tickets none, catch-up STATUS files only). Say so in an ADDENDUM if you want otherwise.

## What the brief orders (next free C-number read: C-161; highest on records main d433ddcd is C-160, heading `CLARIFICATIONS.md:2635`)
- C-161 the 2026-10-20 09:38:08 card (`sm-access ... c "No logon at all"`), the only still-PARKED HPSM-POC register row found (all other HPSM-POC rows are already in C-119, C-120, C-125, C-130, C-133, C-134, C-151); the card id carries a first name, so the seat writes it with the token withheld.
- C-162 the 14:16 timing-floor ruling (`show` read-only: choice a, ruled 14:16:58, delivered 14:17:57) with B514 ADDENDUM-1 (commit a58ba947 on PR #199, open).
- C-163 the 14:21:39 PHASE SCOPE ruling verbatim, beside C-106, with "not settled" on C-73 and the switched-off file import; standing line verbatim in STANDING LINES item 10.
- C-164 PR #196 landing (squash d13acc40, 04:11:45Z, head 5a0fc03b), B510 builder, B523 GO WITH FINDINGS, findings B523-1..-7 as rated, your 15:13 call quoted from the daily note line 155 (one line, read-only).
- C-165 builder claims for #197..#201 in one table, state read live, gates fenced.
- BACKLOG rows for B523-1..-7, B510/B512/B513/B514/B515/B516 follow-ups, shared notes (Dependabot alert, `.tools` tracked paths, name-diff trap, `apiq.sh` filter). Jira: at most 5 comments (HPSMPOC-328, -296, -297, -218 conditional, -318), no create, no transition. Catch-up: B508, B510, B512..B516, B523 STATUS files.

## Things you should know before stamping (my judgement calls, flagged)
1. **Live gates:** G58 `%329` and G62 `%334` live at 16:28. `B525_STATUS.md` does not exist; `B536_STATUS.md` line 1 reads `GATE VERDICT B536: IN PROGRESS ...`, a draft with no verdict. The brief makes "a verdict exists only when the LAST line begins `VERDICT:`" the rule, forbids copying either gate's files, and has the seat read only first and last lines of them (property P3 checks it).
2. **Commercial reason kept out of Jira:** the phase-scope ruling says showing HP finished work weakens their funding case. Jira may be HP-visible, so the brief bars any phase-scope content and the words "phase/funds/funding/justify" from Jira text. C-entries carry it verbatim (the register's own instruction).
3. **"Ticket rows" vs "BACKLOG rows":** your daily note (15:13) says "B523-1/2/3 as ticket rows"; your instruction to me says BACKLOG rows (with HPSMPOC-328). I followed the instruction: BACKLOG rows, no new Jira ticket, one comment on -328 for the B523-3 class. Change by ADDENDUM if you meant tickets.
4. **B526 (H6, B478-5 edge characters) is drafted but not launched** (no `b526*` ref on the code origin; no pane). It is outside your list; the brief only forbids writing it as built. Its brief cites a ruling in force (card `hpsmpoc-refuse-more-invisible-characters`, 2026-10-01, plus the 2026-10-22 extension) which already sits in the record as C-entries from earlier rounds? Not verified by me; unmeasured.
5. **No Jira read by me.** All Jira facts (ids 39905..39922, keys 326..328) are B508's, relayed; the seat re-reads. HPSMPOC-218 is the braces ticket per B510 STATUS line 36; the brief makes its comment conditional on reading it.
6. **Register filter:** `grep -F 'HPSM-POC'` returned 11 rows; row 10 is a Datasec/Security-Composer row (matched on "HPSM-POC seat" inside its text). Not used; the brief tells the seat to skip and say so. It names another project of the same client only by that fact.
7. **Gaps B508 flagged, not in scope here:** PRs #180..#183 absent from the records (B508 STATUS FOR TUESDAY 4). Not added; say if a later seat should take them.
8. **Records main moved** since B508's brief: it is d433ddcd (B508's PR #133 merge). The brief baselines on it and expects C-161 upward.
9. **Ports:** none needed. Highest allotment found in the 2026-10-23 briefs: B539 8800-8809 (next free 8810-8819).
10. **Stamp convenience:** heads at 16:28: records main d433ddcdcbab63ea6828050dfd72ea44478d0ea5; code main d13acc4037ab843fda95280e219b4465b83d59ab; #197 8e1b4688, #198 43c4c25b, #199 a58ba947, #200 da1e875a, #201 28ba1a60 (full shas are in the brief).

## UNMEASURED
Jira states; whether any PR head moved after 16:28; whether a later HPSM-POC deploy exists after 486e74e; the gates' verdicts; whether HPSMPOC-218 concerns the dated braces exception.

## Fences kept
Wrote three files only. `gh api -X GET` under the project's `GH_CONFIG_DIR`; git/gh read verbs only; the register only through `grep -F 'HPSM-POC'`; `decision_queue.sh show` of the one timing-floor id only (no `list`); no scoreboard, no `briefs_staged/`, no Artifact/Docs/mail/chat tools; no `cd`. One slip to disclose: my first `Bash` call in a fetch step typed `cd /tmp`; the pre-tool hook refused it and the call did not run.
