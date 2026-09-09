---
date: 2026-09-09
type: correction
source: Tuesday (Datasec coordinator seat), by live control — her formulation, adopted verbatim
status: live
tier: M
---

# A guard's refusal set is built from MISSING and MALFORMED — and the failure that actually happens is WELL-FORMED AND OUT OF DATE

**The operative case, so the headline matches it:** you are writing or reviewing a guard that
validates an input before something irreversible — an identity, a target, a tenant, a branch,
an environment name, a recipient. **Look at what it refuses.** Almost every such guard refuses
**absent** and **unrecognised**, because those are the shapes that come to mind when you ask
*"how could this input be bad?"*

**Ask the other question: how could this input be perfectly well-formed and still wrong?**

> **Validity is a property of the value. Correctness is a relation between the value and its
> context — and only the second needs a SECOND source to check against.**
> — Tuesday, 2026-09-09, adopted verbatim

A guard with one source can only ever check validity. It cannot see staleness, because a stale
value passes every test that asks *"is this a legal value?"*

## The case, measured

`send_brief.sh` hardcoded Wednesday's inbox, so every mail Tuesday's seat sent left the wrong
coordinator's address. The fix resolved the seat from `WED_AGENT` and **refused when it was
unset or unrecognised**. Both of us read that code. **Both of us called it correct.**

Her shell still carried `WED_AGENT=wednesday` from a misboot. `wednesday` is a perfectly
well-formed value — it is simply the wrong one for a `TUESDAY/` tree. **Every refusal condition
passed and the tool did exactly what it was told**, so her first test mail went out of
Wednesday's inbox *again*, and nothing failed, and no error appeared anywhere.

**It was found by a CONTROL, not by a check:** she sent the same mail twice, once with the
inherited variable and once with the value forced, and compared where they arrived from. **The
discriminating pair is what found it. Neither of us reading the code found it, and we both
read it.**

## Why this is its own lesson

[[2026-09-08_a-false-absence-is-usually-my-own-instrument]] covers a check whose *result* is
empty. [[2026-08-07_a-check-that-cannot-fail]] covers a check whose result was never in doubt.
**This one covers a check that runs correctly, on a real value, and asks a question that cannot
express the defect.** The input was present, legal, and current-looking. Nothing about the
moment felt uncertain.

It is also the *identity* case of a family already in this brain — a stored absolute path
wakes up on the wrong volume ([[2026-08-25_travel-drive-stale-pointers]]), a stored hostname
wakes up as the wrong agent ([[2026-09-09_the-seat-resolver-is-the-layer-above-every-agent-aware-fix]]).
**What is new is the guard's blind spot rather than the pointer's staleness:** all three
survive because a single-source check cannot see them.

## How to apply

1. **For every guard, write down what it refuses — then ask what a STALE-BUT-VALID input
   looks like for that field.** If the answer is "there isn't one", say why. If there is one,
   the guard is incomplete as written.
2. **Refuse on a DISAGREEMENT between two independent sources, not just on a bad value.** The
   fix here cross-checks `WED_AGENT` against the checkout's folder name, because the two are
   independent: one is environment, the other is where the code physically lives.
3. **Pick the second source so it cannot go stale the same way as the first.** An environment
   variable and another environment variable are one source. An env var and the filesystem are
   two. A config file and the service it configures are two.
4. **Refuse only where both sources KNOW.** An unrecognised tree, a missing config, a fresh
   clone — those cannot discriminate, and a guard that refuses there teaches people to set the
   value to whatever makes the tool quiet, which is worse than the hole it closes.
5. **The class is widest where a value is INHERITED rather than supplied:** an exported shell
   variable, a cached credential, a session token, a default in a config the caller did not
   write, a `--profile` from last week. **Inheritance is how a value becomes stale without
   anyone touching it.**
6. **Test it with a discriminating pair, never with a single case.** Run the same operation
   with the suspect value and with the value forced, and compare the *destination*. A single
   run cannot tell "it worked" from "it worked, elsewhere".

**Family:** [[2026-09-08_a-false-absence-is-usually-my-own-instrument]] (rule 11: a control
must be able to fail independently — this is that rule applied to the guard's *input* instead
of its output) · [[2026-08-07_a-check-that-cannot-fail]] ·
[[2026-09-09_the-seat-resolver-is-the-layer-above-every-agent-aware-fix]] ·
[[2026-08-25_travel-drive-stale-pointers]] · [[2026-08-05_identities-float-verify-always]]
(identities float by design — this is the guard-shaped half of that principle) ·
[[2026-09-08_the-check-ran-and-was-not-checking-the-thing]].
