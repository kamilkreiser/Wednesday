# Gate brief: GATE P1 = #1568 ROUND 4 (KS-1612 + KS-1385 (b)), TIER 1, full Opus, the LAST round

Commissioned by the Wednesday seat, 2026-10-19 ~12:4x AEDT. Routing v1.0 row G1 (tier 1: a cross-tenant guard and a data-integrity migration). **This is the LAST round:** Kam ruled card `secuura-ks1612-round3-nogo-1019` = a ("Allow a fourth round, narrowly"). If this is NO GO, nothing more is built on #1568, and the outcome goes to Kam.
0_Brain paths are relative to /Volumes/DevMASTER/WEDNESDAY/. Project paths are under /Volumes/DevMASTER/!CODING/Secuura/Blockchain/.

| what | value (Wednesday `ls-remote` ~12:4x; re-read it yourself) |
|---|---|
| #1568 head now | d2564aeb587bcbd7d9628495e83913c710ca0043 (one commit on round 3's 09588895db75) |
| develop | 37834600a543cb0276f427d969ac034d9df74fbd (eleven merges since round 3's gate) |
| round-3 verdict (gate L1) | 0_Brain/reference/2026-10-19_gate-L1-pr1568-r3/ (NO GO: MAJ-A closed; MAJ-B = 051 refused certification issue/revoke and its census refused to apply; MIN-A = an invented Prisma fixture) |
| J 13th's design (ruled as written by Wednesday) and READY, Secuura content only | this folder: J13_round4_design_mail.md, J13_round4_READY_mail.md |

**Author's claims (NOT evidence):** exactly 4 files (051, `utils/idNamespaceCollision.ts`, its unit test, a NEW integration test), +512/-104; the pk arm and census arm B are dropped; the helper walks the error's properties to depth 4, with a cycle guard and exact message equality; originate 1395/1395; integration 17/17 on node-pg and (in J's prototype on the same tree) 17/17 on real Prisma 7.8.0; 15/15 mutants killed; Q1 inverted control (round 3 with only its pk arm: 201 x4).

## Gate
1. **Scope:** diff d2564aeb587b against 09588895db75: exactly the 4 files, nothing else. `routes/documents.ts` and `certifications.ts` untouched.
2. **MAJ-A stays closed WITHOUT the pk arm.** Re-run gate L1's own M1-M4 e2e on round 4, **with anchoring BOOTED** (the author did not: J's M1/M2 rows come from a stub; the full re-anchor chain through the real guard was not run). Every orphan minter refused (409, 0 rows, the anchor row unchanged), including originate's `/api/anchoring` alias (`originate/src/index.ts:278-279`). Then **hunt for an unnamed writer** that sets `external_id` or `documents.id` from caller input, by symbol across originate and anchoring (not by the author's list).
3. **MAJ-B closed:** certification issue (201) and revoke (200) through the real routes on a real PG, as `secuura_app`, both drivers. Also drive recertify and the expiry write (the author says they share revoke's upsert, unmeasured).
4. **The census applies** on a seeded box holding real issued certifications (seed through the real routes), and refuses on a planted claim.
5. **MIN-A closed against REAL Prisma 7.8.0 + adapter-pg** (L1's prisma_rig method; J's copy is in its scratchpad, j13/r4/tools/rig.sh + mkdeps.sh). Then attack the helper's walk: deeper nesting, a getter that throws, a code on a non-enumerable property, a message that differs by one character, and a 23505 from a DIFFERENT constraint (must NOT map to 051's 409).
6. **The 051 header** now says that round 3's note about the round-2 record was wrong. Check that against the code (the alias), and that nothing else in the header is untrue.
7. Suites on YOUR predicted landing tree (onto live develop 37834600a543), with `packages/shared` rebuilt: originate (the author's 1395 is on an older base, so predict from a base measured at the landing parent), tsc, and both drivers' integration runs. One mutant per product hunk.
8. Merge prediction of d2564aeb587b onto develop 37834600a543 (tree id). Note any file the eleven merged PRs touched.

## Rules
- Read-only on the project. **Your OWN scratch folder is /private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/2ce15c23-3025-4dcd-9e03-2be96a0a6754/scratchpad/p1/. Use nothing else in that scratchpad.** Clone there with `git clone --shared` from /Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files, set origin to git@github.com:Secuura/Distributed_Secuura.git in YOUR clone, and fetch with that checkout's `core.sshCommand` plus `-o ServerAliveInterval=30`. Use your own scratch Postgres on your own ports. Never touch J's ports (55493-55495), and never touch any server or box.
- No git write verb in !CODING, no push, no GitHub or Linear writes, no Docker against shared state. No cd. Never send stderr to /dev/null. Loops go in script FILES run with /bin/bash. Every zero needs a control that fired. A test that cannot fail is a finding.

## Output
- Write 0_Brain/reference/2026-10-19_gate-P1-pr1568-r4/verdict.md.
- Line 1: `VERDICT: GO / GO WITH NOTE / NO GO at head <full sha> (round 4 of 4, the last)`.
- Line 2: one sentence: "MAJ-A closed without the pk arm, anchoring booted: YES / NO / UNMEASURED because <x>".
- Line 3: `sha256/16: <16 hex>` of the report with line 3 deleted.
- Then FOUND / TESTED / HOW per item, NOT tested, and severities with file:line. Final lines: `MODEL:` and `WALL-CLOCK:`.
