# KS-1015 referral-envelope: Spark brief, golden and round 1 (GET /api/referrals/{code} 200 declares the envelope its handler returns)

Written 2026-09-30 03:02 AEST by a Spark brief-writer sub-agent for Wednesday (session ffc4a192). No PR, no merge, no post, no mail, no ticket or PR change. Linear and GitHub were READ only (GraphQL; REST `GET`; `ls-remote`). Nothing was written under `!CODING/`. Git write verbs ran only in this session's scratchpad clones `ks1015/{src,gold,ctl_clone,sparkrun/KS-1015-envelope/clone}`.

- **Carve (Wednesday's ruling):** KS-1015 is a register of 28+ check/operation pairs on Kam's account. This brief takes ONE pair from its 2026-09-29 comment: `response_schema_conformance::GET /api/referrals/{code}`. The comment's direction is "the spec should change to match the runtime", and the handler omits `id`/`ownerUserId` on purpose. **Refs KS-1015, does NOT close it.** The 09-29 delegations pair is out of scope, because no direction was given for it.
- **Base:** develop `37205947ddd2775a72a417beb5b7ac8e3240fbf3`, read by `ls-remote` at 02:46 and again at 02:55 AEST. It matches the base Wednesday named.
- **Premises re-read at the base:** `referral.openapi.ts:480` is `      content: { 'application/json': { schema: ReferralCodeSchema } },` (DELTA's `:480` confirmed). `routes/referrals.ts:105` is `    res.json({`, with the `{ success, data: {...} }` body at `:106`-`:115` (DELTA's `:105` confirmed).
- **Shape:** ONE product hunk (`:480` becomes 21 lines, `@@ -477,7 +477,27 @@`) plus a NEW vitest file of 76 lines in the KS-747 shape.
- **Collision:** 23 open PRs (REST `GET /pulls?state=open`, which equals the 23 live `refs/pull/*/merge`). None touches `referral.openapi.ts` or `secuura-api.yaml`, checked two ways: REST `/files`, and the fetched head's `diff --name-only`. #1351's body cites KS-1015 only as where sweep evidence went. The round counter was 0 (control KS-908 = 3).

## Files
- `KS-1015.md`: the brief. Both fences were filled FROM the golden by script (`fill.py`).
- `golden.diff`: the fence rebuild of the brief (product first, then test), sha256 `45a105d11745…`, 2 files, **97 + / 1 -**. It is IDENTICAL to the `git diff` golden, section by section. Comparator control: a one-token mutation read DIFFER.
- `KS-1015.openapi-yaml.companion.diff`: sha256 `aa52a6b13440…`, the +30/-1 regenerated `docs/openapi/secuura-api.yaml` hunk. **It is NOT the model's.** See "For the raise".
- `precheck/`: build_input on this brief (rc 0), and the CONTROL checker run on the golden. This is the golden dir that hold_ready cites.
- Char lint: 0 `+` lines carry a backslash, backtick or double quote. There are 0 non-ASCII lines and 0 blank context lines.

## Measured (scratch clones at `37205947`, node_modules farmed from sparkfeed by `prepare_clone.sh`, shared built in each clone rc 0)

| step | result |
|---|---|
| test file alone (RED) | **3 failed / 3 passed / 6**, exactly A1-A3, by ASSERTION |
| golden applied (GREEN) | **6 / 6** |
| whole referral suite | base **6 files / 28 / 0 failed**; golden **7 / 34 / 0** |
| tsc | `tsc --noEmit -p services/referral` rc 0 at both. A test-inclusive temp tsconfig also gave rc 0 at both |
| eslint | both changed files rc 0. Control: a planted `debugger`/`var` file gave rc 1 |
| openapi | base `generate-openapi --check` rc 0. **Golden alone rc 1.** Golden + companion: `check:openapi` rc 0 (405 example blocks OK, the same as the base, so the inline schema needs no `example`) |
| arms (golden test vs product variants) | revert = A1+A2+A3 · `success: z.boolean()` = A1 · `customLabel` required = A2 · `isActive: z.string()` = A3 · drop `isExpired` = A2+A3 · add `id` = A2+A3. Each arm restored the golden (`cmp` rc 0) |
| **CONTROL: spark_checker on the golden** | **PASS 7/7 strict + A2a OK** (A3b 1/1, A3c 21, A4 3/6, A5 6/6, A6 no new red, A7 rc 0). A2a negative control: the header moved to `-476` read **BAD** (rc 1) |

## Round 1 (Spark `deepseek-v4-flash-0731`, thinking OFF, one request)
- **Command:** a copy of the day seat's round.sh at `ks1015/round.sh`, with only SRC, TIP and the run-dir date changed (its diff was printed and read):
  `bash round.sh KS-1015-envelope KS-1015 <this dir> - product=Blockchain/Dev/services/referral/src/referral.openapi.ts ref=Blockchain/Dev/services/security/src/__tests__/ks747-keys-list-spec-declares-organizationid.test.ts line=480 ctx=65536`
- **Run:** `runs/spark_secuura_2026-09-30_KS-1015-envelope`. Wall 45.2 s, prompt 20,985 tokens, completion 1,533 tokens, `think=0`, `thinking_chars=0`, `done_reason=stop`.
- **Verdict: PASS 7/7 strict + A2a.** `patch.diff` is BYTE-IDENTICAL to the golden (`cmp` rc 0; the mutated control gave rc 1). The diff was read line by line against the brief: the one `-` line is `:480`, the 21 `+` lines and 6 context lines are as briefed, and the test is 76 lines as briefed.
- **Held:** `night/READY_KS-1015-ENVELOPE-1_spark-dsv4flash_BRIEFED-CODEPATCH-REFERRAL.OPENAPI-PASS-7of7_2026-09-30.diff.md`, by hold_ready with `--model-tag spark-dsv4flash`, so the model label is correct as written and needed no relabel. One line was added by hand, marked as such: the raise-seat YAML step.
- **Harness notes:** sparkfeed lacks `37205947` and belongs to another session, so it was not fetched into. The source is this session's own clone, farmed from sparkfeed's node_modules, which were installed at `94c9c7aa`. Between that commit and the base only overrides and nodemailer moved; zod, zod-to-openapi, vitest and tsx did not.

## For the raise (after QA)
Apply the two model sections from the READY (strict, `git apply -p1`). Then add the companion with `git apply KS-1015.openapi-yaml.companion.diff`, or run `npm run generate-openapi` in `Blockchain/Dev` and confirm it produces the same 31 lines. Then run `npm run check:openapi`. Without the companion, the openapi drift check fails (measured).

## UNMEASURED
Carried in the brief's own section. In short: no Schemathesis re-run (a live re-check waits on KS-1380); the served `/api/docs/openapi.json` was not read; `isExpired`'s Date type from the driver was not traced; other statuses of this operation were not read; the modules are not a fresh `npm ci` at the base.
