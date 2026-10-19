VERDICT: GO WITH NOTE at head de44e3d3ccfc... (tier 2, round 1 of 2; landing tree 54dc22e920569148070ee579fc173753432f6dd4 on develop 2b205beada00a2f0fb3144e38198e471848132b6; 0 blockers, 3 notes)

## BLUF
Both new assertions do what their tickets name. Every tamper I re-ran that is a real blind spot (T1, T2, T3 for KS-1500; K1, K2 for KS-1468) SURVIVES develop's test file and is KILLED by the head's, and every one compiles (tsc rc 0). K3 is killed by BOTH versions (positive control, so the SURVIVED readings are a gap and not an inert suite). The one removed line is replaced by a strictly stronger check, the 25 old cells all still run, and the landing is green: auth 1,095 -> 1,096 cells, test type-check ratchet 42/42 in baseline, 0 new. The notes are residual gaps, not defects in what the PR claims.

Heads re-read at start and at the end (ls-remote of the cache clone's origin): #1643 = de44e3d3ccfcefd58abe5295a1f8a2571e765bc4, develop = 2b205beada00a2f0fb3144e38198e471848132b6, unmoved. merge-tree --write-tree = 54dc22e920569148070ee579fc173753432f6dd4 (equals the author's and Wednesday's). Because develop has not moved, the head's own tree IS the landing tree (git rev-parse HEAD^{tree} = 54dc22e9...), so "the suite at the landing" is the suite at the head. Three-dot diff = 1 file, +10/-1.

## Findings
Blockers: none.

Notes:
1. N1 (residual gap, KS-1468 item 3, survives BOTH versions). A decoy TEMPLATE literal still satisfies the new pin. Tamper K4 (mine): real lookup replaced by `INSERT INTO users (id) VALUES ($1) RETURNING id`, plus `void \`SELECT * FROM auth_find_user_by_wallet\`;` before the loop. tsc rc 0, old 25/25 green, new 26/26 green. The pin proves a backtick sits in front of the text in code position, not that the text is the argument of the one allowed `query(`. The ticket only names comments, so this is outside item 3 as scoped; mention it on the ticket if item 1/2 are still open.
2. N2 (author's matrix, wording). T4 (import dropped, no local fn) is NOT compile-safe in my run: tsc rc 2, TS2304. Its kill is real at vitest level but is exactly the "red is a TS error" shape the brief warns about; T1/T2/T3 are the compile-safe proofs of the KS-1500 assertion. Likewise T3 as literally described ("import kept and local fn added") cannot be a top-level function (TS2440), and a function that simply shadows the import leaves it unused (TS6133). My compile-safe T3: hoisted `function canonicalWalletAddress` declared AFTER the lookup loop inside getOrCreateWalletUser plus a module-level `void canonicalWalletAddress;` to keep the import used. That form gives rc 0 and is the one I report.
3. N3 (fragility, not a weakening). The KS-1468 pin now requires the opening delimiter to be a backtick. A future legitimate refactor of the lookup to a quoted string would go red. That is arguably the point (the old toContain accepted it anywhere), but it is a behavioural narrowing on legitimate code.

## FOUND / TESTED / HOW
Setup: clone --shared of the cache src into the scratchpad gate_bd1/repo, objects fetched by SHA, node_modules REAL copies (not symlinks into the read-only tree), packages/shared built with tsc (rc 0). Runner: python script that asserts each planted line occurs exactly once, plants it in services/auth/src/routes/wallet.ts, runs `tsc -p services/auth/tsconfig.json --noEmit`, then vitest on ks963-preauth-rethrow.test.ts with develop's file (sha b745fe4f...) and then the head's file (sha 4c8de531..., cmp-identical to `git show` of the head), and restores wallet.ts with a sha256 check each time.

| tamper | tsc | develop's test | head's test | killed by |
| -- | -- | -- | -- | -- |
| T0 control, no tamper | 0 | 25/25 green | 26/26 green | none |
| T1 import dropped + top-level impure local fn | 0 | SURVIVED | KILLED | RED KS-1500 m2 |
| T2 import re-pointed to a new impure module walletEmailAlt | 0 | SURVIVED | KILLED | RED KS-1500 m2 |
| T3 import kept + hoisted impure local fn (+ void ref) | 0 | SURVIVED | KILLED | RED KS-1500 m2 |
| T4 import dropped, no local fn | 2 (TS2304) | SURVIVED | KILLED | RED KS-1500 m2 (not compile-safe, see N2) |
| K1 INSERT template + decoy // comment | 0 | SURVIVED | KILLED | "NOTHING is written before the lookup" |
| K2 INSERT template + decoy block comment containing a backtick | 0 | SURVIVED | KILLED | same cell |
| K3 lookup replaced by a different SELECT | 0 | KILLED | KILLED | same cell (positive control) |
| K4 decoy template literal (mine) | 0 | SURVIVED | SURVIVED | nothing (N1) |

In every kill, the failing cell is exactly one cell and is the cell the ticket names; no kill carried a TS code except T4. The control positive (K3 red on develop's file) shows the harness can fail. An extra tamper P1 (parameter default shadows the import) was not usable: it does not compile (TS6133) and the old test already kills it through the extra `query` call.

Q3 no weakening: the removed line was `expect(body.slice(0, lookup)).toContain('SELECT * FROM auth_find_user_by_wallet')`. The replacement takes every raw match of the same text in the same slice and requires one with a backtick at the blanked position just before it. The new condition implies the old (a match must exist), so it is strictly stronger. Cell names by vitest JSON reporter: develop's file 25, head's 26; vanished = none; added = the single KS-1500 m2 cell; non-passing = none. KS-1468 adds no cell.

Q4 landing: full auth suite from the auth dir, both at develop and at the head: develop 1,095/1,095 (99 files, rc 0) -> head 1,096/1,096 (99 files, rc 0); by cell name +1 (KS-1500 m2), 0 vanished, 0 failed. Ratchet `node scripts/typecheck-tests/check.cjs services/auth` (tsconfig.test.json) at the head, rc 0: "tsc examined 150 files, 99 of them under __tests__; 42 errors: 42 in the baseline, 0 new; 0 stale baseline entries" (identical at develop, so the PR moves it by 0). Environment note: ks1009-wallet-status-reveals-only-existence.test.ts locates the Dev root from process.cwd(); run from outside the repo it fails to load (my first run: 1,087/1,088 cells and one failed suite, an artefact, rerun from the auth dir gave the numbers above).

## NOT RUN
- T4 under a compile-safe form (none found); K4-style variants beyond the one above; quoted-string refactor (N3) was reasoned, not run.
- Whole-repo suites other than auth; the preflight legs needing a stack; Docker; any other service's ratchet.
- Open-PR census (0 of 23 touch the file) and the PR body/comment readbacks: not re-checked; GitHub and Linear not touched.
- Commit-by-commit trees (each-alone, order-independence): not re-derived; I used the landing tree only, which equals the head tree.
- Product bytes: confirmed by diff stat (1 test file), not by running prod.

## Wall-clock
About 8 minutes from clone to verdict (node_modules copy about 70 s).
efce70b4afd859089af41e72b86fe42b22550e6f5a4ac1fb8d62b1809af92800
