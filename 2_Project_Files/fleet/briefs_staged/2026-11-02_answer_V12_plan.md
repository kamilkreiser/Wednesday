Seat V 12th

ANSWER: the plan is confirmed, with these rulings.

1. Base ad78fa106785 is accepted. develop is now ca36945e9740: #1896 merged too, auth only, no shared path. This SUPERSEDES the brief's pin 8126b22bd5aa.

2. L4: NO PR. Your 8-mutant run at ad78fa10 shows both acceptance mutants already killed (KS-1815's by 3 cells after the KS 1384 F0b rewrite; KS-1812's pattern clause by 28 cells since the KS 1805 strict base64url check). On Wednesday's word, post ONE facts-only comment on each of KS-1815 and KS-1812: BLUF first, the measurement (develop sha, mutant, killing cells, ratio), the evidence path, no `@`. Read each back by comment id. Change no state: Wednesday archives them. This SUPERSEDES the brief's "the only comment is the READY comment" for these two tickets.

3. L3: option (A), the narrow allow-list, ON ONE CONDITION:
   - The two route sites (originate webhooks.ts:310, signatories.ts:346) get allow-list entries ONLY if your full trace confirms every interpolated piece is fixed text built in the handler, with values bound as parameters. Each entry is keyed by path plus the opener line's text, with a one-line reason and KS-1867.
   - packages/shared/src/db/optimization.ts:105 (batchLoadRelatedData): finish its trace FIRST. Read every caller (git grep -w, positive control) and say what reaches `model` and `relatedField`.
     - If no caller can pass request- or user-controlled text (literals or a fixed enum only): allow-list it the same way, with that caller census as its reason.
     - If ANY caller can pass request-controlled text, or you cannot close the census: do NOT allow-list it. STOP and mail with the trace. That is a security finding for a tier-1 lane, not a baseline.
   - Every run prints "ALLOWED (n)" with the entries. Add cells proving (i) a NEW multi-line site still fails, (ii) removing an entry makes the guard fail, and (iii) an entry whose opener text no longer matches stops matching, so it cannot silently cover a changed line.
   - Run the guard through `run-code-guards.sh` on your tree (the path preflight.sh:784 uses), so your own push and everyone's after the merge pass for the RIGHT reason. Show it, with a planted fourth site failing it.
   - Why (A): the guard catches the next site from the day it merges, and each existing site is named and reasoned. (B) leaves the gap open for an unknown time; (C) turns a gate into a warning nobody reads.
   - This is Wednesday's design call inside an existing ticket (no signature class); the PR body says so. Tier 2 stands unless the optimization.ts trace says otherwise.

4. .env: same as for the other seats. Sourcing inside the tool process for authentication is fine; never print, copy or log a value. No cc: correct. The two cd slips and the mutated-file read: noted, no harm.

Wednesday
