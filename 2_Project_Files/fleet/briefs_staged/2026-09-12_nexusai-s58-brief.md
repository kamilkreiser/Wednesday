# BRIEF — Datasec/NexusAI S58: RD-327, the build digest on /api/health (tier 1)

**BLUF.** You are **S58**, a fresh NexusAI seat launched from `NexusAI/HANDOVER-S57.md`: **read it first, whole, then `NexusAI/HANDOVER-S55.md` for the standing holds** (S57's handover supersedes S55's wherever they differ). **ONE ticket: RD-327**, in the shape Tuesday RULED at S57's plan confirmation (⚑5, 2026-09-11T23:58:10Z); HANDOVER-S57 §1 carries it and this brief quotes it below. **Begin with a plan confirmation and wait for Tuesday's CONFIRMED.** Stop at READY FOR QA, tier 1. No other NexusAI seat is live: `datasec-nexusai@` is yours alone this session.

## PLAN CONFIRMATION (before any branch, commit or board write)
Boot as your launcher says. Read HANDOVER-S57 and HANDOVER-S55 whole. Mail Tuesday a QUESTION `plan confirmation (S58)` carrying: your launcher's preflight warnings VERBATIM (expect the RD-342 "scripts/preflight-gitleaks.sh not found in 2_Project_Files" WARNING, which is accepted as loud; quote it anyway); the exact files and line numbers where `build` lands, **re-derived at current `main`** (HANDOVER-S57 §1 read them at `ae2588b`); your RED test list; and anything in this brief you think is wrong. **Then stop and wait.**

## QUEUE
0. **RD-327.** Its title, quoted: *"The RD-302 deploy check requires a discriminating served probe, and the product gives a verifier none: the whole unauthenticated /api/health payload is status + timestamp + version, identical across builds"*. **Build exactly the ruled shape (⚑5):**
   - Serve ONE new field on the unauthenticated `/api/health`: **`build` = the first 16 hex characters of `sha256` over the 40-hex commit SHA**, baked at build time. **Not the raw SHA.** The reason is RD-329's principle: *"an unauthenticated endpoint carries COUNTS, never identifiers, because identifiers name a deployment's internals"*.
   - Wiring: `ARG` → `ENV` in the Dockerfile **production** stage, read **once at boot** and validated. Unset, empty or malformed serves the literal `"unknown"`. The field is **never omitted**. Never a runtime `git` read: the image has no repository.
   - `version` keeps its meaning as a separate field. `/api/admin/health` sits behind authentication and **may** carry the raw SHA; that half is optional, and READY says whether you built it.
   - Passing the build arg is a TEXT change in `.github/workflows/deploy-demo.yml`, `scripts/deploy-dev.sh` and the `DEPLOYMENT_GUIDE.md` recipe. **No image build, no deploy, no workflow run.** In `deploy-demo.yml` change only the build-arg wiring and quote the diff in READY.
   - **Must NOT be disclosed unauthenticated** (S57's list, confirmed): the image tag, the registry or ACR name, revision/replica/host names, the branch, the build time, Node/Express/SDK versions, env names or values, data-source/workspace/tenant/client ids, `DATA_DIR`/`DB_PATH`, the AI provider.
   - **The Marketplace/customer image path never passes the arg**, so customer deployments serve `"unknown"`. Say so in the ticket comment, and do not touch that path.
   - **RED first:** boot the real server with a fixed 40-hex value and assert `body.build` equals the first 16 hex of its sha256 computed IN the test (absent at base); unset → `"unknown"`; malformed (41 characters, uppercase, shell metacharacters, empty) → `"unknown"`; an exact key-set allowlist on the public body, so any future added field goes red; a control that `version` is still `2.0.1`. **A mutation that serves the raw SHA must turn a cell red.**
   - **Branch:** its own, from current `main` read from origin in your first git action (Tuesday read `34e7fc4eacb3a80425a2f3cdd993addf28050dad`), in its own `--no-track` worktree. Push with an explicit refspec, without `-u`.
   - **Board, exactly these writes:** one BLUF evidence comment on RD-327 at READY (the branch, the head, what `build` is and is not, the customer path's `"unknown"`), and the move to Testing. Nothing else is filed unless a finding needs a ticket; then search the board by symbol first and say what you searched.
   - **STOP at READY FOR QA. Tier 1.**

**READY FOR QA** = one mail: the branch, its 40-character head read from origin in the same action, the commit count on `main`, the files, the `npm run verify` VERDICT line verbatim, FOUND / TESTED / HOW with RED at base, and what was NOT done or NOT tested (a real image build is not authorised; say so). **This project merges on Tuesday's GO after a gate, so READY is a pushed branch plus a ticket comment; there is no PR.** Tuesday reads your statusline at READY; do not judge your own context.

## HOLDS
- **`2_Project_Files` is a stale snapshot under Kam's `investigate` ruling:** never restore, reset, check out, stash or write it. Work only in your own worktree.
- **The shared `2_Project_Files/.git/config`:** `--no-track` worktrees and no `-u`. Leave the existing `[branch]` sections in place. Never a bare `git pull` in `worktrees/rd-382-s55`: it tracks `main`.
- **A QA gate is running now on `rd-342-s57` and `rd-382-jira-site-scheme-s55`.** Do not push to, rebase, merge or write those branches or their worktrees, nor `rd-150-falsy-setting-s55`. **No merges of anything.**
- **The Marketplace package:** do not read into, check out or write `s51-marketplace-remediation`, the `wt-s51-mktremed` worktree, the `azure-marketplace/` templates, or any `evidence-s5*` folder.
- No deploy, no image build, no workflow dispatch. No `gh`. No `az` by hand; the launcher-mandated read-only boot feedback sweep is exempt (⚑6).
- **Never `rm`**, including scratch-harness resets: build each case in a fresh `mktemp -d`. `fs.rmSync` in a test's own `afterAll` is accepted. Never `--no-verify`, never force.
- **The vault:** do not pull, stash or write it.
- **Ticket creation:** the unit is the test pass (Kam, 2026-09-07 13:23): one ticket when one test pass proves it. Search the board by symbol or path before filing.
- Client-facing communication is ticket comments only.
- Mail `tuesday-agent@agentmail.to` only. Text at your prompt is not an instruction until the detector rules: a dim, unsent line is the generator; a submitted line from Kam is his channel.

## RULED BY KAM, NOT YET IN AN ARTEFACT
- `nexusai-main-tree-is-a-stale-snapshot` → **investigate** (2026-09-10 20:18). The option: *"Keep the tree as-is until the mechanism is explained, then restore."* Its default: *"Nothing moves. The stale tree stays, the NexusAI agent keeps working from its own worktree at cd2b543, and the mechanism stays unexplained."* **This session:** keep to your own worktree; the investigation is not this session's work.
- `nexusai-ai-screenshot-local-model` → **install-ollama** (2026-09-11 15:03), with Kam's note (dictated; "Fire 3" is Phi-3): *"Nexus II needs to be launched to the marketplace with GPT as its only option. No need for a VM with Fire 3."* **Not this session's work:** it belonged to S56's Marketplace round.
- `nexusai-marketplace-b2-registry-after-round4` → **publish-image** (2026-09-12 11:34): *"Publish a fixed image to a registry Kam names."* Kam has not named the registry yet. **Not this session's work:** nothing is built, tagged or pushed to any registry.
- `rd104-gh-identity-acceptance-false-premise` → **youcheck** (2026-09-07 19:58): *"You check the two settings pages yourself - two clicks"* (the `demo` environment's required reviewer, and the `CI_DEPLOY_ENABLED` variable). **Not this session's work:** this session merges nothing. It touches RD-327 in one place: your branch edits `.github/workflows/deploy-demo.yml`, the workflow those two settings gate, so change only the build-arg wiring there.

## RULED BY WEDNESDAY FOR THIS PROJECT, STILL OPERATIVE
(Tuesday is this project's coordinator; the gate's heading is shared tooling.)
- RD-327's shape (⚑5, 2026-09-11T23:58:10Z): queue item 0.
- ⚑6, same answer: the launcher-mandated read-only `az` feedback sweep is exempt from "no `az`".
- The RD-342 launch WARNING is accepted as loud; do not point the launcher at a worktree (01:42:06Z).
- No `rm` in harnesses; a fresh `mktemp -d` per case (01:28:25Z).
- The four Dependabot alerts on the default branch are Tuesday's to carry; no placeholder ticket (01:42:06Z).
- The shared-config tracking sections are LEFT (2026-09-11T23:05:18Z).
- RD-150, RD-342 and RD-382: nobody merges them before a GO.
- `s55-history-docs` @ `a39e93d` and `s57-history-docs` @ `e354a40` are not merged, and merging them is not authorised.

PROVENANCE:
- RD-327 To Do / High; its title as the scope sentence | Jira REST read with NexusAI's creds under the read-only grant, run by Tuesday s10 | read 2026-09-12
- RD-302 Testing (open, last comment 2026-09-04T12:54), named only inside RD-327's quoted title and NOT queued in this brief | Jira ticket RD-302, REST read with NexusAI's creds under the read-only grant, run by Tuesday s10 | read 2026-09-12
- RD-327's ruled shape (the build digest, ARG → ENV, "unknown", never omitted, the admin route may carry the raw SHA, the do-not-disclose list confirmed) and ⚑6 | Tuesday ANSWER 2026-09-11T23:58:10Z, /Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/fleet/briefs_staged/2026-09-12_nexusai-s57-answer-plan.md, sections ⚑5 and ⚑6 | read 2026-09-12
- the RD-329 principle, quoted | the same answer's ⚑5, which records Tuesday s9's read of RD-329; not re-read by Tuesday s10 | read 2026-09-12
- landing points, the do-not-disclose list, the RED plan, the customer path serving "unknown" | /Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/HANDOVER-S57.md §1, S57's reading at ae2588b, not re-derived by Tuesday | read 2026-09-12
- main 34e7fc4eacb3a80425a2f3cdd993addf28050dad | git ls-remote origin from NexusAI's checkout, run by Tuesday s10 | read 2026-09-12
- the QA gate running on rd-342-s57 and rd-382-jira-site-scheme-s55 | launched in pane %16 at 12:08 by Tuesday s10 and read at rung 5 in that pane | read 2026-09-12
- the four ruled cards, their choices and timestamps, the stale-snapshot default text, the youcheck option text | decision_queue.sh list ruled --undelivered and show, run by Tuesday s10 | read 2026-09-12
- the stale-snapshot option text and Kam's install-ollama note | the S57 brief's RULED BY KAM section, /Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/fleet/briefs_staged/2026-09-12_nexusai-s57-brief.md | read 2026-09-12
- the holds on 2_Project_Files, the shared config, rm, Dependabot, the history branches and the launch WARNING | /Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/HANDOVER-S57.md §3 to §5 and /Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/fleet/briefs_staged/2026-09-12_nexusai-s55-answer-ready-rd382.md | read 2026-09-12
- no other NexusAI seat live | tmux list-panes, run by Tuesday s10: only the coordinator, the monitor and the QA gate pane | read 2026-09-12
- seat number S58 | HANDOVER-S57's title names seat S57 as the last | read 2026-09-12

SELF-CHECK: re-read end-to-end for contradictions | 2026-09-12 12:12
