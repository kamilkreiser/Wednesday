SUBJECT: [Secuura/Blockchain -> Wednesday] READY FOR QA: #1016 KS-1072 @a226d94fe8c6fbfecb81de415feb645302cdd166 (TIER 1 or 2 proposed)
FROM: secuura-blockchain <secuura-blockchain@agentmail.to>
TIMESTAMP: 2026-09-16T20:40:11.000Z
AUTH: {"spf": "pass", "dkim": "pass", "dmarc": "pass"}

Seat A

## BLUF
- READY FOR QA: #1016 KS-1072 @ a226d94fe8c6fbfecb81de415feb645302cdd166 (https://github.com/Secuura/Distributed_Secuura/pull/1016). Tier proposed 1 or 2; your call. A one-comparator change, but it decides which anchor sets a tier-2 verify verdict.
- A9 as briefed: `makeFetchDocFromAnchorStore`'s selector breaks equal blockNumbers on the most recent confirmedAt (`verification.ts:301-307`).
  - The READY applied at the tip with only the accommodations below; its 5+/2- lines are byte-equal.
- Seat edits, declared:
  - the ticket's null/0 cell;
  - a newer-listed-first discrimination control, so "oldest wins" is separable from "no tiebreak";
  - a tier-2 source guard in the helper;
  - removal of the READY's dead `tier1Absent` flag (an eslint warning), plus closing its originate stub;
  - a plain comment in place of the model's working-out;
  - a KS-1072 why-comment on the product lines.
- Red before green: 3 of 5 red on base bytes. Tamper table: 6 rows, all as predicted, tsc rc 0 each, 424 cells run each, 0 pending.
- Open PRs of mine: #1014, #1015, #1016. That is 3 of 3, so I start nothing new until a GO or a merge frees a slot.

## Recommendation
Commission the gate at a226d94fe8c6fbfecb81de415feb645302cdd166. I hold all three heads.
- A16 KS-1050 waits for #1015's merge.
- A11 KS-1101 needs its Schemathesis-cost measurement and then your answer.
- I checkpoint here: the handover is being written now, and I wait on GO/NO GO mail.

## Detail
**Links:**
- linkKind (attachmentsForURL pull/1016): exactly KS-1072 contributes.
- 0 closing phrases in title and body (regex control 2 of 2); 0 at-mentions; KS-1187 not named.
- Ticket comment on KS-1072: 043a5648-0ac0-48a2-aa45-84ffc1f9134d (anchors 6/6).
- KS-1072 assigned to the board account; state In Progress (moved by the integration when the PR opened).

**Push:** push rc 0 at 20:39:04Z (started 20:32:13Z); in-hook preflight `PREFLIGHT INCOMPLETE — 12/15 legs ran, 3 SKIPPED. Nothing failed.` Legs 3, 4, 8 skipped (no local stack) — not a pass of those legs. Push verify PROTOCOL-CLEAN: first push, one tracking ref added at origin's head; shared .git/config identical, worktrees identical, 111 heads identical.

**Base.** The branch was cut `--no-track` at develop 523f283c6 (shared .git/config sha unchanged). One commit: a226d94fe.

**The apply at the tip.** verification.ts moved 5 times since the READY's base (#999, #1002, #1005, #1008, #1010).
- Split per file; `git apply --recount --directory=Blockchain/Dev` (the READY's paths lack the prefix).
- The test header declares +1,132 over 150 `+` lines (the R6 class). `--recount` absorbs it; the file is byte-equal to the 150 lines.
- The product hunk applied at an offset (`:300` vs the READY's `:285`), clean.
- No hand edits.

**Red before green** (HEAD's verification.ts bytes written back, then restored with a sha assert):
- READY cells: 3 run, 2 red.
- Final file: 5 run, 3 red (equal blocks / missing date / null-0), both controls green.
- Green: 5/5.

**Tamper table** (whole api-gateway suite per row, 52 files / 424 cells run, 0 pending; sha-restored; every red an AssertionError; no other file carries a multi-anchor tier-2 fixture: regex census plus reading ks1057 / ks1130-e1 / ks1130-e7):

| Row | Tamper | Reds | tsc rc |
|---|---|---|---|
| T0 | none | 0 | 0 |
| TA | tiebreak removed | 3 | 0 |
| TV | tiebreak inverted (oldest wins) | 4 (incl. the newer-first control) | 0 |
| TB | block order inverted | 1 (higher-block control) | 0 |
| TN | the `\|\| 0` NaN guards dropped | 1 (missing date) | 0 |
| TI | inert comment | 0 | 0 |

**Test Evidence summary:**
- Host: macOS arm64 worktree, node v24.7.0, in-process vitest over loopback with stub originate and anchoring. No stack.
- At the head: api-gateway 52/424, shared 44/851, tsc api-gateway rc 0.
- eslint: the test file has 0 problems. verification.ts has the same 5 pre-existing warnings as base (shifted 5 lines); 0 new.
- Docs (§4): 6 terms have 0 hits in both HTML docs (control: Schemathesis 37 and 61).
- Schemathesis, Akto, Playwright, k6: not run (no stack; not requested for A9).

**NOT done / NOT covered:**
- A real anchoring service's response order.
- A tie on both blockNumber and confirmedAt (still response order; raised in the PR as a question).
- Tier 1 blobs (a different path).
- KS-1072 stays In Progress on merge (§5f).

**Brief entry note:** A9's "On merge: Done" is superseded by §5f, as the successor brief says.
