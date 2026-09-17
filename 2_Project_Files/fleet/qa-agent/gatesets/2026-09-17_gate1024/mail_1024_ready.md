SUBJECT: [Secuura/Blockchain -> Wednesday] READY FOR QA: #1024 KS-1202 @d1a3280880d85ff31fd409aa1b5a16c428c4bb9a (TIER 1); KS-1212 filed
TS: 2026-09-17T08:11:31.000Z
AUTH: {"spf": "pass", "dkim": "pass", "dmarc": "pass"}

Seat A

## BLUF
READY FOR QA: **#1024 KS-1202 @ `d1a3280880d85ff31fd409aa1b5a16c428c4bb9a`** (tier 1). **Merge on Wednesday's GO** (Kam ruled `build-and-merge`, 2026-09-17 15:09:57 AEST: "Build it, and Wednesday merges on a tier-1 GO like other security fixes"; KS-1202 comment `fa50d21e`). The fix commit is `86b11045cd2202c14af55437aed26d094b5d74a7`. Develop was merged in twice, both trees = the read-only predictions: `1f8763f9f` (develop `f8c7aaa39`) and `d1a328088` (develop `581c9db0d`, #1019, api-gateway only, no overlap; tree `10a71b87631c809a3cb519aef57d4935d621d749`). At the head: originate jest **63 suites / 656, 0 failed, 0 pending**, `tsc --noEmit -p .` rc 0.

**Also: the F-1019-2 record ticket is filed as KS-1212** (Backlog, Low, related KS-1187, not linked to any PR). Searched first: `caseSensitive` 0 fuzzy results to scan, 0 hits; `erasureDoorVerdict` 0 / 0; `F-1019-2` 118 scanned, 1 hit (KS-1187's comments); `KS-1187` 1 scanned, 0 literal. It holds the property, your gate's G-READOUTER 0-red measurement (`report.md:117`, `:186`, `:194`) and the test-only cell pair (door router case-sensitive with the factory default, and the inverse), marked not built. The ticket helper's old KS-1187 held-ticket guard was removed in a copy for this one ticket; the at-sign guard stays. Originate refuses 400 a create whose `data.documentType` is present and differs from the resolved type (`documentType || type || 'DOCUMENT'`, `routes/documents.ts:565`), so a document can no longer be served as a type other than the one stored. Red-proof at develop: 10/19, as predicted. Tamper table: 5/5 as predicted.

## Recommendation
Gate this head (tier 1). `Refs KS-1202`; In Progress on merge (§5f). Merge on Wednesday's GO, per Kam's build-and-merge ruling (supersedes the card default's tap and his earlier measure-first ruling).

## Detail
- **PR** https://github.com/Secuura/Distributed_Secuura/pull/1024, base develop `581c9db0d`. Branch `feature/ks-1202-the-served-document-type-comes-from-datadocumenttype-which` (Linear's branchName, one id, its own). Files vs develop: `services/originate/src/routes/documents.ts` (+12) and the new jest test (19 cells), byte-identical to the fix commit.
- **Push:** 08:04:18Z → 08:10:24Z, rc 0, first push, push protocol **CLEAN**, ls-remote = head. Guards: branch absent on origin, origin develop = `581c9db0d`, HEAD = `d1a328088`, porcelain 0. In-hook preflight: **12/15 legs ran, 3 SKIPPED (3, 4, 8: no stack), nothing failed** (not a full pass); legs 1 (spec in sync), 2, 5 (59 / 59), 6 and 7 OK.
- **Post-push:** 4 login stubs stopped by verified pid (CONTROL: ps rows parsed 1108; 0 alive; non-node controls 17 = 17). `attachmentsForURL(pull/1024)` = [KS-1202 **contributes**]; KS-1202 walked Backlog → In Progress at 08:11:04Z (botActor GitHub, same second as the attachment), left. Closing-phrase scan of the title and body: 0; the body names only KS-1202. The PR body carries Kam's build-and-merge quote.
- **Rule:** exact equality. A case variant (`degree` vs `DEGREE`) and a non-string value are refused too. That is a fail-closed choice worth the gate's eye: any legacy client that sends a differently-cased `data.documentType` would now get 400. No such client is known (not measured).
- **Cells** on the real `documentsRouter` (POST, then GET `/:id` for the served type), in-memory repository, real RBAC; for each of a connector with `documents:write`, `ISSUER_ADMIN` and `SYSTEM_ADMIN`:
  - 🔴 the gate's typed carrier (`type DOCUMENT` + `data.documentType PROPERTY_DEED`), a `documentType DOCUMENT` + `data.documentType SSD_DOCUMENT` body, and an untyped `data.documentType DEGREE` body → `{400, BAD_REQUEST, saved 0}`;
  - 🟢 a matching `documentType DEGREE` + `data.documentType DEGREE` → `{201, stored DEGREE, served DEGREE}`;
  - control: the portal shape → served `DOCUMENT`;
  - control: the legacy `type CERTIFICATE` without `data.documentType` → served `CERTIFICATE`.
  - Plus 🔴 a non-string `data.documentType` → 400.
- **Red-proof** (`documents.ts` written back to develop bytes, restored sha256-equal; prediction written first, 10 red / 9 green): 10 red, all jest `toEqual` assertions; 9 green.
- **Tamper table** at `86b11045c`. Each row: anchor 1, `tsc --noEmit -p .` rc 0, WHOLE originate suite 63 suites / 656 tests, pending 0, restore by bytes + sha256 + `git diff --quiet HEAD`, every red a jest assertion.
  - T0 → 0 (0).
  - NOCHECK (a condition that is always false) → 10 (10).
  - LOOSE (strings only) → 1 (1): the non-string cell.
  - WRONGSIDE (compared with `type` only) → 3 (3): the three matching controls.
  - TI → 0 (0).
  - **Instrument slip, recorded:** my first NOCHECK was `if (false)`. That left `dataDocumentType` unused, so `noUnusedLocals` broke the compile (TS6133) and the row read 3 load-shaped failures in other suites with 0 in this file: a VOID row, not a red. The runner also crashed on their empty failure messages. Both runs are kept (`tamper.run1-void-nocheck`, `tamper.run2-crash`); the table above is the re-run with a compiling tamper.
- **Suites:** at the fix commit originate 63 / 656, tsc rc 0; the same at both merge commits.
- **Not covered:** other originate handlers that might write a `data` blob after creation (not read); a real Postgres; the gateway end to end; Schemathesis / Akto / Playwright / k6 (no stack); preflight legs 3, 4 and 8 (no stack).

- **Open PRs of this lineage:** #1018, #1023, #1024 = 3, the cap. KS-839 waits for a merge.
