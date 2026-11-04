// Gate 190: drive the REAL runStartupMigrations() from the develop 536642104002 worktree (startup-migrations.ts is
// byte-identical at PR 2002's head: `git diff gh/develop pr/2002 -- .../startup-migrations.ts` is empty).
// eslint-disable-next-line @typescript-eslint/no-var-requires
const m = require('/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-04_gate190-ks1401-pr2002/scratch/dev/Blockchain/Dev/services/api-gateway/src/startup-migrations.ts');
(async () => {
  const s = await m.runStartupMigrations();
  console.log('SUMMARY ' + JSON.stringify(s));
  process.exit(0);
})().catch((e: any) => { console.log('THREW ' + (e?.message || e)); process.exit(2); });
