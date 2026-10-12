# Gate brief: Secuura Platform K PR #1521 (KS-1533 arm 1), OPUS tier 1, adversarial

Re-commissioned 2026-10-13 ~05:1x AEDT by the Wednesday seat after the first gate (launched ~17:49Z on 2026-10-12) died with the coordinator rotation and left no verdict.

## What you are gating
- PR #1521, ticket KS-1533 arm 1, author Seat V 5th (Secuura/Blockchain-V).
- Head `c02c0b5dcc22d3a59c7faa787b08a2871bfdafda` (Wednesday's `git ls-remote` at re-commission: equal). develop `425ad3e00ae40ddbce6ead62c127c610e2e67a16`. V reports base 250596098fa9 merged in, never rebased.
- 2 files in `services/security`, +312 -8 (V's figure; measure it).
- Claimed change: arm 1 of the mint fix plus a connectorId refusal on the key mint/rotate route, exempting both platform roles and the provisioner; closes Path 1 and Path 3 of KS-1533; no migration. ADMIN pinned as UNDECIDED policy (a Kam card is open on it: do not rule it); `platform_admin` 403 pinned as MEASURED (decideMint refuses it first).
- V's own numbers (NOT evidence for you; re-measure what matters): red-first 5 red / 10 green over real HTTP on the unfixed service, 16/16 after; 9 of 10 mutants killed on a green baseline (survivor said to be masked by decideMint refusing a scope-less connector); services/security 30 files / 327 tests; packages/shared 949; KS-764 call-site guard 15/15 with no new allowlist entry; pre-push hook 13/16 legs ran, 3 skipped, none failed.

## How to get the code (READ-ONLY on the project)
- The project checkout `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files` is READ-ONLY to you: no fetch, checkout, worktree, merge-tree --write-tree, stash, commit there.
- Make `git clone --shared` of it into YOUR scratchpad, then work only in that clone. Either fetch `refs/pull/1521/head` there with the project's `core.sshCommand` (read it with `git -C <checkout> config --get core.sshCommand`), or use V's bundle: `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-10-12_seatV-5th/bundles/ks1533a-c02c0b5d.bundle` (sha256 first 16 = `3e2f299b5c7aa0c3`, verified; requires 250596098fa9). Assert the head sha before anything else.
- Never push, never comment on GitHub or Linear, never touch Kintsugi, demo or any box. No real secrets in output.

## What to attack (tier 1: auth / key-minting surface)
1. Role x target x connectorId x rotate matrix over REAL HTTP (the service's actual router and middleware order, not the predicate alone), with the stored row read back after each call. Roles: ADMIN, platform_admin, org_admin, issuer_admin, plain user, the provisioner. Targets: own org, another org, org-less account. connectorId: absent, own, another org's, malformed. With and without rotate.
2. Smuggling shapes: connectorId via body vs query vs header, case/whitespace variants, arrays, nested objects, prototype keys, duplicated params.
3. Every writer of `svc_api_keys` and every caller of `revokePriorConnectorKeys`: is there a path that revokes another organisation's keys after this PR (Path 3)? Grep the writers, do not sample.
4. The proxy / api-gateway path to the same route: does the refusal hold when called through the gateway?
5. Races: concurrent mint + rotate on one connectorId.
6. register-connector end to end still works for the legitimate roles.
7. The masked mutant survivor: show whether it is truly masked or a real coverage gap.
8. Regressions: the full services/security suite and the KS-764 guard at the head; compare with develop.

## Output
- Write `0_Brain/reference/2026-10-13_gate-pr1521/verdict.md` (this folder; create nothing outside it and your scratchpad).
- Head under test, how you got it, every number with its instrument and a control. FOUND / TESTED / HOW, and what was NOT tested.
- VERDICT line: GO / GO WITH NOTE / NO GO, Majors and Minors, each with file:line, the reproducing shape, and the minimal fix.
- Do not rule the ADMIN policy question (it is Kam's card); report what each option would mean.
