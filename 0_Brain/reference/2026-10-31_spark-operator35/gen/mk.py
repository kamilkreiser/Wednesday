import os, sys, subprocess, textwrap
TIP = "cb2320368ae42fa793d81776fdd7fc8404ce312d"
STAMP = subprocess.check_output(["date", "+%Y-%m-%d %H:%M AEDT"]).decode().strip()
BR = "/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs"
SVC = "Blockchain/Dev/services/vc-issuer"

def test_credrepo():
    return '''import { describe, it, expect, vi, beforeEach } from 'vitest';

// KS-1868: credentialRepo.loadFromDb must still log its WARN when the thrown value
// itself cannot be read (a revoked Proxy throws on `instanceof`; an Error whose
// `message` getter throws, throws on `.message`).
// The db stand-in is a plain function, not a vi.fn(): a spy inspects what it
// rejects with and could itself fail on a revoked Proxy before the code under test saw it.
const h = vi.hoisted(() => ({
  toThrow: undefined as unknown,
  warn: vi.fn(),
}));

vi.mock('../db', () => ({
  isDbAvailable: () => true,
  query: (sql: string) =>
    /ORDER BY created_at/i.test(sql) ? Promise.reject(h.toThrow) : Promise.resolve({ rows: [] }),
}));

vi.mock('../utils/logger', () => ({
  logger: { info: vi.fn(), warn: h.warn, error: vi.fn(), debug: vi.fn() },
}));

import * as repo from '../repositories/credentialRepo';

const WARNS = () => h.warn.mock.calls.filter((c) => String(c[0]).includes('loadFromDb failed'));

describe('KS-1868 credentialRepo.loadFromDb reads the thrown value safely', () => {
  beforeEach(() => {
    h.toThrow = undefined;
    h.warn.mockReset();
  });

  it('control ks1868 C1 an ordinary Error still logs its message', async () => {
    h.toThrow = new Error('db down');
    await repo.loadFromDb();
    expect(WARNS()).toHaveLength(1);
    expect(WARNS()[0][1]).toEqual({ error: 'db down' });
  });

  it('RED ks1868 R1 a revoked Proxy thrown value logs a constant reason', async () => {
    const { proxy, revoke } = Proxy.revocable({}, {});
    revoke();
    h.toThrow = proxy;
    await repo.loadFromDb().catch(() => undefined);
    expect(WARNS()).toHaveLength(1);
    expect(WARNS()[0][1]).toEqual({ error: 'unreadable thrown value' });
  });

  it('RED ks1868 R2 an Error whose message getter throws logs a constant reason', async () => {
    h.toThrow = Object.create(Error.prototype, {
      message: {
        get() {
          throw new Error('getter boom');
        },
      },
    });
    await repo.loadFromDb().catch(() => undefined);
    expect(WARNS()).toHaveLength(1);
    expect(WARNS()[0][1]).toEqual({ error: 'unreadable thrown value' });
  });
});
'''

def test_pres():
    return '''import { describe, it, expect, vi, beforeEach } from 'vitest';

// KS-1868: loadPresentationsFromDb must still log its WARN when the thrown value
// itself cannot be read (a revoked Proxy throws on `instanceof`; an Error whose
// `message` getter throws, throws on `.message`).
// The db stand-in is a plain function, not a vi.fn(): a spy inspects what it
// rejects with and could itself fail on a revoked Proxy before the code under test saw it.
const h = vi.hoisted(() => ({
  toThrow: undefined as unknown,
  warn: vi.fn(),
}));

vi.mock('../db', () => ({
  isDbAvailable: () => true,
  query: () => Promise.reject(h.toThrow),
}));

vi.mock('../utils/logger', () => ({
  logger: { info: vi.fn(), warn: h.warn, error: vi.fn(), debug: vi.fn() },
}));

import { loadPresentationsFromDb } from '../routes/presentations';

const WARNS = () => h.warn.mock.calls.filter((c) => String(c[0]).includes('loadPresentationsFromDb failed'));

describe('KS-1868 loadPresentationsFromDb reads the thrown value safely', () => {
  beforeEach(() => {
    h.toThrow = undefined;
    h.warn.mockReset();
  });

  it('control ks1868 C1 an ordinary Error still logs its message', async () => {
    h.toThrow = new Error('db down');
    await loadPresentationsFromDb();
    expect(WARNS()).toHaveLength(1);
    expect(WARNS()[0][1]).toEqual({ error: 'db down' });
  });

  it('RED ks1868 R1 a revoked Proxy thrown value logs a constant reason', async () => {
    const { proxy, revoke } = Proxy.revocable({}, {});
    revoke();
    h.toThrow = proxy;
    await loadPresentationsFromDb().catch(() => undefined);
    expect(WARNS()).toHaveLength(1);
    expect(WARNS()[0][1]).toEqual({ error: 'unreadable thrown value' });
  });

  it('RED ks1868 R2 an Error whose message getter throws logs a constant reason', async () => {
    h.toThrow = Object.create(Error.prototype, {
      message: {
        get() {
          throw new Error('getter boom');
        },
      },
    });
    await loadPresentationsFromDb().catch(() => undefined);
    expect(WARNS()).toHaveLength(1);
    expect(WARNS()[0][1]).toEqual({ error: 'unreadable thrown value' });
  });
});
'''

TASKS = {
 "p1": dict(
  dir="ks_1868_o35_p1_credentialrepo_loadfromdb_unreadable_throw",
  prod=f"{SVC}/src/repositories/credentialRepo.ts",
  test=f"{SVC}/src/__tests__/ks1868-credentialrepo-loadfromdb-unreadable-throw.test.ts",
  fn="credentialRepo.loadFromDb", line=432, hunk_start=430,
  warn_line="    logger.warn('credentialRepo.loadFromDb failed — starting with empty store', {",
  slug="credentialRepo.ts loadFromDb catch", testsrc=test_credrepo, ref="ks1295-store-db-unavailable-warn.test.ts",
  extra="Note: `ensureTable()` (called first inside the same `try`) has its own `err?.message` catch at :46-48; it is NOT touched and is not reached by the cells, because the stand-in resolves the existence-check query and rejects only the `SELECT ... ORDER BY created_at` query."),
 "p2": dict(
  dir="ks_1868_o35_p2_presentations_loadpresentationsfromdb_unreadable_throw",
  prod=f"{SVC}/src/routes/presentations.ts",
  test=f"{SVC}/src/__tests__/ks1868-presentations-load-unreadable-throw.test.ts",
  fn="loadPresentationsFromDb", line=182, hunk_start=180,
  warn_line="    logger.warn('loadPresentationsFromDb failed — starting with empty store', {",
  slug="presentations.ts loadPresentationsFromDb catch", testsrc=test_pres, ref="ks1295-store-db-unavailable-warn.test.ts",
  extra=""),
}

def build(k):
    t = TASKS[k]
    d = os.path.join(BR, t["dir"]); os.makedirs(d, exist_ok=True)
    catch_line = "  } catch (err) {"
    err_old = "      error: err instanceof Error ? err.message : String(err),"
    ctx_tail1 = "    });"
    ctx_tail2 = "  }"
    prodhunk = [
      f"@@ -{t['hunk_start']},5 +{t['hunk_start']},11 @@",
      " " + catch_line,
      "+    let reason: string;",
      "+    try {",
      "+      reason = err instanceof Error ? err.message : String(err);",
      "+    } catch {",
      "+      reason = 'unreadable thrown value';",
      "+    }",
      " " + t["warn_line"],
      "-" + err_old,
      "+      error: reason,",
      " " + ctx_tail1,
      " " + ctx_tail2,
    ]
    prod_diff = "\n".join([f"--- a/{t['prod']}", f"+++ b/{t['prod']}"] + prodhunk)
    src = t["testsrc"]().rstrip("\n").split("\n")
    n = len(src)
    test_body = "\n".join("+" + l for l in src)
    test_diff = "\n".join([f"--- /dev/null", f"+++ b/{t['test']}", f"@@ -0,0 +1,{n} @@", test_body])
    golden = "\n".join([
        f"diff --git a/{t['prod']} b/{t['prod']}", prod_diff,
        f"diff --git a/{t['test']} b/{t['test']}", "new file mode 100644", test_diff]) + "\n"
    open(os.path.join(d, "golden.diff"), "w").write(golden)
    ref = f"{SVC}/src/__tests__/{t['ref']}"
    open(os.path.join(d, "spark.pins"), "w").write(
      f"# code_patch2: vc-issuer {os.path.basename(t['prod'])} (1 hunk) + a NEW vitest file; ref = ks1295 (same service, shape only); line = the changed line.\n"
      f"tier=code_patch2\nref={ref}\nline={t['line']}\nctx=65536\n"
      f"started_ok=KS-1868_is_Backlog;_vc-issuer_source_is_in_no_open_PR_(43_PRs_read_{STAMP[:10]},_positive_control_services/auth_in_20_lines);_not_in_the_S9_security_brief;_live_lanes_beyond_PRs_not_checked\n")
    md = f'''# KS-1868 vc-issuer: {t["fn"]}'s catch must still log its WARN when the thrown value cannot be read (one site of the 253; RUNG 3, code_patch2: one product hunk given as a skeleton, one NEW vitest file given whole)

DRAFT by Spark operator 35 for Wednesday, {STAMP}. Secuura (Platform K / vc-issuer) only. A local PASS is a candidate, never a merge; the normal QA gate before merge. Origin: KS-1868 (253 catch sites read a thrown value as `X instanceof Error ? X.message : String(X)`; none is guarded against a thrown value whose read itself throws, e.g. a revoked Proxy). This brief fixes ONE site, inline, with no shared helper: the catch block of `{t["fn"]}` in vc-issuer `{os.path.basename(t["prod"])}`. Today a hostile thrown value makes the catch block itself throw, so the WARN line is never logged and the function REJECTS instead of starting with an empty store (a boot-time load whose whole point is to not abort startup). No open PR touches vc-issuer source (the only vc-issuer files in the 43 open PRs read {STAMP[:10]} through the GitHub API are package.json and package-lock.json; planted positive control: the same scan finds services/auth in 20 lines of its output).

File: `{t["prod"]}`  (product, modified in place: ONE hunk)
Test file: `{t["test"]}`  (NEW file, vitest, given in full below; 3 cells (2 red, 1 control))
Tip: `{TIP}` (origin develop; every line number and quote below was read from it)
Runner: `vitest` (`npx vitest run src/__tests__/{os.path.basename(t["test"])}` from `Blockchain/Dev/services/vc-issuer`)
Tier: `code_patch2`
Rung: **3 (one product hunk, skeleton dictated; new test given whole)**

## The mode - read this twice

CODE+TEST. Your diff touches EXACTLY 2 file(s), in this order:
1. `{t["prod"]}` - modified in place: EXACTLY the one hunk under "The exact change", byte for byte.
2. `{t["test"]}` - a NEW file: `--- /dev/null` (NEVER `--- a/`), `+++ b/<path>`, ONE hunk `@@ -0,0 +1,{n} @@`, every line `+`.

You never touch any other file and no other line of the files above.

## What is wrong (one paragraph)

In `{os.path.basename(t["prod"])}` the catch block of `{t["fn"]}` (starts at line {t["hunk_start"]}) logs `logger.warn(..., {{ error: err instanceof Error ? err.message : String(err) }})` (line {t["line"]}). If the thrown value is a revoked Proxy, `err instanceof Error` itself throws a TypeError ("Cannot perform 'getPrototypeOf' on a proxy that has been revoked") inside the catch block; if it is an Error whose `message` getter throws, `err.message` throws. Either way the WARN is not logged and the function rejects. The fix reads the thrown value inside its own inner `try` into a local `reason`, falling back to the constant `unreadable thrown value`, and the log line uses `reason`. Nothing else changes: an ordinary Error still logs `{{ error: <its message> }}`, and the message text of the WARN is unchanged. {t["extra"]}

## Where

`{t["prod"]}:{t["line"]}` (the `error:` property line, third line of the catch block's `logger.warn` call). The catch block starts at line {t["hunk_start"]}.

## The exact change

ONE hunk in the product file. The file header lines and the `@@` header are DICTATED: copy them character for character, do not recount. Context lines start with ONE space, the removed line with `-`, added lines with `+` (byte-exact; four spaces for the new statements inside the catch, six inside the inner try/catch). The WARN line (the second context line below) contains an em dash; copy it unchanged.

```diff
{prod_diff}
```

**Do NOT touch** the `logger.warn` message text, any other line of the file, or any other catch block in it.

## The test

File: `{t["test"]}`

The test section is a NEW vitest file given whole. The `+` lines are byte-exact. The shape is copied from `{SVC}/src/__tests__/{t["ref"]}` (a `vi.hoisted` holder, `vi.mock('../db')`, `vi.mock('../utils/logger')`, then the import). There is no database, no app boot and no network here.

```diff
{test_diff}
```

## Red cells
- RED ks1868 R1
- RED ks1868 R2

## Cells and controls

- RED at the tip, GREEN after: `R1` (revoked Proxy) and `R2` (Error whose `message` getter throws). At the tip the function rejects (each cell swallows that rejection, so the failure is the assertion that exactly one WARN was logged); after the edit the WARN carries `{{ error: 'unreadable thrown value' }}`.
- GREEN at the tip and after: 'control ks1868 C1' (an ordinary `Error('db down')` logs `{{ error: 'db down' }}`), the control showing the normal path is unchanged.
- The db stand-in is a plain function, not `vi.fn()`, on purpose: a vitest spy inspects what it rejects with and may fail on a revoked Proxy before the code under test sees it.

## Premises (each one measured, with where)

- `{t["prod"]}:{t["line"]}` is `{err_old.strip()}` at the tip (git grep for `instanceof Error` over vc-issuer non-test source at the tip: exactly this site and its sibling in the other vc-issuer file, `credentialRepo.ts:432` / `presentations.ts:182`).
- The catch block spans lines {t["hunk_start"]}-{t["hunk_start"]+4} at the tip (read whole with `git show`).
- Open PRs: 43 read {STAMP[:10]} via the GitHub REST API (pulls?state=open, then pulls/N/files); the only vc-issuer paths are package.json x2 and package-lock.json x1; the positive control services/auth appears in 20 lines of the scan output.

## UNMEASURED - stated rather than glossed

- The golden is written by the operator from the diff design; it is proved by the harness `--control` run (round.sh), not by this text. tsc and eslint on the new file were not run outside the checker. The other 252 sites were not touched or measured. Whether a real path throws such a value here is not known (KS-1868 says the same). The `boot` path of the service (index.ts calling this loader) was not run.

## Scope

**This one site only.** Refs KS-1868; does NOT close it, and introduces no shared helper.

## Output

Exactly ONE fenced ```diff block, nothing outside it: 2 file section(s) in the order of `## The mode`; the first section starts `diff --git a/<path> b/<path>`; a NEW file's section is `diff --git`, `new file mode 100644`, `--- /dev/null` (NEVER `--- a/`), `+++ b/<path>`, then the hunk header `@@ -0,0 +1,N @@` and every body line starting `+`. The opening fence line is exactly ```diff. Every `+` line on its own physical line. Every context line keeps its leading space. Use the dictated `@@` header unchanged.
'''
    open(os.path.join(d, "KS-1868.md"), "w").write(md)
    print(k, d, n)

for k in sys.argv[1:]: build(k)
