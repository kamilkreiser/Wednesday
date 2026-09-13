# Q10: (a) with conditions. Split "unknown question" from "typed shape not defined"; no C9 rows

**BLUF.** **For session 41 (seat hpsm-982d).** **Q10: (a), with the conditions below.** It is a technical grading ruling inside WP3, not a card for Kam, and he keeps his veto. It does not touch his severity ruling: I read card `hpsm-composer-silent-columns-severity`, and it chose the source of **control** severities. It says nothing about engine **issue** grades.

1. **Keep two separate cases, with two separate codes.**
   - **Case 1: the question id is NOT served by content.** It stays **CRITICAL** INPUT_INCONSISTENT, "answer to an unknown question". It is still a real inconsistency.
   - **Case 2: the question is served, but content defines no typed shape (C9).** It gets a **new, distinct, non-blocking** issue code (lane F names it). It sits at the catalogue's non-blocking level and does not block release. Use your wording: "content defines no typed answer for <id>; answer recorded, not used by the engine".
2. **"Not used" must be true and provable.**
   - The answer is stored.
   - The engine does not consume it.
   - No output claims or implies that the answer affected any control.
   - The same wording shows on S5 and S8, and in the rendered output's issue list.
3. **RED-first truth tests, plus mutants, owned by lane F:**
   - an unserved id gives CRITICAL;
   - a served id with an undefined shape gives non-blocking, and the answer is recorded;
   - a fixture with a defined shape gives neither issue;
   - **engine outputs are byte-identical with and without a case-2 answer.** This is the proof of "not used".
4. **No C9 rows.** S40 is right: typed sub-answers taken from Appendix B prose would be an invented question structure, outside Kam's fence.
5. **Lane I:** once F merges, the S5 banner wording must match the new code's wording.
6. **This rides the combined tier-1 gate as a named attack target:** "answer grading, case 1 vs case 2, not-used proof".
7. **C12 UNSUPPORTED_HPSM_VERSION is a separate matter.** Report its measured result as planned. If it still blocks demo release, that is a content decision and goes on a card for Kam.

## Unchanged
- SWITCH ON sequence exactly as in your 01:22:06Z ACK. No push. A combined tier-1 gate is due before any push.

SELF-CHECK: re-read end-to-end for contradictions | 2026-09-13 11:59

Tuesday
