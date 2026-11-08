PR 2100: NO GO

# Gate 268, tier 1, round 1 of 2: PR 2100 (KS-1868 O105-P1, originate email.ts, three catches)

Gate: claude-opus-5-5, row G1. Written 2026-11-09 ~03:4x AEDT. Findings only: nothing fixed, posted, mailed or pushed.

| PR | head | verdict |
|---|---|---|
| 2100 | `60e2bf4e6d25de0ffc462b8226ffee39ecc0bce3` | **NO GO** |

Head readings (ls-remote, origin, branch `feature/ks-1868-originate-email-catches-unreadable-throw` and `refs/pull/2100/head`):
- start 2026-11-08T16:15:59Z: head `60e2bf4e6d25`, develop `fa0592f3b6f5` (both equal to the commission)
- mid 2026-11-08T16:32:58Z: head `60e2bf4e6d25`, **develop moved to `6220c168cc92`** (2 first-parent commits, KS-736 and KS-1858; 2 paths, 0 shared with this PR, control self-intersect 2; nothing under originate)
- end: 2026-11-08T16:48:29Z: head `60e2bf4e6d25` (unchanged, so this verdict stands for that SHA), develop `6220c168cc92`

## BLUF

The product change is right and I could not break it. Over 25 thrown-value shapes at each of the three catches (75 cells, base and head driven by the same probe), every ordinary value logs byte-identical text and resolves the same way. Every hostile value that used to make `sendEmail` reject (26 of 75 cells on base, 0 on head) now resolves `false` and logs text. No new hang, no new throw, and no new secret in the log.

It is NO GO on round 1 for two cheap fixes:

1. **F4 is now explained, and the defect is the new test.** Its ACS mock is registered with `{ virtual: true }` for a module that really is installed. Jest 29.7 keeps one module-ID cache per worker, and that cache ignores the virtual flag. So when this file and the KS-1937 test run in the same worker, whichever runs second does not get its ACS stand-in. That breaks either 5 cells of this file or **3 cells of the existing KS-1937 test**, depending on order. Removing the one flag turns both orders green (16/16). It is not a KS-1937 leak, and it is not a product effect.
2. **A false sentence ships in the docs fragment, the PR body and the test header:** "every caller treats `false` as not sent". The notification client's SMTP fallback ignores the boolean and logs "Notification sent via SMTP fallback". This PR moves the hostile-throw case from that caller's "SMTP fallback also failed" warn onto that false "sent" info line (measured).

Neither needs Kam. Both are round-2 sized.

## Findings

### G268-1 (Major, test isolation, introduced by this PR): the new test's `{ virtual: true }` ACS mock breaks this file or the existing KS-1937 test when both run in one worker
- **Where:** `Blockchain/Dev/services/originate/src/__tests__/ks1868-originate-email-acs-and-smtp-catches-unreadable-throw.test.ts:30-43` (the `jest.mock('@azure/communication-email', ..., { virtual: true })`).
- **FOUND / TESTED (MEASURED AT RUNTIME):** `jest --runInBand --no-cache`, the two files, order pinned by my own sequencer (`/private/tmp/g268/probe/seq.js`), DNS refused in process (`/private/tmp/g268/probe/nodns.js`, its refusal text appears in every failing run, so no reproduction after the first reached the network):

  | tree | order | result |
  |---|---|---|
  | head | ks1937 then ks1868 | 5 failed / 16 (ks1868 C1, C2, R1, R2, R3: the real ACS SDK is reached) |
  | head | ks1868 then ks1937 | **3 failed / 16: ks1937 E1 (got false), E2 and E3 (5 s timeouts), plus "Cannot log after tests are done"** |
  | base product (email.ts at develop), same tests | ks1937 then ks1868 | 7 failed: C1 and C2 fail there too, so **not a product effect** |
  | head, ks1937's `jest.dontMock('@azure/...')` removed | ks1937 then ks1868 | still 5 failed, so **not ks1937's dontMock** |
  | head, **only `{ virtual: true }` removed from the new file** | both orders | **16/16 both ways** |
  | each file alone, cold | | 8/8 and 8/8 |
- **Mechanism (READ ONLY, from source):** `node_modules/jest-resolve/build/resolver.js:522-544` (jest-resolve 29.7.0). `getModuleID` caches by `from + delimiter + moduleName + options` and does not include `virtualMocks` in the key. The Resolver lives for the whole worker, not for one test file. So email.ts's lookup of `@azure/communication-email` keeps the ID the first file computed (real-path or virtual). The second file registers its mock under the other ID, and the mock never matches. The package is installed (`@azure/communication-email` 1.1.0 in the lockfile and in node_modules), so the flag is not needed.
- **Who loses:** any single-worker run of the originate suite (`-i`/`--runInBand`, `-w 1`, or a 1–2 vCPU runner where jest picks one worker), and a multi-worker run whenever the scheduler hands both files to the same worker. In my first unstubbed reproduction, the failing cells made a real DNS query (`getaddrinfo ENOTFOUND acs.invalid`).
- **Fix shape (prose only):** drop `{ virtual: true }` from the ACS mock in the new file. Add a regression check that runs the pair in both orders in one worker. The READY's ticket candidate "the stand-in not applied after ks1937" should not be filed against KS-1937 as written.
- Whole suite single-worker at head: `jest -w 1` over all 221 originate suites (`/private/tmp/g268/out/whole_w1.json`). ks1937 ran at position 98 and ks1868 at 106, and ks1868's five ACS cells (C1, C2, R1–R3) failed, which is consistent with this finding. **However, this substrate is NOT a usable whole-suite baseline:** 144 suites and 1742 of 2572 cells failed overall, unrelated to this PR. Likely causes are my in-process DNS refusal and the borrowed node_modules under one worker. I did not run a base comparison, so no whole-suite figure from me should be weighed. The pinned pair runs above are the evidence.

### G268-2 (Medium, words that ship): "every caller treats `false` as not sent" is false; at the notification client this PR turns a hostile-throw failure into a "sent" log
- **Where the sentence is:** the flow fragment `Projects Documents/fragments/flow/KS-1868-originate-email-acs-and-smtp-catches-unreadable-throw.html` (first table cell), the PR body Summary (draft `5_Project_History/2026-11-09_seatT-16th/drafts/pr_rest_ks1868.md`), and the test header (`ks1868-...test.ts:5`).
- **The callers (READ):**
  - `utils/notificationClient.ts:84-113` awaits the send functions, ignores the boolean, then logs `logger.info('Notification sent via SMTP fallback')`.
  - `routes/adminConfig.ts:1516` is fire-and-forget (`.catch(() => {})`).
  - Only `adminConfig.ts:1650` reads the boolean (`emailSent`).
- **MEASURED AT RUNTIME** (`/private/tmp/g268/probe/g268-caller-probe.test.ts`; real email.ts and real notificationClient; fetch, nodemailer and logger stubbed; base vs head):

  | thrown at SMTP send | base logs | head logs |
  |---|---|---|
  | ordinary Error | warn unreachable, **info "Notification sent via SMTP fallback"** | same (pre-existing) |
  | getter throws / revoked Proxy / `null` | warn unreachable, **warn "SMTP fallback also failed (non-blocking)"** | warn unreachable, **info "Notification sent via SMTP fallback"** |

  The `[Email/SMTP] Failed to send: ...` console.error line is still written on head, so the failure is not invisible. But the caller's structured log now says "sent" for a send that failed.
- **Severity reasoning:** the caller's misreport is pre-existing for ordinary errors, and the product change is correct against `sendEmail`'s documented contract. The defect here is the sentence, which ships in a client-readable fragment, and the unnamed side effect on this caller. **Fix shape:** correct the sentence in all three places (for example "callers that read the result treat `false` as not sent; the notification client's fallback does not read it") and name the notificationClient effect in the PR. Whether to make the caller honour the boolean is a separate ticket, not this PR.

### G268-3 (Low, words / unnamed behaviour): a thrown `null` or `undefined` at the SMTP site changes from reject to "unreadable thrown value", and the three catches now disagree on it
- **MEASURED (probe, `smtp/nullThrown`, `smtp/undefinedThrown`):**
  - Base: rejects (`TypeError: Cannot read properties of null`).
  - Head: resolves `false` and logs `[Email/SMTP] Failed to send: unreadable thrown value`.
  - The same `null` at the two ACS catches logs `...: undefined` on both base and head, because they read `err?.message`.
- None of the PR body, ticket comment, cheat or flow names the thrown-null case. "A missing message (`undefined` or `null`) is logged as before" is true for an Error-like object whose message is missing (measured `msgNull` SAME), but a reader could take it to cover a thrown `null`, which changed.
- The constant also misdescribes `null`: it is readable, it just has no message.
- **Fix shape:** one sentence in the PR body and the flow fragment. Optionally use `error?.message` in the SMTP catch so the three sites agree. KS-2099 item 1 edits this catch next anyway.

### G268-4 (Low, words): "Log text only" understates the change
- The ticket comment BLUF ("Log text only."), the PR Summary heading ("PRODUCT BYTES CHANGE, log text only") and the cheat ("It changes log text only for an unreadable value") all say this.
- The change also moves `sendEmail` from **reject to resolve `false`** for 8 value shapes at each ACS site and 10 at the SMTP site (measured, Q1), and moves `getAcsClient` from reject to `null` (the ACS-init hostile cases now fall through to SMTP).
- The same sentences state the reject-to-resolve effect elsewhere, so a careful reader can piece it together. A client reader skimming the BLUF cannot.

### G268-5 (Low, the seat's evidence): all seven of the seat's tsc planted-error controls fired on a config error, not the planted type error
- `evidence/pA_ks1868/*_tsc_control.out`: 7 of 7 contain `TS6059` (file not under `rootDir`), 0 contain `TS2322`, 1 `error TS` line each (instrument: `/usr/bin/grep -ci` per file). Those controls would fire even if type checking were broken, so they prove nothing about it.
- **Not a product risk:** my own control, a planted `TS2322` inside `src/` in a copy of the head tree, reads 5 lines with the planted one named. That reproduces the seat's counts under a valid control (see Q4).

### Notes (no severity)
- **N1.** The seat's "20 of the last 40 first-parent commits carry a pair" reads **22 of 22** on my classifier (any `Blockchain/Dev/**/src/` file outside tests). Both are under develop `c0e6e744b7b2` and `fa0592f3b6f5`, with every product commit carrying a cheat+flow pair. The ruling's premise holds and only the classifier differs.
- **N2.** The test file has no import or export, so its top-level names (`mockH`, `TO`, `P_INIT`, `savedEnv`, `LINES`, ...) are global script names. This is the same class as the ks488/ks1937 collision. Today's program has 0 errors in this file, but a future test reusing one of these names will collide. Making it a module (`export {}`) closes the class (KS-1989 precedent).

## Answers to the commission's questions

**Q1 Product (MEASURED AT RUNTIME, `/private/tmp/g268/probe/g268-probe.test.ts`, 25 values × 3 sites, base = email.ts at develop, head = PR):**
- **Ordinary values, byte-identical log line and same outcome at all three sites:** `Error`, `TypeError`, `Error('')`, unicode/newline message, bare string, number, `Symbol` thrown, plain object with no message, `{message: 7}`, `{message: null}`, message object with `toString`, `BigInt` message, a circular object whose message is a string, a 5,000,000-char message, and a message containing the recipient. That is 49 of 75 cells SAME (outcome and every logged line), which at the ACS sites includes thrown `null`/`undefined`.
- **Hostile values, base rejects and head resolves `false` with text, at all three sites:**
  - getter throws; getter throws `null`; Proxy whose get trap throws; revoked Proxy; message object whose `toString` throws; `Symbol.toPrimitive` returning an object; circular `message === err` (RangeError).
  - All of these log `unreadable thrown value`.
  - A Symbol message logs `Symbol(msgsym)`.
  - SMTP only: thrown `null`/`undefined` (G268-3).
- **No path now throws:** 0 rejections on head out of 75 cells.
- **No hang:** every cell completed in 0–1 ms on both trees, including the 5 MB string. A getter that never returns was not run (it would hang both trees identically, since each reads `message` once).
- **No new secret in the log:**
  - The recipient, ACS access-key and SMTP password sentinels appear in head output only where base already had them.
  - The positive control `msgContainsRecipient` reads TRUE on both trees. That is pre-existing: provider error text is forwarded verbatim, as KS-1937's header already says.
  - Recipient, key and pass are all FALSE in the other 72 cells on both trees.
- **What the caller receives changes:** reject becomes resolve `false` for the hostile set. At the notification client that turns a failure warn into a "sent" info (G268-2).

**Q2 Scope (READ):** `git diff fa0592f3b6f5...60e2bf4e6d25`: 4 files.
- email.ts has three hunks. Each replaces exactly one `console.error` line inside the three named catches with a guarded read. 3 lines removed, 24 added; the `+/-` lines equal the held patch's section 1 exactly.
- No other catch, WARN line, import or signature changed. The `[Email/ACS] Send failed`, allow-list WARN, no-provider, misconfig and "falling through" lines are byte-unchanged.
- The other paths are the new test and the two fragments.

**Q3 Test quality (MEASURED):**
- **Red first reproduced.** With email.ts at develop, 5 of 8 fail (R1–R5, each `toEqual` on `{ok,sent}`) and 3 controls pass. At head, 8 of 8.
- **Three plants of my own, each caught:**
  - (P1) the ACS-send catch's `String(m)` → `String(m).slice(0,5)`: C2 and R3 fail.
  - (P2) the init catch's guard removed (unguarded `err?.message`): R1 fails.
  - (P3) the ACS-send catch's `String(m)` → template `${m}`: R3 fails.
- **Gaps:** no cell covers a thrown `null`/`undefined` at SMTP, and nothing covers the notification-client effect. The P3 plant shows R3 is what distinguishes `String()` from a template.
- **F4: test-isolation defect in the new file.** It is not a pre-existing ks1937 leak and not a product effect. Evidence in G268-1.

**Q4 Renamed test (MEASURED):**
- **All-originate tsc program** (my scratch tsconfig extending originate's: tests included, `noEmit`, `types: jest,node`), run on exact git file sets:
  - develop file set (312 files under src): 4 `error TS` lines.
  - head (313 files): 4, with 0 in the ks1868 file.
  - The 4 are ks1937 (TS2300, TS2451) and ks488 (TS2300, TS2451), identical to the seat's list.
  - Control: a planted TS2322 in a copy reads 5 and names the file.
- **Cold `--runInBand --no-cache` pair ks1868+ks1937:** both suites load and run, 16 cells executed, no TS diagnostic. The ACS failures are G268-1.
- **The 14-line edit:** verified as the seat states. Blob `174e316a0978`, sha256 `66eed243191ae6e9…` at head, `ca6d92c47c280516…` for the Spark copy. Line citations 138/173/223 match head email.ts.

**Q5 Words:**
- **Checked true:**
  - blob ids `78eed82ffe66` and `d81394daeae8`
  - patch sha256 prefix `0e23427d65d87c46`
  - the develop move c0e6→fa05 (6 files: api-gateway, systemTest, two api-gateway fragments; 0 overlap)
  - three catches at 138/173/223
  - red-first 5 of 8 by assertion
  - the 4/4 tsc figures
  - ACS and SMTP failure descriptions
  - "a hostile value takes the path an ordinary Error already takes"
  - KS-2099 item 1 overlap
- **False:** "every caller treats false as not sent" (G268-2).
- **Incomplete:** thrown null/undefined at SMTP (G268-3), and "log text only" (G268-4).
- **Superseded by this gate:** F4's "cause not investigated". The ticket candidate wording "the stand-in not applied after ks1937" would misfile it (G268-1).
- **Not checked:** the live PR body and live ticket comment bytes. The commission allows no network beyond git fetch, so I read the seat's drafts: `pr_common_head.md` + `pr_rest_ks1868.md` and `ticket_comment_ks1868.md`. Their sha1 does not match the posted `body_sha1` byte-for-byte, because the builder substitutes `@@PII@@`, `@@PREFLIGHT@@` and `@@PR@@`. The eslint 29→30 figure was also not checked (see below).

**Q6 Merge:**
- **Merge base** with develop `fa0592f3b6f5` is `c0e6e744b7b2` (the PR's parent). The develop delta (6 paths) and the PR delta (4 paths) are disjoint (instrument `comm -12`, control self-intersect 6). The later develop `6220c168cc92` adds 2 more disjoint paths.
- The merge is clean by disjoint paths (READ ONLY). `git merge-tree` was refused by the fleet's no-write-verb hook and was not run.
- **Open-PR census:** I fetched `refs/pull/N/head` for all 151 PRs numbered 1950–2101 and diffed each against its merge base with develop on the PR's 4 exact paths. Only PR 2100 (positive control) and PR 2056 touch a shared path. PR 2056's email.ts result blob equals develop's (`78eed82f`; landed as `90b500e1`, KS-1937), so it is already merged.
- **Not covered:** open/closed state (no API), and PRs below 1950.
- KS-2099 item 1 will edit the SMTP catch after this merges, and G268-3 is relevant to it.

## What was NOT tested
- A real ACS or SMTP provider. A booted service. Node 24 (I used v26.8.1). The platform suites.
- eslint: flat config ignores files outside cwd, and the rules forbid cd.
- The docs-fragments checker.
- A non-terminating getter.
- The live PR and ticket bytes.
- Whether the project CI runs originate jest single-worker. `git grep` finds no jest in `.github/` at head; the positive control in the same grep was `extranet-test-run.yml --workers 4`.

## Substrate (named, as the template requires)
- Tree: `git archive` of head `60e2bf4e6d25` into `/private/tmp/g268/head`.
- node_modules: symlinked read-only to gate 258's install, `/private/tmp/g258/Blockchain/Dev`. Its `.package-lock.json` matches develop `fa0592f3b6f5`'s lockfile for every relevant package (zod 4.6.7, jest 29.7.0, ts-jest 29.4.11, typescript 5.9.3, nodemailer 10.2.1, @azure/communication-email 1.1.0). The differences are 54 foreign-platform optional binaries and `set-cookie-parser`.
- The project checkout's own node_modules (`a65ae7ed`, installed 2026-09-03, zod 3.25.76) is stale and fails every cell. I tried it first, and it is quarantined.
- `packages/shared/dist` was built by me with tsc (0 errors).
- Variants (base product, plants, F4 edits) are per-variant copies of `services/originate`.

## Own conduct
- **One real DNS query.** My first F4 reproduction ran without the DNS stub, and the failing cells resolved `acs.invalid` (`getaddrinfo ENOTFOUND`). That is network beyond git fetch: one lookup of a reserved non-resolving name. Every later run had in-process DNS refused, and that refusal is visible in the output.
- **Two hook refusals.** The hook refused `git checkout` and `git merge-tree` in my own clone (it reads a `$R` clone path as outside). I used `git archive` and path disjointness instead and did not bypass it.
- My first background `find` over the WEDNESDAY tree ran long, and I stopped it.
- **Nothing removed.** Superseded node_modules links and the shared dist are in `/private/tmp/g268/_quarantine_2026-11-09/`.
- **Clone and scratch left in place:** `/private/tmp/g268`, 300M (`du -sh` at end).
- Project checkout: read verbs only, with `GIT_OPTIONAL_LOCKS=0`.
- DevMASTER free space stayed at 14 GiB. load1 stayed between 2.99 and 5.81.
- No PR comment, no ticket write, no mail, no push.
