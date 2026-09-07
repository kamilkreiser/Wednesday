# QA GATE — Secuura #892 ROUND 3 @ `34a48abc6`, TIER 2 (through-code). **The cap was SPENT; Kam authorised this round himself.**

**Round 3 of 2 exists because Kam ruled it** (`secuura-892-cap-spent-blocker-open` => `round3-narrow`,
2026-09-07 19:56): *"Authorise ONE narrow round 3 — F1 and F2 only, both one-liners."*
**There is no round 4 without his word.** If this comes back NO GO, the closed instances do not
silently ship — it goes back to Kam.

**TIER 2 is round 2's own call, not a fresh one of Wednesday's.** Round 2's verdict **kept the tier at
2 and corrected only the SEVERITY CEILING**, with a formulation Wednesday accepted verbatim:

> *"F1 does not skip testing. It silently changes the identity every wired suite runs as, to a
> less-correct one, and reports success. The output is not 'less coverage'; it is coverage that
> asserts the wrong thing while looking healthy."*

**In a repo with no CI, where these suites are the only instrument, "tests the wrong thing and
passes" is worse than "does not run."** Weigh F1 at that ceiling.

## 1. Target
- **Head `34a48abc6`**. Change set from the **PR files API**; resolve the merge base yourself.
- **F1 and F2 ONLY.** Round 2's F3 (the strict flag failing OPEN on every spelling but literal `"1"`)
  is already closed. **Anything carried beyond F1/F2 is outside the round Kam authorised — report it
  as a finding, do not gate it as scope.**
- **A GO here is not a merge**; #892 merges on a Wednesday GO after this verdict.

## 2. F1 — quarantine, not skip. **The claim to attack is a POSTCONDITION.**
**The builder's account:** on rejection an existing `generated/actors.json` is now MOVED to
`actors.superseded-<provisionedAt>.json` — moved, never deleted; an existing quarantine is never
clobbered, since overwriting one would be deleting it under another name. **The guard stays in the
FILESYSTEM, not in a reader** — `actor_manifest.py` parses the JSON directly, so a TypeScript-side
staleness check would not have covered it.

**THE THING TO PRESS, and it is the seat's own keeper from round 2:**
> *"a non-write is not a removal, and that sentence is an assumption about the filesystem rather than
> a property the code establishes."*

So: **withholding a manifest is a NON-WRITE. Does this fix actually REMOVE a stale drifted manifest,
or does it only decline to write a new one?** Round 2's F1 survived precisely because a stale
manifest outlives a non-write. **Drive the live shape, not the intended one:** the round-2 instance
had `actors.json` seeded at **07:57** and `actors.rejected.json` at **08:50** — the REJECTED run 53
minutes NEWER — so the newest pass was refused and every consumer still resolved the older file.
**Build that state and prove the fix moves it.**

Second half, and round 2 established it: **the surviving manifest's seed was the shape the TEST
SCRIPT writes** (`presuite-test-72460`), so the consumers were pointed at accounts a test suite
created for itself. **Prove that cannot survive this fix either.**

Also: **`generated/` is gitignored, so a clean `git status` is NOT evidence the manifest is clean.**
Do not use it as one.

## 3. F2 — the set was right in SHAPE and wrong in MEMBERSHIP
**The builder's account:** round 2 moved the gate from a position to a command set and carried
`quality` across unexamined. `quality` dispatches with `run_tests=True`, and
`runner/quality_gate.py` runs *"only when the API is reachable — the integration suite"*. So rather
than inverting one exemption, **every remaining member is now justified against what it dispatches
to** — setup/install build the environment, update-deps upgrades venv deps, report reads from disk,
`quality:static` skips both pytest suites. `_run_pre_suite`'s docstring claimed `quality` drives no
stack; corrected.

**Attack the MEMBERSHIP, one member at a time.** A set justified in prose is not a set justified by
dispatch. **For each remaining member, follow it to what it actually dispatches to** — the round-2
defect was exactly a member carried across without that walk. Round 2's F2 also named
**`run.py quality` as EXEMPT while running 389 live-API cells**; confirm that is now resolved and not
merely re-worded.

## 4. The 13 new cells — and the one thing the builder deliberately did NOT run
**Four red-proofs claimed, four distinct failure sets, each restored byte-identical:** `quality` back
in the set → 3 failed/2 passed · the set emptied → 2 failed/3 passed · quarantine made a no-op → 6
failed/2 passed (survivors are exactly the controls) · delete instead of move → 4 failed/4 passed.
**Re-run them. Four distinct sets is a strong claim — check each tamper reds the cells it should and
no others.**

**The shell suite runs against a temp directory ON PURPOSE**, and the reason is a real defect:
`pre_suite.test.sh` creates five real accounts on any stack answering on `:6882` and overwrites the
real manifest (**KS-973 item 3**). **It probes its own driver first**, because without that "the
function returned nothing" and "tsx never started" are the same empty string — which is how its first
version reported four false failures. **That probe is a control; prove it can fail.**

**NOT run by the builder, and said rather than skipped silently: `pre_suite.test.sh`**, because it
writes to the `:6882` stack whose **data is untrusted**. **Do not run it against `:6882` either.**
If you can stand your own stack from the repo's provisioning path, that is the honest way to cover
it; if you cannot, say so at equal prominence.

## 5. Environment
**The shared local dev stack is STALE BY DESIGN** (121 commits behind at 17:19) and **`:6882` holds
UNTRUSTED DATA**. Build your own from the repo's provisioning path, or state precisely what a stack
of that age cannot prove. **If you build a database, confirm each migration BY NAME** — the #892
round-2 gate established that `run-migrations.sh` reports `applied=N failed=0` for migrations it
**SKIPPED**, so the runner's own summary is not evidence.

## 6. Bounds and report
Findings-only, **never fix**. **NO CI** — you are the only independent instrument. **Say what each
cell MOCKS.** **Search the board before filing and say what you searched** — by SYMBOL, PATH or ERROR
STRING, never by your own phrasing. **Never write into the builder's checkout.** **Never delete —
quarantine.** **A GO is NOT a deploy GO.**

**GO / GO-with-findings / NO GO on the first line.** **F1 gets its own heading**, and say plainly
whether the BLOCKER is closed — Kam authorised this round on the understanding that both remaining
fixes are one-liners, and **round 2 already proved that framing understated it once.** If it is still
open, say so first; that goes back to Kam, not into a merge. **NOT-TESTED at equal prominence**, and
**record what was FOUND, what was TESTED, and HOW — including the controls** (Kam, 2026-09-07 18:56).
Mail `wednesday-agent@agentmail.to`, subject
`[QA -> Wednesday] Secuura KS-969 / #892 round 3 (tier 2)`.

## 7. PROVENANCE
- Head `34a48abc6`, the F1/F2 accounts, the four red-proof sets, the not-run cell | the Secuura seat's own mail, `wednesday-agent@agentmail.to` 2026-09-07T10:21:32Z, read whole in this action — **the builder's claims, not re-derived by Wednesday** | read 2026-09-07
- The tier-2 rating and the severity-ceiling correction | round 2's own verdict, quoted in the 2026-09-07 daily note — **the gate's call, carried, not re-decided** | read 2026-09-07
- The 07:57 / 08:50 manifest timestamps and the `presuite-test-72460` seed | the seat's live measurement reported to Kam's panel 19:42 | read 2026-09-07
- Kam's authorisation for this round | `decision_queue.sh show secuura-892-cap-spent-blocker-open`, ruled `round3-narrow` 2026-09-07T19:57 | read 2026-09-07
- `run-migrations.sh` reporting `applied=N failed=0` for SKIPPED migrations | the #892 round-2 gate's F3, as recorded in the 20:12 handover — **Wednesday has NOT read the verdict's own text** | not read
