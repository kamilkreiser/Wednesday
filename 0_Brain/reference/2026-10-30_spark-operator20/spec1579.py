# KS-1579 items 3 + 4: originate connectorOrganisationErasure.ts header comment (rotated away) + ks695-ask3-erase-connector-refusals.test.ts:279 stale cell title. Spark operator 20.
# code_patch2: TWO existing files (one comment hunk each) + 1 NEW jest source-text file = 3 files (rung 3, one file more than operator 19's comment briefs).
P1='Blockchain/Dev/services/originate/src/services/connectorOrganisationErasure.ts'
P2='Blockchain/Dev/services/originate/src/__tests__/ks695-ask3-erase-connector-refusals.test.ts'
TP='Blockchain/Dev/services/originate/src/__tests__/ks1579-erase-connector-comment-and-title-state-the-truth.test.ts'
OLD1=("//           one connector, and no key table can make an erasure by it safe (a guard that reads live keys cannot see a key that was\n"
"//           deleted or rotated away). The erasure REFUSES it (403, nothing written) before it reads any key. A key without an id\n")
NEW1=("//           one connector, and no key table can make an erasure by it safe (a guard that reads the key table, inactive keys included,\n"
"//           cannot see a key that was DELETED: a rotation only deactivates or shortens the old key). The erasure REFUSES it (403, nothing\n"
"//           written) before it reads any key. A key without an id\n")
OLD2="  it('CONTROL - M-2 liveness is UNCHANGED: a key with a NULL, and one with an empty, connector id already got 403 from the ownership comparison and still does', async () => {\n"
NEW2="  it('CONTROL - M-2 liveness is UNCHANGED: a key with a NULL, and one with an empty, connector id is still refused 403 (this cell pins the status, not which refusal produces it)', async () => {\n"
TEST='''/**
 * KS-1579 items 3 and 4 - two pieces of text in the KS-695 erase-connector files must say what the code does.
 *
 * Item 4: the header comment of connectorOrganisationErasure.ts said the key-table guard cannot see a key "that was deleted or
 * rotated away". A rotation only deactivates the old key or shortens its expiry (security's retirePriorStatement is an UPDATE), and the
 * guard reads inactive keys, so a rotated key IS seen; only a DELETED key escapes it.
 * Item 3: the unit cell titled "... already got 403 from the ownership comparison and still does" kept a reason that stopped being
 * true when the fallback refusal was added in round 6. The cell pins the status, not the reason, and its title now says so.
 * These are source-text cells: they read the two files as text, so no server is started.
 */
import * as fs from 'fs';
import * as path from 'path';

const erasureSource = fs.readFileSync(path.join(__dirname, '..', 'services', 'connectorOrganisationErasure.ts'), 'utf8');
const refusalsSource = fs.readFileSync(path.join(__dirname, 'ks695-ask3-erase-connector-refusals.test.ts'), 'utf8');

describe('KS-1579 items 3 and 4: the header comment and the cell title state what the code does', () => {
  it('RED KS-1579 T1 the erasure header no longer says a key was "rotated away"', () => {
    expect(erasureSource).not.toContain('deleted or rotated away');
  });

  it('RED KS-1579 T2 the erasure header says only a DELETED key escapes the guard and that a rotation leaves the old key readable', () => {
    expect(erasureSource).toContain('cannot see a key that was DELETED: a rotation only deactivates or shortens the old key');
  });

  it('RED KS-1579 T3 the unit cell title no longer claims the 403 "already" came from the ownership comparison', () => {
    expect(refusalsSource).not.toContain('already got 403 from the ownership comparison and still does');
  });

  it('RED KS-1579 T4 the unit cell title says it pins the status, not which refusal produces it', () => {
    expect(refusalsSource).toContain('is still refused 403 (this cell pins the status, not which refusal produces it)');
  });

  it('CONTROL KS-1579 T5 the retitled cell still exists once and still checks the two keys', () => {
    expect(refusalsSource.split('M-2 liveness is UNCHANGED').length - 1).toBe(1);
    expect(refusalsSource).toContain("for (const keyId of ['key-null-695', 'key-empty-695'])");
  });

  it('CONTROL KS-1579 T6 the erasure file still declares the fallback predicate and still names the principal label', () => {
    expect(erasureSource).toContain('export function isFallbackConnectorId(');
    expect(erasureSource).toContain('connector:api-key');
  });
});
'''
S=dict(dir='ks_1579_p1_erase_connector_text',ticket='KS-1579',
 title="originate connectorOrganisationErasure.ts header + ks695-ask3-erase-connector-refusals.test.ts:279 title: two stale texts after round 6 (KS-1579 items 3 and 4): reword both (RUNG 3, code_patch2: two comment/title hunks in two existing files + one NEW jest source-text file; no behaviour changes)",
 intro="DRAFT by Spark operator 20 for Wednesday, 2026-10-30 AEDT. Secuura (Platform K / originate, comment text and one test TITLE only) only. A local PASS is a candidate, never a merge; the normal QA gate before merge. Origin: KS-1579 (follow-ups from the Opus delta gate on pull request 1497 round 6), items 3 and 4 ONLY. Items 1 (published description wording, which edits originate.openapi.ts and the generated yaml), 2 (a new real-Postgres cell) and 5 (a legacy-key divergence, read from code only) are NOT in this brief and are not touched. Both files here are edited in place and neither is a product behaviour: one comment block, one `it(...)` title string. Link the PR as Refs KS-1579, never a close-word. No open PR touches either file (checked 2026-10-30 against the GitHub pulls API per-PR file lists).",
 products=[(P1,[(OLD1,NEW1)]),(P2,[(OLD2,NEW2)])],
 prodnote=['product, modified in place: ONE comment hunk, the two lines :219-220 inside the header block replaced by three lines','a TEST file used as the edited file, modified in place: ONE hunk, the single `it(` title line at :279 replaced by one line'],
 tests=[dict(path=TP,content=TEST)],
 testnote=['NEW file, jest, given in full below; 6 cells (4 red, 2 control); source-text reads of the two files above, no server'],
 runner='jest` (`npx jest src/__tests__/ks1579-erase-connector-comment-and-title-state-the-truth.test.ts` from `Blockchain/Dev/services/originate',
 tier='code_patch2', rung='3 (three files: two existing files with one comment/title hunk each, a new test given whole)',
 pins='''# code_patch2: originate connectorOrganisationErasure.ts (1 comment hunk) + ks695 refusals test (1 title hunk, used as the second edited file) + a NEW jest source-text file; ref = ks1061 (a jest file that reads source as text, shape only); line = the first changed line in the FIRST product.
tier=code_patch2
ref=Blockchain/Dev/services/originate/src/__tests__/ks1061-shared-mock-completeness.test.ts
line=219
ctx=65536
''',
 wrong="Two texts in the KS-695 erase-connector files say something the code no longer does or never did. (4) The header comment of `services/originate/src/services/connectorOrganisationErasure.ts` (:219-220) says a guard that reads live keys 'cannot see a key that was deleted or rotated away'. A rotation does not remove the old key: security's `retirePriorStatement` (`services/security/src/index.ts:215`) is an UPDATE that deactivates it (`is_active = false`) or shortens `expires_at`, and the guard reads inactive keys too, so a rotated key IS seen; only a DELETED key escapes it. (3) The unit cell at `__tests__/ks695-ask3-erase-connector-refusals.test.ts:279` is titled 'a key with a NULL, and one with an empty, connector id already got 403 from the ownership comparison and still does'. After round 6 the 403 for those keys is produced by the fallback refusal (the gate's direct resolver call gets `OrganisationErasureFallbackPrincipalError` for both), so 'already got 403 from the ownership comparison' no longer says why; the cell asserts only the status. Reword both. This brief is wording only.",
 where="- `services/originate/src/services/connectorOrganisationErasure.ts:219-220` - **must change**: the two comment lines (inside the `(2) a key with NO connector id` paragraph) become three lines (byte-exact in the diff below). `:218`, `:221` (`could never erase ...`) and everything else STAY.\n- `services/originate/src/__tests__/ks695-ask3-erase-connector-refusals.test.ts:279` - **must change**: the one `it('CONTROL - M-2 liveness is UNCHANGED: ...` title line. The body at :280-287 (the loop over `key-null-695` and `key-empty-695`) STAYS, byte for byte.\n- `ks695-ask3-erase-connector-fallback-principal.integration.test.ts:241` carries a similar title ('... are still 403 with nothing written'); it is NOT part of items 3 and 4 and is NOT touched.",
 exactnote="Two hunks in two files, each a single edit point. The first replaces two comment lines by three; the second replaces one title line by one line. Everything outside the `+`/`-` lines is context.\n",
 donot="**Do NOT touch** any other line of `connectorOrganisationErasure.ts` (the code, the `isFallbackConnectorId` predicate at :114, the other comment paragraphs), any other line of `ks695-ask3-erase-connector-refusals.test.ts` (the cell body at :280-287 least of all), the integration file, `originate.openapi.ts`, the generated yaml, or any other file.",
 testnote2="The test section is a NEW jest file given whole. The `+` lines are byte-exact. It reads the two files as text with `fs.readFileSync` and has no top-level await and no `jest.mock`.",
 red=['RED KS-1579 T1','RED KS-1579 T2','RED KS-1579 T3','RED KS-1579 T4'],
 cells="- RED `T1` (the header no longer contains `deleted or rotated away`), `T2` (it contains `cannot see a key that was DELETED: a rotation only deactivates or shortens the old key`), `T3` (the title no longer contains `already got 403 from the ownership comparison and still does`), `T4` (the title contains `is still refused 403 (this cell pins the status, not which refusal produces it)`): all fail by assertion at the tip, pass after the edits.\n- GREEN at the tip and after: `T5` (the retitled cell exists exactly once and still loops over `key-null-695` and `key-empty-695`) and `T6` (`isFallbackConnectorId` is still exported and the label `connector:api-key` is still named in the header file).",
 premises="- `connectorOrganisationErasure.ts:219-220` are the two comment lines quoted, :221 starts `could never erase`, :114 is `export function isFallbackConnectorId`; read at the tip by script, the golden is generated from the tree at the tip, not typed.\n- `ks695-ask3-erase-connector-refusals.test.ts:279` is the title line quoted and :283-285 the loop; read at the tip by script.\n- `services/security/src/index.ts:215` is `function retirePriorStatement(` (read at the tip); KS-1579 item 4 states it is an UPDATE of `svc_api_keys` and that the security source contains no `DELETE FROM svc_api_keys` (the ticket's measurement; the drafter read that the function exists, not its body).\n- Another jest test in the same directory reads sibling source with `fs.readFileSync(..., 'utf-8')` and `path.join(__dirname, ...)` (ks1061 :16-22, :61).",
 unmeasured="- The drafter did NOT run the new file; the RED-at-tip / GREEN-after result is the `round.sh --control` run on this golden.\n- Whether 'since round 6 the 403 comes from the fallback refusal' is true for every shape in that cell: the new title deliberately does NOT assert a reason, only that the cell pins the status. The reason is the ticket's measurement (the gate's direct resolver call), not the drafter's.\n- The body of security's `retirePriorStatement` was not re-read by the drafter; the new comment text relies on the ticket's statement that it deactivates or shortens expiry.\n- Whether any other file quotes the old title or the old header words: a tip-wide `git grep` found the old title only in this file at :279 (the integration file's :241 title is different text) and 'rotated away' only at :220.",
 scope="**KS-1579 items 3 and 4 only.** Items 1, 2 and 5 stay on the ticket. Link the PR as Refs KS-1579, never a close-word. Comment and title text only: no behaviour changes, not an auth/token edit.",
)
