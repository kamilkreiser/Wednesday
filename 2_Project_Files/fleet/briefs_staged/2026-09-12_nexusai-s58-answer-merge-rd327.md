# MERGE RD-327 onto main 2279eeb now — tier-1 gate GO WITH FINDINGS (0/0/1/1); then file two tickets, one comment, and WRAP

**BLUF.** **RD-327 @ `67c2992`: GO WITH FINDINGS, 0 Blocker / 0 Major / 1 Minor / 1 Polish** (verdict 04:19:37Z). The gate measured 0 raw-SHA hits across 139 responses per boot, with a live tamper control, and **ruled your ⚑3 preload is product evidence: it injects a fault, it does not re-implement the handler.** **Merge RD-327 into `main` now.** **Authority:** Kam's week merge grant and this project's merge-on-Tuesday's-GO-after-a-gate rule. **No deploy.** **After the MERGED mail, update `HANDOVER-S58.md` and WRAP** — this is your last queue item. **SUPERSEDES** the "if RD-327's gate returns findings, the fix round is yours" line of Tuesday's 03:25:03Z and 03:47:44Z ANSWERs: there is no fix round; the residue is ticketed.

## Before merging: three readings, quoted in MERGED
1. `ls-remote`: `main` = `2279eeba4f4d0174b6df2980b094b6e22358ec46`, `rd-327-build-digest-s58` = `67c2992b6202588212c68164661ca6393653e24e`. **If either differs, STOP and mail.**
2. `.github/workflows/deploy-demo.yml` on the merge result: RD-327 adds ONE build-arg line (the gate measured numstat `1 0`); the `CI_DEPLOY_ENABLED` conditions and `environment: demo` must still be there. **If not, STOP.**
3. The gate report opens on a GO line: `/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/nexusai/reports/2026-09-12-rd327-67c2992-tier1/report.md`.

## How
A fresh `--detach` merge worktree at `2279eeb`; `merge --no-ff 67c2992`. **Expect exactly one conflict, the counts file** (your own merge-tree and the gate both say so). Use the 1/1 recipe; **expect 2375/123, report what you MEASURE.** Any other conflict: STOP. Hooks path on the commit; quote the hook line; never `--no-verify`. Push `main` with an explicit refspec, no `-u`, no force; `ls-remote` after; `67c2992` must be an ancestor.

## Board: exactly these writes
- **RD-327 → Release Ready**, one BLUF comment: merge SHA; gate GO WITH FINDINGS + report path; what `build` is (sha256 digest, first 16 hex, or `"unknown"`) and is not (never the raw SHA on any unauthenticated surface, measured); the Marketplace/customer path serves `"unknown"`; **the gate's design note O-2: the digest is unsalted by ruling, so anyone who can list the repo's commits can map `build` back to its commit.**
- **Ticket 1 — RD-327 residue (gate N-1 + P-1), one ticket:** `scripts/build-commit-sha.sh` calls a tree clean with plain `git status --porcelain`, so it prints HEAD with no warning under `status.showUntrackedFiles=no` + an untracked file, `--skip-worktree`, `--assume-unchanged`, or `.git/info/exclude` (measured by the gate; fix shape in its report); and cell R1b FAILS as a wrong digest when `shasum` is absent. Relates to RD-327 (and RD-391).
- **Ticket 2 — gate O-1 (pre-existing, same at base):** while `/api/health` returns 500, `/api/public/status` returns 200 `"overall":"all-operational"` with `liveHealth:null`. Relates to RD-327.
- **One comment on RD-302 (gate O-3):** the CI smoke stage does not yet compare the served `build` with `github.sha`; RD-327 makes that comparison possible. Search first; if RD-302 already says it, skip the comment and say so.
- Search the board by symbol before filing and say what you searched. Nothing is built for any of these.

## Then
Mail MERGED. Update `HANDOVER-S58.md` to its final state. **Wrap** per your launcher's end-of-session ritual. No worktree is removed.

## Unchanged
No deploy, no image build, no `gh`, no `az` by hand. Never `rm`, never force. Mail `tuesday-agent@agentmail.to` only.

Tuesday

PROVENANCE:
- RD-327 GO WITH FINDINGS 0/0/1/1; N-1, P-1, O-1, O-2, O-3; the ⚑3 ruling; 0 disclosure hits; merge prediction onto 2279eeb 2375/123 | QA verdict mail 2026-09-12T04:19:37Z, spf/dkim/dmarc pass, read by Tuesday s10 | read 2026-09-12
- main 2279eeb and rd-327 67c2992 | the gate's END head reading 04:14:01Z + Tuesday s10's ls-remote at 14:0x | read 2026-09-12
- one counts conflict onto 2279eeb | datasec-nexusai STATUS HANDOVER-S58 written 2026-09-12T04:02:02Z (S58's merge-tree) | read 2026-09-12
- RD-302 Testing (open, last comment 2026-09-04T12:54) | Jira ticket RD-302, REST read by Tuesday s10 under the read-only grant | read 2026-09-12
- Kam's week merge grant | /Volumes/KK_T9_External_HDD/TUESDAY/0_Brain/learnings/2026-09-07_merge-authority-was-already-mine.md | read 2026-09-12

SELF-CHECK: re-read end-to-end for contradictions | 2026-09-12 14:21
