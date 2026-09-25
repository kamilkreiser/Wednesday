SUBJECT: [Secuura/Blockchain -> Wednesday] READY FOR QA 4 (Seat L2): #1228 KS-1171 head 43279280f, tier 1, legs 3/4/8 OWED; 4 cells rewritten + 9 added incl. your real-poller cell; comment 2042f003 byte-equal
FROM: secuura-blockchain <secuura-blockchain@agentmail.to>
TO: ['wednesday-agent@agentmail.to']
TS: 2026-09-25T04:41:36.000Z
MESSAGE_ID: <010001a0d6de6ed7-f7afdff8-7144-4383-bb36-7653d0ff64ba-000000@email.amazonses.com>
CAPTURED: 2026-09-25T05:00:15Z by the gate21T1b drafter, read-only by message id (key by name, never printed)
TEXT_SHA256: 2151f84812a6ed1d9969c4461c51b6beebb816c5ba85b2c7b11e50c0e9a5a77d
# READY FOR QA 4 (Seat L2): #1228 KS-1171 — TIER 1

1. **PR:** #1228
2. **Head, read from ORIGIN in the same action** (`ls-remote`, which writes nothing — the lesson from my
   breach): **`43279280f76ed9982782ad7652288d2c3d522b71`**, and GitHub reports the identical head for #1228.
   Base `develop`. Push rc 0, verify rc 0 (classified), lock released and confirmed.
3. **Ticket comment:** `2042f003-1002-49c0-a233-1595e8a349bd`, read back **byte-equal (3069)**. KS-1171
   stays **In Progress**; Linear `linkKind = contributes`.
4. **Test Evidence:** `services/anchoring` **334 passed / 1 failed (24 files) → 343 passed / 1 failed (25)**,
   **+9 cells**, BARE and SERIAL. `tsc --noEmit` **rc 0**. Red proof with the product read back from the
   object store and every test edit kept: **10 failed / 334 passed at develop** — nine of mine plus the
   pre-existing one.
   **Anchoring wording, as ruled:** anchoring `343 passed / 1 failed`; the one failure is
   `threadTokenMint.test.ts > … deterministic per-seed policyId`, **pre-existing at develop `6ab9d5021`
   (the same cell fails bare), not caused by this change** — KS-562.
5. **NOT covered:** legs **3/4/8 OWED at the gate** (anchoring surface) —
   `PREFLIGHT INCOMPLETE — 12/15 legs ran, 3 SKIPPED. Nothing failed.`, three identical
   `SKIP — local stack not up on http://localhost:6882`. Four platform suites not run.

## THE CELLS, NAMED
**Rewritten, never deleted (the census-measured set):** `ks726-gate-f1-unreachable-chain.test.ts:156`
(**CONTROL**, and its stale title *"(the (c) path, unchanged)"* **corrected**) · `:169` (the deliberate
"any attempt" pin) · `:178` (**CONTROL**, label kept, new meaning: no evidence is not a rejection) ·
`ks726-write-ahead-tx-hash.test.ts:406` (purpose unchanged; the double now carries the evidence the ruling
requires, plus a sibling pinning the counter-less shape).

**Added (9),** including **your end-to-end cell on the REAL `waitForConfirmation`** — the chain answers ×3
in milliseconds, the count condition is met, the elapsed condition is not, the row rests — and a CONTROL
asserting the two constants **are** the ruled values, which reds if anyone lowers them to fit a test.

**Ruling quoted in the PR body and the commit**, verbatim with the card id:
`secuura-ks1171-when-is-an-anchor-absent` — *"c — Both conditions (strictest, fewest double submissions)"*,
Kam, live board, 2026-09-25 12:49:07 AEST.

## HONEST CAVEATS, STATED RATHER THAN BURIED
- **RED (c), the positive arm, passes at develop too** — the old rule also retried there. It is labelled
  the positive control it is, not counted among the reds.
- The **log-collapse defect of mine** the census caught (7 flips measured where the ruling causes 4) is
  named in the PR body, the commit and the ticket comment, not quietly fixed.
- `ConfirmationLike`'s comment, which asserted the opposite of the ruling, is corrected in the same PR.

Nothing merged. #1220 (KS-1129) and #1228 (KS-1171) both await their own GO.

