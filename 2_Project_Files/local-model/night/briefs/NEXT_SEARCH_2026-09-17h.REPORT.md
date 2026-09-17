# NEXT SEARCH 2026-09-17h (13:11–13:28 AEST): the auth tier, continued

**BLUF: ONE FIT, KS-1009. The public wallet-status route stops returning the owner's `userId`, `role` and `createdAt`. It is one product file (`services/auth/src/routes/wallet.ts`) plus a new in-process vitest file.** `:428` becomes `res.json({ exists: true });`. The service's `noUnusedLocals` then forces four deletions of the now-unread locals (`:409 :410 :419 :420`, TS6133 measured), so the task is five edits in three hunks. **The real `checker.sh` (sha256 `f3ce186c…`, the new A3i build) gave RESULT: PASS (7/7), strict,** on the draft input (fin0) and on the placed input (fin1), at develop `d7e95cd9f`. Three wrong variants failed, each at a named gate: A3b PARTIAL FIX, A3c INCOMPLETE and A3i INDENT SHIFT. Nothing was queued.
- **The spec question (the commission's test for KS-1009): the spec does NOT have to change.** The published 200 schema `WalletStatusResponse` requires only `exists`, and the other fields are optional (yaml parse; the zod source is `.optional()` + `.passthrough()`). So `{ exists: true }` conforms. What goes stale is the operation's description PROSE. That is an owed follow-up in two files, not a gate.
- **KS-805: REFUSED, measured.** Its live item (PATCH `.min(1)`) is one runtime line, but the published PATCH body has no `minItems`. The spec must move in the same PR, which makes it multi-file. Items 2 and 3 read as already closed at the tip by the shared resolver.
- **Second fit: none.** 17g's two remaining single-file auth-tier candidates are now both closed. A second fit would need a re-derivation of 17g's text-screened refusals, which is more than 20 minutes, so it was not started.
- **Wednesday must read before queuing:** see the next section (4 items).

## Wednesday must read before queuing

1. **Closes or Refs.** The ticket's suggested fix is "Return `{ exists: true }` / `{ exists: false }` only". This task trims the REGISTERED branch, which removes the whole enumeration surface. It KEEPS the unregistered branch's `message: 'Wallet not registered'`, which carries no identity and does not vary with input. Dropping it would be a sixth edit, over the five-edit cap. Rule "Closes KS-1009" (the disclosure is gone) or "Refs" with the literal shape as a follow-up.
2. **Behaviour change (TIER 1).** On an unauthenticated, public-by-design route, a registered wallet's answer goes from `{exists, userId, role, createdAt}` to `{exists: true}`. In this repo, 0 of the 9 files that mention `wallet/status` read those fields (read; control `wallet/verify` 12 files). **Not measured:** consumers outside this repo, which the ticket itself flags as the owner's call; a live stack; Akto or Schemathesis on the new body.
3. **The stale prose is owed.** `auth.openapi.ts:1864-1868` and `docs/openapi/secuura-api.yaml:17732-17736` say a registered wallet returns the three fields. That becomes false on merge. The fix is two files, and open **PR #922 edits that yaml**. Hand it to a Claude seat after #922, or add it to the raise PR by hand.
4. **Two of the five edits have no assertion red.** EDIT 1 and 2 (the `let role` and `let createdAt` declarations) are witnessed only by tsc (A7) and by A3b, which names them. EDIT 3 and 4 (the assignments) and EDIT 5 have assertion reds. The commission asks for "each with its own red": this meets it with a gate red, not a cell red, for two of the five. Measured per edit (P6).

## FOUND
- **Pool:** 17g's 70-row auth-tier pool. Its POOL STATE left exactly two single-file candidates, KS-1009 and KS-805, and KS-1208 behind the partition. Linear re-pulled at 13:11:56: 328 KS Backlog/Todo (first:50, 7 pages, hasNextPage false).
- **KS-1009 FITS:**
  - Backlog, High (P2), no assignee, creator Kam, 0 attachments.
  - 1 comment (the 09-08 Akto run). It rules nothing.
  - Related KS-1010, which is an e2e check-that-cannot-fail in a different file and tier.
  - It was held only by the auth-tier line in `queue.md`'s 09-15 comment ("security surfaces … kept for Opus builders").
- **KS-805 REFUSED:** the spec must move with item 1 (see the Rejections table).
- **KS-1208 stands** as 17g recorded it: the gateway's `middleware/auth.ts` is still in seat A's heads (re-measured) and needs a 401-vs-forward ruling.

## TESTED (KS-1009)
- **Scratch clone** `/private/tmp/claude-501/night/s17h/clone`:
  - `clone.sh` (`clone --shared --no-checkout`, 13:11:51);
  - `checkout.sh` (detach at the tip, 13:12:34);
  - `prepare_clone.sh` rc 0 (13:12:39; shared built, source tracked-modified 0).
  - Every vitest, tsc and checker run was under `sandbox-exec nonet.sb`.
- **tsc forces the deletions** (13:13:36–40): the tip is rc 0. With only `:428` changed it is rc 2: `wallet.ts(409,9): error TS6133: 'role' is declared but its value is never read.` and `(410,9) … 'createdAt'`.
- **Test alone at the tip** (13:25:42, final path; also 13:17:28 and 13:18:45 under the first name): 3 run / 1 failed. R1: `expected [ { exists: true, …(3) }, …(1) ] to deeply equal [ { exists: true }, 'next-not-called' ]`. CONTROL and COMPLETENESS are green.
- **Golden** (13:25:44): 3 / 3, tsc rc 0.
- **One edit left out each time** (13:17:42–13:18:01):
  - no `:428` → vitest green, tsc rc 2 (caught by A3b / A7);
  - no `:409` → TS6133 `role`;
  - no `:410` → TS6133 `createdAt`;
  - no `:419` → R1 and CONTROL red by assertion (`role is not defined`), plus TS2304;
  - no `:420` → R1 and CONTROL red, plus TS2304.
- **Discrimination** (13:17:44–50):
  - userId-only trim → R1 red only;
  - registered answers `{exists:false}` → R1 and CONTROL red.
- **Completeness arm** (13:18:42): `expected +0 to be 2`.
- **Test file:** 76 lines. 0 non-ASCII (control: `wallet.ts:412` has 1), 0 backslashes, 0 `$`, 0 backticks, 0 double quotes. The brief's fence equals the golden (python True).
- **Real checker** (`tasks/code_patch/checker.sh`): sha256 `f3ce186cf515626f07d324a7df2218304f058a2b03fb26b9f68ec2c40813b53d`, identical before and after every run. It was `2f0003a87b31…` at 13:11:32, so the checker was swapped before my first run, and every proof below ran on the A3i build.

  **fin1** (`s17h/fin1b`), placed input, 13:27:06–13:27:22, rc 0. Verbatim:
```
mode: code_patch
PASS A1 output is exactly one fenced ```diff block, nothing outside it
baseline suite rc=0 total=751 passed=751 failed=0 suites_failed=0 loaded=1 failed_names=[]
baseline tsc rc=0 (0 lines)
PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)
PASS A3 touched-file set == { Blockchain/Dev/services/auth/src/routes/wallet.ts , Blockchain/Dev/services/auth/src/__tests__/ks1009-security-get-api-auth-wallet-status.test.ts }
PASS A3b every must_change site the ticket names is changed by the product hunk (5 site(s))
PASS A3c every '+' line the brief adds is in the product hunk (1 line(s)), and no tip line is re-added as a '+' (A3d)
A3i: every '+' line the brief adds is in the applied Blockchain/Dev/services/auth/src/routes/wallet.ts byte-exact incl. leading whitespace (apply mode strict): OK 1 line(s) byte-exact incl. leading whitespace (of 1; 1 line(s) added by the apply)
PASS A4 RED-FIRST: src/__tests__/ks1009-security-get-api-auth-wallet-status.test.ts fails at the untouched tip (1 failed / 3 run; controls green; assertion reds)
PASS A5 GREEN-AFTER: src/__tests__/ks1009-security-get-api-auth-wallet-status.test.ts passes with the product hunk (3 passed / 3 run)
INFO control cell present: 2 cell(s) passed BEFORE and 3 AFTER (the harness reaches the code both times)
after suite rc=0 total=754 passed=754 failed=0 suites_failed=0 loaded=1 failed_names=[]
baseline: total=751 failed=0 | after: total=754 failed=0
NEW reds: []
PASS A6 whole services/auth suite: no NEW red vs the untouched tip
PASS A7 tsc --noEmit for services/auth: rc 0 after the patch (baseline rc=0)
INFO tsc on the test file alone: rc=0 (0 lines; not gated — vitest does not type-check and the service tsconfig excludes __tests__)
SUMMARY files=2 +77/-5 test=src/__tests__/ks1009-security-get-api-auth-wallet-status.test.ts red_first=yes apply_mode=strict
RESULT: PASS (7/7)
```
  **fin0** (`s17h/fin0b`, draft input, 13:26:08–13:26:24) printed the same PASS lines and `RESULT: PASS (7/7)`.

  **Why the runs were repeated.** The first proof round (13:20–13:23) used the file name `ks1009-wallet-status-answers-exists-only.test.ts`. That round also passed 7/7, with the same three FAILs. But the builder's `suggested_test_file` is the title slug `ks1009-security-get-api-auth-wallet-status.test.ts`, and `task.md` tells the model to use that path. So I renamed the test to match, left the content unchanged, and re-ran every proof. The first placed brief and input were moved to `s17h/quarantine/placed_v1/`.

  **Wrong variants**, all rc 1, verbatim:
  - `wrong1pb`, placed input, 13:27:22–29. It changes `:428` only:
```
FAIL A3b PARTIAL FIX — the product hunk leaves 4 of 5 named site(s) untouched: :409 `let role: string | null = null;` · :410 `let createdAt: string | null = null;` · :419 `role = result.rows[0].role;` · :420 `createdAt = result.rows[0].created_at;`
RESULT: FAIL (1 failed) — stopped at A3b (a partial fix; the tests are not run)
```
  - `wrong1b`, draft input, 13:26:24–31: the same two lines.
  - `wrong2b`, draft input, 13:26:31–38. All five sites are edited, but the `+` line is `res.json({ exists: true, userId });`:
```
FAIL A3c INCOMPLETE — 1 of 1 line(s) the brief adds are ABSENT from the product hunk: res.json({ exists: true });
RESULT: FAIL (1 failed) — stopped at A3c (a dropped addition; the tests are not run)
```
  - `wrong3b`, draft input, 13:26:38–45. It is the golden with the `+` line indented 2 spaces instead of 4:
```
FAIL A3i INDENT SHIFT — 1 of 1 line(s) the brief adds landed in the applied file with DIFFERENT leading whitespace: :424 indent 2, brief 4 (shifted -2) `res.json({ exists: true });` — indentation shifted by 2 space(s) left; copy the brief's lines byte-for-byte, including leading whitespace (apply mode strict)
RESULT: FAIL (1 failed) — stopped at A3i (an indentation shift; the tests are not run)
```

**NOT tested**
- The model run itself, and the raise.
- Consumers outside this repo.
- The live route: stack, Akto, Schemathesis.
- The prose follow-up.
- KS-805 items 2 and 3 were read, not driven.

## HOW (partition, measured)
- **Linear** (GraphQL read, the Secuura key sourced transiently in python and never printed, no Bearer prefix, first: only):
  - pool pull at 13:11:56;
  - KS-1009 and KS-805 in full at 13:12;
  - KS-1009 and KS-1010 again at 13:19.
- **Open PRs** (GitHub REST GET, paginated, 13:12:23): 20 PRs / 102 paths. **0** name `routes/wallet.ts` or `ks1009`; control: 2 name `services/auth/src`. #922 (KS-679) edits `docs/openapi/secuura-api.yaml`, which this task does not touch.
- **Seat A's six local heads** (`git diff --name-only d7e95cd9f <sha>`, the only verb run in `raise-0916-a`, 13:11:51): 15 distinct paths, 0 are `routes/wallet.ts`.
- **READYs** in `night/`: 110; 0 mention `routes/wallet.ts` (control: 14 mention `services/auth/`). **`queue.md`:** KS-1009 appears in 1 line, the 09-15 hold comment; 0 queue lines. `queue.md` was not touched.
- **Spec:** `yaml.safe_load` of the tip's yaml:
  - `WalletStatusResponse` has `required ['exists']`;
  - the PATCH `/api/oauth/apps/{id}` `redirectUris` has no `minItems` (control: `OAuthAppCreateRequest.redirectUris` has `minItems 1`).
- **Source porcelain** (`--untracked-files=no`) = 0 at 13:21:39, 13:23:49 and 13:27:41. Control: the same instrument on the scratch clone with `wallet.ts` edited gave 1, and 0 after restore. No git write verb ran against `!CODING`.

## Tip
`d7e95cd9f153e9036ed77935a73c93504fa6e3dc`. Read by `git ls-remote <source origin URL> refs/heads/develop`, run from the scratch clone with the source's `core.sshCommand`, at 13:11:51, 13:21:45, 13:23:49 and 13:27:41. It did not move. Both inputs record `tip` = the same SHA (builder runs at 13:26:08 and 13:27:06).

## Files

| file | sha256 | note |
|---|---|---|
| `night/briefs/KS-1009.md` | `7a5525bc094e992d0588a21e0f385d6091be8804e445da9ac22f2557075a2be0` | 260 lines. Its test path == the input's `suggested_test_file`. Text-keyed Where, because all five `-` lines are unique (count 1 each). Every `+` and `-` line's indent is stated in prose ("indent is exactly 4 spaces"). Has `## Premises (measured)` P1–P14 and `## Notes for the raise` (behaviour change, TIER 1, unmeasured external consumers, prose follow-up). |
| `night/inputs/code_1009.json` | `cd843a9e7da9224bac35f277f316f0ebdc68a3b59ef530e1a52614cbac6bbe5c` | `build_input.sh` rc 0 at 13:27:06. 8 Where sites (5 must_change), 1 expected `+`, 1 red cell, ~15.0K prompt tokens, ctx 65536, tip `d7e95cd9f`. |
| golden test | `bcc3bbc83eccc56f…` | `/private/tmp/claude-501/night/s17h/golden.test.ts` |
| golden `out.md` | `259da4d71c7c754d…` | `/private/tmp/claude-501/night/s17h/golden.out.md` (fin1 copy: `s17h/fin1b/out.md`) |
| `night/candidates.md` | `1050a963b6f598fe…` | SEARCH 17h block appended in an HTML comment by `.new` + `mv` at 13:24:25, after a re-read showed the base sha unchanged (`97c427fd…`). Backup `candidates.md.pre-1324-search17h`. Backticks 278 before and after (the block has 0). |

**The queue line (NOT added):**
```
KS-1009 input=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/inputs/code_1009.json task=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/tasks/code_patch/task.md ctx=65536
```

**Rebuild pins** (all required): `product=Blockchain/Dev/services/auth/src/routes/wallet.ts ref=services/auth/src/__tests__/ks942-public-wallet-routes-stay-open.test.ts line=428 ctx=65536`.

## Rejections (the rows are in `candidates.md` SEARCH 17h)

| ticket | verdict | reason |
|---|---|---|
| **KS-1009** | **FITS (briefed)** | See above. |
| KS-805 | REFUSED (measured) | Item 1's runtime `.min(1)` (`oauth.ts:1239`) is not in the published PATCH body (`auth.openapi.ts:2896`; the yaml has no `minItems`). A runtime-only change makes a spec-legal body 400, the positive_data_acceptance drift class. So the spec moves in the same PR: 3 files, and #922 edits the yaml. Items 2 and 3 read as closed at the tip: the resolver refuses a zero-URI state at `:264` / `:288` (KS-822 F-7), and deny returns `authorizeRefusal` at `:658` before any URL is built. Read, not driven. |
| KS-1208 | STANDS (17g) | The gateway's `middleware/auth.ts` is in seat A's heads (re-measured 13:11:51), plus a 401-vs-forward ruling. |
| All other auth-tier rows | STAND (17e/17f/17g/ROUTED/HELD) | Not re-derived. A second fit would require re-measuring 17g's text-screened refusals, which is more than 20 minutes. |

## Deviations
- I used a hand-assembled brief (`s17h/assemble.py`: head + golden fence + tail, with the clock from `date`), not `new_brief.sh`. This is the same deviation as KS-623, KS-1156 and KS-1186.
- **Five edits against the "≤ 3 per task" brief rule, within the commission's cap of 5.** Four are forced deletions, and each edit is named by A3b if it is dropped (P6, wrong1).
- No `cd` and no `rm`. The premeasure test copies went to `s17h/quarantine/`, and `wallet.ts` was restored from `s17h/aside/wallet.tip.ts` after every premeasure (`cmp` rc 0 each time). The clone's porcelain is 0 at the end, and 0 processes were left running. Load 12.2 at 13:23 (other seats); I ran single test files until the golden proof.
