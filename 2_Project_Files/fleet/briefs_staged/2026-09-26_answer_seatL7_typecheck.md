# ANSWER (Seat L7): TYPECHECK-DEBT — Q1 (a) · Q2 fix the two in ssrf-guard.ts, TYPE-ONLY · Q3 ONE ticket for the residue AND the leg

## BLUF
Your measurement is accepted as measured (probe v3, the planted TS2322 control 10 → 11, restored byte-identical). The three rulings:
1. **Q1 = (a).** One file, one branch. Nothing into `ks781-p3-3-body-parser-order.test.ts` from the KS-1179 branch; #1268 is gated and its head is held. Its three errors (2× TS2345 at :2817/:2855, 1× TS2741) go into the ticket in item 3, marked "after #1268 merges".
2. **Q2 = fix the two in `ssrf-guard.ts` (TS7006, TS2349) under KS-1179, TYPE-ONLY.** The file's runtime behaviour and every string it emits stay byte-identical. In particular the error text at `:605` stays exactly as it is, because Seat B 29th's ks914 cells assert it (the earlier ruling, unchanged). Prove it: the ks914 cells green at your head, and `git diff` shows no change to any string literal.
3. **Q3 = ONE ticket, not two:** "packages/shared type-checks `src/__tests__`": remove the exclusion's blind spot with a test-inclusive tsc leg AND fix the remaining 8 errors (the 6 in `openapi-operation-ids`, `openapi-415-injection`, `ks914-pinned-address`, `walkTimeouts`, plus ks781's 3 once #1268 merges), with your table and your probe-v3 method and control pasted in. **Why one:** a single test pass proves it (the new leg goes green only when the errors are gone), and that is Kam's creation rule. Search the board first by `tsconfig` / `src/__tests__` / `TS2345` and say what you searched. `Refs KS-1179`. **Do not build it this round**: the leg touches the push gate, which is not in your lane. On KS-1179, record the exclusion as the ACCEPTED debt with your measurement, pointing at the new ticket.

**F-5:** agreed. It closed at develop and nothing changes.

## Queue
N1 and N2 as you are doing, then the ssrf-guard.ts pair, then KS-1319 and KS-1314. A READY never ends your turn.
