---
date: 2026-09-20
type: pickup
scope: SECUURA + all general/generic work. Datasec is TUESDAY's. Datasec mail by subject only.
source: replaced WHOLESALE at 16:45 2026-09-20 by the 16:0x seat (previous copy NEXT-PICKUP.md.pre-0920-1645; older blocks in NEXT-PICKUP-archive.md).
status: live
supersede: replace wholesale at the next pickup; do not append
---

# NEXT PICKUP

## ONE block (the 16:0x Sunday seat) — replace it, never append

**Kam is HERE and on the panel today**, back properly Mon 21, away again from MONDAY NIGHT 2026-09-21. `tasks/WEEK-INSTRUCTION.md` is LIVE only to the END of TODAY: merges on Wednesday's signed GO after a QA gate; deploy KINTSUGI ONLY, never demo; signature classes still pause (KS-1250, KS-1175, money, external comms beyond rule-7); auth LAST. **On Mon 21 set its `status: lapsed`, stop acting on its authority, and bring Kam the Monday list below.** Usage **83%** at 16:4x, cut 90, renews **Fri 25 Sep 8am AEST**. `night/ALLOW_SEATS` armed to tonight 23:00 (epoch 1789909200). **Merge cut-off 23:00 AEST (13:00Z) — no GO after it.**

### FLOOR at 17:52
`%0` wednesday · **`%123` Seat B 9th — MERGING under a signed GO** · `%1` fleet-monitor. The BOARD seat and the QA gate `%162` are both wrapped, scored 1.0 and CLOSED (listeners 18→18 each time, detector read before each close). develop at origin **still `e470198783bcb1ef0eac94780f87579974051423`** as of 17:51 — the first merge had not landed yet.

### 🔴 FIRST ACTS
1. `kam_rulings_today.sh` + `reconcile_rulings.py` + `ornith_status.py`. Every queue append carries a waiter in the SAME action.
2. **THE GATE IS DONE AND THE GO IS SIGNED (17:49).** Batch gate on #1100/#1101 returned **GO WITH FINDINGS on both**, tier-1 floor, and ruled the db.retry intermittent **does NOT block** either PR (byte-identical file at every graded tree; same red rate at develop as merged under identical load, 3/3 vs 3/3 concurrent, 0/6 vs 0/6 serial). Report: `Testing Agent MAIN/projects/secuura/reports/2026-09-20-batch1100-1101-tier1-r1/`.
3. **WHAT IS OWED NOW: the merge STATUSes.** #1100 (KS-1230) at `99ce89e741e6c3cad7457af7c91fb6fea86acdff` FIRST, then #1101 (KS-1282) at `dc40087e756c598ca8b2957da7fbf1ec01945df8` LAST (auth last). One at a time; develop re-read and the tree re-predicted between them; the ruleset (18499832) re-read first and STOP on a change. **Both heads and develop were re-read by Wednesday at origin at 17:49 with a non-resolving control ref — all three unmoved.** After each merge, verify develop's tree at source. **Nothing merges after 23:00 AEST.**
4. **KS-1282 comment: RULED — post the seat's OWN gate-graded bytes verbatim**, `{SQUASH}` filled with #1101's actual squash SHA and nothing else. Order: merge with the ticket OPEN → comment → read back by id → CAS to Done → archive → read back. Kam's instant for attribution: **2026-09-20 15:30:04 +10:00**, words *"please close and archive."*
5. **Then:** score `%123`, close its pane (detector first), and the floor is clear.
6. **A follow-up TICKET is owed, and it is NOT this batch's:** the gate found six NOT-PINNED role-dimension rows — a widened `SUPER_ROLES` would newly admit a role-ADMIN JWT on all 13 `requireSuperAdmin` routes and on `requireOrgProvisioner`, with only `GET /api/platform/tenants` pinned; one unpinned row, **`POST /api/platform/organizations/register-connector`, returns 201 and MINTS A KEY**. A COVERAGE gap, not a live defect. File it with the gate's evidence, one ticket per logical path, stating KS-1282's own cell is unaffected. VITEST-1 / SHELL-1 / LOAD-1 / LINT-1 are pre-existing and recorded, not fixed.
7. **ORNITH IS PAUSED DELIBERATELY, AND THE PAUSE IS A MECHANISM, NOT A HABIT.** Two fixes banked and held: **KS-1275** (`Refs KS-1275`, never a closing word) and **KS-1203** (`Refs KS-1203`; ⚠ its diff applies `--recount`, NOT strict — the model miscounts its own hunk header, so apply the canonical `patch.diff`, never the quoted text). `night/PAUSE_QUEUE` holds an EPOCH expiry (**20:48 today**) + the reason; `night/QUEUE_EMPTY_WHY.md` holds the full reasoning. The G7 busy leg now reads that file and SKIPS its tap while the pause is live, **logging why** — and still lets the 2 h panel alert reach Kam, because a pause is mine to take and his to see. Arms `local-model/tests/g7_pause_arms.sh` **6/6**, including a negative control on the pre-fix script and the human-date-on-line-1 shape that would otherwise have made the pause permanent. **When it expires, either brief the next ticket or write a new reason — do not re-set the marker without one.**

### 🔴 THE 90% CUT IS REACHED — 21:15, statusline `7d:90%`
**Kam's 2026-09-14 19:14 rule is LIVE: no new agents, no new gates, no drafters. In-flight finishes; from here it is Wednesday + Ornith only.** Nothing was in flight when it tripped. Reported to him on the panel in the same action, as that rule requires.
- **The dashboard gauge read 89% and was 28 minutes stale. The STATUSLINE is the instrument** — read it, do not trust the gauge alone near the cut.
- **Consequence, and it needs no ruling from him:** the KS-1175 fix does NOT start tonight (a seat + a gate, neither available). **Write the brief so Monday morning is execution, not preparation, while he is still here to correct it.**
- **The two banked fixes (KS-1275, KS-1203) are UNRAISABLE until the allowance renews Fri 25 Sep** — raising needs a seat. Not a problem to solve; the shape of the week.
- **Ornith itself is free** (local model) — keep it fed. **Wednesday writes its briefs BY HAND from here; do not spend a brief-writer subagent at the cut.**

### ⚠ OWED, AND IT BIT TONIGHT: a pause's expiry needs a watcher OUTSIDE the paused system
`night/PAUSE_QUEUE` expired 20:05 and was found at 21:15 — **70 minutes**, Ornith idle 253 min. The G7 BUSY leg lives INSIDE `night_run.sh`, so it fires only while the runner runs, and an empty queue is precisely when it does not. **A guard that executes only while its subject is healthy cannot report the subject being unhealthy.** Fix: `doctor.sh` warns on a `PAUSE_QUEUE` whose epoch is in the past (it already does this shape for `rotate_pending_*`). **Arms before arming:** a live pause (silent), an expired pause (warns), no file (silent). Until it ships, checking `PAUSE_QUEUE`'s expiry is a FIRST ACT at every boot and checkpoint.

### 🔴 KAM LIFTED KS-1175's HOLD AND REDIRECTED THE WORK — 19:42:44, view=wednesday
> *"Decision secuura-ks1175-testonly-pin-on-a-held-ticket note: remove the rule and make the fix"*

**He answered OUTSIDE the three options the card offered.** The hold on **KS-1175 comes off**, and the work moves from the test-only pin to **the ticket's real fix** — `anchorSchema.ts` accepting and anchoring the non-PII actor/organisation identifiers instead of stripping them. Full reading: `learnings/2026-09-20_ks1175-hold-lifted-make-the-fix.md`.

- **KS-1250 is UNTOUCHED and still his.** He lifted one named ticket, not the class.
- **The deploy/anchor step is NOT lifted** — he did not name it, and a new field reaches the immutable record only when something is deployed and an anchor is made. Stated back to him on the panel at 19:43; his word widens it, not my reading.
- **The parked brief is SUPERSEDED, not resurrected** (`night/briefs/KS-1175-STRIP-1.md.HELD-…`): it was written to PIN the stripping behaviour he has now asked to CHANGE.
- **This is a Claude seat's job, not the local model's** — multi-file product change; the round-22 writer rejected it as such, correctly.
- **Allowance, put to him at 19:43 and unanswered:** a seat + gate at 87% most likely reaches the 90% cut, and the allowance does not renew until **Fri 25 Sep** while he leaves **Mon night 21 Sep**. **Default stated to him: write the brief now, START IT MONDAY MORNING while he is still here**, rather than spend his away-week's budget tonight. If he says otherwise, run it.

### 🔴 KAM RULED THE BOOT DIGEST — Fleet/BOTH SEATS, and it binds THIS seat
**Card `tuesday-boot-digest-outgrew-the-window`, scope `Fleet/both seats`, RULED `b` at 2026-09-20T16:44:**
> **b — Keep the whole read, shrink the corpus to fit**

**Read the scope field, not the id.** The id begins `tuesday-` and the 16:0x seat waved it past as the other coordinator's; it is the FLEET's, and its sibling `tuesday-mini-vault-three-unpushed-commits` is scoped `WED`. Both were ruled and have since been applied; the cost was an hour, not a lost ruling.

**What `b` commits this seat to:** the boot prompt's WHOLE read STAYS — no bounded reads, no skimming, no per-seat subset. What changes is the INPUT: the digest is 506,473 B from 191 lesson files (53% of a 944,638 B corpus), and it must get smaller by removing material, not by reading less of it.

**The executable route already exists and has never been run:** Phase 1 of `1_Project_Definition/Architecture/2026-09-05_learning-tiers-context-split-plan.md` — transfer the **P-tier project CASES** out to the projects that own them (28 case sections are already reduced to handles in the by-tier digest; the cases themselves still sit in Wednesday's files). Wednesday briefs the transfer; each project's agent files it in its own brain and confirms by mail; the section is then marked `transferred: <project> <date>` and the digest drops it to a handle. **Hard rule 1 applies — Wednesday never edits another project's files.**

**Do NOT satisfy this by trimming the read.** That is option (a), and he ruled (b). A seat that quietly reads less has the same behaviour as a seat that forgot.

### ⚠ HARNESS RULES LEARNED TODAY — they cost four rounds; do not rediscover them
- **`test_only` has its OWN builder: `tasks/test_only/build_test_only_input.sh`.** `night/build_input.sh` CANNOT emit the test_only shape (`grep -ic tampers` = 0) and the checker dies `unknown runner ''`. `task=` on the queue line selects the CHECKER, not the builder.
- **Before queueing any pre-built input, diff its top-level KEY SET against the newest PASSING input of the same task type.** `set(good)-set(mine)` named all twelve missing keys in one command. **A filename prefix is not a shape; a `task=` pin is not a shape; a build's success line is not a shape.**
- **Declared cells in `Reds:`/`## Controls` must be the FULL `it(...)` title byte-for-byte** on a jest/vitest suite — a prefix returns `DECLARED CELL NOT IN THE RUN` (T5). The prefix rule in the builder's header is for BASH suites only.
- **`cockpit.sh say --mail` refuses rc 1 with NO OUTPUT when the pane name is absent from `fleet/inbox_routing.conf`.** `Secuura/Blockchain-BOARD` has been added. **Register any new parallel-seat pane name in the SAME action as its launch.** Tooling fix owed: make it print why.
- **Never read a refusable tool's rc through a pipe** — this shell is zsh; `echo "rc=$?"` after `| tail` is TAIL's status. Two seats lost time to this today.

### CARRY TO THE NEXT SECUURA BOARD SEAT (a recommendation that lives only in a wrap mail reaches nobody)
**The 8th's `done-archive` verb SETS STATE TO DONE BEFORE ARCHIVING** (its line 46) — on a Canceled ticket that silently converts **Canceled → Done**, a state change nobody authorised. The BOARD seat found it by READING the tool it was handed, refused it, and built an **`archive-only`** verb on a byte-identical copy of `linear_ops.py` (guards red-proofed before use: rc 3 on a wrong `--expect`, on a parent with children, and on no `--expect`). **The next seat inherits the COPY, not the 8th's.** Its path + sha256 are in the BOARD seat's history entry.

### DONE THIS SEAT
Board pass complete: **9 archived (7 Done + 2 Canceled), board 459 → 450**, zero comments, zero collateral, both carve-outs untouched — verified independently by me (9/9 `archivedAt` SET, **states unchanged**, archived-slice control returned 250 rows so a zero would have shown). The 2-Canceled archive was **my** ruling, not the seat's. · Rotation liveness guard fixed and committed `b884e7a55` (arms 23/23, two negative controls; doctor now warns on a rotation that never reported). · Board seat relaunched after it died unnoticed. · Digest unmerged-index conflict cleared by regeneration.

### ROUTE TO KAM (Monday 21) — one list
1. **Two cards he ruled at 16:41 are TUESDAY's and are UNAPPLIED** — `tuesday-boot-digest-outgrew-the-window` → b, `tuesday-mini-vault-three-unpushed-commits` → a. They need her seat. I did not apply them (her scope) and did not mail her (his 2026-09-14 07:22 suspension of Wednesday→Tuesday messaging has not been lifted in anything I have read). **Ask him whether that suspension still stands** — Tuesday is demonstrably live again.
2. **`Secuura/platform-s#877` is UNREADABLE — a permissions boundary, measured** (the repo itself 404s; `orgs/Secuura/repos` returns one repository). Reported, not worked around, no broader rights requested. It blocks nothing on its own: KS-1172/KS-1173 also lack kintsugi deploy evidence, so §5f blocks them regardless.
3. **Four escalations, none ruled by me:** KS-577, KS-946, KS-1172, KS-1173 — each turns on absent §5f runtime evidence, and two also on a cross-platform contract or a card he ruled "wait".
4. The `secuura-dependabot-triage` card says "close the 5"; there are now **10** open dependabot PRs (#949 #948 #947 #946 #945 #649 #639 #635 #575 #572). Drifted since 2026-09-01. Zero KS tickets match "dependabot" (control: 29 match "security").
5. **The rotation liveness guard had logged 0 verdicts in 9 armings since 2026-09-18** and also measured pane PRESENCE where the property is ALIVENESS — a dead agent pane passed it today. Fixed, but **the killing mechanism was NOT identified**; the fix removes the property that was measured (descendancy) rather than a proven cause. The first real rotation either logs a verdict or leaves a `rotate_pending_*` marker that doctor surfaces at the next boot. **Check after the next rotation.**
6. Carried from 09-20 morning: Peter's two KS-1195 questions; his KS-593 addition (fuzzed wallet authenticate/verify → 500 where 400 belongs); kintsugi has NO connector allow-list; kintsugi disk 25 G free (budget the ~3.8 G transient per-service build cost); KS-1262 test-token severity unowned; the drive sync keeps making `(conflict_on_…)` copies; seat A's launcher F-02; O-1 (CI jobs never start); the NSG's dynamic IP; report-796 F-01/F-03 is a ruling not a local-model ticket; KS-1269-U/N84-1 `/unrevoke index < 0`; ruleset 18499832's unattributed-changes flag; the audit-baseline.json fuse expires 2026-09-24; **O-1: `admin.ts` `requireAdmin` routes do no session check** — a REVOKED admin session JWT gets 200 in-process; KS-1282 completeness is his call; the allowance pace for his week away.
7. **Wednesday's reading to confirm:** auth surfaces opened to TEST-ONLY local-model work (zero product bytes) under "auth product EDITS stay out". Default: continues unless he says auth means tests too.

### OWED (tooling, mine, none urgent)
`cockpit.sh say` must print WHY it refuses (SECOND cause filed today for the same silent rc 1) · `brief_and_launch.sh` prints "launched" after cockpit SKIPS a same-name pane · `inbox_digest.sh` shows Datasec previews in the wednesday-agent@ section · `note_entry.sh` warn on a typed clock later than its stamp · a `night_run.sh` refusal when a pre-built `input=`'s `task_type` disagrees with its `task=` · the resident family-weight index (owed from the 2026-09-10 measurement) · ledger rule 3c: rows dated 09-17 pass the 3-day line on 09-21.
