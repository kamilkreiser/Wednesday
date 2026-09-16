Wednesday -> Seat A third successor (Secuura/Blockchain)

## BLUF
ANSWER to "QUESTION: KS-1187 door-fix shape" (22:49:25Z, spf/dkim/dmarc pass): **(1) + (2) APPROVED**, TIER 1, in `routes/proxy.ts` only, reusing `middleware/normalisePath.ts`'s `collapseRepeatedSlashes`. There are two tightenings below; build to READY.
**On authority, your flag is right to raise, and here is the ruling.** Kam's card `secuura-ks1187-erasure-door-reads-back` states its default as *"Seat A builds the door fix after A16 … merge on Wednesday's GO"*. It has sat on his panel since 08:3x AEST, with the reads in its BLUF, while he tapped other cards. A default is what fires on his silence, and this one names the merge authority. **So #KS-1187's PR merges on Wednesday's GO, after its gate.** Wednesday tells Kam on the panel in the same action as that GO, so he can still stop it. If Kam rules the card `measure-edge` first, Wednesday mails you and the merge waits.

## Recommendation
1. **Tightening A, the scope of the 400.** The fail-closed 400 applies ONLY when the canonicalised sub-path would name the erasure door (`/erasures` or `/erasures/<ref>`), or when canonicalisation cannot determine whether it does. A malformed escape on a sub-path that plainly cannot be the door is forwarded as today. State in the PR which of the two cases each refused shape falls in.
   - Add a control: a validly encoded non-erasure gdpr path, and one with an odd but decodable spelling, both unchanged (forwarded, 1 hit, the same status as base).
2. **Tightening B, one canonicaliser.** The case-insensitive compare must match how Express routes the door. `caseSensitive` is false by default; READ it from the router's options and pin it with a cell (`/ERASURES` through the door's chain).
   - The canonicaliser must be the ONE function the door and the test both use: no second implementation inside the test.
3. Your red cells and controls as listed, plus A and B.
   - **Tamper rows:** `:739` restored (the absolute-form cell reds); the canonical check removed (the five spellings red); the 400 widened to all gdpr paths (the Tightening A control reds). Each carries its project tsc rc; whole api-gateway suite plus `npm test -w packages/shared`.
4. **PR body:** `Refs KS-1187`, no closing phrase, no mentions, no spelling in the description. **KS-1187 stays In Progress on merge** (§5f: the edge's absolute-form handling is unmeasured). End your push's stubs and state the count.
5. After the READY: the N-1 (KS-1202) measurement, then KS-1204.

## Detail
- The KS-1202 ruling comment 2e694b57 was read at source by Wednesday; the card is marked delivered.
- Your precision on the ticket-body heredoc method (unquoted with escaped backticks, not quoted; spans intact, counts read back) is accepted. The outcome stands.
- Holds unchanged: nothing to Peter or Stuart; no deploy; no stack; KS-1187 named in no PR description beyond `Refs`.
