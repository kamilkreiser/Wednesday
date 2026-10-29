# KS-1816 (filed 2026-10-29 by R 61st): two reconciler.ts comments are false. Spark operator 15. code_patch2: 2 comment hunks in ONE product + 1 NEW vitest source-text file. gen/mk.py.
P='Blockchain/Dev/services/anchoring/src/reconciler.ts'
TP='Blockchain/Dev/services/anchoring/src/__tests__/ks1816-reconciler-comments-match-the-code.test.ts'
E1=(" *   - a chain-provider error leaves the row untouched for the next pass.\n",
    " *   - a chain-provider error leaves the row untouched for the next pass only below\n *     the give-up age; at or past it the same error is read as absence and the row\n *     is marked failed (KS-1810).\n")
E2=("      // MIN_AGE keeps the reconciler off rows the live submit/confirm loop is\n      // still actively working (it touches updated_at as it goes).\n",
    "      // MIN_AGE keeps the reconciler off rows that were written recently. The age is\n      // read from updated_at, which each status write moves, but the confirmation poll\n      // writes nothing between submitted and confirmed, so a row the live loop is still\n      // polling can pass MIN_AGE (KS-1816).\n")
TEST='''// KS-1816 (anchoring reconciler.ts): two comments said what the code does not do. The header property claimed a chain-provider error always leaves the row untouched for the next pass
// (past the give-up age the same error is read as absence and the row is failed). The MIN_AGE comment claimed the live loop touches updated_at as it goes (the confirmation poll writes nothing).
// These cells read reconciler.ts as text. R1 and R2 are red until the two comments are corrected; C1 to C3 pin the code lines the comments describe, which must not move.
import { describe, it, expect } from 'vitest';
import { readFileSync } from 'fs';
import { resolve } from 'path';

const SRC = readFileSync(resolve(__dirname, '..', 'reconciler.ts'), 'utf8');

describe('KS-1816: the two reconciler.ts comments match the code', () => {
  it('RED KS-1816 R1 the header property no longer claims a provider error always leaves the row untouched', () => {
    expect(SRC).not.toContain('error leaves the row untouched for the next pass.');
    expect(SRC).toContain('only below');
    expect(SRC).toContain('marked failed (KS-1810)');
  });

  it('RED KS-1816 R2 the MIN_AGE comment no longer says the live loop touches updated_at as it goes', () => {
    expect(SRC).not.toContain('it touches updated_at as it goes');
    expect(SRC).toContain('writes nothing between submitted and confirmed');
  });

  it('control KS-1816 C1 the select still ages rows by updated_at', () => {
    expect(SRC).toContain("AND updated_at < NOW() - ($1 || ' milliseconds')::interval");
  });

  it('control KS-1816 C2 the give-up test still reads created_at', () => {
    expect(SRC).toContain('else if (now() - new Date(row.created_at).getTime() > config.giveUpMs) {');
  });

  it('control KS-1816 C3 the file was read (the instrument is not reading an empty string)', () => {
    expect(SRC.length).toBeGreaterThan(3000);
  });
});
'''
S=dict(dir='ks_1816_p2_reconciler_comments',ticket='KS-1816',
 title='anchoring reconciler.ts: two comments say what the code does not do (a provider error leaves the row untouched; the live loop touches updated_at): correct both (RUNG 3, code_patch2: two comment hunks in one file + one NEW source-text vitest file; no behaviour changes)',
 intro="DRAFT by Spark operator 15 for Wednesday, 2026-10-30 AEDT. Secuura (Platform K / anchoring) only. A local PASS is a candidate, never a merge; the normal QA gate before merge. A COMMENT fix: no behaviour changes. Origin: KS-1816 (filed by Seat R 61st from Seat W 7th's KS-1384 design census; R 61st re-read every line at develop 6d41673e0f79). The defects those comments hide are KS-1810 (a provider outage read as absence at the give-up age) and KS-1808 (the give-up age measured from created_at); this brief changes neither, only what the two comments say. Link the PR as Refs KS-1816, never a close-word.",
 products=[(P,[E1,E2])],
 prodnote=['product, modified in place: TWO comment hunks (a header line, then a two-line comment), no code'],
 tests=[dict(path=TP,content=TEST)],
 testnote=['NEW file, vitest, given in full below; 5 cells (2 red, 3 control; source-text reads of the file above)'],
 runner='vitest` (`npx vitest run src/__tests__/ks1816-reconciler-comments-match-the-code.test.ts` from `Blockchain/Dev/services/anchoring',
 tier='code_patch2', rung='3 (two files: a product file with two comment hunks, a new test given whole)',
 pins='''# code_patch2: anchoring reconciler.ts (2 comment hunks) + a NEW vitest source-text file; ref = another anchoring test that reads a source file as text (shape only); line = the first changed line in the FIRST product.
tier=code_patch2
ref=Blockchain/Dev/services/anchoring/src/__tests__/ks1175-getid-view-wired.test.ts
line=22
ctx=65536
''',
 wrong="Two comments in `services/anchoring/src/reconciler.ts` say something the code does not do. (1) The header property at `:22`, \"a chain-provider error leaves the row untouched for the next pass\", holds only below the 24 hour give-up age: `waitForConfirmation(tx, 1, 0, 0)` (index.ts) catches a provider error and returns `{ confirmed: false }` instead of throwing, so the reconciler's own `catch` at `:106-109` is not reached by an outage, and at `:98` a row older than `giveUpMs` is written `failed`. (2) The comment at `:63-64`, \"MIN_AGE keeps the reconciler off rows the live submit/confirm loop is still actively working (it touches updated_at as it goes)\", is false for the confirmation phase: every status write moves `updated_at` (submitting, submitted, confirmed) but the poll between submitted and confirmed writes nothing, and it outlasts MIN_AGE (the ticket sums the poll at 27.2 to 28.2 minutes against the 10 minute default). Both are source readings from the ticket, re-read by the drafter at the tip. The replacement text states only what the ticket establishes.",
 where="- `services/anchoring/src/reconciler.ts:22` - **must change**: the one header line ` *   - a chain-provider error leaves the row untouched for the next pass.` becomes three comment lines (the diff below gives them byte-exact).\n- `services/anchoring/src/reconciler.ts:63-64` - **must change**: the two lines `      // MIN_AGE keeps the reconciler off rows the live submit/confirm loop is` and `      // still actively working (it touches updated_at as it goes).` become four comment lines (byte-exact below). The `const rows = await deps.query(` line under them is NOT touched.",
 exactnote="TWO product hunks (the header line, then the MIN_AGE comment), in file order.\n",
 donot="**Do NOT touch** any code line, any SQL, or any other comment in `reconciler.ts`, and no other file.",
 testnote2="The test section is a NEW file given whole. The `+` lines are byte-exact. The new file is pure ASCII, uses `vitest` imports, reads `reconciler.ts` with `readFileSync` relative to `__dirname`, and has no top-level await.",
 red=['RED KS-1816 R1','RED KS-1816 R2'],
 cells="- RED `R1`: at the tip the header still carries the sentence that ends `for the next pass.`, and neither `only below` nor `marked failed (KS-1810)` is present.\n- RED `R2`: at the tip the MIN_AGE comment still says `it touches updated_at as it goes` and the replacement sentence is absent.\n- CONTROL `C1` to `C3`: green at the tip AND after (the SELECT's `updated_at` age test, the `created_at` give-up test and the file length are not edited).",
 premises="- `reconciler.ts:22` and `:63-64` are as quoted (read at the tip by script; the golden is generated from the tree at the tip, not typed).\n- `reconciler.ts:76` is the `updated_at < NOW() - ...` age test and `:98` the `created_at` give-up test, read at the tip; the service's test runner is vitest and an existing anchoring test already reads a source file as text.",
 unmeasured="- Nothing was run by the drafter apart from the harness dry-run and control.\n- The 27.2 to 28.2 minute poll length is the ticket's arithmetic over `confirmation.ts`; the drafter did not re-sum it, and the new comment does not quote the figure.\n- KS-1384's design revision plans to change this file (KS-1808 and KS-1810 are the same file); a comment-only hunk here may conflict with that build and need a trivial rebase.\n- Whether other comments in the file (the header's give-up property at `:16-19`, which KS-1808 owns) are also stale: not touched here.",
 scope="**KS-1816 only.** Link the PR as Refs KS-1816, never a close-word. No behaviour change.",
)
