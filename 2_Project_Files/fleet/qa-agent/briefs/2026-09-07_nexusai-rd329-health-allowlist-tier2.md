# QA GATE — Datasec/NexusAI RD-329, `rd-329-health-payload-allowlist-s43` @ `2e78c76`. **TIER 2 (through-code), round 1 of 2.**

**Charter first, in full:** `/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/CLAUDE.md`
(T9 seat — DevMASTER is not mounted. Every path here is a T9 path.)

## 🔴 READ THIS FIRST — this gate is unusual and the shape matters
**No product code changed.** The change is **129 lines of test plus a counts bump**. The builder
established that the public-response restriction has been correct since **2026-04-25** (`ea37e29`,
Pen-test Tier 3) and is present in `main` *and* the campaign tip. **So no code change closes RD-329.**

**It shipped the guard that was missing, and it told me plainly that no red-proof exists** — the code
is already right, so the suite passes at the base by construction. **Its discriminator is the control
cell, which tampers a copy in both syntaxes and asserts each tamper actually landed before asserting
anything.** That honesty is why this is tier 2 and not tier 1: there is no product-behaviour claim to
falsify, only a guard to weigh.

**Your job is therefore narrower and sharper than usual: is this guard REAL, or is it another spelling
check?** That question is not rhetorical — see §2.

## 1. Target
- **Branch:** `rd-329-health-payload-allowlist-s43` · **Head:** `2e78c76e573c5836037d80d99479cf5129dfba6d`
- **Parent (the baseline):** `9546da5f5585eb6e215d935c4cae2a55c339104b`
- **`origin/main`:** `a9a8cb6e3fc62b8c08e1f3aadecb08519f1f6ddc` — 🔴 **the branch is 248 commits ahead
  of it. DIFF AGAINST THE PARENT, NEVER AGAINST `main`.** (Standing line: base every NexusAI gate on
  `parent..head`; main is the integration branch but is ~247 commits behind — RD-367.)
- **Change:** 2 files, +132/−3 — `__tests__/public-health-payload-allowlist.test.js` (new, 129 lines)
  and `scripts/verify-expected-counts.json`.
- **Repo:** `/Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/2_Project_Files` — **read-only to
  you.** Work in your own worktree or clone.
- **NON-PROD. NO DEPLOY. NO `az`, no live box, no registry, at any point.** Kam's 2026-09-07
  production lift is **Secuura only**. Datasec production is out of scope entirely.
- 🔴 **`nexusai-staging` is a LIVE host currently serving the un-fixed payload. DO NOT CONTACT IT.**
  Its exposure is real and already recorded; it is not yours to probe and re-measuring it is not part
  of this gate.

## 2. 🔴 THE CENTRAL QUESTION — is it an allow-list in behaviour, or only in name?
The builder's stated design is an **ALLOW-LIST**, deliberately, with its own reasoning:
*"no `nodeVersion`" would pass happily while someone adds `tenantId`.* That reasoning is right. **Test
whether the implementation delivers it.**

**A directly relevant precedent from ninety minutes ago, same repo, same builder, same session:** the
RD-362 gate found that repo's runtime-read control cell was `expect(lines).not.toContain('*.md')` —
**exact string identity against four literals, computing no exclusion.** It fired on the literal
spelling and was **silent on four equivalents that all broke the live routes**. Its verdict:
*"a spelling check wearing the costume of a semantic guarantee."*

**So, concretely — tamper a copy and assert each tamper LANDED before concluding anything:**
1. **Add a NEW field** to the public health response (`tenantId`, `workspaceId`, a version string, a
   nested object). **Does the cell go red?** An allow-list must fail on anything unlisted; a deny-list
   dressed as one will pass.
2. **Add a field whose NAME is innocuous but whose VALUE is sensitive.** Does the guard reason about
   keys only, or about the payload it actually serves?
3. **Rename or re-nest an allowed field** (`status` → `data.status`). Does the assertion follow the
   shape, or match a flat key list?
4. **Reach the payload by a different route** — is `/api/health` the only path that renders this
   object, or does another handler build it separately? **Enumerate the render paths**; a guard
   pinned to one call site is blind to a second.
5. **Does the cell drive the real handler, or a fixture that reimplements it?** A test helper that
   reimplements the product is a mock the moment the product moves.

## 3. The counts file
`scripts/verify-expected-counts.json` moves by +6/−3 lines. **Confirm the test-count delta matches
exactly the cells actually added and that they RAN** — a counts bump larger than the cells added is
how a skipped suite hides. Report skipped/disabled counts explicitly.

## 4. What NOT to spend time on
- **Do not re-derive that the product code is correct** — the builder established it (`ea37e29`,
  2026-04-25, present in main and the campaign tip) and Wednesday accepts it. Spot-check it if cheap;
  do not audit it.
- **Do not chase the staging host.** Its stale build is a category-2 infrastructure item, recorded.
- **Do not recommend a red-proof that cannot exist.** The builder was right to decline one; a demand
  for it would be a process error on our side, not a finding.

## 5. Evidence rules — mandatory
1. **Every cell: say what it MOCKS and therefore what it cannot prove.**
2. **Both controls on every negative claim** — a positive control that your instrument fires, **and a
   negative control (an impossible pattern) so a zero is one your reader can vouch for.**
3. **Assert each tamper LANDED before asserting its effect**, and restore afterwards.
4. **`rc` on its own line** for any bounded command. **A uniform non-zero across every variant is as
   suspect as a uniform zero** — the RD-362 gate's tamper matrix returned rc=1 on all five variants
   and looked like a clean red-proof; it was a jest config error and the runs never executed.
   *"A 1 from a crashed command is no more evidence than a 0 from a killed one."* Establish the
   command RAN before reading its exit code as evidence.
5. **Never delete.** Cleanup means quarantine. **Findings-only — you never fix.**

## 6. Verdict
**GO** · **GO-with-findings** · **NO GO**. Severity yours, priority Wednesday's. Round 1 of 2 under
Kam's cap. **A guard that is real but narrow is a GO-with-findings, not a NO GO** — say precisely
which tampers it catches and which it does not, because that list is the deliverable here.

Report by mail to `wednesday-agent@agentmail.to`, subject
`[QA -> Wednesday] Datasec RD-329 health allow-list (@ 2e78c76, tier 2)`.

PROVENANCE:
- head `2e78c76e573c5836037d80d99479cf5129dfba6d`, parent `9546da5f…`, 2 files +132/−3 | `git ls-remote` + `git show --stat`, run by Wednesday in the same action as writing this | read 2026-09-07
- 248 commits ahead of `origin/main` `a9a8cb6e…` | `git rev-list --count` | read 2026-09-07
- the code correct since `ea37e29` (2026-04-25), present in main and the campaign tip; no red-proof available; the control cell is the discriminator; staging serves an older build | the builder's mail `[Datasec/NexusAI -> Wednesday] RD-362 in-repo half SHIPPED …` §RD-329, 2026-09-07T07:43:47Z, re-read from the inbox in this action | read 2026-09-07
- the "spelling check" precedent and the crashed-tamper-matrix rule | the RD-362 gate's verdict mail, 2026-09-07T08:14:21Z | read 2026-09-07
- tier cap of two NO GO rounds | Kam, 2026-09-05 20:19 | read 2026-09-07
- production lift is Secuura-only | Kam, panel 2026-09-07 12:07 + 12:10 | read 2026-09-07
- **UNMEASURED, stated as such:** whether the guard fails on an unlisted field, and whether any second render path builds this payload. Those are this gate's questions.

SELF-CHECK: re-read end-to-end for contradictions | 2026-09-07 18:32
