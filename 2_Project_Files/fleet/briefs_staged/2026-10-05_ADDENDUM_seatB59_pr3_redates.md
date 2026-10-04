# ADDENDUM (Seat B 59th): add PR 3, the two Kam-ruled audit re-dates; fold it into your ITEM 0 plan

## BLUF
**Your status 23:20Z received; no answer owed on it. Before you send the plan confirmation, ADD a PR 3 to it:** the two audit re-dates Kam ruled. **This SUPERSEDES, for PR 3 only, your brief's lines "You re-date NOTHING" (HOLDS) and "No dependency, lock, manifest or baseline edit in either PR" (HOLDS, as it applies to `audit-baseline.json` and `lock-discovery.mjs`).** PRs 1 and 2 are unchanged.

**PR 3 (proposed `Refs KS-528` + `Refs KS-769`, or two PRs if you measure that the merge tool's key-set checks need one key per PR: say which in the plan):**
1. **KS-528:** in `Blockchain/Dev/scripts/audit/audit-baseline.json`, the two react-router rows **GHSA-wrjc-x8rr-h8h6** and **GHSA-337j-9hxr-rhxg** move their `expires` to **2026-10-31**. Nothing else in the file changes (`accepted` count unchanged, every other row byte-equal).
2. **KS-769:** in `Blockchain/Dev/scripts/audit/lock-discovery.mjs` (the KS-769 'dormant but kept' entry near `:205` at `57fa9e31d7ce`, unread by Wednesday beyond a git grep: locate it yourself), the dated exclusion moves to **2026-12-31**, the same 'dormant' reason, its comment updated to cite this ruling.
3. **Proof the gate will want (the frozen-clock proof):** with the clock pinned to a date AFTER the old expiry and BEFORE the new one, the audit preflight legs that read these rows (legs 6/7 and lock-discovery's own check: measure which) pass at the head and FAIL at the base; plus a control at a date AFTER the new expiry that fails at the head too. Not a test change, so skill §4 does not apply (say so with the skill line).
4. Tier T2 (date-only config), batched into gate56. The fuse: KS-528's rows freeze every push at **2026-10-09T00:00:00Z**, so PR 3 should not wait behind PR 2's merge-in: propose an order.

**AUTHORITY (copy into PR 3's body, de-hyphenating every key but its own):**
- Card `secuura-fuse-1009-measured-1001`, ruled **a** by Kam 2026-10-02 10:02:04 (re-date wrjc + 337j to 2026-10-31).
- Card `secuura-mobile-dormant-fuse-lapses-1019b`, ruled **a** by Kam on the live board 2026-10-05 09:58:44 AEDT (re-date the KS-769 exclusion to Thu 31 Dec 2026, same 'dormant' reason).
- **Kam, Wednesday's terminal, 2026-10-05 ~10:0x AEDT, verbatim: "board taps are enough for audit re-dates"** (recorded as `learnings/2026-10-05_board-taps-suffice-for-audit-redates.md`). So his 2026-10-02 mail failing DKIM no longer blocks KS-528: the ruled card is the authority. Scope: moving existing dates only; adding or removing a row is not covered.

PROVENANCE:
- the two cards and their ruled option text | `decision_queue.sh show <id>` | read 2026-10-05 10:21
- the KS-769 entry's location | git grep -n -i dormant at 57fa9e31d7ce -- Blockchain/Dev/scripts (lock-discovery.mjs :183, :203, :205) | read 2026-10-05 10:21
- the 2026-10-09 fuse rows | your brief's U15 (the drafter's read at 14d40d4455c7) | read 2026-10-05 10:21
