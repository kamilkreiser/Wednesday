PR 2129: GO WITH NOTES; PR 2130: GO WITH NOTES

# Gate 286, tier 1 batch (Opus): PR 2129 (KS-784) and PR 2130 (KS-624). Verdict

| PR | head | verdict |
|---|---|---|
| 2129 (KS-784, Seat R 91st) | 902b3161e4350df9468c7459f2c402d291c4a721 | GO WITH NOTES |
| 2130 (KS-624, Seat Y 10th) | 11a39402623328f2ee8368284cd397630bca13d5 | GO WITH NOTES |

**Pins.** I read them with `git ls-remote` at 06:01:16Z (start) and 06:13:02Z (end). Both reads were identical, so nothing moved: develop 6beac8734a2f, 2129 902b3161e435, 2130 11a394026233, 2080 83ee8509c985 (files /private/tmp/g286/pins_start.txt and pins_end.txt). Both PRs were cut from 204e62acdc35. Develop's one-commit move to 6beac87 (PR 2112) touches `services/transfer/src/services/transferAccess.ts` (a comment-only change, +3/-1) and two KS-2120 fragments. It shares no path with either PR.

**Merge trees** (`git merge-tree --write-tree` in my clone, all rc 0, no conflicts):
- develop + 2129 and develop + 2130 are both clean.
- 2129 + 2130 is clean, and both orders give the same tree, ba9f8d831807.
- 2129 + 2080 is clean, and both orders give the same tree, e34e7987b3e8.
- 2130 + 2080 is clean.

**Open-PR census.** My instrument was `ls-remote 'refs/pull/*/merge'`, which found 56 refs.
- Positive controls: 2129, 2130, 2080 and 2127 are all present, and all 54 PRs in gate 285's 16:35 open list are present.
- Negative control: merged PR 2112 is absent.
- I fetched all 56 heads and compared their paths, each against its own merge base with develop. The only other PR on either PR's paths is **PR 2080**, on `m365-integration/src/index.ts`. Nothing else is on prism.
- Planted control: adding `services/prism/package.json` to the path list makes PRs 575 and 649 appear, which matches the seat's own planted read.
- **Merge order:** none required. Every pair is clean in both orders.

No finding below needs Kam's ruling.

---

## PR 2129 (KS-784): GO WITH NOTES

**BLUF.** The reorder does what card row A2 asks and nothing else. The Teams webhook address is now checked before the Microsoft 365 configuration check, and the guard that runs is the real `assertSafeOutboundUrl` (MEASURED AT RUNTIME).
- `requireM365` is removed from this one route only. No other route's middleware list changed. The 503 body is the same constant object, sent by the same function.
- The red cells, the controls and the seat's mutants reproduce. My own two mutants were caught.
- The suite reads 303/303, and 318/318 when merged with PR 2080.
- The notes: one Minor about the guard's refusal text now being reachable on unconfigured stacks, and two Nits in the PR body's figures.

**Q1, the reorder** (MEASURED AT RUNTIME unless marked otherwise)
- **Only this route changed.** I diffed every `^app.` line and every `requireM365` line between develop and head (/usr/bin/grep -i). There are 32 route lines on each side. The only route-line change is `app.post('/api/teams/webhook-config', requireM365, async` becoming the same line without `requireM365`. `requireM365` stays on connections/init, connections/:id/refresh, sites, documents/sync, onedrive (both routes), GET webhook-config and outlook/exchange-token.
- **The 503 body is identical.** The handler calls `requireM365` itself (index.ts:1302-1304), and `requireM365` sends `M365_UNAVAILABLE_RESPONSE` (index.ts:150, sent at 267). Cell C1 matches the full body with `toEqual`.
- **The guard is the real one, and it is reached for every form.** I wrote a probe suite: the seat's harness with `dns/promises.lookup` spied on, so no real DNS was used. The spy is shown to work by the public-hostname control: its lookup is recorded, and the configured stack stores it with 201. I sent 25 webhookUrl forms to an **unconfigured** stack at head:
  - These IP and address forms all get 400 `webhookUrl rejected` with no lookup and no insert: decimal `2130706433`, hex `0x7f000001`, `127.1`, `0`, `[::1]`, `[::ffff:169.254.169.254]`, `[::ffff:a9fe:a9fe]`, `[fe80::1]`, `[fd00::1]`, NAT64 `[64:ff9b::10.0.0.1]`, userinfo `93.184.216.34@127.0.0.1` and `user:pw@169.254.169.254`, `localhost`, `localhost.`, `metadata.google.internal`, the single label `intranet`, 192.168/16, CGNAT, `ftp:` and `javascript:`.
  - Hostnames that resolve to a private address, or to one public and one private address (the mixed case), are refused after the lookup. NXDOMAIN is refused too.
  - Controls: a public IP, and a public hostname, both get the 503.
  - The same 25 forms on develop all get 503 with zero lookups.
  - Redirects: there is no outbound request at registration. The notify route re-checks the address and pins the connection (KS-914, READ ONLY). Files: /private/tmp/g286/probe_head.txt and probe_dev.txt.
- **Consequences.**
  - A token with no organisation on an unconfigured stack now gets 403. Cell R5 shows it, and my probe `nouser` gets 403 with zero lookups.
  - A hostname is resolved before the 503. My probe CTRL-public-host shows a recorded lookup followed by the 503.
  - DNS is not reachable by an unauthenticated caller. Within the handler, `requireCallerOrg` runs first, so a caller with no organisation gets 403 before any lookup (MEASURED). Before the handler, `app.use('/api', jwtAuthenticate(...))` at index.ts:709 runs ahead of the route at :1276 (READ ONLY: my harness mocks `authenticate`).

**Q2, red first.**
- With the new suite on develop, exactly R1-R5 fail, each one 503 SERVICE_UNAVAILABLE, and C1-C3 pass (/private/tmp/g286/r784_dev.out). At head all 8 pass.
- Seat mutant S1 (`requireM365` back on the route) turns exactly R1-R5 red. Seat mutant S2 (the check removed) turns exactly C1 red.
- **My own mutants:**
  - G1 moves the configuration check to between the Zod parse and the guard. Exactly R1-R3 go red.
  - G2 drops the `if (!m365Configured) return;` line. C1 goes red.
- The m365-integration suite at head reads **303/303 in 32 files** (vitest).
- `tsc --noEmit` reads 0. My planted control (a TS2322 type error) makes it fail with rc 2.

**Q3, the notify comment.** The comment says registration "stores nothing wherever Entra is unconfigured" and that the notify route "is not gated". Both are true at head. The notify route is declared at index.ts:1381 with no `requireM365`. C1 and the probes show zero inserts on an unconfigured stack.

**Q4, PR 2080.**
- 2080's head is 83ee8509c985, unchanged since the seat's read.
- I merged in both orders and got the same clean tree. In the merged index.ts, all **23** lines that 2080 adds are present (22 non-blank; numstat 23/5), none of its 5 removed lines remains, and all 15 of 2129's added lines are present. Control: deleting one of 2080's lines from my copy of the merged file makes my checker report 1 missing.
- The m365 suite on the merged index.ts, with 2080's test file added, reads 33 files, **318/318**.

### Findings, PR 2129
- **G286-2129-1, Minor. index.ts:1286-1292 with packages/shared/src/security/ssrf-guard.ts:338-343.** On an unconfigured stack, an authenticated caller whose token carries an organisation can now make m365-integration resolve any hostname. The 400 text then repeats the address it resolved to, for example `host "ks784-private.example.com" resolves to 10.1.2.3, which is forbidden: RFC1918 private`. That is an internal-DNS oracle, newly reachable wherever ENTRA_* is unset. It already existed on configured stacks, and the DNS-before-503 order is the ruled consequence. What the PR body does not state is that the refusal text carries the resolved address.
  - FOUND / TESTED / HOW: probe host->private and host->mixed, MEASURED AT RUNTIME with the lookup mocked.
  - Not a blocker. Fix shape for the owner, for a follow-up: return a fixed refusal text and keep the detail in the log.
- **G286-2129-2, Nit. PR body, "303 of 303, 76 files".** 76 is the number of describe-suites (`numTotalTestSuites` in the seat's own S2_m365_fixed.json), not files. vitest at head reads 32 files. The 303 is correct.
- **G286-2129-3, Nit. PR body and READY, "all 19 of 2080's added lines".** 2080 adds 23 lines to index.ts (22 non-blank), and all of them survive. Only the count is wrong; the conclusion stands.
- **G286-2129-4, Info.** The order requireCallerOrg → schema and guard → `requireM365` → insert, and the 403 consequence that follows from it, are Wednesday's design call. They sit inside Kam's row A2 ("validate the Teams webhook address before the `requireM365` check") and are not wider than it. SETUP.md:58 ("Teams webhook configuration ... answer HTTP 503") is still true for valid requests. The systemTest skip and the Schemathesis expectation are named in the PR body as follow-ups.

**NOT tested, PR 2129:** real DNS; the real `jwtAuthenticate` in front of the route (READ ONLY); any running stack; Schemathesis; the systemTest Python; the pre-push hook; whether production has ENTRA_* set (this decides where finding 1 applies).

---

## PR 2130 (KS-624): GO WITH NOTES

**BLUF.** prism now refuses issuance with 501 in PR 685's shape, reports the constant mode 'mock', and its verify route can no longer pass a proof it never checked. The removed code had no other users.
- Red first gives 7/10 on develop and 10/10 at head. The 39 existing cells are unchanged, now 49/49.
- The seat's mutants and my three were all caught.
- The notes: one factually wrong sentence in the client-read PR body (Nit), and Info items.

**Q5, POST /api/credentials** (MEASURED AT RUNTIME, probe /private/tmp/g286/probe624_head.txt against probe624_dev.txt)
- At head, these bodies all get **501 NOT_IMPLEMENTED**: a valid shape, `{}`, an array, no body, and `text/plain`.
- Upstream middleware refuses some bodies before the handler is reached, exactly as on develop: a JSON string or `null` (400), malformed JSON (400), a NUL byte (400 VALIDATION_ERROR), 2 MB (413), and no or bad authentication (401).
- On develop the same five bodies get 400.
- **Shape.** I compared the head handler with develop's `wallet-connector/src/routes/walletVerify.ts` (PR 685, commit 2aebb0b30). Both use `success:false`, `error.code` NOT_IMPLEMENTED and a fixed message, log a warn line with presence booleans only, and do no lookup and no store. Cell C3 shows the subject count is 0 afterwards.
- **Removed code.** `issueCredentialSchema` and `dbSaveCredential` were module-local (`const` and a plain `function`, neither exported). `git grep -i` at develop finds other `issueCredentialSchema` hits only in kyc and vc-issuer, which are their own local definitions. `dbSaveCredential` appears only in prism's index.ts. `isoDateTimeSchema` is still exported from shared and used by 7 other files. `tsc` at head reads 0; my planted TS2322 makes it fail with rc 2. prism's tsconfig has `noUnusedLocals: true`, as the PR body says.

**Q6, D1.**
- At head, `PRISM_MODE = 'mock'` is a constant (index.ts:47), and the env is no longer read. The constant feeds /health :360, /api :374, the log :853 and the banner :859 (log and banner READ ONLY). C4 and C5 measure /health and /api.
- compose:1197 and bicep:1084 still set `basic`, as stated.
- Nothing asserts `basic`. I ran `git grep -i -E` for mode-near-basic; the compose and bicep hits act as its positive control. I also searched for `.mode` readers in the gateway, frontend, systemTest, tests and scripts, with the new test file as positive control: 14 hits, none about prism. The healthchecks (compose:1206 and the Dockerfile) are `wget --spider` only. system-status.ts:330-345 reads only version, status and degradedReasons (READ ONLY).

**Q7, D2.**
- At head the verify route's proof check is `{check:'proof', passed:false, message:'Proof signature not verified: not implemented (KS-624)'}`, with `verified` false, status 200 and the same fields (C7). The no-proof branch is unchanged (C10).
- **Callers.** proxy.ts has exactly one `proxy('prism'` mount, at :947, which forwards `/api/did`. Control: the same grep counts 6 `proxy('vcIssuer'` mounts, and `/api/credentials` goes to vcIssuer at proxy.ts:997-999. `PRISM_SERVICE_URL` is read only by the gateway's config/services.ts and system-status.ts, plus deploy files.
- Callers outside the repo were not measured.
- **Scope note.** D2 is not wider than Kam's card: pack row A6 cites `prism/src/index.ts lines 669 and 794`, and develop's line 794 is the `passed: true // Mock verification` line.

**Q8, red first.**
- With the new suite on develop, 7 of 10 fail (C1-C7), each with the seat's predicted actual: 201/true, 400, count 1, `basic` twice, the old listing text, and verified true. The 3 controls pass. At head, 10/10 pass.
- The full prism suite on develop with the new file reads 42 passed, 7 failed. Without the new file it reads 39/39 on both trees, and the names and results are identical (verbose diff). At head with the file: 6 files, **49/49**.
- Seat mutants reproduced: the mode line turns exactly C4 and C5 red; reverting D2 turns exactly C7 red. I did not reproduce the seat's issue-handler revert mutant; the develop red run covers C1-C3 against the old handler.
- **My own mutants:**
  - G1 validates `issuerDid` before the 501. Exactly C2 goes red.
  - G2 makes the proof check `passed` whenever `proofValue` is non-empty. C7 goes red.
  - G3 echoes the env at /api only. Exactly C5 goes red.

**Q9, ks1868 C1 timeout.** **Not reproduced.** I ran the full prism suite 7 times; its files run in parallel. One of those runs was the first run in a fresh clone, so the cache was cold. I saw 0 timeouts. In the verbose runs, C1 took 152-176 ms, at load1 about 4.8-5. Classed as Info.

### Findings, PR 2130
- **G286-2130-1, Nit (client-read text). PR body "Overlap" paragraph, and READY.** Both say develop's move to 6beac8734a2f was "3 files, all in the two shared docs pages". One of the 3 is a code file, `Blockchain/Dev/services/transfer/src/services/transferAccess.ts` (a comment-only change, +3/-1).
  - FOUND / TESTED / HOW: `git diff --name-only 204e62acdc35 6beac8734a2f`.
  - The conclusion (no overlap) stands.
- **G286-2130-2, Info. PR body "501 ... for every body".** Every body that reaches the handler gets 501. JSON scalars, malformed JSON, NUL bytes and oversized bodies are refused earlier by the shared middleware, as before (MEASURED, above). If the sentence is touched again, "every body the handler receives" is the exact form.
- **G286-2130-3, Info, doc drift.** These docs still present `PRISM_MODE` as an operating mode: `Blockchain/Dev/docs/ENVIRONMENT-VARIABLES.md:347`, `Projects Documents/Secuura-Crypto-Blockchain-Reference.md:100`, `Projects Documents/Secuura-Security-Reference.md:384` and `.planning/codebase/INTEGRATIONS.md:29`. None is a check. They are outside this PR's scope, a follow-up.
- **G286-2130-4, Info, test gap.** No cell pins the log line or the banner. Both read the same constant (READ ONLY).

**NOT tested, PR 2130:** Postgres-backed storage (the harness uses the in-memory fallback); callers outside the repo; Schemathesis, Akto, Playwright and k6; any live stack; eslint (not re-run); the seat's issue-handler revert mutant.

---

## Own conduct
- **Writes.** I wrote only under /private/tmp/g286 (my clone, its worktree `w`, scratch, probes, and parked files moved with `mv`) and this file. I ran no git write verb in any /Volumes/DevMASTER/!CODING checkout. That checkout was read only for its remote URL and key path. The Seat R 91st and Y 10th history files I read: the READYs, PR bodies, comments and evidence JSON.
- **Network.** I used the network only for git: ls-remote, clone, and fetch of develop, 2080, 2129, 2130 and the 56 open PR heads. I used no gh and opened no .env or credentials file. No box, kintsugi or demo.
- **Deviations.**
  - (a) One early command wrapped a `cd` in a subshell, `(cd …; true)`. It changed nothing, but it breaks the never-cd rule.
  - (b) load1 read 8.44 once, right after `npm ci`. It was under 8 at every other reading (4.3-6.8).
  - (c) My first clone, which used `--reference /private/tmp/g285/repo`, failed with "unable to read 69471ab4…". **g285's clone object store looks incomplete or corrupt; Info for Wednesday.** I then cloned plainly.
- **No rm.** The clone stays at /private/tmp/g286, 2.4 GB, not removed. The commission's no-rm rule overrides the common file's "remove it".
- **Disk.** df on DevMASTER read 104 GiB free at the start and 105 GiB at the end.
- **Gate rules.** Findings only. Nothing posted, mailed or pushed.
