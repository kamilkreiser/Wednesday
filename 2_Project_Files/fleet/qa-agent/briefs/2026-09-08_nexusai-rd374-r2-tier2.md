# QA RE-GATE — Datasec/NexusAI **RD-374 ROUND 2** `rd-374-f2-guard-coverage-s46` @ `7c10437`. **TIER 2.**

## Scope — the delta only
    5e6077e   the round-1 head, GO-with-findings on 2026-09-08   — already gated, NOT your subject
    7c10437   THE SUBJECT.  Range 5e6077e..7c10437 = ONE commit, ONE file, 186+/43-
              __tests__/auth-gate-fail-closed.test.js   — NO product code
    NOT main — frozen, RD-367, ~251 behind. Nothing merged, nothing deployed. **You may not merge.**

**Round 2 of this class, and round 1 was GO-with-findings, not a NO GO** — the two-NO-GO cap is not
engaged. Judge it on its merits.

Round-1 report (read the findings it raised, then check they are closed):
`/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/nexusai/reports/2026-09-08-rd374-tier2/report.md`

**Independently verified by Wednesday before this brief** (`ls-remote` from the NexusAI checkout, a
read verb): `rd-322-root-guard-vacuity-s45` is still `432617a` and `rd-361-round4-s45` is still
`731aa6e`. **No gated branch moved. Confirm it yourself anyway** — it is the claim everything rests on.

---

## 🔴 THE BUILDER ASKED FOR THIS AGAINST ITSELF, AND IT IS YOUR FIRST JOB
**The builder did NOT implement the remedy Wednesday specified for G-1a, said so unprompted, and
named the exact reason its own evidence cannot settle the difference:**

> *"My negative control passes under both and cannot tell them apart on its own. The gate should
> confirm which one is actually in the file."*

**Wednesday's specified shape was a NAME HEURISTIC** — *treat any computed key whose identifier
matches `/^AUTH_ENFORCED/` as the key.*
**What the builder says it implemented is a BINDING RESOLUTION** — resolve the computed key against
a proven binding: the module's own exports derived **by value from the real module** (so the set is
measured, not named), plus a local `const`, plus one re-alias hop.

**These two fail in OPPOSITE directions, and that is why the distinction is not pedantry:**
- a **name heuristic** produces a FALSE POSITIVE on a binding called `AUTH_ENFORCED_ANYTHING` that
  does **not** hold the key, and a FALSE NEGATIVE on any binding holding the key that is **not**
  named that way;
- a **binding resolution** does neither, but is only as good as the bindings it can actually follow.

**So: read the implementation, and then BUILD THE ARM THAT DISCRIMINATES.** The builder's arm table
cannot, by its own admission. Two arms settle it and neither exists yet:
1. **A binding NAMED like the constant but holding something else** — e.g.
   `const AUTH_ENFORCED_MODE = 'somethingElse'` used as the computed key. **A name heuristic flags it
   (false positive); a binding resolution leaves it green.**
2. **A binding holding the key under an unrelated name** — e.g. `const zzz = 'authEnforced'` used as
   the computed key. **A name heuristic misses it; a binding resolution catches it.**
**Report which behaviour the file actually exhibits.** If it is the heuristic, Wednesday's remedy
shipped with the two holes the builder described and the finding is NOT closed.

## Also on G-1a — the "by value from the real module" claim
The builder says the export set is **derived from the real module by value**, so it *"picks up a
second export without being edited"* — today exactly `['AUTH_ENFORCED_KEY']`.
**Verify that is what the code does, not what the comment says.** Concretely: does the cell `require`
the real `authEnforcement` module at test time and read its exports, or is the set written down?
**Then prove the claim:** add a second export holding the same value, and confirm the detector picks
it up **without the test being edited**. Restore after. If the set is hard-coded, the sentence is
wider than the code — the exact defect this branch exists to fix, one register down again.

## Q-2 and Q-3 — closed by the mechanism, or incidentally?
The builder found two shapes while proving the fix: **Q-2**, a local `const` of the literal; **Q-3**,
a renamed destructure. Both now RED. **Establish they are caught by the resolution mechanism itself
and not by some unrelated detector that happens to fire** — mutate the resolution path specifically
and confirm Q-2 and Q-3 go green again while T-MB2 (the literal-key control) stays RED. A fix that
passes for a reason other than the one claimed is this file's own recurring family.

## G-1b — the detector was fixed, not the sentence
The builder chose to fix the detector and proved R-2 (`const wfs = fs.writeFileSync; wfs(...)`)
green→RED **in `backend/jsonStorage.js` deliberately** — the file with no object-literal second net,
which was the point of the round-1 finding. **Confirm the proof site is that file**, that an alias of
`readFileSync` stays green (the anti-over-fire control), and that the docblock sentence now matches
what the detector does.

## G-2a / G-2d — the trap was DECOUPLED rather than ordered, and the vacuity risk moved
Wednesday told the builder to land the two together so the tree would not go red on a correct change.
It did that **and removed the dependency**: the regression arm now asserts a property of the
TECHNIQUE against a six-line synthetic fixture, and the spans derive from the old regex's own match
ranges — *"used when present and asserted over nothing when absent, with a synthetic arm that always
runs so the cell cannot go vacuous."*

**"Asserted over nothing when absent" is the sentence to interrogate.** That is a vacuity path by
construction, and the synthetic arm is the only thing standing between it and a cell that passes
because it checked nothing. **Prove the synthetic arm ALWAYS runs** — including when the spans are
empty — and prove the cell can still FAIL in that state. Reproduce both of the builder's numbers:
after cleaning all three stray prose comments, OLD `5e6077e` = 1 failed / 36 passed and NEW = 37/37;
and reverting `codeOnly` to the regex on NEW = 2 failed. **A cell that cannot go red when the spans
are empty is a check that cannot fail.**

## G-2b — the correction, and the formulation to verify is IN the file
Three strays, not two: `:1251` sat inside the 1097→2062 bogus span, so the broken instrument's own
match list had already swallowed it. The builder's rule, which Wednesday has adopted fleet-wide:

> *A census taken with the broken instrument is silent about precisely what the breakage hides.
> Count the CAUSE, never the damage.*

**Confirm that reasoning is in the docblock and not only in its mail**, and that the corrected counts
(three strays; **four** call sites for the named `stripComments`, not three; five for `serverCode()`)
are the ones in the file.

## The claims to re-derive rather than accept
- **PASS 2191/2191 across 113 suites**, jest exit 0. Re-run it.
- **Cell count unchanged at 37**, which is why `scripts/verify-expected-counts.json` is untouched —
  **the diff stat shows one file, so confirm no other suite moved.** Re-derive counts by
  **name-diffing cells**, never by trusting a total.
- **No product code in the diff.** One file, `__tests__/auth-gate-fail-closed.test.js`. Verify.

## Evidence rules
Positive control on the instrument **opening and closing** · **every mutation asserted PRESENT before
its result is read**, restored after, tree clean between · **matched pairs so exactly one variable
moves** · **read every RED and say why it is red** — a parse error, a throw, or a pre-existing
condition answering first is **not** a detection · **NAME THE FRAME** in any completeness claim ·
**FOUND / TESTED / HOW with the controls named under HOW** · **state what you did NOT test**.
**Stop any server you start and prove the port reads 000.** No `az`, no registry, no demo, no
staging. Work in your own clone or worktree — **the project checkout is not yours to write to.**

## Verdict
**GO · GO-with-findings · NO GO**, with severities. A guard real but narrow is **GO-with-findings** —
say so rather than failing it for a **stated** limit. **If the implementation turns out to be the name
heuristic rather than the binding resolution, that is a NO GO on G-1a specifically** — not because
the heuristic is useless, but because the record would then say something the code does not do.
Report to **Wednesday**. Write the report under
`projects/nexusai/reports/2026-09-08-rd374-r2-tier2/` and **NAME THAT PATH IN YOUR MAIL** — a verdict
mail on this fleet arrived with a zero-byte body last night, and the report on disk is what saved it.

RULED BY KAM, NOT YET IN AN ARTEFACT:
- (none for RD-374): Kam's last panel input was 21:00 on 2026-09-07 and nothing since bears on this branch. His week-scoped grants (merge on Wednesday's word once the gate passes, deploy, board judgement calls, through Sunday 2026-09-13) change nothing about this pass, and Datasec holds NO production grant.

PROVENANCE:
- Head 7c10437, the range being exactly one commit, the single-file stat, and that rd-322 is still 432617a and rd-361 still 731aa6e | `git -C /Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/2_Project_Files ls-remote origin` and `rev-list --count` / `diff --stat`, run by Wednesday in the same action as writing this brief - read verbs only, Wednesday did not fetch | read 2026-09-08
- The builder's own account of what it implemented, its Q-1/Q-2/Q-3/NEG arm table, the 2191/2191 claim, and its sentence that its control cannot discriminate | the builder's round-2 mail 2026-09-07T14:56:54Z, DKIM-verified - relayed, NOT re-measured by Wednesday; discriminating it is this gate's job | read 2026-09-08
- G-1a, G-1b, G-2a, G-2b, G-2d as round-1 findings with their severities | /Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/nexusai/reports/2026-09-08-rd374-tier2/report.md - the round-1 gate's own report | read 2026-09-08
- That Wednesday's specified G-1a remedy was a name heuristic | /Volumes/KK_T9_External_HDD/WEDNESDAY/2_Project_Files/fleet/s46_rd374_findings.md - Wednesday's own sent mail, its own words, not the builder's characterisation | read 2026-09-08

SELF-CHECK NOTES: the two discriminating arms are specified concretely rather than as "check which one"; the vacuity path the decoupling introduced is named as a probe rather than accepted as a mitigation; the NO GO condition is stated as a record defect, not as a claim the heuristic would be useless.
SELF-CHECK: re-read end-to-end for contradictions | 2026-09-08 01:02
