# FOR RECORDS: delta gate of the resolution commit of OXPd 2, WP4.2 (part), head ce38c25 on main c56f3f3

Only what THIS commit adds. The second gate's list (`2026-11-21_B1819_verify/FOR-RECORDS.md`) stands as written; nothing
below was filed, sent or decided by the gate.

## 1. State

- **Delta gate: GO WITH FINDINGS at ce38c25e08a4c9f6f1cec55214e51a60f75a4f5f** (no Blocker, no Major). The second gate's
  landing condition (its finding L, section 1 of its list: "Resolving it needs ONE new commit") is MET by this commit: a merge
  of main c56f3f3b into the branch whose only change against the three-way merge is the solution file, byte-equal to the
  block (sha256 df48c25f...), tree 6fc18eaa1e7356cf394c3fe2c47bfa1003fafb9c.
- The branch now holds three commits beyond main (9f4238ad, ec75619e, ce38c25e, the last a merge). Land it by this folder's
  `landing.txt` (head-pinned squash at ce38c25e), with this folder's `pr-body.md`.
- The hosted code scan has NOT run on this code; it runs on the pull request and is the authority.
- WP4.2 and `OXPD2-18` stay OPEN after the landing (unchanged). The server does not reference the library (unchanged).

## 2. Added by this commit

1. **Text: two sentences of the second gate's pull-request body became untrue** ("285 tests on both legs", "Two commits").
   Re-worded in this folder's `pr-body.md`; the squash texts did not change.
2. **Records: the builder's `proofs.py` P8 (identity) cannot fail on a wrong identity** (it reads the clone's config and its
   control compares a constant). For the next resolution or proof kit: compare with the checkout's config and plant an
   identity in the control commit.
3. **Records: local and hosted NEUTRAL-SCAN counts differ after a local merge** (316 against 312): the merge leaves 4
   unreachable objects in the seat's clone. A fresh clone reads 312, equal to the hosted run. Expected, not a fault.
4. **Records, for gate kits:** a gate that publishes behind the closed proxy must pass `-p:NuGetAudit=false` to `dotnet
   publish` too (its implicit restore otherwise fails `NU1900`); this gate's first two publishes did.
5. **Records (RELAYED from the seat's STATUS, not measured by this gate):** a `VBCSCompiler` of another lane's gate folder
   (`/private/tmp/b1824-gate`) was alive at 09:44 after its job; the seat left it alone.

## 3. Ticket states

- No ticket was read or written by this gate.
