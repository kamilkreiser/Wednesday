# Spark operator 101 — commission (Wednesday, 2026-11-04 02:04 AEDT). Secuura only.

## Why you exist (BLUF)
Kam's standing rule (2026-10-28, verbatim): "never keep the spark idle". The Spark has been idle since 22:41 on 3 Nov
(spark_status: IDLE 198 min at 01:59). Operator 100 found the doc_only class nearly exhausted (451 KS Backlog/Todo
candidates, ~330 screened by TITLE ONLY) and recorded the blocker: `night/hold_ready.py` has NO hold kind for the
Spark tier `test_only_input`, so even a passing test_only_input round cannot be held. Your job: remove that blocker,
then keep the Spark fed from the unscreened candidates. Target 6 held passes; never pad (a thin pool is a finding).
Routing: Sonnet subagent, model-routing P3 "Spark operator driving local work" (gauge 7d 94%: be lean).

## Read first (whole)
1. `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-11-02_spark_operator_common.md` — its
   THE QUEUE, Limits and Deliverable sections bind you EXCEPT: (a) its "The class" (KS-1868 catch class) does NOT
   apply — your classes are below; (b) its tip and in-flight list are stale — use this file's.
2. Operator 100's report and tools: `/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_spark-operator100/`
   (report.md; gen/fetch_tickets.py = the read-only candidate fetch; gen/mk100.py; gen/patch_hold.py).
3. `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/README.md` (tiers) and each tool's header before
   first use (round.sh, queue.sh, brief_lint.py, night/hold_ready.py incl. hold_doc_only() at ~line 274).

## ITEM 1 — the hold kind (tooling, Wednesday's own tree)
Add a hold kind for Spark tier `test_only_input` to `night/hold_ready.py`, modelled on operator 100's hold_doc_only():
detect from input.json/round.json tier; product files UNCHANGED (sha-asserted) — any product hunk REFUSES; strict
`git apply --cached --check -p1` (non-strict REFUSES); red-first evidence carried from checker.out.
- Edit by COPY then `mv` (never in place; check `pgrep -fl hold_ready` first); backup `hold_ready.py.pre-1104-op101`.
- Arms BEFORE use (save outputs in your report dir): an existing test_only_input PASS run (if one exists in
  local-model/runs — `ls` named dirs only) or your first real one dry-runs OK; a diff touching a product file REFUSES;
  a non-strict diff REFUSES; the existing doc_only and code_patch arms still pass (`tests/` beside it).
- Add the IMPROVEMENTS.md row (local-model/IMPROVEMENTS.md) closing operator 100's "owed" line.

## ITEM 2 — feed the Spark
Classes, easiest first: `test_only_input` (a test that pins EXISTING behaviour; no product change) then `doc_only`.
Candidates: re-fetch fresh with a copy of gen/fetch_tickets.py (paginated `first:` reads; read-only; never `last:`).
Start with the ~330 operator 100 did NOT read past the title. Per ticket, read it whole and the code at the tip before
briefing. Skip with a one-line reason (decision-shaped, real Postgres/Redis, auth design, anchoring/money, HTML,
in-flight file). KS-1343: its remaining notes (op 100 raised N-1286-4/-7/-8 only) are allowed ONLY if they live in a
file NOT in the exclusions below; otherwise skip and say so.
Flow, counter, queue discipline: exactly the common commission's (one control at a time until the first
CONTROL-PASS; model line only after its CONTROL-PASS; original + ONE rebrief; never hand-edit model output).

## Limits (these override the common file where they differ)
- Tip: develop `79145a312f0150ca9adaf5a36bb3dea93d108cff` (Wednesday's `git -C <checkout> ls-remote origin
  refs/heads/develop`, 15:03:51Z 3 Nov); re-read the same way at start and end. It may move (merges).
- NEVER brief these files (in flight or held for a raise seat tonight): `Blockchain/Dev/scripts/restore-local-secrets.sh`
  and its test (PR 1989, held for Kam); PR 1982's files; PR 1992 and PR 1993 files; `services/nft-certificate/src/routes/nft.routes.ts`;
  the three doc_only files of op 100's held passes (CONTRIBUTING.md and the MULTI-TENANCY.md / RLS-FAIL-CLOSED-PLAN.md
  docs — paste their exact paths from op 100's held_paths.out); `services/auth/src/services/session.ts`,
  `routes/health.ts`, `index.ts` (auth; a ticket is being filed on them); any file any OPEN PR lists (scan with a
  planted control at start AND end); any path a held READY in `night/` already covers.
- **Disk:** `df -g /Volumes/DevMASTER` before every round batch; **under 18 GiB free = STOP** (a raise seat needs the
  last 15). Read 24 GiB at 02:0x. Prune only your own run dirs with spark/prune_work.py if its header allows; delete
  nothing else.
- Load: capacity reads FULL from Spotlight indexing (mds_stores), not a seat; it does not stop you.
- Never `grep -r`/`find`/`du` over spark/runs, night/, worktrees/ or a gate clone; `ls` named dirs.
- Writes ONLY under /Volumes/DevMASTER/WEDNESDAY/. No push, PR, comment, ticket write, mail. Secuura content only.
- Stop when 6 are held, or the pool is genuinely exhausted (say the counts: read / skipped by reason / briefed),
  or at ~2.5 h of wall clock, whichever first. Leave nothing running.

## Deliverable
`/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-04_spark-operator101/report.md` (heredoc), common-commission
shape plus: the ITEM 1 diff summary + arm outputs (paths), held names pasted from `ls`, per pass the hold_ready line
verbatim and a recommended tier, skipped-with-reasons, round log with done.md row times, disk start/end, UNMEASURED.
Final message to Wednesday: BLUF + held names + done.md row times only.
