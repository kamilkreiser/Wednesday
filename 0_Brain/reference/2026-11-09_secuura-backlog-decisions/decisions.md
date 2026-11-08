---
date: 2026-11-09
type: decision-pack
source: Seat S 41st decision_candidates.md (31 rows), each ticket re-read at source (Linear, description + all comments) by an Opus subagent of Wednesday; code at develop 64671e97ce62 (git ls-remote origin develop, 2026-11-09) via the GitHub contents API, read-only
status: for Kam
---

# Secuura Backlog: 31 decisions

## BLUF

- **31 rows, sorted into 30 items** (KS-960 and KS-1200 are the same question, so they are one item).
- **(A) Kam alone: 20 rows (19 items).** **Reply "all recommendations" and all 20 are ruled.** That moves 20 Backlog tickets in one reply. One exception: changing the 3 demo rows in KS-607 needs a separate yes from you, because it writes to demo.
- **(B) Kam with Stuart at your monthly meeting: 6 rows.** Each one is ready as an agenda item. If you don't answer, they stay on hold until that meeting. "All recommendations" covers these too if you want to rule them now.
- **(C) Wednesday rules: 5 rows.** These are listed for your veto only.
- **Security rows: 10, marked [SECURITY].** They are KS-619, KS-621, KS-624, KS-625, KS-648, KS-1208, KS-1473, KS-1992, KS-590 and KS-630.
- **Read at source:** all 31 tickets, 31 of 31. Every code line I re-read at today's develop still says what the ticket says. The exception is KS-1400, where the problem is already fixed in code.
- **Nothing was written.** No ticket, comment, mail or push. Anything that has to reach Peter, Stuart, Phil or the lawyers is yours to send.

---

## (A) Kam alone: 20 rows

**1. KS-960 + KS-1200: which database blueprint is the real one**
- **Question:** our code has two blueprints for the database that disagree. Should the official one be what the running systems are actually built from?
- **Options:**
  1. **What runs is official.** A build seat first reads each environment's schema (read-only), then aligns the other files to it and adds a check so they can't drift apart again. That also fixes the demo-user seed, which fails 14 of 14 times (KS-1990).
  2. **The old migration files are official.** That would add a unique rule on the email column, but email is stored encrypted, so the rule would block nothing.
  3. **Keep "do not reconcile".**
- **Recommendation:** option 1.
  - Every check so far points at the docker-init blueprint. Demo has 0 links on `issuer_organization_id` (2026-09-07), and the local stack is built from docker-init (2026-11-04).
  - At develop today, `docker/init/01-schema.sql` has no unique rule on email, `migrations/001` line 20 has `UNIQUE`, and `adminConfig.ts` line 2121 still uses `ON CONFLICT (email)`.
  - Whether the anchor_store unique rule (from migration 031) exists on the deployed databases is UNMEASURED.
- **Default:** option 3. Nothing changes and the seed keeps failing.

**2. KS-784: check the Teams webhook address before or after the Microsoft 365 check [SECURITY: outbound-request guard]**
- **Question:** when someone saves a Teams webhook, should we check the address is safe *before* checking whether Microsoft 365 is set up?
- **Options:**
  1. **Check first.** A small code change by a build seat. The address-safety test can then run on any stack.
  2. **A local test mode.** Bigger, and it changes how the service behaves.
  3. **Neither.** The test stays skipped.
- **Recommendation:** option 1. It is the smaller change, and it makes a security guard testable. At develop, `m365-integration/src/index.ts` line 1276 still runs `requireM365` first. Telling Peter is yours.
- **Default:** option 3.

**3. KS-1208: a login token with no user id or role [SECURITY: auth]**
- **Question:** if a login token has no user id or no role, should the gateway refuse it with "unauthorised" instead of crashing with an internal error?
- **Options:**
  1. **Refuse with 401,** plus one guard covering every header copied from the token. That guard also fixes the case where an illegal character crashes the gateway.
  2. **Forward the request without those headers.**
  3. **Leave it.**
- **Recommendation:** option 1. It fails safe and closes two holes in one change. At develop, `api-gateway/src/middleware/auth.ts` lines 685 and 687 set `x-user-id` and `x-user-role` with no guard. Today nothing issues such a token, so the risk is not live.
- **Default:** option 3.

**4. KS-619: a login token with no tenant [SECURITY: tenant]**
- **Question:** if a login token names no tenant, should the gateway refuse it instead of quietly placing the caller in the default tenant?
- **Options:**
  1. **Refuse,** except for platform-admin roles, whose tenant switching keeps working and gets a test.
  2. **Accept the default and close.**
- **Recommendation:** option 1. The default tenant holds most of the data.
  - At develop, line 683 reads `if (!decoded.tenantId) decoded.tenantId = DEFAULT_TENANT_ID`.
  - The caller's own tenant header no longer gets through, but the code still doesn't refuse the token, which is what the ticket asks for.
  - No live path was found on 2026-08-13 (0 null tenants on keys or users). That count is not re-measured.
- **Default:** leave as is.

**5. KS-621: documents with no owner leak across organisations [SECURITY: tenant/organisation]**
- **Question:** documents created by a connector have no owner, and another organisation in the same tenant can read them. Do we close that hole now?
- **Options:**
  1. **Add an organisation filter to every document read.** A large change to a tenant that holds 94k documents.
  2. **Keep the owner-based rule and close the no-owner gap.** This is KS-1695, already In Progress, and it has five costed fixes.
- **Recommendation:** option 2 now. The leak was measured live by Peter (200 instead of 404, 2026-10-06) and on develop (gate BX1, 2026-10-20). Whether an organisation should be a hard wall at all is a long-term question: carry it to the Stuart meeting next to his ownership-model work (PS-690, In Progress).
- **Default:** KS-1695 carries on as it is. No new ruling.

**6. KS-624: prism stamps fake signatures [SECURITY: crypto]**
- **Question:** the prism service puts random bytes where a signature should be and then reports them as valid. Should it refuse instead, or be built for real?
- **Options:**
  1. **Make it honest now.** It refuses to issue (a 501, the same fix as the wallet-verify one in PR #685) and stops reporting its mode as "basic". Small.
  2. **Build real signing.** Only worth it if prism has a future.
  3. **Label it a mock and leave it.**
- **Recommendation:** option 1. There is a precedent, it is cheap, and one revert undoes it. At develop, `prism/src/index.ts` line 669 is `crypto.randomBytes(64)` ("Mock signature") and line 794 is `passed: true` ("Mock verification"). The gateway does not route to prism's issuing path (ticket, 2026-08-13; not re-read).
- **Default:** leave it. Nothing reaches it today.

**7. KS-625: presentation check never verifies the signature [SECURITY: crypto]**
- **Question:** the presentation check answers "verified" without checking the holder's signature. Should it say it didn't check, or check properly?
- **Options:**
  1. **Build the real signature check.** Tier-1 build seat.
  2. **Make it honest now.** Answer "not verified" until the check exists.
  3. **Document it as by design.**
- **Recommendation:** option 2 now, with option 1 as the follow-up build.
  - Unlike prism, this endpoint is reachable behind login.
  - At develop, `vc-issuer/src/routes/presentations.ts` lines 358–365 compare only challenge and domain. Line 365 is the comment "In production, verify the cryptographic signature".
  - A forged proof was never actually sent to it (UNMEASURED).
- **Default:** leave it.

**8. KS-648: issuer site's looser browser security setting [SECURITY: CSP]**
- **Question:** keep the issuer site's looser browser setting (`unsafe-eval`), which the Cardano wallet library needs, as a written-down risk?
- **Options:**
  1. **Accept it and close.**
  2. **Schedule the library upgrade that removes it.** Size UNMEASURED.
- **Recommendation:** option 1. Signing needs it, the reason is written beside it, and no exploit is claimed. Revisit when the Cardano library is upgraded. At develop, `frontend/issuer/nginx.conf` line 74 has it, with the reason (KS-35) at lines 63–73.
- **Default:** leave the ticket open.

**9. KS-1473: developer page lists an endpoint that doesn't exist [SECURITY: CSRF exemption]**
- **Question:** the developer page advertises a "verify many documents" endpoint that doesn't exist. Build it, or delete the mention?
- **Options:**
  1. **Build it.**
  2. **Delete the page row and both CSRF exemptions for it.** Small.
- **Recommendation:** option 2. An exemption for a route that doesn't exist would silently cover any route later added under that name. At develop, the portal lists it at line 294 and `csrf.ts` exempts it at lines 115 and 119.
- **Default:** leave it.

**10. KS-1632: an admin setting that does nothing**
- **Question:** the admin setting "verifier verification level" no longer does anything. Remove it, label it, or make it work again?
- **Options:**
  1. **Remove it.**
  2. **Label it "not enforced".**
  3. **Enforce it again on a non-public route.**
- **Recommendation:** option 1. Public verify is public by ruling (KS-442), so the gate can't come back on that route, and the setting misleads admins. Its one check point had 0 calls in 30–38 days (ticket, 2026-10-19; not re-measured).
- **Default:** leave it.

**11. KS-1992: a failed credential cancellation is not retried [SECURITY: credential revocation]**
- **Question:** if cancelling (revoking) a credential fails to save, should the system keep retrying on its own, or keep telling the caller "save failed, try again"?
- **Options:**
  1. **Accept the cancellation and retry the save in the background.** Medium build.
  2. **Keep today's behaviour:** refuse, and the caller retries.
- **Recommendation:** option 2. It is honest and explicit, and the test gate graded it LOW. Reopen only if a deployed environment ever shows a failed save (UNMEASURED). At develop, `credentialRepo.ts` writes the in-memory copy at line 552, throws at lines 574 and 578, and contains 0 retry/queue/backoff.
- **Default:** option 2.

**12. KS-757: two retries can process one GDPR erasure twice**
- **Question:** two retries arriving at the same time can process the same GDPR erasure twice. Which of the three repairs goes first?
- **Options:**
  1. **One atomic "claim" step** using the statuses that already exist, plus a timeout for claims left behind by a crash.
  2. **Pass one database transaction through the create step and add a lock.**
  3. **Settle the 4 duplicate erasure records first, then add a unique rule.**
- **Recommendation:** option 1. It needs no ruling on GDPR records and can't deadlock the connection pool. At develop, `gdprService.ts` line 1511 still reads with no lock (0 `FOR UPDATE` or advisory-lock hits). The duplicate count is from 2026-09-02 and not re-measured.
- **Default:** leave it.

**13. KS-263: GitHub's paid security features**
- **Question:** turn on GitHub's paid code-security features for the main repo?
- **Options:**
  1. **Turn them on.** You do it in GitHub settings; it is paid per committer.
  2. **Leave them off and close the ticket with the reason.**
  3. **Leave them off and keep the ticket open.**
- **Recommendation:** option 2. Measured today, the repo still answers 403 "Code Security must be enabled". GitHub Actions is retired (2,000 runs, all failing to start, since 2026-08-20; KS-638), so the CI scans this was meant to show no longer run.
- **Default:** option 3.

**14. KS-305: the customer contract (DPA) sentence on Microsoft 365**
- **Question:** who adds the sentence "the customer controls, and erases, its own Microsoft 365 documents" to the customer contract?
- **Options:**
  1. **You send it to the lawyers.**
  2. **Park it until the next contract revision.**
- **Recommendation:** option 1, bundled with the terminology pack (B4). Platform S did not cover it: PS-1080 names KS-305 as "the K-side counterpart for the contract wording", and the three linked S tickets are storage builds with no contract wording.
- **Default:** option 2.

**15. KS-339: extranet access for Phil and Steve**
- **Question:** do we still give Phil and Steve access to the extranet?
- **Options:**
  1. **Do it.** An extranet code change first, then you set their passcodes and brief them.
  2. **Drop it and close.**
- **Recommendation:** option 2. You said on 09-05 the team barely uses the extranet. Adding people also widens edit rights, because the login has no roles (ticket, 2026-08-14; extranet code not re-read today).
- **Default:** leave it open.

**16. KS-590: what an anonymous verify may reveal [SECURITY: tenant disclosure]**
- **Question:** when anyone checks a document anonymously, may the answer reveal another customer's details? Four cases are waiting on you:
  - the organisation's id,
  - two chain-first answers that skip the scrub,
  - old rows with no tenant,
  - lookups by document id.
- **Options:**
  1. **Rule "withhold all four".** A build seat makes the code match, and the test then checks it.
  2. **Park it again.**
- **Recommendation:** option 1. It matches the answer v2 already gives ("fields withheld") and the stance that verify can answer without naming anyone. The four gaps come from a code reading on 2026-08-11 and were still open on 2026-10-06. Not re-read at today's develop (UNMEASURED).
- **Default:** option 2.

**17. KS-604: the system-details document you owe Peter and Stuart**
- **Question:** does the finished docs update (KS-1807) count as the system-details document you owe Peter and Stuart?
- **Options:**
  1. **Yes.** You point them at it and the ticket closes.
  2. **No.** An agent drafts a separate handover for you to review.
- **Recommendation:** option 1. Seven docs PRs merged and reached kintsugi on 2026-11-01. Gaps: the anchoring pages, the API contract, and 26 lines marked UNDECIDED.
- **Default:** leave it open.

**18. KS-607: 3 demo anchors marked "failed" that actually landed on chain**
- **Question:** 3 demo anchors read "failed" even though they landed on chain. Fix the record at the source, or rely on Platform S's workaround?
- **Options:**
  1. **Fix at source.** Add a rule that a row with a real transaction and block can't read "failed". Built after the KS-1384 reconciler work.
  2. **Accept S's workaround and close.**
- **Recommendation:** option 1 for the code. Fixing the 3 demo rows is a write to demo and needs a separate yes from you. Your 2026-08-12 measurement found 3 rows with a real transaction, block and confirmation time still reading "failed". The rows today are UNMEASURED.
- **Default:** leave it open. S's workaround keeps users seeing the right answer.

**19. KS-1781: two warnings on Node 26**
- **Question:** do two warnings that only appear on Node 26 matter now?
- **Options:**
  1. **Leave them until the Node upgrade is planned.**
  2. **Find their source now.**
- **Recommendation:** option 1. All 1,212 tests pass, and the images run Node 24, not 26 (KS-530; not re-measured).
- **Default:** option 1.

---

## (B) Kam with Stuart, monthly meeting: 6 rows

**B1. KS-304: privacy token for personal data**
- **Question:** has Platform S started the privacy-token work, and does Platform K keep waiting for it?
- **Options:**
  1. **K waits.**
  2. **K builds its half first.**
- **Recommendation:** option 1. On 2026-09-02 you ruled "S goes first". Whether S has started is UNMEASURED. It is a status check for the meeting.
- **Default:** option 1.

**B2. KS-602: the certification model**
- **Question:** when does the build of the certification model (attestation + signing + optional watermark) start?
- **Options:**
  1. **Set a start date at the meeting,** then a seat splits the epic.
  2. **Hold.**
- **Recommendation:** option 1, as a date only. It is long-term product design (2026-08-11 weekly).
- **Default:** option 2.

**B3. KS-603: verification as a configurable smart-contract workflow**
- **Question:** build verification as a configurable smart-contract workflow now, or hold it?
- **Options:**
  1. **Schedule it.**
  2. **Hold.**
- **Recommendation:** option 2 until B2 has a date, because it builds on the certification model.
- **Default:** option 2.

**B4. KS-605: definitions for the lawyers**
- **Question:** are the lawyer-facing definitions of certification, verification, signing and watermarking done? The open part is Phil's research on "signing".
- **Options:**
  1. **Close it.**
  2. **Still open.**
- **Recommendation:** you confirm Phil's status. A seat then drafts the four definitions from BM-1 and BM-2 for you to send with KS-305 (A14). Phil's status is UNMEASURED.
- **Default:** option 2.

**B5. KS-630: a security probe as a 7th pre-push check [SECURITY: XSS]**
- **Question:** add the status-page security probe as a 7th automatic check before every push? This changes Peter's and Stuart's push path.
- **Options:**
  1. **Add it.**
  2. **Don't.**
- **Recommendation:** option 1. It needs no network and gives the same answer every run, and the ticket recommends it. Agree it at the meeting first. At develop, `preflight.sh` has 0 mentions of the probe (case-insensitive; control: 34 "check" hits).
- **Default:** option 2.

**B6. KS-651: the shared code library's dependency is invisible to audits**
- **Question:** 22 services use the shared code library without listing it, so the security audit can't see it. What do we do?
- **Options:**
  - A. Formalise the workspace.
  - B. Publish the library to a private registry.
  - C. Keep the current link but document it and teach the audit about it.
  - D. Leave it, on purpose.
- **Recommendation:** C now, with A as the target. C is the cheapest way to close the audit blind spot. The counts come from 2026-08-17; today's count is UNMEASURED.
- **Default:** D.

---

## (C) Wednesday rules: 5 rows (Kam: veto only)

**C1. KS-565: the sweep tracker**
- **Question:** split the 2026-08-05 sweep tracker item by item and close the fixed items?
- **Recommendation:** **keep it as the tracker.** Peter still adds to it (22 comments, the latest 2026-10-21), and the test baseline cites it. A related ticket being Done doesn't make an item on the tracker fixed.

**C2. KS-636: the monthly base-image vulnerability scan**
- **Question:** GitHub Actions is retired, so what runs the monthly scan of the base images for known vulnerabilities?
- **Recommendation:** **a local scheduled scan** (Trivy) on a Secuura seat's schedule, reporting to the board. Each deploy also records which base image it built on. This adds a doctor check and a portability item.
- **Measured:** the alarm fired 2026-08-01 and went unread, and Actions has been dead since 2026-08-20 (KS-638).

**C3. KS-866: the 2026-09-06 merge method**
- **Question:** is the 2026-09-06 merge method (merge locally, then push the merge commit) still the protocol?
- **Recommendation:** **no, superseded.** Close it with a facts comment that keeps the 9-second race as the reason the API merge is not used.
- **Measured:** the project rule is now "Never push straight to `develop`" (`Blockchain/CLAUDE.md` line 241). `DEV-PROCESS.md` and `CONTRIBUTING.md` have 0 lines describing the old method (case-insensitive; control: 32 and 41 "merge" hits).

**C4. KS-1870: reconciler rule R7**
- **Question:** run a census of the affected rows, then decide whether to build rule R7?
- **Recommendation:** **run the read-only census at the next deploy seat.** Building R7 comes back to Kam afterwards, because it writes "failed" rows that Platform S reads.
- **Measured:** at develop, `reconciler.ts` line 67 says "R7 is NOT built". KS-1384 and KS-1751 stay hands-off.

**C5. KS-1400: the Urgent dependency-advisory ticket**
- **Question:** the problem behind this Urgent ticket is gone from the code. Re-prioritise it, and close it once the running kyc service is checked?
- **Recommendation:** **drop it from Urgent to Low now.** The next deploy seat reads kyc's axios version in the running container, then closes it under Rule A.
- **Measured:** at develop, `services/kyc/package-lock.json` line 1293 has axios 1.20.0.

---

## What I could not read at source
- **Tickets:** none. All 31 were read (description + all comments; KS-565 has 22, none was paged past 50).
- **Not re-measured today, marked UNMEASURED above:**
  - the extranet login code (KS-339)
  - the four disclosure code sites (KS-590)
  - the demo anchor rows (KS-607)
  - prism's gateway routing (KS-624)
  - the 22/24 shared-library counts (KS-651)
  - Phil's research (KS-605)
  - whether S has started the privacy token (KS-304)
  - the null-tenant counts (KS-619)
  - the duplicate erasure records (KS-757)
  - the running kyc image (KS-1400)
  - the enforcement call counts (KS-1632)
