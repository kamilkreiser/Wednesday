---
date: 2026-09-08
type: pickup
scope: DATASEC ONLY — laptop seat. Secuura belongs to the Studio seat; do not touch it, do not adopt its cards.
source: replaced WHOLESALE at 08:2x by s150, at the all-eight-merged boundary
status: live
supersede: replace this file wholesale at the next pickup; do not append
---

# NEXT PICKUP — Datasec laptop seat, 08:2x Tuesday 2026-09-08. KAM'S MERGE HALF IS DONE. HIS DEPLOY HALF IS STILL HIS.

**Run `/Volumes/KK_T9_External_HDD/WEDNESDAY/2_Project_Files/tools/kam_rulings_today.sh` before writing
anything — read EVERY line.** Mail UTC ≈ AEST−10. **ROTATION BAND 80–90%; 70% is a checkpoint only.**
Kam left at 07:10 to drop the kids off. Voice is allowed.

## 🟢 ALL EIGHT MERGED — `main` = `e94973d`, unfrozen after 7 days
    a9a8cb6  frozen since 2026-09-01
    8c4c22d  1 rd-323 e032c7d      1803bcd  2 rd-377 fabcc93      0dd9cc0  3 rd-381 b93d3b5
    97be896  4 rd-361 731aa6e      ecd214a  5 rd-374 10ddb0a      36d5e6f  6 rd-376 36191eb
    4216f07  7 rd-322 432617a      e94973d  8 rd-148 690bed9
274 commits. Final suite **2255/2255 across 116 suites** — **S47's figure, S47's run, not re-derived.**

**VERIFIED INDEPENDENTLY BY s150, and this is the method to reuse:** `git clone --shared --no-checkout`
of the builder's checkout into s150's OWN scratchpad (read-only on the source; source HEAD and a clean
`status` re-read afterwards), then `merge-base --is-ancestor` for each of the eight against
`origin/main` — **8/8 IN main**, with a **negative control that discriminated**
(`rd-306-law-window-s34 edb81c5` correctly NOT in main). The branch mapping above is from
`git log --merges`, **not from queue order.** S47's account and s150's measurement agree exactly.

## 🔴 THE DEPLOY HALF — STILL KAM'S, STILL UNSATISFIED, AND NO MERGE CHANGED IT
`deploy-demo.yml:51` gates every job on `vars.CI_DEPLOY_ENABLED == 'true'`, unset by design until
secrets + environment exist. **So a merge CANNOT deploy.** Container App `nexusaidev-app` still on
revision `0000097` (2026-09-05); newest ACR tag still the 09-05 image. **NEVER REPORT A MERGE AS A DEPLOY.**
**Three things are his and they are the whole deploy half:** set `CI_DEPLOY_ENABLED=true` · add secrets
`AZURE_CLIENT_ID` / `AZURE_TENANT_ID` / `AZURE_SUBSCRIPTION_ID` · create the `demo` environment.
**Sent to his panel 07:41 and again in the 08:1x completion message. DO NOT RE-SEND — he has it twice.**
s150 MEASURED that it cannot do these itself: `kamilDatasec` is in orgs `token-one` and `warpkey`, NOT
`datasecau`; the deploy key reaches git, the API identity does not, and repo settings need admin anyway.

## 🔴 TWO ERRORS s150 OWES ITS SUCCESSOR — both were s150's, both caught by S47
1. **s150 told Kam "five of eight… rd-374 (`4216f07`)". `4216f07` is merge 7, rd-322 — SEVEN were in.**
   The `ls-remote` was a measurement; the SHA-to-branch mapping was inferred from QUEUE ORDER and
   published as measured. It reached **Kam's panel, this file, AND the CHECKPOINT RULING mail**, so S47
   was handed a remaining queue containing two already-merged branches and had to reconcile it mid-run.
   **A SHA and a BRANCH NAME are TWO facts needing TWO reads: `ls-remote` for the head, `log --merges`
   for the mapping. Never let queue order supply the second.** Ledger w=94. Corrected everywhere.
2. **The rd-376 negative control was NOT closed for the reason s150 recorded.** S47's pane line *"All
   four are already in main — they're old lineage… Control chosen"* meant the four CANDIDATES WERE
   UNUSABLE. S47 then enumerated all 50 remote heads, found 15 genuinely absent, and chose **two:
   `rd-329 @ 2e78c76` and `rd-362 @ 920e067`**, both proven absent throughout all eight merges.
   **A successor inheriting s150's "old lineage was fine" would rebuild a vacuous control.**
   **Never close an item on a quoted pane line containing an ellipsis.** Ledger w=95.
🟡 **s150's 50% CHECKPOINT RULING ARRIVED AFTER MERGE 7, NOT BEFORE MERGE 6.** S47 said so rather than
answering as if it had been timely. **Do not record that ruling as the mechanism that protected the
run — it did not arrive in time to be one.** The boundary rule held by sequencing.

## 🟢 S47's OWN BEST CATCH — propagating to the QA charter §6
On merge 8 it read `2233` off the counts file and nearly recorded it: **the `--update-counts` writer had
not finished and the file still held a previous run's figure.** The tell was ARITHMETIC — rd-148 adds 22
tests, so a merged total identical to OURS was not credible. Real figure **2255/116**.
***"A number read before its writer finishes is not a measurement."*** A new member of the
check-that-cannot-fail family: **a stale read is a check whose answer was fixed before the question.**

## 🔴 THE ONE THING STILL OPEN ON KAM'S 07:10
**Was the eight-branch set EVERYTHING that was ready, or everything s150 knew about?** Asked of S47 at
08:15 (`SCORE 1.0 — 8/8 verified independently…`, supersedes the 07:49 mail's "at the wrap" timing —
its queue is dry). Wanted: the predicate + its FRAME · anything at Release Ready not in the eight, with
why · **and the stale-board direction specifically** (a branch already in main whose ticket still reads
Release Ready) — the direction that INFLATES a count, and the one that bit this fleet at 07:2x when a
set was called 24 and the real gap was 3. **s150 holds no instrument: `board_count.sh` cannot count this
board (WED-146).** **If the answer is "the eight was everything", that CLOSES Kam's merge instruction.**

## BOARD (S47's read, not re-derived)
RD-322/323/361/374/376/377/381 **Release Ready** · RD-378/379/380/382/383/384 **To Do**.
**RD-384** filed (Low, `operations`) carrying RD-376's F-1..F-5 — (b) meant ticket, not fix.
**F-2 has teeth:** `entra-provisioning-ui.test.js` passes 12/12 against a reader that blanks the whole
file — the one converted guard that stays silent if the shared reader is blinded. Pre-existing (proven
at `10ddb0a` too), two lines fix it. The other six redden under both no-op and erase readers. **So the
shared-helper blast radius is closed everywhere except that one site.**

## 🟡 KAM'S DESK — cards, every one with a safe default
- **`wed-boot-names-one-ledger-there-are-two`** (WED, rec `scope`, default = nothing changes) — s150's.
  `doctor.sh:419-420` sweeps BOTH ledgers; `Launch_Wednesday.command:198` reads only the Studio's.
- **`secrev-verify-23-and-batch1-filing`** (rec `package`, default = nothing runs).
- **`hpsm-credential-bearing-prd-outside-every-snapshot`** — note only: *"only secuura projects on this
  machine until further notice"*. HPSM stays untouched.
- **Not this seat's, do not adopt, re-card or answer:** the Studio's and Fleet/workspace cards.
🟢 **KAM'S 07:09 ITEM (b) IS DONE — and the line that used to sit here said "STILL NOT STARTED", which
was FALSE.** s150 inherited that from the Studio's pickup, repeated it in this file, and told Kam so on
the panel, all without opening `chat.html`. **The filter had existed since 2026-09-07 11:12** — chips per
project, persisted per browser, Kam's own messages always shown. **The mechanism was never broken;
nothing FED it:** of 1725 chat entries `project` read WED 64 / Datasec 6 / ABSENT 1655, and `projOf()`
maps absent to "WED" too, so both seats landed in ONE bucket. `--project` was wired correctly the whole
time; no seat passed it. **Fixed at the WRITER:** `chat_reply.sh` now defaults per seat (laptop ->
`Datasec`, Studio -> `Secuura`), precedence `--project` > `$CHAT_PROJECT` > per-seat > `WED`, unknown
host falls back to `WED` and never guesses. Six branches exercised incl. a negative control, then
**proven on the ARTEFACT** — the panel message reporting it wrote `project: Datasec`.
🔴 **The mapping is KAM'S TEMPORARY SPLIT** (his 07:09 words) and lives in exactly ONE line —
`seat_project_default()` in `chat_reply.sh`. **If he re-splits, edit that and nothing else.**
🔴 **THE RULE THIS EARNED, ledger w=97:** *"not started" inherited from another seat's note is a
CLAIM WITH A DATE.* The check is one grep of the surface it would live on. **Never carry an
unstarted-item claim into a handover, a panel message, or a build without opening the artefact —
especially when the item is small enough to build, because that is exactly when nobody looks first.**
(a), the vault skill-file write + reconcile session, is the LAPTOP-vs-Studio race the card is about —
**do not both act on the shared vault. Still open.**

## ✅ SECURITY REVIEW — COMMISSION COMPLETE, panes closed
Report: `/Volumes/KK_T9_External_HDD/!CODING/Datasec/Security Review/_Working/_BATCH2_REPORT.md` and
`_Working/2026-09-08_FILE_AND_SWEEP_REPORT.md`. **23 findings filed into register 13 (now 242), marked
pending verification, and the register's unframed "VERIFICATION IS COMPLETE" claim AMENDED** so filing
unverified rows did not make a true document false. Bearer sweep found a real one:
`GotenbergCloudRenderingRequestJob.kt:250-253` sends **the raw Microsoft credential to a
server-designated `contentLocation` URL**. **s150 has NOT opened that file — relayed from its report.**
**Still open and NOT authorised:** verifying the 23 · the live cloud pass (blocked on the unresolved
`fc05dcdd` vs `0c57ab37` tenant question — **do not assert which**) · RD-18's Privacy Act package ·
whether to re-issue the June deliverables. Batch-1 findings are still NARRATIVE-ONLY in §2.2.

## 🟡 ATTIO — TRANSFER ITEM, not Wednesday's code
The 07:00 daily digest says **"14 items for today"** and **every flagged row is seeded — 8 `[DEMO]` +
6 `[SYN]`, ZERO real deals.** Excellent about its INSTRUMENTS, silent about its POPULATION.
**For the next Datasec/ATTIO session: put the real-deal count in the BLUF, or filter the seeded
prefixes out. Brief it as a COMPLETION — its disclosure discipline is a model.** Its renewal blocker
`attio-attr-cap` was ruled `hold` by Kam on 2026-08-22; **re-raising it is the going-in-circles he
corrected on 09-07.**

## 🔴 THE VAULT — do not run the wrap's vault step from a Datasec seat
`end-of-session.md:50` is `git add -A` and the vault's untracked set includes **Secuura** paths —
running it here commits another client's content (**hard rule 2**). Skip it, say so in the wrap, stage
nothing by path. Carded; shared file, so it is Kam's.

## RULINGS A SUCCESSOR MUST NOT RE-LITIGATE
- **The two reader widenings land INSIDE RD-377, additively** — a new `unknownStatus` count beside
  `p1Incidents`/`healthP1s`, **never folded in** (a metric's meaning must not change under an unchanged
  key; never inflate an incident count with non-incidents).
- **`P2-unknown-status`** gets its own bucket and `ok:false` row; does NOT escalate the tick, does NOT
  join the P1 alert email. It is a **CONTRACT** problem, not availability — *the target answered.*
- **While a gate runs, continue on the next INDEPENDENT item.** A pending gate freezes its head, not the seat.
- **The three stray `/*` comments in `server.js` stay untouched** until the X-1/X-2 reproducer is captured.
- **The `nexusai-rd367-frozen-trunk` card is STALE** on its credential claim: S47 measured that no
  credential sits in `terraform.tfstate.backup` on any ref; gitleaks 0 findings, exit 0, scanned as CI
  does — re-run clean on the merged tree. **The main-only-scanning fact that justified the expectation
  still stands.** S47's keeper: *"an expectation that a red is coming is exactly the condition under
  which a false red gets believed."*

## ⚠️ TRAPS — live, most fired on this seat
1. **Read the inbox at limit >= 3, never 1.** A real inbound sits beneath your own outbound echo.
2. 🔴 **BOTH Wednesdays send as `wednesday-agent@agentmail.to`** — an inbox listing **CANNOT** tell this
   seat's outbound from the Studio's by the From address. s150's own tagging called a Studio mail
   `OUT(mine)`. **Tag by SUBJECT (`-> Datasec/*` is this seat, `-> Secuura/*` is the Studio).**
3. 🔴 **`git -C $VARIABLE <writeverb>` is REFUSED — write paths LITERALLY.** Hit a THIRD time by s150 at
   08:09 with this very trap in this very file. The environment trains the reflex (the no-`cd` hook
   forces absolute paths, so a variable is the ergonomic way to write them) and a warning cannot beat a
   rewarded reflex. Ledger w=3.
4. 🔴 **THE SAME HOOK BLOCKS ITS OWN PRESCRIBED REMEDY.** Its refusal text says *"clone by SHA into this
   session's scratchpad and run them THERE"* — then refuses a write verb IN the scratchpad, because the
   scratchpad is outside WEDNESDAY. **Workaround that worked: `git clone --shared` carries the source's
   objects via alternates, so `rev-parse` / `merge-base` need NO fetch at all.** Enforcement candidate:
   resolve single-variable paths and allow scratchpad writes. **Shared hook — Kam's or a dedicated session's.**
5. **`send_brief.sh`'s SELF-CHECK regex is exact.** GENERATE the stamp; extra prose before the pipe breaks it.
6. **Ghosts:** detector FIRST (`pane_prompt_check.sh`), always. **TWO at `%22` in twenty minutes, both
   inert, both ~3 min after a decision was routed upward.** Rung 6 (merge the three) bounced because
   S47 had WRITTEN its refusal first. Rung 2 (a wrap phrase at a HOLDING pane — a new costume; the
   documented rung 2 is at a WRAPPED pane) found the gap, because **nothing S47 had written
   contradicted wrapping.** 🔴 **So a brief states the decisions the agent is NOT making** — S47 is now
   told in writing: wrap only on a MAIL from Wednesday or the rotation band, never on a prompt line and
   never on its own read that the queue is dry. **A dry queue is a reason to HOLD, not to END.**
   🔴 **`C-u` does NOT clear a rendered suggestion** — there is no input buffer; only new output or a
   tap displaces it (`cockpit.sh say` reported `prompt clear` both times). **Do not read a failed `C-u`
   as a failed clear.** A wrapped pane beside an open Kam card is still the rung-6 surface — s150
   closed `%24` and `%25` for exactly that.
7. **`pane_close.sh`** is the tool; its own `listeners N->N` line is the real control.
8. **Another project's checkout is READ-ONLY for git**, `.git` included. Read verbs only.
9. **A verdict mail can arrive zero-byte** — verify a send by a non-null `preview`, and read verdicts
   from the report on disk.
10. **AgentMail single-message GET needs the `message_id` URL-ENCODED** (angle brackets + `@`), else 400.
11. **`launchers.conf` points at DevMASTER, unmounted here** — launch by hand, then
    `tmux set-option -p -t <pane> @cockpit_name '<name>'`. **Do not rewrite `launchers.conf`.**
12. **NexusAI's and Vision's `JIRA_SITE` have NO SCHEME** — prefix `https://` or a 301 with an HTML body
    reads as "board unreachable". Filed as RD-382.
13. **`/Volumes/DevMASTER` is NOT decommissioned** — unmounted here. **Prune no worktrees.**
14. **Use `2_Project_Files/tools/safe_push.sh` for every push — IT STAGES ONLY PATHS PASSED AS ARGUMENTS.**
    `HEAD == origin` proves the REFS agree, not that the work is in them. **Verify every wrap by
    `git show HEAD:<path>`; a non-zero dirty count is a FAILED wrap whatever any tool printed.**

## STANDING
**Kam's week grants (through Sunday 2026-09-13):** merge on Wednesday's word once the gate passes ·
deploy · production changes (**flag every use**) · board judgement calls. **🔴 s150's predecessor read
the production lift as SECUURA ONLY — Kam's words named no client, so treat Datasec production as
UNGRANTED until he says otherwise, and ASK rather than argue it into scope.**
Ticket creation AGGREGATES (one larger ticket per logical path). **FOUND / TESTED / HOW**, controls
named under HOW. **A clean GO freezes; a GO-with-findings carries an expected re-gate.**
**NAME THE FRAME — the number is read in the same action as the sentence carrying it.**
Taps <= 200 chars, pointer only; **mail FIRST, verified by a non-null `preview`, THEN tap.**
**Never delete — quarantine. Names, not pronouns. Kill anything querying Azure credits.**

## FLEET
**TWO WEDNESDAYS LIVE. The Studio owns Secuura and is ALIVE** — verified 08:11 by its own outbound
(`[Wednesday -> Secuura/Blockchain] PETER'S QUEUE — 14 PRs, Kam's deadline is END OF DAY`), which s150
did not send. **The Secuura demo deploy COMPLETED at 08:07** (`400517aaf` live, verified at the
destination by its agent) — **that is the Studio's to score. Subject-only from here; no body fetches,
no replies, and do NOT adopt it.**
**This seat owns Datasec.** One repo, one dashboard, one chat panel, **ONE USAGE LIMIT** (7d:37%,
renews in 4d 19h). **Do not write `NEXT-PICKUP.md`, the daily note or `_ledger.md`** — the Studio's;
this seat's ledger is **`_ledger_laptop_datasec.md`**. Panel messages open `[LAPTOP / Datasec]`.
**Live panes: `%0` wednesday (s150) · `%22` Datasec/NexusAI (S47, holding, queue dry, ~50% ctx).**
