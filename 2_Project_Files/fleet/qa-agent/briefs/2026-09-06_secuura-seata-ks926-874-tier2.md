# QA Agent Invocation Brief — Secuura/Blockchain SEAT A · KS-926 campaign · PR #874 · TIER 2 (through-code)

**TIER 2 — through-code only, and the reason: this PR is DOCS-ONLY.** One markdown file, no runtime
file, no route, no schema, no config, no migration, nothing deployed. It changes no behaviour
whatsoever. There is no rendered surface and no browser leg. Per Kam's 2026-09-05 tiering ruling,
docs get the through-code half and not the full weight.

**But read this before you scope it down further.** The document's entire value is that its CLAIMS
ARE TRUE, and tonight this exact finding-set produced a measured error rate: **three of the ten
member descriptions handed to seat A were wrong**, and member 10 alone carried THREE successive wrong
mechanisms across three agents (including two from Wednesday) over one sound measurement. So the
pass is not "does the prose read well" — it is **does every claim reconcile with the code it cites,
at this SHA.** That is a through-code pass with teeth.

## Charter (read first, in full)
`/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/QA_AGENT_CHARTER.md`. Findings-only; you
never fix. Boundaries below are hard.

## 1. Target
- Repo: `/Volumes/DevMASTER/!CODING/Secuura/Blockchain` (Platform K).
- **PR #874, head `fe5225f31bb7bd7e6d3466fd6d65a4f35db0af10`, base develop `066cff67554a5bd5398fcc9fb4b9ade422fbbd5b`.**
  Both read by Wednesday with `ls-remote` from Wednesday's own seat in the same action as writing this.
- The file under test: `Blockchain/Dev/docs/KS-926-CHECKS-THAT-CANNOT-FAIL.md`.
- **Work in YOUR OWN clone/worktree, pinned to the literal SHA.** Note from tonight's launcher gate,
  which cost that tester time: **in a clone taken from the local project repo, `origin/develop`
  resolves to the SOURCE's stale local develop.** Pin `refs/qa/base` to the literal `066cff675` and
  use only that.

## 2. Spec / DoD being tested against
The document's own thesis, which is the standard to hold it to:
> No behaviour should be called "guarded" without a cell that goes red when the guard is removed —
> and the cell must assert WHICH CLAUSE judged the input, not merely that the input was judged.
A document about checks that cannot fail must not itself contain claims that cannot be checked.

## 3. Scope — the claims, one at a time
Every one of these is the builder's measurement, not Wednesday's. Verify or refute each **against the
code at `fe5225f31` / `066cff675`**, and say which instrument you used:
1. **The census: 3 reached / 17 unreached `check-*.sh`.** The builder's first re-run said 4/16; it
   caught its own filter (it stripped `#` and not `//`, so a mention inside a `/** */` block counted).
   Re-derive independently. Carry the load-bearing positive control the ticket names: **`check-shared-relink.sh`
   must be REACHED** — expected at `scripts/preflight/preflight.sh:419` now that #870 has merged. If your
   census cannot show that one as reached, your census is wrong, not the tree.
2. **KS-933's exclusion hides 42 test files**, not the 2 its ticket names.
3. **Members 8 and 9** confirmed in the guard source; member 8 reproduced with five fixtures whose
   controls fail independently on both axes.
4. **Member 10:** `ks796:130-137` `vi.mock('../middleware/authenticate')` → passthrough; `wallet.ts:30`
   imports exactly that path; adding `authenticate()` to the route leaves ks796 at **10 passed, 0 failed**.
   **Re-run the tamper yourself.** Restore by INVERSE EDIT and prove it by sha256 — the pre-tamper hash
   is `ee048d4c1bce7cf6292b628931cad6e2458d2c1bf06647be075ed8314c51506b`. Do NOT restore by checkout.
   Note the trap the builder fell into and self-caught: the real middleware is a **FACTORY**
   (`middleware/authenticate.ts:121`, used as `authenticate()` at `:441`/`:489`). Writing `authenticate`
   without the call hands Express a factory where middleware belongs; `next()` never runs, the request
   hangs, and the suite reds on a 5000 ms timeout. **That red proves nothing.** If your tamper reds,
   say WHICH assertion tripped and why.
5. **The PREMISE AUDIT** — the document claims members 1, 4, 5, 6 and 10 have premises strictly WORSE
   than their mechanisms, i.e. fixing the mechanism leaves the premise unstated. **This is the
   document's most load-bearing and least verifiable section. Press it hardest.** For each of the five,
   is the named premise actually unasserted by any cell, and is "worse" defensible?
6. **Every line number the document cites.** It cites many across the launcher, its suite, the guards
   and the tests. A wrong line number in this document is a Minor; a wrong MECHANISM is a Major,
   because this file is about to become the canonical statement of the class.
7. **Internal consistency:** does the ten-member table agree with the premise-audit table and the
   worked examples? Does any member appear with two different mechanisms?
8. **The two correction notes** — the document records that row 6's withdrawal was over-broad and that
   member 10 arrived with two wrong mechanisms. Confirm those notes describe what actually happened
   rather than smoothing it.

## 4. Credentials (POINTER ONLY)
`4_Credentials/.env` in the project. You should not need any: this is a read + local-test pass.

## 5. State-mutation & cleanup
- **Two builder seats are LIVE in this repo right now** — seat A in `worktrees/seat-a`, seat B in
  `worktrees/seat-b`. **Touch neither.** Work only in your own copy.
- No `rm`. Quarantine by rename. Restore any tamper by inverse edit + sha256, never checkout.
- Report the LISTEN set and Docker container count before and after, as previous passes have.

## 6. Output boundary
One mail to Wednesday, subject `[QA -> Wednesday] Secuura SEAT A KS-926 campaign (#874, tier 2)`.
Findings-only; severity yours, priority Wednesday's. **NOT-TESTED at equal prominence to findings.**

## 6a. Evidence class on every finding that recommends an action
As the template requires: the oracle, the measurement, the control, and what you did NOT establish.

## 7. Known-fragile / known-changed areas
- **A control proves the INSTRUMENT RUNS; it does not prove the QUERY CAN MATCH.** Seat B lost a
  finding to this tonight: a grep for `wallet/status` returned 0 because the cells call RELATIVE
  paths, and its `describe` control proved grep ran and therefore agreed with the null for the wrong
  reason. **Where you search a corpus, PLANT the thing you are looking for and find it with the same
  command.**
- **A measurement travels; an explanation of it does not.** Every mechanism in this brief is the
  builder's; TAMPER-E-class greens have carried three wrong explanations tonight. Trust none of the
  prose, including Wednesday's above.
- A red arriving by timeout, crash, syntax error or setup failure is not a red-proof — it is the run
  failing to happen.
- A fresh worktree has no `node_modules`; preflight leg 1 refuses on it. `npm ci` from `Blockchain/Dev`
  is the documented fix, not `--no-verify`.
- Env notes from tonight's passes: darwin, bash 3.2.57, awk (BWK), `core.fileMode` false, `/bin/dash`
  present, `git grep -a` / `git diff -a` for files with NUL bytes.

## 8. Logistics
Wednesday reads your verdict whole and rules. Box: ~30 minutes. If the claim set is larger than that
allows, do items 1, 4 and 5 first and say plainly what you did not reach.

---

PROVENANCE:
- PR #874 head fe5225f31bb7bd7e6d3466fd6d65a4f35db0af10 and base develop 066cff67554a5bd5398fcc9fb4b9ade422fbbd5b | `git ls-remote origin` run from Wednesday's seat (READ verb only) | read 2026-09-06
- the claim set, the census figures, the 42 files, the member-10 tamper and its sha256 restore hash | seat A's READY mail `[Secuura/Blockchain -> Wednesday] READY FOR QA: KS-926 campaign PR #874 @ fe5225f31` 2026-09-06T12:57Z and its two prior mails, all read whole by Wednesday | read 2026-09-06
- the factory-vs-call trap and the passthrough mock | seat A's mail `Member 10 measured` 2026-09-06T12:55:26Z | read 2026-09-06
- the control/plant lesson | seat B's mail 2026-09-06T12:49Z §4, adopted into fleet/specs/brief-standing-lines.md | read 2026-09-06
- the stale `origin/develop` trap in a derived clone | the launcher gate's verdict 2026-09-06T12:18:53Z | read 2026-09-06
- NOT READ by me: the document itself, the guards, ks796, and every line number it cites. I have opened none of them and run nothing — every claim in §3 is the builder's, quoted, and is the thing under test | not read | read 2026-09-06
