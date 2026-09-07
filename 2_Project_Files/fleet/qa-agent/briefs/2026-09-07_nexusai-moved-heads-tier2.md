# QA GATE — Datasec/NexusAI **TWO MOVED HEADS**. `731aa6e` and `690bed9`. **TIER 2.**

## Why this pass exists — a GO names a head, and both heads moved after their GO
Two branches carry tier-1/tier-2 GOs at commits that are **no longer their heads**. The deltas are
small and both were built to Wednesday's commission, but **a verdict describes the commit it was taken
on, and neither of these commits has one.**

    rd-361-round4-s45   GO at f93730c   HEAD 731aa6e   delta: the F-B/F-A/F-D/F-E work · claims PASS 2187/2187
    rd-322…             (separate gate, already running — NOT in scope here)
    rd-148-round2-s45   GO at ea4d229   HEAD 690bed9   delta: the N-4 cell fix · claims PASS 2176/2176

**Base each diff on its own GO'd commit** — `f93730c..731aa6e` and `ea4d229..690bed9`. **NOT main**
(~251 behind). **Two subjects, two verdicts; neither gates the other.** Through-code only — neither
delta has a rendered surface.

Nothing is merged and nothing may be merged by you. **Kam's two GitHub answers gate all three merges
regardless of what you find.**

---

## SUBJECT 1 — `731aa6e`: the census guard was rewritten on an AST
The previous guard's `stripComments()` did `line.replace(/\/\/.*$/,'')` — **and `https://` contains
`//`** — so it corrupted 18 of the 80 files it read and **deleted any writer sharing a line with a URL
before counting it.** That was F-B, found by the tier-2 gate at `f93730c`.

**It is now acorn + acorn-walk over an AST.** Write positions are found structurally:
`setSetting('authEnforced', …)`; an `AssignmentExpression` onto a member named `authEnforced`
(**every operator**, so `??=` and `||=` are covered where `=(?!=)` was not); and a `Property` keyed
`authEnforced` inside a `writeFile`/`writeFileSync` argument.

**🔴 THE QUESTION: does the AST guard actually see what the regex could not, and does it now MISS
anything the regex caught?** A rewrite that fixes one blindness and introduces another is the failure
this whole class keeps producing.
- **Re-run the matched pair yourself:** `M-B2` (additive bulk write, no URL) must be **RED**, and
  `M-G2` (**the same write, URL earlier on the line**) must now be **RED** — it was GREEN under the
  regex. The builder also re-ran the OLD predicate against M-G2 and got `bulkWrites = 0`, which is
  F-B demonstrated rather than described. **Confirm that contrast.**
- **Then look for what the AST misses that the regex caught.** Ask it of the three structural shapes
  above: a write reached through a helper; a re-exported `setSetting`; an aliased binding; a spread
  that carries the key; a key written as a computed literal `['authEnforced']`.

**THE FRAME WIDENED — check the widening, not just the claim.** From `backend/**` to **everything
tracked except `__tests__`** — the builder says **148 tracked `.js`/`.mjs`/`.cjs` that ship**. That
closes three bypasses the previous gate found outside the old frame (one directory up, a `.mjs`, a
repo-root file). **The `__tests__` exclusion is ASSERTED, not assumed** — a new cell reads the
Dockerfile and requires that no `COPY` line mentions `__tests__`. **Verify that cell can fail**: make a
`COPY` line mention `__tests__` and confirm it reddens.

**THE KNOWN LIMIT, stated by the builder with a measurement — verify the measurement, not the
sentiment:** the guard covers **syntactic** write positions. A **dynamic** write (`settings[k] = v`
with `k` a variable) needs dataflow, and it reports **256 computed assignments in the tree**, so
asserting zero is not available. **Re-derive that 256 over a frame you name.** If it is materially
different, the limit is stated wrongly and that is a finding.

**F-D and F-E, in scope as regression only:** the control cell is renamed **"F-2 INSTRUMENT
LIVENESS"** — confirm its title now matches what it can prove, and that the F-B case is a permanent
cell inside it. The new **additive** bulk-write cell must leave both writers in place so `bulkWrites`
is genuinely evaluated (the old `M-B` converted `:3349`, so jest stopped at `setSettingWrites` 2→1 and
never reached it).

**One thing left deliberately:** `stripComments()` is **still in that file** for the WIRING cells. The
builder's reasoning is that a URL on the line cannot hide what those cells count. **Rule on that.** If
it can, the broken helper is still load-bearing somewhere and that is a finding.

---

## SUBJECT 2 — `690bed9`: the N-4 cell
The RD-148 gate found *"the new STRUCTURE cell does not guard the risk it appears to guard"* — a check
that cannot fail, inside the suite built to stop exactly that. This is its fix.

**THE QUESTION: can the cell now fail, and does it fail for the risk it NAMES?** Tamper the structure
it claims to guard and confirm red; then confirm it stays green under an unrelated change. **A cell
whose title and whose assertion disagree is the defect, not the assertion alone.**
Counts: 2164 → 2176 claimed. **Re-derive by name-diffing the cells, never by trusting a total.**

---

## BOTH SUBJECTS — evidence rules
Positive control on the instrument, **opening and closing** · **every mutation asserted PRESENT before
its result is read**, restored after, tree asserted clean between · **matched pairs so exactly one
variable moves** · read every hit before counting it · **NAME THE FRAME** in any completeness claim ·
**FOUND / TESTED / HOW with the controls named under HOW** · **state what you did NOT test.**

**Housekeeping:** **stop any server you start and prove the port reads 000.** No `az`, no registry, no
demo, no staging. **Work in your own clone or a worktree — the builder's checkout is READ-ONLY**, and
note it has handed over, so nothing should be moving under you.
*(Incidental, flagged and NOT yours to fix: `git worktree list` prints ~120 prunable entries pointing
at `/Volumes/DevMASTER/…`, a path that no longer exists. Noise, but it makes that command useless for
seeing what is checked out. Some are the QA project's own. Do not prune them in this pass.)*

## Verdict
**A separate verdict per subject**: GO · GO-with-findings · NO GO, with severities. A guard that is
real but narrow is **GO-with-findings** — say so rather than failing it for a **stated** limit.
**Say plainly which of the two, if either, you would ship.**

Report to **Wednesday**. Write the report under
`projects/nexusai/reports/2026-09-07-moved-heads-tier2/` and **NAME THAT PATH IN YOUR MAIL** — a
verdict mail on this fleet arrived with a zero-byte body tonight and the report on disk is what saved
it.

PROVENANCE:
- Both heads and their GO'd bases | `git -C <NexusAI>/2_Project_Files ls-remote origin` run by Wednesday - Wednesday's read, not yours | read 2026-09-07
- F-B's cause, the AST rewrite, the widened frame, the 256 computed assignments, the retained stripComments | the builder's mail 2026-09-07T13:03:10Z, DKIM-verified - relayed, not re-measured by Wednesday | read 2026-09-07
- F-B/F-A/F-D/F-E as findings | /Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/nexusai/reports/2026-09-07-rd361-f2-census-tier2/report.md | read 2026-09-07
- N-4 as a finding | /Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/nexusai/reports/2026-09-07-rd148-round2-tier1/report.md | read 2026-09-07

SELF-CHECK: re-read end-to-end for contradictions | 2026-09-07 23:20
