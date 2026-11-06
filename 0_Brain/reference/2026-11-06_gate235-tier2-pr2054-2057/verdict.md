# Gate 235 verdict: Secuura / Blockchain, PRs 2054, 2055, 2056, 2057 (batched), tier 2, round 1 of 2 each

QA Gate 235, Sonnet, row G2. Written 2026-11-06 about 22:30 AEDT. Findings only; nothing fixed, nothing posted, no box, no docker.
Evidence class on every finding: MEASURED AT RUNTIME / PROBED / READ ONLY. A GO below is a statement about the SHA named, not the PR.

## Verdicts

- PR 2054 KS-1509: NO GO at tier 2. Re-commission at tier 1. Head 7bd7697c86ad29f2f5e3fc898e4bcc8935940704.
- PR 2055 KS-1666 N1: GO. Head 9417e964ce02895c6b08b075c26f6eb7b342b842.
- PR 2056 KS-1937: GO WITH NOTES. Head f5c8b2bd849a45a1dd5dce7d1267d1146ef9fc01.
- PR 2057 KS-1600 item 2: GO WITH NOTES. Head 25c122a3be56edb4f1b0de6de286fd209514ee05.

Heads at start (ls-remote 21:50:38 AEDT) equal pins.txt for all four; develop was 44ee04cb at start. Heads at end (22:25:39): all four unchanged. develop MOVED to b7d433fda83c (one commit, KS-957, 4 files); I re-ran merge-tree of all four against it (clean, 0 shared paths). Three timestamped readings, branch names beside: start/mid/end = develop 44ee04cb / 44ee04cb (clone fetch) / b7d433fd; each feature branch equal at all three.

## BLUF

2054 trips the STOP LINE. The only consumer I found outside this repo's own tree, Platform S's public verify page, treats a block height of 0 and null differently and the user sees it: 0 shows a "Block 0" row, null hides the row. A freshly created, still-pending document is exactly the case where the 202 path stored 0 and now stores null. I stopped the 2054 review there (see F1); the notes under it are what I had already measured. The other three PRs are test-only or log-only and behave as claimed. 2056 still leaks the recipient address in the failed-send line when an SMTP server echoes it (measured). 2057's "single-tenant, the live configuration" is not true of the Azure originate config, so the arm that matters is the arm it did not measure. Merge trees are clean for all four, no shared files among them, no merge order needed.

## Findings

### F1  PR 2054  MAJOR  STOP LINE  (src: Platform S, outside this repo)
- Where: `/Volumes/DevMASTER/!CODING/Secuura/platform-s-main/ssd/Services/CardanoAnchor/CardanoAnchorService.cs:795-797,829` (`long? BlockHeight`, JSON `blockHeight`, read off originate's verify answer `blockchain`) and `ssd/Views/Verify/_VerifyResult.cshtml:92-96` (`@if (Model.BlockHeight.HasValue)` renders `<dt>Block</dt><dd>@Model.BlockHeight</dd>`). `0.HasValue` is true, null is false.
- Path: originate `routes/verification.ts` returns the stored blob as `blockchain: chain` (lines 1258/1272, 963/989, 1049/1061); GET `/api/documents/:id` spreads the blob too (`routes/documents.ts:1234`). The create 202 blob (`documents.ts:1022`) and the retry 202 blob (`:1785`) are written from an anchoring 202 that never carries `blockHeight` (`services/anchoring/src/index.ts:590-605` lists id, documentId, contentHash, status, network, metadataLabel, createdAt, payloadTimestamp, message). So on a real, non-simulated create the stored value was always 0 and is now always null until the poller confirms.
- Effect: a pending document's public verify page used to show "Block 0" and will now show no Block row. Arguably more honest, but it is a caller-visible difference, in another service, from a reader that branches on 0 versus null. That is the STOP LINE condition as written.
- FOUND READ ONLY (source in the platform-s-main snapshot, which is not a git repo here, so its version against the deployed Platform S is unknown). Not exercised against a running Platform S.
- Wednesday's own search covered Blockchain/Dev only; Platform S was not in it. The 2054 flow fragment says "Platform S's reading of the field is not checkable from this repository"; it was checkable from the workspace.
- Fix-shape for the owner (prose): decide whether "Block 0 shown for pending" to "row hidden" is wanted by the Platform S owner; if yes, say so on the ticket and tier it 1; and a cell that pins the Platform S reader (or its fixture) belongs in that PR. READ ONLY recommendation.

Review of 2054 before and around the stop (kept as measured, not as a verdict basis):
- MEASURED AT RUNTIME: the 8 new cells, 8 of 8 pass on the head (jest, originate, Node v26.8.1). Three tampers of my own, each caught: create-202 reads `anchorData.blockNumber` instead of `blockHeight` (2 cells red), retry site `?? 0` (s4 red), anchor_failed blob omits the key (1 red). `documents.ts` restored byte-identical (sha256 checked).
- MEASURED AT RUNTIME: `toBlockHeight` on bad input (probe via node strip-types): undefined/null/''/whitespace/'abc'/NaN/Infinity/true/{}/[]/bigint to null; '0' to 0; -5 and '-5' kept; 1.5 kept; '0x10' to 16; '1e3' to 1000; '9007199254740993' to 9007199254740992 (precision). So negative, fractional and hex heights are stored, and a literal 0 or '0' is still stored as 0. Not a regression (`x || 0` kept all of those except it also stored digit strings as strings).
- READ ONLY: readers inside this repo that differ on 0 versus null: only `isAnchoredHonestly` (`routes/verification.ts:108-145`, `isAnchorHeight` refuses 0, accepts null). Not reachable from these four writes: the create blob is status `pending` with no txHash, the simulated blob returns false first, the failed blob returns false first, the retry blob has no status or `anchored` key. The fragment says the same and the source agrees. All other readers are falsy-alike: `anchorStateSync.ts:590-592` (`stored > 0`), verifier `ResultPage.tsx:497` and issuer `DocumentDetail.tsx:120` (`|| 0`), systemTest `anchor_honesty.py:143` (`bool(...)`). The spec has no `blockHeight` for document or verify blobs (`blockchain` is `properties: {}`, additionalProperties open); the only typed one (`VcVerificationResult`, line 12240) and the SDK `certifications.ts:47` are different routes.
- Is it a response change: yes, in value, not in shape. GET `/api/documents/:id` and every verify answer carry `blockHeight: null` where they carried `0`, for new documents until confirmation. The READY's "no response shape change" is true; "no predicate" is true in this repo.
- Ticket's "seven other places" against four changed: the fragment accounts for 1 (markDocumentAnchorFailed, "PR 1569", not verified by me; the current code at `anchorStateSync.ts:241-243` does carry the KS-1509 comment and `?? null`) + 4 here + 2 heal-path sites that no longer default a height. Census over originate and packages non-test src for a zero default on a height/number: one hit left, `routes/anchors.ts:79` (`row.block_number ? Number(...) : 0`), a response default on the anchors table, a different place the fragment's census does not mention. READ ONLY.
- Docs: both 2054 fragments quote "212 files / 2504 cells, develop 1b1b65c7415f" while the head's base is 4ccdc3b3e7cf and the READY says 215 / 2565. Stale figures in the fragments (MINOR).

### F2  PR 2056  MODERATE  the address is still logged on a failed SMTP send
- `services/originate/src/services/email.ts:210` `console.error(\`[Email/SMTP] Failed to send: ${error.message}\`)`. MEASURED AT RUNTIME (loopback stub SMTP server, real nodemailer 10.2.1 from a sibling seat's node_modules, scratch `smtp_probe.cjs`): the line printed was `[Email/SMTP] Failed to send: Can't send mail - all recipients were rejected: 550 5.1.1 <ks1937.probe.recipient@example.test>: Recipient address rejected: User unknown`, address present true. Also READ ONLY in nodemailer `smtp-connection/index.js:1221` (`'Invalid recipient ' + JSON.stringify(address)`).
- The tests forward `'ks1937 smtp boom'` and prove nothing about what a server echoes (their header says so). The READY says "unmeasured"; it is now measured, on the very line the PR edits. Same class, not measured: ACS `result.error` object (`:164`), `err?.message` (`:167`), `notificationClient.ts` `String(err)` (WARN lines) and `body.substring(0,200)` of the notification service's reply. Under Kam's card (ruled a, "never their values") forwarding thrown text is the unfixed half; Wednesday's KS-1937 answer is "the address"; this is the address.
- Fix-shape (prose): log the error's class/code (`error.code`, `error.responseCode`) instead of its message on those lines, or strip the recipient from the message before logging; test with a stub server that echoes the address, as above. READ ONLY recommendation, feasibility PROBED by the stub.
- Verdict effect: the PR does what it says (ten lines lose the field) and is no worse than before; the residual is a stated non-goal that is now measured. GO WITH NOTES, owner to file the residual (extend KS-2036 or a new ticket).

### F3  PR 2057  MAJOR (claim)  "single-tenant, the live configuration" is not what Azure runs
- Test header and flow fragment: "(single-tenant mode, the live configuration)". `Blockchain/Dev/deployment/azure/services.bicep:818` sets `MULTI_TENANCY_ENABLED=true` on the originate container app; `deployment/azure/env.demo.json:7` and `env.dev.json:7` set it true; only docker-compose defaults false. The code's own comment (`utils/requestTenant.ts:12-24`) says that in multi-tenant mode `extractTenantContext` assigns the raw `x-tenant-id` and the provenance strip is the only line. The PR measures the other arm and discloses the multi-tenant gap, but its headline "a forged header cannot steer the mint" is a single-tenant result presented next to a "live configuration" label. READ ONLY (bicep, json, source); the multi-tenant arm was NOT RUN (needs a database).
- Also READ ONLY: originate logs "[gateway-provenance] FAIL-CLOSED ... a multi-tenant deploy will lose its tenant until the secret is set", seen in my own run, consistent with multi-tenant being the deployed shape.
- Fix-shape (prose): drop "the live configuration"; say the result holds for single-tenant mode only; leave the ticket open for the multi-tenant arm with a real-database cell.

### F4  PR 2056  MINOR  the claimed census is not complete for the same class
- Fragment: "a scan of every log call ... flags those two [certifications.ts:1385, adminConfig.ts:2123] and nothing else". READ ONLY grep over originate src (non-test): `routes/thirdPartyVerifiers.ts:87` `logger.info('Third-party verifier registered', { id, organizationName, contactEmail })` also logs an email address. Different purpose (a contact, not a recipient), but an address in an INFO line; not in KS-2036's list.

### F5  PR 2056  MINOR  cells blind to a partial leak
- MEASURED AT RUNTIME tamper X: allow-list refusal line changed to `...refusing to send: ${options.to.split("@")[1]}` (the recipient's domain). 12 of 12 cells stay green. The cells only look for the full address. The ACS path's "address still reaches the mailer" is also unpinned (E1-E3 never check `beginSend` arguments); only the SMTP path has `mockSendMail.mock.calls[0][0].to` (E6). Tampers Y (full address on SMTP Sent), Z (address back on the client fallback INFO line) and W (blank the SMTP `to`) were each caught by exactly one cell.

### F6  PR 2056  NOTE  losing who was refused / to whom a send failed
- The refusal line (`email.ts:181`) and the failure lines no longer identify the recipient. Under Kam's card (`secuura-ks1346-logging-thrown-objects-leaks-secrets`, read with `decision_queue.sh show`: status ruled, choice a, ruled 2026-09-27T16:32:47+10:00, "Log what kind of thing was thrown and the NAMES of its fields, never their values") the card is about thrown objects; the address ruling is Wednesday's on KS-1937. Acceptable under that ruling, with the cost stated in the PR. Operational cost: nothing in the originate log now joins a refusal or failure to a recipient or document; the caller must log its own id. A log-text monitor for "refusing to send" or "Sent to" does not exist in the repo (git grep over the head: only the fragment).

### F7  PR 2055  NOTE  OWN1 is my reconstruction
- I did not find gate 203's report. I built OWN1 from the test's and fragment's own definition (`anchoringStatus === 'failed'` to `!upstreamAnchorId` at `routes/certifications.ts:711`). On that mutant A5b is the only failing cell of 11 (MEASURED AT RUNTIME), baseline 11 of 11. Second tamper of my own (`anchoringStatus === "failed" || upstreamAnchorId === null`): again only A5b red. Fragment's "survived all 21 cells at gate 203" not re-run.

### F8  PR 2057  NOTE  what the cells can and cannot see
- MEASURED AT RUNTIME: 5 of 5 pass. V 24th's tampers reproduce: strip removed alone, 5/5 green; vouched-only read removed alone, 5/5 green; both removed, M2 and M3 red (M1 and controls green). My own: tenant resolver additionally falling back to the token's tenant claim (`req.user.tenantId`), all 5 green, so the cells would not notice the stored tenant moving from the default to the caller's own tenant (the ticket's literal expectation) via that route; M1 pins the default-tenant behaviour but only for requests where that field is not on `req` at resolution time. Inconclusive about intent; reported as a blind spot, not a defect.
- First attempt at the tamper broke compilation (unused import under ts-jest) and made all 5 cells red; that was my instrument, not a test property. Fixed by keeping the symbol referenced.
- Real stack: yes. The test imports the real `index.ts` (real mount order, provenance middleware, KS-458 resolution, `authenticate()`, `requireRole`, admin router) with only `express.application.listen` and `prisma.$queryRaw` replaced; a control cell asserts the listen spy fired. The INSERT slot read is pinned by M1.
- Item 3 wording: card `secuura-ks1600-originate-malformed-permissions-1106` read with `show`: ruled, choice a, "Refuse with 400, matching the security service", ruled_ts 2026-11-06T14:58:43+11:00, tier-1, test first, callers measured first. The 2057 fragments say item 3 "is a decision and is untouched"; the second half is true, the first is stale (it is ruled and unbuilt). The READY says the PR body's Finisher note corrects "default no behaviour change"; I did NOT read the PR bodies (no API access under this commission), so I cannot say whether the body is now true. NOT TESTED.

## Q-by-Q short answers

1. 2054 readers: enumerated above (F1). Value 0 to null is a response change in value on GET document and verify; STOP LINE tripped via Platform S. `toBlockHeight` bad input measured. Planted 3 tampers, all caught.
2. 2056: address gone from all ten lines (diff read, 3 + 7; test run 12/12; four neighbouring suites 183/183 still pass); address still reaches the mailer (SMTP asserted, ACS read only); provider error text CAN carry it (F2, measured); losing who was refused is acceptable under the ruling as worded (F6).
3. 2055: OWN1 (reconstructed) fails only A5b; tamper sample caught; `routes/certifications.ts` is byte-identical: git blob 4257bdf3ba6e at the PR's parent, at its head and at develop 44ee04cb (MEASURED, rev-parse).
4. 2057: what makes cells fail is F8; real stack yes; item 3 wording see F8.
5. Docs fragments against code: 2055 counts check (3 files, 5+11+2 = 18 cells; 202 at `anchoring/src/index.ts:590`, `id` at 593; two ks1666 files 11+2 = 13); 2056 counts check (10 sites, 12 cells); 2057 as F3/F8; 2054 stale figures. Hook legs 3, 4, 8 (from `scripts/preflight/preflight.sh` step names): 3 spec-auth conformance (unauthenticated requests to bearer-authed ops), 4 path resolvability (every spec'd path routes), 8 served-spec consistency (`/api/docs/openapi.json` vs `.yaml`). None of the four PRs touches the spec, a route mount or auth, so those legs would have checked nothing that these diffs can move; a skip costs nothing here except that none of them could have caught F1 (it lives in another repo). Merge trees: below. PR bodies unread (above).

## Merge trees

Against develop 44ee04cba478 (git 2.54.0, `git merge-tree --write-tree`): all four rc 0 and a tree, no conflict list.
- 2054 tree be3de41aa5a1, base 4ccdc3b3e7cf, 32 behind, shared paths with the moved range 0.
- 2055 tree 74a247cdee88, base 4ccdc3b3e7cf, 32 behind, 0.
- 2056 tree b2c2f8560481, base 7ad5a8b4bdf7, 31 behind, 0.
- 2057 tree 133a9e22f265, base aa4200e8a34c, 27 behind, 0.
Against develop b7d433fda83c (end of session): all four clean (trees 53e1a556, 94abc19f, e4237938, 2d571f55), 0 shared paths with the 4 newly moved files.
Pairwise (all six pairs): rc 0. Files changed by the four PRs: 17 distinct paths, none changed by more than one PR (`uniq -d` empty). Combined tree of all four on develop: `tsc --noEmit -p .` in originate rc 0 (MEASURED); the ten test files touching these changes (ks1293, ks1509, ks1937 x2, ks1600-a-forged, ks1666 x3) 8 suites / 53 cells pass (MEASURED). No merge order needed. If 2054 is re-commissioned, KS-1695 touches `documents.ts` and must rebase on it (READY).

## Not tested

- The whole originate suite (216 files) was not run; disk and time. Only the suites named above.
- Platform S running; any Postgres; multi-tenant mode (2057); real ACS; PR bodies and PR/ticket comments (no API); the four platform suites; any LTS Node (Node v26.8.1 only); preflight legs 3, 4, 8 (no stack, none allowed).
- Gate 203's report and the exact OWN1 patch (F7). PR 1569 merged state (F1 notes).
- Whether the deployed Platform S matches the local snapshot (not a git repo).

## My own conduct

- Network: git ls-remote and git fetch into my own clone only (`--filter=blob:none --depth=80`, scratchpad `clone/`). One loopback-only stub SMTP server for F2, no outbound traffic.
- To avoid per-blob round trips I pointed my clone's `objects/info/alternates` at the Blockchain project's object store (read only) and symlinked `node_modules` from sibling seat worktree `s-k18-hchk` (read only; its zod 4.6.7 matched, the 2_Project_Files one was zod 3 and failed). I built `packages/shared/dist` inside my own scratch tree.
- I ran `rm -f` once, in my first `nm.sh`, on a symlink I had created in my own scratch tree; afterwards I moved things into `scratchpad/_quarantine_2026-11-06/` instead. I killed three of my own background processes (a lazy-fetch `ls-tree -l`, a `checkout`, a grep). A first tamper run broke compilation and was my instrument error (F8).
- Disk: scratchpad 243 MB (clone .git about 3 MB plus a 232 MB source tree plus dist); no second clone; DevMASTER free 26 GiB before and after. Nothing written outside this folder and the session scratchpad. No commit on any head. Scratch files for the tampers and probes are in `/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/3578fa00-67a9-41ee-bfc5-e42f919f70e9/scratchpad/` (not copied into evidence/; the `evidence/` folder here was left empty).
