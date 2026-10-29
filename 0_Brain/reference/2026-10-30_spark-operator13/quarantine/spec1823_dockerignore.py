# KS-1823 (Seat D 43rd evidence, filed 2026-10-30): demo's api-gateway image carries two old OpenAPI yaml backups from the host's docs/openapi dir.
# Spark operator 13. code_patch2: 1 .dockerignore hunk + 1 NEW vitest source-text file in api-gateway. gen/mk.py.
P='Blockchain/Dev/.dockerignore'
TP='Blockchain/Dev/packages/shared/src/__tests__/ks1823-dockerignore-keeps-spec-backups-out-of-the-image.test.ts'
E1=("!docs/openapi\ntests\n",
    "!docs/openapi\n# KS-1823: the host's docs/openapi also holds rollback copies of the spec; they must not ride into an image.\ndocs/openapi/*.pre-*\ndocs/openapi/*.rollback-*\ntests\n")
TEST=r'''// KS-1823 (api-gateway image): Blockchain/Dev/.dockerignore re-includes docs/openapi (`!docs/openapi`) and the gateway Dockerfile copies the whole directory, so the two rollback copies of the spec
// that sit on the demo host (secuura-api.yaml.pre-ks508, secuura-api.yaml.rollback-2026-08-27-ks661) were baked into demo's image. These cells read .dockerignore and the gateway source as text.
// R1 to R4 are red until two ignore lines are added after the re-include (last match wins in .dockerignore); C1 to C5 pin what must not move, in particular that the spec the gateway reads is still copied.
import { describe, it, expect } from 'vitest';
import { readFileSync } from 'node:fs';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
// packages/shared/src/__tests__ -> four levels up is Blockchain/Dev, the build-context root
const IGNORE = readFileSync(resolve(here, '../../../../.dockerignore'), 'utf8').split('\n');
const GATEWAY_INDEX = readFileSync(resolve(here, '../../../../services/api-gateway/src/index.ts'), 'utf8');

const REINCLUDE = IGNORE.indexOf('!docs/openapi');
const AFTER = REINCLUDE < 0 ? [] : IGNORE.slice(REINCLUDE + 1).filter((l) => l !== '' && !l.startsWith('#') && !l.startsWith('!'));

// a .dockerignore line is matched from the context root: `*` is any run of characters except `/`
function lineMatches(line: string, path: string): boolean {
  const rx = new RegExp('^' + line.replace(/[.+^${}()|[\]\\]/g, '\\$&').replace(/\*/g, '[^/]*') + '$');
  return rx.test(path);
}
const ignoredAfterReinclude = (path: string) => AFTER.some((l) => lineMatches(l, path));

describe('KS-1823: the api-gateway image does not carry the spec rollback copies', () => {
  it('RED KS-1823 R1 a line after the re-include excludes secuura-api.yaml.pre-ks508', () => {
    expect(ignoredAfterReinclude('docs/openapi/secuura-api.yaml.pre-ks508')).toBe(true);
  });

  it('RED KS-1823 R2 a line after the re-include excludes secuura-api.yaml.rollback-2026-08-27-ks661', () => {
    expect(ignoredAfterReinclude('docs/openapi/secuura-api.yaml.rollback-2026-08-27-ks661')).toBe(true);
  });

  it('RED KS-1823 R3 the exclusion is the pattern docs/openapi/*.pre-*', () => {
    expect(IGNORE).toContain('docs/openapi/*.pre-*');
  });

  it('RED KS-1823 R4 the exclusion is the pattern docs/openapi/*.rollback-*', () => {
    expect(IGNORE).toContain('docs/openapi/*.rollback-*');
  });

  it('control KS-1823 C1 the spec the gateway reads is NOT excluded', () => {
    expect(ignoredAfterReinclude('docs/openapi/secuura-api.yaml')).toBe(false);
  });

  it('control KS-1823 C2 the two markdown files that kintsugi carries are NOT excluded by the new lines', () => {
    expect(ignoredAfterReinclude('docs/openapi/WORKFLOWS.md')).toBe(false);
    expect(ignoredAfterReinclude('docs/openapi/TRACK2_OPENAPI_MIGRATION.md')).toBe(false);
  });

  it('control KS-1823 C3 the re-include of docs/openapi is still there, and so are the docs and nested __tests__ lines', () => {
    expect(IGNORE).toContain('docs');
    expect(IGNORE).toContain('!docs/openapi');
    expect(IGNORE).toContain('**/__tests__');
  });

  it('control KS-1823 C4 the gateway still reads docs/openapi/secuura-api.yaml', () => {
    expect(GATEWAY_INDEX).toContain("docs/openapi/secuura-api.yaml");
  });

  it('control KS-1823 C5 the instrument reads real files (the re-include was found and the gateway source is not empty)', () => {
    expect(REINCLUDE).toBeGreaterThan(-1);
    expect(GATEWAY_INDEX.length).toBeGreaterThan(5000);
  });
});
'''
S=dict(dir='ks_1823_p1_dockerignore',ticket='KS-1823',
 title='Demo api-gateway image carries two old OpenAPI yaml backups (pre-ks508, rollback ks661): exclude them in .dockerignore after the docs/openapi re-include (RUNG 3, code_patch2: one .dockerignore hunk + one NEW source-text vitest file; no TypeScript changes)',
 intro="DRAFT by Spark operator 13 for Wednesday, 2026-10-30 AEDT. Secuura only (Platform K, build config). A local PASS is a candidate, never a merge; the normal QA gate before merge. NOTE: `Blockchain/Dev/.dockerignore` is the build-context file of EVERY service built from the Dev root, so the QA gate should read the two new lines against every image, not only the gateway's; the lines match only files named `*.pre-*` and `*.rollback-*` directly inside `docs/openapi/`. A deploy is a separate, human step: this brief changes a file and a test only. Link the PR as Refs KS-1823, never a close-word.",
 products=[(P,[E1])],
 prodnote=['config, modified in place: ONE hunk, three lines added after the `!docs/openapi` line (no existing line changes)'],
 tests=[dict(path=TP,content=TEST)],
 testnote=['NEW file, vitest, given in full below; 9 cells (4 red, 5 control; reads `.dockerignore` and the gateway `index.ts` as text; it lives in packages/shared beside the KS-1289 test of the same file, because the builder maps a product at the Dev root to that package)'],
 runner='vitest` (`npx vitest run src/__tests__/ks1823-dockerignore-keeps-spec-backups-out-of-the-image.test.ts` from `Blockchain/Dev/packages/shared',
 tier='code_patch2', rung='3 (a config hunk of three added lines, and a new test given whole)',
 pins='''# code_patch2: .dockerignore (1 hunk, 3 added lines) + a NEW vitest source-text file; ref = the KS-1289 test that reads the same .dockerignore (shape only); line = the first changed line in the FIRST product.
tier=code_patch2
ref=Blockchain/Dev/packages/shared/src/__tests__/ks1289-dockerignore-excludes-nested-tests.test.ts
line=13
ctx=65536
''',
 wrong="The api-gateway Dockerfile builder stage runs `COPY docs/openapi/ ./docs/openapi/` (`Dockerfile:32`) and `Blockchain/Dev/.dockerignore` re-includes the directory (`!docs/openapi`, line 12) under its `docs` exclusion. The demo host's `docs/openapi` also holds two rollback copies of the spec, `secuura-api.yaml.pre-ks508` and `secuura-api.yaml.rollback-2026-08-27-ks661` (Seat D 43rd's evidence: demo's image has them, kintsugi's does not), so both were baked into demo's image. The gateway reads only `docs/openapi/secuura-api.yaml` (`api-gateway/src/index.ts:590-592`), and a search of its non-test source for `express.static` finds nothing, so this is hygiene, not a stated exposure. The fix is the smallest one: two ignore lines placed AFTER the re-include (last match wins in a .dockerignore), `docs/openapi/*.pre-*` and `docs/openapi/*.rollback-*`. The Dockerfile is not touched.",
 where="- `Blockchain/Dev/.dockerignore:12` - (correct, STAYS) `!docs/openapi`.\n- `Blockchain/Dev/.dockerignore:13` - (correct, STAYS) `tests`.\n- **The new lines go between :12 and :13**: one comment line and the two patterns, byte-exact in the diff below. No existing line changes.",
 exactnote="ONE hunk in `.dockerignore` (three added lines).\n",
 donot="**Do NOT touch** any existing `.dockerignore` line, the Dockerfile, or any TypeScript file.",
 testnote2="The test section is a NEW file given whole. The `+` lines are byte-exact. The new file is pure ASCII, uses `vitest` imports, reads the two files with `readFileSync` relative to `import.meta.url` (the same pattern as `ks1289-dockerignore-excludes-nested-tests.test.ts`), and has no top-level await.",
 red=['RED KS-1823 R1','RED KS-1823 R2','RED KS-1823 R3','RED KS-1823 R4'],
 cells="- RED `R1` and `R2`: at the tip no line after `!docs/openapi` matches either backup file name.\n- RED `R3` and `R4`: at the tip the two literal patterns are absent.\n- CONTROL `C1` to `C5`: green at the tip AND after (the live spec and the two markdown files are not matched by any line after the re-include; the existing lines stay; the gateway still reads the spec; both reads are non-empty).",
 premises="- `.dockerignore` lines 10-13 are `*.md`, `docs`, `!docs/openapi`, `tests` at the tip (read by script; the golden is generated from the tree at the tip, not typed).\n- `Dockerfile:32` is the whole-directory COPY and `index.ts:590-592` is the single-file read (the ticket's reads; the drafter re-read both at the tip).\n- The test's matcher treats `*` as any run of non-`/` characters, which is how `.dockerignore` (Go `filepath.Match`) treats it for these two patterns.",
 unmeasured="- No image was built: the drafter did NOT run `docker build` or inspect any image. The test measures the ignore file's lines, not what an image contains. Whether the build actually drops the two files is a separate, human check at the next deploy.\n- Whether any other service's image builds from the Dev root and expects a `docs/openapi/*.pre-*` file: not searched (the lines match only these two name shapes).\n- The deploy rsync (whether it runs with `--delete`) was not read; the host will still hold the two files.",
 scope="**KS-1823 only: the image-contents hygiene.** Removing the two files from the host is a separate human step. Link the PR as Refs KS-1823, never a close-word.",
)
