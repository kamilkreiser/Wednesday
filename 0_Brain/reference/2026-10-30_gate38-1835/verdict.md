## QA GATE - TIER 1, round 1: GO WITH NOTES
(Filed by the Wednesday seat from gate 38's returned text, 17:5x AEDT. Probes in `probes/` beside this file, on disk, gitignored. Container daaef837f032 (g38-pg-1835) started and removed by the gate by id.)

**Subject:** PR #1835 (Secuura/Distributed_Secuura), KS-1848 + KS-1849, author Seat F 18th (WRAPPED). The MFA backup-code burn removes the matched code in one conditional UPDATE.
**Head:** `598f50ed29d44acb6fefa0f4053378f150556c01` equal at 06:36:29Z and 06:57:01Z; one commit on 85cd24d81cb9; develop a8c554659cb3; merge-tree conflicts ONLY in the two Projects Documents html.

### Verdict
Atomic: `UPDATE users SET mfa_backup_codes = array_remove(mfa_backup_codes,$1) … WHERE id=$2 AND $1 = ANY(mfa_backup_codes)`, rowCount decides (missing = 0). Real Postgres, RLS live as secuura_app: develop wrong 20/20 in every red cell (same code twice; A+B replay; regenerate loses the new set; disable leaves a code); head correct 20/20. The REVERSE interleaving the author could not force was forced (burn's UPDATE first in the lock queue): correct 20/20. Wednesday's ruling holds on every leg. Six gate mutants all killed (M6 only by the unit file and the probe). **FIX BEFORE MERGE: none.**

### Findings
- **F1 FOLLOW-UP (low).** Lost-race refusal ~30 ms faster than wrong/spent (medians 45.4 vs 77.8/76.6 ms, IQR 3-5 ms; 15 samples, set size 2): verifyBackupCode returns on first match. Status, body and lockout identical. Very low likelihood (needs the password + a valid code + a ms race window). The new comment in passwordLoginGate.ts "so a lost race is no oracle" overclaims for TIME: reword it, or verify over every hash.
- **F2 FOLLOW-UP.** M6 ("0 rows with the hash still stored counts as spent", breaks the ruling's third leg) survives the author's real-PG file; killed by unit U5c/U11 and probe N5a/N5b. Add a real-PG blind-write cell: tenant_id NULL row, or runWithTenantId(<other tenant>) with a positive control under the row's own tenant (both 503 at head).
- **F3 FOLLOW-UP.** Pin the reverse interleaving (probe G3/G4: hold FOR UPDATE; start the sign-in and wait until its UPDATE queues in pg_stat_activity; start regenerate/disable; wait for 2 queued; release). Head 20/20: regenerate -> burn ok + new set intact; disable -> burn ok + row disabled with NULL codes; an unspent old-set code refused after regenerate, 503 after disable. Develop red on the stale follow-up 20/20.
- **F4 INFO, pre-existing.** No audit row on a backup-code sign-in at develop or head (only logger.info 'MFA verified via backup code', once per success, 0 on a lost race).
- **F5 INFO.** array_remove removes every copy of a duplicated hash (splice removed one): errs safe; needs a legacy unsalted code generated twice.
- **F6 INFO.** One burn site only; mfa/disable checks a code without burning but NULLs the whole set (no replay).

### Ruling table (cell N, real PG, head)
N1 non-NULL set lacking the hash -> refused, set unchanged · N2 `{}` -> refused · N3 NULL set -> 503 (develop: ok) · N4 no row -> 503 · N5a hash still stored, NULL-tenant blind write -> 503 · N5b wrong ambient tenant -> 503 · control under own tenant -> ok.

### Mutants (unit 18 / author real-PG 8 / probe 8 red)
M1 drop WHERE hash: 4/4/7 · M2 read-then-write: 8/6/8 · M3 ignore rowCount: 5/4/7 · M4 gate ignores consumed:false: 2/3/6 · M5 NULL set counts as spent: 1/1/3 · **M6 0 rows + hash stored counts as spent: 2/0/1 (F2)**. Unit 9/18 -> 18/18; author real-PG 6/8 red -> 8/8; probe 8/8 red at develop -> 8/8 green at head. Whole auth unit at head 1344/1344; tsc 0 (control fires); eslint 0.

### NOT TESTED
The burn UPDATE's own connection fault (stays 500); real Redis lockout (mocked, counts only); HTTP routes end to end; a running stack; platform suites; MULTI_TENANCY_ENABLED=true; pgbouncer; isolation levels other than READ COMMITTED; legacy SHA-256 path on real PG; Node 24; timing at larger code sets or at the route level.

### Instrument faults
I1 ks949 5 s timeouts (tree walk ~17 s on this drive) -> --testTimeout=120000: 31/31, suite 1344/1344. I2 silenced console -> --silent=false. I3 probe mislabelled regenerate/disable results -> fixed before any run. I4 hook refused a variable-path merge-tree -> literal paths. I5 tamper.py captured the "Failed Tests" banner; the per-cell red lists are the evidence.
