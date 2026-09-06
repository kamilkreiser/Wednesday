# SEAT successor brief — Secuura/Blockchain, 2026-09-07 09:4x. ONE narrow round, Kam-authorised.

## BLUF
You are a fresh seat. **s144 wrapped cleanly at 23:33Z** — read its handover,
`5_Project_History/HANDOVER-s144.md`, in your own tree.

**Kam has authorised exactly ONE narrow round 3 on #876, regression only** (card
`secuura-ks930-cap-vs-regression` => `one-more`, 09:38 AEST). **This is an exception to his own
two-NO-GO cap, granted because the residue is a REGRESSION rather than a known gap.** Do the
regression and nothing else.

**Your predecessor already measured the fix and deliberately did NOT apply it.** It is on **KS-956** as
a comment. Read that before writing a line.

## THE ITEM — the whole round
**#876 head `3047bcb1dd852561d8ae3267b02f0056f881c999`**, base develop `306d0db923183f3b62b053f0242549e37bdf362c`.

**The defect, in s144's own words** (it diagnosed itself at wrap so Kam could rule on the true size):
> It is **six** version-suffixed spellings, all EXEMPT at head and BLOCKED at base: `node-22`,
> `node22`, `node.22`, `node_22`, `nodejs-22`, `node-lts`.
> **Cause, mine:** the boundary class `[^A-Za-z0-9_.-]` puts `-`, `.` and `_` INSIDE the word set, so a
> version suffix detaches the token. Fifteen lines above, `base_is_js_runtime` at `:367-369` already
> reads `^(node|nodejs|bun|deno)([0-9._-]|$)` — it allows the suffix explicitly. **I read that function
> while writing the fix and still did not mirror it.**

**The candidate fix it measured and left unapplied:**
```
shipped:    (node|nodejs|bun|deno)([^A-Za-z0-9_.-]|$)
candidate:  (node|nodejs|bun|deno)([0-9._-]|[^A-Za-z0-9_.-]|$)
```
It reports this closes all seven suffixed spellings **and keeps the false-positive control exempt** —
`nodes`, `anode`, `nodex` — which is why a boundary class was chosen in the first place.

**Verify that yourself; do not take it.** Then:
1. **One cell per spelling**, and a cell for each false-positive control.
2. **One red-proof**: restore the shipped class and confirm exactly those cells red and nothing else.
3. **Run it at THREE SHAs** — base `306d0db92`, the current head, and your fix — so "closed" is a
   measured transition. **The base column is what makes a regression a regression.**
4. **Leg 13 must stay green on the real 25-file tree** (it was: rc 0, 4 copy / 21 re-install).

## WHAT IS *NOT* IN THIS ROUND — Kam ruled "regression only"
The round-2 verdict also names three claim-level defects: **F6** a hand-written census wrong at every
SHA in the series, **F5** a clause the author names as unable to fail and leaves in, **F4** a "CONTROL"
cell that cannot fail for the reason its name asserts. **Ticket them, aggregated as one logical path
(a suite whose own claims are false), and do not fix them here.** The verdict is in your inbox,
forwarded verbatim, subject begins `FORWARDED: the #876 round 2 verdict`.

## HOLDS
Nothing merges. Nothing deploys. Demo box never touched. **Fix round goes on #876's own branch.**
**#884 has PASSED its re-gate and is awaiting Kam's merge word — do not push to it.** #882 is READY and
never gated; #885 round 1 is unre-gated. **Push to none of them.** Never delete — quarantine. Restore
every tamper by inverse edit verified with sha256, **then RE-RUN**. Count first; never truncate a list
you will call complete. **A relayed claim carries its author's sentence including its hedges.**

## NOTE ON THE COORDINATOR
Wednesday is rotating to a fresh seat as you boot. **Your plan confirmation may wait up to ~10 minutes
for the successor — that is expected, not silence.** Start item 1 meanwhile; it needs no ruling.

RULED BY KAM, NOT YET IN AN ARTEFACT
- secuura-ks930-cap-vs-regression: "Authorise ONE narrow round 3, regression only" -> **must land in
  this round's PR and in KS-956's comment thread.** That is your work.
Older, none an action for you: secuura-ci-billing (wait) · secuura-agent-github-identity (Kam org
action) · secuura-dependabot-triage (Peter's repo) · secuura-ks229-disclosure-mailbox (later) ·
secuura-ps-759-760-merge-owner (Platform S, out of scope).

PROVENANCE:
- The six spellings, the cause, and the candidate fix | s144's wrap mail 2026-09-06T23:33Z, quoted verbatim — Wednesday has verified none of it | read 2026-09-07
- Kam's authorisation | card secuura-ks930-cap-vs-regression => one-more, his panel message 09:38 AEST | read 2026-09-07
- #876 head and develop SHAs | git ls-remote origin run from Wednesday's own seat in the same action as writing this line | read 2026-09-07
- Whether the candidate fix actually keeps the false-positive controls exempt | NOT ESTABLISHED by Wednesday — that is your item 1 | read 2026-09-07

SELF-CHECK: re-read end-to-end for contradictions | 2026-09-07 09:39
