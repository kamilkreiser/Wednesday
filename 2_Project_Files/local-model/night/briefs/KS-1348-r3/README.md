# KS-1348 rev 3: Spark brief + golden (the ruled round "allow-list the file format")

Written 07:18 AEST 2026-09-28 by a brief-writer sub-agent for Wednesday. It ran no model, raised no PR, changed no GitHub or Linear state (Linear and `ls-remote` were READ), mailed nobody and wrote nothing under `!CODING/`. Every write ran in this session's scratchpad, in a `cp -a` copy of `ks1346cd/base`. The base was only read: its HEAD was verified equal to the tip before copying, and its porcelain was 0 at the end.

- **Ruling:** Kam, live board 2026-09-28 06:58 AEST, card `secuura-ks1348-r2-files-still-leak-allowlist`, option a, "Third attempt: allow-list the file format (recommended)". The files record only named safe fields; redaction stays on the Console. This is gate33's fix-shape (a) (`report.md:131`-`:137` of `2026-09-28-batch1310-g33`).
- **Base:** develop `ec32c40e2b1e2698d2e855a916f390d48dad1b45` (`ls-remote` at 07:07 and again at 07:18). `logger.ts` there is blob `ca9a27ef13a4`, the same blob r2 was written against.
- **Supersedes:** #1310 (OPEN, gate33 NO GO). Its `logger.ts` (head `2cd351fa`, blob `7706a8f6`) is **byte-identical** to the r2 golden's product (`cmp`), so the "#1310 arm" below is #1310's real logger. Raise FRESH against develop.
- **Edit points:** 2 hunks in `logger.ts`, the same two places as r2:
  - Hunk 1 inserts r2's redaction block plus a new `keepFileFields` allow-list format, and gives each File transport `format: combine(keepFileFields(), json())`.
  - Hunk 2 adds `redactSecrets(),` last in the logger-level `combine`.
  - One new jest file, 203 lines.

## Files
- `KS-1348.md` is the brief.
- `KS-1348.golden.diff` is the golden, sha256 `cd63c59e6622…`: 2 files, 244 `+` lines, 2 `-` lines.
- **Fence rebuild:** the diff rebuilt from the brief's two fences is **IDENTICAL** to the golden (`cmp`). Comparator control: a one-token mutation (`[REDACTED]` to `[REDACTE]`) printed DIFFER.
- **Char lint:** 0 `+` lines carry a backslash, backtick or double quote (control: a planted backslash line counted 1). There are 0 non-ASCII lines and 0 blank context lines.

## The file allow-list
The files keep `timestamp, level, service, message, requestId, method, path, statusCode`, each only when it is a string or a number. They also keep `error` when it is a string. Everything else is dropped: nested Errors, `toJSON` output, every unnamed key, and also `userId`, `documentId`, `ip` and `stack` (see the doubts). The Console keeps r2's key-suffix redaction unchanged.

## Measured (scratch copy at `ec32c40e`, node_modules as farmed in `ks1346cd/base`)

| step | result |
|---|---|
| `git apply --check` / `patch -p1 -F0 --dry-run` at the tip | rc 0 / rc 0 |
| test file alone at the tip (RED) | **5 failed / 6 passed / 11**: exactly A1 x2, A3 x2 and B1, by ASSERTION. A1 got `['undefined']`. A3 got `message:false`. B1's `leaked` was the six ruled keys, with `markers 0`. |
| golden applied (GREEN) | **11 / 11**; both files equal the golden byte for byte |
| whole originate suite (`jest --json`) | develop **86 suites / 1013 passed / 0 failed**; golden **87 / 1024 / 0** (+1 suite, +11 tests) |
| `tsc --noEmit -p services/originate` | rc 0 at the tip and with the golden |
| tsc with tests (temp tsconfig, `include src/**/*.ts`, `exclude []`) | rc 0, 0 errors, at both. Control: a planted type error in a test file gave 1 error there and 0 under the service tsconfig. |
| eslint (`logger.ts` and the new test) | rc 0. Control: a planted `var` + `debugger` file gave rc 1. |

**Arms** (the golden test against variant `logger.ts` files; the golden was restored and checked with `cmp` after each):

| arm | failed / 11 | which |
|---|---|---|
| develop | 5 | A1 x2, A3 x2, B1 |
| **#1310's logger** (`7706a8f6`) | **4** | A1 x2, A3 x2; **B1 green**. In error.log, A3's `leaked` = nestedAuthorization, nestedResponseToken, toJsonAuthorization, passwordHash, privateKey, secretKey, mnemonic, phone, email_address, userEmails[0], ip. combined.log also has recipientPhone and sessionId. This reproduces gate33 W-1 and W-2 with this file's own sentinels. |
| allow-list admits `ip` (`'statusCode'];` changed to `'statusCode', 'ip'];`) | 4 | A1 x2, A3 x2 |
| Console redaction off, type-clean (`key !== 'level' && …` changed to `key === 'ks1348-never'`) | 1 | B1 only (the files stay clean) |
| golden | 0 | none |

**About "RED at develop for the file-leak cases".** At develop the files hold only `undefined`, so no sentinel is in them, and a leak-only assertion is GREEN there. A1 (the exact entry, closed world) and A3 (no sentinel, AND the message and error text present) are red at develop because the message is missing. They are red on #1310 because the sentinels are present. The #1310 arm is the measurement that the leak half discriminates. B1 is red at develop and green on #1310: that is the "the Console still redacts" control against the previous round.

## build_input: rc 0
```
NIGHT_SOURCE_CHECKOUT=/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/a0b3d8ae-4820-440f-b4d5-5c87b239ed04/scratchpad/ks1346cd/base NIGHT_BRIEFS_DIR=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/KS-1348-r3 bash /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/build_input.sh KS-1348 <out>/input.json product=Blockchain/Dev/services/originate/src/utils/logger.ts ref=Blockchain/Dev/services/originate/src/__tests__/ks488-smtp-opt-in.test.ts line=45 ctx=65536 supersedes=1310 "started_ok=Kam-ruled-2026-09-28-06:58-card-secuura-ks1348-r2-files-still-leak-allowlist-option-a-allow-list-the-file-format;fresh-PR-replaces-#1310"
```
The build output:
- The ticket is In Progress, ADMITTED by `started_ok`.
- #1310 is OPEN, ADMITTED by `supersedes=`. #1302 is closed, not merged.
- `prompt source: WEDNESDAY BRIEF … (28269 chars)`.
- Red cells `['RED KS-1348 A1', 'RED KS-1348 A3', 'RED KS-1348 B1']`, 36 expected `+` lines (A3c).
- `suggested_test_file` = the brief's `File:` line; the contract key set is OK.
- input.json 43,359 B, about **10.8K prompt tokens**, whole file (no excerpt needed).

## The round command (NOT run)
It uses the round script already pinned to this tip. It pins `SRC=ks1346cd/base` and `TIP=ec32c40e…`, and it refuses if the source is not clean at the tip.
```
bash /private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/a0b3d8ae-4820-440f-b4d5-5c87b239ed04/scratchpad/sparkrun/round.sh KS-1348-R3 KS-1348 /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/KS-1348-r3 - product=Blockchain/Dev/services/originate/src/utils/logger.ts ref=Blockchain/Dev/services/originate/src/__tests__/ks488-smtp-opt-in.test.ts line=45 ctx=65536 supersedes=1310 "started_ok=Kam-ruled-2026-09-28-06:58-card-secuura-ks1348-r2-files-still-leak-allowlist-option-a-allow-list-the-file-format;fresh-PR-replaces-#1310"
```
**Round counter:** KS-1348 has had #1302 (round 1; this writer did not check which engine produced it) and #1310 (the r2 brief, "Round 2" in its own header). By Kam's rule (original brief + ONE rebrief, then cloud) the Spark allowance may already be spent. Kam's ruling names this the "Third attempt", but it does not say which engine. **Wednesday rules.** The golden is raise-ready for a cloud seat either way.

## UNMEASURED / doubts for Wednesday
- **No Spark round was run.**
- **What the files now lose.** Every key outside the list is dropped, including `userId`, `documentId` (a single-line grep counted 27 metadata uses in originate's logger calls), `id`, `anchorId`, `pgCode`, and `stack`. errorHandler (`middleware/errorHandler.ts:70`-`:77`) keeps `message`, `statusCode`, `path` and `method`; its `userId` and `ip` are dropped. This is what "closed world" means. The field list is the gate's, a superset of Kam's words ("message, error text, request method and path"): `timestamp, level, service, requestId, statusCode` are line bookkeeping. **Confirm the list, especially whether `userId` or `documentId` should be in it.**
- **Residue in the files, by the ruling:** the message text, the string `error` text, and `path`. gate33 W-3 (a non-Error `String(err)` in `error`) is still a string, so it still reaches the files. It belongs to KS-1346's remainder, not here.
- **The Console is unchanged from #1310.** A nested Error and the unnamed keys still reach stdout, as they did at develop. Redaction under development (unruled since r2) carries over.
- stdout itself was not read. B1 reads the line the Console transport formats at its `log` call.
- A real fail500 route through the real logger was not added. The test drives `logger.error` / `logger.info` directly.
