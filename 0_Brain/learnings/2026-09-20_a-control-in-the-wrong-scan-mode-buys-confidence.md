---
date: 2026-09-20
type: correction
source: S71 (Datasec/NexusAI), self-reported after its suppression reddened main; the brief that caused it was Tuesday's
status: live
tier: W
---

# A control that runs in a different MODE from the one that will judge you proves less than it appears to — and it is worse than no control, because it buys the confidence to ship

**The lesson, in the agent's own words, adopted verbatim:**

> *"A control that runs in a different mode from the one that will judge you proves less than it
> appears to — and it is more dangerous than no control, because it buys confidence."*

**Executable form:** a control names the **MODE**, the **INVOKER** and the **REF SET** it ran
under. **The mode you verify in must be the mode the judge runs in.** Otherwise it is evidence
about a different instrument, presented as evidence about yours.

## The case

Rescuing an unversioned design document, an agent committed it to a branch. Gitleaks blocked the
commit on two placeholder secrets inside example ATTACK payloads. It handled that **well**: it
called them true positives rather than waving them off, suppressed **by fingerprint, never by
path**, and then — unprompted — **proved the suppression narrow with a canary**: it injected a
fresh secret into the same file, confirmed the scan still caught it, removed the canary, and
verified the file byte-identical. It reported all of that honestly, and it was true.

**Then main went red.**

CI checks out main with `fetch-depth: 0` and runs `gitleaks git .` — a **history scan across every
fetched ref**. The canary had run `gitleaks protect --staged`. History findings are keyed
`COMMIT:path:rule:line`; the suppression was written `path:rule:line`. Correct format for the mode
it was tested in; wrong format for the mode that judges.

**The control passed, and its passing is exactly what made the push feel safe.** No control at all
would have produced more caution.

## Two properties worth keeping on their own

1. **A BRANCH PUSH IS AN ACTION ON THE SHARED BOARD.** A leak on any branch reddens *main*, because
   the history scan sees every ref. The branch was never merged and may never be. Treating branch
   pushes as private is wrong wherever CI scans history — and the coordinator had explicitly called
   the branch "a rescue, not a change". It was not a change to the suite. It was a change to
   main's CI.
2. **Commit before a destructive control.** Running the canary, the agent `git reset --hard`'d with
   its fix still uncommitted and wiped it. It caught this because it **read the number** — "leaks
   found: 2" where clean was expected — instead of assuming the run had worked. Widened:
   **a destructive step runs against a committed tree, or in a scratch clone.**

## The coordinator's half, which is where this actually started

**Tuesday commissioned committing a 99,937-byte file it had never opened**, having measured only
its size and its path. A design document for an SSRF control is the single most likely place in a
repo to contain attack payloads with credential-shaped placeholders. That is
[[2026-08-04_validate-brief-pointers]] exactly: the brief validated that the file EXISTED and never
what it CONTAINED, and what it contained is what broke main.

**Rule: before commissioning a file into a scanned or built repo, ask what the tooling will SEE in
it** — not only whether it exists and where it goes. Same family as
[[2026-09-20_most-of-a-project-folder-is-outside-its-git-repo]] (naming a directory is naming a
behaviour) and the placement error in the same session.

## Why the existing lessons did not catch it

[[2026-08-07_a-check-that-cannot-fail]] asks whether a check CAN fail — this one could, and did,
on its canary. The 2026-09-08 false-absence family asks whether the instrument could return a
false zero — it could not; the staged scan was working perfectly. **Both rules were satisfied.
The control was sound, honest, and pointed at the wrong instrument.** That is a third axis, and it
is invisible to a question that only asks "did the control fire?".

The nearest neighbour is [[2026-08-06_local-proof-is-not-target-evidence]] — a green local proof is
not evidence about an environment that differs by design. This is its sharper sibling: **the
environments need not differ at all; only the INVOCATION MODE needs to.**

## 🔴 THE w=3 ROOT — three of Tuesday's errors in ONE session, and they are one mistake

Recorded here rather than in a fourth file, because Kam's ruling (b) of 2026-09-20 says shrink the
corpus, and a root shared by three instances belongs in one place, not three.

| # | what was specified | the property measured | the property that actually governed |
|---|---|---|---|
| 1 | "put the cells in `__tests__/` or a clearly-marked staging path" | that the path EXISTS and is clearly marked | what **jest collects** there — no `testMatch`, no `roots`, so `docs/` and `qa-reports/` are collected. ~30 un-run cells would have armed. |
| 2 | "the design file belongs in the repo's docs" | its SIZE (99,937 B) and its PATH | what the file **CONTAINS** — two credential-shaped placeholders — and what gitleaks would see. Main went red. |
| 3 | "RD-464 r3 is released by the RD-545 merge" | that the predicate COUPLES them | what the coupling **MEANS** — a necessary condition, not a sufficient one. Two other holds survived. |

**THE ROOT, in one sentence: I specify using a property I measured, and the property that governs
is one I did not.** Existence, size, path and coupling are all cheap to measure, which is precisely
why they are the ones I reach for — and none of them is the property that decides the outcome.

**The failing-test treatment (w≥3):** before any instruction that names a PATH, a FILE or a
DEPENDENCY, write down the one sentence *"this will behave the way I expect because ___"* and fill
the blank with a property I have actually read — the config that governs that path, the contents of
that file, the clause that states that dependency. **If the blank can only be filled with
existence, size or location, I have not checked the governing property and the instruction is a
guess wearing a measurement's clothes.**

All three were caught by the receiving agent, not by me. That is the system working, and it is not
a substitute for the blank being filled.

## How to apply

1. Before trusting any control, write down the **exact command the judge runs**, and run that.
   `protect --staged` vs `git .` vs `dir .` are three instruments wearing one tool's name.
2. When a suppression, ignore-file or allowlist is involved, **check its key format against the
   mode that will read it** — history findings, staged findings and directory findings are keyed
   differently by the same tool.
3. **A control's report names its mode.** "I proved the suppression narrow" is not a claim; "I
   proved it narrow under `gitleaks protect --staged`" is, and it is the version that would have
   exposed this before the push.
4. This generalises past scanners: test runners with different collection roots, linters in
   `--fix` vs check mode, CI matrices that differ from local, `npm ci` vs `npm install`.
