# Findings: what "Wednesday's words" PRs 2195 and 2159 need (2026-11-24)

Source: the Sonnet drafter commissioned 13:34 (commission.md beside this file). Its Write tool refused a report file, so Wednesday saved its returned text here. Key claims RE-VERIFIED by Wednesday at source (13:3x, by reading the named files): gate 319 verdict line 1; gate 301 verdict line 1 + G301-2159-1 at line 101; daily/2026-11-10.md line 115 (PR 2159 to a fix round); fleet/briefs_staged/2026-11-12_B145_addendum_2195.md exists.

## BLUF
1. Neither hold is a Kam card: decision_queue list all searched for 2159, 2195, KS-2111, KS-1988, KS-2075: 0 hits (control: 'secuura' 602 lines). "NO READY without Wednesday's words" is a standing line in Wednesday's OWN K briefs (K 90th brief line 17), carried forward after its reason ended.
2. **PR 2195** needs only a RELEASE: gate 319 (tier 1) GO WITH NOTES at head 3eed5f75fa28 = the live head. GO terms were drafted 2026-11-12 (B145 addendum); B 145th wrapped before the row; no withdrawal found.
3. **PR 2159** needs its 2026-11-10 ruling EXECUTED: gate 301 G301-2159-1 (MEDIUM) — inherited names (toString, hasOwnProperty) still mutate shared built-ins; the verdict said "Wednesday's call: a fix round on this branch, or a follow-up ticket"; Wednesday ruled fix round on 11-10; no fix seat ever ran (head unchanged since 11-10).
4. The "2159-only waiver" (OVL_IGNORE_PRS=2159, given to W 41st 11-20 for PR 2260) is spent (2260 merged). It was never a hold on 2159.
5. gh: both MERGEABLE, mergeStateStatus UNSTABLE (repo-wide red CI rollup per gate 319). No merge-tree on develop b69addc39652 was run (no fetch allowed).

## PR 2195 — recommended ruling (Wednesday's, under the board grant to 27 Nov)
> PR 2195 (KS-1988 + KS-2075), head 3eed5f75fa28cb9b27feeedbe38c4181525faaef, tier 1, gate 319 GO WITH NOTES: RELEASED to the K merge seat as a normal row; READY re-pinned to the head and to develop at READY time (merge-tree both orders, planted conflict at each hunk); the GO and the MERGED name the two behaviour changes: (1) the migrations readiness probe yields an empty host/port for a URL it does not match, so pg_isready falls back to the local default (G319-2195-1, Minor); (2) observability.sh's file-scope `|| true` lets every action proceed when the Redis password cannot be resolved, so start/up run with the platform down (G319-2195-3, Minor). The MERGED says "this merge deploys nothing" plus those two names, never a demo sentence. Filings for G319-2195-1/-2/-3 go to a board seat after the merge.
Re-gate: none if the head is unchanged at READY; a rebase measure is required (develop moved since the gate's pin c78c80bd5370).

## PR 2159 — recommended ruling (Wednesday's 2026-11-10 fix-round ruling, executed)
> PR 2159 (KS-2111), head 7b54e7cbb6f0082a32b496c1773aa2e43bfe3ea2: HELD until a FIX ROUND closes G301-2159-1. One build seat, one commit on top of the head, no force-push: (a) buildSettingsUpdate and flattenSettings safe for EVERY inherited name (own-property check or null-prototype updates), red-first cells for toString and hasOwnProperty; (b) correct the false comment ("can never reach an inherited property"); (c) the gateway PUT gets an own-key refusal for inherited names OR the body states it still stores them; (d) trim G301-2159-2's sentence; (e) rebase onto current develop (PR 2260 changed admin.ts after the gate) and re-run the whole api-gateway vitest suite. Then a tier-1 DELTA gate on Opus at the new head; then a K merge seat on its own GO.

## Not measured
Real merge-trees on develop b69addc39652; daily notes 11-13..11-19; Linear state of KS-1988, KS-2075, KS-2111; the gate NOT TESTED lists (real Postgres/Docker stack); whether any live settings record holds a prototype-named key.
