KS-1316 ks781 LEG F: a guard DEFINED but never called inside the parser continuation still reads guarded true (over-reports)
state In Progress

## BLUF

Pre-existing limit of LEG F's guard walk, recorded by the tier-2 gate on PR #1248 (KS-1143 GF-2, merged `fa25c9b10fb4`). **A guard that is DEFINED but never CALLED inside the parser's continuation still reads** `guarded: true`**.**

This **over-reports**, which is the **unsafe** direction: the leg says something inspects the parsed body when nothing does. It is the same asymmetry KS-1143's own GF-1 was about, one step further in.

## Mechanism

GF-2 moved the walk's start from the whole wrapper body to the parser call's **continuation** — the function-valued arguments of the parser call. Inside that continuation the walk still hits on a **call node whose callee name is a known guard**. It does not establish that the call is reached: a guard call sitting in a branch that never executes, or bound and shadowed, is indistinguishable from one on the path.

Not introduced by #1248 — the predicate it replaced had the same property over a wider region, so GF-2 narrowed the region without changing this. Recorded so the remaining looseness has a name.

## Relationship to what is already open on KS-1143

KS-1143 stays In Progress for the **indirect-invocation false negative**, which is the *opposite* direction (under-reports: a continuation passed by NAME is not followed, so a genuinely mounted guard reads unguarded). **This one over-reports.** Two different directions, two different risks; they are not the same defect and should not be closed by one change without saying which each fix addresses.

## Done when

- [ ] a fixture where the guard call inside the continuation is unreachable reads `guarded: false`, **or**
- [ ] a line in the file records why reachability is deliberately out of scope for a text-level walk, so the limit is stated rather than latent

## Board search before filing

Literal match over **1,305 issues (includeArchived) and 3,677 comments**: `CONT-DEFERRED` -> 1 (KS-1143, this finding's own record) · `parserContinuations` -> **0** · `defined but never` -> 1 (KS-1143) · `never called` -> 17 total / 5 open, each read and none this subject (KS-1291 a stale comment, KS-1185, KS-843, KS-1143 itself). **Searched those four terms, 0 open hits for this defect.** Controls: `readYaml` -> 8 hits, fires; `zzz-nonexistent-token-l6-control` -> 0.

## Provenance

Tier-2 gate `QA/Secuura-batch1243`, non-blocking, recorded at the merge of #1248.

Refs KS-1143
