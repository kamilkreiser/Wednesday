# Operator 49, task 2 (KS-1868 security index.ts :293 and :400): code_patch2 brief generator (O47 shape).
import sys, os, importlib.util
MK='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/gen/mk.py'
spec=importlib.util.spec_from_file_location('mk',MK); mk=importlib.util.module_from_spec(spec); spec.loader.exec_module(mk)
TIP=mk.TIP='d7691f35312ea158f043e87a3227e477cccb183d'
BR='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/'
SV='Blockchain/Dev/services/security/'
PROD=SV+'src/index.ts'
REF=SV+'src/__tests__/ks1556-connector-chain.test.ts'
MSG='KS-577: revoke-on-rotate FAILED'

def mknew(old,ind):
    marker='error: err instanceof Error ? err.message : String(err)'
    assert old.count(marker)==1
    s=' '*ind
    head=(s+"let reason: string;\n"+s+"try {\n"+s+"  reason = err instanceof Error ? err.message : String(err);\n"+s+"} catch {\n"+s+"  reason = 'unreadable thrown value';\n"+s+"}\n")
    return head+old.replace(marker,'error: reason')

CASES='''
  it('control ks1868 C1 an ordinary Error still logs its message and %(okname)s', async () => {
    h.toThrow = new Error('db down');
%(act)s
%(ok)s
    expect(LINES()).toHaveLength(1);
    expect(LINES()[0].error).toBe('db down');
  });

  it('RED ks1868 R1 a revoked Proxy thrown value logs a constant reason and %(okname)s', async () => {
    const { proxy, revoke } = Proxy.revocable({}, {});
    revoke();
    h.toThrow = proxy;
%(act)s
%(ok)s
    expect(LINES()).toHaveLength(1);
    expect(LINES()[0].error).toBe('unreadable thrown value');
  });

  it('RED ks1868 R2 an Error whose message getter throws logs a constant reason and %(okname)s', async () => {
    h.toThrow = Object.create(Error.prototype, {
      message: {
        get() {
          throw new Error('getter boom');
        },
      },
    });
%(act)s
%(ok)s
    expect(LINES()).toHaveLength(1);
    expect(LINES()[0].error).toBe('unreadable thrown value');
  });
});
'''
COMMON_TOP='''import { describe, it, expect, vi, beforeAll, beforeEach, afterEach } from 'vitest';

process.env.SECURITY_DISABLE_BOOT = '1';

// KS-1868: %(what)s must still log its line and %(carry)s when the thrown value itself cannot be
// read (a revoked Proxy throws on `instanceof`; an Error whose `message` getter throws, throws on `.message`).
// The db stand-in rejects with a plain function, not a vi.fn(): a spy inspects what it rejects with and could
// itself fail on a revoked Proxy before the code under test saw it. The outcome is captured with
// `.then(onOk, onReject)` so the hostile value is never handed to an assertion message.
// The service logs through console.log (JSON lines), so the log is read from a console.log spy.
const h = vi.hoisted(() => ({
  toThrow: undefined as unknown,
  sql: [] as string[],
}));

%(mock)s

const TENANT = 'c0000000-0000-4000-8000-000000001868';
const CONNECTOR = 'ks1868-connector';
const LOGGED: string[] = [];
const LINES = () =>
  LOGGED.filter((s) => s.includes('KS-577: revoke-on-rotate FAILED')).map((s) => JSON.parse(s) as { error: unknown });

%(decl)s

beforeAll(async () => {
  const mod = await import('../index');
%(assign)s
});

beforeEach(() => {
  h.toThrow = undefined;
  h.sql.length = 0;
  LOGGED.length = 0;
%(reset)s
  vi.spyOn(console, 'log').mockImplementation((...args: unknown[]) => {
    LOGGED.push(String(args[0]));
  });
});

afterEach(() => {
  vi.restoreAllMocks();
});

describe('KS-1868 %(what)s reads the thrown value safely', () => {'''

T={}
T['p1']=dict(dir='ks_1868_o49_p1_security_revoke_prior_connector_keys_unreadable_throw', fn='revokePriorConnectorKeys', line=293, ind=4,
  test=SV+'src/__tests__/ks1868-security-revoke-prior-connector-keys-unreadable-throw.test.ts',
  oldblock="    log('error', 'KS-577: revoke-on-rotate FAILED — the prior credential is still valid', {\n      connectorId, tenantId, keepKeyId, error: err instanceof Error ? err.message : String(err),\n    });\n",
  indent=4,
  top=dict(what='`revokePriorConnectorKeys`',carry='return null (the KS-577 contract)',
    mock="""vi.mock('../db', () => ({
  isDbAvailable: () => true,
  initDb: async () => true,
  query: () => Promise.reject(h.toThrow),
}));""",
    decl="let revokePriorConnectorKeys: (connectorId: string, tenantId: string, keepKeyId: string) => Promise<number | null>;",
    assign="  revokePriorConnectorKeys = mod.revokePriorConnectorKeys;", reset=""),
  cases=dict(okname='the function still answers null',
    act="    const outcome = await revokePriorConnectorKeys(CONNECTOR, TENANT, 'new-key').then(\n      (value) => ({ rejected: false, value }),\n      () => ({ rejected: true, value: undefined }),\n    );",
    ok="    expect(outcome).toEqual({ rejected: false, value: null });"),
  descr=dict(
   site_intro="the catch block of `revokePriorConnectorKeys` in `services/security/src/index.ts` (the database leg of the KS-577 revoke-on-rotate)",
   consequence="Today a hostile rejection from the database layer makes the catch block itself throw, so nothing is logged and the function rejects instead of returning `null`.",
   red1="At the tip the function rejects (outcome `rejected: true`) and nothing is logged, so the outcome assertion fails",
   whatwrong="In `index.ts`, `revokePriorConnectorKeys` retires the connector's prior in-memory keys, then (database available) runs the retire UPDATE; its catch logs `log('error', 'KS-577: revoke-on-rotate FAILED ...', { connectorId, tenantId, keepKeyId, error: err instanceof Error ? err.message : String(err) })` (the read is on line 293) and returns `null`, the KS-577 contract for a failed retire. If the UPDATE rejects with a revoked Proxy, `err instanceof Error` itself throws a TypeError inside the catch; if it rejects with an Error whose `message` getter throws, `err.message` throws. Either way the catch throws before the line is logged and before `return null`, so the function rejects with the hostile value. The fix reads the thrown value inside its own inner `try` into a local `reason`, falling back to the constant `unreadable thrown value`, and the log call uses `reason`. Nothing else changes: an ordinary Error still logs `error: <its message>`.",
   callers="CALLERS (git grep at the tip, services/security/src): `saveKeyAndRetirePriors` at :380 inside its `!isDbAvailable()` branch, and the unit test seam `ks577-revoke-on-rotate.test.ts`. At :380 the database is unavailable, and `revokePriorConnectorKeys` itself returns at :280 (`if (!isDbAvailable()) return retired;`) BEFORE the try, so through the rotate route the :293 catch is reachable only if the availability flag flips between those two reads. In that window a hostile throw today makes `saveKeyAndRetirePriors` reject, and the route (:1399) answers 503/500 `The API key could not be saved` and drops the in-memory key; after the fix it returns `null` and the route answers 201 with `priorKeysRevoked: null`, as an ordinary DB error already does.",
   dbnote="`../db` is replaced (`isDbAvailable` true, `query` rejecting with the thrown value); no database, no port. `SECURITY_DISABLE_BOOT=1` keeps the import of `../index` from binding its port, as `ks577-revoke-on-rotate.test.ts` does. The function is exported (the KS-577 test seam), so it is called directly."))
T['p2']=dict(dir='ks_1868_o49_p2_security_save_key_and_retire_priors_unreadable_throw', fn='saveKeyAndRetirePriors', line=400, ind=8,
  test=SV+'src/__tests__/ks1868-security-save-key-and-retire-priors-unreadable-throw.test.ts',
  oldblock="        log('error', 'KS-577: revoke-on-rotate FAILED — the prior credential is still valid', {\n          connectorId, tenantId: k.tenantId, keepKeyId: k.id, error: err instanceof Error ? err.message : String(err),\n        });\n",
  indent=8,
  top=dict(what='the rotate transaction of `saveKeyAndRetirePriors`',carry='let the mint stand with `priorKeysRevoked` null (the KS-577/KS-1549 contract)',
    mock="""vi.mock('../db', () => ({
  isDbAvailable: () => true,
  initDb: async () => true,
  query: async () => ({ rows: [], rowCount: 0 }),
  transaction: async (fn: (client: unknown) => Promise<unknown>) =>
    fn({
      query: (sql: string) => {
        h.sql.push(String(sql));
        if (/^\\s*UPDATE\\s+svc_api_keys/i.test(String(sql))) return Promise.reject(h.toThrow);
        return Promise.resolve({ rows: [], rowCount: 0 });
      },
    }),
}));""",
    decl="""let saveKeyAndRetirePriors: (k: unknown, connectorId: string) => Promise<number | null>;
let memApiKeys: Map<string, unknown>;
const KEY = {
  id: 'key_ks1868',
  tenantId: TENANT,
  connectorId: CONNECTOR,
  name: 'ks1868',
  keyHash: 'ks1868-hash',
  keyPrefix: 'ks1868',
  scopes: [] as string[],
  usageCount: 0,
  isActive: true,
  createdAt: new Date(),
};""",
    assign="  saveKeyAndRetirePriors = mod.saveKeyAndRetirePriors as unknown as typeof saveKeyAndRetirePriors;\n  memApiKeys = mod.memApiKeys as unknown as Map<string, unknown>;", reset="  memApiKeys.clear();\n  delete process.env.API_KEY_ROTATION_GRACE_SECONDS;"),
  cases=dict(okname='the mint stands with a null retire count',
    act="    const outcome = await saveKeyAndRetirePriors(KEY, CONNECTOR).then(\n      (value) => ({ rejected: false, value }),\n      () => ({ rejected: true, value: undefined }),\n    );",
    ok="    expect(outcome).toEqual({ rejected: false, value: null });\n    expect(h.sql).toContain('ROLLBACK TO SAVEPOINT ks1549_retire');\n    expect(memApiKeys.has(KEY.id)).toBe(true);"),
  descr=dict(
   site_intro="the savepoint catch inside the rotate transaction of `saveKeyAndRetirePriors` in `services/security/src/index.ts`",
   consequence="Today a hostile rejection of the retire UPDATE makes the catch block itself throw AFTER `ROLLBACK TO SAVEPOINT`, so the throw leaves the transaction callback, the transaction (`db.ts transaction()`) issues ROLLBACK for the WHOLE transaction (the key INSERT included) and the rotate fails with no key.",
   red1="At the tip `saveKeyAndRetirePriors` rejects (outcome `rejected: true`), the new key is not in memory, so the outcome assertion fails",
   whatwrong="In `index.ts`, `saveKeyAndRetirePriors` mints the new key and retires the connector's prior keys in ONE transaction; the retire runs under the savepoint `ks1549_retire` so that a failed retire rolls back alone and the mint stands (KS-577 + KS-1549: `null` means the retire failed, the new key still stands, and the route reports `priorKeysRevoked: null`). The catch at :397-403 runs `ROLLBACK TO SAVEPOINT`, then logs `log('error', 'KS-577: revoke-on-rotate FAILED ...', { connectorId, tenantId: k.tenantId, keepKeyId: k.id, error: err instanceof Error ? err.message : String(err) })` (the read is on line 400) and returns `null`. If the UPDATE rejects with a revoked Proxy, `err instanceof Error` itself throws a TypeError inside the catch; if it rejects with an Error whose `message` getter throws, `err.message` throws. Either way the catch throws before the line is logged and before `return null`, which aborts the callback. The fix reads the thrown value inside its own inner `try` into a local `reason`, falling back to the constant `unreadable thrown value`, and the log call uses `reason`. Nothing else changes: an ordinary Error still logs `error: <its message>`.",
   callers="CALLERS (git grep at the tip): the only caller is the register/mint route `POST /api/keys` at :1395 (`priorKeysRevoked = await saveKeyAndRetirePriors(apiKey, data.connectorId)`, only when `data.rotate && data.connectorId`), inside a try whose catch (:1399-1407) drops the in-memory key and answers 503/500 `The API key could not be saved, so no key was issued`; on success the 201 body carries `priorKeysRevoked`. **BEHAVIOUR CHANGE the raise PR must state:** for a hostile throw from the retire UPDATE, a rotate today FAILS (500, no key issued, nothing committed, the prior key still live and nothing persisted); after the fix it MINTS (the transaction COMMITs the new key), the prior key is left active, and the 201 body reports `priorKeysRevoked: null`. That is exactly what an ordinary DB error from the retire UPDATE already does (the KS-577 contract: the old credential is still valid, the operator is told).",
   dbnote="`../db` is replaced: `isDbAvailable` true, `transaction` runs the callback with a stand-in client whose `query` records the SQL text and rejects (with the thrown value) only for the `UPDATE svc_api_keys` retire statement; every other statement (SET TRANSACTION, set_config, advisory lock, INSERT, SAVEPOINT, ROLLBACK TO SAVEPOINT) resolves. The stand-in does not emulate COMMIT/ROLLBACK of the whole transaction; the cell watches what `saveKeyAndRetirePriors` returns, that `ROLLBACK TO SAVEPOINT ks1549_retire` ran, and that the key is in `memApiKeys` (which is set only after the transaction callback returns)."))

def build(k):
    X=T[k]
    old=mk.rd(PROD); assert old.count(X['oldblock'])==1
    new=old.replace(X['oldblock'],mknew(X['oldblock'],X['indent']))
    pd=mk.udiff(PROD,old,new); pd_body=pd.split('\n',1)[1]
    top=COMMON_TOP%X['top']
    tbody=top+(CASES%dict(X['cases']))
    td=mk.udiff(X['test'],'',tbody,True); nlines=len(tbody.splitlines())
    golden=pd+td
    d=BR+X['dir']; os.makedirs(d,exist_ok=True)
    open(d+'/golden.diff','w',encoding='utf-8').write(golden)
    pins=("# code_patch2: security index.ts (1 hunk) + a NEW test file; ref = shape only; line = the changed line.\ntier=code_patch2\nref=%s\nline=%d\nctx=65536\n"
          "started_ok=KS-1868_is_In_Progress_(umbrella_ticket,_file-disjoint_sites);_services/security_src/index.ts_and_src/__tests__/_are_in_no_open_PR_(23_PRs_134_files_read_2026-11-02_by_op49,_security_only_as_package.json_in_575/649,_positive_control_services/auth_in_10_entries);_live_lanes_beyond_PRs_not_checked\n")%(REF,X['line'])
    open(d+'/spark.pins','w').write(pins)
    D=X['descr']; tp=X['test'].split('/')[-1]
    txt=f"""# KS-1868 security: {X['fn']} must still report when the thrown value cannot be read (one site of the 253; RUNG 3, code_patch2: one product hunk given as a skeleton, one NEW test file given whole)

DRAFT by Spark operator 49 for Wednesday, 2026-11-02. Secuura (security) only. A local PASS is a candidate, never a merge; the normal QA gate before merge. Origin: KS-1868 (253 catch sites read a thrown value as `X instanceof Error ? X.message : String(X)`; none is guarded against a thrown value whose read itself throws, e.g. a revoked Proxy). This brief fixes ONE site, inline, with no shared helper: {D['site_intro']}. {D['consequence']} No open PR touches this file or its `src/__tests__/` directory (the 23 open PRs read 2026-11-02 through the GitHub API; 134 file entries; services/security appears only as package.json in PRs 575 and 649; planted positive control: the same scan finds services/auth in 10 entries). The other site of the same file (`revokePriorConnectorKeys` :293 / `saveKeyAndRetirePriors` :400) is a separate brief, one hunk each; the two hunks are 100+ lines apart and are meant for one sequenced PR.

File: `{PROD}`  (product, modified in place: ONE hunk)
Test file: `{X['test']}`  (NEW file, vitest, given in full below; 3 cells (2 red, 1 control))
Tip: `{TIP}` (origin develop; every line number and quote below was read from it)
Runner: `vitest` (`npx vitest run src/__tests__/{tp}` from `Blockchain/Dev/services/security`)
Tier: `code_patch2`
Rung: **3 (one product hunk, skeleton dictated; new test given whole)**

## The mode - read this twice

CODE+TEST. Your diff touches EXACTLY 2 file(s), in this order:
1. `{PROD}` - modified in place: EXACTLY the one hunk under "The exact change", byte for byte.
2. `{X['test']}` - a NEW file: `--- /dev/null` (NEVER `--- a/`), `+++ b/<path>`, ONE hunk `@@ -0,0 +1,{nlines} @@`, every line `+`.

You never touch any other file and no other line of the files above.

## What is wrong (one paragraph)

{D['whatwrong']}

## Where

`{PROD}:{X['line']}`. {D['callers']}

## The exact change

ONE hunk in the product file. The file header lines and the `@@` header are DICTATED: copy them character for character, do not recount. Context lines start with ONE space, removed lines with `-`, added lines with `+` (byte-exact; spaces only). The log message text contains an em dash; copy it unchanged.

```diff
{pd_body}```

The `+` lines are byte-exact: copy them. Indentation is spaces only. Context lines begin with one space (the diff marker) followed by the file text.

**Do NOT touch** any message text, any other line of the file, or any other catch block in it. The other KS-1868 site of this file is not this brief's.

## The test

File: `{X['test']}`

The test section is a NEW test file given whole. The `+` lines are byte-exact. The shape is copied from `{REF}` (`process.env.SECURITY_DISABLE_BOOT = '1'` before a dynamic `import('../index')`, as the service's other tests do). {D['dbnote']} **The test contains backslashes in regular-expression text (`\\s`): copy every backslash exactly.**

```diff
{td}```

## Red cells
- RED ks1868 R1
- RED ks1868 R2

## Cells and controls

- RED at the tip, GREEN after: `R1` (revoked Proxy) and `R2` (Error whose `message` getter throws). {D['red1']}; after the edit the result carries the constant `unreadable thrown value`.
- GREEN at the tip and after: 'control ks1868 C1' (an ordinary `Error` logs its own message), the control showing the normal path is unchanged.
- The stand-in rejecting with the thrown value is a plain function, not `vi.fn()`, on purpose: a vitest spy inspects what it rejects with and may fail on a revoked Proxy before the code under test sees it.

## Premises (each one measured, with where)

- `{PROD}:{X['line']}` is the `instanceof Error` read at the tip (read whole with `git show` at `{TIP[:12]}`).
- Open PRs: 23 read 2026-11-02 via the GitHub REST API (pulls?state=open, then pulls/N/files); none touches `{PROD}` or `src/__tests__/` (23 PRs, 134 file entries; services/security only as package.json); the positive control services/auth appears in 10 file entries.
- This file is neither `tenant-context.ts` nor `tenant-pool-manager.ts` and is outside services/auth, services/originate, services/anchoring, services/tenant-provisioning and vc-issuer; the S9 brief itself was not re-read by the operator.

## UNMEASURED - stated rather than glossed

- The golden is written by the operator from the diff design; it is proved by the harness `--control` run (round.sh), not by this text. tsc and eslint on the new file were not run outside the checker. The other sites of the 253 were not touched or measured. Whether a real path throws such a value here is not known (KS-1868 says the same). The service boot path and a real Postgres were not run.

## Scope

**This one site only.** Refs KS-1868; does NOT close it, and introduces no shared helper.

## Output

Exactly ONE fenced ```diff block, nothing outside it: 2 file section(s) in the order of `## The mode`; the first section starts `diff --git a/<path> b/<path>`; a NEW file's section is `diff --git`, `new file mode 100644`, `--- /dev/null` (NEVER `--- a/`), `+++ b/<path>`, then the hunk header `@@ -0,0 +1,N @@` and every body line starting `+`. The opening fence line is exactly ```diff. Every `+` line on its own physical line. Every context line keeps its leading space. Use the dictated `@@` header unchanged.
"""
    open(d+'/KS-1868.md','w',encoding='utf-8').write(txt)
    print('wrote',d); print(pd)
for k in sys.argv[1:]: build(k)
