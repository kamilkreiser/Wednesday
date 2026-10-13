# Gate brief: Secuura Platform K pull request 1546 (ticket KS-1032, originate's gateway-vouch trust), OPUS tier 1 (an authentication/tenant boundary)

Commissioned by the Wednesday seat. All 0_Brain paths are relative to /Volumes/DevMASTER/WEDNESDAY/; project paths under /Volumes/DevMASTER/!CODING/Secuura/Blockchain/.

## Kam's ruling this implements (verbatim, card secuura-ks1032-fail-closed-when-vouch-secret-unset-1013, ruled a at 2026-10-13 18:54 AEDT)
Card title: "KS-1032: originate trusts forged identity headers when no gateway secret is set; should a box with no secret refuse them?"
Option (a), chosen: "Fail closed, deployed only after the secret is set" — "Seat J builds the refusal. The deploy seat sets GATEWAY_VOUCH_SECRET on Kintsugi and demo and checks Platform S metering end to end BEFORE this change deploys; Wednesday records that ordering as a deploy blocker."
Gate the code against THAT: an unset secret must REFUSE forged identity headers; nothing about deploy timing is the code's job, but the PR body must state the deploy condition honestly.

## What you are gating
- Head ad366066e620037d753f9421bcd051ad09a9a7af (Wednesday's own ls-remote of refs/pull/1546/head = the author's). Author says: ONE commit directly on 405e33a1061310662b10245c5154c3d75c49f0f4, tree b371f9483256d83e07e73ad630a7de242b5149b3, six files, +464/-43, parts (a)+(b)+(c) of the ticket's originate slice.
- develop has MOVED: Wednesday's ls-remote reads 026c2d1614065c79fc8d96007ac0d80f19fb9363 (pull request 1542, KS-1119, which changes routes/verification.ts and one ks1119 integration cell per its author). Measure the file overlap between 1546 and develop's moved commits since 405e33a1, with a planted control that proves the scan can register a hit, and run git merge-tree --write-tree of the live develop tip and the head (report rc and tree, with a conflicting negative control). Gate head ad366066 only.
- Author's own points to weigh (from its READY mail, NOT evidence):
  1. Red-first 6 red / 6 green of 12, both controls green. A straight revert is a compile break (the cells import a new module), so the red variant restores develop's BEHAVIOUR with the plumbing present. Check the variant is not too kind: does it really reproduce develop's trust of forged headers?
  2. Mutants 7/7; A1-A3 CANNOT catch a verdict-reader mutant because the strip removes the headers first on an unconfigured request. Decide whether the verdict read is under-pinned and, if so, build the cell that pins it.
  3. Part (c) is a second line (the KS-458 resolution moved to utils/requestTenant.ts) whose effect is invisible while the strip works. Judge whether it is tested as real behaviour or decoration.
  4. Two PRE-EXISTING KS-1041 cells are INVERTED (were "unconfigured - fail-open, but LOUD"). Check the inversion is honest: the ruling covers it, and nothing else that relied on fail-open was silently flipped.
  5. Linear attachment flipped closes -> contributes (do NOT write to Linear; read only if you can).
  6. Deploy condition in the body: GATEWAY_VOUCH_SECRET must be set before the change ships, or Platform-S metering answers 401 and multi-tenant loses its tenant; single-tenant falls back to the migration-039 tenant. Check what the code actually does on each branch.
- Author's NOT RUN: Schemathesis, Akto, Playwright, k6; preflight legs 3, 4, 8 (local stack not up). In-hook push PUSH_RC=0, leg 14 88/88, KS-1086 post-push quarantine re-read clean.
- Author's evidence: the PR body (https://github.com/Secuura/Distributed_Secuura/pull/1546) and 5_Project_History/2026-10-13_seatJ-8th/evidence/ks1032/. Read, trust none.

## How to get the code (READ-ONLY on the project)
git clone --shared of 2_Project_Files into YOUR scratchpad, push URLs disabled; fetch refs/pull/1546/head and develop with the project's core.sshCommand; assert the shas. No git write verb in the project folder; no push; no GitHub or Linear write; no remote box; no Docker. Never write inside !CODING. Do not touch Postgres ports 55413, 55414, 55418, 55419, 55436 (other lanes); use your own port if you need Postgres.
TOOLING RULE: never run a command that deletes files and never put rm inside bash -c or sh -c; use fresh directory names or mv into a _quarantine folder in your scratchpad. Never cd; absolute paths only.

## What to attack
1. Re-run the author's cells on the head AND on develop (red/green), with controls each harness can fail; the originate unit + integration suites touched by the six files; tsc.
2. THE BOUNDARY: every way an identity or tenant header can reach originate's four reads: secret unset, set, set-but-wrong, empty string, whitespace, header case variants, duplicate headers, a header present with no vouch, a vouch for a different request (replay), a vouch computed over a subset of headers. Every request path that reads req.user / tenant (enumerate them; do not sample) must refuse forged headers when the secret is unset. Look hard for a path that still trusts a header (false pass) and for a legitimate gateway-vouched call that is now refused (false refusal).
3. Platform S metering: what exactly answers 401 when the secret is unset, and is the body's statement precise?
4. Mutants: re-derive the author's 7, add at least FIVE of your own (e.g. the unset-secret branch made fail-open again; the verdict read inverted; the strip removed; the vouch compared with == instead of a constant-time compare; the tenant fallback changed). Report by cell name; include a comment-only control.
5. Scope and hygiene: diff --stat vs develop; only the six declared files; the PR body vs the code; no closing keyword in the body.
6. Say plainly what you could not test and whether any of it could hide a Major.

## Output
0_Brain/reference/2026-10-13_gate-pr1546/verdict.md (this folder only, plus your scratchpad; raw outputs under evidence/, never a directory named out). Head under test; every number with its instrument and a control; FOUND / TESTED / HOW; NOT tested; severities with file:line, the reproducing shape and the minimal fix. VERDICT (GO / GO WITH NOTE / NO GO) and sha256/16 of the report on LINE 2 (recipe: delete that one line, sha256 of the rest, first 16 hex). Do not recommend deploying: this change deploys only after the secret is set (DEPLOY-BLOCKERS). Merge only on Wednesday's head-bound GO.
