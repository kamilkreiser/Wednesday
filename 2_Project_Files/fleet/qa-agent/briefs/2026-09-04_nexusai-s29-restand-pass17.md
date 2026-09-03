# QA Agent Invocation Brief — Datasec/NexusAI, S29's restand (items 1+2+3), PASS 17

## Charter (read first, in full)
`/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/QA_AGENT_CHARTER.md`

## 1. Target
- **Client / Project:** `Datasec / NexusAI`
- **Running target:** **`http://127.0.0.1:3075`** — pid 3957, worktree `qa-worktrees/ea6378d`,
  isolated data dir, seed verified (`cost_per_sheet_paper=0.011`, money tile 136.345 off the wire).
  **Left UP for you.** `:3073` (`93cbdc4`) and `:3074` (`be2159f`) are also up as the before/after
  pair — use them as controls.
- **DO NOT TOUCH `:3072` or `:3068`.**
- **Environment:** local run, fresh data directory, **same commit as the branch, NOT the demo
  image**. **Authentication: none — open mode by design** (`isAuthEnforced()` in
  `backend/server.js`; no auth shim, no test-only branch). RD-76 stands: the demo's `/login` is an
  Entra button with zero `<form>` and zero `<input>`, so no test account opens it. **Say "same
  commit, local open mode" in your report — never that the demo was tested.**
- **Production?:** NO. Nothing deployed. `--0000094` still serves `9520b8c` and the `caf1fe7`
  deploy GO is WITHDRAWN. **You must not deploy, and no finding of yours triggers one.**

## 2. Spec / DoD being tested against
Branch `rd-136-nga-defaults-s12` @ **`4aabad0`**. **Read `ea6378d` for product code** — `4aabad0`
adds only HISTORY.md and the handover. Commit walk:

    e141ca4  item 1  the four ratio figures + 28 declarations rewritten + css-ratio-comments test
    75c2f76  item 3  RD-284 — the light contrast arm walks the state matrix; global ceiling gone
    be2159f  item 2  RD-283 — every colour rule states its ground; the head text moves on-guide
    f8ab34b  item 3 follow-ups + repinned token counts
    ea6378d  the before/after capture script

**The claims to falsify** (all the builder's, none re-derived by Wednesday):
- **Item 2 / RD-283:** light rank head `#6c757d` on `#f8f9fa` 4.449 (margin −0.051, BELOW AA) →
  `#495057` on `#f8f9fa` **7.757**; dark `#8c8c8c` on `#262626` 4.500 (margin **+0.000**) →
  `#b4b4b4` on `#262626` **7.299**. **The GROUND is unchanged in both modes** — the header keeps
  its ratified tint and now DECLARES it rather than inheriting it from a bare `th` in another
  sheet; only the text moved, onto the token `docs/BRAND.md` R4 already prescribes for that ground.
- **Item 1:** the four corrected figures and 28 annotated declarations in a checkable shape, plus
  `__tests__/css-ratio-comments.test.js` recomputing every ratio comment through the repo's own
  helper and failing beyond 0.005.
- **Item 3 / RD-284:** the light arm walks 23 states, 23 visible; **a per-state failure LIST, not a
  count**, so a swap cannot net to zero; the single global `LIGHT_BASELINE` ceiling is gone.
- **Items 1 and 3 move NO pixels.** Only one visible change exists in the whole restand: the
  Sustainability rank-table headers, both modes. **Do not hunt a full-page before/after difference
  that is not there** — the builder stated this explicitly and it is a fair statement.
- **Source tree (read-only):** the worktree behind `:3075`.

## 3. Scope — and the builder named its own weak points, which is where to start
It handed you five attack lines unprompted. Take all five; they are good.
1. **Re-derive the four pairings independently.** They are the whole of item 2 and they are its own.
2. **Check the 0.15 margin floor is not FITTED to the answer.** Its own words: it has to pass the
   4.689 card class (+0.189) and fail the 4.500 rank heads (+0.000), *"which is one step from
   choosing it to make my own numbers pass."* It is stated in the file header as a headroom policy
   rather than derived. **Say plainly whether that is a policy or a curve fit.**
3. **Try to make the light arm vouch for nothing again.** It is a per-state failure list
   specifically so a swap cannot net to zero — **so try a swap.**
4. **The margin gate's vacuity guard** requires >60 measured elements per mode. **Close the tab
   under it and confirm it REDDENS** rather than reporting a clean empty page.
5. **RD-286 — the builder's own late find, and the live hole:** nothing checks that a ratio
   comment's NAMED ground is the ground the browser actually PAINTS, and 28 annotated declarations
   sit behind that gap. **This is the highest-value thing in the brief.** A comment that says
   `/* 7.757:1 — #495057 on #f8f9fa */` is only true if `#f8f9fa` is what paints there.
- **Out of scope / do NOT touch:** `:3072`, `:3068`, any deploy, any Azure resource, the demo, and
  any write to the NexusAI repo.

## 4. Credentials
**None — the surface is open mode.** If you believe something needs auth, report it as a coverage
gap; do not provision anything.

## 5. State-mutation & cleanup
**Exclude-and-report-only.** `:3075` has an isolated data dir; you may drive the UI freely, but any
scratch file goes in YOUR scratchpad and nothing is copied back. Regenerate the before/after frames
with `BEFORE_URL=http://127.0.0.1:3073 AFTER_URL=http://127.0.0.1:3074 node
scripts/capture-rank-head-before-after.js` — it prints each frame's measured colour and ground
beside the filename.

## 6. Output boundary (fixed)
**Findings, reports and recommendations ONLY.** No code, no tests, no fixtures, no tickets, no
config. Describe the fix-shape and the regression test in prose; the project's own agent authors it.

## 7. Known-fragile / known-changed — do NOT re-report as new
- **The screenshots are NOT committed** — `tests/screenshots/.gitignore` is a bare `*` and the
  builder left it alone rather than forcing past it with `git add -f`. Correct call; not a finding.
- **Item 4 (RD-282, the 701px overflow) was FILED, not fixed** — it is shared page chrome
  (`.tab-button` in `.tab-buttons`), affects all nine tabs, and is not this tab's defect. Do not
  re-file it. Item 5 is a Kam card, untouched by design.
- **The light difference is close to imperceptible at reading size.** That is the INTENDED outcome
  for a legibility fix on a design Kam ratified by eye — a small visual delta is not a finding here.
- Three self-disclosed errors are in the builder's handover. Read them; do not re-report them as
  your discoveries, and say if any is understated.

## 8. Logistics
- **Time-box:** one bounded pass. Depth over breadth — items 2 and 3 and RD-286 first if you cut.
- **Report to:** `projects/nexusai/reports/2026-09-04-s29-restand-pass17/SUMMARY.md` under your own
  tree, then mail Wednesday a summary. **Wednesday reads the FULL report, not the mail** — put the
  load-bearing measurements in the report and do not compress them away.
- **Escalation:** `wednesday-agent@agentmail.to`, QUESTION subject. Approval-class items always
  pause for Kam. Priority on any finding is the humans' call, never yours.
- **Your NOT-TESTED list is first-class output** and is read as carefully as the findings.

PROVENANCE:
- The branch, SHA `4aabad0`, code head `ea6378d` and the six-commit walk | S29's READY FOR QA mail 2026-09-03T14:33:43Z in wednesday-agent@agentmail.to | read 2026-09-04
- The surface :3075, its pid 3957, worktree, seed values and the three off-the-wire sha matches | that same mail | read 2026-09-04
- :3073 / :3074 / :3075 all answering 200 | curl from Wednesday's seat in this action | read 2026-09-04
- The four RD-283 pairings and their margins | that same mail's frame table | read 2026-09-04
- The five attack lines and RD-286 | that same mail's "FOR THE TESTER" section | read 2026-09-04
- Open mode / RD-76 / no test account opens the Entra login | that same mail, and the standing RD-76 position | read 2026-09-04
- The deploy hold (--0000094 serves 9520b8c; caf1fe7 GO withdrawn) | /Volumes/DevMASTER/WEDNESDAY/0_Brain/daily/2026-09-03.md, the 22:37 rotation block, and that same mail | read 2026-09-04
- Kam's QA-gate order (agent -> Wednesday -> testing agent -> Wednesday) | /Volumes/DevMASTER/WEDNESDAY/0_Brain/learnings/2026-09-01_qa-gate-before-my-verification.md | read 2026-09-04

SELF-CHECK: re-read end-to-end for contradictions | 2026-09-04 00:53
