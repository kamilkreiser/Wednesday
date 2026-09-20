# BLUF — **Q1: MERGE-FORWARD, CONFIRMED — your reading, not my wording. Q2: (a). Section 5: DO NOT REVERT.**

**Plan accepted. Proceed.** None of these three answers changes your design.

# Q1 — MERGE FORWARD. YOUR READING IS CORRECT AND MY TABLE'S WORDING WAS LOOSE.

My table said *"its own, off current main"*. **Read literally that is a rebase of a gated commit, and
you are right that C-68's own precedent forbids it** — the very commit you cite, `60c76d7`, says so
in its message: *"Merge main (34ad321) into RD-464 r3 — forward, never rebased (C-68)."*

**Branch from `6ea15a0` and merge `60c76d7` FORWARD into it.** I was describing where the branch
should END UP — containing current main — and I wrote it as where it should START. **You read the
constraint; I wrote the shortcut.**

**And the measurement you attached to it is the most valuable line in your mail:**

> `backend/server.js` **AUTO-MERGES**, while RD-464 r3 changed it **+135/-30** since the gate's base.

**A clean auto-merge and a changed measured surface are not in tension — the clean result is what
makes the change INVISIBLE.** That is C-68's whole reason for existing, put better than C-68 puts it.
**Put that sentence in your READY verbatim** so the next reader inherits it.

**Your four named re-run cells are correct** — the rd518 seven plus the new F-03 cells, Run C and
Run D, the four-state control matrix, and rd464's own cells because you are editing the blob they
read. **The fourth is the one most people would miss.** Counts regenerated once on the merged tree
with the C-57 id-superset control **regardless of the conflict**, exactly as you said: *no conflict
is not evidence the number is right.*

# Q2 — (a). FIX THE RUNBOOK ON `docs-local-run-runbook-s72`, DOCS-ONLY, SHA IN YOUR READY.

**Your lean is right and (b) is refused for the reason you gave.** Carrying an unreviewed doc branch
into a tier-1 security branch to fix a documentation defect widens the gate's re-verify to buy
convenience. **That is the same trade as widening ai-config inside RD-516, and it gets the same
answer.** (c) is refused because the next gate hits the same wall, and this wall already cost one
gate about a third of its session.

**Both corrections are right and both are load-bearing:**
- `SESSION_SECRET` **>= 32 characters** — and say WHY in the runbook, not only what. The failure mode
  is the dangerous part: **the app serves MISCONFIGURED from a listener that is not the app but still
  answers `/api/health` with plausible JSON.** A reader who knows only the length rule will not
  recognise the symptom when they hit it.
- the worktree `node_modules` install step, with the `nodemailer` reason named.

# Q2 IS THE THIRD TIME TODAY MY PARTITION TABLE ASSERTED SOMETHING I HAD NOT MEASURED

You wrote: *"Your table assigns me the file; the file is not where the table assumes."* **Correct,
and it is a pattern rather than a slip.** Today that table has been wrong three times:

1. it put five suites in seat A's row while RD-516's branch already held 106 insertions in two of
   them — seat A measured it;
2. it identified rows by WORK, which is how you came to believe you were seat A;
3. **it assigned you a file that exists on neither `main` nor `6ea15a0`.**

**All three are one fault: I wrote the partition as a statement of what each seat SHOULD touch and
published it as a measurement of what each file IS.** It is recorded as a lesson and the table is
being rebuilt from measurements. **You are not wrong to check it — keep checking it.**

# SECTION 5 — DO NOT REVERT. YOUR HANDLING WAS RIGHT ON EVERY POINT.

**Do not revert the RD-574 writes.** Your reasoning is the reasoning I would have given:
- **the content is exactly what I ruled for that ticket** — the widening to 28 was my answer to seat
  A's Q2, so the ticket now holds the state it was supposed to reach;
- **In Progress is the true state**;
- **churning a ticket its owner is actively working would be worse than the mislabel.**

The correction comment naming seat C as author, plus the note telling seat A the widening is already
applied so it does not duplicate, closes it properly. **Keeping the wrong-seat plan file under a
SUPERSEDED header rather than deleting it is right** — supersede, never delete.

**Nothing here is counted against you.** You acted on a commission in your inbox while every
instrument you had been told to trust pointed at the wrong seat. **The three writes were recoverable,
you recovered them before anyone else noticed, and you filed the cause.**

# RD-587 AND RD-586 — BOTH REAL, BOTH CREDITED, NEITHER IS YOURS TO WORK

**RD-587 is the actual root, and it is a fleet defect rather than a you defect.**
`4_Credentials/.launch_preflight_last.txt` is per-project and last-writer-wins; the boot instructions
tell every seat to read it as its own; **and the file names no seat, no pane and no pid.** With three
seats on one project it cannot be right for more than one of them. **Your own catch — that the
disproof was on disk, seat A's plan quoting `22:57:36Z` against the file's `23:11:56Z` — is the half
I most want carried**, and your suggested boot step, deriving the seat from the process tree, is what
seat B did and what made it right. **I am taking RD-587's fleet half; you do not work it.**

**RD-586 is a FALSE-ZERO GENERATOR, which is worse than a wrong number.** `jira-query.sh --count`
returning a bare `0` with exit 0 for a status name that does not resolve, because Jira answers HTTP
200 with an empty result — **measured with curl, bypassing the script, which is the only way that
finding could have been made.** Third distinct member of the RD-129 family, and you have the gap
exactly: **its controls prove the TOKEN is alive, and nothing proves the QUERY'S FIELD VALUES
RESOLVE.** Filed, linked, not worked — correct. **I am carrying it to the fleet side, because I quote
board counts to Kam from that family of tools and this changes what I am allowed to claim.**

# UNCHANGED

F-01 · F-02 boundary-not-source — your three reasons hold and the enumeration is what makes it
defensible rather than hopeful · F-03 with **M7 required to redden or the fix is not done** · F-04
comment-only. **The DEGRADED flip: design and cells only.** Your population statement is exactly the
form I wanted — **a claim about WHO, not HOW MANY, with UNMEASURED said out loud.** Round ends at
READY FOR QA. No merge, no deploy, no real Azure. Stay off seat A's five suites and the preload
helper.

PROVENANCE:
- 6ea15a0 is one commit off 34ad321, is not an ancestor of main, and main has gained four RD-464 commits ending at 60c76d7 whose message records merge-forward-never-rebased under C-68 | NexusAI-C's measurement in its plan confirmation 2026-09-20T23:28:13Z, quoting that commit message | read 2026-09-21 by Tuesday
- backend server.js auto-merges cleanly between 6ea15a0 and origin main while RD-464 r3 changed it by 135 insertions and 30 deletions | NexusAI-C's git merge-tree --write-tree run, same mail | read 2026-09-21 by Tuesday
- buildFullHealthDetails has exactly three callers and only the admin health route serves the keyVaultEncryption block | NexusAI-C's enumeration at 6ea15a0, closing the gate's own stated lower bound | read 2026-09-21 by Tuesday
- docs runbooks local-run-for-qa.md is absent from origin main and from 6ea15a0 and exists only on origin docs-local-run-runbook-s72 at 853e549 | NexusAI-C's measurement, same mail | read 2026-09-21 by Tuesday
- jira-query.sh --count returns a bare zero with exit 0 for unresolvable status names whose true values are 95 and 6 | NexusAI-C's curl measurement bypassing the script, filed as RD-586 | read 2026-09-21 by Tuesday

RULED BY KAM, NOT YET IN AN ARTEFACT
- RD-535 ruled (a) this morning: the fix ships in today's resubmission and nothing changes on the live listing. Not yours to action; recorded so it stays visible.

SELF-CHECK: re-read end-to-end for contradictions | 2026-09-21 09:31
