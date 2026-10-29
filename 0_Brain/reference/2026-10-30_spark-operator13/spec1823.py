# KS-1823 (Seat D 43rd evidence, filed 2026-10-30): demo's api-gateway image carries two old OpenAPI yaml backups from the host's docs/openapi dir.
# Spark operator 13. First attempt was a .dockerignore edit; the builder refuses a product at the Dev root (one service per brief), so this is the gateway Dockerfile instead.
# code_patch2: 1 Dockerfile hunk (comment + one RUN line) + 1 NEW vitest source-text file in api-gateway. gen/mk.py.
P='Blockchain/Dev/services/api-gateway/Dockerfile'
TP='Blockchain/Dev/services/api-gateway/src/__tests__/ks1823-dockerfile-drops-spec-backups.test.ts'
E1=("# Relax strict unused-variable checks for production build\n",
    "# KS-1823: the host directory can also hold rollback copies of the spec; the gateway reads secuura-api.yaml only.\nRUN rm -f ./docs/openapi/*.pre-* ./docs/openapi/*.rollback-*\n# Relax strict unused-variable checks for production build\n")
TEST=r'''// KS-1823 (api-gateway image): the builder stage copies the whole docs/openapi directory (`COPY docs/openapi/ ./docs/openapi/`), so the two rollback copies of the spec that sit on the demo host
// (secuura-api.yaml.pre-ks508, secuura-api.yaml.rollback-2026-08-27-ks661) were baked into demo's image. These cells read the Dockerfile and the gateway source as text.
// R1 to R3 are red until the builder stage removes the rollback copies right after that COPY; C1 to C5 pin what must not move, in particular that the spec the gateway reads is still copied.
import { describe, it, expect } from 'vitest';
import { readFileSync } from 'fs';
import { resolve } from 'path';

const DOCKERFILE = readFileSync(resolve(__dirname, '..', '..', 'Dockerfile'), 'utf8').split('\n');
const GATEWAY_INDEX = readFileSync(resolve(__dirname, '..', 'index.ts'), 'utf8');

const COPY_SPEC = 'COPY docs/openapi/ ./docs/openapi/';
const COPY_AT = DOCKERFILE.indexOf(COPY_SPEC);
const RM_LINE = 'RUN rm -f ./docs/openapi/*.pre-* ./docs/openapi/*.rollback-*';
const RM_AT = DOCKERFILE.indexOf(RM_LINE);
const RUNTIME_STAGE_AT = DOCKERFILE.findIndex((l, i) => i > COPY_AT && l.startsWith('FROM '));

describe('KS-1823: the api-gateway image does not carry the spec rollback copies', () => {
  it('RED KS-1823 R1 the builder stage removes the pre-ks508 style rollback copies', () => {
    expect(DOCKERFILE.some((l) => l.startsWith('RUN rm -f') && l.includes('./docs/openapi/*.pre-*'))).toBe(true);
  });

  it('RED KS-1823 R2 the builder stage removes the rollback-dated copies', () => {
    expect(DOCKERFILE.some((l) => l.startsWith('RUN rm -f') && l.includes('./docs/openapi/*.rollback-*'))).toBe(true);
  });

  it('RED KS-1823 R3 the removal is the single line given, after the spec COPY, before the build, and before the runtime stage', () => {
    expect(RM_AT).toBeGreaterThan(COPY_AT);
    expect(RM_AT).toBeLessThan(RUNTIME_STAGE_AT);
    expect(RM_AT - COPY_AT).toBeLessThanOrEqual(4);
  });

  it('control KS-1823 C1 the whole-directory spec COPY is still there (the spec is still copied)', () => {
    expect(COPY_AT).toBeGreaterThan(-1);
  });

  it('control KS-1823 C2 the runtime stage still copies the directory from the builder', () => {
    expect(DOCKERFILE).toContain('COPY --from=builder /app/docs/openapi ./docs/openapi');
  });

  it('control KS-1823 C3 no line removes the spec itself or the whole directory', () => {
    const rmLines = DOCKERFILE.filter((l) => /\brm\b/.test(l) && l.includes('docs/openapi'));
    for (const l of rmLines) {
      expect(l).not.toContain('secuura-api.yaml');
      expect(l).not.toMatch(/docs\/openapi\/?\s*$/);
      expect(l).not.toMatch(/docs\/openapi\/\*(\s|$)/);
    }
  });

  it('control KS-1823 C4 the gateway still reads docs/openapi/secuura-api.yaml', () => {
    expect(GATEWAY_INDEX).toContain('docs/openapi/secuura-api.yaml');
  });

  it('control KS-1823 C5 the instrument reads real files (the Dockerfile has several stages and the gateway source is not empty)', () => {
    expect(DOCKERFILE.filter((l) => l.startsWith('FROM ')).length).toBeGreaterThanOrEqual(3);
    expect(GATEWAY_INDEX.length).toBeGreaterThan(5000);
  });
});
'''
S=dict(dir='ks_1823_p1_dockerfile',ticket='KS-1823',
 title='Demo api-gateway image carries two old OpenAPI yaml backups (pre-ks508, rollback ks661): remove them in the Dockerfile builder stage after the docs/openapi COPY (RUNG 3, code_patch2: one Dockerfile hunk of two added lines + one NEW source-text vitest file; no TypeScript changes)',
 intro="DRAFT by Spark operator 13 for Wednesday, 2026-10-30 AEDT. Secuura only (Platform K, api-gateway build). A local PASS is a candidate, never a merge; the normal QA gate before merge. A deploy is a separate, human step: this brief changes a Dockerfile and adds a test only. A first draft edited `Blockchain/Dev/.dockerignore` (shared by every service); the Spark builder refuses a product at the Dev root (one service per brief), and the Dockerfile is the narrower change anyway, so that draft is quarantined. Link the PR as Refs KS-1823, never a close-word.",
 products=[(P,[E1])],
 prodnote=['Dockerfile, modified in place: ONE hunk, two lines added after the spec COPY of the builder stage (no existing line changes)'],
 tests=[dict(path=TP,content=TEST)],
 testnote=['NEW file, vitest, given in full below; 8 cells (3 red, 5 control; reads the Dockerfile and the gateway `index.ts` as text)'],
 runner='vitest` (`npx vitest run src/__tests__/ks1823-dockerfile-drops-spec-backups.test.ts` from `Blockchain/Dev/services/api-gateway',
 tier='code_patch2', rung='3 (a Dockerfile hunk of two added lines, and a new test given whole)',
 pins='''# code_patch2: api-gateway Dockerfile (1 hunk, 2 added lines) + a NEW vitest source-text file; ref = an api-gateway test that reads files by path from __dirname (shape only); line = the first changed line in the FIRST product.
tier=code_patch2
ref=Blockchain/Dev/services/api-gateway/src/__tests__/ks1054-startup-migration-failure-on-health.test.ts
line=34
ctx=65536
''',
 wrong="The api-gateway Dockerfile builder stage runs `COPY docs/openapi/ ./docs/openapi/` (`Dockerfile:32`) and the runtime stage copies that directory on (`COPY --from=builder /app/docs/openapi ./docs/openapi`, `:69`). The demo host's `docs/openapi` also holds two rollback copies of the spec, `secuura-api.yaml.pre-ks508` and `secuura-api.yaml.rollback-2026-08-27-ks661` (Seat D 43rd's evidence: demo's image has them, kintsugi's does not), so both were baked into demo's image. The gateway reads only `docs/openapi/secuura-api.yaml` (`api-gateway/src/index.ts:590-592`), and a search of its non-test source for `express.static` finds nothing, so this is hygiene, not a stated exposure. The smallest fix is one `RUN rm -f` line right after that COPY removing exactly the two name shapes (`*.pre-*`, `*.rollback-*`) inside `docs/openapi`; the two markdown files kintsugi carries and the spec stay. No TypeScript changes.",
 where="- `services/api-gateway/Dockerfile:32` - (correct, STAYS) `COPY docs/openapi/ ./docs/openapi/`.\n- `services/api-gateway/Dockerfile:33` - (blank line, STAYS); :34 is `# Relax strict unused-variable checks for production build` (STAYS).\n- **The two new lines go between the blank line :33 and the comment `# Relax strict unused-variable checks for production build` (:34)**: one comment line and the `RUN rm -f` line, byte-exact in the diff below. No existing line changes.",
 exactnote="ONE hunk in the Dockerfile (two added lines: a comment and one RUN).\n",
 donot="**Do NOT touch** any existing Dockerfile line, `.dockerignore`, or any TypeScript file.",
 testnote2="The test section is a NEW file given whole. The `+` lines are byte-exact. The new file is pure ASCII, uses `vitest` imports, reads the two files with `readFileSync` relative to `__dirname`, and has no top-level await.",
 red=['RED KS-1823 R1','RED KS-1823 R2','RED KS-1823 R3'],
 cells="- RED `R1` and `R2`: at the tip no `RUN rm -f` line names either pattern.\n- RED `R3`: at the tip the `RUN` line is absent (index -1), so the ordering assertions fail.\n- CONTROL `C1` to `C5`: green at the tip AND after (the COPY lines stay, no `rm` line touches the spec or the whole directory, the gateway still reads the spec, both reads are non-empty).",
 premises="- `Dockerfile:32` is `COPY docs/openapi/ ./docs/openapi/` and `:69` is the runtime copy (read by script at the tip; the golden is generated from the tree at the tip, not typed).\n- `index.ts:590-592` is the single-file read (the ticket's read; the drafter re-read it at the tip).\n- The Dockerfile has three `FROM` stages (shared-builder, builder, runtime) and the builder's WORKDIR is the directory the relative `COPY` paths resolve under, so `./docs/openapi/` in the `RUN` line is the same directory as the COPY destination.",
 unmeasured="- No image was built: the drafter did NOT run `docker build` or inspect any image. The test measures the Dockerfile's lines, not what an image contains. That `rm -f` with an unmatched glob leaves the build green (it does under `sh` without `nullglob`, since the literal pattern is passed to `rm -f`) is the drafter's reading, not a build.\n- The deploy rsync (whether it runs with `--delete`) was not read; the host will still hold the two files.\n- Whether anything reads the two markdown files in the image: not searched (they are left in place).",
 scope="**KS-1823 only: the image-contents hygiene.** Removing the two files from the host is a separate human step. Link the PR as Refs KS-1823, never a close-word.",
)
