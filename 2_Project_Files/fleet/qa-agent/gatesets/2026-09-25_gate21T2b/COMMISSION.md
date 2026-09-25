# COMMISSION — DRAFT the round-21 SECOND tier-2 batch QA gate kit over #1225 #1227 #1229 #1231 #1232 — do NOT launch

Relayed by Wednesday to the drafter on 2026-09-25 (~15:2x AEST). Recorded here as the gate's commission; the QA agent reads it. Shape copied from the
running sibling tier-2 kit of the same round (`gatesets/2026-09-25_gate21T2`: template + pins + fill, self-locating launcher, repin-and-launch,
controls, derive_repin), with the QA brief template's §2a (LEGITIMATE SHAPES for checkers) and §7 (build the schema the product deploys) applied.

## The batch — TIER 2, ONE gate, FIVE PRs (FROZEN at five)
Heads as read by Wednesday with `git ls-remote origin` between 14:5x and 15:1x AEST 2026-09-25 (the drafter re-read every one: identical —
lsremote_1.out 05:18:55Z, predict_1.out 05:24:54Z, fill_2.out 05:40:59Z, repin_dryrun_1.out 05:42:25Z):
- #1225 KS-1291, head 120420a2e7b1a0d10dd41ee4320f7e88bc1529c6 (Seat L1; originate — a dead route guard removed (the #1174 guard); a route surface, so
  legs 3/4/8 are OWED)
- #1227 KS-1252 + KS-1253, head 69a72726e8eee0711a56b782d04936bf647e9160 (Seat L4; scripts contract.mjs; KS-1253 is a NARROWING: candidate B exact
  deny-prefixes closes 14, 0 collateral, `Refs KS-1253`, the ticket stays open — Wednesday ruled it; its READY says 58/58 suites and spec findings
  identical base/head)
- #1229 KS-865 + KS-808 (3), head ed85bd81d0acb137c89e1257d05ef9c72855086b (Seat L4; scripts; KS-865 i+ii+iii with a dropped stale entry named as a
  loosening, net stricter; KS-808 (3) option b = the script's citation only, BACKLOG.md NOT touched)
- #1231 KS-1281, head bd1d2daec2bf1b934437eae19c6239fe257305a6 (Seat B 25th; an Ornith local-model fix held as PASS 7/7; vc-issuer credentialRepo
  runtime CREATE TABLE -> an existence check, the ticket's SECOND offered shape; seat's stated limit: whether the least-privilege role can SELECT the
  table on every environment is NOT measured)
- #1232 KS-1128, head ec0d7efcf682112639505cf45baec71b899b665f (Seat B 25th; an Ornith fix; api-gateway startup-migrations platform seed catch -> WARN;
  proven with an in-process fake pg, no real PostgreSQL; seat ran three text-pinned cross-package readers, none moved)
- CURRENT develop at origin: ecb1aa75aefae35a8e2d8694f303adac7c17ab55 (moved today by four merges from 6ab9d5021e96ea1481cb6c6ff2d6d33b414aecb7).
  Merge-base and behind count per PR measured via the GitHub compare API; the merge checks are BASE-INVARIANT (the PR's diff vs current develop ==
  the PR's own paths); pairwise path-disjointness across the five and against develop's four new commits measured.
- NOT in this gate: #1230 KS-1131 (tier 1; rides in Seat B 25th's same READY mail).

## Gate rules the prompt must carry (Wednesday's, in substance)
1. Tier 2 = through-code: diff review of each PR against its ticket's claim, AND each PR's red-proof really bites (named red cell RED at base / GREEN at
   head in the tester's own worktree/scratch clone). Per-PR GO / NO GO / GO WITH FINDINGS, findings-only. Round 1 of 2 under the two-NO-GO cap.
2. Worktrees from refs/pull/<n>/head shas; never write to the shared checkout; no fetch into it.
3. Legs 3/4/8: OWED for #1225 (route surface) — if no stack is up, record OWED, never green; NOT run (no surface) for the other four, stated.
4. #1231: state the least-privilege SELECT as UNMEASURED unless the gate can measure it; check the existence-check against a DB NOT built by migration
   001 (fallback to memory) as the seat describes.
5. #1232: fake-pg only — state it; verify the WARN text and that the `:1142` inner catch was untouched (same class, out of scope).
6. #1227: verify the narrowing is exactly as ruled (14 closed, 0 collateral; the two L3 rows `len12`/`credit` in `ks256-spec-example-contract.test.ts`
   stay green).
7. Load false-red: `Test timed out in 5000ms` in packages/shared repo-walk guards under load = KS-1155's known class; re-run once; an assertion failure
   is real.
8. Orphaned `login_stub.mjs`: reap only the gate's own (cwd + ppid, never by name, never pid 1); report before/after counts.
9. HOLDS: no merge, no push, no ticket state change, no PR or ticket comment, no deploy.
10. GO string verbatim: `GO: merge #1225, #1227, #1229, #1231, #1232 batch`. Routing name `QA/Secuura-batch1225`; PROPOSED routing line
    `QA/Secuura-batch1225|coagent@agentmail.to|yes` — NOT written into inbox_routing.conf by the drafter.

## Deliver (do NOT launch, send, tap, commit or push)
The prompt, the launcher (generated the precedent's way, `bash -n` clean), the gate set contents per the precedent, the controls run both ways, a
`--dry-run` of the repin script, and a PROPOSED inbox_routing line.
