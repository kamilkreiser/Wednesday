# QA Agent Invocation Brief — Datasec/NexusAI, S29's F1/F2 fix round, PASS 18

## Charter (read first, in full)
`/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/QA_AGENT_CHARTER.md`

## 1. Target
- **Client / Project:** `Datasec / NexusAI`
- **Running target:** **`http://127.0.0.1:3076`** — the fix at `fe4eed3`, stood by the builder and
  sha-verified off the wire. **`:3073` (`93cbdc4`, pre-RD-283)** and **`:3075` (`ea6378d`, the
  regression)** are up as your before/regressed controls. **A three-surface comparison is available
  and is the point of this pass.**
- **DO NOT TOUCH `:3072` or `:3068`.**
- **Environment:** local run, fresh data dir, **same commit, open mode, NOT the demo image**
  (`isAuthEnforced()` in `backend/server.js`; RD-76 stands — the demo `/login` is an Entra button
  with no form). Say "same commit, local open mode" — never that the demo was tested.
- **Production?:** NO. Nothing deployed; `--0000094` still serves `9520b8c`, the `caf1fe7` GO is
  WITHDRAWN. You must not deploy and no finding of yours triggers one.

## 2. What changed and the claims to falsify
Head **`fe4eed3`**. Predecessor pass (pass 17) found F1 Major, F2 Minor, F3 Structural. This round
answers all three. **All measurements below are the BUILDER's — falsify them.**
- **F1 fix:** `.nx-sus-rank td:last-child` split from `th:last-child`, given `#ffffff`. Claimed
  three-surface measurement: `:3073` own=transparent → painted `#ffffff` (×6) · `:3075` own=`#f8f9fa`
  → painted `#f8f9fa` (×6) · `:3076` own=`#ffffff` → painted `#ffffff` (×6).
- **The class audit — this is the claim most worth attacking.** The builder says comment-stripped
  there are **exactly two** grouped selectors carrying a ground it added in `sustainability.css`, and
  **all 18 in `dark-mode.css` are single**. The second light group,
  `.nx-sus-topbar h1, .nx-sus-title`, is claimed **inert** because the `h1` IS the `.nx-sus-title`
  element, so the group is redundant and the declared `#00719f` equals the ancestor ground.
  **Verify the enumeration itself, not just the two it names** — *"the tester found one" is not
  "there is one"*, which is the builder's own line and it cuts both ways.
- **F2 fix:** shipped `#8c8c8c` on `#262626` = **4.5004**; `#868686` on `#262626` = **4.1566**. The
  builder also corrected the *reason*: muted is **not** illegal on the dark raised ground — it clears
  AA by **0.0004** — so the dark head moved because a 0.0004 margin is not a margin, while light
  moved because 4.449 is genuinely below AA. **Check both sheets now state which reason applies to
  which mode, and that neither still claims illegality in dark.**
- **RD-286 re-size:** the builder probed option (b) rather than taking it on trust. Claimed:
  **107 declared grounds, CSSOM-unset ineffective on 0** (so CSP does not govern CSSOM writes),
  **mismatches 31 pre-fix → 25 post-fix, and the 31→25 delta is exactly the six `td` cells and
  nothing else.** It reports a **false-positive floor of 25**, all claimed legitimate: 19 intentional
  design surfaces + 6 correctly-restated cross-sheet grounds. **Attack the floor: are all 25 really
  legitimate, or is a real mismatch hiding among them?** That is the question that decides whether
  the guard is shippable.
- **Regression check:** `npm run verify` claimed **1391/1391**; full Playwright **90/90**.

## 3. Scope
- **Charter:** confirm the regression is gone on the rendered artefact, then hunt the class the
  builder says it already hunted. **Its own account of why it could not see F1 is the highest-value
  lead in this brief** (see §7) — look for anything else that instrument hid.
- **In scope:** the rank tables both modes, the two grouped selectors, the ratio comments, the
  RD-286 probe's arithmetic and its 25-item floor.
- **Out of scope / do NOT touch:** `:3072`, `:3068`, any deploy, any Azure resource, the demo, any
  write to the NexusAI repo.

## 4. Credentials
**None — open mode.** Report anything needing auth as a coverage gap; provision nothing.

## 5. State-mutation & cleanup
**Exclude-and-report-only.** Scratch stays in YOUR scratchpad; nothing copied back.

## 6. Output boundary (fixed)
**Findings, reports and recommendations ONLY.** No code, tests, fixtures, tickets or config.
Fix-shapes and regression tests in prose; the project's agent authors everything.

## 7. THE LEAD — the builder's account of why it could not see F1
Quoted because it is the most useful thing in the round and it may not be exhausted:

> *"The script that added the grounds took each selector as `sel.split('\n')[-1]` — the LAST line
> only — so a grouped selector was silently truncated to its final member. I then 'verified' with
> `sed -n '/^\.nx-sus-rank th:last-child/,+7p'`, which starts AT that line and hides the
> `td:last-child,` above it. Two views of the file, truncated the same way, and I never read the raw
> rule. I built the instrument that hid it and then trusted it."*

**That is two independent-looking views sharing one truncation — suspicious agreement, where the
harness is the suspect rather than the subject.** Ask: **what else did those two views touch?** Any
declaration added or checked through the same `split('\n')[-1]` path inherits the same blindness, in
any sheet. Also note the builder's own admission that **dark came out 16/16 by luck of the regex it
happened to use there, not by judgement** — so dark's clean result is not evidence of a sound method.

## 8. Known-fragile / known-changed — do NOT re-report as new
- **RD-282 (701px overflow) is filed-not-fixed** — shared page chrome, all nine tabs, not this tab's
  defect.
- **Screenshots are not committed** (`tests/screenshots/.gitignore` is a bare `*`) — deliberate.
- **The light header text difference is imperceptible at reading size** — intended for a legibility
  fix on a design ratified by eye. Not a finding.
- Item 5 (mock date format + the extra Refresh button) is **Kam's card**, untouched by design.

## 9. Logistics
- **Time-box:** one bounded pass. Depth over breadth — F1's class audit and RD-286's 25-item floor
  first if you cut.
- **Report to:** `projects/nexusai/reports/2026-09-04-s29-f1fix-pass18/SUMMARY.md` under your own
  tree, then mail Wednesday a summary. **Wednesday reads the FULL report, not the mail.**
- **Escalation:** `wednesday-agent@agentmail.to`, QUESTION subject. Approval-class pauses for Kam.
- **Your NOT-TESTED list is first-class output.**

PROVENANCE:
- Head fe4eed3, the F1/F2 fixes, the class audit and the RD-286 probe figures | S29's READY FOR QA (2) mail 2026-09-03T15:45:40Z in wednesday-agent@agentmail.to | read 2026-09-04
- F1/F2/F3 as originally found, and the pass-17 measurements | /Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/nexusai/reports/2026-09-04-s29-restand-pass17/SUMMARY.md | read 2026-09-04
- The builder's account of the split('\n')[-1] truncation | that same READY FOR QA (2) mail | read 2026-09-04
- The deploy hold (--0000094 serves 9520b8c; caf1fe7 GO withdrawn) | /Volumes/DevMASTER/WEDNESDAY/0_Brain/daily/2026-09-04.md | read 2026-09-04
- Kam's QA-gate order | /Volumes/DevMASTER/WEDNESDAY/0_Brain/learnings/2026-09-01_qa-gate-before-my-verification.md | read 2026-09-04

SELF-CHECK: re-read end-to-end for contradictions | 2026-09-04 01:48
