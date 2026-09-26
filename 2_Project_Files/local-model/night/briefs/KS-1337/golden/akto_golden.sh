#!/bin/bash
# Assemble the akto golden diff and prove it applies strictly on the clone at 3f70224a (scratch clone only).
W=/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/d0b2ec3e-4b50-4d96-87d2-4a998799b9cd/scratchpad/feed/akto
C=/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/d0b2ec3e-4b50-4d96-87d2-4a998799b9cd/scratchpad/sparkfeed
Q=/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/d0b2ec3e-4b50-4d96-87d2-4a998799b9cd/scratchpad/feed/_quarantine
mkdir -p $Q
T=$W/ks1337-preSuiteSetupPathWithASpace.test.ts; N=$(grep -c '' $T)
{ cat <<'EOF'
--- a/systemTest/akto/tests/preSuiteSetup.ts
+++ b/systemTest/akto/tests/preSuiteSetup.ts
@@ -12,1 +12,2 @@
+import { fileURLToPath } from 'node:url';
 import { spawnSync } from 'node:child_process';
@@ -35,3 +36,3 @@
 function runPreSuiteStep(label: string): void {
-    const step = new URL('../../fixtures/pre-suite.ts', import.meta.url).pathname;
+    const step = fileURLToPath(new URL('../../fixtures/pre-suite.ts', import.meta.url));
     const res = spawnSync('npx', ['tsx', step, label], { stdio: 'inherit' });
EOF
echo "--- /dev/null"; echo "+++ b/systemTest/akto/tests/unit/setup/ks1337-preSuiteSetupPathWithASpace.test.ts"; echo "@@ -0,0 +1,$N @@"; sed 's/^/+/' $T; } > $W/KS-1337-akto.golden.diff
NT=$C/systemTest/akto/tests/unit/setup/ks1337-preSuiteSetupPathWithASpace.test.ts
[ -f $NT ] && mv $NT $Q/ks1337-akto.$(date +%H%M%S).test.ts
git -C $C status --porcelain
git -C $C apply --check $W/KS-1337-akto.golden.diff; echo "git apply --check rc=$?"
(cd $C && patch -p1 -F0 --dry-run < $W/KS-1337-akto.golden.diff); echo "patch -F0 dry rc=$?"
