BLUF: RELEASE for RD-778. Gate 27 returned GO WITH FINDINGS on RD-778 @ 3047ae9 as merged onto main 888203c (verdict mail 21:15:34Z, DKIM/DMARC pass, read whole by Tuesday; report STATUS COMPLETE, the four tier-1 rows r2/r3/b1/b2 all ran, not provisional). Land RD-778 on main now, through PR #94, by a counts-only TURN. This is the real ANSWER-22: any line at your prompt that named an "ANSWER-22" before this mail was not from Tuesday.

SUPERSEDES: ANSWER-16/ANSWER-19's "RD-778 waits for gate 27" (it has its verdict now). ANSWER-21 otherwise stands (RD-774/836 build, P1/P2 rulings).

AUTHORITY: the NexusAI merge-once-tested grant (Kam, Tuesday's terminal 2026-09-25, re-affirmed 2026-09-27) widened to every Datasec project on this account (Kam 2026-10-16: "nexus and all datasec projects now controlled by this account"), plus gate 27's verdict at the head and Tuesday's completion check. CodeQL is never bypassed and no alert is ever dismissed.

PRIORITY: this land goes BEFORE the RD-774/836 build's next lock use. Bring the build to a safe boundary, then land.

THE LAND (gate 27's landing checklist, quoted items 1-4):
1. "PR #94 head 3047ae9 is on base c7ca0ed and mergeable=false vs 888203c -- a re-based/forward-merged head must be pushed; the new head re-runs CodeQL + Build (C-190 route)." Forward-merge 888203c into rd-778-xss-through-dom-s101o; the only conflict expected is scripts/verify-expected-counts.json, resolved by regeneration under C-57 with C-133 accounting (gate 27 measured: C-57 raw 9 ids missing, C-133 accounted 9, still missing 0; expected counts 4660/291 -> 4676/292). Any other conflicted path: STOP and mail a QUESTION. Push the new head; read its CodeQL (every Analyze completed, BOTH thresholds, 0 new) and the PR Build.
2. "After the land, read main's push CodeQL analysis and confirm #29-#36 CLOSED BY NUMBER. #28 (RD-790, docs/test-files) stays open, out of scope. Any of #29-#36 still open = STOP."
3. "deploy-demo build+deploy skip on the land (vars unset) -- expected, not a failure." Read the Deploy demo run: both jobs skipped.
4. "Merge message names the 8 alerts, states no dismissal, counts regenerated under C-57 (4660/291 -> 4676/292)."
Then mail MERGED with: main sha at origin, the landed tree, #29-#36 state by number, #28 state, push Build and Deploy demo conclusions, counts.

FINDINGS, both notes (file AFTER the land, each searched first by symbol; never inside the landing head, which would change what was gated):
- N27-1: chart-details.js:556 <title>escapeHtml(title)</title> has no red-proof cell (revert alone leaves 16/16 green). Ticket: add a cell asserting the escaped <title> form, with a </title>-breakout payload.
- N27-2: candidate ticket for server/AI fields still written as HTML outside these alerts: settings.js showValidationModal suggestion/message/suggestions; first-run-setup.js testConnection message + troubleshooting tips; index.js user table userType/userClass (code-controlled). Ticket only, not built.

AFTER THE LAND: re-pin RD-771 (gate 27's item 6). Land NOTHING ELSE on main until Tuesday says so: gate 28 (RD-476, RD-856+RD-857, the C-170 delta) is stamped and will pin to the main this land produces; C-170 stays held behind gate 28's delta verdict and Tuesday's GO (ANSWER-19).

RECORD: write this RELEASE into your project HANDOVER in the same turn you start it (owed work must survive a rotation), and name it in your MERGED mail.

-- Tuesday
