P='Blockchain/Dev/services/originate/src/services/connectorOrganisationErasure.ts'
T1='Blockchain/Dev/services/originate/src/__tests__/ks695-ask3-erase-connector-refusals.test.ts'
TP='Blockchain/Dev/services/originate/src/__tests__/ks1579-two-stale-statements-about-the-erase-connector-guard-are-corrected.test.ts'
E1=("//           one connector, and no key table can make an erasure by it safe (a guard that reads live keys cannot see a key that was\n//           deleted or rotated away). The erasure REFUSES it (403, nothing written) before it reads any key. A key without an id\n",
    "//           one connector, and no key table can make an erasure by it safe (a guard that reads the key table cannot see a key that was\n//           DELETED; a rotated key is only deactivated or shortened and is still read). The erasure REFUSES it (403, nothing written) before it reads any key. A key without an id\n")
TITLE_OLD="  it('CONTROL - M-2 liveness is UNCHANGED: a key with a NULL, and one with an empty, connector id already got 403 from the ownership comparison and still does', async () => {\n"
TITLE_NEW="  it('CONTROL - M-2 liveness is UNCHANGED: a key with a NULL, and one with an empty, connector id is still refused 403 (now by the fallback-principal refusal, not the ownership comparison)', async () => {\n"
TEST='''// KS-1579 items 3 and 4 (originate, the erase-connector guard): two statements in the tree had gone stale after round 6 of KS-695.
//   item 4: the header comment of services/connectorOrganisationErasure.ts said the guard cannot see a key that "was deleted or rotated away". A rotation only deactivates or shortens the old key
//           (an UPDATE), and the guard reads inactive keys, so a rotated key IS seen; only a DELETED key escapes it.
//   item 3: the title of a unit cell in ks695-ask3-erase-connector-refusals.test.ts said a key with a NULL or empty connector id "already got 403 from the ownership comparison". After round 6 the 403 for
//           those keys comes from the fallback-principal refusal; the cell pins the status, not the reason, so the title is what a reader trusts.
// These cells read the two files as text. R1 and R2 are the product-comment cells (red until the comment is corrected); T1 and T2 pin the corrected cell title; C1 to C3 pin what must not move.
import { describe, it, expect } from '@jest/globals';
import { readFileSync } from 'fs';
import { join } from 'path';

const ERASURE_SRC = readFileSync(join(__dirname, '..', 'services', 'connectorOrganisationErasure.ts'), 'utf8');
const REFUSALS_SRC = readFileSync(join(__dirname, 'ks695-ask3-erase-connector-refusals.test.ts'), 'utf8');

describe('KS-1579: the erase-connector guard statements say what the code does', () => {
  it('RED KS-1579 R1 the guard header no longer says a key can be "deleted or rotated away" from the guard', () => {
    expect(ERASURE_SRC).not.toContain('deleted or rotated away');
  });

  it('RED KS-1579 R2 the guard header says a rotated key is only deactivated or shortened and is still read', () => {
    expect(ERASURE_SRC).toContain('a rotated key is only deactivated or shortened and is still read');
  });

  it('control KS-1579 T1 the refusals cell title no longer claims the 403 comes from the ownership comparison', () => {
    expect(REFUSALS_SRC).not.toContain('already got 403 from the ownership comparison');
  });

  it('control KS-1579 T2 the refusals cell title names the fallback-principal refusal', () => {
    expect(REFUSALS_SRC).toContain('(now by the fallback-principal refusal, not the ownership comparison)');
  });

  it('control KS-1579 C1 the guard header still says the erasure REFUSES a key with no connector id before it reads any key', () => {
    expect(ERASURE_SRC).toContain('The erasure REFUSES it (403, nothing written) before it reads any key.');
  });

  it('control KS-1579 C2 the refusals cell is still there under its M-2 liveness title', () => {
    expect(REFUSALS_SRC).toContain('CONTROL - M-2 liveness is UNCHANGED');
  });

  it('control KS-1579 C3 both files were read (the instrument is not reading an empty string)', () => {
    expect(ERASURE_SRC.length).toBeGreaterThan(1000);
    expect(REFUSALS_SRC.length).toBeGreaterThan(1000);
  });
});
'''
S=dict(dir='ks_1579_p1_wording',ticket='KS-1579',
 title='(items 3 and 4) the erase-connector guard header says a rotated key escapes the guard, and a unit-cell title names the wrong source of the 403: correct both statements (RUNG 3, code_patch2: one comment hunk + one title hunk in an existing test + one NEW source-text jest file)',
 intro="DRAFT by a Spark brief drafter for Wednesday, batch 5 of 2026-10-28 AEDT (never-keep-the-Spark-idle round). Secuura only. A local PASS is a candidate, never a merge; the normal QA gate before merge. A COMMENT AND TITLE fix: no behaviour changes. Items 1 (openapi wording, needs the yaml regenerated), 2 (a real-Postgres cell), 5 (a legacy-key divergence) of the ticket are NOT in this brief.",
 products=[(P,[E1])],
 prodnote=['product, modified in place: ONE hunk, a two-line comment replaced (no code)'],
 tests=[dict(path=TP,content=TEST),dict(path=T1,new=False,edits=[(TITLE_OLD,TITLE_NEW)])],
 testnote=['NEW file, jest, given in full below; 7 cells (2 red, 5 control; source-text reads of the two files above)','EXISTING, modified in place: ONE hunk, one cell TITLE (the string argument of one `it(`) replaced; no assertion changes (SUPPORT: green at the tip and after)'],
 runner='jest` (`npx jest src/__tests__/ks1579-two-stale-statements-about-the-erase-connector-guard-are-corrected.test.ts src/__tests__/ks695-ask3-erase-connector-refusals.test.ts` from `Blockchain/Dev/services/originate',
 tier='code_patch2', rung='3 (three files: a comment hunk, a title hunk in an existing test, a new test given whole)',
 pins='''# code_patch2: originate connectorOrganisationErasure.ts (1 comment hunk) + ks695-ask3 test (1 title hunk, SUPPORT) + a NEW jest source-text file; ref = another ks695 test (shape only); line = the first changed line in the FIRST product.
tier=code_patch2
ref=Blockchain/Dev/services/originate/src/__tests__/ks695-ask3-erase-connector-erasure.test.ts
line=219
ctx=65536
''',
 wrong="Two statements went stale after round 6 of KS-695 (gate follow-up, KS-1579 items 4 and 3). (4) The header comment of `services/originate/src/services/connectorOrganisationErasure.ts` (`:219-220`) says a guard that reads live keys cannot see a key that \"was deleted or rotated away\". A rotation only deactivates or shortens the old key (an UPDATE; the security service contains no `DELETE FROM svc_api_keys`), and the guard reads inactive keys, so a rotated key IS seen; only a DELETED key escapes it. (3) The title of the unit cell at `__tests__/ks695-ask3-erase-connector-refusals.test.ts:279` says a key with a NULL or empty connector id \"already got 403 from the ownership comparison and still does\"; after round 6 that 403 comes from the fallback-principal refusal. The cell pins the status, not the reason; the title is reworded. No code and no assertion changes.",
 where="- `src/services/connectorOrganisationErasure.ts:219` and `:220` - **must change**: the two comment lines `//           one connector, and no key table can make an erasure by it safe (a guard that reads live keys cannot see a key that was` and `//           deleted or rotated away). The erasure REFUSES it (403, nothing written) before it reads any key. A key without an id` become the same two lines with `reads live keys` -> `reads the key table` and `deleted or rotated away).` -> `DELETED; a rotated key is only deactivated or shortened and is still read).` (the rest of each line unchanged, in particular `The erasure REFUSES it (403, nothing written) before it reads any key.`).\n- `src/__tests__/ks695-ask3-erase-connector-refusals.test.ts:279` - **must change**: the `it('CONTROL - M-2 liveness is UNCHANGED: ...', async () => {` line: the title tail `already got 403 from the ownership comparison and still does` becomes `is still refused 403 (now by the fallback-principal refusal, not the ownership comparison)`.\n- Every other line of both files is NOT touched.",
 exactnote="ONE hunk in the product file (comments only).\n",
 donot="**Do NOT touch** any code line, any other comment, or any assertion in either existing file.",
 testnote2="The first test section is a NEW file given whole; the second modifies an EXISTING file (one title line). In both, the `+` lines are byte-exact. The new file is pure ASCII, uses `@jest/globals` imports, reads the two files with `readFileSync` relative to `__dirname`, and has no top-level await.",
 red=['RED KS-1579 R1','RED KS-1579 R2'],
 cells="- RED `R1`: at the tip the comment still contains `deleted or rotated away`.\n- RED `R2`: at the tip the new sentence is absent.\n- CONTROL `T1` and `T2`: the title cells read the existing test file, which the patch's other test section has already edited when only the test sections are applied, so they are green with the tests alone and green after the product edit; they pin the new title.\n- CONTROL `C1` to `C3`: green at the tip AND after.",
 premises="- Lines `:219-220` of the product file and `:279` of the existing test are as quoted (read at the tip, ASCII only, see the diff).\n- The security service has no `DELETE FROM svc_api_keys` and rotation only UPDATEs (the ticket's own check; not re-run by the drafter).\n- The service's test runner is jest. The golden is generated by script, not typed.",
 unmeasured="- Nothing was run by the drafter apart from the harness dry-run and control.\n- The ticket's claim about rotation (UPDATE only) is the ticket author's check; the drafter did not re-grep the security service.\n- Open PRs touching these files: none by the file lists of every open PR read on 2026-10-28.",
 scope="**Items 3 and 4 of KS-1579 only.** Items 1, 2 and 5 stay open on the ticket. Link the PR as Refs KS-1579, never a close-word.",
)
