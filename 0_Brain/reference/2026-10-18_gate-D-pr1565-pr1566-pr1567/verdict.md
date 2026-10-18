#1566 KS-1541 @ 3697013868483a28c2da99169b5c8cdd4aef2427: GO WITH NOTE (tier 2; red-first 3/3 and green 6/6 reproduced, 13/16 mutants killed; the 3 survivors (M3, M8, and the M9 bound) are notes, not defects)
#1565 KS-724 @ 47ca56213b6eb7b34d30fd91aea411478f33d9b1: GO WITH NOTE (tier 3; comment-only proven by token stream 270 = 270; quote "Accept as built" matches the card verbatim; the time in the header does not match the card's ruled_ts)
#1567 KS-1614 item 4 @ 09de80685fb6b0945cae4908723d67e6a10c76ce: GO (tier 3; test-only, byte-identical to the golden; green at the tip, red for the right reason under the :157 tamper; api-gateway 1166/1166)
sha256/16: dacec9e78fccfe6e

# GATE D, round 1 of 2: #1566 + #1565 + #1567 (Opus QA gate, findings only)

Live develop re-read 20:37:24 AEDT by `git ls-remote`: d2ec786e6130c7ce13384185c84cc1e7566d77cb, unchanged since R raised all three. All three heads equal the brief and ls-remote. #1555 (head 986732cf) has NOT landed. Clone: /private/tmp/claude-501/gateD-1567/repo (git clone --shared, origin Secuura/Distributed_Secuura, fetched with the checkout's core.sshCommand plus ServerAliveInterval=30). Raw outputs: evidence/ in this folder.

## FOUND

### #1566 KS-1541 (tier 2)
- **LOW: the relayed error text has no length bound.** `Blockchain/Dev/services/mcp-server/src/tools/info.ts:131` copies `data.error` (a string) or `data.error.message` (a string) into the note as it is. A 503 carrying a 100,000-char message produced a 100,045-char note (evidence/14_1566_probes.txt, "503 100KB message"). Newlines and quotes are relayed raw (JSON-escaped in the tool's output, so they are harmless). On secrets: only those two fields are read, plus the status number. No header, no other body field, no stack. The gateway's own texts on this route are fixed literals (`api-gateway/src/services/health.ts:42,70,75,85`, `middleware/auth.ts:368,442,495,530`). Its terminal handler redacts every 5xx to "An unexpected error occurred" (`api-gateway/src/middleware/errorHandler.ts:84`). So against the real gateway the text is bounded (at most about 90 chars) and holds no secret. The unbounded case needs SECUURA_API_URL to point at something that is not the gateway (a proxy, or a misconfigured URL). A `.slice(0, N)` mutant survives (H1-M9), so no test pins either behaviour.
- **NOTE: "refused" is also said of statuses that are not deliberate refusals.** `info.ts:129,132` treats every non-ok status except 401/404 as "refused by the gateway". At the head: 400, 429, 500 and 502 (an HTML proxy page) read `Connector info refused by the gateway (502)`. C3 pins this for 500, and the brief at night/briefs/ks_1541_p1/KS-1541.md:18 intends it. So it is to spec. The comment's claim that "any status but 401/404 is the gateway REFUSING on purpose" is wrong for a crash or a proxy 502, but the note now carries the status, so the reader can tell.
- **NOTE: two surviving mutants (test gaps, behaviour is right at the head).** (H1-M3) Dropping `!connectorResult.ok` from `info.ts:132` survives. At the head, a 200 with a JSON `null` body correctly reads the old note (probe "200 JSON null"). Under the mutant it would read "refused by the gateway (200)", and no cell drives a 200 with a falsy body. (H1-M8) Loosening `typeof …message === 'string'` to `!= null` survives. At the head, `{error:{message:123}}` gives no text (probe), and no cell drives a non-string message.
- **NOTE: the nested ternary at `info.ts:131` was read branch by branch.** None of its 3 branches is unreachable or wrong. Branch 1 (string error) is reached by C2. Branch 2 (an `error.message` string) is reached by C1. Branch 3 (`''`) is reached by C3 and by these probes: error null, a number message, code only, `''`, a top-level `message`, a JSON null body, a JSON string body and a non-JSON body. Each was killed by its own mutant (H1-M6, H1-M7, H1-M10). `typeof null` is 'object', but `?.message` guards it (probe "403 error null" gives no text and does not throw). The `as unknown as` cast on :130 exists because `api-client.ts:125` types `error?: string`, while the gateway sends `{code, message}`. That typing predates this PR (out of scope).
- Diff scope is clean: 2 files, +62/-1, exactly the named ones. Its +/- lines are the same 63 lines as night/briefs/ks_1541_p1/golden.diff (only the order of the files differs).

### #1565 KS-724 (tier 3)
- **NOTE: the header's time does not match the card.** `systemTest/akto/src/scan/credentialLiveness.ts:88` says "2026-10-18 19:00:36 AEDT". decisions.json gives card secuura-ks724-locked-account-template-exclusion-1015 `ruled_ts` 2026-10-18T19:02:56.744834+11:00 (evidence/32_1565_card.txt). Wednesday's daily note puts the tap at 18:59-19:00 and says reconcile_rulings applied it at about 19:0x. So 19:00:36 is probably the tap time from the cloud chat and 19:02:56 the apply time. I could not find 19:00:36 in any local file, so it is not verified. The quoted words are verbatim: option (a) label "Accept as built", `ruled_choice` "a", status "ruled". The scope sentence ("covers this one id") matches option (a)'s detail.
- Comment-only is proven. The TypeScript scanner token stream, comments skipped, is 270 = 270 tokens with the same sha (7c3dd36dcd67d686) at develop and the head. The comment-trivia count is 13 = 13, so the 5 lines are inside the existing JSDoc block. Planted control: removing one `readonly` token gives 269 tokens and a different sha, so the comparison can see a one-token change.

### #1567 KS-1614 item 4 (tier 3)
- No findings. Product files changed: NONE. verification.ts has the same blob (3741ef9f) at develop and the head. golden.diff applied to develop's test file is byte-identical to the PR's file (cmp). The PR's hunk is +7 against the golden's -1/+8, which is the same bytes.

### Merge prediction (live develop d2ec786e)
- Each alone is clean: #1565 -> tree 18e11bfd, #1566 -> 33f3bb72, #1567 -> c81de14a.
- All three, in all 6 orders: clean, and every order gives tree 9c0e81f9f6e1039a96714796655bc06860a35206. That equals R's prediction.
- Overlap: 0 paths shared between the PRs. Develop has touched none of the 4 files since the merge-base, which is d2ec786e for all three.
- Planted conflicting control: a develop-side commit editing the old note line in info.ts makes merge-tree with #1566 return rc=1, with stages 1/2/3 on info.ts (the check can see a conflict). The same planted commit with #1565 is clean (disjoint).
- If #1555 lands first: #1555 has 7 files, 0 shared with these three. #1555 then all three is clean, giving tree 1d7f47fa5cfa.

## TESTED / HOW
- **#1566 red-first:** the PR's test file was copied onto develop's info.ts (blob c0f2268c). Result: 3 failed / 3 passed, and the failures are exactly C1, C2 and C3, each with Received = the old note (evidence/11). **Green at the head:** 6/6 (evidence/10).
- **#1566 mcp-server suite at the head:** 4 files, 11/11 passed (evidence/12). Author's 5 -> 11 confirmed.
- **#1566 tsc:** the repo's tsconfig (which excludes `__tests__`) gives rc 0. tsconfig.gate.json includes the tests, and `--listFilesOnly` confirms the ks1541 file is in the program: rc 0. Planted control: a `number = "string"` appended to the ks1541 test gives rc 2 with TS2322 at ks1541…test.ts(57,7); restored, 0 diff (evidence/13). ESLint on both files: rc 0 (evidence/16).
- **#1566 reply shapes:** 26 shapes through a mocked api-client, plus 9 through the REAL api-client with a stubbed global `fetch` returning real `Response` objects (HTML 503, empty 403, HTML 502, `null` 200, fetch throws). All 26 also ran on develop as the baseline (evidence/14). The notes at the head:

  | Gateway reply | Note at the head |
  |---|---|
  | 200 | connector relayed |
  | 200 `{}` | `{}` relayed, same as before |
  | 200 `null` | old note |
  | 401 (with or without body) | old note |
  | 403 with error object | `refused (403): <message>` |
  | 403 with string error | `refused (403): <string>` |
  | 403 with no, empty, non-JSON, null or string body, or a non-string/missing message | `refused (403)` |
  | 404 | old note |
  | 429 | `refused (429): Too many requests` |
  | 400 | `refused (400)` |
  | 500 redacted | `refused (500): An unexpected error occurred` |
  | 502 HTML | `refused (502)` |
  | 503 gateway JSON | `refused (503): Connector allow-list configuration could not be read; …` |
  | 503 HTML or empty | `refused (503)` |
  | thrown / network | old note |

  No shape gave `isError`.
- **#1566 mutants:** 16 mutants plus 1 comment-only control, run against the ks1541 and ks1232 files (evidence/15). The control is green as expected. Hunk 1: M1 (drop !==404), M2 (drop !==401), M4 (drop null-guard), M5 (only 403/503), M6 (drop string branch), M7 (drop message branch), M10 (always append ': '), M11 (read data.message), M12 (constant status) and M13 (error.code for message) are KILLED. M3, M8 and M9 SURVIVED (see FOUND). Hunk 2: M1 (revert to the old literal), M2 (an extra field) and M3 (always the refusal form) are KILLED. The file was restored, and git status is clean.
- **#1567:** at the tip the file is 26/26 green. With the KS-1614.md tamper planted at verification.ts:157 (`Object.prototype.toString.call(value)` -> `String(value)`, the line asserted before the edit), only the new cell is red: `expected '1' to be '[object Array]'` at test.ts:171, an assertion failure, with the first expect (toThrow) still passing. The same tamper on develop's test file is 25/25 green, which reproduces M2 surviving before this PR. Restored, 0 changed. api-gateway suite: 120 files, 1166/1166 at the head and 1165/1165 at develop (evidence/20, 21). That includes the KS-1090 test-typecheck gate, so the new `[1n]` cell is type-checked. ESLint on the test file: rc 0 (evidence/22).
- **#1565:** `npm run format:check` (prettier, whole akto) passes. Prettier on the file alone passes. no_kamil_verbatim_header.test.sh: 4 passed, 0 failed (1245 files scanned, both planted controls found). akto unit tests/unit/scan/: 19 files, 309/309 (evidence/30).
- **Merge:** `git merge-tree --write-tree` (git 2.51.0), chained with commit-tree in my clone (evidence/40).

## NOT tested
- **Legs 3, 4 and 8** (the local stack): no Docker and no live gateway, per the rules. No real HTTP was sent to a running api-gateway `/api/connector/info`. The gateway's 403/503 bodies were taken from reading health.ts and errorHandler.ts and fed through real `Response` objects, not taken from a live process.
- **The full akto unit suite, as the author's 2035/2035:** here it is 5 failed / 2017 passed (2022). The failures are in lintOverrideHygiene, lintToolchainPins and lintConfigContract (the oxlint toolchain), and they are IDENTICAL on develop d2ec786e (evidence/31). The cause is my environment: node_modules is borrowed from the project checkout, which sits at 76698952. The PR cannot cause them, because its token stream is unchanged. akto `lint` (tsc + oxlint) was not run, for the same toolchain reason.
- **node_modules** is symlinked read-only from the project checkout (develop 76698952). For api-gateway, the worktree got its own node_modules overlay, and `@secuura/shared` was rebuilt from the worktree's own source. The first run against the checkout's stale shared dist failed 9 tests on BOTH develop and the head (kept as evidence/20_1567_run1_stale-shared-dist.txt). The mcp-server and akto runs used the checkout's packages as they are.
- I did not compare against R's preflight 13/16 (legs 3, 4 and 8 skipped).
- Whether 19:00:36 is Kam's tap time: no local record found.

Severities: #1566 1 LOW (info.ts:131, unbounded relay, unreachable against the real gateway) and 3 NOTE (info.ts:129/132 wording, M3/M8 test gaps, api-client.ts:125 typing). #1565 1 NOTE (credentialLiveness.ts:88 timestamp). #1567 none. No HIGH or MEDIUM. Merge only on Wednesday's head-bound GO; nothing deploys.
