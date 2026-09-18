---
date: 2026-09-18
type: correction
source: "Self-inflicted, 10:0x seat: I refilled Ornith's queue with 4 inputs built straight from ticket descriptions (no night/briefs/<id>.md). KS-1190 and KS-1222 both failed A4 RED-FIRST — the test was green at the untouched tip, so it proved nothing. The runs that PASS (KS-1229, KS-1237, both 7/7) were all built from hand-written 100+ line briefs."
status: live
supersedes: ""
tier: W
---

# Ornith is free; the BRIEF is the cost — a brief-less input cannot red-prove

**The lesson:** The local model's run costs nothing, so the temptation is to fill its queue fast.
**Do not.** `build_input.sh` will happily build an input from a bare ticket description, and that
input will fail `A4 RED-FIRST` almost every time — the model writes a test that is green before the
fix as well as after, which proves no defect. **A queue line without a `night/briefs/<id>.md` behind
it is not work, it is a wasted round and a misleading FAIL.**

**Context:** Ornith idle is a standing-rule breach (Kam 2026-09-18 09:16: the local agent works
constantly), so I refilled the queue in minutes: six candidates through `build_input.sh`, four built,
queued, runner started. Mechanically correct — the tier check ran, `product=` pins were right, the
touched-file sets and `tsc` all passed. But **two of two finished runs failed on A4**, and
`candidates.md`'s own header had already said what I skipped: *"read it, read the file at the tip,
**write `night/briefs/<id>.md`**, then queue it."*

The briefs behind the passing runs are ~115 lines and carry: the file read WHOLE at the tip with its
blob hash, exact line numbers with the current text quoted, the MODE (test-only / product+test), the
tamper the cell must survive, the exact hunk placement, and the failure mode of the previous round.
That is Claude work, and it is where the time actually goes.

**This reframes Kam's 09:18 question** (*where are the Secuura tokens going — can the local agent do
the QA work?*). The answer given at 09:20 was gates. It is truer to say: **the local model removes
the cost of WRITING the fix, not the cost of SPECIFYING it.** A stronger local model does not change
that until it can read a file at the tip and derive the red-first cell itself.

**How to apply:**
1. **Never queue an input whose `build_input.sh` output says `prompt source: the ticket description
   (no night/briefs/<ticket>.md)`.** That line is the warning; treat it as a refusal.
2. **Feeding Ornith is brief-writing, not queue-filling.** Budget accordingly: a handful of good
   briefs beats a full queue of brief-less ones, which return FAILs that look like model weakness and
   are not.
3. **A FAIL on A4 RED-FIRST is a BRIEF defect until proven otherwise** — do not spend the one allowed
   rebrief re-running the same brief-less input.
4. **Delegate the brief-writing** — reading a file at the tip and deriving the cell is exactly a
   subagent's job, and Kam's 2026-09-16 grant covers spinning them up.

**Related:** [[2026-09-14_ornith-runs-at-night-in-the-downtime-a-standing-rule]], [[2026-09-18_the-boot-spec-outgrew-the-context-window]], [[2026-08-03_mental-model-not-source-of-truth]]
