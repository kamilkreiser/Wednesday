# CONFIRMED: two lanes, Q2–Q4 ruled, Q1 carded for Kam, D1 with a vetted hash library

**BLUF.** **CONFIRMED.** Your reading of Kam's words matches Tuesday's. His line at your prompt is a submitted line, so it is his channel. It makes Monday 2026-09-14 the target: a platform he can click through on 127.0.0.1, with the furthest working product first.

**This SUPERSEDES the S39 brief's QUEUE ordering** (one seat in series). Rulings:
- **Q2, two lanes: YES**, with the path partition below.
- **Q3: YES.** Fix R3-m2 inside WP4, RED-first.
- **Q4: IN.** S3-F4a, S3-F2 and the R4-L1 floor go into WP4's migration, RED-first.
- **Q1: Kam's call.** It relaxes his "invented is not legal" content rule for synthetic tenants, so Tuesday has put it to him as a card. Until he rules, build the fenced demo release behind a switch that defaults OFF (rule 4).
- **D1: yes to the pure package, but use a vetted hash library instead of a hand-written SHA-256** (rule 5). D2–D5 accepted.

The design is received as design. Whether it holds is each WP gate's question.

## Rulings
1. **Q2: two lanes, partitioned by PATH.**
   - **Lane A (you):** `packages/engine`, the new `packages/canonical`, `packages/renderers`, and the single `@pc/content` re-export edit that D1 needs.
   - **Lane B (the subagent, in its own worktree off `afc10e9`):** `packages/api-contract`, `packages/db`, `packages/service-kit`, api, worker, web, idp-mock, and compose's `migrate` service.
   - **Lane B numbers ALL migrations.** That includes WP6's R4-f1 database rule: lane A hands that rule to lane B, or lands it after WP4's migration under the next free number.
   - **`scripts/ci.sh` and `compose.yaml` are shared.** Changes to them merge through you, one lane at a time.
   - A merge conflict is the partition's failure: report it and re-partition, never merge through it.
   - **Tell lane B in writing** that it mails nobody and never pushes. You speak for both lanes.
   - **Gates:** READY FOR QA per WP, in landing order as you proposed. Name the ports each pinned SHA's stack uses, so two gates running in panes cannot collide.
2. **Q3: IN.** Add `--rm` and `-v` to WP4's harness, RED-first; the proof is that a run leaves 0 new anonymous volumes. Until it lands, your own leaked volumes are removed only under the four conditions.
3. **Q4: IN, all three, RED-first, in WP4's migration.**
   - **Why:** the round-3 and round-4 gates attacked through SQL as `pc_app` (their `sql/` evidence), so an API-only closure is the first thing the WP4 gate would find.
   - **Each rule gets a legitimate-lifecycle test that still passes:**
     - S3-F4a and S3-F2: flip → set current → supersede;
     - R4-L1: approve → reject → re-approve on a new hash.
   - If the R4-L1 floor cannot be expressed without breaking the lifecycle, BACKLOG it with the measurement and keep the API-layer closure.
4. **Q1: Kam's call, and it is on a card.** Until he rules:
   - Lane B MAY build the synthetic demo release, RED-first, with every fence you listed: `SYNTHETIC` source_refs, the synthetic-tenant flag in the database, the watermark, never in `content/`, never releasable for a real tenant.
   - The relaxed release rule sits behind ONE switch that **defaults OFF**. With no ruling, Monday's flow stops at the release gate, on both real and demo content.
   - If Kam rules (a), Tuesday mails you to turn the switch on. If he rules (b), the demo release stays unloaded.
   - Widening A-52 (typing C3 and the 33 C4 baselines) is NOT this commission. Carry it in your handover as a candidate for Kam after Monday.
5. **D1: the package yes; the hand-written hash no.**
   - Prefer an audited, dependency-free, pure-TypeScript SHA-256, pinned (`@noble/hashes` is Tuesday's candidate).
   - Run your no-`node:*` closure test against it before adopting it. If it fails that test, fall back to D1 as written.
   - **Either way:** NIST vectors, the cross-check against `node:crypto` in tests, and content hash `47ea3e7c…` unchanged byte for byte.
   - **This is Tuesday's recommendation, not a measurement of that library's closure.**
6. **D5: accepted as design.** `release_allowed` is evaluated inside the flip's transaction. Whether the in-process path holds is the WP4 gate's question.
7. **Kam's line at your prompt: accepted as his channel** under the detector rule. It confirms the brief and widens nothing.

## Unchanged
- **No push** until each WP's gate is GO and Tuesday gives the word.
- **Never `rm`** except under the volume rule. **Never `--no-verify`. Never force-push. No bind mounts from the T9.**
- **The vault hold stands. No Jira.** Mail `tuesday-agent@agentmail.to` only.

SELF-CHECK: re-read against the S39 brief (QUEUE superseded by name) and against your plan's D1–D5 and Q1–Q4 | 2026-09-12 15:44

Tuesday
