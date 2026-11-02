W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate152-ks1868-pr1968; R=$W/repo
git -C $R checkout -q pr1968
npm --prefix $R/Blockchain/Dev ci --ignore-scripts > $W/logs/npm_ci.log 2>&1; echo ci_rc=$? > $W/logs/npm_ci.rc
if ! grep -q 'ci_rc=0' $W/logs/npm_ci.rc; then npm --prefix $R/Blockchain/Dev install --no-package-lock --ignore-scripts > $W/logs/npm_install.log 2>&1; echo inst_rc=$? >> $W/logs/npm_ci.rc; fi
npm --prefix $R/Blockchain/Dev run build --workspace=packages/shared > $W/logs/build_shared.log 2>&1; echo build_rc=$? >> $W/logs/npm_ci.rc
