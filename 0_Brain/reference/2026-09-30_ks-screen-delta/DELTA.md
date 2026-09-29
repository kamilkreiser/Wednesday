# KS board delta since the 09-29 screen — Spark predicate, 2026-09-30

Written 02:43 AEST 2026-09-30 (shell `date`; 2026-09-29T16:43Z) by a Spark brief-writer sub-agent for Wednesday. Secuura/Blockchain only. **Read-only:** the board was read over GraphQL with no mutation; nothing was posted, moved, commented, raised or mailed; no file under `!CODING/` was written. The 09-29 screen this extends is `0_Brain/reference/2026-09-29_ks-screen/SCREEN.md` (its "none updated since 2026-09-27T20:00Z" premise is what this re-measures).

## BLUF

- **Delta: 29 KS issues** in Backlog/Todo (state type `backlog` or `unstarted`), created or updated after 2026-09-29T00:00Z. That is a real count, not a cap: `fleet/board_count.sh` reported `TOTAL=29 (limit was 250)`.
- **Excluded: 3** on Peter (KS-982, KS-984, KS-985) and **0** on Stuart. That leaves **26 read in full**: each description plus every comment. `comments(first:50)` had `hasNextPage=false` on all 26.
- **Spark-briefable: 1, conditional on a carve.** That is **KS-1015**, carved to ONE pair from its 09-29 comment: `GET /api/referrals/{code}`'s declared 200 response in `services/referral/src/referral.openapi.ts:480` becomes the `{ success, data: {…} }` envelope the handler returns (`routes/referrals.ts:105`). The comment spells out the direction ("the spec should change to match the runtime … adding those fields to the handler … would be the wrong fix"). The same file already declares this envelope for a sibling (`POST /generate` 201, the KS-498 comment). The condition: KS-1015 is a register, and the comment says "please split them out if you'd prefer". Carving it or splitting it is Wednesday's call. The round would ref KS-1015 and not close it.
- **The other 25 fail the predicate.** The reasons, by frequency:
  - 8: a decision or ruling is needed first, or the ticket says the fix shape is "not chosen" (KS-953, 955, 964, 1178, 1384, 1389, 1390, 1393).
  - 6: multi-file, a register or an umbrella (KS-723, 772, 1355, 1381, 1382, 1385).
  - 4: an auth, token, credential or security surface (KS-1102, 1357, 1377, 1383).
  - 4: build, lockfile or frontend work that no checker tier can run in-process (KS-1379, 1380, 1387, 1391).
  - 2: `.github/workflows`, which is excluded (KS-1162, 1392).
  - 1: docs or config with no failable test (KS-1388).
- **Board size, for scale:** Backlog `TOTAL=239` and Todo `TOTAL=34`, 273 in all, each counted by `board_count.sh` against a limit of 250. The 09-29 screen had 237 + 30 = 267.

## The predicate and the instrument

**Predicate** (SCREEN.md method; kit `02_FOR_THE_COORDINATOR.md` §2). A ticket passes only if ALL of these hold:
1. One product file.
2. The fix shape is spelled out.
3. A runnable in-process test exists to copy.
4. It is not an auth, token, credential or security surface.
5. It is not already at the round counter.
6. It uses a runner the checker can run.

The exclusions SCREEN.md applied still stand: KS-1054 startup-migration and /health, the security `index.ts` validate/revoke paths, `.githooks`, `.github/workflows`, and anything on Peter or Stuart.

**Runner note, new today.** The Spark has now passed a round on the **bash_patch** tier: product `.sh` plus an existing `*.test.sh` modified in place (KS-1054 N-1350-1, `local-model/runs/spark_secuura_2026-09-30_KS-1054-N-1350-1`). So "bash outside `services/`" is no longer a harness refusal on the Spark path. That was half of SCREEN.md's reason for rejecting KS-1355 spot 1. The other half, an undesigned output format, still stands.

**Count.** Commands:
- `set -a; . <Secuura Blockchain 4_Credentials/.env>; set +a`, sourced transiently. The key was never printed.
- `bash fleet/board_count.sh linear LINEAR_API_KEY '{ team: { key: { eq: "KS" } }, state: { type: { in: ["backlog", "unstarted"] } }, or: [ { createdAt: { gt: "2026-09-29T00:00:00.000Z" } }, { updatedAt: { gt: "2026-09-29T00:00:00.000Z" } } ] }'` gave `TOTAL=29`.
- The unfiltered Backlog+Todo query printed "MORE PAGES EXIST — this is not a total" at 250, so it was split by state: `backlog` gave 239 and `unstarted` gave 34.

**Pull.** One paginated GraphQL read with the same filter, `first: 50`, run to `hasNextPage=false`: 1 page, 29 nodes, matching the count. It fetched identifier, title, state, assignee, labels, dates, description, `comments(first:50)` and attachments into this session's scratchpad (`n1350/delta.json`), not into the brain.

**Round counter (KS-1015).**
- `^KS-1015` in `night/done.md`: 0.
- `READY_KS-1015*` in `night/`: 0.
- Positive control: `^KS-908` in `done.md` gave 3.

**Collision (the carve).**
- PR heads #1351 (`eac2dae2afb7`), #1352 (`6e84a130dae7`) and #1353 (`2b8414090bb8`) were fetched into this session's scratch clone and diffed `--name-only` from their merge-base with develop `37205947d`.
- Result: 0 paths under `services/referral/`.
- Control: the same instrument counted 3 `deployment/azure/` paths on develop's #1350 squash and 1 `Blockchain/` path on #1353.
- The full open-PR census (older live heads) was NOT re-read. See NOT COVERED.

## Every ticket read (26), one line each

| Ticket | State | Verdict | Reason (with where it was read) |
|---|---|---|---|
| KS-723 | Todo | NOT | Bulk OpenAPI authoring of about 157 operations over four or more PRs. The description calls it "Peter-sized". The 09-29 comment adds slice-order advice only. |
| KS-772 | Todo | NOT | A review-stream umbrella of 20 tickets. All 34 comments are develop/kintsugi notices, the last dated 09-23, so the 09-29 update is metadata. |
| KS-953 | Backlog | NOT | Decision: "Shapes worth considering (not chosen — this needs a decision)". No comment after 09-13. Unchanged from SCREEN.md. |
| KS-955 | Backlog | NOT | Decision: "Fix shapes (not chosen)". No comment after 09-10. Unchanged. |
| KS-964 | Backlog | NOT | Decision: quarantine 104 files, "do not delete". No comment after 09-08. Unchanged. |
| **KS-1015** | Backlog | **SPARK-BRIEFABLE AS A CARVE (conditional)** | The ticket is a register of 28+ pairs, so it is NOT briefable whole. Its 09-29 comment adds 2 pairs. **The referral pair passes:**<br>1. One file: `referral.openapi.ts:480` is `schema: ReferralCodeSchema`, 1 hit. The regenerated `docs/openapi/secuura-api.yaml` goes as a raise-seat companion, the KS-747 precedent.<br>2. Shape spelled out: the runtime body is quoted, and `routes/referrals.ts:105` was read.<br>3. Test to copy: KS-747's spec-registration vitest. Referral runs `vitest run`.<br>4. Not auth: a bearer lookup route, and its spec's `security` is not touched.<br>5. Counter: 0.<br>6. Runner: vitest under `services/`.<br>**The delegations pair fails:** the handler returns `{ delegation, chain }` against a flat spec, and no direction is given. Condition: Wednesday decides the carve (the register is Kamil's). |
| KS-1102 | Backlog | NOT | Auth gating of `/system/status` and the dashboard, with a choice between "gate … or serve a public variant". Security surface and a decision. |
| KS-1162 | Backlog | NOT | `.github/workflows` (excluded). The fix is "derive … or delete … needs Kam's nod". |
| KS-1178 | Backlog | NOT | Decision on whether the email belongs on the document row, and it is cross-platform. Stuart's 09-29 comment asks for a live re-check before any change. |
| KS-1355 | Todo | NOT | Four spots across four files. Spot 1 alone (`stack_guard.sh` + `stack_guard.test.sh`) still needs a designed output format ("group by project and append an unknown count"). SCREEN.md's harness half of the reason is obsolete (see the runner note). The design half stands. |
| KS-1357 | Backlog | NOT | OAuth rotate-secret, whose body carries a client secret: a credential surface. The fix is a choice ("adding `id` … or a rotate-specific schema"). |
| KS-1377 | Backlog | NOT | The security `/api/keys/validate` route (the KS-1370 exclusion). N-1338-3 needs a real DB, and N-1338-4 is "a product decision". |
| KS-1379 | Backlog | NOT | Lockfile regeneration that is blocked on host npm (`edgesOut` crash). The added cells reach auth's JWT signing-key load, a credential surface. |
| KS-1380 | Todo | NOT | Refresh `@types` locks in 3 to 11 services: "Likely fix (Kamil's call)". Multi-file lockfiles, and only a docker build reproduces the failure. |
| KS-1381 | Todo | NOT | Many files (compose, m365, bootstrap, 20 `.env.example`, scripts). "Fix shape (Kamil's call)". Acceptance requires per-slot tests across all of them. |
| KS-1382 | Todo | NOT | Five `Blockchain/Testing` entry points of the security harness: "Kamil's call", multi-file. |
| KS-1383 | Backlog | NOT | Credential verify is not bound to the proof: a security surface. "The fix shape is deliberately blank". |
| KS-1384 | Backlog | NOT | Labelled Decision: "Decisions needed (Kamil)" on one-anchor-per-document vs per-event. |
| KS-1385 | Backlog | NOT | Three routes, the OpenAPI spec and a response echo. It is "subject to the per-document-anchor ruling" (KS-1384) and cross-platform. |
| KS-1387 | Backlog | NOT | Three services fail a docker build (TS2742 / TS2345). Only a docker image build reproduces it, which the checker has no runner for. Duplicate family of KS-1380. |
| KS-1388 | Backlog | NOT | Item 1 is a comment line in two `.env.example` files (`:6882` → `:80`): two files and no failable test. Item 2 is documented-as-decided, for when KS-984 lands. |
| KS-1389 | Backlog | NOT | "Asks for your view on one coordinated change" across `slot-target.sh`, `.githooks/pre-push` and `preflight.sh`. A decision, and it touches `.githooks`. |
| KS-1390 | Todo | NOT | Docs and a gate-table row. "Decision needed before fixing — naming the three Playwright estates". |
| KS-1391 | Todo | NOT | Item 1 is one line in `frontend/issuer/package.json` (`"test": "vitest run"`), but there is no red cell and `frontend/` is outside every checker tier (build_input refuses paths outside `services/*` and `packages/shared`). Items 2 to 4 are decisions. A trivial cloud-seat task, not a Spark one. |
| KS-1392 | Todo | NOT | `.github/workflows/ci.yml` (excluded), plus "scan before fixing". |
| KS-1393 | Todo | NOT | Three hygiene decisions: delete or move specs, a branch-retention rule, and a duplicated package. |

## For Wednesday

- **The one candidate, as a brief-writer would take it:**
  - **Product:** `Blockchain/Dev/services/referral/src/referral.openapi.ts`, `:480` (`content: { 'application/json': { schema: ReferralCodeSchema } },` inside the `GET /api/referrals/{code}` registration at `:469`-`:491`). It becomes an inline `z.object({ success: z.literal(true), data: z.object({ code, isActive, isExpired, customLabel, referredReward, referrerReward }) })`, in the KS-498 shape the same file uses for `/generate`'s 201.
  - **Test:** a NEW vitest spec cell reading the registered response, in the shape of KS-747's.
  - **Raise-seat companion:** the regenerated `docs/openapi/secuura-api.yaml` (`npm run generate-openapi`).
  - **Unmeasured, to settle while writing the brief:**
    - whether `customLabel` is nullable at runtime;
    - whether `check:openapi`'s example guard (KS-256, E1-E7) needs an `example` on the inline schema;
    - whether `ReferralCodeSchema` is still used by the list endpoint at `:531` (it is, so the component stays).
- **KS-1380 / KS-1387:** develop does not build three service images, per Peter's 09-29 comment re-checked at `8c810023f`. That blocks every live re-check named on KS-1015, KS-1390 and KS-1386. It is not local-model work, but it is the board's current bottleneck.

## NOT COVERED (what this frame did not read)

- **The 247 other Backlog/Todo tickets** (273 − 26): none of them was created or updated after 2026-09-29T00:00Z. They rest on SCREEN.md (09-29) and `candidates.md` as those left them. Nothing here re-reads them.
- **KS-982, KS-984, KS-985** (Peter) were excluded at the filter and not read.
- **In Progress, In Review and Blocked** states are outside this commission.
- **Open-PR census:** only PR heads #1351–#1353 were diffed. The 22 older live merge refs SCREEN.md listed were not re-read, and neither were any PRs opened after #1353. There is no GitHub API read, so merge state is not known.
- **The carve's premises** were read at develop `37205947d` in a scratch clone and NOT run: no referral suite, no `check:openapi`, no `generate-openapi`.
- **"Updated after"** includes metadata-only updates, such as relation links and label changes. KS-772, KS-953, KS-955 and KS-964 were in the delta with no new comment. The filter cannot tell a content change from a metadata touch.
