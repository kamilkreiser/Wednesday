#!/bin/bash
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate143-ks1868-pr1959; R=$W/repo; Q=$W/logs/q5b
[ -e $Q ] && { echo exists; exit 1; }
mkdir -p $Q/base $Q/p3 $Q/p1 $Q/o1 $Q/o2 $Q/full
F=events.ts
git -C $R show 2d3b3bb3:Blockchain/Dev/services/auth/src/events.ts > $Q/base/$F
git -C $R show pr1959:Blockchain/Dev/services/auth/src/events.ts > $Q/full/$F
python3 - <<'PY'
Q='/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate143-ks1868-pr1959/logs/q5b/'
b=open(Q+'base/events.ts').read(); f=open(Q+'full/events.ts').read()
g="""      let reason: string | null | undefined;
      try {
        const m = err?.message;
        reason = m === undefined || m === null ? m : String(m);
      } catch {
        reason = 'unreadable thrown value';
      }
      logger.debug('EventBus Redis error (non-fatal)', { error: reason });
"""
old3="      logger.debug('EventBus Redis error (non-fatal)', { error: err.message });\n"
assert old3 in b and g in f
open(Q+'p3/events.ts','w').write(b.replace(old3,g))
old1="    logger.warn('Failed to initialise EventBus', { error: err?.message });\n"
g1="""    let reason: string | null | undefined;
    try {
      const m = err?.message;
      reason = m === undefined || m === null ? m : String(m);
    } catch {
      reason = 'unreadable thrown value';
    }
    logger.warn('Failed to initialise EventBus', { error: reason });
"""
assert old1 in b
p1=b.replace(old1,g1); open(Q+'p1/events.ts','w').write(p1)
assert b.replace(old3,g).replace(old1,g1)==f; print('independent reconstruction of head from base + P3 + P1 == head: True')
PY
diff -U3 $Q/base/$F $Q/p3/$F | sed 's#^--- .*#--- a/events.ts#; s#^+++ .*#+++ b/events.ts#' > $Q/P3.patch
diff -U3 $Q/base/$F $Q/p1/$F | sed 's#^--- .*#--- a/events.ts#; s#^+++ .*#+++ b/events.ts#' > $Q/P1.patch
grep '^@@' $Q/P3.patch $Q/P1.patch
cp $Q/base/$F $Q/o1/$F; cp $Q/base/$F $Q/o2/$F
echo "== P3 then P1 (patch -F0, no fuzz)"; patch -F0 --no-backup-if-mismatch -p1 $Q/o1/$F < $Q/P3.patch; echo rc=$?; patch -F0 --no-backup-if-mismatch -p1 $Q/o1/$F < $Q/P1.patch; echo rc=$?
echo "== P1 then P3"; patch -F0 --no-backup-if-mismatch -p1 $Q/o2/$F < $Q/P1.patch; echo rc=$?; patch -F0 --no-backup-if-mismatch -p1 $Q/o2/$F < $Q/P3.patch; echo rc=$?
shasum -a 256 $Q/o1/$F $Q/o2/$F $Q/full/$F
echo "== git apply --check on a real git tree (clone worktree not touched): use git apply --check with --directory on files via index-less mode"
