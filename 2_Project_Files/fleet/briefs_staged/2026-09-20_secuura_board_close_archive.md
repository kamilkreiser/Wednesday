Secuura/Blockchain BOARD PASS seat, from Wednesday

⚠ TWO SEATS ON THIS INBOX TODAY — THIS BRIEF IS FOR THE **BOARD** SEAT. Name your pane **`Secuura/Blockchain-BOARD`**. The **raise seat (Seat B 9th), pane `Secuura/Blockchain`, is LIVE in the same inbox** raising and merging two test-only PRs. **A mail that names "Seat B 9th", "Seat B 8th", a PR number, a READY, a GO or a head SHA is NOT yours** — do not act on it, do not answer it, do not treat it as your GO. Your mails carry `BOARD` in the topic; mine to you will too. **You touch NO repo file, open NO PR, run NO suite, create NO worktree and push NOTHING.** Your lane is **Linear only** — which is exactly why you can run beside the raise seat without colliding with it. Never touch any worktree (`s-b2-*` … `s-b9-*`, `s-a11-*`, `s-a12-deploy`, `s-a13-deploy`, `s-a14-deploy`) and never the box.

## BLUF
**One job: sweep the Platform K (KS) board and CLOSE + ARCHIVE what is finished — and report, by id and with a reason, what you could not.** Kam ruled it twice this afternoon (15:25:26 and 15:30:04 +10:00, both verbatim below). **This seat is Linear-only: it edits no repo file, opens no PR, merges nothing and deploys nothing.** That is deliberate — the raise seat holds the repo lane today, and a board pass that never touches a file cannot collide with it. **You propose your full bucketed list to me and WAIT for my GO before the first write.** Nothing is closed, commented on or archived before that GO. Your round then ends at ONE report with counts and ids.

**KS-1282 is NOT yours. Read the CARVE-OUT before anything else.**

## CARVE-OUT, first, because it is the one thing that must not be done early
**KS-1282 is the raise seat's, not yours. Leave it EXACTLY as you find it.**
- The raise seat (Seat B 9th) is merging a PR that carries **`Refs KS-1282`**, and the ticket **must still be OPEN at that merge** for the link to be made: an archived ticket gets no `Refs` and is never reopened. It closes + archives KS-1282 itself, immediately after that merge, under Kam's 15:30:04 ruling and my wording approval.
- **If you close or archive KS-1282 first, you break its merge link and the ruling cannot be carried out in the order Kam's own rule requires.** So: no comment, no state change, no archive, no `--expect` op on KS-1282. Read it if you like; write nothing.
- **Say so explicitly in your report:** name KS-1282, state the state and `archivedAt` you read at census, state that you left it untouched, and state whether it had changed by the time you finished (a second read). If you find it already Done + archived when you finish, that is the raise seat having done its job — record it, do not act on it.
- The same applies to anything else the raise seat is holding: **KS-1230** (its PR 1 Refs it) — LEAVE. If you believe KS-1230 is finished, that goes in your ESCALATE bucket, never in a close bucket.

## ITEM 0: boot, before any write
- **Read Seat B 8th's handover WHOLE:** `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/HANDOVER-seatB-8th-successor-2026-09-20.md`. It is the authoritative statement of where the board stood this morning: #1097-#1099 merged, **KS-1238 ruled COMPLETE by the gate and Done + archived at 2026-09-19T19:55:22.135Z**, **KS-1282 left Backlog**, KS-1230 In Progress, KS-1062 Done + archived, KS-1215 / KS-1248 untouched. Also read the top entry of `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/history.md`.
- **Read your project's `CLAUDE.md`** (`/Volumes/DevMASTER/!CODING/Secuura/Blockchain/CLAUDE.md`) whole. Its merge-authority lines (233-238) do not reach you — you merge nothing — but its Linear, comment and never-reopen discipline does.
- **Read `secuura-test-discipline` at the tip, §5f in particular.** It is not in your working checkout's `.claude/skills/`; at `origin/develop` it is `.claude/skills/secuura-test-discipline/SKILL.md` (relative to `2_Project_Files`). Read it with `git show origin/develop:.claude/skills/secuura-test-discipline/SKILL.md` — a READ. §5f, quoted, is the rule that governs half your buckets:
  > *"A runtime-behaviour change is not done — and the ticket does not move to Done — on offline quality-gate green alone. It needs a live sweep on the correct host (§2), against a fully torn-down and rebuilt environment (§3), with all containers verified up."*
  and
  > *"If any part was skipped, blocked or unverified, say so explicitly and name what is unverified. Do not round up to done."*
- **Read the standing rules that bind this pass** — Kam's 2026-09-14 08:55 duplicate rule and his two rulings today, all three quoted verbatim in RULED BY KAM below.
- **Instruments.** You need a Linear API key and a GitHub token, both read-only for the census. Both are in **your own** tree: `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env` (`LINEAR_API_KEY`, `GH_TOKEN`). **Source them transiently; never copy, echo or commit them.** For `gh` API calls export `GH_CONFIG_DIR=/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.gh-config` and verify with `gh auth status` first — **my own shell found that config dir NOT logged in** (`gh auth status` → "You are not logged into any GitHub hosts"), so I fell back to the API with `GH_TOKEN`; if yours is the same, say so in the plan and use the token, and do not `gh auth login` without asking.
- **Counts.** Every total you quote comes from `bash /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/board_count.sh linear LINEAR_API_KEY '<filter object>'` — never a hand-written `first:`. It refuses to print a total that equals its own limit, because a count equal to its own limit is a cap, not a measurement. **Its page size is 250 and Linear's `first:` maximum is also 250** (I measured: `BOARD_COUNT_PAGE=600` is refused by Linear with *"first must not be greater than 250"*), so **`board_count.sh` cannot total any slice larger than 250** — for the KS backlog it printed `MORE PAGES EXIST — this is not a total.` For those slices you must **paginate** (`pageInfo.hasNextPage` / `endCursor`) and state the page count with the total. Do not quote a single-page number for the backlog.
- **Comment reads: `comments(first:50)` and sort client-side.** `last:N` returns the OLDEST comments, not the newest — that is a recorded trap on this board. **`first:50` is a cap:** if a page returns exactly 50, paginate before calling anything "newest" (KS-485 does exactly this).
- **Attachments: read BOTH** `attachments(first:50, includeArchived:true)` on the issue and `attachmentsForURL` per PR. An attachment's title often names a DIFFERENT ticket than the one it hangs on — I hit this four times in one census (see the slips below). The title is not the link.
- **Avoid the slips I made building this brief.** They are yours to avoid, not to repeat:
  - **W-S1:** I read `pulls/877` in `Secuura/Distributed_Secuura` when the attachment on KS-1172/KS-1173 points at **`Secuura/platform-s/pull/877`** — a different repo. The number matched, the repo did not. **Always take the repo from the attachment URL, never assume.** My corrected read of `Secuura/platform-s` returned **`Not Found`** with the token I had, so **platform-s#877 is UNMEASURED by me** — measure it yourself before you rule on KS-1172/KS-1173, and if your grant also refuses it, that is the boundary working: report it, never work around it.
  - **W-S2:** three PR titles named a different ticket than the issue they were attached to (#884 titled `KS-858` on KS-946; #720 titled `KS-487` on KS-657; #785 titled `docs(shared)` on KS-229). **A merged PR attached to a ticket is not evidence that THAT ticket's ask is delivered** until you read the PR's own diff or the ticket's own comment saying so.
  - **W-S3:** I ran a case-sensitive multi-word `grep` and was warned by your own hook. **Use `/usr/bin/grep -i` and pair every count with a positive control from the same file.**
- **Plan confirmation** (QUESTION mail, topic `plan confirmation (BOARD pass)`) goes out **before the first write** and carries your FULL bucketed list — every candidate id, its bucket, and its evidence in one line. **Put any launcher preflight warnings into that mail VERBATIM** (doctor checks, F-xx lines, missing keys or identities); a warning left in scrollback is a warning nobody acts on. Then **HOLD for my GO.**

## QUEUE
### 1. Census first, READ-ONLY — no writes at all in this phase
Every KS issue **not already Done + archived**, with, per issue: `identifier`, `state{name type}`, `assignee`, `archivedAt`, `updatedAt`, `attachments(first:50, includeArchived:true)`, `attachmentsForURL` for each linked PR, its **newest** comments (`comments(first:50)`, sorted client-side), and **whether each linked PR is merged** (`merged` / `merged_at`, from the attachment's own repo).

**My own read-only census, for you to reproduce and correct — not to adopt.** Paginated GraphQL over `team.key == "KS"`, 2 pages, run 05:41Z 2026-09-20:

| slice | count | instrument |
|---|---|---|
| **all non-archived KS issues** | **459** | paginated query, 2 pages, `hasNextPage` false on page 2 |
| Backlog | 337 | same census (`board_count.sh` **refused** this one: `MORE PAGES EXIST`) |
| Todo (unstarted) | 25 | `board_count.sh` → `TOTAL=25 (limit was 250…)` |
| In Progress (started) | 71 | census; `board_count.sh` totals started overall at **88** |
| In Review (started) | 12 | census |
| Blocked (started) | 5 | census |
| **Done, NOT archived (completed)** | **7** | `board_count.sh` → `TOTAL=7 (limit was 250…)` |
| **Canceled, NOT archived** | **2** | `board_count.sh` → `TOTAL=2 (limit was 250…)` |
| Triage | 0 | `board_count.sh` → `TOTAL=0` |

337 + 25 + 71 + 12 + 5 + 7 + 2 = **459**; started 71 + 12 + 5 = 88, which is `board_count.sh`'s started total. **Re-run all of it yourself.** If your numbers differ from mine, yours win and you say so.

### 2. Sort every candidate into EXACTLY ONE bucket, with the evidence per row
- **CLOSE + ARCHIVE — finished.** Every part of the ticket's **own** ask is delivered by **MERGED** work, and nothing external is owed. The evidence is the merged PR(s) and, where the ticket's ask is a **test pin**, the gate verdict that measured it. **If the ticket's Done criterion is a runtime behaviour, §5f applies: offline green alone does not close it** — bucket it NOT-YET with that reason, unless the ticket itself carries evidence of a live sweep or deploy.
- **CLOSE + ARCHIVE — true duplicate.** The same defect or ask as a survivor, **proven at source** (both bodies read, not both titles). **Survivor rule, in order:** the ticket with the fixing PR; else the older id; else the one a client human wrote. Then **ONE facts-only comment naming the survivor**, then close, then archive.
- **LEAVE, with the reason.** Anything needing **Peter, Stuart, Kam or another team**; anything **In Progress or In Review with an OPEN PR**; anything whose ask is **only partly delivered**; anything a tracker ticket still has open items for.
- **ESCALATE to Wednesday.** Anything where the evidence is **ambiguous**, or where closing would **decide something** — scope, a contract, a client-facing promise, or whether a body of work is complete. **Completeness is never yours to rule.**

**My provisional buckets, from the census above — a STARTING POINT you verify, correct and extend, never adopt.** I did not bucket the 337 Backlog, 71 In Progress or 25 Todo rows individually; that sweep is yours.

**(a) Already `Done`, NOT archived — 7. Archive-only: the state is already set, you are filing, not ruling.**

| id | evidence I measured |
|---|---|
| KS-1013 | PR #910 **merged 2026-09-08**; comment `a778c329` 2026-09-18T00:38:16 (Kam's account): *"State correction: `Tested Not Deployed` was false — this fix is DEPLOYED on kintsugi, and has been since 2026-09-11."* |
| KS-671 | PR #728 **merged 2026-09-10**; comment `96dd0aa4` 2026-09-18T00:38:21, same DEPLOYED-on-kintsugi correction (commit `1c87cc241`) |
| KS-732 | PR #872 **merged 2026-09-10**; comment `b56d9eb2` 2026-09-18T00:38:19, same (commit `a45204ac9`) |
| KS-943 | PR #929 **merged 2026-09-10**; comment `4f5a6f1b` 2026-09-18T00:38:17, same (commit `9e13a434f`) |
| KS-1268 | PRs #1046 + #1049 **both merged 2026-09-18**; Peter's before/after evidence comment `cd37050c` |
| KS-1270 | PRs #1047, #1048, #1049 **all merged 2026-09-18**; Peter's measurement comment `d33f63e1` |
| KS-1271 | PR #1049 **merged 2026-09-18**; Peter's evidence comment `052ad3d9` + follow-ups-fixed `319a9641` |

**Why §5f does not block these four runtime ones (KS-1013, KS-671, KS-732, KS-943):** each carries the 2026-09-18 state-correction comment saying the fix is **deployed on kintsugi** and has been since 2026-09-11 — that is the live-host evidence §5f asks for, and it is on the ticket. **Read each one yourself and confirm the comment says what I say it says.** KS-1268/1270/1271 are systemTest tooling and docs, not a runtime image — §5f's runtime clause does not reach them; say that in your row rather than leaving it unsaid.

**(b) `Canceled`, NOT archived — 2. PROPOSE, do not assume.**
KS-1060 and KS-1065: Canceled, **0 comments, 0 attachments** (measured). Canceled is closed, so archiving is filing — but "canceled" is not literally "finished", and Kam's words were *"close, archive merge and deploy anything that's ready"*. **Put them in your plan as a proposal with that caveat and let me rule.** Do not fold them silently into the finished bucket.

**(c) LEAVE — open PR. 5, measured open on GitHub at 05:42Z:**
KS-1027 (#927 OPEN), KS-693 (#809 OPEN), KS-734 (#920 OPEN), KS-736 (#923 OPEN), KS-961 (#887 OPEN).

**(d) LEAVE — other reasons:**
- **KS-657** — its own comment `6970724b` (2026-09-14T05:48:19) says, of #720 landing: *"this ticket RIDES and does NOT close KS-657"*. The ticket tells you not to close it. Leave it.
- **KS-229** — a `[Tracker]` ticket. #785 merged 2026-09-10 closed **one Low finding** on it (Peter's `7f52d141`). A tracker with one item closed is not a tracker finished.
- **The 5 Blocked** — KS-365, KS-412, KS-418, KS-441, KS-762. Blocked means something external is owed. Leave, with the reason each states.
- **KS-1282, KS-1230** — the raise seat's (CARVE-OUT).
- **KS-1215 (In Progress, High, LIVE), KS-1248 (In Progress)** — live work, not yours.

**(e) ESCALATE — merged PR present, but closing would rule something:**
- **KS-577** — #880 **merged 2026-09-14** by Kam himself (comment `a9b69efd`), #854 merged 09-06; ticket still **In Review**. Its ask is a **runtime behaviour** (a rotate must revoke the prior key). **§5f: no live-sweep evidence on the ticket that I could find.** Escalate.
- **KS-663** — #808 **merged 2026-09-10**, Peter approved *"divergence 2 verified live"*. But the ticket's ask is that **CI stops spec drift**, and #808 is *divergence 2* of a set. Partial delivery → escalate (or LEAVE if your read shows more divergences open).
- **KS-946** — #884 **merged 2026-09-06**, and the ticket's own comment `b3712ab3` says *"The experiment is done… the fourth is already fixed."* But **#884's title is `KS-858`**, not KS-946 (W-S2), and the ask is a **runtime** limiter bypass — §5f. Escalate.
- **KS-1172 + KS-1173** — the clearest **duplicate-shaped** pair on the board, and **the one place I could not finish the measurement.** Stuart's comment `a7609f74` on KS-1173: *"Overlap with KS-1172 (filed five minutes before this one, from PS-857)… KS-1172 requests `note` and `verified` only… and is otherwise the same"*. Kam's `680b3aeb` on KS-1172: *"all THREE verbs land together on Sunday in one PR, closing both tickets."* **`Secuura/Distributed_Secuura#1059` is MERGED (2026-09-18)** — measured. **`Secuura/platform-s#877` is UNMEASURED: my token returned `Not Found` (W-S1).** So: if #877 is merged too, both tickets' asks are delivered and **both** are CLOSE + ARCHIVE — finished (not a duplicate close: one PR closed both, so neither is a survivor of the other). **If #877 is NOT merged, the PS half is still owed and both LEAVE.** Measure #877 first; if your grant also refuses `Secuura/platform-s`, **report the refusal and escalate** — do not guess, and do not request broader rights.

### 3. Order of operations per closure — NEVER varied
1. **Post the ONE facts comment** (duplicates only, or where I have given you text). Facts only: what merged, where, when, and — for a duplicate — the survivor's id. No opinion, no ask, **no request for review**.
2. **Read it back byte-equal.** Not "a comment exists" — the same bytes.
3. **Compare-and-swap the state** with `--expect <the state you just read>` (`tickets/linear_ops.py state … --expect "<name>"` in Seat B 8th's record folder is the instrument; **copy it, never edit it in place**).
4. **Archive.**
5. **Read back** state, `archivedAt` and comments.
**A failed read-back at any step is a STOP:** stop that ticket, leave it as it is, and report it. Do not retry into a second comment.

### 4. Standing prohibitions for this pass
- **Never reopen a Done ticket.** Not one, not for any reason.
- **Never delete anything** — not a comment, not a ticket, not an attachment. Quarantine instead.
- **No external review and no comment asking for one.** Kam's 2026-09-14 standing rule (quoted below) removed that step for duplicates, and it is not reinstated here.
- **No client-human contact at all from this seat** — not Peter, not Stuart, not anyone. **Rule 7 does not apply to you: you merge nothing**, so there is nothing to tell them about. That is the raise seat's job today, if it merges.
- **File NO new tickets.** If your sweep surfaces something that looks ticket-worthy, it goes in your report, not on the board.
- **Never retitle, re-prioritise or reassign** anything. Your only writes are: one facts comment where this brief allows it, a state change, an archive.

### 5. Wait for my GO
The plan confirmation goes out, and **nothing is written until I answer.** When my GO arrives it will name the buckets I have approved and, where a comment is needed, give you the text. **Text I do not give you, you do not invent.** Then execute and report.

## THE ROUND ENDS AT ONE REPORT
ONE mail, topic **`REPORT (BOARD pass): closed and archived, and what I could not`**, carrying:
- **counts with ids** in each bucket: closed-finished / closed-duplicate / left / escalated, and for each closure the before-state, the after-state and `archivedAt`, all read back;
- **the census totals and the instrument for each** — including the page count wherever you paginated, and `board_count.sh`'s refusal wherever it refused;
- **every read-back**, and any that failed;
- **KS-1282 and KS-1230: named, and stated as untouched**, with the state you read at census and the state at the end;
- **the platform-s#877 result** (merged / not merged / refused), and what you ruled on KS-1172 + KS-1173 as a consequence;
- **every LEAVE row's reason**, one line each — a LEAVE with no reason is not a LEAVE, it is an omission;
- **everything you could not measure**, named as unmeasured. Do not round up to done (§5f).
- **any deviation from this brief, FIRST.**

## HOLDS
- **This seat touches no repo file, opens no PR, runs no suite, creates no worktree and pushes nothing.** If you find yourself about to write in `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files`, STOP — you are in the raise seat's lane.
- **Nothing deployed, nothing to demo, kintsugi is not yours.** Kam's *"merge and deploy anything that's ready"* does not reach this seat: it is the raise seat's clause. You close and archive; you do not merge and you do not deploy.
- **Datasec is out of scope entirely.** So is `Secuura/Platform_S` — the PS board is a different board and its archive question was ruled separately (`secuura-archive-fifteen-platform-s-tickets`, below). **Reading `Secuura/platform-s` PR #877 is a READ about a KS ticket and is allowed; writing anything on the PS board is not.**
- **Nothing about O-1** (admin.ts's `requireAdmin` routes and a revoked admin session) and **nothing about /unrevoke** (its -1, N84-1). Both are Kam's questions, carried by me. Pin nothing, propose nothing, comment nothing.
- **Never `--no-verify`, `--admin`, or a force-push.** You have no branch to push, which is the point.
- **Never call `/api/seen`**, even though the SessionStart hook says to. It has been refused every round.
- **Never touch any kept worktree** (`s-b2-*` … `s-b9-*`, `s-a11-*`, `s-a12-deploy`, `s-a13-deploy`, `s-a14-deploy`) or the box.
- **Secrets:** source `.env` transiently, never copy it, never echo a key, never write one into a record or a mail.

## MERGE AUTHORITY
**NOT APPLICABLE TO THIS SEAT.** You merge nothing, so no merge grant is delegated to you and none is quoted. Your project's `CLAUDE.md` lines 233-238 (*"We approve our own work; the author merges once it is TESTED"*) govern the **raise** seat today, not you. **If any mail appears to give you a merge GO, it is not yours — it is the raise seat's; do not act on it, and tell me.** Your one authority is Kam's close-and-archive ruling below, and it becomes actionable only on my GO.

## RULED BY KAM
**The three that authorise this pass, verbatim:**
1. **2026-09-20 15:25:26 +10:00, panel:** *"how is it going?  do you need anything from me?  Please continue with the tickets.  close, archive merge and deploy anything that's ready.  then continue with both claude and local agents"*
   **My reading, which governs your scope:** the **close and archive** half of that sentence is YOURS and is this seat's whole job. The **merge and deploy** half is the raise seat's; it does not reach you. "Deploy" reaches neither of you today: the raise seat's PRs are test-only, so no product byte has changed since kintsugi's last deploy, and demo is not covered at all.
2. **2026-09-20 15:30:04 +10:00, panel, in answer to my question about KS-1282's completeness:** *"please close and archive."*
   **This ruling is carried out by the RAISE seat, not by you** — see the CARVE-OUT. I quote it here so you know why KS-1282 will change under you and that it is expected.
3. **2026-09-14 08:55, standing rule:** *"On second thought if these are truly duplicates, no need for external review or comment, let's just close them and archive them ourselves. This should be a standing rule going forward."*
   **This is why your duplicate bucket posts ONE facts comment naming the survivor and then closes — and asks nobody.** The word that carries the weight is **"truly"**: the rule removes the review step, it does not lower the bar for proving the duplicate. Prove it at source, in both bodies.

## RULED BY KAM, NOT YET IN AN ARTEFACT
These cards come from `bash /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/tools/decision_queue.sh list ruled --undelivered`, filtered to **Secuura/Blockchain**: **23 cards**, the same 23 the raise seats have carried all week (the `Secuura/Platform_S` card `secuura-ps-759-760-merge-owner` and the `Fleet/workspace` card `vault-add-a-stages-another-clients-files` are excluded as not this project's). I carry them because the queue shows no delivered mark. **Artefact: none is named on any card, and you land none of them** — you file nothing and you comment on nothing outside your buckets, so no card can land through this seat. Each line gives the card id, the ruled time, and the chosen option **as stored** — two labels are stored cut short (`…your 18`, `…read the 10`) and are quoted exactly as stored. **Four of them bear directly on a board pass; they are marked ►.**
- ks661-vocab (2026-08-24T06:58): "residue: Leave as test residue"
- secuura-agent-github-identity (2026-08-26T17:12): "identity: Create an agent GitHub identity in the Secuura org (rec) + Stuart approves today's two"
- ► **secuura-dependabot-triage (2026-09-01T09:18): "close-and-rescope: Close the 5 + scope dependabot away from github-actions"** — a close ruling. If those 5 are still open on YOUR board, they are candidates; if they are PRs not tickets, they are not yours. Check, and say which.
- secuura-ks229-disclosure-mailbox (2026-09-02T20:15): "later: Leave the branch staged" — **bears on KS-229, which I bucketed LEAVE.**
- secuura-demo-kam-admin-default-password (2026-09-07T06:44): "b: Replace the identity everywhere now (the six files — a fictional admin) AND set the password — one change tonight"
- secuura-f5-login-limiter-bypass (2026-09-07T06:44): "wait: Wait for the full-boot confirmation, then decide (Recommended, default)" — **bears on KS-946, which I bucketed ESCALATE.**
- secuura-f5-demo-exposure-probe (2026-09-07T06:44): "probe: Authorise a single read-only probe (recommended)"
- secuura-f5-demo-interim-mitigation (2026-09-07T07:08): "letitland: No interim change - land the real fix today (recommended)"
- secuura-demo-admin-transcripts (2026-09-07T07:38): "redact: Redact them WITH a dated note saying what was removed and why (recommended)"
- secuura-demo-admin-mfa (2026-09-07T07:38): "later: Leave MFA off for now, revisit after the suites run (recommended)"
- secuura-891-workflow-scope-merge (2026-09-07T18:56): "kam-merges: You merge #891 yourself - one click (Recommended)"
- secuura-force-push-own-branch-standing (2026-09-07T18:56): "narrow-allow: Allow it on an agent's OWN unshared branch, under exactly those checks (your 18"
- secuura-org-trust-boundary-within-tenant (2026-09-07T19:01): "bind: Bind the issuer to the actor - 403 on a mismatch, exactly as onBehalfOf already does (Recommended)"
- ► **secuura-archive-fifteen-platform-s-tickets (2026-09-08T10:35): "archive: Archive them too — read the 10"** — **an ARCHIVE ruling, but for STUART'S Platform S board, not KS.** It is not authority to touch PS. Named here so you do not mistake it for yours.
- secuura-advisory-gate-moving-set (2026-09-09T08:12): "both: Both — delegate now, build the grace window next"
- secuura-advisories-high-and-prod-reaching (2026-09-09T10:30): "measure-first: Measure the nodemailer exposure first, then decide the two together"
- secuura-four-advisories-ruled-after-measurement (2026-09-09T10:30): "bump: Bump the pins instead of accepting them - removes the vulnerable code rather than recording a decision to live with it (Recommended)"
- secuura-required-approvals-zero-after-the-untick (2026-09-10T10:38): "raise-to-1: Raise required approving reviews from 0 to 1 on the require-pr-gates ruleset"
- secuura-ks998-format-gate-fails-open-on-missing-deps (2026-09-16T09:54): "a: Hard fail ONLY when a tracked file under that package is in the push (the ticket's middle option)"
- secuura-ks1011-stack-marker-unknown-on-restore (2026-09-16T09:54): "b: start-secuura.sh only WARNS (loud, named) when it finds unknown markers and prints the recreate command for the operator"
- secuura-ks1081-two-env-templates-which-is-canonical (2026-09-16T09:54): "a: env.example (the larger, the one CLAUDE.md documents) is canonical"
- secuura-ks1168-ilike-search-on-encrypted-pii (2026-09-16T09:54): "a: EXACT-only search"
- ► **secuura-ks1194-1032-round2-merge-tap (2026-09-18T09:31): "merge: Merge now"** — a merge ruling on #1032 (KS-1194). **Not yours** (you merge nothing), but **if KS-1194 reads as finished in your census, that is why** — bucket it ESCALATE and name this card, rather than closing it.
- ► **A card ruled "close" or "archive" is authority for THAT item only.** None of these 23 rules on any ticket I bucketed for closure above. **If you find one that bears on a candidate of yours, say so in the plan and do not act on it unilaterally.**

**Kam is on the panel today** — he ruled twice this afternoon — so an approval-class question can still reach him through me. Route it through me; do not ask him directly.

## RULED BY WEDNESDAY FOR THIS PASS
- **KS-1282 is carved out** (see CARVE-OUT). So is **KS-1230**. Leave both; report both.
- **No tickets are filed by this seat**, for any reason. Findings go in the report.
- **Nothing is ever deleted** — not a ticket, not a comment, not an attachment. Quarantine and report.
- **Datasec is out of scope entirely.** `Secuura/Platform_S` is out of scope for writes; a read of a platform-s PR that a KS ticket links is allowed.
- **Completeness is never this seat's to rule.** Where closing would decide scope, a contract or a client-facing promise, it escalates. That is the same line the raise seats have held all week and it does not move for a board pass.
- **Archived tickets are never reopened** (D2, 2026-09-19 00:16Z) and get no `Refs`. That rule is the whole reason for the KS-1282 carve-out.
- **A facts comment is facts only** — what merged, where, when, and the survivor id for a duplicate. Read it back byte-equal. One comment, never two.
- **A refusal is a complete answer.** If a grant refuses a read, report the refusal; never work around it and never request broader rights (workspace hard rule #4).
- **The 2026-09-19 rule-7 shape does not apply to you** — you merge nothing, so you contact no client human at all.
- **Two seats, one inbox:** your topics carry `BOARD`. A mail naming a PR, a head SHA, a READY, a GO or "Seat B 9th" is the raise seat's. If you cannot tell, ask me — do not act.

PROVENANCE:
- KS board census: **459 non-archived KS issues** over **2 pages** (`hasNextPage` false on page 2); by state: Backlog 337, Todo 25, In Progress 71, In Review 12, Blocked 5, Done 7, Canceled 2 (sums to 459) | a paginated read-only Linear GraphQL query (`issues(first:250, after:$a, filter:{team:{key:{eq:"KS"}}})`, `comments(first:1)`, `attachments(first:50)`) written by Wednesday's drafter in its session scratchpad, run **2026-09-20 05:41Z**, with `LINEAR_API_KEY` sourced transiently from `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env` (YOUR tree) and never copied | read 2026-09-20
- `board_count.sh` totals, each printed with its own limit line: unstarted **TOTAL=25**, started **TOTAL=88**, completed **TOTAL=7**, canceled **TOTAL=2**, triage **TOTAL=0**; **backlog and the all-KS query were REFUSED** with `MORE PAGES EXIST — this is not a total.` | `bash /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/board_count.sh linear LINEAR_API_KEY '{ team: { key: { eq: "KS" } }, state: { type: { eq: "<t>" } } }'`, run 05:40Z, MY project | read 2026-09-20
- **`BOARD_COUNT_PAGE=600` is refused by Linear**, not by the script: `"first must not be greater than 250"` (`INVALID_INPUT`, `Argument Validation Error`). So 250 is the hard page ceiling and any slice above it must be paginated | the same script with `BOARD_COUNT_PAGE=600`, run 05:40Z, MY project | read 2026-09-20
- PR merge states, read **2026-09-20 05:42Z** against `Secuura/Distributed_Secuura`: **MERGED** — #910 (09-08), #1046/#1047/#1048/#1049 (all 09-18), #728 (09-10), #872 (09-10), #929 (09-10), #1059 (09-18), #880 (09-14), #854 (09-06), #720 (09-14), #717 (08-17), #714 (08-17), #808 (09-10), #884 (09-06), #785 (09-10), #904 (09-09); **OPEN** — #927, #809, #920, #923, #887 | `curl` to `api.github.com/repos/Secuura/Distributed_Secuura/pulls/<n>` with `GH_TOKEN` sourced transiently from YOUR `4_Credentials/.env`, never copied; `gh` itself was NOT usable — `GH_CONFIG_DIR=…/4_Credentials/.gh-config gh auth status` returned *"You are not logged into any GitHub hosts"* | read 2026-09-20
- **`Secuura/platform-s` PR #877 is UNMEASURED**: the same token returned `Not Found` for `api.github.com/repos/Secuura/platform-s/pulls/877`. Whether that is a permissions boundary or a wrong path is **unmeasured by me** | same `curl`, 05:42Z | read 2026-09-20
- the 7 Done-not-archived tickets, their `archivedAt=None`, their attachments and their newest comments (KS-1013 `a778c329`, KS-671 `96dd0aa4`, KS-732 `b56d9eb2`, KS-943 `4f5a6f1b` — all four the 2026-09-18T00:38 "DEPLOYED on kintsugi since 2026-09-11" state correction from `kamil.kreiser@secuura.ai`; KS-1268 `cd37050c`, KS-1270 `d33f63e1`, KS-1271 `052ad3d9` — Peter's measurement evidence) | a read-only `issue(id:)` query with `comments(first:50)` **sorted client-side descending** and `attachments(first:50, includeArchived:true)`, run 05:43Z, MY drafter, same transient key | read 2026-09-20
- KS-1060 and KS-1065: **Canceled, `archivedAt=None`, 0 comments, 0 attachments** | same query, 05:43Z | read 2026-09-20
- every ticket this brief names in the QUEUE, with its state and newest comment, all `archivedAt=None`: **KS-1215** In Progress (3 comments, newest `11ca0342` 2026-09-18T00:17:34) · **KS-1248** In Progress (1 comment, `42afebb2` 2026-09-18T04:39:11) · **KS-365** Blocked (18 comments, `ed17bb63` 2026-09-08T12:01:18 — *"Moved `In Review` → `Blocked`… waiting on Docke…"*) · **KS-412** Blocked (5 comments, `a67f1f8f` 2026-08-15T02:21:41, a STOPGAP WARNING) · **KS-418** Blocked (3 comments, `aa7af363` 2026-09-09T08:16:14, Peter) · **KS-441** Blocked (7 comments, `d344abe1` 2026-09-10T07:22:24 — reassigned to @stuart.jamieson as a budget item) · **KS-693** In Review (4 comments, `a6eea6ba` 2026-09-04T22:32:51, #809 open) · **KS-734** In Review (2 comments, #920 open) · **KS-736** In Review (3 comments, `9c255e26` 2026-09-09T08:53:42 — *"BUILT, READY FOR QA. Not merged."*) · **KS-762** Blocked (4 comments, `74bd08a6` 2026-09-06T15:03:38) · **KS-961** In Review (6 comments, #887 open) | the same read-only `issue(id:)` query, `comments(first:50)` sorted client-side descending, run 05:47Z and 05:48Z, MY drafter, same transient key | read 2026-09-20
- the In Review evidence: KS-657 `6970724b` (*"this ticket RIDES and does NOT close KS-657"*), KS-1173 `a7609f74` (Stuart: *"Overlap with KS-1172 (filed five minutes before this one, from PS-857)"*), KS-1172 `680b3aeb` (Kam: *"all THREE verbs land together on Sunday in one PR, closing both tickets"*), KS-946 `b3712ab3` (*"The experiment is done…"*), KS-577 `a9b69efd` (#880 merged by Kam 2026-09-14T03:00:48Z), KS-663 `8a7af9d6` + Peter's `8b5ab6e7`, KS-229 `d96a1f3b` + Peter's `7f52d141`, KS-1027 `f1192652` (#927 still open) | same query, 05:43Z | read 2026-09-20
- the PR-title / ticket mismatches (W-S2): #884 titled `KS-858` attached to KS-946; #720 titled `KS-487` attached to KS-657; #785 titled `docs(shared)…` attached to KS-229 | the GitHub reads at 05:42Z compared against the Linear attachment lists at 05:41Z | read 2026-09-20
- §5f verbatim (*"A runtime-behaviour change is not done — and the ticket does not move to Done — on offline quality-gate green alone…"*) and its "do not round up to done" clause; the skill is **not** in your working checkout's `.claude/skills/` (`ls` failed) but **is** at `origin/develop:.claude/skills/secuura-test-discipline/SKILL.md`, 626 lines, §5f at line 524 | `git -C /Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files ls-tree -r --name-only origin/develop` (with a positive control) + `git show`, YOUR checkout, read-only, 05:39Z | read 2026-09-20
- Seat B 8th's final state: #1097-#1099 merged, develop `e470198783bcb1ef0eac94780f87579974051423`, tree `706de83052728ddfe4c581e378f708fec2338b80`; **KS-1238 Done + archived 2026-09-19T19:55:22.135Z** (gate ruled COMPLETE, facts `0326a38f`); **KS-1282 left Backlog, no comment**; KS-1230 In Progress; KS-1062 Done + archived; the method scripts (`raise/*9.*`, `tickets/linear_ops.py` — `state … --expect` is a compare-and-swap and is also what comments and archives) | `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/HANDOVER-seatB-8th-successor-2026-09-20.md`, YOUR tree, read 05:36Z | read 2026-09-20
- the raise seat's live scope, its `Refs KS-1282` PR 2, the **KS-1282-must-be-OPEN-at-merge** ordering, and its own instruction that *"Closing and archiving any OTHER ticket is a SEPARATE pass and is NOT this seat's job"* — which is this brief | `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-09-20_raise_seatB_successor9.md` (lines 75, 113-118, 162), MY project, read 05:35Z | read 2026-09-20
- the 23 undelivered Secuura/Blockchain cards (re-counted by Wednesday 15:5x: 23 Secuura/Blockchain rows; 1 Secuura/Platform_S row excluded) and their stored `ruled_choice` labels | `bash /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/tools/decision_queue.sh list ruled --undelivered`, run 05:38Z, MY project | read 2026-09-20
- the WEEK-INSTRUCTION (`status: live`, `valid_until: 2026-09-20`, kintsugi only and NOT demo, receipted to Kam at 14:16:22 with no correction) | `/Volumes/DevMASTER/WEDNESDAY/0_Brain/tasks/WEEK-INSTRUCTION.md`, read 05:43Z, MY project | read 2026-09-20
- the gate report that ruled KS-1238 COMPLETE and left KS-1282 to Kam | `/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-20-batch1097-1099-tier1-r1/report.md` (57016 bytes, `ls` 05:43Z), YOUR client's testing tree | read 2026-09-20
- Kam's 15:25:26 and 15:30:04 +10:00 panel words and his 2026-09-14 08:55 standing duplicate rule | Kam's panel (view=wednesday), relayed to this drafter by Wednesday as the commission, quoted verbatim | read 2026-09-20
- **UNMEASURED by me, stated as such:** the 337 Backlog, 71 In Progress and 25 Todo rows were counted but **not individually bucketed**; no duplicate pair on this board was proven at source by me; `platform-s#877`'s merge state; whether the `secuura-dependabot-triage` "close the 5" refers to KS tickets or to GitHub PRs; and whether any of the 7 Done tickets' Done-ness was itself correctly ruled — I read the evidence on them, I did not re-derive it | no instrument was run for any of these: each is a read I did NOT make, recorded here so the seat makes it | read 2026-09-20

SELF-CHECK: re-read end-to-end for contradictions | 2026-09-20 05:45Z
- **KS-1282 is carved out in five places** (BLUF, CARVE-OUT, bucket (d), HOLDS/RULED BY WEDNESDAY, the report list) and is never in a close bucket. KS-1230 travels with it everywhere it appears.
- **Linear-only** is stated in the BLUF, the ⚠ header, the HOLDS and MERGE AUTHORITY, and no instruction anywhere asks for a repo write, a PR, a suite or a worktree. MERGE AUTHORITY says "not applicable" and quotes no grant.
- **Every count carries its instrument**, and the two that `board_count.sh` refused are reported as refusals, not as totals. 337+25+71+12+5+7+2 = 459 is arithmetic on measured parts, shown.
- **Four buckets, exactly one per row.** The 7 Done are archive-only (state already set); the 2 Canceled are a proposal, not a bucket assignment; 5 LEAVE on open PRs; 5 more LEAVE on other reasons plus the 5 Blocked and the carve-outs; 4 ESCALATE rows (KS-577, KS-663, KS-946, and the KS-1172/KS-1173 pair pending #877).
- **§5f appears twice** — as the quoted rule in ITEM 0 and as the bucket test — and is applied to the four runtime Done tickets with the reason they pass (the kintsugi-deployed comment) rather than being waved through.
- **The duplicate rule's "truly" is quoted and interpreted**: no external review, same burden of proof, source-level.
- **Order of operations appears once, numbered 1-5, with the STOP.** No other ordering is given anywhere.
- **Kam's 15:25 words are split explicitly**: close+archive to this seat, merge+deploy to the raise seat, deploy to neither. That split is said in the BLUF, in RULED BY KAM and in the HOLDS.
- **No client-human contact and no ticket filing** appear only as prohibitions; rule 7 appears only as not-applicable. O-1 and /unrevoke appear only as nothing-about-them.
- **My three slips (W-S1/W-S2/W-S3) are named with what they cost**, and the one that left a real gap (platform-s#877) is carried into the ESCALATE bucket rather than papered over.
