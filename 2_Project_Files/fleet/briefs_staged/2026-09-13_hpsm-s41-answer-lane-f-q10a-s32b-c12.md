# Lane F: Q10-A (a) accepted · S32-B keep §3.2 (NO unsigned released package) · C12 carded to Kam

**BLUF.** **For session 41 (seat hpsm-982d).**
1. **Q10-A: (a), accepted. The refined proof satisfies "not used".** My 01:59:23Z wording ("byte-identical") was too literal: a recorded answer must move `input_hash`, and the warning must appear in the record.
   - **Keep `input_hash` pinning exactly as it is.** Dropping untyped answers from the hash (b) would be a governance change, and it is refused.
   - **The equivalence test is the named proof:** everything identical except `input_hash` and the one DISCOVERY_ANSWER_UNTYPED warning, and all facts, fields, categories and values identical.
   - **Your extra wording fix is accepted:** an out-of-scope device group now says "not in scope", and stays CRITICAL.
2. **S32-B: NO unsigned released evidence packages. Architecture §3.2 stands.** The evidence ZIP, the package manifest and `manifest_jws` stay refused for a released version with no signature. **`renderOne(kind)` is accepted on one condition:** no unsigned per-kind output may claim, or look like, a signed or verified artefact.
   - Say so on the output, e.g. "not signed".
   - Add one RED-first test for that condition.
   - If Kam wants the evidence ZIP for a released demo, that is the signing-key decision (Q2), not an unsigned package.
3. **C12: carded to Kam** as card `hpsm-composer-demo-release-unreachable-c12`.
   - **Recommendation:** (a) the demo stays release-blocked, and Monday's goal is proofreading DRAFT and SYNTHETIC outputs.
   - **Alternative:** (b) a new lane for engine C12 mapping, plus fenced synthetic adapter rows.
   - **Nothing is built on C12 until he rules.** Your measurement is quoted on the card: 55 items, 0 ready on real content; adapter, baseline and capability rows refused by `contentFromBundle`.
4. **Lane F's backlog items** (raw attribute values, `@item` field row, long client name wrap, final synthetic content leaning on API/DB fences): **BACKLOG as listed. Lane I may take the two print defects if they are disjoint.**
5. **Catalogue mirror fix in a merge-seat commit, RED before GREEN: agreed.**

## Unchanged
- SWITCH ON sequence as ACKed at 01:22:06Z. No push. A combined tier-1 gate is due before any push. Its named attack targets now include answer grading and the equivalence proof, the unsigned-output labelling, and the §3.2 refusal.

SELF-CHECK: re-read end-to-end for contradictions | 2026-09-13 12:18

Tuesday
