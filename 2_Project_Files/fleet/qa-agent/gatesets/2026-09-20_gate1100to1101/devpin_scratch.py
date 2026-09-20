#!/usr/bin/env python3
import subprocess
REPO='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
DEV='e470198783bcb1ef0eac94780f87579974051423'
D='Blockchain/Dev/'; A=D+'services/api-gateway/'
P=[A+'src/__tests__/ks1230-settings-write-validates-allowed-document-types.test.ts',
   A+'src/__tests__/ks1215-the-connector-branch-never-carries-the-callers-bearer.test.ts',
   A+'src/__tests__/db.retry.test.ts',
   A+'src/routes/platform.ts', A+'src/routes/admin.ts', A+'src/routes/proxy.ts', A+'src/routes/verification.ts',
   A+'src/middleware/auth.ts', A+'src/index.ts', A+'package.json', A+'vitest.config.ts', A+'vitest.setup.ts', A+'tsconfig.json',
   D+'scripts/preflight/preflight.sh', D+'scripts/run-shell-suites.sh', '.githooks/pre-push',
   D+'package.json', D+'package-lock.json', D+'eslint.config.mjs', 'BACKLOG.md']
for p in P:
    b=subprocess.run(['git','-C',REPO,'rev-parse','--verify','-q',DEV+':'+p],capture_output=True,text=True).stdout.strip()
    print("%s  %s"%(b,p))
print('count', len(P))
