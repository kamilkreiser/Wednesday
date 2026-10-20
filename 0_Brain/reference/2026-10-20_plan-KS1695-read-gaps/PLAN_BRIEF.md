# Plan brief: KS-1695 (two same-tenant read gaps in services/originate) — a DESIGN PLAN, no code, no pushes

Commissioned by Wednesday. Row C3 (auth read-path design) of `2_Project_Files/fleet/specs/model-routing.md`. Output: `PLAN.md` in this folder (only file you write). Nothing under `!CODING`, no GitHub or Linear writes, no `cd`, no `rm`, no stderr to /dev/null.

## Read first (all local)
1. `KS-1695.md` in this folder (the ticket as read live from Linear 12:5x AEDT, description + comments; comments were fetched first:50, check the count line).
2. Gate BX1 verdict: `/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-10-20_gate-BX1-pr1659-ks1659-tier1/verdict.md` (the measured audience table: who got 200 and who got 404; N1, N2, N4; the Q4 remedy table).
3. The precedent: Kam's KS-1116 ruling (`secuura-ks1116-null-owner-who-reads-1020`, answer a: tenant administrators, ORG_ADMIN / SYSTEM_ADMIN with a tenant on the token, read owner-less rows). Find its seat plan under `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/` (C 30th, 2026-10-19/20) and read how the ruling was framed.
4. Source, read-only, at live develop `7e3b9362e08b1b5b2c418f43e05c9bd0616f896e`: use `git --git-dir` reads on `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/cache/src` (`git -C … show <sha>:<path>`; do not check out or fetch into it). Files: `services/originate/src/routes/certifications.ts` (GET /:id ~956-1010), `routes/documents.ts` (~1124 cloak), `repositories/documentRepo.ts` (~176, ~373-375, ~501), `principalId.ts`.

## What the plan must contain
- **Audience table, copied from the gate's measured rows** (who is served 200 / 404 today for each route and row type), never paraphrased into a familiar unit. The ledger records Wednesday narrowing this exact audience once already today.
- **Remedy options** for each gap (certifications GET ownership check; documents cloak failing closed on an empty owner): what each blocks, who loses access, what legitimately breaks (read every caller: Platform S connector, human UI, gateway, vc-issuer; cite file:line), and the migration/backfill need for existing owner-less rows (counts on demo/kintsugi are UNMEASURED unless you can read them from an existing report; say so, do not guess).
- **Recommendation** with the single smallest PR that closes the gap plus what follows; whether KS-1116's ruling (tenant admins read owner-less rows) extends to these routes or needs its own decision.
- **A card draft for Kam**: plain English, no code names in the options, each option's consequence for a person ("a normal user in another organisation can no longer open this certification"), a recommendation and the default if he does not answer. Wednesday posts it; you do not.
- **What you could not establish**, stated as unmeasured.

Every claim about code carries `sha:path:line` read in the same action; every zero has a positive control; if you cannot open a line, write "I believe X; I have not read it".
