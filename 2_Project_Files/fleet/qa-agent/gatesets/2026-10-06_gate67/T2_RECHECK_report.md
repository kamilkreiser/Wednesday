# gate67 round 2: T2 TEXT re-check, PR #1394 (KS-723)

Independent QA checker for Wednesday. Checking only: no PR, ref, ticket or checkout write.
Scratch: `/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/e2216636-d4a8-4372-af80-77a0943bf859/scratchpad/t2_1394/`

## VERDICT: GO (TEXT round)
**The GO condition.** The merge-in M must have tree **6884601a03dc1685476b69e94efe29a9573d53a7**. That is the key-anchored tree (TAIL rule) on develop **3f9ff4e1e1b93e2e704918a7825f13a72c9ec76f**, which I read by ls-remote at 2026-10-05T23:59:52Z and again at 2026-10-06T00:01:50Z. If develop moves, this prediction no longer holds and has to be redone.

## Rows
| # | Check | Result | Control |
|---|---|---|---|
| 1 | Head unchanged | ls-remote rc 0 at the start (23:59:52Z) and the end (00:01:50Z): pull/1394/head == feature/ks-723-anchors-tx-b64-1 == a94ec8f6a2c6ec382fb7b5dbafcf8a7f9ce68427; develop 3f9ff4e1e1b9 both times. GIT_SSH_COMMAND count in env was 0. The repo's own core.sshCommand was used. | n/a. Same read at both ends. |
| 2 | Live PR body | HTTP 200. sha256 **b6a3686b169002617b11de2d0aabee76509ddd8d422245f68badad4713779e0c**, 6,503 bytes, 6,445 chars, 45 LF, 0 CR, trailing NL. This **equals the READY**. State open, not draft, base develop, merged false, mergeable_state dirty, updated_at 2026-10-05T23:52:47Z. Title is 78 chars and byte-equal to the declared subject. | The old copy (gate67 `api/body_1394.md`, also B66 `boot/pr1394_body_OLD.md`) re-hashes to d6adc2a75838b7e7…, which differs. |
| 3 | Line diff vs OLD | `diff` shows exactly `5c5` and `16c16`. :5 `## NARROWING, not closing` -> `## NARROWING — KS-723 stays open`. :16 `(one hunk at \`:406\`)` -> `(one hunk adding \`:410\`-\`:452\` at this head; \`@@ -409,0 +410,43 @@\` at \`-U0\`)`. With lines 5 and 16 deleted from both bodies, `cmp` rc 0 over 43 lines. | `cmp` on the full files: rc 1. |
| 4 | Closing-word scan, LIVE body | Wide regex: 0. Window scan (family word within 3 lines before a KS-723): 0. Hyphenated keys: only {KS-723: 7}. KS 1005 is de-hyphenated. Co-Authored-By: 0. `Refs KS-723`: 1. `:406`: 0. | 5 of 5 planted positives HIT. "Closes KS-723", "## NARROWING, not closing\n\nKS-723 covers", "fixing: KS-723" and the linear.app URL each hit wide 1 and window 1. "completes #1394" hits wide 1. The OLD body HITS: wide `closing\n\nKS-723`, window line 5 -> line 7. A clean negative text reads 0. |
| 5 | :410-:452 true at the head | `diff -U0 d784b613c81e a94ec8f6a2c6` gives hunk `@@ -409,0 +410,43 @@`. numstat is 43/0, so the added range is 410-452. The file is 569 lines. :410 is the KS-723 comment and :413 is `sharedRegistry.registerPath({`. | Line :406 at the head is `404: commonErrorResponses[404],`, so the old ":406" claim was false. At the default context the hunk is `@@ -407,6 +407,49 @@`. |
| 6 | Declared squash body | The READY's squash body is byte-identical (`cmp`) to B66's Q-SQ proposal in `mail_b66p.txt`. That is 23 lines, sha256 41504672ba75d0f7…. Wide 0, window 0, `Refs KS-723` 1, only KS-723 hyphenated (4), Co-Authored-By 0, `:406` 0, `Merged by Seat B 66th` 1. Subject is `KS-723: declare GET /api/anchors/tx/{txHash} in the published OpenAPI contract`, 78 bytes. | Same planted positives and OLD-body control as row 4, same instrument. |
| 7 | Merge-in prediction on 3f9f | Own `clone --shared --no-checkout`. Fetched 3f9f and a94e by SHA from git@github.com:Secuura/Distributed_Secuura.git using `-c core.sshCommand`, fetch rc 0. Kit c4_docs_gate67.py sha256 cd06394fc964649b… (matches the READY's pin), with G67_SCRATCH set to my scratch. **predict key:** 6884601a03dc1685476b69e94efe29a9573d53a7, rc 0. Flow 9a015f632039: h2 18, 1..14,16,18,19,20 ascending, neighbours 14/18, 0 markers, READ-BACK OK. Cheat 31fa671bc193: h2 8, KS-723 LAST, predecessor KS-938, READ-BACK OK. **predict wrong:** 582e3a4d9fb3…, READ-BACK FAIL on both docs (as required). **mergetree:** rc 1, tree 21c445285cb3…, both docs CONFLICTED, DIVERGENCE. Take-OURS reads back OK but differs from the key blob on both docs, which is the trap again. `diff --shortstat 3f9f 6884601a` gives exactly 5 paths, +354/-0. The added-line multiset (grep ^+, drop +++, LC_ALL=C sort, sha256) is 763449a071a8476e on both 3f9f->key and d784->head. | Predict on 22b2 reproduces gate67's e23888941fda. The 22b2->3f9f multiset is 5ea5f669ad299d31, which differs, so the equality is not vacuous. |
| 8 | Linear KS-723 | GraphQL HTTP 200 (read only): state **In Progress** (started), completedAt null, assignee kamil.kreiser@secuura.ai, attachment #1394 present, updatedAt 2026-10-05T13:38:57Z. | n/a |

## Observations (not blockers)
- **"prefix" contains "fix".** It sits on live body :9 (`…sharing the prefix. **KS-723 stays OPEN…`) and squash :13 (`…the prefix. Kam ruled card secuura-ks723-…`). Neither scan counts it. The wide regex does not match because "." follows "fix". The window scan counts whole words only, and "prefix" is not a closing word. Line :9 is unchanged from the OLD body, and gate67 did not flag it. Linear's magic words are whole words, so I expect no effect, but this is NOT TESTED against Linear itself.
- **3f9f is now present in the shared checkout's object store.** `cat-file -e` in my shared clone returned rc 0 before my fetch. B66 measured it ABSENT at 23:27Z, so someone else fetched it in between. I did not fetch into the checkout. My fetch went into my own clone only.
- **The shared checkout shows 17 porcelain lines** at my end read. I did not take a baseline, so I cannot attribute them. My actions there were read verbs plus `clone --shared` reading from it.

## NOT TESTED
- Linear's actual magic-word parse. Text was scanned; Linear was not exercised.
- Q-M on a real merge-in M. Only predicted, since no M exists.
- Actions on M (RULINGS 3).
- Live sweep, gateway serving, runtime envelope, /api/docs.
- Type-checking of the test file.
- Preflight legs 3, 4 and 8.
- Wednesday's ANSWER confirming Q-SQ: I did not read the ANSWER itself. I confirmed the READY's squash body is byte-equal to the B66 Q-SQ text that the brief says was confirmed.
- Every gate67 product, test, spec and edge row. These carry over unchanged because the head is unchanged; I did not re-run them.

## Writes
This file, plus the scratch dir (clone, PR json, bodies, scan.py, predict/mergetree outputs, linear json). Nothing else.
