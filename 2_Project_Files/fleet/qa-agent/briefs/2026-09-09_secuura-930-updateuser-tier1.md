# QA BRIEF — Secuura/Blockchain #930 (KS-1052), TIER 1. Round 1. Schemathesis is a REQUIRED leg.

## BLUF
**One PR, tier 1, auth service. `#930`, head `d491c72c1`, base `develop`. Gate the SHA, not the branch tip** — if the tip has moved, say so and stop. **Findings only: you never fix, never merge, never push, never deploy.**

## WHAT CHANGED
`userRepo.updateUserOrThrow(id, updates, operation)` — calls `updateUser` and, on `null`, logs and **throws 503**. **Ten call sites switched to it**, so the guard is one function rather than ten copies of an `if` that ten authors must each remember.

**The defect being fixed:** `updateUser` returns `null` when a write matches no row, and ten callers **discarded the return and reported success anyway.** The worst two are credential-lifecycle:
- **`passwordLoginGate.ts:256`** — burns a **single-use MFA backup code**. On a 0-row write the code was **not consumed, stayed valid, and the login still succeeded**, under a comment reading *"Single-use: burn it before it can buy a second credential."*
- **`auth.ts:823`** — reported *"Password has been reset successfully"* then consumed the reset token, with the password unchanged.

**At both token sites the check now runs BEFORE the consume.** That ordering is the property to verify — not merely that a 503 appears.

## 🔴 REQUIRED LEG — SCHEMATHESIS. This is why the PR is tier 1.
**The change turns previously-200 responses into 503 on EXISTING auth operations.** No spec change, no new route or method — **and the contract is what a 200 meant to a client.** Run the contract sweep and report what it says about the changed operations specifically. **A gate on this PR that skips Schemathesis has not answered the question the PR raises.** If you cannot run it, say so plainly and prominently — that is a real result and it changes my ruling.

## WHAT THE BUILDER SAYS IS NOT COVERED — test these, do not re-derive them
1. **The backup-code burn has NO dedicated cell** — covered only indirectly by two KS-781 suites.
2. **MFA routes were converted and typechecked, NOT driven.**
3. **No live-RLS reproduction** — the unset-GUC path is argued from source, not exercised.
4. **The mock class was closed EMPIRICALLY, not structurally:** 18 of 20 `userRepo` mocks lack the new export and only the 2 reaching a burn path failed, so **the full-suite run is the discriminator rather than a grep.** The structural fix (a shared `__mocks__` built from the real export list) is F-926-2's, not this PR's.

## DELIBERATE DIVERGENCE, ruled and not to be reported as an inconsistency
**`updateUserOrThrow` answers 503; `wallet.ts` in #929 answers 500 for the sibling condition.** Ruled deliberate by Wednesday: the condition is retryable and **at the token sites the caller still holds an unburnt single-use credential**, so a 500 invites them to abandon a valid token. Cross-referenced on #929. **Report anything that makes 503 the WRONG choice; do not report the difference itself as a defect.**

## THE BUILDER'S OWN EVIDENCE — verify, do not assume
    tsc --noEmit          0 diagnostics, positive control: planted TS2322 seen in the changed file
    services/auth full    642/642 green, TWICE consecutively (193 suites)
    clean-develop control 635/635 on a separate worktree at d4cf7e3cf
    RED PROOF             both auth.ts guards reverted -> 7 tests RAN, exactly the 4 defect cells red,
                          BOTH CONTROLS still green; restored byte-identical, sha256 c1c3515c...e3a0
⚠ **`null` has TWO indistinguishable causes** — 0 rows, or a blind read-back under an unset GUC. **Every message therefore says "could not be confirmed" and none says "matched no row."** Check that the wording holds everywhere, including any message you can reach that the builder did not name.

## HOW TO WORK — traps that cost the last three seats real time
- **`services/auth` and `services/api-gateway` are VITEST. `services/originate` is JEST.** The wrong runner gives 27 suites failed / 0 tests — the all-fail signature meaning *test the tool, not the subject*.
- **A fresh worktree needs `npm ci`, `npm run build -w packages/shared`, AND the nested `node_modules`.**
- **A tamper that breaks compilation is not a red-proof** — the suite reddens having executed zero tests.
- **A tamper's restore needs a UNIQUE anchor:** `grep -c` == 1 before you tamper, whole-file sha256 after. A seat was saved last night by exactly that assertion from corrupting a sibling function that every test would have passed over.
- **Do not pipe a command through `tail`/`head` and read the absence as a result.** Two consecutive seats made that error last night, including the one warned about it.
- **A known flake:** `ks949-platform-admin-seed-identity.test.ts` (KS-1053) — fails run 1, passes 2-7 and 30/30 alone, timeout hypothesis refuted, mechanism unestablished. **If you see it, that is it; capture the name BEFORE re-running.**

## YOUR RULES
- **Findings only.** Never fix, never merge, never push, never deploy. **Demo and UAT are HELD by Kam — do not reach any Secuura environment or shared database.** Disposable local containers only, removed at close.
- **Every finding: what you did, what it produced, and the control that makes the result mean something.** A zero without a control is not a finding.
- **State what you did NOT test with the same prominence as what you did.**
- **Verdict: GO / GO WITH FINDINGS / NO GO, with severities. This is round 1 — nothing is at the two-NO-GO cap.**
- **Mail the verdict to `wednesday-agent@agentmail.to`.** A verdict that lives only in your scrollback is one pane-close from being lost, and that has happened in this fleet.
