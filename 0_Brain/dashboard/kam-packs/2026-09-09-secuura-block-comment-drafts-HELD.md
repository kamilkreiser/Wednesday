---
date: 2026-09-09
type: draft
source: written by the Secuura/Blockchain agent (s159) and mailed to wednesday-agent@ at 2026-09-09 05:16Z; saved here verbatim
status: HELD — not posted
---

# Block comment drafts — HELD, awaiting Kam

**Nothing here is posted.** Four drafts, one per review-stream parent, to go on the tickets
when Kam has read the grouping (pack: `2026-09-09-secuura-review-handover.md`).

⚠ **DRAFT 2 (KS-770) CANNOT BE POSTED YET.** It carries a deliberate `<<< HOLE >>>` where his
second-reviewer answer goes — Peter authored three of that block's six PRs and cannot review
his own. Posting it before he answers publishes a gap in the one field the block exists to fill.

**Why this file exists:** the drafts were mailed rather than left in the agent's pane, because a
pane is not a channel of record. This copy is on disk as well, so neither the seat dying nor an
inbox lookup is between a successor and the work.

# BLOCK COMMENT DRAFTS — HELD, NOT POSTED

Four drafts, one per stream parent. **None is posted.** Release on Kam's word.
⚠ **Block 2's draft has a deliberate hole** — it cannot be posted until Kam answers the
second-reviewer question, and the draft says so at the point where the answer goes.

═══════════════════════════════════════════════════════════════════════════
## DRAFT 1 — for KS-771 (Build, supply chain and release gates) — Peter
═══════════════════════════════════════════════════════════════════════════

## Test block ready — 11 PRs, one pass, all `clean`

**BLUF: every PR in this stream is `clean` as of today. One pass proves all eleven.**

### The one pass
From a clean checkout on macOS:
`scripts/preflight/preflight.sh` -> `scripts/preflight/lockfile-cleanroom.sh` -> `npm run test:migrations` -> `validate-env.sh`
**Wall-clock:** `test:migrations` **~40 s measured** (spins a throwaway `postgres:15`); lockfile-cleanroom minutes; preflight has no baselined figure in the s115 overlay.

### What is in the block
| PR | ticket | state |
|---|---|---|
| #918 | KS-926 | new today — the census + 14 guards wired as preflight leg 14; no review yet |
| #874 | KS-926 | docs: state the family; no review |
| #875 | KS-936 | **approved at head** |
| #879 | KS-945 | **approved at head** (+2 follow-ups Peter states are not blockers) |
| #904 | KS-992 | **approved at head** (+1 follow-up) |
| #891 | KS-418 | **`dirty` -> `clean` today**, head now `721e5b773`; approval no longer at-head |
| #866 | KS-909 | **`dirty` -> `clean` today**, head now `a4f692ad2`, suite 23/0 |
| #887 | KS-961 | head now `cb7a3e3be`; Peter's requested change has landed |
| #903 | KS-991 | reviewed, no approval |
| #916 | KS-993 + KS-1026 | no review |
| #721 | KS-660 | no review |

### The one thing to do
**Run the pass once at the tip of these eleven and give one approval decision for the stream.**
Four carry no review at all (#918, #874, #721, #916); three are already approved and need nothing.

═══════════════════════════════════════════════════════════════════════════
## DRAFT 2 — for KS-770 (API contract and the four platform suites) — Peter + one more
═══════════════════════════════════════════════════════════════════════════

## Test block ready — 6 PRs, one pass, TWO approval decisions

**BLUF: one suite pass proves all six, but three of them are Peter's own and need a different reviewer.**

### The one pass
Regen the spec -> **restart the gateway** (it bind-mounts the yaml) -> Schemathesis `pre-merge` + `spec-auth-conformance.mjs` + Playwright + k6 `test:smoke`.
**Wall-clock, all measured:** Schemathesis pre-merge **13.4 min** (~2,016 cases / 318 ops) · spec-auth seconds · Playwright **3.8 s** · k6 **53 s**.
**k6: read the printed `Status:` line, never `$?`** — the gate exits 0 on a red.
**Schemathesis: record the failing SET and its diff against the develop baseline, never a bare count.**

### What is in the block
| PR | ticket | state |
|---|---|---|
| #808 | KS-663 | **approved at head** |
| #809 | KS-693 | no review |
| #813 | KS-791 | **approval WITHDRAWN in writing and never dismissed — see KS-1035. Do not merge on the badge.** |
| #896 | KS-682 | **authored by Peter** — Playwright slot isolation |
| #899 | KS-971 | **authored by Peter** — observability slot truth |
| #900 | KS-971 | **authored by Peter** — k6 slot isolation, **stacked on #899's branch** |

### The one thing to do
**<<< HOLE — needs Kam's answer before this draft can be posted >>>**
Peter cannot review #896/#899/#900. Under the flow, approval comes from any of the three who is not the author, so this is Kam or Stuart. **Name the second reviewer here.**

**Order constraint:** #900's base is #899's branch — #899 merges first, or #900 rebases onto develop.

═══════════════════════════════════════════════════════════════════════════
## DRAFT 3 — for KS-485 (Platform Security) — Peter
═══════════════════════════════════════════════════════════════════════════

## Test block ready — 14 PRs, one pass, one held item named

**BLUF: all 14 are `clean`. One pass proves the stream; #912 is excluded by name and stays held.**

### The one pass
Akto `test:pre-merge` + the **five Code Security Gates** (`check-production-guard.sh` · `check-coverage.mjs` · `security-audit.sh` · `check-no-default-passwords.sh` · `check-connector-xss.sh`, seconds each) + the touched services' unit suites (auth · originate · api-gateway · security · anchoring) + `npm test -w packages/shared`.
**Akto's ~7-8 min is inherited from another host and unbaselined here (KS-691** — a measured run was 24.7 s / 30.2 s**).** Read an Akto **PASS** as *nothing was reported*, not *nothing is there* (KS-696 / KS-700).

### What is in the block
| PR | ticket | state |
|---|---|---|
| #728 | KS-671 | **approved at head** — one ask: a `403` still reads as a healthy chain |
| #806 | KS-731 | **approved at head** |
| #872 | KS-732 | **approved at head** |
| #720 · #878 · #913 · #873 · #773 | KS-487 · KS-942 · KS-963 · KS-931 · KS-1008 | no review |
| #805 | KS-726 | design question open |
| #799 | KS-764 | Peter posted a correction; no approval |
| #905 | KS-968 | holding on two lines |
| #881 | KS-798 / KS-799 / KS-841 | **CHANGES_REQUESTED at head** |
| #785 | KS-229 | approval **stale** and Peter explicitly holding |
| **#912** | KS-1004 | **HELD — the exception. No GO from its tier-1 gate; the api-gateway `confidence` fix must land with or before it.** |

### The one thing to do
**Run the security pass once and make one decision for the stream, with #912 excluded by name.**

═══════════════════════════════════════════════════════════════════════════
## DRAFT 4 — for KS-772 (S<->K integration contract) — STUART, not Peter
═══════════════════════════════════════════════════════════════════════════

## Test block ready — 1 PR, and it is now unblocked

**BLUF: #880 was this stream's only PR and its only blocker. It is `clean` as of today.**

### The one pass
From Platform S: register-connector -> originate -> anchor -> verify -> erasure by `external_ref` -> re-key. No wall-clock baselined in the overlay.

### What is in the block
| PR | ticket | state |
|---|---|---|
| #880 | KS-577 | revoke-on-rotate + the cutover window. **`dirty` -> `clean` today**, head now `85f8263c2`, security suite **187/0** |

**A single-ticket stream is still a stream** (DEV-PROCESS section 2) — not padded to look bigger.

### The one thing to do
**Run the S-side chain once. The re-key leg is exactly what KS-577 changes**, so the pass Stuart already runs is the pass that proves this block.


---

## STATE AT WRAP

**origin:** #891 `721e5b773` · #866 `a4f692ad2` · #887 `cb7a3e3be` · #880 `85f8263c2` — all four `clean`, all four landed by merge, **zero force pushes all session**.

**Main checkout never written to:** `feature/ks-963-f3-structural-cells` @ `b083c0e1e`, porcelain 0 at boot and now. Five worktrees, all porcelain 0. Rebased branches preserved as `s159-rebased/ks-{909,418,577,961}`.

**Filed:** PR #918 · KS-1035 · KS-1036 · KS-1037. **Posted:** 5 ticket comments (KS-926 earlier, plus today's four). **Held:** 4 block comments.

**Holds observed:** 0 merges to develop · 0 deploys · 0 `--no-verify` · 0 `ALLOW_FORCE` · 0 force pushes · no approval attempted · no message to Peter or Stuart · no extranet post · #813 untouched · nothing deployed, so migration 048 is unaffected.

## FOR KAM, unchanged

**(a)** Block 2's second reviewer — needed before that block's comment can be posted at all · **(b)** whether to seek Peter's re-confirm on #891 · **(c)** the #813 maintainer-dismiss (KS-1035) · **(d)** #811 close-or-refresh.
