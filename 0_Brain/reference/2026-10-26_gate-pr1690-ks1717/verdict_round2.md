# QA GATE — TIER 1, round 2 of 2: GO WITH NOTES — PR #1690 at b6dcc14c3fdf

- Repo: Secuura/Distributed_Secuura, PR #1690 (KS-1717), branch `feature/ks-1717-signed-emitter-hop`.
- PRIOR ROUND: round 1 gated `dfc89078979b`, verdict GO WITH NOTES. Its report is at `/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-10-26_gate-pr1690-ks1717/verdict.md`.
- **Head ASSERTED** `b6dcc14c3fdf9cd71dfc366d9b1355a7abbba465` at `refs/pull/1690/head`, matching the brief. Three readings, each with its branch:
  - 02:38:23Z, start: pr/1690 = branch `feature/ks-1717-signed-emitter-hop` = b6dcc14c3; develop c2505d5c6.
  - ~02:46Z, mid: worktree `r2/head` HEAD b6dcc14c3, detached in my clone.
  - 02:52:41Z, end: `ls-remote` pr/1690 = branch = b6dcc14c3; develop c2505d5c6.
  - The head did not move during the gate.
- Shape: b6dcc14c3 is one commit on top of dfc890789, touching 9 files (+220/-57). The PR against develop is still 14 files.
- Scratch: `/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/eaab5e79-9f7f-4dbd-b3bc-d0dc2aca4d65/scratchpad/gate1690/r2/`. In it:
  - `repo/` is my own clone, shared from round 1's and fetched from origin.
  - `head/` is the worktree at b6dcc14c3.
  - `out/` holds the logs, my planted cells (`preamble.ts` + `cells.ts`, assembled as `gate1690r2-planted.test.ts`), `redproof2.sh` and `suites.sh`.
- Findings only. Nothing was fixed, pushed, commented on or merged. The project checkout got read verbs only (`config --get`).
- This is a CHECKER, so legitimate shapes were measured alongside the defect shapes: same-bearer hop (G1, G2c, R2), padded same bearer (E4), duplicate header keeping the signer's bearer (E5), and the 32-char control R11.

## Checks

| # | Check (FAIL condition stated first) | FOUND | TESTED | HOW |
|---|---|---|---|---|
| 1 | **Minor 2, the bearer binding.** FAIL if a hop captured under connector A verifies under any other bearer; if the same-bearer hop no longer verifies; if either setter signs a value other than the one it sends; if `authorization` can be omitted; or if any other path builds the hop. | **CLOSED.** Signing string at head: `secuura-emitter-v1 \n method \n path \n timestamp \n marker \n sha256(authorization ?? "") \n sha256(body)` (`emitterSignature.ts:101-112`). The verifier reads `headers.authorization`, and a non-string counts as absent (`:189`). `signEmitterHop` declares `authorization: string \| undefined` with no `?`: a call that omits it fails tsc with **TS2345 "Property 'authorization' is missing"**, while explicit `undefined` compiles (`out/probe/tsc.log`). **Setters:** create (`documents.ts:976`) passes `anchoringAuth \|\| undefined`, and the header is `...(anchoringAuth ? {Authorization: anchoringAuth} : {})` (`:877`). Lifecycle (`:1410`) passes `authHeader \|\| undefined`, with the same conditional header (`:1394`). Each passes exactly what it puts on the wire. **No other path:** `signEmitterHop` / `emitterSigningString` are called only at those two lines outside tests (git grep -i over `Blockchain/Dev` at head). **My round-1 replay cell G2, inverted** (A's hop sent under another org's connector B) is now **REFUSED**, and the row is recorded for B. Same-tenant B (G2b): refused, row recorded for B. Same bearer: still skipped (G1 twice, G2c, R2). **Edges:** <br>• missing Authorization → **401** (E1). <br>• empty Authorization → **401** (E2). <br>• `bearer <tok>` (lowercase) → **401** (E3). <br>• a hop signed for `BEARER <tok>` and sent as `Bearer <tok>` → refused, row recorded (E3b). <br>• leading/trailing spaces on the wire → **verifies**: Node trims OWS before both the authenticator and the verifier see the value, so it is the same bearer (E4, legitimate). <br>• `Bearer  <tok>` (two spaces) → **401** (E4b). <br>• `Bearer <tok> junk` → authenticates as `<tok>` but is refused, row recorded (E4c). <br>• two Authorization headers `[A, B]`, signed for A → Node keeps the first, so the authenticator and the verifier both read A: skipped, attributed to A (E5). <br>• `[B, A]`, signed for A → refused, row recorded for B (E5b). <br>• a hop signed for the bare token without `Bearer ` → refused (E6). <br>• a round-1-format MAC (no bearer hash) → refused (E7). | Yes, MEASURED AT RUNTIME | 26 planted cells (`out/gate1690r2-planted.test.ts`) run through the real anchoring `index.ts` app on an ephemeral port with real RS256 bearers (the builder's harness), next to the builder's 11. **37/37 green at head** (`out/planted.log`, `rp-baseline.json`). **Red-proof:** <br>• **X**, the same 26 cells at the round-1 head dfc890789: **G2, G2b, E3b, E4c, E5b, E6, E7 red** (7). The cells are therefore not vacuous, and the binding is what changed. <br>• **MA**, `authHash` dropped from the join in the shared `dist` anchoring loads: those 7 plus the builder's **R9** red. <br>• Restored by `cmp`: 37/37. <br>• originate **MO1** (create passes `authorization: undefined`) → **O1 red**. <br>• originate **MO2** (lifecycle passes `authorization: undefined`) → **O2 red**. <br>• Restored by `cmp`: 5/5. |
| 2 | **Note 4, the floor in anchoring's own cells.** FAIL if removing the 32-char floor leaves all of the builder's anchoring cells green. | **CLOSED.** R10 (31 chars refused, a hand-MAC under that same key) and R11 (exactly 32 honoured) are present. **M4** (`secret.length >= EMITTER_SECRET_MIN_LENGTH` → `secret.length > 0` in the shared `dist`) turns **R10 red**, along with my G12. R11 stays green, as a control should. | Yes, MEASURED AT RUNTIME | `out/redproof2.sh` / `out/redproof2.log`, `rp-M4-no-length-floor.json`: 35/37, with R10 and G12 the only reds. |
| 3 | **The residual wording.** FAIL if a place states a window or a scope that differs from the measurement. | **Measured** (G10, bearer bound): signed at T.000 → T+60.999 accepted, T+61.000 refused. A signer 60 s fast (verifier at T-60.000) is accepted; at T-61.000 it is refused. So the window is just under 61 s when the clocks agree and up to about 121 s with a fast signer. Scope is the same bearer only (item 1). **Exact:** <br>• helper header, `emitterSignature.ts:37-51` ("just under 61 s … up to about 121 s … under the SAME bearer"). <br>• anchoring comment, `index.ts:538-552` ("under the SAME bearer verifies for just under 61 s (up to ~121 s with a fast signer clock …)"). <br>• `docs/ENVIRONMENT-VARIABLES.md:138-146`. <br>**Not updated:** both env templates (`.env.example:348-352`, `env.example:483-489`) now name "the caller's Authorization header" but still say only "a timestamp within 60 s", and carry **no residual statement at all**: no same-bearer scope, no 61 s, no 121 s (finding N1). **PR body: the live GitHub body was NOT read** (no `gh` credential: the project's `4_Credentials/.gh-config` and the global config are both logged out). **The builder's local copy WAS read**: `!CODING/Secuura/Blockchain/5_Project_History/2026-10-26_seatJ-ks1717/PR_BODY_FINAL.md` (mtime 13:18), ll.24-28: "a byte-identical replay under the **same bearer** … **just under 61 s** … up to **about 121 s**". That matches the measurement. Its head line (l.3) is garbled: it calls b6dcc14c3 "commit 708be64ccafd, a merge of develop". In fact b6dcc14c3 sits on merge dfc890789 (= 708be64cc + develop 28dac5c12). Cosmetic (N4). | READ ONLY (wording) + MEASURED (window) | `git grep -i` for "byte-identical", "within 60", "61 s", "121", "same bearer" over the 9 touched non-test files. G10. |
| 4 | **Regression.** FAIL if any red other than the two known reds appears, if the counts differ from the builder's, if tsc fails, or if any round-1 cell regresses. | **anchoring 390/391**: the one red is `threadTokenMint` "parameterises mint + spend with a deterministic per-seed policyId". **originate 1655/1655**, 140/140 suites. **shared 1030/1031**: the one red is `wallet-signature` "accepts a valid wallet signature over the message" (KS-1727). These match the builder exactly, and both reds are the known ones. **tsc `--noEmit`** rc 0 on shared, anchoring and originate. **Every round-1 cell** G1, G3–G12, ported to the bearer-bound API (the signer now binds the bearer it sends), is green. G2 is deliberately inverted, and the inversion is the fix. | Yes, MEASURED AT RUNTIME | `out/run1.sh` ran `npm ci --ignore-scripts` (1806 packages), the shared build and tsc. `out/suites.sh` ran `npm test` per package, with my planted file moved out so the counts are the PR's own (`out/suite-*.log`). Load stayed under 7 at every start (logged in each log). The worktree was clean afterwards. |
| 5 | **Merge onto the moved develop.** FAIL on a conflict or a file overlap with #1691. | `git merge-tree --write-tree origin/develop(c2505d5c6) pr/1690(b6dcc14c3)` → tree `b21cadde4935`, **rc 0, no conflicts**. The merged tree differs from develop in exactly the PR's 14 files, and from the PR head in exactly #1691's 5 vc-issuer files. Files changed by 28dac5c12..c2505d5c6 ∩ files changed by 28dac5c12..pr/1690 = **0**. The merge-base is 28dac5c12. | Yes, MEASURED (in my clone) | `merge-tree` in `r2/repo`, never in the project's checkout. |

## Findings

**N1 — Note: the two env templates do not carry the residual statement (READ ONLY).**
- Where: `Blockchain/Dev/.env.example:348-352` and `Blockchain/Dev/env.example:483-489`.
- What they say: "a timestamp within 60 s" and "the caller's Authorization header".
- What they leave out: the "same bearer only; just under 61 s; up to ~121 s with a fast signer" sentence. The docs, the helper header and anchoring's comment all have it.
- Why it matters: little. The window and scope are stated exactly in the docs page these templates sit beside, so nothing is misstated about the binding. The templates are simply less precise than the brief expected.
- Fix-shape: one comment line in each template, mirroring `ENVIRONMENT-VARIABLES.md:142-145`.

**N2 — Note: an absent and an empty Authorization hash the same, so the helper's "including none" wording is relative (MEASURED AT RUNTIME, E2b + E1 + E2 + E5).**
- What I measured: `sha256(authorization ?? "")` makes a hop signed with no bearer verify under `authorization: ""`. An array-valued authorization also counts as absent at the verifier (E2b).
- Not reachable: `authenticate()` answers 401 to both an absent and an empty header before the row decision (E1, E2). Node also collapses a duplicated Authorization header to its first value, so an array never arrives over HTTP (E5, E5b).
- No widening. Optional wording only: "a hop signed with a bearer is refused under any other value, including none".

**N3 — Note: the shared unit cell S7d says "extra whitespace is a different bearer", which holds for the function but not on the wire (MEASURED, E4).**
- What happens: Node strips leading/trailing OWS from the header before anchoring sees it, so `Bearer <tok>   ` on the wire verifies as the same bearer.
- This is the same token, so it is legitimate and not a widening.
- Internal whitespace answers 401 (E4b). A suffix is refused with its row recorded (E4c).
- Separately, E4c shows the shared authenticator accepts `Bearer <tok> junk` as `<tok>` (`authHeader.split(' ')[1]`, `packages/shared/src/middleware/index.ts:117`). That predates this PR and sits outside the diff. The signature fails safe on it, recording the row.
- Fix-shape for S7d (optional): name it a unit-level property, or add an app-level cell like E4.

**N4 — Note: the builder's PR-body draft misdescribes the commit shape on its head line (READ ONLY).** `PR_BODY_FINAL.md:3`: "`b6dcc14c3…`. That is commit `708be64ccafd`, a merge of develop…". The actual chain is b6dcc14c3 → merge dfc890789 → (708be64cc, develop 28dac5c12). The residual wording in the same file is exact. Fix-shape: reword l.3.

**Carried from round 1, not in this round's scope:**
- **Minor 1** (no deploy path passes `emitterSigningSecret`): unchanged at head. Neither `deploy.sh` nor `deploy-demo.yml` is in the round-2 delta. Wednesday's daily note says the builder filed **KS-1730**. I read that from `0_Brain/daily/2026-10-26.md:97` and did not check it on Linear.
- **Notes 5 and 6** (raw-body retention; no end-to-end run): unchanged and still apply.
- **Note 3** (window wording): closed in the docs, the helper and the anchoring comment; see N1 for the templates.
- **Note 7**: the two known reds reproduced again.

## Instrument errors (mine)

- **Seat hooks refused three Bash calls:**
  - `git -C $VAR fetch` / `merge-tree`: the write-verb hook cannot see a variable path. I re-ran them with literal scratch paths.
  - A `======` separator: zsh expands `=word`. I re-ran with `----`.
  - Nothing reached the project checkout.
- **Round-1 cells re-signed:** they had to be re-signed for the new API. Under the round-1 `hop()` (no bearer), every marked cell would go red at the head, and that red would measure my harness, not the change. The ported cells sign the bearer they send.
  - The cross-head run X is the proof that the port did not make them vacuous: 7 cells red at the round-1 head, green at the new head.
- **E3b's title is badly worded** (it is a scheme-case mismatch between signer and sender). Its assertion is what counts: refused, row recorded.
- **M4 and MA mutate the compiled shared `dist`**, not `src`. They prove what the running anchoring app depends on, and say nothing about the shared unit cells.
- **Mutant MO1/MO2 proves the cells, not the reading of the code.** The claim that originate passes exactly what it sends rests on reading `documents.ts:873-877, 976, 1394, 1410`. MO1/MO2 prove only that O1/O2 would catch a setter that dropped the bearer.

## What I could not test

- **The live PR body on GitHub:** no credential is logged in, so I cannot confirm that `PR_BODY_FINAL.md` is what was posted.
- **An end-to-end originate → anchoring run** on compose or ACA (round-1 note 6): no stack was stood up.
- **The tenant ownership guard against a cross-tenant replay:** the harness has no DB. It matters less now, since the signature refuses the replay first (G2).
- **Whether undici's outbound header normalisation could ever differ from what originate hashes.** Inbound values are already OWS-trimmed by Node's parser, so the two agree in every case I could construct. I did not fuzz header bytes such as obs-text or tabs.
- **KS-1730's existence and content** on Linear.
- **The two known reds on develop:** not re-run. As in round 1, neither file is touched and neither imports the changed code.

## Summary

1. Verdict: **GO WITH NOTES** for PR #1690 at `b6dcc14c3fdf`. A GO is about this SHA only.
2. Findings: 0 Major, 0 Minor new. 4 Notes: N1 env templates lack the residual line; N2 absent/empty bearer collide, unreachable past auth; N3 S7d whitespace claim is unit-level only; N4 PR-body draft head line garbled (the residual wording is exact in the local draft; the live body is unread). Round-1 Minor 1 (deploy plumbing) is carried, reportedly filed as KS-1730.
3. Round-1 Minors and notes: **Minor 2 CLOSED**: G2 is refused at head and red at the round-1 head; the MA mutant reddens R9 plus 7 of my cells; MO1/MO2 redden O1/O2. **Note 4 CLOSED**: the M4 mutant reddens R10. **Minor 1 is out of scope and unchanged.**
4. Merge-tree onto develop c2505d5c6: rc 0, tree b21cadde4935, no conflicts. 0 files overlap #1691 (vc-issuer only).
5. Verdict path: `/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-10-26_gate-pr1690-ks1717/verdict_round2.md`
