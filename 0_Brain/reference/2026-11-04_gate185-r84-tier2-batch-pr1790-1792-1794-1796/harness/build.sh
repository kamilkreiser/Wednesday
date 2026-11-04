# usage: build.sh <fn-file> <out>
H=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-04_gate185-r84-tier2-batch-pr1790-1792-1794-1796/cwd/h1790
{
cat <<'X'
import { createRequire } from 'node:module';
const req = createRequire('/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files/Blockchain/Dev/package.json');
const { Client } = req('pg');
const SHARED_STACK_PORTS: string[] = ['5432', '6432'];
X
cat "$1"
echo 'function T() {'
cat $H/tables.txt
cat <<'X'
  let pass = 0, fail = 0;
  const rep = (ok: boolean, n: string, e?: unknown) => { ok ? pass++ : fail++; console.log((ok ? 'PASS ' : 'FAIL ') + n + (ok ? '' : ' :: ' + String(e).slice(0, 100))); };
  for (const [what, dsn, why] of REFUSED) { try { disposableDsnTarget('TEST_DATABASE_URL', dsn); rep(false, 'refuses ' + what, 'did not throw'); } catch (e: any) { rep(why.test(String(e.message)), 'refuses ' + what, e.message); } }
  for (const [what, dsn, target] of ACCEPTED) { try { const r = disposableDsnTarget('TEST_DATABASE_URL', dsn); rep(r === target, 'accepts ' + what, r); } catch (e: any) { rep(false, 'accepts ' + what, e.message); } }
  console.log(`RAW pass=${pass} fail=${fail} total=${pass + fail}`);
}
T();
X
} > "$2"
