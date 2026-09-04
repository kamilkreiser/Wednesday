---
date: 2026-09-04
type: pickup
source: Kam's request at 15:16 — "create a note to action things when we pick up"
status: live
supersede: replace this file wholesale at the next pickup; do not append
---

# NEXT PICKUP — written 2026-09-04 15:1x, fleet deliberately shut

**Kam closed the fleet at ~14:38 on weekly usage (~96%). Both agents wrapped clean and their
panes are closed. Nothing is broken. Nothing is half-done. Everything below is either waiting
on a human or waiting on the queue reopening.**

🔴 **THE 2026-08-28 "agents run until the queue is finished" GRANT IS SUSPENDED.** It is
suspended by Kam's word and only his word lifts it. Both agents recorded the suspension in
their own `history.md`. **A seat that boots, reads the grant, and relaunches the fleet has
misread this file.**

---

## 1. THE ONLY THING NEEDING KAM'S HANDS — ROTATE ONE TOKEN

🔴 **Wednesday leaked a live GitHub token into its own terminal output at 15:1x.** Not into
any file, commit, or mail — measured: zero occurrences across the whole brain and project
tree, zero in `git log -S`, and the transcript lives in `/Users/kam_code/.claude/projects/`
which is **outside `/Volumes/DevMASTER`**, so the drive sync could not carry it.

**Rotate it anyway. A credential rendered once is one whose secrecy cannot be asserted.**

✅ **CLOSED 15:4x — ROTATION COMPLETE AND VERIFIED BOTH WAYS.** New token ALIVE on `kksecura`
(expires 2026-12-03) and reaching `Distributed_Secuura` with push; **OLD token returns 401 — genuinely
REVOKED, not merely replaced, which is the check that actually closes it.** Kam's terminal edit did NOT
reach the file (verified: `.env` still held the dead token and 401'd), so **on Kam's explicit "yes, go
ahead" Wednesday made the write itself** — the one time this session Wednesday wrote into another
client's folder, on his named word. Backup at `4_Credentials/.env.pre-rotation-2026-09-04.bak` (0600).
**Proven: exactly 1 line changed, 12 variables before and after, names identical, every other value
byte-identical, perms preserved 0600, and the token IN THE FILE authenticates.**

⚠️ **STILL OPEN, low urgency:** `4_Credentials/Secuura-git.rtf` is a **second live copy of the token**,
**world-readable (0644)** where `.env` is 0600, and it sits in a folder that syncs to the travel drive.
**Wednesday did NOT move or delete it — Kam's consent covered the `.env` write only.** Offer at pickup:
move it to a dated quarantine folder (never delete). Also: the new token is still named `claude-ci-read`
while holding **admin + push** — scope or rename it when convenient.

~~STATUS AT 15:3x — KAM HAS REGENERATED IT. The remaining steps are: he pastes the new value into the
path below (line 24, `GH_TOKEN=`, no quotes), then Wednesday verifies TWO separate facts — that the NEW
token authenticates and can reach the repo, AND that the OLD one is genuinely DEAD rather than merely
replaced in the file. Only the second closes the incident. If this pickup note is being read and that
second check has not been recorded, DO IT FIRST.**

🔴 **AND THE SEVERITY IS HIGHER THAN THE NAME SUGGESTS: the token is called `claude-ci-read` and it holds
`admin: true, push: true, pull: true` on `Distributed_Secuura`. It is not a read token — it can push code
and administer the repository.** Wednesday initially under-described the exposure by reasoning from the
name. **When it is reissued, scope it to what it is named for or rename it to what it holds — a
credential's NAME is not its GRANT, and the wrong name invites exactly that mis-reasoning.**

| | |
|---|---|
| **Which** | Fine-grained PAT on GitHub account **`kksecura`**, value ends `…7zOd` |
| **Stored** | `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env` → `GH_TOKEN` |
| **Rotate at** | github.com/settings/tokens?type=beta → Fine-grained tokens |
| **After** | Update that one `.env`. Nothing else reads it. |

**Cause and the rule, so it cannot recur:** the presence check was written
`echo "token set: ${T:+yes}${T:-no}"`. `${T:+yes}` is safe; **`${T:-no}` returns THE VALUE
when the variable is set**, and the two forms look symmetrical. **Never interpolate a secret
into an echo in any form — use `[ -n "$T" ] && echo set || echo unset`, which cannot emit the
value because the value never enters the format string.** Ledgered severity-high.

---

## 2. KAM'S THREE RULINGS — recorded, unstarted, front of the queue

**All three cards ruled 15:08–15:10. His desk is EMPTY.**

**(a) `secuura-ks788-gate-fails-open` → `merge-when-peter-approves`.**
PR **#807** (`98e9a09025a0…`) is **open, mergeable, clean, ZERO reviews** — read from the API
at 05:09Z. **Peter has not looked at it.** It merges on his approval alone; Kam does not need
to sign again. **Kam's sequencing instruction: "merge first"** — #807 merges before the
KS-781 work, which is already the natural order because **#807 unblocks the four held
branches** (a branch without the KS-788 timeout cannot complete a push).
**Action next session: check #807's review state first. If merged, the branches push.**

**(b) `secuura-ks781-mfa-bypass-fix-order` → `authorize-fix-now`.**
Fix the confirmed runtime MFA bypass on `POST /api/oauth/authorize`, **with KS-790 explicitly
blocked behind it.** This is the authorisation Wednesday would not give without his signature.
**It is authorised and unstarted.**

**(c) `nexusai-rd296-sizing` → `build-it`.**
Commission the 1–2 day wiring of Sustainability to the same log sources as every other tab,
knowing it lights **no new tile** and `SECURE_RELEASE_AVOIDED` stays dark structurally.
**The RD-296 BUILD hold is now LIFTED by this ruling.**

---

## 3. 🔴 STILL KAM'S, STILL LIVE, AND IT OUTRANKS EVERYTHING ABOVE

**Peter and Stuart must be told NOT to fix KS-790 until the authorize path is gated.**
External comms are his alone; Wednesday cannot send it.

**Why it survives his ruling:** KS-781 is now *planned* rather than *done*. Until the fix
actually lands, **KS-790 being broken is the only thing stopping a leaked authorization code
becoming a session.** KS-790 reads like a routine broken-OAuth ticket. It is not.

**Measured 05:09Z: KS-790 still Backlog, High, UNASSIGNED, untouched since 02:32:43Z.**
Nobody has picked it up, so there is still time — but re-measure before assuming that holds.

---

## 4. SECUURA / BLOCKCHAIN — s124 wrapped 0.95, queue for s125

**FOUR BRANCHES COMMITTED LOCALLY AND UNPUSHED. None is unfinished.**

| branch | SHA | unblocks when |
|---|---|---|
| `feature/ks-663-…` | `df169eaf5` | Wednesday's hold lifts |
| `feature/ks-693-…` | `88684fb25` | Wednesday's hold lifts |
| `feature/ks-792-…` | `b6e8a5650` | **#807 merges** |
| `docs/pr-status-for-peter-…` | `80677e8c6` | **#807 merges** |

All four verified local-only with zero at origin. **Whoever picks this up must not read
"unpushed" as "unfinished".** The `--no-verify` exception is **spent** and was scoped to
#800/#806 — it does not extend.

**Owed:** the **leg-5 advisory re-run on #800 `c06860658`** — still gated on npm's bulk
advisory endpoint, last probed 03:35Z (0 bytes at 30s against `GET /lodash` 200 in 0.083s).
When it answers: re-run the preflight, post the result, mark the `--no-verify` disclosure
resolved.

**Written, NOT sent:** the Peter PR-status document at `80677e8c6`,
`Blockchain/Dev/docs/PR-STATUS-FOR-PETER-2026-09-04.md`, 3,436 B. **The send is Kam's.**
Its headline fact: **#785 is the only PR ever approved, and its approvals sit on `50a741aaf`
and `878081e98` while head is `a27b3f9b3` — the approval did not survive a push.** So it is
not "nobody approved anything"; it is "the one approval that exists no longer applies."

**Held:** KS-597/598 on Kam's plan-sheet approval (Wednesday holds that request, deliberately
queued behind the security item). **Unstarted:** KS-791, sized and ready.

---

## 5. DATASEC / NEXUSAI — S32 wrapped 0.85, the open round

🔴 **RD-245 IS REOPENED (In Progress). Its fix was FALSIFIED by the QA gate, not shipped.**

**F-1 (Blocker) + F-3 (Major) are the round, unstarted**, written up as section 1 of that
project's `HANDOVER-CURRENT.md`. The governing framing, which must survive into the fix:

> **The regression test must drive `setSetting()` — the product's own entry point. If the new
> test cannot be made to go RED on current code BY THE PRODUCT'S PATH, it is not a test of
> this defect.**

**Highest-value first step: the incident-artifact question.** The tester never read
`$HOME/data` or the 2026-09-03 files, so F-1's reconstruction of *that* incident is unproven
— **while F-1's exposure stands independently on the measured replay.** Keep those two apart.

**Wednesday's ruling attached:** if the fix changes **how many generations are kept, or the
write cost of keeping them**, that tradeoff comes back to Wednesday as a QUESTION before it
is built. Retention depth is product behaviour a user notices.

**The re-gate is BATCHED, deliberately:** `1c5d3f7`'s F-2 fix has NOT been through QA. One
pass covers F-2 plus the F-1/F-3 work after the round. **A decision, not an omission.**

**Also filed and needing a ruling: RD-303** — `4_Credentials/.azure/` is *tracked* in that
repo (6 files). **Nothing is exposed** — Wednesday verified all six independently, 0
suspicious matches against a firing control. The agent closed the path with ignore lines at
wrap. **The open question is whether to untrack the six, which touches committed history.**
Fleet sweep result: **one real instance.** Vision's tracked `.azure/config` is *not* the same
thing (141 B of deployment defaults, no credentials); Secuura, CypherKey, HPSM, Tokenomics and
Wednesday's own are clean.

---

## 6. HELD BACK DELIBERATELY — RD-75, and its trigger has now fired

**RD-75 (High, needs-decision): "No working mechanism for Kam-traceable authorisation of
approval-class deploys — the CC path named in briefs has never existed."**

The 11:45 handover set the trigger as *raise it once the deploy verifies*. **RD-299 verified,
so it is owed.** It was kept off Kam's desk only so it would not bury the security warning.

🔴 **It matters more than its age suggests: it is a ticket about the authorisation chain
Wednesday exercised all day** — two deploy GOs, a gate bypass on #800/#806, and a string of
rulings, all under the v1.3 signed delegation. **Card it once Kam has answered §3.**

---

## 7. THE PORTABLE-DRIVE SYNC

**DevMASTER ⇄ KK_DEV_Local only — the NAS leg was deliberately NOT run** (it is the leg that
deleted six folders on 2026-08-26; Kam asked for the portable drive).

**Preflight passed both checks that were skipped on 08-25:** case-consistency probe found
**zero** case mismatches (the only top-level difference is `Archive`/`BACKUP`, which the
profile ignores), and the `.devnas-sync-state` marker is present so the **first-sync FORCE
path — which deletes anything on the target not on the source — was not taken.**

**Check on pickup: did it finish, and did it delete anything?**
- Log: `2_Project_Files/fleet/state/sync_kkdevlocal_pty.log` (path also in `state/sync_current.txt`)
- `grep -c 'Deleting'` — it was **zero** throughout. **Verify it stayed zero.**
- **Verify content at the destination, not the exit code:**
  `/Volumes/KK_DEV_Local/WEDNESDAY/0_Brain/daily/2026-09-04.md` was **ABSENT before the run**.
  If it is present and matches DevMASTER's size, the chain delivered.

**Two things worth Kam's word, neither actioned:**
1. **13 GB across 53 `qa-worktrees/*/node_modules`** in NexusAI is most of the sync's time.
   It is **under 1% of the drive's 1.5 TiB free**, so it is a time cost, not a space problem.
   One ignore line would make the sync minutes instead of hours — **but `~/.unison/devnas.prf`
   is user-global config and is Kam's to edit, not Wednesday's.**
2. The profile carries **`confirmbigdel = false`** — it cannot refuse a deletion, which is the
   2026-08-26 shape unchanged. Mitigated by `backup = Name *` / `backuploc = central`, so
   deletions land recoverably in `~/.unison/backup/`. **Recommendation stands from 08-26:
   turn `confirmbigdel` back on.**

---

## 8. THE T9 WAS NOT PLUGGED IN

Only `KK_DEV_Local` was mounted. **If Kam wants the T9 synced, it needs connecting** and the
same leg run against `/Volumes/KK_T9_External_HDD`. Same preflight applies — run the case
probe first.

---

## 9. STANDING OPERATIONAL NOTES, all learned the hard way on 2026-09-04

- **`cockpit.sh say` takes the REGISTERED PANE NAME** from `inbox_routing.conf`, never a
  `%id` — and **its refusal prints NOTHING**. Read the output for `delivered to`, never the rc.
- **A non-zero `ctx` on a freshly launched pane proves A turn ran, not the COMMISSIONED turn.**
  Verify a launch from the pane's **content** naming the commission. `ctx:-` still means no
  turn at all.
- **macOS bash 3.2 mishandles a heredoc inside `$( )`** — build long prompts in their own file.
- **`timeout N find … | wc -l` prints 0 when the find is KILLED**, and a `||` guard cannot fire
  because `wc` exits 0. A zero that means "did not finish" is indistinguishable from "none".
- **The sync engine's log prints `Sync finished` on both success and failure** — only the exit
  code discriminates. The first attempt failed with rc=1 and said `Sync finished`.
- **In another project's repo: `ls-remote` for heads, `git show <sha>:<path>` for local
  objects, the API for the rest. Never a fetch.**
- **`gh` is NOT authenticated in the Secuura project's `GH_CONFIG_DIR`** — use the project's
  own `GH_TOKEN` against the API, and verify identity at point of use.
- 🔴 **Wednesday's own pre-commit secret scan REPORTS BUT DOES NOT REFUSE** — it was written
  `grep -c … || echo clean`, which prints a hit and lets the commit through. **And its
  predicate (`github_pat_`) matches Wednesday's own incident write-up**, so it alarms on the
  commits that discuss security. **Two fixes, both sized and unbuilt: gate on the result
  (`if grep -q …; then exit 1; fi`), and scan for the secret BODY not the vendor prefix. The
  durable home is the repo's existing pre-commit hook, which already blocks artefact classes.**
- **The QA project still has no launcher entry, no inbox and no wrap hook.** Its one-off
  wrapper at `fleet/state/launch_qa_nexusai_rd245.sh` **does not travel** — `state/` is
  gitignored by design. **The durable fix — a real launcher in `launchers.conf` with the
  prompt-in-a-file pattern and its two guards, plus an `inbox_routing.conf` entry — is sized,
  named, and unbuilt.**
