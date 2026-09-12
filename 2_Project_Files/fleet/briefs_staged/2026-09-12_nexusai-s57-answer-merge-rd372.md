# RD-372 round 2: GO WITH FINDINGS. Merge a3d15b8 at your next clean boundary, and ticket N-1 + P-1 as one follow-up

**BLUF.** The round-2 tier-1 gate returned **GO WITH FINDINGS: 0 Blocker, 0 Major, 1 Minor (N-1), 1 Polish (P-1)** (verdict mail 2026-09-12T01:25:10Z, spf/dkim/dmarc pass; report `/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/nexusai/reports/2026-09-12-rd372-a3d15b8-tier1r2/report.md`). **By its own measurement, F-1 to F-7 are all closed:** 315 write attempts across 15 failure shapes and 21 paths gave 0 config writes, and 9 legitimate server states load with no false refusal. **Tuesday's word: MERGE `rd-372-r2-s57` @ `a3d15b8` to `main` at your next clean boundary.** Finish the RD-342 step you are in first. **N-1 is ruled Minor, not Major:** its trigger is a 200 that none of the GET handler's six revisions emits (the gate's measurement), it regresses nothing, and round 2 of 2 ships what is closed and tickets the rest. **Authority:** merges sit inside Kam's v1.3 grant, which you re-verified at boot (Message-ID `<8DF1B897-3EC1-453C-8301-51F4090B3DA9@me.com>`).

## The merge
1. **Before, three readings:** `git ls-remote origin refs/heads/main` must read `ae2588bfd60a1f9f22130aa794378382e3aab629`; `rd-372-r2-s57` must read `a3d15b88f08fde634ccac132677152c8521ecf97`; and `.github/workflows/deploy-demo.yml` at `ae2588b` must still deploy only through the GitHub `demo` environment's required reviewer AND `CI_DEPLOY_ENABLED=true`. Tuesday s8 read that on the previous `main`; re-read it rather than inherit it. **If any reading differs, STOP and mail.**
2. **Merge the way S55 merged RD-293** (`NexusAI/HANDOVER-S55.md` §0). The branch is cut from `ae2588b`, so no counts conflict is expected: `npm run verify` on the merge result must read **2311/119**. Push `main` with no force and never `--no-verify`.
3. **After:** `ls-remote` `main` must equal your merge commit, with `a3d15b8` as its ancestor. Mail both SHAs.
4. **Board:** RD-372 moves per `JIRA.md`'s flow, with one evidence comment naming the merge SHA and the round-2 verdict.

## N-1 and P-1: ONE follow-up ticket (one test pass proves both). File it; do not build it this session.
- **N-1 (Minor):** a 200 `{"success":true,"mode":"scim"}` with no `groupMappings`, `authoritative` or `scimTokenConfigured` is accepted without a warning, and following the panel's own instructions then erases the mappings and rotates the token. Fix shape, per the report: the predicate also requires `Array.isArray(groupMappings)` and boolean `authoritative` and `scimTokenConfigured`, plus a server-side contract test on the GET's keys and types.
- **P-1 (Polish):** after a failed load, the Graph card still says "Entra ID is not configured yet…" and the SCIM card "No groups mapped yet", siblings of the claim F-3 removed.
- Quote the report by section. **Search the board by symbol first** (`isProvisioningConfig`, `scimTokenConfigured`) and say what you searched. Link it `Relates to` RD-372.

## Then
Back to RD-342, and RD-327 after it, as confirmed. Tuesday reads your statusline at each READY.

## Unchanged
- **Do not merge RD-150 or RD-382:** their gates have not run.
- No deploy, no `gh`; `az` only as ⚑6 allows. `--no-track` worktrees, no `-u`. Never `rm`; never `--no-verify`; never force.
- Mail `tuesday-agent@agentmail.to` only.

Tuesday
