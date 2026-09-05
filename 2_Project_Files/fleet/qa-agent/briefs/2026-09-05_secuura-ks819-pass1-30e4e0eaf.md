# QA Agent Invocation Brief — Secuura / Blockchain (Platform K), KS-819 TIER-2 THROUGH-CODE PASS 1: PR #824 @ `30e4e0eaf` — the OAuth-state consume order and the provider-in-key fix for the KS-722 gate's five findings; two pins on #822's unguarded changes

**TIER 2 (through-code only) — reason: a follow-up on a surface ALREADY gated tonight (KS-722's tier-1 pass at `ca4db0b1c`); the changes are ordering, a key shape, a doc contract and tests; no new door, no deploy, no rendered surface (JSON callbacks). ROUND 1 of the KS-819 class.**

**R0 (client isolation):** exactly one client's content — Secuura / Blockchain (Platform K). Report under `projects/secuura/`. Platform S is a different project.

## Charter (read first, in full)
`/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/QA_AGENT_CHARTER.md`.

## 1. Target
- **Client / Project:** Secuura / Blockchain. **Source tree (read-only):** `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files`. The builder s132 is LIVE in that tree (working KS-820/821) — never touch its checkout, its stack (`:6882`), or its worktrees. **Work from YOUR OWN by-SHA copy** (`git archive`, own mktemp, farmed node_modules, own Redis container on your own port proven refusing first — the KS-722 pass's setup is the template).
- **Branch under test:** PR #824 at **`30e4e0eaf`** — verified at origin by Wednesday (`git ls-remote`, no fetch), rebased onto develop **`055182bfe`** (which holds #823). File set and stat: from Wednesday's `git diff --name-status 055182bfe 30e4e0eaf` in the launch call — the report states what YOU measure.
- **Environment:** the auth service under vitest + the real routes with the provider stubbed, a REAL Redis of your own (the double is under test again — see claim 6). No demo, no deploy, no board writes.

## 2. The builder's claims at `30e4e0eaf` — inputs to FALSIFY (s132's mail 2026-09-05T12:05:07Z, read whole by Wednesday; the KS-819 ticket = the KS-722 gate's F-1…F-5 + the social-link line + Wednesday's two pins S131-F2/S131-F3)
1. **F-1 (validity oracle) + F-3 (the "never throws" contract) fixed by ORDERING and a catch:** `if (!code)` moved ABOVE the consume, so a codeless probe neither reveals validity nor burns the state; `consumeOAuthState` catches and returns false (fail-closed → 403 `OAUTH_STATE_INVALID`, not 500) while `storeOAuthState` keeps throwing.
2. **F-2 (cross-provider burn) is NOT closed by ordering — the builder REFUTED the ticket's own recommendation by measurement** (a cross-provider callback carries a good code, so it reaches the consume whatever runs first): fixed separately by putting the provider in the KEY — `oauth_state:<provider>:<state>` — so the wrong provider MISSES rather than reads-then-compares after a destructive read. **Deploy cost stated:** old-shape keys are unreadable in the new shape, so sign-ins in flight at a deploy refuse once, bounded by the 10-minute TTL.
3. **F-4** (`?error=` from the provider) handled: `OAUTH_PROVIDER_ERROR` — the state's fate on that path is a cell (burned or not? the builder says what).
4. **F-5 and the `/api/auth/social/link` state gap are RECORDED at their call sites, NOT closed** — each with why. Verify the recording exists and that nothing claims closure.
5. **S131-F2 and S131-F3 are PINS, not fixes:** a test on the RETURNED trimmed email (→ the JWT claim, `jwt.ts:167`/`:190`) and an adapter test on `google.ts`'s `?? ''` — both shipped in #822 guarded by nothing. Tamper controls by the inverse edit: `?? ''` reddens exactly 1; the untrimmed address reddens exactly 2.
6. **Red-proof, predicted before running, SET and COUNT separately, both exact: 13 cases, 6 failed / 7 passed against the unfixed code** — the six failures = the six findings; the seven passes = four controls + three pins. After: 40 files / 534 tests / 0 failed; tsc 0; lint 0 errors (13 warnings, none in a touched file); `check:openapi` PASS; the 12-leg preflight PASSED on both pushes (spec-auth conformance 321/321; path resolvability 341/341). **Its own corrections, already on the PR:** the total predicted 529 measured 534 (#823's contribution was 18, not 13 — a baseline inference); a first baseline run exited 0 having run ZERO tests (`--reporter=basic` no longer loads, `ERR_LOAD_URL`, vitest still exits 0) — the 503 is from the default reporter's totals line.
7. **The yaml after the rebase:** textual merge md5 `47ac277a5bfd74f3b1c00d2a3fab6e53` = regenerated md5 (agreement measured); `check:openapi` PASS.

## 3. Scope — through-code, narrow
- **Read the diff whole.** State the two mechanisms (ordering; provider-in-key) in your own words and where the KS-722 gate's `consumeOAuthState` call sites moved.
- **Drive through the real routes against a REAL Redis** (provider stubbed): (a) NO code + valid state → the state SURVIVES (EXISTS = 1) and the response does not distinguish valid from invalid state (compare bodies byte-for-byte against the invalid-state case); (b) cross-provider callback (a google state on the github callback) → 403, the victim's state SURVIVES (EXISTS = 1 under the new key shape), then the legitimate google callback → 200 (the whole point of F-2); (c) Redis connected-but-broken (a Proxy that throws on GETDEL/MULTI) → callback 403 `OAUTH_STATE_INVALID`, initiate 500 generic, no stack, no "Redis" string; (d) `?error=access_denied` from the provider → `OAUTH_PROVIDER_ERROR`, and say whether the state is burned; (e) the OLD key shape planted (`oauth_state:<state>`) → the new callback MISSES it (the stated deploy cost, measured) — this is the cell that proves the deploy note true.
- **The KS-722 closure matrix RE-RUN at this head** (the 21 cells from the KS-722 pass's report — `projects/secuura/reports/2026-09-05-s131-ks722-shape1-pass1-ca4db0b1c/`, read it): nothing the door proved may regress under the key change; atomicity 2-way + 8-way again; the MULTI fallback forced again (the new key shape must be in the fallback path too — a fallback that still reads the old shape is the introduced defect to hunt).
- **The no-oracle property re-measured under the new shape:** five refusal conditions → ONE byte-identical body (the KS-722 pass's cell), now including the codeless probe.
- **Red-proofs by extraction:** vitest JSON at `055182bfe` and `30e4e0eaf`; reproduce the 6/7 split from the builder's 13 (predict first); the inverse-edit tampers on the two pins (predict 1 and 2); a tamper that restores the OLD key shape in `storeOAuthState` only (predict which cross-provider cases red).
- **The hunt on the changed hunks:** what else formats or parses `oauth_state:` keys (a TTL sweeper? metrics? an admin listing?) — a second reader still on the old shape is a live defect; error-message parity between the codeless and the invalid-state paths (the oracle's other costume: timing or headers); the social-link recording's wording (is it a claim of safety or a claim of deferral?).
- **Gate re-run** from your copy; tsc, lint, `check:openapi`; console n/a; palette n/a.

**Out of scope:** any deploy; the demo; KS-820/821 (the token endpoint — its own gate later); #823 (merged, gated); Platform S; the builder's checkout/stack; board or GitHub writes.

## 4–6. Credentials / state / boundary — as before
`.env` untouched, never echoed. Own copy, own ports, own Redis (stopped not removed at the end). **NEVER `rm`**; tampers on your copies only, restored by hash; **predict every tamper's failing SET and COUNT before running.** Findings only. Any `rm` the harness stops you on: press nothing, mail a QUESTION. Measure `git status --porcelain` in the builder's tree at START and at END separately, and report both — a start-state carried as an end-state claim was the KS-804 pass's own correction.

## 7. Known-fragile / carried
A fix-shape in a gate report is a hypothesis — run it against the unfixed product first (the builder did, and refuted the ticket's shape for F-2 — reproduce THAT); `--reporter=basic` no longer loads and vitest exits 0 on zero tests — read the totals line AND the exit code, never one; the door-2 grep is self-satisfying — derive your instrument; `fetch` drops a bare `?` — raw socket for wire cases; a bounded command's zero is a suspect until its rc is read; `mergeable_state: unknown` is not `clean`; a generated yaml that merges clean is the WORSE case — regenerate and compare.

## 8. Logistics
- **Time-box:** narrow — the diff read, the five driven cases with the old-key-shape cell, the KS-722 matrix re-run, the extraction red-proofs with predictions, the second-reader hunt, the gate. Aim ~45 min.
- **Findings sink:** `projects/secuura/reports/2026-09-05-s132-ks819-pass1-30e4e0eaf/report.md` + `evidence/`. Claims table (1–7); driven cases; the re-run matrix; red-proof table (predicted vs measured); new findings by severity with evidence class; NOT-TESTED led with the biggest hole; the head observed at the end; porcelain at start AND end.
- **Escalation:** through Wednesday (`wednesday-agent@agentmail.to`, QUESTION subject). Approval-class pauses for Kam.
- **When done:** mail Wednesday, subject `[QA -> Wednesday] KS-819 PASS 1 @ 30e4e0eaf (PR #824)` — BLUF (PASS or NO GO for merge in the first line), report path, the claims table, the driven cases incl. the old-key cell, the re-run matrix's state, red-proofs, new findings, NOT-TESTED, the head observed at the end.

---

PROVENANCE:
- develop = `055182bfe` at origin (#823 merged); PR #824 = `30e4e0eaf` at origin, rebased onto it; the file set by `git diff --name-status` | `git ls-remote --heads origin` + `git diff` on LOCAL objects from Wednesday's seat, no fetch | read 2026-09-05 22:0x
- Claims 1–7 (the two mechanisms, the refuted ticket shape, the deploy cost, the recordings, the pins, 13 → 6/7, 40/534/0, the yaml md5s, the three self-corrections) | s132's mail `[Secuura/Blockchain -> Wednesday] MERGED #823 @ 506b4505e …` 2026-09-05T12:05:07Z (5,284 chars, read whole) | read 2026-09-05 22:0x
- The KS-722 gate's F-1…F-6, its 21-cell matrix, the MULTI fallback forced via a Proxy, the no-oracle cell | `[QA -> Wednesday] KS-722 Shape 1 PASS 1 @ ca4db0b1c (PR #821)` 2026-09-05T11:11:48Z (10,203 chars, read through NOT-TESTED) + its report at the QA tree | read 2026-09-05 21:1x
- S131-F2 / S131-F3 (the two pins' subjects) | `[QA -> Wednesday] S130 follow-ups PASS 1 @ 56f42f5ab (PR #822)` 2026-09-05T11:25:19Z | read 2026-09-05 21:2x
- The KS-804 pass's start/end porcelain correction | `[QA -> Wednesday] CORRECTION: KS-804 PASS 1 …` 2026-09-05T11:57:38Z | read 2026-09-05 21:5x
- TIER 2 / ROUND 1 | Kam's 2026-09-05 20:19 grant, /Volumes/DevMASTER/WEDNESDAY/0_Brain/learnings/2026-09-05_qa-gate-tiers-and-the-two-nogo-cap.md — a follow-up on an already-gated surface | read 2026-09-05 21:0x
- scope: through-code pass 1 on `055182bfe..30e4e0eaf` only — the two mechanisms, five driven cases incl. the old-key cell, the KS-722 matrix re-run, extraction red-proofs, the second-reader hunt, the gate; KS-820/821, #823, the demo, Platform S OUT | this brief's §3, written by Wednesday | read 2026-09-05 22:0x

SELF-CHECK: re-read end-to-end for contradictions | 2026-09-05 22:0x
(checked against the previous mails to the Secuura agent — the #823 GO's queue names KS-819 as tier 2 "READY FOR QA at the end": this is that gate; the claim "F-2 not closed by ordering" is the builder's measured refutation of Wednesday's own #821 GO wording ("move `if (!code)` above the consume" for F-1+F-2) — stated as the builder's, to be reproduced, not adopted; consistent.)
