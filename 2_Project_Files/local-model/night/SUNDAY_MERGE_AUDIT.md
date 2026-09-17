# Sunday merge audit — the held Ornith work, and what will collide

**GENERATED 2026-09-18 06:53 by the 06:0x Wednesday seat — re-run the block at the foot of this file; do not hand-edit the numbers.**

Kam's grant (2026-09-15 16:36): *"complete as many tickets as possible. work with the local LLM. we will do QA on these Sunday night and merge / commit all at once"* — expiry **end of Sunday 2026-09-20**. This file exists so Sunday is an EXECUTION, not a discovery.

**Scale, in both units (they are different and both get stated):** **147 READY files** covering **94 distinct tickets**, against origin develop `34cdcfb26`.

## 1. Collisions — 19 files carry more than one READY (54 of 147 files)

Each group is ONE pull request, or a sequence applied lowest-hunk-first with the tree re-predicted between applies. Two READYs on one file applied independently is how a clean set turns into a conflict pile.

| n | target file (normalised) | tickets |
|---|---|---|
| 6 | `services/originate/src/__tests__/ks1213-a-derived-writer-relabel-is-refused.test.ts` | KS-1229-AFTERVERIFY, KS-1229-LOOSE, KS-1229-SIGNCERT, KS-1229-SIGNWALLET, KS-1229-UNTYPEDSRC, KS-1229-VERSIONTRIM |
| 5 | `services/security/src/index.ts` | KS-888, KS-908, KS-974-A, KS-976-A, KS-976-B |
| 4 | `CONTRIBUTING.md` | KS-1037, KS-1049-A, KS-1097-B, KS-1097-C |
| 4 | `services/api-gateway/src/routes/verification.ts` | KS-1072, KS-1073, KS-1087, KS-1185-F1 |
| 4 | `services/originate/src/services/anchorStateSync.ts` | KS-1074-A, KS-1074-B, KS-1074-C, KS-1158-R1 |
| 3 | `docs/DEV-PROCESS.md` | KS-1035-D, KS-1036-item3, KS-1097-A |
| 3 | `packages/shared/src/security/ssrf-guard.ts` | KS-1179-F4, KS-1179-F5, KS-932 |
| 3 | `services/api-gateway/src/routes/system-status.ts` | KS-1101-B, KS-864-PartA-helper, KS-864-PartB-portals |
| 2 | `.githooks/pre-push` | KS-1047, KS-884 |
| 2 | `CLAUDE.md` | KS-1097-Da, KS-1097-Db |
| 2 | `Start_Up/start-secuura.sh` | KS-1011, KS-972 |
| 2 | `deployment/KINTSUGI-DEV-SERVER-PLAN.md` | KS-1045-A, KS-1045-B |
| 2 | `routes/proxy.ts` | KS-1090-R2-3, KS-1212 |
| 2 | `scripts/check-stack-safety.sh` | KS-1034, KS-1093 |
| 2 | `scripts/run-shell-suites.sh` | KS-1089, KS-1127 |
| 2 | `services/api-gateway/src/middleware/audit.ts` | KS-871-PartA-details-path, KS-871-PartB-deriveAction |
| 2 | `services/auth/src/repositories/userRepo.ts` | KS-1186, KS-999 |
| 2 | `services/auth/src/routes/users.ts` | KS-1018, KS-1050 |
| 2 | `services/originate/src/originate.openapi.ts` | KS-1133-A, KS-794 |

## 2. ⚠ The path-spelling split — it HID collisions until the paths were normalised

READY diffs use two conventions for the same tree: `services/…` and `Blockchain/Dev/services/…`. Un-normalised, the same file appears under two keys and its collision is under-reported. Measured:

| file | spellings found |
|---|---|
| `packages/shared/src/security/ssrf-guard.ts` | `Blockchain/Dev/packages/shared/src/security/ssrf-guard.ts` · `packages/shared/src/security/ssrf-guard.ts` |
| `services/api-gateway/src/routes/system-status.ts` | `Blockchain/Dev/services/api-gateway/src/routes/system-status.ts` · `services/api-gateway/src/routes/system-status.ts` |
| `services/api-gateway/src/routes/verification.ts` | `Blockchain/Dev/services/api-gateway/src/routes/verification.ts` · `services/api-gateway/src/routes/verification.ts` |
| `services/auth/src/repositories/userRepo.ts` | `Blockchain/Dev/services/auth/src/repositories/userRepo.ts` · `services/auth/src/repositories/userRepo.ts` |
| `services/auth/src/routes/users.ts` | `Blockchain/Dev/services/auth/src/routes/users.ts` · `services/auth/src/routes/users.ts` |

**Any future audit of these files normalises the prefix first.** `services/api-gateway/src/routes/verification.ts` reads as 2+2 un-normalised and is in fact **4 READYs on one file**.

## 3. Known structural defect — the indented `--- a/` header (2 files)

A second file's `--- a/` header is indented INTO the previous hunk, so `patch(1)` will not apply the diff. Confirmed independently here; it matches the bound recorded on 2026-09-17 ("exactly 2 of the 81 READY files"), so it is **bounded, not a class**:

- `READY_KS-1172-A3_ornith35b-q4_JEST-MODIFYINPLACE-THREE-VERBS-PASS-7of7_2026-09-15.diff.md`
- `READY_KS-1172-B3_ornith35b-q4_MODIFYINPLACE-THREE-VERBS-PASS-7of7_2026-09-15.diff.md`

**Fix at raise:** de-indent the header line, or apply with `git apply` (which tolerates it) rather than `patch`.

## 4. ⚠ GAP, stated rather than hidden — 20 READYs whose target this instrument could not resolve

These are fence-only READYs (no `--- a/` header) whose header prose names no path, so **their collision risk is UNKNOWN, not zero.** Resolve each from its brief or its run's input pin before Sunday:

- `READY_KS-1118-F2_ornith35b-q4_TESTONLY-JEST-PASS-7of7_2026-09-15.diff.md`
- `READY_KS-1120-F1_ornith35b-q8_TESTONLY-PASS-7of7_2026-09-15.diff.md`
- `READY_KS-1120-F2_ornith35b-q4_TESTONLY-PASS-7of7_2026-09-15.diff.md`
- `READY_KS-1120-F2_ornith35b-q8_TESTONLY-PASS-7of7_2026-09-15.diff.md`
- `READY_KS-1123-F2_ornith35b-q8_TESTONLY-PASS-7of7_2026-09-15.diff.md`
- `READY_KS-1123-F3_ornith35b-q8_TESTONLY-PASS-7of7_2026-09-15.diff.md`
- `READY_KS-1130-E1twin_ornith35b-q4_TESTONLY-PASS-7of7_2026-09-15.diff.md`
- `READY_KS-1130-E3twin_ornith35b-q4_TESTONLY-PASS-7of7_2026-09-15.diff.md`
- `READY_KS-1130-E7twin_ornith35b-q8_TESTONLY-PASS-7of7-DECLSPLICED_2026-09-15.diff.md`
- `READY_KS-1158-R3_ornith35b-q4_TESTONLY-TAMPER-PASS-7of7_2026-09-16.diff.md`
- `READY_KS-1171-8j_ornith35b-q4_TESTONLY-PASS-7of7_2026-09-15.diff.md`
- `READY_KS-1171-8j_ornith35b-q8_TESTONLY-PASS-7of7_2026-09-15.diff.md`
- `READY_KS-1179-F1_ornith35b-q4_TESTONLY-TAMPER-PASS-7of7_2026-09-17.diff.md`
- `READY_KS-1181-F3_ornith35b-q4_TESTONLY-TAMPER-PASS-7of7_2026-09-17.diff.md`
- `READY_KS-1185-F4_ornith35b-q4_TESTONLY-TAMPER-PASS-7of7_2026-09-17.diff.md`
- `READY_KS-1188-F2_ornith35b-q4_TESTONLY-TAMPER-PASS-7of7_2026-09-17.diff.md`
- `READY_KS-1192_ornith35b-q4_TESTONLY-TAMPER-PASS-7of7_2026-09-17.diff.md`
- `READY_KS-1193-F1_ornith35b-q4_TESTONLY-TAMPER-PASS-7of7_2026-09-17.diff.md`
- `READY_KS-1193-F2_ornith35b-q4_TESTONLY-TAMPER-PASS-7of7_2026-09-17.diff.md`
- `READY_KS-1199_ornith35b-q4_TESTONLY-TAMPER-PASS-7of7_2026-09-17.diff.md`

## 5. How to re-run

```
python3 - <<'EOF'   # see git history of this file for the generator
EOF
```

Re-run after every new READY lands; the collision table is only true for the set that existed when it was generated.
