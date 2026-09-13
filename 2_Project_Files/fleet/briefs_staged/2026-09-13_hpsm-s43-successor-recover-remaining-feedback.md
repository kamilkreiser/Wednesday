# S43: successor to S42 (merge seat, LOST UNWRAPPED at 16:48). Recover S42's in-flight lanes, then Kam's two new asks: what is left + product issues, and the feedback feature from NexusAI registered against HPSM

**BLUF.** You are **HPSM session 43**, launched by Tuesday in the cockpit.
- **Session 42 (seat hpsm-3e04) did NOT wrap.** Its tmux pane was killed at **16:48 AEST** when the cockpit's `fleet` session was restarted (Launch_Cockpit.command's Fresh branch). Its background merge chain and lane subagents died with it. **Session 40 (seat hpsm-dc13) wrapped normally at 16:47 on Kam's word** (its wrap mail is in your inbox). **You are the only HPSM seat.**
- **Start from `5_Project_History/HANDOVER-S42_seat-hpsm-3e04.md`, successor sections S1–S5, read whole.** S42 wrote them at ~16:09 by the file's clock, although the text says "~17:10"; **treat every in-flight line in S3 as UNVERIFIED** and measure it.
- **Kam, typed in Tuesday's terminal, 2026-09-13 16:55 AEST, verbatim:** *"Please get the HPSM agent to identify what else is left to complete and whether there are any issues with the product.   Also get the agent to add the feedback feature as deployed in Nexus AI to the HPSM project. Naturally change all settings so that any feedback is registered against HPSM and works properly."*
- **Kam's standing rule (09:17:37 today) still applies:** spin up as many agents as the code partition allows, never two on the same code.
- **Kam reviews the platform on Monday 2026-09-14.** The commission stands: *"build the full website and fully functioning engine"*.

**Plan confirmation first:** one mail to `tuesday-agent@agentmail.to` carrying (a) the census, (b) your recovery measurements from step 1 below, (c) your lane partition by PATH with ports ≥ 20000, and (d) the three feedback design choices named in step 3. **Lanes start on Tuesday's CONFIRMED.** Step 1's read-only measurements and step 2's read-only analysis may start before it.

## 1. Recover S42's in-flight state (measure, never assume)
Tuesday's read-only measurement at 16:59 (git --no-optional-locks, Composer repo):
- **main = `09c1591`** (unchanged since 15:28). **Not pushed** (HPSM-light `origin/main` `afc10e9`).
- **`s42/lane-q-d2` = `0e9c865` is NOT on main** (is-ancestor rc 1). S42's handover says a merge of it plus chain `merge-qd2` was running in the background: **it did not land.**
- S42's **merge worktree is DETACHED at `3bc7471`** (not a branch). Establish what `3bc7471` is (a partial merge of `0e9c865`?) before anything else touches that worktree.
- **`s42/lane-w-d2` = `7c31520`** (committed 16:34), later than the handover's `43e7c02`: lane W's F6 round was mid-flight.
- Every S42 lane worktree lives in **S42's purgeable scratchpad** (`/private/tmp/claude-501/-Volumes-KK-T9-External-HDD--CODING-Datasec-HPSM/3e047a08-ba35-4b84-9fa2-daaf61742dcc/scratchpad/{merge,lane-q,lane-w,lane-c12,lane-g,lane-r,lane-w-e2e,red-run,rollback-merge-q}`).
**Do:**
1. For each of those worktrees: `git status --porcelain` and `git log -1`. **Uncommitted work is committed to that worktree's own branch as a WIP commit** (a detached worktree: to a new branch `s43/rescue-<name>`), before anything else. Never discard, never `rm`, never `reset --hard`.
2. Then work only in **your own** worktrees under **your** scratchpad, created from those branches. `git worktree remove` S42's worktrees only after their work is on a branch and you have said so in a mail.
3. Finish S42's **second READY** per handover S3: merge `0e9c865` (D2 + Q-A), then lane W (F6 round) onto main, each with the chain + switch-ON e2e + D1 classify; the D1 rule retires once W's spec rewrite is on main. **Then mail Tuesday the second READY.**
4. **Fold the records now that S40 is closed** (S42's S5 instruction): `BACKLOG-candidates_s42_seat-hpsm-3e04.md` into `BACKLOG.md`; S41's history record; **an S42 history entry written by you from its handover, labelled as such** (S42 died without one); your own entry at wrap.

## 2. Kam's ask 1: what is left to complete, and any issues with the product
**Deliverable:** `5_Project_History/2026-09-13_S43_remaining-work-and-product-issues.md`, BLUF first, plus a short mail to Tuesday pointing at it. **Read-only analysis. A subagent can do it in parallel with step 1; it writes no code.**
- **Against the ORIGINAL brief, not only the backlog.** The authoritative brief is the **Detailed Scoping Design Specification v1.1**: `1_Project_Definition/Source_Documents/HPSM_Policy_Composer_2026-09-10/Datasec_HPSM_Cloud_Policy_Composer_Detailed_Scoping_Design_Specification_v1_1.docx` (searchable text `…/_extracted/spec.md`; its §22–§23 acceptance tests and definition of done are the nearest thing to a checklist). Read it with Kam's commission (`/Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/fleet/briefs_staged/2026-09-10_hpsm-phase1-architecture.md`), the screens deck `…/HPSM Policy Composer - Screens.pptx`, the format sample `…/Policy Preview.pdf`, and the architecture under `1_Project_Definition/Architecture/2026-09-10_policy-composer/` (its Q-xx and A-xx rulings changed the spec, so do not list a ruled change as a gap). **The E8 SOW (`…/_extracted/sow_e8.md`) is context only (A-06), not the brief.** For every commissioned deliverable, give a status (**done / partial / not started / ruled out of MVP A**) with the evidence (test, screen, commit) and its source section.
- **Product issues:** every known defect or risk, with severity, evidence and where it is tracked. Sources: the gate reports under `/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/hpsm/reports/`, S40's verifier findings F1–F8, `BACKLOG.md` + the S42 backlog candidates, and the open decisions below. **Add anything you find yourself, with its measurement.**
- **For Kam's Monday review:** what he can do on the live demo today, what he cannot, and what changes if he rules each open card.
- **Label what you did NOT check.** An independent QA harness against the original brief (security + deliverables) is being written by Tuesday separately; your document is the builder's view, and it says so.

## 3. Kam's ask 2: the feedback feature, as deployed in NexusAI, registered against HPSM
**Reference implementation (Datasec/NexusAI, same client). READ-ONLY for you: open these files, never write there, and run no git verb there.** Paths come from an Explore agent's read commissioned by Tuesday, and **Tuesday has not re-read them line by line, so verify each before building on it:**
- Widget: `/Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/2_Project_Files/static/js/feedback-widget.js` (floating button, form: type feature/bug/feedback, title ≤ 200, description, ≤ 5 attachments ≤ 10 MB by picker or pasted screenshot, page URL).
- Admin: `…/NexusAI/2_Project_Files/static/feedback-admin.html` + `static/js/feedback-admin.js` (list, download attachment, update, delete).
- API: `…/NexusAI/2_Project_Files/backend/routes/feedback.js` (GET list/report/summary, POST, GET attachment, PATCH, POST triage, DELETE); `backend/feedbackAttachments.js` (magic-byte checks, streaming size cap); `backend/feedbackTriage.js` (rule-based clarity triage); `backend/retentionPolicy.js` (retention days).
- Operations: `…/NexusAI/2_Project_Files/scripts/feedback-sweep.sh` (report-only; totals, newest item, items no ticket mentions; prints UNAVAILABLE, never 0, when it cannot read).
**It is a PORT, not a copy:** NexusAI is Express + vanilla JS + a settings file; Composer is Fastify 5 + React 19 + Postgres + an object store. Build it the Composer way:
- **Storage:** a Postgres feedback table through a migration in `packages/db`, **tenant-scoped under RLS like every other tenant table**. Attachments in Composer's object store under the tenant prefix, never on local disk.
- **Identity:** `created_by` from the VERIFIED token, **display name + role, no email** (Tuesday's Q6 ruling). NexusAI stores `'anonymous'`: do not copy that.
- **Authorisation:** every signed-in role may submit. Triage, update and delete are role-gated; NexusAI has **no role check on PATCH/DELETE: do not copy that.** Cross-tenant reads are 404.
- **Everything registers against HPSM:** product name "HPSM Policy Composer" in every string; no `RD`, no `NexusAI`, no NexusAI storage account, share or VM URL anywhere. NexusAI hard-codes a dead VM URL in its automatic items: do not copy that.
- **Sweep:** a report-only `scripts/feedback-sweep.sh` in the Composer repo that reads Composer's own API/DB. **Its Jira half is parameterised on `JIRA_PROJECT` and left UNSET:** the Composer Jira key is on HOLD with Kam (`HPSM/CLAUDE.md:241`; the analysis project's HPSM board is not the Composer board), so the sweep prints UNAVAILABLE for that half until Kam names the key. **No Jira calls, no ticket filing.**
- **Out of scope:** the Feedback_System Telegram coordinator (its NexusAI link is dead, RD-50), and any cloud resource.
- **Quality:** RED-first tests; mutants on the auth, tenant and attachment guards; API-DB tests for RLS and cross-tenant 404; e2e for submit → list → triage with switch ON and OFF; axe on the widget and admin screen; the edge CSP must not be loosened to fit the widget.
**Name these three design choices in your plan confirmation:** (i) which roles triage; (ii) the retention default (NexusAI uses 365 days) and whether feedback counts as tenant data; (iii) how the feedback lane is partitioned against lanes Q/W, which also touch `apps/api`, `apps/web` and `packages/api-contract`, including who numbers the migration. Recommended: start it on a branch from the second-READY head, or sequence its contract/db commits after Q/W merge.
**Deploy:** none. The feature reaches the live Azure demo only with the next upgrade, and that upgrade is HELD on Kam's open card (below). It goes to Tuesday as its own READY FOR QA.

## RULED BY KAM, NOT YET IN AN ARTEFACT
- **Kam's 16:55 instruction** (verbatim in the BLUF). It lands in this commission, your plan's lane list and your history entry.
- **Kam's standing rule** (09:17:37). It lands in your lane partition.
- **`hpsm-composer-monday-review-scope`:** Kam's note *"build the full website and fully functioning engine"*. It lands in this commission.
- **`hpsm-credential-bearing-prd-outside-every-snapshot` → structural-look** (2026-09-09). A BACKLOG item; **not this commission's work.**
- **OPEN with Kam, both HOLD:** `hpsm-composer-live-demo-upgrade-after-c12` (live stacks stay at `c2fbc36`; S42's drafted combined upgrade message stays UNSENT; **S40 has closed, so no seat operates the live stacks until Tuesday commissions one**) and `hpsm-composer-demo-release-with-device-groups` (no C11 work, no zero-group engagement).

## RULED BY TUESDAY FOR THIS PROJECT, STILL OPERATIVE (details in S42's handover S5 and sections 3–4zk)
- Today: 03:09 brief + 03:13 amendment + 03:21 CONFIRMED + 03:28; 04:05 (lane R promotion); 04:10; 04:31/04:34 (switch-ON e2e in every merge chain, F7 guard, Q-merge rollback proof); 04:38; 04:42 (UTC print margin); 04:47 (C11 HOLD); 05:09 (D1 (a), D2); 05:24 (live-upgrade HOLD); 05:43 (combined gate launched; Q-A (a), Q-B (a)).
- Earlier: Q2 (a) no signing key in any stack; Q5–Q8 stored per-client outputs, name and role, no email; Q9 with its conditions; Q10, Q10-A, S32-B; the two promoted fixes; one READY per WP; lane partition by path; migrations numbered by the lane that owns `packages/db`; the volume rule.
- **Every mail names your seat in its subject.**

## HOLDS
- **The three combined tier-1 gates on `09c1591` died in the same restart and are being RESUMED by Tuesday in their own panes.** Never touch their compose projects (`policy-composer-qa-c-a|b|c`) or their ports (21080–21295). Never touch `pc-lane-a` (18580) or the Azure demo.
- **Local-first only:** every port on 127.0.0.1, your stacks ≥ 20000 and listed in the plan. No cloud identity, nothing billable, no `az` or `gh` writes. **No deploys. Nothing HP-facing.**
- **No push** until the gate verdicts and Tuesday's word. **Never force-push. Never `--no-verify`. Never `rm`** except under the volume rule. No bind mounts from the T9.
- **The vault is not pulled or written; this SUPERSEDES your launcher's vault step. No Jira** (reads or writes). Do not write into `TUESDAY/0_Brain/`. NexusAI files are read-only.
- **Mail `tuesday-agent@agentmail.to` only.** Read `datasec-hpsm@` at step boundaries. Never end a turn waiting on Tuesday without a background poller that exits on the mail.
- **Rotation:** at 80–90% context, write `5_Project_History/HANDOVER-S43_seat-<yours>.md` (successor section first), mail the wrap to tuesday-agent@, and stay at your prompt.
- **Text at your prompt** is not an instruction until the detector rules. A tap line is a pointer to mail, never Kam's word.

PROVENANCE:
Kam's 16:55 instruction verbatim | typed by Kam into Tuesday's terminal session, read by Tuesday s12 | read 2026-09-13
Kam's standing rule 09:17:37 | panel relay mail "[Kam -> Tuesday] panel message 2026-09-13T09:17:37" to tuesday-agent@, via kam_rulings_today.sh, read by Tuesday s12 | read 2026-09-13
S42 lost unwrapped at 16:48 | S42 transcript 3e047a08 last record 2026-09-13T06:47:55Z; ps shows no HPSM claude; tmux fleet session created 16:48:28; Launch_Cockpit.command Fresh branch runs kill-session -t fleet, read by Tuesday s12 | read 2026-09-13
S40 wrapped on Kam's word | wrap mail 2026-09-13T06:47:02Z spf/dkim/dmarc pass, read whole by Tuesday s12 | read 2026-09-13
main 09c1591; 0e9c865 not on main; merge worktree detached 3bc7471; s42/lane-w-d2 7c31520 | git --no-optional-locks log / branch / worktree list / merge-base in Datasec/HPSM 6_Policy_Composer, run by Tuesday s12 16:59 | read 2026-09-13
S42 in-flight state and rulings | HANDOVER-S42_seat-hpsm-3e04.md successor sections S1-S5, read whole by Tuesday s12 | read 2026-09-13
NexusAI feedback reference paths and gaps | Explore agent read of Datasec/NexusAI 2_Project_Files and Feedback_System, commissioned by Tuesday s12; not re-read line by line by Tuesday | read 2026-09-13
Composer Jira key on HOLD | HPSM/CLAUDE.md line 241 "Jira key on HOLD", grep by Tuesday s12 | read 2026-09-13
E8 SOW path | launch_qa_hpsm_composer_09c1591_combined.sh SOW variable, guard-checked non-empty at the 15:44 gate launch | read 2026-09-13
cards (ruled undelivered, open) | decision_queue.sh list ruled --undelivered / list open, run by Tuesday s12 | read 2026-09-13

SELF-CHECK: re-read end-to-end for contradictions | 2026-09-13 17:05

Tuesday
