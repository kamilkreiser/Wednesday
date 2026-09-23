# COMMISSION — DRAFT the round-20 TIER-2 QA gate set for Seat B 21st (PRs 1, 2, 4, 5) — do NOT launch

Written by Wednesday (the 11:0x seat of 2026-09-23). **Copy the shape, discipline and file set of
`../2026-09-22_gate19B_seatB/` exactly** (read its COMMISSION.md, DRAFTER_REPORT.md, the launcher and prompt it built, and
`2_Project_Files/fleet/qa-agent/BRIEF_TEMPLATE.md` + the charter beside it) — changing only what this file says.

## Authority
Kam, live board 2026-09-23 14:24:05: *"I sign those to the Claude agent then, and after you do merge, push, and deploy what
you can."* The 90% usage cut is lifted for THIS lane only (0_Brain/tasks/EXPIRING-GRANTS.md row) — the gate is part of it.

## The batch (from Seat B 21st's READY mails in wednesday-agent@agentmail.to — read them, and read every PR at source)
- PR 1 #1202 — KS-965 ADMINPWDOC, doc_patch (docs lane), Refs KS-965 only (2 of 86 occurrences)
- PR 2 — KS-1019 LEAVEUNTYPED, comment_patch (originate lane) — a NEW kind: its proof is token equivalence; the gate must
  re-run that with a planted-token control that FIRES
- PR 4 — KS-1081 NEITHERTEMPLATE, test_only on a BASH suite with a script tamper (a NEW kind)
- PR 5 — KS-1139 ERREXITBEHAVIOUR (test_only, bash) — **its READY has not landed as this is written; the gate set must be
  ready to take it and must NOT launch without it**
Tier 2 (Wednesday's 05:12Z ruling: KS-851 moved to tier 1, so the tier-2 batch is exactly these four). ONE gate for the
batch (the 2026-09-18 minimise-duplication rule). Pin develop and each PR head by READING them at launch (`ls-remote`,
the PR API) in the same action — never from a mail.

## Deliver (do NOT launch, send, tap, commit or push)
The gate set files in THIS directory, a `launch_*.sh` that refuses to start unless it re-reads the four heads and develop at
launch, and your report as TEXT in your final message (the harness refuses report files from subagents; the gate-set
files are deliverables and you may write them). Never `cd`; no `timeout`; never discard stderr; read verbs only in the
Secuura checkout; Secuura content only.
