---
date: 2026-11-13
type: grant
source: Kam, live board 2026-11-13 07:52:34 (view=wednesday), card secuura-premerge-block-nine-prs-1113 = c
status: live
tier: W
---

# Our PRs no longer carry a "do not merge until the pre-merge tests run" sentence, and the nine held for it merge like the rest

**The operative case, so the headline matches it:** Wednesday is writing a raise or build brief for Secuura, stamping one, or deciding whether a gated PR whose own body says "Do not merge until the pre-merge tests have been run and pass" may join a merge queue. **It may.** Since Kam's ruling (c) at 07:52:34 on 2026-11-13, those PRs merge on the TESTED grant like every other, and new PR bodies stop writing that sentence.

**His words, verbatim:** *"Decision secuura-premerge-block-nine-prs-1113: c — Merge them, and drop the 'do not merge' sentence from our PR text going forward"*

**How to apply:**
1. The nine released (2134, 2126, 2098, 2097, 2096, 2095, 2090, 2089, 2079) join the merge queue behind the current merge seat's rows, each still on its own gate verdict at its current head and Wednesday's head-pinned GO. The GO says once that the Schemathesis/Akto suites were not run and the boxes stay unticked.
2. Every Secuura raise/build brief carries the standing line in `2_Project_Files/fleet/STANDING_LINES.md` (section dated 2026-11-13): no self-hold sentence; the Test Evidence block still names what was NOT run.
3. Existing bodies are not edited for this (a merge seat edits no body).
4. Unchanged: the QA gate before every merge, the signature classes, demo frozen.

**Family:** [[2026-09-11_secuura-we-approve-and-merge-our-own-tested-work]] (the TESTED grant this rests on) · [[2026-09-09_my-authority-and-the-targets-rules-are-two-checks]] (why the nine went to Kam rather than being waived by stamp) · [[2026-08-03_go-slow-earn-autonomy]] (rule 5: every grant recorded).
