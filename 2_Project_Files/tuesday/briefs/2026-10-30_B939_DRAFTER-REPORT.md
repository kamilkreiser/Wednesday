STARTABLE: YES after your stamp, but NOT at once: load1 read 14.99 at 12:29 (ten builders and gate G215 live), so launch_when_cool will hold it; CI on the head was mid-run at 12:27 (CodeQL neutral pending the csharp analysis; e2e shards queued; web (Next.js) not listed): the gate reads them last, after a wait

# B939 drafter report (2026-10-30, about 12:26 to 12:45 AEDT)
Kit: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-30_B939_SEAT-G216_hpsmpoc-246-admin-metrics-gate-tier2.md` (67 lines; 8 four-underscore lines = 7 slots + the last line, lines 59-65 and 67, counted by `grep -c -E '_''_''_''_'`; at-sign slot pattern 0, control 1; non-ASCII bytes 0 by `LC_ALL=C grep -c '[^ -~]'`; person-name grep 0). Shape: the stamped B938 kit (checks, conventions, Stamp, Launch line) adapted to PR #246. I read everything else read-only: gh `-X GET` under the project `.gh-config`, `git --no-optional-locks` read verbs on the shared repo, no Jira call, no `cd`, no hosted HTTP, no ref written, no message, nothing in the project folder.

## BLUF
Seat `Datasec/HPSM-POC-G216` (Sonnet, `BRIEF_SEAT_LEVEL=sonnet` inside the quotes), ports 9710-9719, gates PR #246 @ `98abd3a0` (6 commits on main `e21d8044`, 0 behind, 7 paths +341 -35). Round 1 of 2 on class "admin status list and metrics restyle". The gate measures: the four status words and each row's evidence at source; the byte-equal fences (feedback, link, the single nav-dead-ends hunk); a base-vs-head strings program over the two screens; no sideways scroll at five widths on three pages, axe, and /admin reachability per role (the tier-1 tripwire); the `relative` pair (p6, p6b); eleven plants (p1-p10 red, p11 green); suites in CI order; CI and CodeQL last; overlap with H61 by hunk plus a merge-tree combined run.

## Facts re-measured (instrument; control)
- **PR and refs (12:27):** #246 open, draft false, mergeable true, `blocked`; 6 commits all unsigned; title 130 chars with `HPSMPOC-386`; merge ref `b17f7fb8` parents `e21d8044`, `98abd3a0`, tree `3e474346` = head tree. Open PRs 246, 245, 244.
- **Patch read whole** (495 lines, 0 non-ASCII). Product: `/admin` static server page (two Cards, typed 4-row const, StatusPill "Not connected" x3, RulesStatusTag draft); both screens className-only (cell/th padding, hover, mb-4); `relative` kept at Attribution :73. nav-dead-ends: one hunk `@@ -10,3 +10,3 @@`.
- **Role-shaped grep:** 30 loose hits in added lines, all in test files (getByRole queries, signIn harness) plus 1 comment; product files 0. proxy.ts, server/** unchanged.
- **Rulesets:** 4 files; top-level `status` absent 4 of 4, `ruleset.status` = draft 4 of 4 (`python3 -I`).
- **globals.css:65** `[data-scroll-x] { position: relative; }` at base: explains the builder's p6 non-widening.
- **Mail:** `JiraRestMailSink.cs:20,207-212` sends ACS email (`emails:send`) to `mailSettings.To` (`RouteSettings.cs:13`), a single configured feedback address.
- **CRM:** `-w CRM` hits only placeholder summaries (3 api seed, 6 web content) plus the PR's two admin files.
- **CodeQL neutral:** output title "1 configuration not found": `/language:csharp` default setup on main not found for the PR; Analyze (csharp) in progress at 12:27; analyses on pull/246/head 3 rows (results 0), merge ref 0; open alerts 0/0.
- **Overlap:** b928 0, b929 0, b931 0, b932 0; b930 (H61, 7ae229e9) shares `nav-dead-ends.test.ts` at `@@ -23,10 +23,16 @@` (disjoint from 10-12); b97/gate-b99-notes is the merged #82 leftover. Control: the 7 against themselves 7.
- **Round count:** 99 GATE VERDICT first lines; loose hits B477, B554, B784 only (other PRs/classes); control B805/B817 counted 2.
- **Ports/trees/panes:** 9710-9719 listeners 0 (unrestricted 15); `.tools/b939`, `.tools/wt-b939-head` absent; no G216 pane. Instruments `crawl.mjs` 95597931a0fa3753, `probe.cjs` 495ec186ee717ee2, `lock.sh` d9df031bcce14e93, `waitload.sh` cbd78c3800469050. Model rows G2 :109, G-cap :111; models_latest.json:23 `claude-sonnet-5-5`; brief_seat.sh:24 defaults to opus.

## Builder claims found wrong or loose at drafting
1. **D-1 mail evidence:** "no mail sender to customers in api/src (grep)": the grep (`smtp|sendgrid|IEmailSender|MailKit`) is blind to the ACS email sender in the feedback module. The row is very likely still TRUE (the recipient is one configured feedback address), so it reads as a Minor for the instrument, not a false status. The gate reads every recipient (C2c).
2. **The 1334 px `relative` comment** (Attribution :71-72) is not reproduced on this base (builder Correction 3, correct): `globals.css:65` already positions every scroll region. The gate adds p6b (also drop that rule, scratch only) to prove whether the mechanism is real.
3. **"CodeQL on the new head: 0 check runs"** was true before the PR existed; there are now 18 runs. That claim is superseded, a Note.
4. **The nav-dead-ends "named exception" row is vacuous** now that the list is empty (it loops zero times). This was not claimed wrong, but the builder said nothing about it. Note plus a follow-up ticket shape. The "no dead end" row carries /admin, and p7 proves it.
5. Correct, and the commission was wrong: the rulesets' status is at `ruleset.status`, not top level (builder Correction 1). Your gate brief repeats "top-level"; the kit uses the measured key.
6. Disclosed deviation: the head-cell padding changed against D-3's "leave the head classes" default (Correction 4). Typography is untouched. Note.
7. **PR body (Tuesday's text):** it holds one non-ASCII generated-by character, and the land-order sentence says "takes main by one merge commit", which does not fit a head-pinned squash. Minor, text; neither goes into the squash. The squash subject must be at most 100 characters (the title is 130).

## D-decisions (mine, in the kit)
- D-1: The status evidence is read at source (HttpClient users, mail recipients, CRM, ruleset key), with no load cost. It is never cut.
- D-2: A base-vs-head strings program over JSX text and non-className props of the two screens. className changes are listed and the guarded classes asserted.
- D-3: The role tripwire is /admin per role at base vs head, by URL and h1. Any difference is a tier-1 STOP.
- D-4: Plants: the builder's p1-p8 re-made, plus p9 (link text, through the real e2e), p10 (rules literal vs the four files), p11 equivalent (green), plus p6b.
- D-5: The combined tree with H61 (merge-tree plus the nav-dead-ends run) is the first thing cut under load.
- D-6: Hard stop: target 130 and HARD STOP 190 minutes after Step 0 (two trees, not three).

## Q-questions for Tuesday (each with a default)
- Q-1: Is the mail-evidence grep gap graded Minor when the only recipient is the configured feedback address? Default YES.
- Q-2: May p6b remove the `globals.css:65` rule in the scratch mut tree only (never committed)? Default YES.
- Q-3: Should the fetch include a third refspec for `b930` and the combined-tree nav-dead-ends run? Default YES; cut it first under load.
- Q-4: What does a NO GO mean? Default: the PR is parked open and Tuesday writes a round-2 fix kit.

## Reasons not to launch now
Load1 was 14.99 at 12:29, so the waiter will hold the launch. CI was mid-run, but that does not block a launch (the gate waits for CI). There is no other blocker: the head and main are as briefed, the ports and trees are free, and there is no role or auth shape.

## UNMEASURED
All runtime numbers in the kit (they are the builder's, written as predictions); whether CodeQL re-concludes after csharp completes; whether `web (Next.js)` and the e2e shards will pass; the hosted `Feedback:Mail:To` value; p6b's width; the combined tree with H61.

## Outside-the-fences disclosure
None breached. I computed sha256 prefixes of two METHOD files and two helpers under `.tools/` (read only) and listed `.tools/b939` and `.tools/wt-b939-head` (both absent). I did not open `.tools/b934/` or any `wt-b934-*`. I read only the builder's STATUS file and a listing of its evidence folder (plus `measure-p6-attribution-1280.json` and `e2e-whole-suite-summary.txt`). Scratch is in the session scratchpad only (PR json, body, patch, path lists, first lines).
