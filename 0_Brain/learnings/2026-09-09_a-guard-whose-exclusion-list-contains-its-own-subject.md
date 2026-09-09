---
date: 2026-09-09
type: correction
source: Tuesday pushed a corrupt decisions.json straight through the hook built to stop exactly that
status: live
tier: M
---

# Read a guard's EXCLUSION list before trusting the guard — the file class it skips is usually the one it was written for

**The operative case, so the headline matches it:** you are relying on a guard — a
pre-commit hook, a linter, a scanner, a CI gate, a backup job — and you are about to treat
its silence as evidence. **Before you do, read its exclusion list out loud and ask: is the
thing I am worried about ON it?** An exclusion list is a claim that a class of file cannot
contain the defect, and it is the one part of a guard nobody ever tests.

## The case, measured

The repo's `pre-commit` hook exists to stop conflict markers reaching origin. Its own
header cites the incident that created it: *ledger w=5 — a note with markers reached
origin twice in one day.* Its scan line read:

    git diff --cached --name-only --diff-filter=AM | grep -Ev '\.(json|png|jpg|pdf|xlsx|gif)$'

**So it skipped `.json` — and `decisions.json` and `chat_log.json` are the only two files
in this repo that have ever carried conflict markers into origin.** Six times by
2026-09-09, including the 2026-09-08 incident that nearly erased Kam's rulings.

Proven by doing it: commit `beb32de7` pushed a `decisions.json` carrying
`<<<<<<< Updated upstream` at line 6630 to `origin/main`, with the hook installed,
executable, and running. **An unparseable `decisions.json` makes `decision_queue.sh` and
`send_brief.sh` refuse for BOTH seats** — so it blocks the fleet and puts the principal's
rulings at risk, which is precisely the blast radius the hook exists to prevent.

## Why it survived, and it is not carelessness

`json` was sitting in a list that reads unmistakably as a **binary/asset skip**:
`png|jpg|pdf|xlsx|gif`. In that company it looks like housekeeping. **The list's SHAPE
disguised a semantic decision as a performance one** — and the author of a guard is the
person least likely to re-read the clause that makes their guard cheap.

## How to apply

1. **When you write or adopt a guard, name its subject and then read its exclusions
   against that subject.** *"This stops conflict markers. Which files have actually had
   conflict markers?"* If any are excluded, the guard is decoration for the case that
   matters. One question, asked once, at the moment of writing.
2. **An exclusion is a CLAIM needing evidence, exactly like a scope word**
   ([[2026-08-16_classification-is-the-field-that-grants-authority]]). *"JSON cannot
   contain conflict markers"* is checkable and false. Write down why each exclusion is
   safe, or drop it.
3. **Test the exclusion, not just the detection.** A red-proof that plants the defect in
   an INCLUDED file proves nothing about the excluded ones. The proof that matters here
   was planting markers in a `.json` and watching it be refused.
4. **Prefer excluding by what a tool CANNOT read (true binaries) over what you assume is
   safe.** `png|jpg|jpeg|pdf|xlsx|gif|zip|dmg` is a claim about encoding; `json` was a
   claim about content, and content claims are where this lives.
5. **Where the fear is false positives, test the fear instead of honouring it.** The
   worry here was legitimate JSON containing `=======`. A positive control settled it in
   one command: `json.dump` escapes newlines, so **no line inside well-formed JSON can
   begin with a marker unless it is one** — and a clean JSON whose string *value* contains
   `=======` passes. The fear was real, the risk was not, and only running it separated
   them ([[2026-09-08_a-false-absence-is-usually-my-own-instrument]] rule 11 — a control
   must be able to fail independently).
6. **A guard that lives in an untracked, machine-local path is not fixed when you fix it.**
   `.git/hooks/pre-commit` does not travel; pulling the tracked master does NOT install it.
   Every seat copies it into its own `.git/hooks/`, and **the fix is not delivered until
   each one has** ([[2026-09-05_a-relayed-ruling-is-delivered-only-when-it-is-in-the-artefact]]
   pointed at a mechanism instead of a ruling).

**Family:** [[2026-08-07_a-check-that-cannot-fail]] (rule 1 — *what would make this check
fail?* For a JSON file, nothing could) ·
[[2026-09-08_the-check-ran-and-was-not-checking-the-thing]] (it ran on every commit and was
blind to the file that mattered) ·
[[2026-09-07_a-census-complete-over-a-frame-that-is-not]] (complete over every extension
except the one) · [[2026-08-09_an-enforcement-you-must-arm-is-not-one]] (in-path
enforcement, with a hole in the path).
