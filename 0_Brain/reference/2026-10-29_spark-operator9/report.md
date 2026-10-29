# Spark operator 9 report, 2026-10-29 (tip fd84001c738a = refs/wed/develop in the cache clone, re-fetched first)

## BLUF
KS-1454 part 1 (the write side) is briefed, proven and was run: the real Spark round PASSED, golden BYTE-IDENTICAL. Nothing held or raised (Wednesday reads the diff).

- Brief dir: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1454_p1/` (KS-1454.md, golden.diff, spark.pins; tier code_patch; spec + generator: `spec1454.py` beside this report, built with `GEN_TIP=fd84001c738a... python3 -I spark/gen/mk2.py`).
- Queue line (queue.md, with the dated comment above it): `ks_1454_p1`
- --dry-run: `SPARK ROUND ks_1454_p1: DRY-RUN OK — brief accepted, input built at fd84001c738a (59611 B) in /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/state/dry/ks_1454_p1_20261029-191726; a real round would call http://127.0.0.1:47788 with code_patch/task.md, thinking OFF`
- --control: `SPARK ROUND ks_1454_p1: CONTROL-PASS — PASS (checker rc 0 + A2a anchor OK) · golden BYTE-IDENTICAL · tip fd84001c738a · 94s round, no model (control) · /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-29_ks_1454_p1-control-r2` (first control run, before a prose-only fix of the cell count, also PASS: `-control`)
- Real round: `SPARK ROUND ks_1454_p1: PASS — PASS (checker rc 0 + A2a anchor OK) · golden BYTE-IDENTICAL · tip fd84001c738a · 143s round, 58.644s model, 21267+2131 tok · /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-29_ks_1454_p1` (done.md row 19:21:45, checker 7/7)
- Run dir: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-29_ks_1454_p1`

## Ticket text: found
Linear export `0_Brain/reference/2026-10-12_ks-routing-triage/raw_ks_issues.json` (KS-1454, Backlog, 0 comments, updated 10-10). Items: 1 accept `metadata.signatureHash` (`^[a-f0-9]{64}$`); 2 carry into CIP-674 payload; 3 read-back on `GET /api/anchors/{id}` and verify-by-hash with multiplicity; 4 restrict to `documentType = sign`, 400 elsewhere ("a requirement, not an option"). Not decision-shaped to build: Stuart ruled the plain hash; Kam's 10-19 card (a) says build the S contract additions after KS-1454. So I briefed, did not stop.

## Scope carved (the ticket is wider than a Spark predicate)
p1 = items 1, 2, 4 in ONE product file `anchoring/src/anchorSchema.ts` + one NEW vitest file. NOT in p1: item 3 (anchorReadback.ts, index.ts; by-id route is KS-723), and the OpenAPI declaration (`anchoring.openapi.ts` is hand-written, so zod changes do not reach it). S's served-spec gate needs that declaration, so S's switch stays off until a p2/p3 ships.

## The edits commissioned (anchorSchema.ts, 3 insertions; line numbers at fd84001c738a)
1. after :214 (inside `metadata`): `signatureHash: z.string().regex(/^[a-f0-9]{64}$/, '...').optional(),` + a comment.
2. after :247 (end of the `superRefine`): if `metadata.signatureHash !== undefined && metadata.documentType !== 'sign'`, `ctx.addIssue` custom, path `['metadata','signatureHash']`.
3. after :304 (payload builder): `...(data.metadata?.signatureHash ? { signatureHash: data.metadata.signatureHash } : {}),`.
Plus NEW `anchoring/src/__tests__/ks1454-signature-hash-is-accepted-and-anchored-on-the-sign-verb.test.ts`: 14 vitest cells (R1 accepted+anchored verbatim; R2 refused on upload; R3 refused with no verb; R4 x6 malformed: uppercase, 63, 65, non-hex, number, array; R5 reaches the Cardano metadatum as ONE string; C1-C4 controls).
Must not change: `anchoring.openapi.ts`, `anchorReadback.ts`, `index.ts`, the codec, `identitySchema`, verb lists, the did:jwk pattern from #1805, and the existing exact-key-set cells (their inputs carry no signatureHash).

## Things for Wednesday
- Ticket says K's minimisation review should object BEFORE building if it disagrees; no K-side answer is recorded in the notes I read.
- Same file as the merged did:jwk (#1805); the brief is built on the merged tip, so no conflict at the tip. Overlap with open PRs was NOT checked (gen/overlap.py not run).
- Raise as `Refs KS-1454` (not Closes). Hole to watch in the diff: a PR cannot make the S contract usable without the spec declaration (p3).

## TESTED / NOT TESTED / HOW
TESTED (round.sh, real checker in a cache-clone): lint + build (dry-run); golden control twice (A3 file set, A4 10 of 14 cells red at the untouched tip by assertion with controls green, A5 14/14 green with the hunks, A6 whole services/anchoring suite: no new red vs tip (the baseline has 1 pre-existing red, threadTokenMint emulator round-trip, same before and after), A7 tsc, A2a anchors); then ONE real Spark round: PASS 7/7, golden BYTE-IDENTICAL.
NOT TESTED: the route over HTTP (400 mapping rests on the read of index.ts:477 `parse` and :582 `ZodError` handling, not run); the docs/openapi YAML or any spec-drift test (A6 showed no new red in the anchoring suite only; other services not run); a real chain submit; read-back (not in p1); open-PR overlap; whether S really sends `documentType: sign` on every detached signature.
HOW: `bash spark/round.sh night/briefs/ks_1454_p1 --dry-run` / `--control`, then queue.md + `nohup queue.sh`. Nothing outside the brief dir, queue.md, done.md/state (written by the drainer) and this folder was edited.
