SUBJECT: [Secuura/Blockchain -> Wednesday] MERGED: #1011 KS-871 @523f283c6cd2550263ec9869dc5ee722be40df4e
FROM: secuura-blockchain <secuura-blockchain@agentmail.to>
TIMESTAMP: 2026-09-16T20:14:54.000Z
AUTH: {"spf": "pass", "dkim": "pass", "dmarc": "pass"}

Seat A

## BLUF
- #1011 KS-871 MERGED at 20:10:46Z as squash 523f283c6cd2550263ec9869dc5ee722be40df4e, pinned with --match-head-commit to the GO head 6dc8256448b50de6a15519001a4f7032ace1ae19.
- Verified at origin:
  - develop tip = M;
  - one parent = e0f41a8fafd64fa31524390cfeab320e822f3d15;
  - tree 839294c16de1ec6392964daddd5d967132465abc = my merge-tree prediction = the gate's;
  - files base..M = the PR's 4 files;
  - all four blobs equal your targets.
- KS-871 stays In Progress. Facts comment 9f762589-b194-4b10-9cbc-c9f7950fe956 carries the §5f line and the 574-row blast-radius statement.
- KS-1189 comment 1c68f433-303e-488b-acf1-01cbe1bf2009: R-3 MOVED, R-5 CLOSED.
- New tickets, both Backlog, board account, not built:
  - **KS-1191** (R-4, Medium, related KS-871 and KS-1189);
  - **KS-1192** (F-1011-6, Low, related KS-871).
- **One deliberate omission, for you to rule:** KS-1191 does NOT carry R-4's "reaching gdpr spellings" (`x/../`, `./`, `;x=1`, `%65`). Those are the same requests the gate lists under D6 as passing the erasure door. Your Detail line sends that measurement to Kam through you, not to a ticket. KS-1191 says only that routed spelling examples exist and that you hold them.

## Recommendation
- If you want the routed gdpr spellings on KS-1191, say so and I will add them as a comment. Otherwise no reply is needed.
- Next, per your RECEIVED 20:10:12Z: A15 KS-1018 (branch already cut at e0f41a8fa, READY test section applied, nothing committed). #1014 is held at 616c766a5 for its gate.

## Detail
**Pre-steps, 20:10:21Z to 20:10:44Z:**
- Mail guard: 0 STOP/HOLD leading tokens. The newer mails were your RECEIVED #1014 and the GO.
- attachmentsForURL(pull/1011) = exactly KS-871 contributes.
- 0 closing phrases in the PR title, body, comments, all three commit messages, the squash body and the squash subject (regex control 2 of 2).
- Head re-read in the same action: API and ls-remote both 6dc825644. develop e0f41a8fa, equal to the expected base.
- Wrong-sha control stopped with rc 13 before any merge call; the dry run passed.

**Squash subject.** I wrote my own subject rather than using the PR title, whose "records the original path" no longer describes round 2:
"KS-871: the audit row records the canonical path captured at entry, so a refused erasure is audited as /api/gdpr/erasures and gdpr.create (#1011)".
- The PR title itself is unchanged, as you asked.
- The squash body does not name KS-1187 or the bypass.
- It states the 256 test / 574 production row change and that out-of-repo consumers are unmeasured.

**Blob equalities** (M vs your targets):
- middleware/audit.ts 052131de0
- ks871-audit-path-captured-at-entry.test.ts 8d66dfaf7
- ks871-the-audit-log-records-req-path.test.ts f6bf4f9d4
- ks871-real-app-canonical-audit-rows.test.ts ef19446f2

**Board writes,** each gated on the previous step's rc and read back:
a. KS-871 facts comment 9f762589… at 20:11:20Z, anchors 9/9.
   - The §5f line verbatim from your GO.
   - The blast-radius paragraph: 256 test / 574 production census rows moved toward canonical, 0 regressions, e.g. v1.login → auth.login; out-of-repo action grouping UNMEASURED.
   - Records: R-1 closed for the fixture (root mount only), R-2, R-7 (KS-858 named, no relation), R-8 closed, R-9 (51/419 merged).
   - KS-871 reads In Progress after it; pull/1011 = KS-871 contributes/merged.
b. KS-1189 comment 1c68f433… at 20:11:42Z, anchors 7/7.
   - R-5 CLOSED: 574 production rows, canonical 527 → 1101 of 1101.
   - R-3 MOVED: the login-429 row is auth.login in both modes; H29 attemptedEmail is still never written.
c. KS-1191 (R-4): case splits the action namespace (`GDPR.create`, `LOGS.create`); `/API/` is unaudited; unrouted 404 caller text in action (`qa-attacker-chosen.create`, `%6cogs.create`, `logs;x=1.create`, `..create`, `V1.create`).
   - Searched first: GDPR.create 92/1, LOGS.create 116/2, unaudited 8/4, case-split 125/0, deriveAction 2/2. KS-1189 has no R-4, so one new ticket.
d. KS-1192 (F-1011-6): the production cell survives `vi.resetModules()` removal at 3/3; "0 hits" cannot tell the door from CSRF. Fix shape as the gate gave it: assert X-CSRF-Token on the 307 plus `INSUFFICIENT_SCOPE`.
   - Searched first: ks871-real-app 123/1, resetModules 1/1, INSUFFICIENT_SCOPE 107/1, X-CSRF-Token 95/5. None covers it.

**The §5f live-sweep list for Sunday** is now: KS-1165, KS-932, KS-1073, KS-844, KS-1183, KS-745, KS-999, KS-871.

**State at 20:12Z:** develop 523f283c6; #1014 head 616c766a5 (unmoved); KS-1176 In Progress; KS-1018 Backlog (board account).
Nothing deployed. Nothing to Peter or Stuart. KS-1187 untouched.
