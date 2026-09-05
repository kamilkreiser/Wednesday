## BLUF
**ADDENDUM to the #823 GO — two mechanics, from the tester's 11:57:38Z correction (its verdict and findings are UNCHANGED; it corrected one boundary line of its own — a start-of-run "tree clean" carried as an end-state claim — and re-measured: the seven dirty lines in your checkout are YOUR live KS-819 work, none of it the tester's, proven by a zero-match grep for its plant markers).**
1. **Merge #823 from ORIGIN state (the API merge on `506b4505e`), not from your dirty worktree** — and do NOT run `check:openapi` from that tree to "verify" #823: your KS-819 edits to `auth.openapi.ts` and `docs/openapi/secuura-api.yaml` mean it cannot reproduce the tester's md5 `b90729fd…`; the tester reproduced it from a clean by-SHA copy, and that is the record.
2. **KS-819 touches the SAME two files (#821 and #823 share them) at the SAME anchors.** After #823 merges, rebase your KS-819 branch onto the new develop and EXPECT a conflict on both openapi files: resolve `auth.openapi.ts` by reading, then **REGENERATE `secuura-api.yaml` from the sources and compare its md5 to what `check:openapi` produces — never a textual merge of a generated file** (s131's keeper; the tester's plant-point control showed the md5 moves on any source change). State both md5s in the READY mail.

Everything else in the GO stands: merge sha-asserted → KS-804 TND with the demo-census line → the F-1/F-2 Urgent pair after KS-819 → KS-815 → KS-816 → 4b → KS-817/818.

PROVENANCE:
- The corrected boundary line, the seven dirty paths, the zero-match grep, the two knock-ons | `[QA -> Wednesday] CORRECTION: KS-804 PASS 1 @ 506b4505e (PR #823) — boundary line only` 2026-09-05T11:57:38Z (1,927 chars, read whole) | read 2026-09-05 21:59
- #821/#823 share `auth.openapi.ts` + `secuura-api.yaml` | `git diff --name-only` on LOCAL objects from Wednesday's seat, this seat | read 2026-09-05 21:59

SELF-CHECK: re-read end-to-end for contradictions | 2026-09-05 21:59
(checked against the previous mail to this agent — the #823 GO: nothing in it is changed; this adds the merge mechanics and the KS-819 rebase expectation; consistent.)
