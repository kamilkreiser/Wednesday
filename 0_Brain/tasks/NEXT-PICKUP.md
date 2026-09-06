---
date: 2026-09-06
type: pickup
source: replaced wholesale by the 22:1x seat at its 70% handover (23:40)
status: live
supersede: replace this file wholesale at the next pickup; do not append
---

# NEXT PICKUP — both seats productive, FIVE PRs open, gate queue is the bottleneck; Kam's queue = 1 card, nothing waits on him

**Kam, verbatim, both still operative:** (1) 20:19 *"change your boot script for the rest of the week
to boot in opus 5 rather than fable. we are burning through credits a little too quickly"* — the
launcher is pinned, `doctor.sh` WARNs after 2026-09-13. (2) 20:19 *"keep pushing the secuura agent to
polish the platform to a ready state."* His last panel message was 19:31; **0 new from him since.**

## 🔴 FIRST ACT: the gate queue. Two panes free, four subjects waiting.
No tester is running. Launch in this order (wrappers: copy `state/launch_qa_secuura_seatb_ks733.sh`,
python `str.replace` NEVER `sed`, and red-proof rc 6 / rc 7 before arming — both branches, every time):
1. **`a0ad0a084e7ecdd772d106740a283f738ccdadf7` (#876, KS-930) — TIER 1 re-gate.** F-5's keyword
   upper-casing, the whole F-6 exemption AND Finding 2's new single-write cell are UNGATED. **Re-read
   `ls-remote` before you brief it — this head moved TWICE while it sat in a queue** (`af954c691` →
   `ff7704135` → `a0ad0a084`), and seat A mailed the correction unprompted both times.
2. **`6f7885602` (#874, KS-926) — TIER 2, ROUND 2 OF 2 under Kam's cap.** Seat A asked to be told
   findings as a CLASS rather than item by item; hold to that.
3. **#875 (KS-936)** and **#878 (KS-942)**, seat B's, both tier 2.
**Briefs live in `fleet/qa-agent/briefs/`; the last four are the pattern.**

## THE FLOOR
- **Secuura develop `306d0db923183f3b62b053f0242549e37bdf362c`** — seat B's #877 merge LANDED, so
  **TEN merges tonight**. Verify it from objects yourself; this seat read it from `ls-remote` at 23:40
  and did not yet `cat-file` its parents. **Re-read `ls-remote` before trusting any SHA in this file.**
- **seat A `%130` (s141b)** — KS-945 FILED and Finding 2's fifth cell already in `a0ad0a084` (suite
  39 → 40); on its table next.
- **seat B `%129` (s140e)** — merging #877, then **F5 P1**, then the bounded KS-486 sweep, then build.
- **NexusAI PAUSED** on Kam's 17:01 word. **NO testers running.**
- Panes closed this seat, listeners 24 → 24 every time: `%126 %119 %121 %127 %128 %131 %132 %133`.

## 🔴 F5 IS THE HIGHEST-VALUE OPEN QUESTION IN THE FLEET
From #877's tier-1 verdict. Four path spellings — `/api/users/me//mfa/disable`,
`%6Dfa`, `mfa;x=1`, `mfa%2Fdisable` — **dodge EVERY path-scoped gateway limiter** (all seven at
`index.ts:939-1016`, `/api/auth/mfa` included). The spec gate falls through by design
(`:1047 if (!matched) return next();`), and **express's own prefix strip normalises the dodge away
AFTER the limiter was skipped** — driven: 429 on the canonical spelling, **200** on `//mfa/disable`.
**PRE-EXISTING, not #877's defect.** The tester refused to rate it and was right to:
> *"If auth 404s them, F5 is a curio. If auth serves them, F5 is a Blocker on the whole limiter
> layer, not just MFA."*
**Ruled P1; its first act is the experiment** — local booted gateway + auth in seat B's own copy,
never the demo box, four spellings driven, canonical as the control, severity set by the result.
**And KS-733 must not close as if the 450x gap were fully shut.**

## OWED, in order
1. The four gates above.
2. **#876 and #874 do not merge until their own heads are gated** — `af954c691` and `fe5225f31` both
   passed, and both branches have moved past those SHAs.
3. Seat B's F3+F4 ticket from #877 (the parity cell compares only `windowMs`/`max`; the gate is purely
   relative). **#876's F1+F3 is already filed as KS-945** (P2, Backlog, related to KS-926) with the
   fail-closed inversion as its design — five spellings re-measured by seat A with a blocking control:
   `npm add`, `npm it`, `npm install-test`, bare `yarn`, `pnpm add` all rc 0 FALSE CLEAN; `pnpm i`
   caught only by accident and `mynpm i` a FALSE BLOCK, both from the missing left word boundary.
4. Kam's card `secuura-demo-kam-admin-default-password` — OPEN, default HOLD. Nothing on the demo
   identity moves.

## 🔴 THE MISTAKE TO NOT REPEAT — a gate's subject is a SHA
Twice tonight a builder pushed to a branch mid-gate and the verdict described a head the branch had
moved past (#874, then #876 — the second on Wednesday's own instruction, given without naming the
live gate). **Any instruction that could cause a push NAMES the gates running against that branch;
new work goes on a new branch.** Now a standing line. And **re-read a verdict's own target line
against `ls-remote` before merging on it** — that is what caught the second one.

## TONIGHT'S LEDGER AGAINST WEDNESDAY, one line each
🔴 a forward titled "the KS-720 verdict" that carried the LAUNCHER verdict (a message id reused, the
true subject printed into the body by Wednesday's own script and never compared) · 🔴 **two
OVER-WITHDRAWALS in ten minutes**, the second two minutes after filing the lesson for it — one nearly
destroyed a live finding, one removed a working fix; diagnosis: both were urgent relays, so the rule
went into the standing lines · 🟡 **three overstatements of a relayed claim**, the third dropping a
builder's hedge into a QA brief as the thing to press · 🔴 the gated-subject miss above.
**Every one was caught by an agent, and the agents were right every time.**

## STANDING OPERATIONAL NOTES
A card add is ALWAYS its own tool call (now gated: `card_id_gate.sh` in `send_brief.sh` +
`chat_reply.sh`) · a wrapped pane closes only with no queued tap and no spinner · **never
`fetch`/`merge-tree --write-tree`/`worktree add` in an agent's checkout** · SELF-CHECK is the
canonical sentence + `| $(date)` with NOTHING between · **EMPTY OUTPUT IS NOT A RESULT — read the
exit status; `bash -n` on a zero-byte file returns 0** · a relayed claim carries the counterpart's
sentence VERBATIM INCLUDING ITS HEDGE · a red that proves nothing is as blind as a green that proves
nothing · a hash proves the bytes, only a run proves the file still works · **`send_brief.sh`'s
DQ_PREFIX now covers `Secuura/Blockchain-B`** (it did not, so seat-B briefs skipped the ruled-cards
gate) · Linear: an issue fixed under an ALREADY-ARCHIVED ticket **can never be marked Duplicate** —
close it Done with the fixer's id, SHA and PR in the comment TEXT, and say why · the two daily notes
are ~700 KB: read the newest seat block, the rotation block and this file, never whole.
