# QA Agent Invocation Brief — Datasec/NexusAI, RD-464 r3 merged with main — TIER 1, round 1 of 2

**Written by Tuesday 2026-09-20 19:4x. Commissioned but NOT YET LAUNCHED — see LOGISTICS.**

## Charter
Read `fleet/qa-agent/QA_AGENT_CHARTER.md` in full first. You are an independent tester. You did not
build this and you owe it nothing.

## 1. Target
- **Branch `rd-464-r3-merged-main-s72` @ `60c76d76350321ad8f51324e042052a8a9f49a96`**, pushed to origin.
- Parents: `1f27b4d` (RD-464 r3) and `34ad321` (main). **Both verified ancestors by Tuesday — C-68 holds both ways.**
- **NOT on main. Nothing merges on your word or the builder's.**

## 2. What this change IS, and where a gate earns its keep
**It is a MERGE of two already-separately-gated changes. It introduces no new visual behaviour of its
own.** **The merge-specific risk is their INTERACTION — and that is the one thing neither parent
could have tested**, because `getUsableLLMAdapter()` exists only on main and `aiReadiness` only on r3.
**Do not re-gate either parent's work. Gate the seam.**

## 3. The two places that carry the seam
**(a) `static/js/first-run-setup.js` AUTO-MERGED although BOTH sides changed it** (main +217/−25, r3 +21/−3).
The builder checked rather than trusted: base ranges disjoint (r3 318–347; main 289–298 then 371+),
both sides' symbols present after the merge — r3's `_aoaiResultBox` **17**, main's `_aoaiPendingAct`
and `_renderAoaiPending` **3** each — and RD-549's `d.pending` branch surviving. *"Active
immediately."* is pre-existing at the merge-base and remains the fallback for the NOT-pending case only.
> **Verbatim, and it is this gate's premise: "A clean auto-merge is an absence of textual
> disagreement, never a verdict. A browser is what settles it."**

**(b) The AI Setup step, end to end.** Save an unconfirmed config → confirm it → clear it. And the
Test action's result box across **notChecked / throttled / reachable-but-deployment-not-ready**.
**r3 rewrote that result box; main rewrote the confirmation UI around it.**

## 4. The property that must hold (RD-549 × RD-464)
**AI config that is saved but NOT admin-confirmed must never be probed or reported "ready".**
`getUsableLLMAdapter()` must drop unconfirmed config BEFORE `aiReadiness` sees an adapter.
R14 (`__tests__/rd464-rd549-unconfirmed-not-probed.test.js`) asserts this and red-proves; **your job
is whether the UI agrees with the cells.**

## 5. Drivable surface — LOCAL RUN, **NOT THE DEMO**
🔴 **The demo cannot test this. RD-76 is real: the demo's `/login` carries ZERO `<form>` and ZERO
`<input>` elements, so no test account opens it.** A local run at `60c76d7` against a **fresh data
dir** serves every page and API in open mode by design (`isAuthEnforced()`), with **no auth shim and
no test-only branch** — the same commit, not the demo image.
**SAY THIS IN YOUR VERDICT so nobody later records a demo pass that did not happen.**
- Recipe: **`docs/runbooks/local-run-for-qa.md` on branch `docs-local-run-runbook-s72` @
  `853e5498765936fa537383ab90a3c87ac4c0ff4b`** (83 lines, tracked, pushed — verified by Tuesday in
  the object store at 19:5x, not read back from the mail). It is **off main, so `60c76d7` is
  untouched by it**; check it out separately or read it with `git show
  853e5498765936fa537383ab90a3c87ac4c0ff4b:docs/runbooks/local-run-for-qa.md`.
  *(This replaces the earlier "ask the builder" line: its first copy lived in `session-tools/`,
  outside version control, and the builder moved it on being told.)*
- Expect at boot: `🚀 Printer Dashboard API running on port <N>` and **`🚨 AUTH NOT ENFORCED at boot`**.
- `GET /api/health` → 200. **`build: unknown` is CORRECT for a local run** (`BUILD_DIGEST` is set at
  image build) — do not file it.
- A driven browser is **PROVEN on this machine tonight** at this SHA on `/first-run-setup`
  (real render, PNG read back, console zero errors, five pre-existing verbose DOM advisories).
  `claude-bridge` MCP is down (`CONNECTION_CLOSED`); Playwright is separate and works. **If you need
  `claude-bridge`, STOP and say so rather than routing around it.**

## 6. ALREADY MEASURED — do not redo it; spend your session on the seam
- `VERDICT: PASS — 3772/3772 across 214 suites` (jest exit 0, 880.8 s).
- Counts **read from the file**: tests 3772, suites 214, `_updated 2026-09-20T09:19:47.049Z`. Two
  predictions committed in advance, **both exact**.
- **Seven rd545 cells BY NAME: 7/7** (K-live, K-switch, K-addr, A1–A4).
- **M4 arm re-applied at the merge head: STILL REDDENS** — 5 failed / 2 passed; K-switch and K-addr
  stay green *correctly*, neither reads the counter M4 disconnects. sha256 restored.
- Acceptance criteria, re-measured by Tuesday at `60c76d7`: `getLLMAdapter()` **0** ·
  `getUsableLLMAdapter()` **9** · `namedAoaiError` **7** · `AiEndpointRedirectError` **7** ·
  `AOAI_FETCH_OPTIONS` **3** · `startDeadline` **4** · `HEALTH_PROBE_TIMEOUT_MS` **3** ·
  `readiness:'not-checked'` **3**.

## 7. Known-fragile / known-changed
- **`module.exports` in `azureOpenAIAdapter.js` was resolved as a UNION.** Neither parent's line
  alone is correct; taking either makes `__tests__/rd523-aoai-redirect-refused.test.js` **fail at
  IMPORT** — a suite-wide error that reads as "the merge broke the tests". **If you see an import
  failure there, check the export line before anything else.**
- **Hunk 2 of that adapter** was resolved to keep BOTH main's `namedAoaiError(e)` with its `code` AND
  r3's deadline/readiness additions. **Any regression to `e.message` alone deletes RD-486/RD-523's
  redirect-refusal naming** — shipped the same day.
- `git ls-files`-based census cells **triple their population during an unresolved merge** (C-104).
  The tree you get is committed, so this should not bite — **but if a census cell reports a count
  that is an exact multiple of 3, check `git ls-files | wc -l` against `sort -u | wc -l` before
  believing it.**

## 8. Output boundary
**Write your report to:**
`/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/nexusai/reports/2026-09-20-rd464-r3-60c76d7-tier1/report.md`

**MAIL YOUR VERDICT** to **tuesday-agent@agentmail.to** with the subject line exactly:
`[QA/Datasec-NexusAI -> Tuesday] GATE VERDICT — RD-464 r3 @ 60c76d7 (tier 1)`
and open the body with one of **GO** / **GO WITH FINDINGS** / **NO GO**.

**Every finding carries its evidence class.** A Major comes to Tuesday; **a further round is Kam's
(C-62)**. Cap: two NO GO rounds on this class — this is round 1.
**You do not merge, push to main, or edit product code.**

## LOGISTICS — RESOLVED 2026-09-20 19:5x
**The earlier note here said every QA launcher points at an unmounted DevMASTER. That was a census
over the WRONG FRAME** — it was true of the newest launcher, which is Wednesday's Secuura one. **The
NexusAI launchers are already T9-pathed**: `launch_qa_nexusai_rd327_67c2992.sh` carries
`QA_DIR='/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN'` and `TUE='/Volumes/KK_T9_External_HDD/TUESDAY'`.
This gate's launcher is derived from it: `launchers/launch_qa_nexusai_rd464_r3_60c76d7.sh`.

**Measured by Tuesday at 19:5x, in the worktree, before the launch:**
- Worktree `/Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/worktrees/s72-rd464-r3`,
  HEAD `60c76d76350321ad8f51324e042052a8a9f49a96`, branch `rd-464-r3-merged-main-s72`, clean
  (only untracked `node_modules`).
- **Parents read from `rev-list --parents`:** `1f27b4dadac61f8ab305e5a25f1acd2f92d4bafa` (r3) and
  `34ad321ee18401c1f965244e5c4e06438aae01d0` (main). **This is a MERGE commit — a single-parent
  commit-count guard does not apply to it, and the launcher asserts both parents instead.**
- `git ls-remote origin rd-464-r3-merged-main-s72` = `60c76d7…` — the head is at origin.
- Usage gate at launch: **89% < 95%** (this seat's stop, per Kam's "bump yours to 95%").
