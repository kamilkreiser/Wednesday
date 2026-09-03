# QA Agent Invocation Brief — Datasec/NexusAI, S31 ITEM 0 (Kam's mock conformance), THROUGH-CODE + LOCAL RENDER

## Charter (read first, in full)
`/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/QA_AGENT_CHARTER.md`

**Then your own pass 21 on this project's previous round, for the baseline and the open findings:**
`/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/nexusai/reports/2026-09-04-s30-fixround-through-code/SUMMARY.md`

## 1. Target
- **Client / Project:** `Datasec / NexusAI`
- **Subject:** branch `rd-136-nga-defaults-s12` @ **`2f3ce7d`** (item 0 only), over the prior head `3dda4ec`.
- **Running target: a LOCAL run you stand yourself. NOT the demo.** RD-76 stands, and RD-294 means the demo
  has no sustainability data to render at all.
- **Production?:** nothing is deployed and **no finding of yours triggers a deploy.** `caf1fe7`'s GO is
  WITHDRAWN. A deploy happens later, on Wednesday's GO, bundled with a config change — not on this pass.

**SURFACES TO LEAVE ALONE — do not restand, restart or kill any:** `:3068` `:3072` `:3073` `:3075` `:3076`
`:3077`. **`:3077` is the source of the frames Kam is reviewing.** The builder stood its own on `:3080`;
stand yours on a port of your own choosing that is none of the above.

## 2. THE BUILDER'S TWO WARNINGS — carried VERBATIM and credited, so you do not lose the time it predicted
The S31 builder named these unprompted. **Both are real and both would cost you twenty minutes:**
1. **A fresh `DATA_DIR` redirects `/` to `/first-run-setup`.** Set `firstRunComplete: true` in `settings.json`
   and restart.
2. **`SEED_DEMO_DATA=true` DOES NOTHING on a local run** — the seeder is only wired into the LAW boot branch
   (`server.js:3553` versus the `else` at `:4087`). **That is RD-293, already filed.** Seed out of band by
   calling `seedDemoDataIfRequested` against the same DB. **Seeded, the window resolves to
   2026-01-30..2026-04-29 — which is the mock's own example window**, so the pill you are checking has real
   dates behind it rather than an empty state.

Its suggested stand-up line:
`DB_PATH=<dir>/printer_logs.db DATA_DIR=<dir> RATE_LIMIT_MAX=20000 PORT=<port> NODE_ENV=development node backend/server.js`

## 3. The claims to falsify — all the builder's, and it has already been right against Wednesday once
1. **The pill renders `30 Jan – 29 Apr 2026 · all stored data`** with **U+2013**, not a hyphen and not the
   word "to". **THIS IS THE LOAD-BEARING ONE AND IT IS WHERE WEDNESDAY WAS WRONG:** Wednesday's brief said
   "to"; the builder hexdumped the ratified mock at
   `docs/sustainability/mocks/s25-relayout-mock.html:117` and found `e2 80 93`. **Verify the RENDERED
   character by its codepoint, not by how it looks** — a hyphen, an en dash and an em dash are three
   different characters that read almost identically at normal size.
2. **The Refresh button is gone from the topbar**, along with the `.nx-sus-refresh` rule.
3. **Error recovery is UNTOUCHED.** The builder claims `window.refreshSustainabilityKpis` is still wired to
   the error panel's Retry at `sustainability-ui.js:928`, and says it asserted this **on the error render**
   rather than by reading the code. **Drive the error state and confirm Retry actually re-fetches.** This is
   the claim that would hurt most if wrong.
4. **Gate PASS 1414/1414 across 83.** Measure it yourself, at this SHA.
5. **Its four red-proofs, each with the failing SET predicted in writing before the run** (pill reverted to
   ISO → 5 named cases; `humanDate` via `new Date()` → 2 hostile-clock cases only, with describe-1 staying
   green; Refresh restored → 1; pill dropped/topbar kept → 8, with the positive control firing).
   **Re-run at least the second one:** it is the one whose value depends on a timezone patch, and the builder
   disclosed that its FIRST two attempts at that guard could not have failed.
6. **The year rule is the builder's EXTRAPOLATION, not the mock's, and is labelled as such in the tests.**
   The mock gives one same-year example. **Check the label is actually there** — an extrapolation presented
   as the mock's rule is the defect; an extrapolation marked as one is correct practice.

## 4. What is NOT in scope
Pass 21's F-7…F-12 (the builder is working them in parallel — do not re-report them), the demo environment,
RD-294's seeding gap, and any deploy question.

## 5. Credentials
`/Volumes/DevMASTER/!CODING/Datasec/NexusAI/4_Credentials/` — you should need nothing beyond a local run.

## 6. State-mutation & cleanup
**Exclude-and-report-only.** Zero writes to the NexusAI tree.
**NEVER `rm`, in your scratchpad or anywhere else — STANDING, all projects** (Kam's rule: cleanup means
quarantine, not removal). Build each attempt in its own `mktemp -d` and abandon the old one; if a path must be
cleared, move it into a dated `_quarantine_YYYY-MM-DD/` and say so. Guard every expansion
(`"${DIR:?unset}/${SUB:?unset}/…"`). **If cleanup is costing real budget, stop and report the affected checks
as NOT RUN with the blocker named.**

## 7. Output boundary
**Findings only.** No code, no tests, no fixtures, no tickets, no config. Describe the fix-shape in prose.

## 8. Method
**Green baseline first, then tamper with the failing SET predicted in writing. A control that has never been
made to fail is a claim; a control that isolates nothing measures nothing.** And the one this project keeps
producing: **a guard can be green because it cannot SEE** — the builder's own timezone case was green against
the defect it names because the ambient zone hid it. **Ask of every assertion what would make it red.**

## 9. Logistics
Report to `projects/nexusai/reports/2026-09-04-s31-item0-through-code/`. Escalate through
`wednesday-agent@agentmail.to`, subject `[Testing Agent MAIN -> Wednesday] QUESTION: <topic>`.

---

PROVENANCE:
- Subject SHA `2f3ce7d`, the gate figure, the rendered pill string and the removed button | the S31 builder's STATUS mail to wednesday-agent@, 2026-09-03T23:03:56Z — its measurements, not re-derived by Wednesday | read 2026-09-04 09:08
- The mock's separator is U+2013 at line 117 | the builder's hexdump quoted in that mail; the mock itself is at /Volumes/DevMASTER/!CODING/Datasec/NexusAI/2_Project_Files/docs/sustainability/mocks/s25-relayout-mock.html — the NexusAI tree, not yours | read 2026-09-04 09:08
- The two stand-up warnings and RD-293 | the same mail | read 2026-09-04 09:08
- Kam's `conform-both` ruling that item 0 implements | his panel message 2026-09-04T07:08:15+10:00 | read 2026-09-04 08:31
- The six surfaces that must stay up, and `:3077` as the frames' source | /Volumes/DevMASTER/WEDNESDAY/0_Brain/daily/2026-09-04.md, the 04:41 handover block — Wednesday's own tree, not yours | read 2026-09-04 06:05
