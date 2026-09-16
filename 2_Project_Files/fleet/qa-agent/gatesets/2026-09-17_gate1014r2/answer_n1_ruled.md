Wednesday -> Seat A third successor (Secuura/Blockchain)

## BLUF
RULED: Kam ruled card `secuura-served-documenttype-unchecked-n1` → **measure-first** (panel card tap 2026-09-17 08:47:23 AEST, view=wednesday). The chosen option, verbatim: *"First run a real originate in-process to confirm what it stores and serves, then decide"*. This is the N-1 finding from the #1014 round-2 gate (the served `data.documentType` is unchecked). It adds ONE measurement item to your queue, placed after the KS-1187 door fix and before the N-2/N-3 follow-up. **Nothing is built for N-1.**

## Recommendation
1. When you file the N-1 ticket (item 3b of GO #1014), add ONE comment on it quoting the ruling verbatim with its tap time, gated on the ticket's creation rc. Name the comment id in the #1014 MERGED receipt.
2. **The measurement, when its turn comes.** Use the real originate router and its documents routes in-process in your worktree, the same shape as your KS-1187 read (2) harness, with no stack and no real DB write beyond an in-memory or loopback stand-in you name.
   - Send each carrier through create, then read it back through the endpoints the verify gate consumes: typed allowed + `data.documentType` DEGREE; untyped + `data.documentType` DEGREE; typed with no `data.documentType`.
   - Record for each: what originate STORES (the column / field) and what it SERVES (:311, :1053), and whether the gateway verify gate (:546) would match it.
   - Controls: a plain allowed document, and a row where stored = served.
   - Results go as ONE facts comment on the N-1 ticket (MEASURED vs READ vs UNMEASURED, instruments named), plus a STATUS mail. Wednesday re-raises the card with it.
3. Queue order now: #1014 merge → KS-1187 door fix (shape QUESTION first) → **N-1 measurement** → N-2/N-3 follow-up → A11 → KS-1194.

## Detail
- If the measurement needs a DB beyond what an in-process harness can stand in for, stop and ask. That would be a stack, and the stack hold stands.
- Holds unchanged: nothing to Peter or Stuart; no deploy.
