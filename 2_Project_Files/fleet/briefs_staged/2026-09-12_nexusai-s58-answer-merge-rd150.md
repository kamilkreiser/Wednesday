# MERGE RD-150 onto main `7a11418` now — tier-1 gate GO WITH FINDINGS (0/0/2/1); one counts conflict predicted (2338/122); TWO residue tickets

**BLUF.** **RD-150 @ `bec76f6`: GO WITH FINDINGS, 0 Blocker / 0 Major / 2 Minor / 1 Polish** (verdict 03:45:01Z). **Merge it into `main` now** — the first of the two merges Tuesday's 03:25:03Z ANSWER told you to hold for. **Authority:** Kam's week merge grant (merge on Tuesday's GO once the gate has passed, through Sunday 13 September) and this project's merge-on-Tuesday's-GO-after-a-gate rule. **No deploy.** RD-327's merge still waits for its own gate, which launches now.

## Before merging: three readings, quoted in your MERGED mail
1. **`ls-remote`:** `main` = `7a11418e605a9e371561be8f7dc1514b35cd01ac` and `rd-150-falsy-setting-s55` = `bec76f686de5415090350117437d11d1a49acb82`. **If either differs, STOP and mail.**
2. **`.github/workflows/deploy-demo.yml` at `main`** still carries the `CI_DEPLOY_ENABLED` conditions and `environment: demo`, as you read them at 02:59Z. **If not, STOP and mail.**
3. **The gate report opens on a GO line:** `/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/nexusai/reports/2026-09-12-rd150-bec76f6-tier1/report.md`.

## How
- **A fresh `--detach` merge worktree** from `origin/main` at `7a11418`.
- **`merge --no-ff` `bec76f6`.** The gate predicted, in its own clone, **exactly one conflict against `7a11418`: `scripts/verify-expected-counts.json`.** Resolve it with your recipe (a `1/1` placeholder, then `npm run verify -- --update-counts`); **expect 2338/122 and report what you MEASURE.** The branch is three merges behind `main`: **any other conflict, STOP and mail.**
- Commit with the hooks path and quote the hook's line. Never `--no-verify`.
- **Push `main`** with an explicit refspec: no `-u`, no force. `ls-remote` afterwards; **`bec76f6` must be an ancestor.**

## Board: exactly these writes
- **RD-150 → Release Ready**, with one BLUF comment carrying the merge SHA, the gate's GO WITH FINDINGS and report path, and **the deploy behaviour change as the gate measured it:**
  - a stored `red_flag_enabled=false` with a live frequency **stops risk-alert digests** after deploy (intended);
  - a stored `aiEnabled=false` flips the setup API to "disabled" **while AI keeps working** (ticket 1 below);
  - **the live demo and dev stores' values are UNMEASURED** — one key each (`red_flag_enabled`).
- **File TWO tickets** (Kam, 2026-09-07 13:23: separate fixes). Search the board by symbol first and say what you searched; link each `Relates to` RD-150.
  1. **`aiEnabled` is display-only (gate F-1).** With it stored `false`, `GET /api/setup/ai-model` reports disabled, but `POST /api/chat` still calls the LLM; no other reader exists; the product's writer is `POST /api/setup/ai-config {skipped:true}`. **Two fix shapes, NEITHER chosen here:** gate AI on it (this changes deployed behaviour for any tenant that stored `false`), or document it as informational. Say both in the ticket.
  2. **`red_flag_enabled` stored as `''` or `0` shows the toggle OFF (`settings.js:937`) while the scheduler runs (gate F-2, pre-existing),** plus **F-3:** the scheduler log prints an empty value for a stored `''`.
- Nothing is built for either.

## After the merge
Mail MERGED, then **HOLD again** for RD-327: its merge comes only on its own ANSWER after its gate. Wrap only on Tuesday's mail or the 80–90 band.

## Unchanged
No deploy, no image build, no `gh`, no `az` by hand. Never `rm`, never force. No worktree removed. RD-327's branch is not merged. Mail `tuesday-agent@agentmail.to` only.

Tuesday

PROVENANCE:
- RD-150 GO WITH FINDINGS 0/0/2/1, F-1..F-3, the deploy behaviour change, the merge prediction against 7a11418 (one counts conflict, 2338/122) | QA verdict mail 2026-09-12T03:45:01Z, spf/dkim/dmarc pass, read by Tuesday s10 | read 2026-09-12
- RD-150 Testing (open; last comments 37339 READY and 37340 correction) | Jira ticket RD-150, REST read with NexusAI's creds under the read-only grant, run by Tuesday s10 | read 2026-09-12
- main 7a11418 and rd-150-falsy-setting-s55 bec76f6 | git ls-remote origin from NexusAI's checkout, run by Tuesday s10 at 13:2x, and the gate's END reading 03:36:56Z | read 2026-09-12
- the deploy-demo.yml guards and the 1/1 counts recipe | datasec-nexusai STATUS MERGED 2026-09-12T03:22:45Z (S58's own readings) | read 2026-09-12
- Kam's week merge grant | /Volumes/KK_T9_External_HDD/TUESDAY/0_Brain/learnings/2026-09-07_merge-authority-was-already-mine.md | read 2026-09-12

SELF-CHECK: re-read end-to-end for contradictions | 2026-09-12 13:47
