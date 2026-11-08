# Spark operator 102 — commission (Wednesday, 2026-11-08 22:4x AEDT). Secuura only.

## Why you exist (BLUF)
Kam, panel 2026-11-08 20:26 (verbatim): "please check that the spark is running flash 4 and keep it active as much as
possible. then work through as many secuura in progress and backlog tickets as possible". The Spark has been idle since
11-04 02:13; its tunnel was re-opened at 22:45 tonight and serves deepseek-v4-flash-0731 (/v1/models 200). Your job: feed
it. Target 6 held passes; never pad (a thin pool is a finding, report the counts).
Routing: Sonnet subagent, model-routing P3 "Spark operator driving local work".

## Read first (whole)
1. `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-11-02_spark_operator_common.md` — its THE QUEUE,
   Limits and Deliverable sections bind you, EXCEPT its "The class" section and its tip / in-flight list (stale; use this file).
2. Operator 101's commission and report: `/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-04_spark-operator101/`
   (commission.md, report.md, gen/), and operator 100's tools `/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_spark-operator100/gen/`.
3. `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/README.md` and each tool's header before first use.

## Feed the Spark
Classes, easiest first: `doc_only` (Markdown/text docs; not HTML), `test_only_input` (a test pinning EXISTING behaviour, no
product change), then log-only catch fixes (code_patch/code_patch2) on non-security surfaces only.
Candidate pool: re-fetch fresh (paginated `first:` reads, read-only, never `last:`). Start with tickets FILED SINCE 11-04
(KS-2080 and above, including tonight's gate-note filings KS-2105 to KS-2116 — several are wording/test-pin notes), then the
older Backlog/Todo titles operator 100/101 did not read past the title. Read each ticket whole and the code at the tip
before briefing. Skip with a one-line reason (decision-shaped, security/auth/key/role surface, real Postgres/Redis,
anchoring/money, HTML fragment, a file any open PR lists, a path a held READY in night/ already covers).
Flow, counter and queue discipline: exactly the common commission's (lint, dry-run, one control at a time until the first
CONTROL-PASS; model line only after its CONTROL-PASS; original + ONE rebrief; never hand-edit model output; hold with
night/hold_ready.py).

## Limits (override the common file where they differ)
- Tip: develop `abd044f63a9dd5673f1b9ff7a2b1e42e1c26de82` (Wednesday's `git -C "/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files" ls-remote origin refs/heads/develop`, 22:43:31 AEDT). Re-read the same way at start and end; it WILL move tonight (a merge seat is merging), so re-pin per round and record the pin.
- Open PRs: about 40 are open and merging tonight. Scan with a planted control at start AND before each round; any file an open PR lists is out.
- Disk: DevMASTER read 23 GiB free at 22:46. `df -g /Volumes/DevMASTER` before every round; UNDER 18 GiB = STOP. Prune only your own run dirs with spark/prune_work.py if its header allows; delete nothing else.
- Load1 under 8 (seats and gates are running); wait, do not stop, while it is above.
- Never `grep -r`/`find`/`du` over spark/runs, night/, worktrees/ or a gate clone; `ls` named dirs. Never `cd`.
- Writes ONLY under /Volumes/DevMASTER/WEDNESDAY/. /Volumes/DevMASTER/!CODING/ is READ-ONLY including its .git (ls-remote, show, cat-file only; never fetch there). No push, PR, comment, ticket write, mail. Secuura content only.
- Stop at 6 held, a genuinely exhausted pool (counts: read / skipped by reason / briefed), or ~2.5 h wall clock. Leave nothing running.

## Deliverable
`/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-08_spark-operator102/report.md` (quoted heredoc), the common shape:
BLUF, held names pasted from `ls`, per pass the hold_ready line verbatim and a recommended gate tier, skipped-with-reasons,
round log with done.md row times, tip and disk start/end, UNMEASURED. Append the queue.md comment line operators write.
Final message to Wednesday: BLUF + held names + done.md row times only.
