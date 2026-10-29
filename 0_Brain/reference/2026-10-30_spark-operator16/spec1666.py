# KS-1666 note (d)/N5 (gate AK1 on PR #1623, KS-1633): two stale comments in originate routes/certifications.ts. Spark operator 16. code_patch2: ONE two-edit comment hunk + 1 NEW jest source-text file. gen: op16 patched mk2.
P='Blockchain/Dev/services/originate/src/routes/certifications.ts'
TP='Blockchain/Dev/services/originate/src/__tests__/ks1666-certify-reservation-comments-match-the-code.test.ts'
E1=("      // KS-1612 round-2 Major). Writing the row first removes the window rather than narrowing it.\n",
    "      // KS-1612 round-2 Major). Writing the row first NARROWS that window, it does not remove it: when the reservation\n      // itself fails, the anchor-then-fail path is unchanged (KS-1666 d).\n")
E2=("      // the sub-second window before the second write, and introduces no new `anchoringStatus` value into the blob\n",
    "      // the window before the second write (bounded by the anchoring call's AbortSignal.timeout(10000), so up to 10\n      // seconds, not sub-second), and introduces no new `anchoringStatus` value into the blob\n")
TEST='''// KS-1666 note (d) (gate AK1 on PR #1623, KS-1633): two comments in routes/certifications.ts said what the code does not do. One claimed that writing the documents row before the anchor
// "removes the window rather than narrowing it" (when the reservation itself fails the anchor-then-fail path is unchanged, and the code's own comment further down says an orphan anchor can still be created).
// The other called the provisional row's under-claim a "sub-second window" (the window lasts until the second write, after an anchoring call bounded by AbortSignal.timeout(10000)).
// These cells read certifications.ts as text. R1 and R2 are red until the two comments are corrected; C1 to C3 pin the code the comments describe, which must not move.
import { describe, it, expect } from '@jest/globals';
import { readFileSync } from 'fs';
import { join } from 'path';

const SRC = readFileSync(join(__dirname, '..', 'routes', 'certifications.ts'), 'utf8');

describe('KS-1666 (d): the certify reservation comments match the code', () => {
  it('RED KS-1666 R1 the reservation comment no longer says the row-first order removes the window', () => {
    expect(SRC).not.toContain('removes the window rather than narrowing it');
    expect(SRC).toContain('NARROWS that window, it does not remove it');
  });

  it('RED KS-1666 R2 the provisional-row comment no longer calls the window sub-second and names the 10 second bound', () => {
    expect(SRC).not.toContain('the sub-second window before the second write');
    expect(SRC).toContain('up to 10');
    expect(SRC).toContain('seconds, not sub-second');
  });

  it('control KS-1666 C1 the anchoring call is still bounded at 10 seconds', () => {
    expect(SRC).toContain('signal: AbortSignal.timeout(10000),');
  });

  it('control KS-1666 C2 the code still says an orphan anchor can be created when the reservation fails', () => {
    expect(SRC).toContain('when the reservation itself fails the request proceeds and an orphan');
  });

  it('control KS-1666 C3 the file was read (the instrument is not reading an empty string)', () => {
    expect(SRC.length).toBeGreaterThan(3000);
  });
});
'''
S=dict(dir='ks_1666_p1_certify_reservation_comments',ticket='KS-1666',
 title='originate routes/certifications.ts: two comments around the pre-anchor reservation say what the code does not do (the row-first order "removes the window"; the under-claim window is "sub-second"): correct both (KS-1666 note d; RUNG 3, code_patch2: one two-edit comment hunk in one file + one NEW source-text jest file; no behaviour changes)',
 intro="DRAFT by Spark operator 16 for Wednesday, 2026-10-30 AEDT. Secuura (Platform K / originate) only. A local PASS is a candidate, never a merge; the normal QA gate before merge. A COMMENT fix: no behaviour changes. Origin: KS-1666 note (d) / gate AK1 N5 on PR #1623 (KS-1633); the gate recorded that both comments were wrong, corrected the PR body, and deliberately left the code comments alone so as not to move the head the GO was pinned to. ONLY (d) is in this brief; (a) is a design question, (b) and (c) need new cells with mocks, (e) is in an integration suite header, (f) is a policy choice. Link the PR as Refs KS-1666 and KS-1633, never a close-word.",
 products=[(P,[E1,E2])],
 prodnote=['product, modified in place: TWO comment edits in ONE hunk (a one-line comment becomes two lines, a one-line comment becomes two lines), no code'],
 tests=[dict(path=TP,content=TEST)],
 testnote=['NEW file, jest, given in full below; 5 cells (2 red, 3 control; source-text reads of the file above)'],
 runner='jest` (`npx jest src/__tests__/ks1666-certify-reservation-comments-match-the-code.test.ts` from `Blockchain/Dev/services/originate',
 tier='code_patch2', rung='3 (two files: a product file with a comment hunk, a new test given whole)',
 pins='''# code_patch2: originate routes/certifications.ts (1 comment hunk, 2 edits) + a NEW jest source-text file; ref = another originate test that reads a file as text (shape only); line = the first changed line in the FIRST product.
tier=code_patch2
ref=Blockchain/Dev/services/originate/src/__tests__/ks1114-served-spec-describes-the-title-lookup.test.ts
line=520
ctx=65536
''',
 wrong="Two comments in `services/originate/src/routes/certifications.ts` (the KS-1633 block above `reserveCertificationRow`) say something the code does not do. (1) `:520` says writing the row first \"removes the window rather than narrowing it\". It narrows it: when the reservation itself fails the request proceeds and the anchor-then-fail path (an orphan anchor) is unchanged, which the code's own comment says a few lines further down (`:571-572`, \"when the reservation itself fails the request proceeds and an orphan anchor can still be created\"). (2) `:527` says the provisional row under-claims for \"the sub-second window before the second write\". The second write comes after the anchoring call, which is bounded by `AbortSignal.timeout(10000)` (`:616`), so the window is up to 10 seconds. Both were corrected in PR #1623's body and deliberately left in the code; they are wrong in the merged tree.",
 where="- `Blockchain/Dev/services/originate/src/routes/certifications.ts:520` - **must change**: the one comment line `      // KS-1612 round-2 Major). Writing the row first removes the window rather than narrowing it.` becomes two comment lines (the diff below gives them byte-exact).\n- `Blockchain/Dev/services/originate/src/routes/certifications.ts:527` - **must change**: the one comment line `      // the sub-second window before the second write, and introduces no new \\`anchoringStatus\\` value into the blob` becomes two comment lines.\n- `:571-572` (the comment that already says an orphan anchor can still be created) and `:616` (`signal: AbortSignal.timeout(10000),`) - (correct, STAY) the lines the new cells C1 and C2 pin.",
 exactnote="ONE product hunk holding both edits, in file order.\n",
 donot="**Do NOT touch** any code line or any other comment in `certifications.ts`, and no other file.",
 testnote2="The test section is a NEW file given whole. The `+` lines are byte-exact. The new file is pure ASCII, imports `describe`, `it` and `expect` from `@jest/globals`, reads `certifications.ts` with `readFileSync` relative to `__dirname`, and has no top-level await.",
 red=['RED KS-1666 R1','RED KS-1666 R2'],
 cells="- RED `R1`: at the tip the comment still contains `removes the window rather than narrowing it` and not `NARROWS that window, it does not remove it`.\n- RED `R2`: at the tip the comment still contains `the sub-second window before the second write` and not `seconds, not sub-second`.\n- GREEN at the tip and after: `C1` (the 10000 ms bound), `C2` (the orphan-anchor sentence), `C3` (the file was read).\n- After the edit all five are green.",
 premises="- `certifications.ts:520` and `:527` are as quoted, `:571-572` carries the orphan-anchor sentence and `:616` the 10000 ms bound (read at the tip by script; the golden is generated from the tree at the tip, not typed).\n- originate's runner is jest; the tip's `ks1114-served-spec-describes-the-title-lookup.test.ts` reads files as text.",
 unmeasured="- Nothing was run by the drafter apart from the harness dry-run and control.\n- The 10 second figure is the `AbortSignal.timeout(10000)` at `:616`; whether the second write can also be delayed by anything else (a slow save) was not measured, so the new comment says 'up to 10 seconds' for the anchoring bound only.\n- The wording of the replacement comments is the drafter's, not the gate's.\n- Other items of KS-1666 are untouched.",
 scope="**KS-1666 note (d) only.** Link the PR as Refs KS-1666 and KS-1633, never a close-word. No behaviour change.",
)
