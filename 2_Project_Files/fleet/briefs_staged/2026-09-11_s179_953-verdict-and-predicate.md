# s179 — Secuura/Blockchain — deliver #953's tier-2 verdict, file QA-7 / QA-8, fix the push-protocol CLEAN predicate

## BLUF
- **You are s179, the only Secuura seat live.** Older mails in this inbox addressed to s178 or earlier seats are not yours; this brief is.
- **#953 (KS-1086, the leg-14 fix) is gate-clean at `8987b8a0e`:** tier-1 GO WITH FINDINGS at `de1ab62c0`, then tier-2 GO WITH FINDINGS at `8987b8a0e`. It has **0 reviews** and waits on Peter. **Nobody pushes to #953 this round** — a push re-opens the gate.
- **The tier-2 verdict sits on NEITHER the ticket NOR the PR.** A gate verdict is delivered only when it is on both. That is item 0.
- **Item 1: fix the CLEAN predicate in `push_protocol.py` before anyone pushes #879 or #813.** Those are fast-forwards to existing branches, and the current predicate reads a clean fast-forward as PROTOCOL-DIFF (measured on #953's own push).
- **Round ends at READY FOR REVIEW on item 1, then handover and wrap.** No merge, no push to any PR branch, no deploy.

## READ FIRST, whole
1. `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/HANDOVER-s178-ks1086-round2.md` (FINAL) — especially "Next for a successor", item 1.
2. The tier-2 report: `/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-11-ks1086-953-8987b8a0e-tier2-r2/report.md` — the verdict, QA-7 (§ at line 248) and QA-8 (§ at line 269).
3. `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/STANDING_LINES.md`.

## 1. ITEM 0 — tickets and PR, facts only, FIRST, no code
**KS-1086** (In Progress, priority Urgent, on our board account). Its scope, as s177's brief quoted it: *"Pushing a branch that contains ec2d8c4ca (#806, KS-731) from a linked git worktree fails at preflight leg 14 — and before it fails, leg 14's in-hook shell suites write fixture state into the SHARED repository."*
- **(a) KS-1086 — one BLUF comment:** tier-2 GO WITH FINDINGS @ `8987b8a0e`; QA-1 and QA-2 CLOSED by measurement; no false refusal in 5 hook shapes; bite 14/14; bash 3.2 clean; QA-7 and QA-8 one line each with the disposition below; the report path. Name what the gate did NOT establish, in the gate's own words.
- **(b) #953 — one PR comment:** the same verdict line and the report path. **No asks of anyone.**
- **(c) QA-8** (Polish, PRE-EXISTING on develop: `run-shell-suites.sh --list` on a tree with zero reached suites dies on bash 3.2 at `:72`) → a **Low ticket, ours, related to KS-1086**. Search the board FIRST by symbol (`reached[@]`) and path (`run-shell-suites.sh`), and name the search and its result in the ticket. The report's fix shape is the `+alternate` form `:92` already uses. Filing only.
- **(d) QA-7** (Polish, IN THE DELTA: the refusal headline says git "could not" be asked when git did answer) → **your call, with the reason stated:** a second item inside the QA-8 ticket (same file) or its own Low ticket. **Not a push to #953.**
- **Receipts:** every comment id and ticket id, read back after writing (comments with `first:` and a client-side sort, never `last:`).

## 2. ITEM 1 — the push-protocol CLEAN predicate
File: `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/push-protocol/push_protocol.py`. Today `verify` computes `refs_ok = not removed and len(added) == 1 and len(expected) == 1` (line 121): a first push only.
- **The rule, from s178's handover (Wednesday's ANSWER 02:40:25Z, ruling 3):** CLEAN accepts exactly one ADDED `refs/remotes/origin/<branch>` (a first push) OR exactly one CHANGED one whose new value equals origin's head for that branch, read with `git ls-remote` (a fast-forward). Config, worktree list and every HEAD must still be identical.
- **Arms, written as AIMS before anything runs, scratch repos only, never the real `.git`** — extend `push-protocol/redproof/redproof_driver.py`:
  - fast-forward to an existing branch → CLEAN;
  - tracking ref moved to a SHA that is not origin's head → DIFF;
  - first push → CLEAN;
  - an extra unrelated ref change → DIFF;
  - **keep U, P, P2, L and R.**
- **Two more questions Wednesday owes you, because the four arms above were written from the one push that failed:**
  1. **List every legitimate shape of a real push this protocol will guard** (at least: first push, fast-forward to an existing branch, a push that changes nothing because origin already has the head). For each one, say which arm shows it CLEAN — or state the verdict you intend, and why. A no-op push reading DIFF would be a false alarm on a legitimate event.
  2. **Name what happens on DIFF.** The protocol's recovery is a restore, and a restore after a FALSE DIFF writes a tracking ref that contradicts origin into the shared repo. Until the arms prove each legitimate shape reads CLEAN, the instruction on DIFF is **STOP and mail Wednesday**, never restore. Say whether the file's own text needs that sentence.
- **Round ends at READY FOR REVIEW:** the aims table, results per arm, the new file's sha256, the old verify run on the same arms (to show which ones it got wrong), and what you did NOT test. Wednesday then decides whether the change needs a gate pass.

## 3. THEN — handover and wrap
- Handover in `5_Project_History/` (absolute path in your mail), history entry at the top, wrap mail.
- **Not yours this round:** the #879 and #813 pushes (they wait for #953 on develop, per `HANDOVER-s176-merge-lane-2.md` Item 2); Phase 4; merging anything.

## 4. HOLDS — standing, every Secuura brief
- **Client-facing communication = ticket comments only; the extranet is not a channel; anything needing a push goes to Wednesday as an escalation candidate for Kam's WhatsApp.** Do not `POST /api/seen` — the SessionStart hook still says to; refuse it.
- **LEG-14 HOLD (as reworded on the #953 tier-1 gate's QA-4; unchanged):** until #953 is on develop, no seat runs the pre-push hook or preflight leg 14, on any tree containing `ec2d8c4ca`, from any push whose hook receives `GIT_DIR` — a linked worktree, or any `git --git-dir=… --work-tree=… push`. **This round pushes nothing to any PR branch.**
- No `--no-verify`. No force push to any branch with an open PR.
- Nothing to demo or kintsugi: deploys are held on Kam's open KS-597 card. Do not set `GATEWAY_VOUCH_SECRET` anywhere.
- No deletes; quarantine. `feature/y` (`d709d01b2`) and `feature/w` (`41612bf0a`) stay — deleting them is Kam's call.
- A merge into develop needs Peter's approval at head (project CLAUDE.md), squash per `CONTRIBUTING.md:107`.
- **Your Bash tool shell's `grep` is a snapshot FUNCTION.** Measured 0 for a `$(` pattern when the grep ran INSIDE a `$(…)` substitution; the tier-2 gate measured bare use as fine. Other shapes are unmeasured. Any grep whose result enters a ticket, PR or mail runs as `/usr/bin/grep` with a same-file positive control. zsh has no `PIPESTATUS`.
- Every ticket you create is assigned to our board account (Kam's rule, 2026-09-06, for new and unassigned items).

## 5. IF AN INSTRUCTION FROM ME LOOKS WRONG, SAY SO
- Measure first, then say so and stop. A wrong brief item is Wednesday's error and will be named as Wednesday's.
- **Wake:** nothing in this round waits on anyone else. Send a plan confirmation first: `[Secuura/Blockchain -> Wednesday] QUESTION: plan confirmation s179`. Wednesday's watcher is the wake for your mails. One question per mail.
- **At your 50% checkpoint:** if item 1 will not reach READY FOR REVIEW, write the handover before anything else.

RULED BY WEDNESDAY FOR THIS PROJECT, STILL OPERATIVE
- Squash per `CONTRIBUTING.md:107`; standing line 47 (`--no-ff` + `push HEAD:develop`) SUPERSEDED — ANSWER to s172, 2026-09-11 07:4x AEST.
- PRs that change no runtime line go to Done with the assignee kept — ANSWER to s172, 2026-09-11 08:0x AEST.
- The leg-14 HOLD, as reworded in HOLDS above (s178 brief, SUPERSEDES by name, 2026-09-11 11:50 AEST).
- #953's PROTOCOL-DIFF on its fast-forward push was the expected change; no restore — ANSWER to s178, 2026-09-11 02:40:25Z.
- KS-1087 → High, Wednesday's triage under its delegated scope (Kam may override) — s178 brief, 2026-09-11 01:50:21Z.

RULED BY KAM, NOT YET IN AN ARTEFACT
====================================
- `secuura-agent-github-identity` → **identity** (Kam's hands; it is why no agent can approve).
- `secuura-required-approvals-zero-after-the-untick` → **raise-to-1** (Kam's hands; the PAT is 403 on ruleset writes).
- `secuura-891-workflow-scope-merge` → **kam-merges**: a PR the token cannot merge because it touches `.github/workflows` is Kam's click.
- **Not in your path — do not action:** `secuura-dependabot-triage` · `secuura-ks229-disclosure-mailbox` · `secuura-ps-759-760-merge-owner` · `secuura-demo-kam-admin-default-password` · `secuura-f5-login-limiter-bypass` · `secuura-f5-demo-exposure-probe` · `secuura-f5-demo-interim-mitigation` · `secuura-demo-admin-transcripts` · `secuura-demo-admin-mfa` · `secuura-force-push-own-branch-standing` · `secuura-org-trust-boundary-within-tenant` · `secuura-archive-fifteen-platform-s-tickets` · `secuura-advisory-gate-moving-set` · `secuura-advisories-high-and-prod-reaching` · `secuura-four-advisories-ruled-after-measurement`

SELF-CHECK: re-read end-to-end for contradictions | 2026-09-11 13:37

PROVENANCE:
- seat number s179 follows s178 | /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/history.md top entry is s178 (line 24) | read 2026-09-11
- #953 open, not merged, base develop, head 8987b8a0e, 0 reviews; control #904 returns 1 review (PeterObeden APPROVED) through the same endpoint | https://api.github.com/repos/Secuura/Distributed_Secuura/pulls/953, /pulls/953/reviews and /pulls/904/reviews, run by Wednesday with the GH_TOKEN in /Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env | read 2026-09-11
- #953 has 2 issue comments, the newest the tier-1 verdict by kksecura at 2026-09-11T02:14:41Z; no tier-2 verdict comment | https://api.github.com/repos/Secuura/Distributed_Secuura/issues/953/comments run by Wednesday | read 2026-09-11
- origin develop 2d864ae9220c57ddcd8dc77af1b80fbd8001d530 and #953 head 8987b8a0ecfae29aed2b934188d947a1a6a581df | git ls-remote origin run by Wednesday on /Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files | read 2026-09-11
- KS-1086 In Progress, priority 1, on our board account, 3 comments, newest the round-2 READY at 2026-09-11T02:43:18Z; no tier-2 verdict comment | Secuura Linear GraphQL, comments(first:50) sorted client-side, run by Wednesday | read 2026-09-11
- KS-1086 scope sentence, quoted as s177's brief quoted it and not re-read by this seat | /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-09-11_s178_953-fix-round.md line 81 | read 2026-09-11
- tier-2 verdict GO WITH FINDINGS @ 8987b8a0e, QA-1 and QA-2 closed, 5 shapes with no false refusal, bite 14/14, bash 3.2 clean, QA-7 wording in the delta, QA-8 the pre-existing --list crash at :72 with the :92 fix shape | /Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-11-ks1086-953-8987b8a0e-tier2-r2/report.md lines 1-120 and 379-380 (the rest not read by Wednesday) | read 2026-09-11
- the current CLEAN predicate text | /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/push-protocol/push_protocol.py line 121 | read 2026-09-11
- the predicate rule and the four arms | /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/HANDOVER-s178-ks1086-round2.md lines 23-32 | read 2026-09-11
- #879 approved at 79f1fcb48 and #813's approval withdrawn 09-08 14:56Z | same handover line 38 (s178's reading, not re-derived by Wednesday today) | read 2026-09-11
- deploys held on the open KS-597 card; the undelivered ruled set | /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/tools/decision_queue.sh list open and list ruled --undelivered secuura- (Wednesday's tree, not yours) | read 2026-09-11
- the Wednesday rulings still operative | /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-09-11_s178_953-fix-round.md lines 50-54 and /Volumes/DevMASTER/WEDNESDAY/0_Brain/daily/2026-09-11.md entries 12:08 and 12:38 | read 2026-09-11
- the grep-function scope correction | /Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-11-ks1086-953-8987b8a0e-tier2-r2/report.md lines 42-43 and /Volumes/DevMASTER/WEDNESDAY/0_Brain/learnings/_ledger.md row 2026-09-11 on the tool-shell grep | read 2026-09-11
- tickets-only rule | /Volumes/DevMASTER/WEDNESDAY/0_Brain/learnings/2026-09-05_tickets-are-the-channel-whatsapp-via-kam-is-the-escalation.md | read 2026-09-11
