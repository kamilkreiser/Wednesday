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
   🔴 **AND THAT PREFIX RULE IS NOT ENOUGH — s150's own heuristic failed on its first hard case at
   09:28.** A gate verdict arrives as **`[QA -> Wednesday] Secuura KS-969 / #892 round 5 — GO WITH
   FINDINGS`**: the arrow prefix carries **no client at all**, so a prefix-only tagger leaves it
   unclassified — and a DATASEC gate verdict looks identical at the prefix. **Classify on the subject's
   CONTENT, not only its arrow:** the client, ticket key or PR number named in the line (`Secuura`,
   `KS-`/`PS-` = the Studio's; `Datasec`, `RD-`, `VSP-` = this seat's). **The arrow says who is
   speaking; only the body of the subject says whose work it is.**
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

## 08:5x — DOCTOR RUN CLEAN, and one check that cries wolf (s150)
`doctor.sh` run in full at 08:44. **The rule-3c ledger check Kam approved at 07:07 IS live and
passing** — `✓ ledger archive: no rows older than 2026-09-05`. **s150 first reported it MISSING; that
was `head -40` truncating the output at line 40 when the check prints at 41.** A cap read as an
absence — see the new lesson below.
**Also confirmed by doctor, and it settles a line s150 had hedged:** `Kam's week-scoped merge + deploy
+ PRODUCTION grants live until 2026-09-13 (production: SECUURA ONLY, confirmed by Kam 12:10)`.
**So the Secuura-only narrowing is HIS, not the predecessor's reading.** Datasec production stays
ungranted; s150's earlier "treat as ungranted until he says otherwise" was right but over-hedged.

🟡 **A CHECK THAT CRIES WOLF, noted not fixed:** the exec-bit warning lists 10 paths. **Measured: only
5 of ~120 `fleet/state/launch_qa_*.sh` lack the bit, and all 5 are SPENT one-shot launchers that will
never run again.** The rest of the list is a quarantine copy, a `TESTCOPY`, two
`(conflict_on_2026-09-04)` files and an Obsidian plugin inside a worktree — **none of which should
ever be flagged.** The real risk the 2026-08-06 lesson names (a live script failing at `nohup`
because a sync dropped its mode) does not apply to any of them. **Left alone deliberately:** it is a
scoping decision on a shared check, mid-session, on a judgement call — and `chmod`-ing spent scripts
would only hide the noise. **Candidate: scope the check to tooling that can still be invoked, and
exclude `_quarantine_*`, `*TESTCOPY*`, `*(conflict_on_*)*` and `worktrees/`.** A preflight that flags
10 items where 0 matter is the overstated-record lesson pointed at a boot check.

## 🔴 NEW LESSON FILED — read it, it is about this seat's own checking
`0_Brain/learnings/2026-09-08_a-false-absence-is-usually-my-own-instrument.md` (W tier).
**THREE instrument failures in ninety minutes, all producing a FALSE ABSENCE, all self-caught:** a
harness whose bash syntax error made all six branches read FAIL while the code was correct (the tell:
**the negative control failed too**, which is impossible if the subject is merely wrong) · a `grep`
returning 0 on text that was present because the phrase **LINE-WRAPS** — a trap documented in the very
file being edited · `doctor.sh | head -40` hiding a passing check at line 41.
**The through-line: this seat's WORK held all morning and its INSTRUMENTS kept failing, and every
near-miss was in the CHECKING rather than the doing.** Both digests regenerated (119 files); doctor
confirms current.

## 08:5x — 50% CHECKPOINT (rhythm §2, NOT a rotation — the band is 80–90%)
**Default declared: hold.** Nothing is in flight, nothing is owed, no heavy work started past this
point. S47 holds on `%22` (acked, quiet); Kam has three cards; the deploy settings are his.

### NEW CARD `fleet-cross-seat-mail-wakes-keep-or-filter` (WED, rec `leave`, default = nothing changes)
**The predecessor promised this card to the morning board yesterday and it was never filed.** Filed now.
**Measured by s150 in one action: of 12 inbound since boot, SEVEN were Secuura** — the Studio's, which
this seat must not act on. The Studio measured the mirror image (six Datasec wakes in twenty minutes,
three inside 33 seconds). **Each coordinator spends about one wake in two on the other's traffic.**
**The predecessor's note says explicitly: "this is the judgement a successor should RE-MAKE rather
than inherit."** s150 re-made it and **it holds, with evidence the predecessor did not have:** at 07:53
a Secuura deploy was in flight and the Studio had been silent in git for 41 minutes; **what proved it
alive at 08:11 was Secuura mail in the shared inbox.** A filter would have blinded this seat at the
exact moment it was asking whether the other coordinator had died. **Keep reading by SUBJECT, treat
the other client's traffic as a one-line noop, do NOT build a filter on a seat's own judgement.**

### 🟡 UNVERIFIED, and it is Kam's money so it is worth someone checking
Kam's 11:01 split ruling (2026-09-07, verbatim) gives two reasons — *"this machine is running a little
bit slow"* and *"I have an additional Claude Max account for Datasec that I will use to split the
credits across the two projects."* **The predecessor's handover recorded "ONE USAGE LIMIT" across both
Wednesdays.** If that is right, **the credit split he set the second account up for is not in effect.**
🔴 **s150 has NOT established this and cannot from here:** this seat and S47 both read `7d:37%`, which
is expected for two panes on ONE machine and says nothing about the Studio's account. **The predecessor's
"one usage limit" line is a REPRESENTATION, not a measurement s150 reproduced.** Do not report it to Kam
as fact. **The check is a single statusline read on the STUDIO machine** — a percentage differing from
the laptop's proves two accounts; an identical one is suggestive and not conclusive.

## 10:4x — 65% CHECKPOINT. THREE PANES LIVE. Kam is at the panel and ruling.
**Default: continue.** Band is 80-90; this is a checkpoint, not a rotation.

    %22  Datasec/NexusAI      S47, holding. 8/8 merged, 4 tickets closed on Kam's word,
                              RD-369 re-cut + READY, gate launched. RD-372 is NEXT, not now.
    %26  Datasec/SecurityReview  fix §7.1 -> verify the 23 -> file batch-1 -> continue.
    %27  QA/NexusAI-RD369     TIER 1 gate on `rd-369-recut-s47` @ `117931e`.
    %0   wednesday            s150.

### KAM RULED SIX THINGS THIS MORNING — all recorded, mine executed
`close-superseded` (done, 4 tickets, verified on the board with RD-384 as a control) ·
`package` (already running on %26) · `leave` (cross-seat wakes — nothing to build) ·
`scope` (**BUILT: the launcher now sends each seat to its OWN ledger**; 3 hosts exercised,
prompt tail asserted intact; backup `.pre-0908-seatledger`). Two Secuura rulings left alone.
🔴 **AND TWO STANDING INSTRUCTIONS FROM HIM:** *"fix the register section"* (running on %26 —
**given to that session rather than done by hand, because the `.docx` is what ships and only
that session can regenerate it**) and *"from now on, any work on wednesday, take ownership so
both agents dont work on the same things"* → **`2_Project_Files/tools/wed_claim.sh`, live and
red-proofed** (dup rc 3, free rc 0). **CLAIM BEFORE STARTING ANY WED WORK.**

### 🔴 RD-369 — the day's second going-backwards branch, and the biggest catch
The ticket's premise was **INVERTED at main**: it reads as residue after SEC-03/SEC-04, but
**neither is landed at main** — the whole fix sat on `rd-362 @ 920e067` at Testing. So it was
the FULL exposure, wider than filed: no guard at all at main, the `.md` report neither redacted
nor excluded (582 lines, **7 gitleaks fingerprints pinned inside it**), all five session-notes
files shipping. **Wednesday had told Kam it was partly fixed and corrected him inside three
minutes, scoped to exactly what was refuted.**
🔴 **Merging `920e067` as it stood would have DELETED two test helpers and ~700 lines of
`scheduler-failure-vocabulary.test.js` — reverting RD-376 and RD-377.** RD-304 was the same
shape twelve hours earlier. **Both caught by diffing CONTENT, not by trusting a branch name.**
**Ruled: re-cut, never re-author.** S47 did it; **Wednesday verified in its own clone: delete-set
EMPTY, the three files present, 700 lines both sides, exactly five files added.**
**Wednesday's ruling on the open judgement call: KEEP the directory-level `docs/runbooks/`
exclusion** — over-exclusion is visible and reversible, under-exclusion is silent and is this
ticket; and it fixes the class, not the instance. **It rests on S47's unverified claim that no
runbook is referenced at runtime — the gate is checking that, and a runtime reference makes it a
BLOCKER.**
**Still open and must not vanish: F3** (redaction defeated by its own context — hash one line
above the marker, key directory eleven below, 22 short-form hashes remain) **and F6** (never
re-measured).

### THE RULE THIS EARNED (ledger w=100)
**A ticket's findings carry the REF they were measured at. A ticket measured on a BRANCH describes
the branch, not the product** — re-derive at the current head before any fix. That single line in
the RD-369 brief is the only reason this surfaced in five minutes instead of after a merge.

## 10:5x — 70% CHECKPOINT. Not a rotation (band 80-90). Default: continue, bounded work only.

### 🟢 SECURITY REVIEW COMPLETE — all four items. Deliverable:
`!CODING/Datasec/Security Review/_Working/2026-09-08_FIX_VERIFY_REPORT.md`
(+ `_Working/verification-2026-09/_BATCH2_VERIFICATION_2026-09-08.md`,
`_Working/2026-09-08_ITEM4_COVERAGE_GAPS.md`, `_Working/build-doc13.sh`)
- **§7.1 FIXED in BOTH `.md` and `.docx`**, verified by reading the rendered result; deletion audit:
  **seven heading lines changed, not one body line removed.**
- **All 23 re-derived at source: 0 refuted outright · 2 down-scored · 1 aggravator refuted · 1 claim
  partly refuted · 3 strengthened. NOTHING moved up.** All three severity-gating questions CLOSED,
  all downward. **A pass that only ever confirms is a check that cannot fail — this one moved.**
- 🔴 **THE UNFILED GAP WAS 96 FINDINGS, NOT ~20** — across **15 components, not 7**, including
  **THREE Criticals never counted**. All 96 filed. **Estate 242 -> 339.**

### 🔴 THREE CORRECTIONS TO WEDNESDAY, TWO OF WHICH REACHED KAM AS FACT
1. **"roughly twenty" was a 4.8x undercount** (96), and the gap was NOT confined to batch 1 — the
   eight components §7.1 calls **"Done" have 34 unfiled findings**. *Done* meant REVIEWED, not FILED.
2. 🔴 **THE GOTENBERG EXFILTRATION PATH DOES NOT EXIST.** Wednesday escalated to Kam that D-MF-07's
   credential goes to a **service-designated** `contentLocation` and would need a rescore well above
   Low. **That was a FIELD MIX-UP in the register, already answered 2026-09-07 in this project's own
   `mailflow-main.md:325-327`.** No exfiltration path, no pdf-api question, no rescore, no live pass
   needed for it. **Wednesday relayed the register's wording without opening the file that settled it
   — and it reached Kam as a security escalation.**
3. **SecurePDF's `spdf_encode` is IN THE TREE** under a different name, not "not in the tree" as §7
   said — it cost the engagement a component's worth of coverage.
**Where Wednesday was right, per the agent: the §7.1 diagnosis, re-frame-don't-delete, REGENERATE THE
`.docx` (the `.md` alone would have been the same defect in a worse place), and the standing warning
that a verification pass which only confirms cannot fail.**

### 🔴 NEW CARD `secrev-live-pass-blocked-on-tenant` (rec `name-tenant`, default = nothing runs)
**The live pass has stopped being a coverage gap and is now costing PUBLISHED SEVERITIES** — Critical
13's rescore hangs on it and the evidence points DOWN. Blocked on the workspace CLAUDE.md's
**UNRESOLVED** Datasec tenant mapping (`fc05dcdd` vs `0c57ab37`), which says *do not assert which*.
**Wednesday held three agents off `az` today on that line and will keep doing so.** Only Kam settles it.
The gate refused this card on four priors; **all four opened**, and the closest (`secrev-verify-23…`,
ruled `package`) is the PROOF it is new — that ruling explicitly listed the live pass as OUT of scope.

### PANES
    %22  Datasec/NexusAI      S47, holding, ~65%. RD-369 re-cut READY @ `117931e`, gate running.
                              🔴 **RD-372 (High) is NEXT and should go to a SUCCESSOR, not to S47** —
                              it is at 65% and the gate may return findings it must fix. Bounded work only.
    %26  Datasec/SecurityReview  COMPLETE, holding. **A ghost sat at its prompt — `verify the 96 filed
                              rows` — detector-classified SUGGESTION, NOT actioned.** Rung 6 again:
                              it proposed the plausible next step seconds after the agent named that number.
    %27  QA/NexusAI-RD369     TIER 1 gate on `117931e`, running.
    %0   wednesday            s150 at 69%.

### 🔴 A DEFECT OF WEDNESDAY'S OWN THAT THE STUDIO SEAT FIXED (ledger w=101)
`wed_claim.sh` — the tool built FOR Kam's ownership rule — was **hardcoded to
`/Volumes/KK_T9_External_HDD/WEDNESDAY`**. On the Studio seat every write went to a nonexistent path
**and it still printed `claimed … and published`.** A check that cannot fail, in the one tool whose
job is making two seats agree. **Same defect fixed in `safe_push.sh` the day before.** The Studio made
it self-locating; s150 verified the fix on its own seat (resolver correct, `list` works, dup still
refuses rc 3). **THE RULE: a tool whose PURPOSE is cross-seat is exercised with its path resolution
FORCED to the OTHER seat's root before it is armed** — s150 did exactly that for `chat_reply.sh`'s
seat mapping an hour earlier and not for this one.

## 11:5x — ROTATION-READY. Nothing in flight. `main` = `edf1ab7`.

### STATE, all verified by s150 on the live board / `ls-remote`, not relayed
    main            edf1ab7   8 authorised merges + RD-369 fix + RD-369 round 2
    RD-369          Release Ready (High) — fix merged and PROVEN in a real built image
    RD-385          To Do (High) — tenant correspondence + staging roster SHIP to customers
    RD-386          To Do (High) — the round-2 residue (R2-A window, R2-B certifying cell)
    RD-372          To Do (High) — NOT started, routed to a SUCCESSOR, never to S47
    control         RD-372 still To Do => the closes were surgical, not a sweep

    %22  Datasec/NexusAI  S47 at ~70%, STOPPED at the cap, holding, acked. Its register stands.
    %0   wednesday        s150 at ~78%.

### 🔴 THREE THINGS ON KAM'S DESK, all with safe defaults
1. **`nexusai-rd369-round3-or-ship-at-the-cap`** (rec `round3`) — **the exposure is CLOSED and
   proven; this is only the GUARD.** It survives on a **one-line margin**: a purely cosmetic reflow
   flips 3 of 4 real RD-385 files from carrier to CLEAN, and the certifying cell asserts only `>0`
   so killing either detection path leaves it green. **Third option (NOT scoped by s150): also
   REMOVE the RD-385 files from the image — the only option that stops the identifiers shipping.**
2. **`secrev-live-pass-blocked-on-tenant`** (rec `name-tenant`) — a published Critical cannot be
   rescored while the tenant mapping is UNRESOLVED. **s150 held three agents off `az` on that line.**
3. **The three GitHub settings** — still the only unclosed part of his 07:10. Sent twice; do NOT re-send.

### 🔴 THE RULE THIS SEAT EARNED THE HARD WAY (ledger w=103) — OBEY IT
**After ANY commit touching `chat_log.json` or `decisions.json`, PARSE THE FILE OUT OF HEAD:**
`git show HEAD:<path> | python3 -c 'import json,sys; json.load(sys.stdin)'`.
**NOT `HEAD == origin`, NOT the tool's exit line, NOT another file's presence.** s150 pushed a
corrupt `chat_log` **40 minutes after the Studio warned it in writing**, because the union step
CRASHED and wrote nothing while four unrelated checks stayed green. **Those two files conflicted
FOUR times in one session.** The repair needed brace-matching intact objects out of a NESTED
conflict — a two-sided split gave two unparseable halves, and one candidate merge was **0 entries**,
which would have erased Kam's whole conversation. **Never install a union smaller than its sources.**

### THE DAY'S PATTERN, stated so a successor inherits the diagnosis and not just the rows
**Three different agents corrected s150 and every one was right:** the eight merges were not the
whole ready set · the Gotenberg exfiltration path s150 escalated to Kam **did not exist** (a field
mix-up already answered in the project's own notes) · "~20 unfiled findings" was **96** · "6
carriers" was **not reproducible**. **One root cause: relaying numbers and characterisations that
were never re-derived.** Ledger w=94/96/100 and the w=103 row. **The two things that HELD were both
pre-registered:** the brief's *re-derive at current main* requirement (caught an inverted ticket
premise) and the round-2 brief's *no round 3 without Kam* (caught s150 wanting a round it had
already forbidden itself).

