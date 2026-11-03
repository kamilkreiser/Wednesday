#!/bin/bash
# mut_h5.sh : is survivor H5 (drop the DOMException name probe) equivalent? Run a DOMException('AbortError') whose name
# getter throws through the dashboard oracle at head, at H5-mutated head, and at base. Restores the head blob after.
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate177-ks1868-pr1993
AG=$W/repo/Blockchain/Dev/services/api-gateway
sed -e "s#^const V17 = .*#const V17: Array<[string, () => unknown]> = [['VX DOMException AbortError whose name getter throws', () => { const e = new DOMException('gate177', 'AbortError'); Object.defineProperty(e, 'name', { get() { throw new Error('name boom'); } }); return e; }]];#" -e 's/oracle dashboard/oracle dom/' $W/harness/oracle_agw.test.ts > $W/harness/oracle_agw_dom.test.ts
echo "value line present: $(grep -ci 'VX DOMException' $W/harness/oracle_agw_dom.test.ts)"
mkdir -p $AG/src/__gate177__; cp $W/harness/oracle_agw_dom.test.ts $W/harness/values.ts $AG/src/__gate177__/
F=$AG/src/routes/health-dashboard.ts
git -C $W/repo show refs/gate/1993:Blockchain/Dev/services/api-gateway/src/routes/health-dashboard.ts > $W/tmp/hd.head.ts
for t in head H5 base; do
  case $t in
    head) cp $W/tmp/hd.head.ts $F;;
    H5) python3 -c "import sys;p=sys.argv[1];s=open(p).read();a='      void (error instanceof DOMException && error.name);\n';assert a in s;open(p,'w').write(s.replace(a,'',1))" $F;;
    base) git -C $W/repo show refs/gate/develop:Blockchain/Dev/services/api-gateway/src/routes/health-dashboard.ts > $F;;
  esac
  env -i PATH=/opt/homebrew/bin:/usr/bin:/bin HOME=$W/home TMPDIR=$W/tmp NODE_ENV=test $AG/node_modules/.bin/vitest run --root $AG --config $AG/vitest.gate177.agw.config.ts src/__gate177__/oracle_agw_dom.test.ts > $W/runs/mut_H5_dom_$t.txt 2>&1
  echo "$t rc=$? $(grep -oE 'Tests +.*(passed|failed)' $W/runs/mut_H5_dom_$t.txt | sed 's/\x1b\[[0-9;]*m//g' | head -1)"
done
cp $W/tmp/hd.head.ts $F
echo "repo clean vs head: $(git -C $W/repo diff --quiet HEAD -- Blockchain/Dev && echo yes || echo NO)"
