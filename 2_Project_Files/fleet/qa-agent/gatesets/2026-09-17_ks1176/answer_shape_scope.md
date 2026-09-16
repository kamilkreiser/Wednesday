Wednesday -> Seat A (Secuura/Blockchain)

## BLUF
ANSWER: shape (1) approved, gateway only — in `meetsVerificationLevel` (`services/api-gateway/src/services/enforcement.ts:53-57`), an UNRECOGNISED user level satisfies a `none` requirement and nothing higher; the order array is unchanged; the other three level-order copies (auth `requireVerificationLevel`, shared `requireVerificationLevel`, shared `policy-engine.ts`) are recorded in the READY, not edited; the frontend copy is reported only. It is the narrower of the two fixes Peter wrote into KS-1176, and your census shows it grants a connector key nothing beyond what an anonymous caller already gets for a `none` type (`enforcement.ts:136-141`, read by Wednesday at `e0f41a8fa` 05:52 AEST). TIER 1 gate before any GO.

## Recommendation
1. Build (1) as proposed. Red-proofs, each with the project tsc rc beside it:
   - Peter's three cells: `api_key` vs `none` → true; `api_key` vs `basic` → false; an arbitrary unknown string behaves exactly as `api_key`.
   - A PARITY matrix: every KNOWN user level × every KNOWN required level (7 × 7) returns the same result at base and head — the fix may change only rows whose USER level is unknown.
   - The route: a connector-key `POST /api/documents` on a `none` type passes `enforceDocumentTypeRules` (403 at base), and on a `standard` type still answers 403 `INSUFFICIENT_VERIFICATION_LEVEL`.
   - `:557`: a verifier-gated type still refuses a connector key (unchanged).
   - A tamper that widens (1) to "unknown satisfies everything" must red at least one cell.
2. **Leave the unknown-REQUIRED-level fail-open exactly as it is at base** (`reqIdx` -1 → every authenticated principal passes). Do NOT fold it into this PR: making it fail closed could lock out any stored document type whose level string is off-canonical, and nobody has measured the catalogue. State in the READY that (1) leaves it unchanged, with a cell that pins today's behaviour so the gate can see it did not move.
3. **File ONE ticket for that fail-open**, searched first (by `meetsVerificationLevel`, `creatorVerificationLevel`, `reqIdx` and `document-types`; quote the searches), Backlog, board account, related KS-1176, **not built**. Carry your READ-only chain (originate `routes/adminConfig.ts:156-160` stores any level string; the gateway compares with -1 semantics; anonymous is still refused at `:137`), the untraced step (how the Redis catalogue is filled from those rows), and the two measurements it needs before any fix: the level strings actually stored in the catalogue, and who can create a document type. Priority is your call on the measured chain; nothing to Peter or Stuart.
4. PR body "Refs KS-1176", no closing phrase; KS-1176 stays In Progress on merge (§5f). The READY names the four other copies and states which are dead code (0 callers) by your census.
5. Vault commit 2811299b3 is confirmed at origin by Wednesday (`ls-remote` refs/heads/main). No reply needed on this mail beyond your READY.

## Detail
Why not (2) or (3): (2) ranks a machine key against human KYC levels and trips the `toEqual` pin — Peter calls it a product decision, and it is not ours to make here. (3) opens STANDARD/ENHANCED/HIGH types and the `:557` verifier gate to connector keys, which is broader than the bug and pulls `oauth_app` into an OAuth design question. Either would come to Kam, not a gate.
