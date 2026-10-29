# KS-1840 (Seat R 63rd, filed 2026-10-30): a stale code comment above GET /api/anchors/document/:documentId (anchoring index.ts) and the DEVELOPMENT.md:121 row cite
# makeFetchDocFromAnchorStore, retired in KS-1628. Spark operator 13. code_patch2: 1 comment hunk + 1 doc-row hunk + 1 NEW vitest source-text file. gen/mk.py.
P='Blockchain/Dev/services/anchoring/src/index.ts'
D='Blockchain/Dev/DEVELOPMENT.md'
TP='Blockchain/Dev/services/anchoring/src/__tests__/ks1840-stale-gateway-citation-is-gone.test.ts'
E1=(" * match. Gateway callers already handle non-200 by resolving null\n * (see makeFetchDocFromAnchorStore in api-gateway/src/routes/verification.ts),\n * so the verifier-portal flow is unaffected.\n",
    " * match. The gateway function once cited here as the caller that handles a\n * non-200 was retired in KS-1628. Whether a current caller treats a 404 from\n * this route as no anchor is not measured (KS-1840).\n")
E2=("Gateway's `makeFetchDocFromAnchorStore` already handles non-200 by resolving null, so verifier-portal flow is unaffected. |",
    "The gateway function once cited here as handling a non-200 was retired in KS-1628; whether a current caller treats the 404 as no anchor is not measured (KS-1840). |")
TEST='''// KS-1840 (anchoring): the block comment above GET /api/anchors/document/:documentId in index.ts, and the struck-through H2 row of DEVELOPMENT.md, cited a gateway function
// (the one that "already handles non-200 by resolving null") that was retired in KS-1628. These cells read index.ts as text (the DEVELOPMENT.md row is a separate, doc-only follow-up: the Spark builder measures one service per brief).
// R1 and R2 are red until the stale citation is replaced; C1 to C3 pin what must not move.
import { describe, it, expect } from 'vitest';
import { readFileSync } from 'fs';
import { resolve } from 'path';

const INDEX_SRC = readFileSync(resolve(__dirname, '..', 'index.ts'), 'utf8');

describe('KS-1840: no comment or doc row cites the retired gateway function', () => {
  it('RED KS-1840 R1 index.ts no longer cites the retired gateway function', () => {
    expect(INDEX_SRC).not.toContain('makeFetchDocFromAnchorStore');
  });

  it('RED KS-1840 R2 index.ts says the cited function was retired in KS-1628 and the caller question is not measured', () => {
    expect(INDEX_SRC).toContain('was retired in KS-1628');
    expect(INDEX_SRC).toContain('is not measured (KS-1840)');
  });

  it('control KS-1840 C1 the route comment still explains the 404 with no echoed id', () => {
    expect(INDEX_SRC).toContain('BACKLOG H2 (was F-API-01 part 2)');
    expect(INDEX_SRC).toContain('* GET /api/anchors/document/:documentId');
  });

  it('control KS-1840 C2 the route handler line is untouched', () => {
    expect(INDEX_SRC).toContain("app.get('/api/anchors/document/:documentId', async (req: Request, res: Response) => {");
  });

  it('control KS-1840 C3 the file was read (the instrument is not reading an empty string)', () => {
    expect(INDEX_SRC.length).toBeGreaterThan(5000);
  });
});
'''
S=dict(dir='ks_1840_p1_stale_citation',ticket='KS-1840',
 title='anchoring index.ts:980 comment cite makeFetchDocFromAnchorStore, retired in KS-1628: replace the citation with what is true and what is not measured (RUNG 3, code_patch2: one comment hunk + one NEW source-text vitest file; no behaviour changes; the DEVELOPMENT.md:121 row is NOT in this brief)',
 intro="DRAFT by Spark operator 13 for Wednesday, 2026-10-30 AEDT. Secuura (Platform K / anchoring) only. A local PASS is a candidate, never a merge; the normal QA gate before merge. A COMMENT fix: no behaviour changes. The builder (build_input2) refuses a brief spanning more than one service, so the second hit the ticket names, Blockchain/Dev/DEVELOPMENT.md:121 (the struck-through H2 row), is NOT in this brief; it stays open on KS-1840 as a doc-only follow-up. Origin: KS-1840 (filed by Seat R 63rd), whose own text says the edit waits for KS-1822 (pull request 1813, now merged) because index.ts was Seat A 17th's file. The ticket's whole-repo grep at d7ddfa1f6433 found exactly two hits (this file and DEVELOPMENT.md:121) of the symbol, the comment and DEVELOPMENT.md:121; this brief removes the index.ts one. Link the PR as Refs KS-1840, never a close-word.",
 products=[(P,[E1])],
 prodnote=['product, modified in place: ONE hunk, a three-line comment replaced (no code)'],
 tests=[dict(path=TP,content=TEST)],
 testnote=['NEW file, vitest, given in full below; 5 cells (2 red, 3 control; source-text reads of the two files above)'],
 runner='vitest` (`npx vitest run src/__tests__/ks1840-stale-gateway-citation-is-gone.test.ts` from `Blockchain/Dev/services/anchoring',
 tier='code_patch2', rung='3 (three files: a comment hunk, a doc-row hunk, a new test given whole)',
 pins='''# code_patch2: anchoring index.ts (1 comment hunk) + a NEW vitest source-text file; ref = another anchoring test that reads index.ts as text (shape only); line = the first changed line in the FIRST product.
tier=code_patch2
ref=Blockchain/Dev/services/anchoring/src/__tests__/ks1175-getid-view-wired.test.ts
line=983
ctx=65536
''',
 wrong="The block comment above `GET /api/anchors/document/:documentId` in `Blockchain/Dev/services/anchoring/src/index.ts` (`:979-981` in the ticket, `:983-985` here) says gateway callers already handle a non-200 by resolving null and cites `makeFetchDocFromAnchorStore` in `api-gateway/src/routes/verification.ts`. That function no longer exists: `api-gateway/src/routes/verification.ts` says the verify mock route beside it was retired in KS-1628. The struck-through H2 row of `Blockchain/Dev/DEVELOPMENT.md` (`:121`) carries the same claim; it is OUT of this brief (one service per brief). Nothing read shows another caller treats a non-200 as no anchor, so the replacement text states only what is true: the cited function was retired, and whether a current caller relies on the 404 is not measured. No code and no assertion changes.",
 where="- `services/anchoring/src/index.ts:983-985` - **must change**: the three comment lines ` * match. Gateway callers already handle non-200 by resolving null`, ` * (see makeFetchDocFromAnchorStore in api-gateway/src/routes/verification.ts),` and ` * so the verifier-portal flow is unaffected.` become three comment lines (the diff below gives them byte-exact). The lines above (`BACKLOG H2 ...`) and the `app.get(...)` handler line below are NOT touched.",
 exactnote="ONE product hunk (the index.ts comment).\n",
 donot="**Do NOT touch** any code line, or any other comment in `index.ts`, and no other file.",
 testnote2="The test section is a NEW file given whole. The `+` lines are byte-exact. The new file is pure ASCII, uses `vitest` imports, reads the two files with `readFileSync` relative to `__dirname`, and has no top-level await.",
 red=['RED KS-1840 R1','RED KS-1840 R2'],
 cells="- RED `R1`: at the tip `index.ts` still contains the symbol (the line the ticket names).\n- RED `R2`: at the tip the replacement sentences are absent.\n- CONTROL `C1` to `C3`: green at the tip AND after (the comment's first paragraph and the handler line are not edited; the file is non-empty).",
 premises="- `index.ts:983-985` is as quoted (read at the tip by script; the golden is generated from the tree at the tip, not typed).\n- The ticket's tracked-file grep at d7ddfa1f6433 found 2 hits of the symbol (these two) and 0 in `api-gateway/src/routes/verification.ts`; the drafter re-ran a `git grep` of the symbol at the tip and found the same 2 hits.\n- The service's test runner is vitest and an existing anchoring test already reads `index.ts` as text with `readFileSync(resolve(__dirname, '..', 'index.ts'))`.",
 unmeasured="- Nothing was run by the drafter apart from the harness dry-run and control.\n- Whether any current gateway caller of the anchoring document route treats a non-200 as no anchor (the ticket did not read one either); the new wording says exactly that.\n- Whether other tracked docs carry a paraphrase of the same claim without the symbol name: not searched.",
 scope="**KS-1840 only.** Link the PR as Refs KS-1840, never a close-word. No behaviour change.",
)
