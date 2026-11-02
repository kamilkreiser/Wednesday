#!/bin/bash
G=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate126-ks1724-pr1944
T=$G/base/Blockchain/Dev/packages/shared/src/__tests__
Q=$G/logs/_quarantine; mkdir -p $Q
cp $G/scripts/gate126-base-shim.ts $T/gate126-base-shim.ts
sed "s#} from '../middleware/request-limits';#} from './gate126-base-shim';#" $G/repo/Blockchain/Dev/packages/shared/src/__tests__/ks1724-bounded-json-structural-caps.test.ts > $T/ks1724-bounded-json-structural-caps.test.ts
grep -c "gate126-base-shim" $T/ks1724-bounded-json-structural-caps.test.ts
# the setup file at base does not list the new file; copy the head setup in so the structural cell gets the same budget
cp $T/support/walkTimeouts.setup.ts $Q/base_walkTimeouts.setup.ts.orig
cp $G/repo/Blockchain/Dev/packages/shared/src/__tests__/support/walkTimeouts.setup.ts $T/support/walkTimeouts.setup.ts
bash $G/scripts/vt.sh base packages/shared $G/logs/red_base_new_tests.log ks1724-bounded-json; echo "red rc=$?"
mv $T/ks1724-bounded-json-structural-caps.test.ts $Q/red_base_ks1724.test.ts
mv $T/gate126-base-shim.ts $Q/red_base_shim.ts
cp $Q/base_walkTimeouts.setup.ts.orig $T/support/walkTimeouts.setup.ts
git -C $G/base status --short
