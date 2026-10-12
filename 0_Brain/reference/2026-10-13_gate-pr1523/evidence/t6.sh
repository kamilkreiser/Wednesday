#!/usr/bin/env bash
# T6 failure modes. Mutations asserted; restores asserted.
S=<scratch>
G="git -C $S/repo"; Q=$S/quarantine; mkdir -p $Q
PAT='SKIP|OK —|FAIL —|cannot resolve|could not|HARNESS|examined'

echo "== T6a fresh linked worktree at head, NO install"
$G worktree add -q --detach $S/wt-noinst refs/gate/head
[ ! -e $S/wt-noinst/Blockchain/Dev/node_modules ] && echo "   precondition: no node_modules"
bash $S/harness/leg16.sh $S/wt-noinst/Blockchain/Dev > $S/ev/T6a.log 2>&1; echo "   rc=$?"; grep -E "$PAT" $S/ev/T6a.log | sed 's/^/   /'

echo "== T6b install present, typescript package removed (deps-present still passes)"
D=$S/wt-merged/Blockchain/Dev
mv $D/node_modules/typescript $Q/typescript-merged
bash $D/scripts/preflight/deps-present.sh >/dev/null 2>&1; echo "   deps-present rc=$? (0 = precondition holds)"
find $D/services/auth/node_modules $D/services/api-gateway/node_modules $D/services/vc-issuer/node_modules -maxdepth 1 -name typescript 2>/dev/null | sed 's/^/   nested ts: /'
bash $S/harness/leg16.sh $D > $S/ev/T6b.log 2>&1; echo "   rc=$?"; grep -E "$PAT" $S/ev/T6b.log | sed 's/^/   /'
mv $Q/typescript-merged $D/node_modules/typescript; [ -d $D/node_modules/typescript ] && echo "   restored"

echo "== T6c install present, packages/shared NOT built (dist moved away)"
mv $D/packages/shared/dist $Q/shared-dist-merged
bash $S/harness/leg16.sh $D > $S/ev/T6c.log 2>&1; echo "   rc=$?"; grep -E 'typecheck-tests:|FAIL —|HARNESS' $S/ev/T6c.log | sed 's/^/   /'
mv $Q/shared-dist-merged $D/packages/shared/dist; [ -d $D/packages/shared/dist ] && echo "   restored"

echo "== T6d invoked through a symlinked spelling (/tmp -> /private/tmp)"
L=${D/#\/private\/tmp/\/tmp}; echo "   path: $L"; [ -L /tmp ] && echo "   /tmp is a symlink"
bash $S/harness/leg16.sh $L > $S/ev/T6d.log 2>&1; echo "   rc=$?"; grep -E "$PAT" $S/ev/T6d.log | sed 's/^/   /'

echo "== T6e path with spaces (linked worktree, own install)"
SP="$S/gate dir with spaces"; mkdir -p "$SP"
$G worktree add -q --detach "$SP/wt head" refs/gate/head
DS="$SP/wt head/Blockchain/Dev"
bash $S/harness/inprefix.sh "$DS" npm ci --ignore-scripts --no-audit --no-fund > $S/ev/T6e-ci.log 2>&1; echo "   ci rc=$?"
npm --prefix "$DS" run build --workspace=packages/shared > $S/ev/T6e-build.log 2>&1; echo "   build rc=$?"
bash $S/harness/leg16.sh "$DS" > $S/ev/T6e-clean.log 2>&1; echo "   clean rc=$?"; grep -E "$PAT" $S/ev/T6e-clean.log | sed 's/^/   /'
F="$DS/services/vc-issuer/src/__tests__/smoke.test.ts"; printf '\nexport const __gatePlant: number = "x";\n' >> "$F"; echo "   plant landed: $(grep -c __gatePlant "$F")"
bash $S/harness/leg16.sh "$DS" > $S/ev/T6e-plant.log 2>&1; echo "   plant rc=$?"; grep -E "smoke|FAIL —|HARNESS" $S/ev/T6e-plant.log | sed 's/^/   /'
git -C "$SP/wt head" checkout -q -- Blockchain/Dev; echo "   dirty=$(git -C "$SP/wt head" status --porcelain | wc -l | tr -d ' ')"
