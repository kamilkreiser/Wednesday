# Secuura / Blockchain — the review, ready to hand over

**Built 2026-09-09 by the Blockchain agent (s159), verified by Wednesday. Nothing has been
sent to Peter or Stuart. Nothing is published on their tickets yet — that waits on you.**

---

## FOUR CALLS, none blocking each other

**1. Name the second reviewer for Block 2.** Peter authored three of its six PRs (#896, #899,
#900) and cannot review his own. Under the flow's own rule that is **you or Stuart**.
*Default if you say nothing: Blocks 1, 3 and 4 go out and Block 2 waits.*

**2. Ask Peter to re-confirm #891 — a re-approve, not a re-review.**
<https://github.com/Secuura/Distributed_Secuura/pull/891>
The sole delta is a merge of `develop`; his review comment is untouched. See "the one carried
cost" below for why it needs doing. *Default: nobody asks him, and #891 sits with a stale
approval.*

**3. #813 — a maintainer needs to DISMISS the stale approval.**
<https://github.com/Secuura/Distributed_Secuura/pull/813>
Peter withdrew it in writing and said he could not retract it himself. Until someone
dismisses it, every instrument reads the PR as approved and clean.
*Default: it stays as it is — and stays a trap.*

**4. #811 — close it, or refresh it.** A status document written for Peter on 2026-09-04 and
never sent. This exercise supersedes it. *Recommendation: close. Default: it stays open and
stale.*

---

## 🔴 THE TRAP, IF YOU READ NOTHING ELSE

**Do not merge #813 on "approved + clean".** Peter approved it at 14:52:21Z and **withdrew
that approval in writing at 14:56:21Z**, four minutes later. Nobody dismissed it, so:

| instrument | reads #813 as |
|---|---|
| the reviews endpoint | `APPROVED`, `commit_id == head.sha` → **at-head** |
| the search index | matches `review:approved` |
| `mergeable_state` | `clean` |
| **Peter's own words** | **withdrawn, holding for complete systemTest evidence** |

Wednesday confirmed both of his comments directly on Linear KS-791, independently of the
agent's report. Filed as **KS-1035**.

**The count should not be flattened into one bucket.** The index says 10 approved. Of those:

- **#813 — withdrawn outright.** The only one where merging contradicts a human's stated
  refusal.
- **#785 — stale** because its head moved on its own.
- **#891 — stale** because of an action we took deliberately today, for good reason.

---

## THE FOUR BLOCKS — all runnable for the first time today

A block is the largest set of PRs that **one test pass** proves. The human runs the pass once
and gives one decision for the stream.

### Block 1 — Build, supply chain & release gates · parent KS-771 · **Peter**
**11 PRs, 11 clean.** Both of this morning's dirty PRs cleared.
**The pass:** clean checkout → `preflight.sh` → `lockfile-cleanroom.sh` → `npm run
test:migrations` → `validate-env.sh`. *`test:migrations` ~40 s measured; lockfile-cleanroom
"minutes"; preflight itself has no baselined figure.*
**He does:** run it once at the tip of the eleven, then one approval decision for the stream.
Four of the eleven carry no review at all; four are already approved.

### Block 2 — API contract & the four platform suites · parent KS-770 · **Peter, except three**
**6 PRs, 6 clean — blocked on call 1.**
**The pass:** regen the spec → **restart the gateway** (it bind-mounts the yaml) → Schemathesis
`pre-merge` **13.4 min / ~2,016 cases** + `spec-auth-conformance.mjs` (seconds) + Playwright
**3.8 s** + k6 `test:smoke` **53 s**.
⚠ **k6: read the printed `Status:` line, never `$?`** — the gate exits 0 on a red.
⚠ **Schemathesis: record the failing SET and its diff against the develop baseline, never a
bare count.**
**Order:** #900's base is #899's branch — #899 merges first, or #900 rebases.

### Block 3 — Platform Security · parent KS-485 · **Peter**
**14 PRs clean, with #912 excluded by name** (NO GO from its tier-1 gate; its api-gateway
`confidence` fix must land with or before it).
**The pass:** Akto `test:pre-merge` + the five Code Security Gates (seconds each) + the touched
services' unit suites + `npm test -w packages/shared`.
⚠ **Akto's ~7–8 min figure is inherited from another host and unbaselined here** (a measured
run was 24.7 s). **An Akto PASS means nothing was reported, not that nothing is there.**

### Block 4 — S↔K integration contract · parent KS-772 · **Stuart**
**1 PR: #880 (KS-577).** It was the block's only PR and its only blocker; it landed today.
**The pass:** from Platform S — register-connector → originate → anchor → verify → erasure by
`external_ref` → re-key. **The re-key leg is exactly what KS-577 changes**, so the chain he
already runs proves it.
*A single-ticket stream is still a stream — not padded to look bigger.*

### The exception, stated rather than hidden
**#811** — one docs file, no ticket, a five-day-old status snapshot. No test pass proves a
stale snapshot, so it fits no block. See call 4.

### Not a block: the dependabot ten
#572 #574 #575 #579 #635 #636 #637 #638 #639 #649 — no single platform pass proves a set of
unrelated version bumps. They want their own batching round.

---

## WHAT LANDED TODAY TO MAKE THIS POSSIBLE

Four PRs were **dirty** and could not be reviewed. Every route to fixing that ran through a
force push — which is one of your reserved classes, and which the repo's own hook refuses.

**It never had to come to you.** A fourth route worked: merge `develop` **into** each branch
rather than rebasing onto it. A merge is a fast-forward, so no force was needed and no history
was rewritten.

**#891** `3c07157a2` → `721e5b773` · **#866** `9e4aebd04` → `a4f692ad2` ·
**#887** `bb0502c80` → `cb7a3e3be` · **#880** `47b2b60f2` → `85f8263c2`

**Zero force pushes. Zero `--no-verify`. PREFLIGHT 13/13 on every one. All four `dirty` →
`clean`.** *These SHAs are the agent's `ls-remote` read, relayed — Wednesday holds no GitHub
identity for this repo and did not re-derive them.*

**#918** was also opened for KS-926, whose work had been sitting on origin since 11:4x with no
pull request at all.

### The one carried cost, and it is call 2
Merging `develop` in moves the head, so **#891's approval is no longer at-head**. The record
survives and the approved commit is still a reachable ancestor — a force push would have
destroyed both. Net: a dirty PR whose approval was never actionable became a clean PR whose
approval needs one click to re-confirm. Better, but not free.

### Also filed
**KS-1035** the withdrawn-approval blind spot · **KS-1036** the review-stream overlay covers 57
of 114 active tickets while the process doc says "nothing left over" · **KS-1037** the
no-force-push rule exists **only** in `.githooks/pre-push` and in no document in the repo.

---

## PASTE-READY, once you have made call 1

*Short by design — the detail is on the tickets, which is your own rule.*

**To Peter:**

> Kamil's side is ready for review and it is grouped into three test blocks rather than a list
> of PRs — KS-771 (11), KS-485 (14) and KS-770 (6). Each block names the one pass that proves
> it, so it is three runs and three decisions rather than thirty-one. KS-770 has three PRs you
> authored; [REVIEWER] will take those. One small thing: #891 needs a re-approve rather than a
> re-review — the only change is a merge of develop, your comment is untouched.

**To Stuart:**

> One for you on the S↔K side: KS-772, a single PR (#880, KS-577, revoke-on-rotate). The S-side
> chain you already run proves it — the re-key leg is exactly what it changes.

**Not included deliberately:** #813. Nothing goes to Peter about it until the stale approval is
dismissed, or the message hands him a contradiction.
