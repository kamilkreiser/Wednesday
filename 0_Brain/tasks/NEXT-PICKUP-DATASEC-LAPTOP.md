---
date: 2026-09-08
type: pickup
scope: DATASEC ONLY — laptop seat. Secuura belongs to the Studio seat; do not touch it, do not adopt its cards.
source: replaced WHOLESALE at 12:3x by s152, at Kam's wrap-everything boundary
status: live
supersede: replace this file wholesale at the next pickup; do not append
---

# NEXT PICKUP — Datasec laptop seat, 12:3x Tuesday 2026-09-08. EVERYTHING IS WRAPPED. KAM IS MOVING THIS AGENT TO A NEW MACHINE.

**Run `/Volumes/KK_T9_External_HDD/WEDNESDAY/2_Project_Files/tools/kam_rulings_today.sh` before writing
anything — read EVERY line.** Mail UTC ≈ AEST−10. **ROTATION BAND 80–90%; 70% is a checkpoint only.**

## 🔴 READ THIS BEFORE YOU TRUST YOUR OWN BOOT — s152 DID NOT LOAD THE BRAIN AND DID NOT NOTICE
s152 issued the mandatory `_boot_digest_by_tier.md` read as two `sed` calls through **Bash**. The file
is ~292 KB; **both chunks exceeded the tool's inline limit and were PERSISTED TO FILES**
(`Output too large (60.7 KB). Full output saved to: …`) — and s152 read that receipt as a completed
read and carried on. It ran the entire session on this pickup, Kam's rulings and the two CLAUDE.md
files. Good sources. **Not the lessons.**
**MEASURED, not assumed:** a `Read` of the same file at `offset 3600, limit 60` returned real content
into context. The file is fine; the PATH was the fault.
🔴 **SO: read the digest with the `Read` tool in offset/limit chunks (3,952 lines, ~4 calls) and
ASSERT THE LAST LINE LANDED.** A "saved to file" notice is a **failed** read, not a completed one.
Ledger w=104. Everything else this session was checked and worked; the one step with no check on it
is the one that silently did not happen.

## 🟢 STATE — NOTHING IS IN FLIGHT. NO AGENT PANES ARE OPEN.
    NexusAI  main = cd2b543   (a9a8cb6 frozen 09-01 -> 8 authorised merges -> RD-369 fix -> round 2 -> S47 history)
    S47      WRAPPED and CLOSED, listeners 13 -> 13. Ritual run, pushed, 12/12 artefacts verified in
             the REMOTE by content. Started nothing.
    Panes    %0 wednesday only. %22 closed 12:2x. %26 (SecurityReview) closed earlier by s150.
**`main = cd2b543` was verified by this seat against `ls-remote`, not taken from S47's mail.**

    RD-369  Release Ready   RD-386 To Do (round-2 residue)   RD-385 To Do   RD-372 To Do (NOT started)
    RD-382/383/384 To Do    Release Ready 50 · Done 86 · open 294   (S47's read, not re-derived here)

## 🔴 KAM'S DESK — FIVE CARDS, EVERY ONE WITH A SAFE DEFAULT
1. **`nexusai-rd369-round3-or-ship-at-the-cap`** (rec `round3`) — exposure CLOSED and proven in a real
   built image; this is only the GUARD, and it survives on a **one-line margin** (a cosmetic reflow
   flips 3 of 4 real RD-385 files carrier→clean; the certifying cell asserts only `>0`). **Third
   option NOT scoped: also REMOVE the RD-385 files from the image** — the only one that stops the
   identifiers shipping rather than just detecting them. If he rules that, **come back with a plan first.**
2. **`secrev-live-pass-blocked-on-tenant`** (rec `name-tenant`) — a published Critical cannot be
   rescored while the workspace CLAUDE.md's Datasec tenant mapping (`fc05dcdd` vs `0c57ab37`) says
   *do not assert which*. **Three agents were held off `az` on that line and that should continue.**
3. **`secrev-verify-23-and-batch1-filing`** — ruled `package`; follow-through open.
4. **`hpsm-credential-bearing-prd-outside-every-snapshot`** — note only: *"only secuura projects on
   this machine until further notice"*. HPSM stays untouched.
5. **NEW (s152) — the dead schedulers, below.** Recommendation: re-run the installer, but AFTER the
   machine move, not before.
🔴 **The three GitHub settings** (`CI_DEPLOY_ENABLED=true`, the three `AZURE_*` secrets, the `demo`
environment) are still the only unclosed part of his 07:10. **Sent twice. DO NOT SEND A THIRD TIME.**
`deploy-demo.yml:51` gates every job on that variable, so **a merge CANNOT deploy — never report one as one.**

## 🔴 NEW: THREE OF WEDNESDAY'S OWN RITUALS ARE DEAD, AND DOCTOR SAID THEY WERE FINE
`com.wednesday.shiftchange` (05:30) · `.wake` (06:00) · `.close` (23:00) — **every fire since
2026-09-07 has failed with exit 127.** The plists were generated 2026-09-02 and hardcode
`/Volumes/KK_DEV_Local/WEDNESDAY/…`, a volume that does not exist here. `.err` logs date it exactly:
last success `wake` 09-07 06:00, then 09-07 23:00, 09-08 05:30 and 09-08 06:00 all
`No such file or directory`.
**`doctor.sh` printed `✓ scheduler … loaded (last exit 127)` for all three** — its own comment said
*"launchd jobs must execute from this drive"* and it never checked that. **FIXED by s152 and both
branches exercised:** doctor now stats the plist's script path, names the stale path and the remedy;
red-proofed live, positive control confirms present-path+exit-0 still goes green.
🔴 **THE JOBS ARE NOT RE-ARMED, DELIBERATELY.** `install_scheduler.command` self-locates and fixes all
three in one command — but re-arming three **session-spawning** jobs unsupervised on the eve of a
machine migration is Kam's call. **On the new machine, run the installer FROM THAT DRIVE as a
bring-up step.** The plists live in `~/Library/LaunchAgents/` and do not travel.

## 🔴 WHAT DOES NOT TRAVEL TO THE NEW MACHINE — this is the list Kam actually asked for
1. **`.git/hooks/pre-commit`** — untracked by design. It is the guard that refuses conflict markers,
   i.e. **the exact thing that corrupted `chat_log.json` and `decisions.json` five times today.**
   A restore carries it; a fresh clone does not. **Test it before that machine does any work.**
2. **Per-clone git config:** `core.hooksPath`, `core.fileMode`, `core.sshCommand`. NexusAI's hook FILE
   is tracked and the config that activates it is not — a fresh clone has the hook and does not run it.
3. **`~/Library/LaunchAgents/com.wednesday.*`** — machine-local, and currently pointing at a dead volume.
4. **`4_Credentials/` and `3_Access_Keys/`** — gitignored by design, restore out of band.
5. **NexusAI: 12 root `HANDOVER-*.md`** sit outside the repo by design and do not travel.
6. **Matilda Premium voice** — doctor warns; fallback chain active.
7. 🔴 **NexusAI `HISTORY.md` at `main` runs S32…S39 then jumps to S47 — S40–S46 is a SEVEN-SESSION
   HOLE.** Four branches (`s40-`, `s41-`, `s43-`, `s46-history-docs`) are in the remote and **none is
   an ancestor of main** (re-derived by this seat with `merge-base --is-ancestor`, not relayed).
   Not lost — and not in a fresh clone either. **S47 flagged this as the item it would most want ruled
   before the move, and did not merge them because it was told to start nothing. That was right.**

## THE SECURITY REVIEW — ANSWERED FOR KAM, AND THE WEAKNESS IS NAMED
**No reviewed code was changed.** Nothing under `Security Review/Source_Code` touched today; newest
file anywhere in it **2026-09-04 20:13**. The discriminator that makes that worth something: the three
trees added since 01 Sep each carry **exactly ONE distinct timestamp across 299 / 412 / 312 files** —
a snapshot drop, not editing.
🔴 **The weakness, and it should be closed rather than re-argued: none of the 34 trees is a git repo,
so mtime is the ONLY evidence and there are no hashes to compare.** Recommended to Kam: hash the trees
and keep the manifest, plus a read-only bit. **NOT DONE — another project's folder is his boundary.**
**NexusAI is explicitly OUT of the review's scope** by its own brief and is not in `Source_Code` at all,
which is why 21 commits today are not a review breach. **HPSM (31 dirty) and myPKI (32 dirty) both
PRE-DATE today** — August conflict copies and 16 July respectively.

## ⚠️ TRAPS — live, and most of these fired on this seat or its predecessor
1. **Read the inbox at limit >= 3, never 1.** A real inbound sits beneath your own outbound echo.
2. 🔴 **BOTH Wednesdays send as `wednesday-agent@agentmail.to`.** Tag by the subject's **CONTENT**, not
   its arrow — `Secuura`/`KS-`/`PS-` = the Studio's, `Datasec`/`RD-`/`VSP-` = this seat's. A gate
   verdict arrives as `[QA -> Wednesday] …` and carries no client in the prefix at all.
3. 🔴 **`git -C $VARIABLE <writeverb>` is REFUSED — write paths LITERALLY.** Hit a third and fourth time.
4. 🔴 **`cd` is refused by a hook.** Absolute paths everywhere; tools self-locate.
5. **`send_brief.sh` prepends its own routing prefix** — `--subject-file`'s first line takes the BARE
   topic. s152 doubled it (harmless, cosmetic). Its self-check regex is exact; GENERATE the stamp.
6. **Ghosts:** run `pane_prompt_check.sh` FIRST, always. **A brief states the decisions the agent is
   NOT making.** A dry queue is a reason to HOLD, not to END.
7. **`pane_close.sh` needs the `%ID`, not the name** — it refuses a name that does not resolve to a
   tty, correctly, because every check after it would be vacuous. Its `listeners N->N` line is the control.
8. **Another project's checkout is READ-ONLY for git.** Read verbs only.
9. **Verify a send by a non-null `preview`; a mail can arrive zero-byte.** Single-message GET needs the
   `message_id` **URL-encoded**.
10. **`launchers.conf` points at DevMASTER, unmounted here** — launch by hand, then
    `tmux set-option -p -t <pane> @cockpit_name '<name>'`. **Do not rewrite `launchers.conf`.**
11. **`/Volumes/DevMASTER` is NOT decommissioned** — unmounted here. **Prune no worktrees.**
12. **Use `safe_push.sh` — it stages ONLY paths passed as arguments.** `HEAD == origin` proves the refs
    agree, not that the work is in them.
13. 🔴 **After ANY commit touching `chat_log.json` or `decisions.json`, PARSE IT OUT OF HEAD:**
    `git show HEAD:<path> | python3 -c 'import json,sys; json.load(sys.stdin)'`. Those two files
    conflicted **five times** in one session. **Never install a union smaller than its largest source.**
14. 🔴 **THE VAULT: do not run the wrap's vault step from a Datasec seat.** `end-of-session.md:50` is
    `git add -A` and the vault's untracked set includes **Secuura** paths — hard rule 2. Skip it, say
    so in the wrap, stage nothing by path. Carded; shared file, so it is Kam's.

## STANDING
**Kam's week grants (through Sunday 2026-09-13):** merge on Wednesday's word once the gate passes ·
deploy · production changes — **production is SECUURA ONLY, confirmed by Kam 12:10 and asserted by
doctor. DATASEC PRODUCTION IS UNGRANTED: ask, do not argue it into scope.**
Ticket creation AGGREGATES. **FOUND / TESTED / HOW**, controls named under HOW.
**NAME THE FRAME — the number is read in the same action as the sentence carrying it.**
Taps <= 200 chars, pointer only; **mail FIRST, verified by a non-null `preview`, THEN tap.**
**Never delete — quarantine. Names, not pronouns. Kill anything querying Azure credits.**
**CLAIM BEFORE STARTING ANY WED WORK** (`wed_claim.sh`).

## FLEET — AND KAM'S NEW ARCHITECTURE, WHICH IS THE NEXT REAL WORK
**The Studio seat rotated at 12:2x too** (`9e033aa4`, *"Rotation handover on Kam's word — the
commission is the successor's first job"*). Both coordinators turned over inside twenty minutes.
🔴 **Kam ruled at 11:56 that the Datasec agent is named TUESDAY**, and at 11:59 asked for the folder to
be copied and labelled, with separate Claude instances per agent and a travel-mode answer. **That
commission is the STUDIO seat's** — it holds the two architecture documents
(`1_Project_Definition/Architecture/2026-09-08_two-machine-fleet-and-one-shared-panel.md` and
`…_two-agent-fleet-implementation-plan.md`). **Do not duplicate it from here.** What this seat owes it
is the migration list above, which is now written down rather than in one seat's head.

## WHAT THIS SEAT WOULD SAY IF IT COULD SAY ONE THING
**Its work held and its boot did not, and only one of those had a check on it.** The security-review
answer was measured three ways and volunteered its own weakness; the scheduler fault was found,
diagnosed, fixed and red-proofed; S47's figures were re-derived rather than relayed. And underneath
all of it, the mandatory brain load had silently not happened, because a tool said where it had put
the payload instead of handing it over — and nothing was watching that step. **Put a check on the
step you do first.**
