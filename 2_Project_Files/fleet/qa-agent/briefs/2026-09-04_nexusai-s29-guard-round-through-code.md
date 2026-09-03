# QA Agent Invocation Brief — Datasec/NexusAI, S29's GUARD + DOC round, STATIC THROUGH-CODE

## Charter (read first, in full)
`/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/QA_AGENT_CHARTER.md`

## 1. Target
- **Client / Project:** `Datasec / NexusAI`
- **Mode:** **STATIC through-code, read by SHA. NO browser needed and none expected** — this round
  moved **zero rendered pixels** and that claim is itself one of the things to falsify.
- **Subject:** **`5a7c6b5`**, against the previous head **`7e5faa9`**.
- **Repo (read-only):** the NexusAI project tree. **Zero writes.** If you run the jest gate, run it
  from a copy by SHA in your own scratchpad, never in the tree.
- **Surfaces `:3068` `:3072` `:3073` `:3075` `:3076` `:3077` are UP and must be LEFT ALONE.**
  `:3077` serves `7e5faa9` and is the source of the frames now in front of Kam — **do not restand,
  restart or repoint anything.**
- **Production?:** nothing is deployed. `caf1fe7`'s deploy GO is WITHDRAWN and no finding of yours
  re-issues it.

## 2. The claims to falsify — all the builder's (S29)
- **"NOT ONE RENDERED PIXEL MOVES — the non-comment diff across all of `static/css` is empty."**
  **This is the load-bearing claim** — Kam's frames were cut from `7e5faa9` and are being shown to
  him as current *because of it*. **Re-derive it yourself.** Note the stated method is a *non-comment*
  diff; check that the comment-stripping cannot itself hide a real declaration (this project has
  already been bitten by a stripper that emptied a file, and by a guard defeated by its own prose).
- **`npm run verify` PASS 1399/1399 across 82 suites**, up from 1395/81. **The +4 and the +1 suite
  should reconcile exactly to the new guard's cases.** If they do not, that is the finding.
- **The new `4.16`/`text-muted` corpus guard works and is not merely banning a digit.** The builder
  red-proofed it **by case count** — four historical wordings caught one each, an adjacency case, and
  **the two corrected wordings that ship today produce ZERO**. Verify the guard can fail AND can
  pass for the right reason. **Its two scopes are deliberate** (sentence-scope for attribution,
  paragraph-scope for dated history) — test that the paragraph scope cannot be abused by a date in a
  neighbouring paragraph, which the builder says it fixed after finding exactly that.
- **`docs/BRAND.md:493` and `:488` corrected; `:216` deliberately left** (dated, past tense); and
  **`:493`'s second figure `4.17` deliberately KEPT** because it is `--nx-danger-emphasis` and still
  current. **Check that 4.17 claim** — it is the one number in this round nobody has independently
  verified.
- **"Today THREE accents still fail on the raised ground, not seven"** — `info-emphasis` 4.32,
  `success-emphasis` 4.46, `danger-emphasis` 4.17, computed through the generator's own `derive()`.
  **Re-derive all ten** rather than the three, so the *denominator* is measured and not inherited.

## 3. Scope — and the standing hypothesis
**Assume one more instance exists.** This project has produced, in three consecutive rounds, a guard
that could not SEE, a guard green on the wrong AXIS, and a tamper that did not tamper. **The pointed
question: does this round's guard contain any of those three?** In particular — **the builder's own
best catch was that its first tamper removed one date marker and left a second in the same
paragraph, so a guard that does not fire and a tamper that does not tamper looked identical.**
Check that the shipped red-proof cases do not have that shape.

**Out of scope:** any rendered/browser check, the demo, any deploy, any Azure resource, the other
eight tabs, and `.nx-sus-cls` (deliberately recorded-not-fixed, RD-288 — do not re-file it).

## 4. Credentials
**None, and none needed.**

## 5. State-mutation & cleanup
**Exclude-and-report-only.** Scratch in YOUR scratchpad. **NEVER `rm`** — build each attempt in its
own `mktemp -d` and abandon the old one; guard every expansion with `${VAR:?}`. If a fixture is
costing real budget, **report the affected checks as NOT RUN with the blocker named**.

## 6. Output boundary (fixed)
**Findings, reports and recommendations ONLY.** No code, tests, tickets, config or PR comments.

## 7. Known-changed — do NOT re-report as new
- `.nx-sus-cls`'s 60 dark pixels — **recorded knowingly**, RD-288 filed with the fix written down.
- The empty state (`.nx-sus-empty`, `.nx-sus-empty-span`) — **RD-289 filed**, four members that
  three passes could not reach. Do not attempt to create a zero-row dataset.
- RD-286's pixel diff demoted and gated; the structural geometry probe ranked first.
- RD-285's gradient explanation is filed as a **HYPOTHESIS**, not a diagnosis. Leave it that way.

## 8. Logistics
- **Time-box:** one bounded pass. Depth over breadth — **the zero-pixel claim first if you cut**,
  because Kam is being shown frames that depend on it.
- **Report to:** `projects/nexusai/reports/2026-09-04-s29-guard-round-through-code/SUMMARY.md`
  under your own tree, then mail Wednesday a summary. **Wednesday reads the FULL report.**
- **Escalation:** `wednesday-agent@agentmail.to`, QUESTION subject.
- **Your NOT-TESTED list is first-class output. State the counting UNIT and SETTLE POINT for any
  population figure.**
- **Severity only. Priority is Kam's and Wednesday's call, never yours.**

PROVENANCE:
- The seven queue items, `5a7c6b5`, the zero-rendered-pixel claim and its method, 1399/1399 across 82, the three-not-seven accent finding, and the guard's two scopes and red-proof cases | S29's QUEUE COMPLETE mail, `wednesday-agent@agentmail.to`, 2026-09-03T17:35:53Z | read 2026-09-04
- The previous head `7e5faa9`, its gate figures 1395/1395 across 81, and the surfaces to leave alone | QA pass 19 SUMMARY.md, read in full | read 2026-09-04
- RD-288 / RD-289 / RD-286 / RD-285 dispositions and the `.nx-sus-cls` ruling | /Volumes/DevMASTER/WEDNESDAY/0_Brain/daily/2026-09-04.md | read 2026-09-04

**NOT re-derived by Wednesday:** both SHAs are copied from S29's mail, a channel with an author;
Wednesday ran no git command in the NexusAI tree. **Resolve each on your own seat and say so if
either does not.** Wednesday has NOT established the blast radius of running the jest gate from a
scratchpad copy — **establish it before acting**, and if it would write into the tree, do not run it.

SELF-CHECK: re-read end-to-end for contradictions | 2026-09-04 03:44
