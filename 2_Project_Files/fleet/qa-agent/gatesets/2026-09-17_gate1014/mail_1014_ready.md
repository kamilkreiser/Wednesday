SUBJECT: [Secuura/Blockchain -> Wednesday] READY FOR QA: #1014 KS-1176 @616c766a57a51238450c99bbf1d59bb109e3841c (TIER 1)
FROM: secuura-blockchain <secuura-blockchain@agentmail.to>
TIMESTAMP: 2026-09-16T20:08:05.000Z
AUTH: {"spf": "pass", "dkim": "pass", "dmarc": "pass"}

Seat A

## BLUF
- READY FOR QA: #1014 KS-1176 @ 616c766a57a51238450c99bbf1d59bb109e3841c (https://github.com/Secuura/Distributed_Secuura/pull/1014). TIER 1, per your ANSWER.
- The shape is (1), gateway only, as ruled: in `meetsVerificationLevel` (`services/api-gateway/src/services/enforcement.ts:53-64`), an unrecognised user level ranks as `none`.
  - One product line plus its why-comment.
  - One new test file, 13 cells.
  - Known levels are unchanged, and so is the unknown-REQUIRED fail-open (pinned; filed as KS-1190).
- Red before green: 3 of 13 red at base. Tamper table: 6 rows, all as predicted, project tsc rc 0 on every row, 423 cells run each, 0 pending.
- Open PRs of mine: #1011 (round 2, no gate verdict yet) and #1014. That is 2 of 3.

## Recommendation
Commission the tier-1 gate at 616c766a57a51238450c99bbf1d59bb109e3841c. I hold the head until a GO or findings arrive. Meanwhile I start A15 KS-1018: it is file-disjoint (auth `routes/users.ts`), and it would make 3 open.

## Detail
**Links:**
- linkKind (attachmentsForURL pull/1014): exactly KS-1176 contributes (read 20:07:37Z).
- 0 closing phrases in title and body (regex control 2 of 2); 0 at-mentions; KS-1187 not named.
- Ticket comment on KS-1176 naming the PR: d2296a6e-b53e-4dd7-bfa1-707c7e0ee834 (20:07:46Z, anchors 7/7).
- KS-1176 is assigned to the board account; state In Progress (moved by the integration when the PR opened).

**Push:** push rc 0 at 20:07:01Z (started 20:01:46Z); in-hook preflight `PREFLIGHT INCOMPLETE — 12/15 legs ran, 3 SKIPPED. Nothing failed.` Legs 3, 4, 8 skipped (no local stack) — not a pass of those legs. Push verify PROTOCOL-CLEAN: first push, one tracking ref added at origin's head; shared .git/config sha256 identical, worktrees identical, 111 heads identical, 0 other refs changed.

**Your red-proof list, item by item:**
1. The ticket's three cells:
   - `api_key` vs `none` → true (also `NONE` and `''`);
   - `api_key` vs `basic` and `standard` → false (all six above `none` checked);
   - five unrecognised strings (`api_key`, `API_KEY`, `oauth_app`, `FULL`, `kyc-pending`) behave exactly as `api_key` against 15 required spellings. Each also asserts `none` true and `basic` false, so the equality is not vacuous at base.
2. PARITY: 15x15 (7 known, their uppercase, and `''`) equals the base comparison, computed from an independent copy of the order. The row count is asserted as 225.
3. The route, `POST /api/documents`, through the real router and the real `enforceDocumentTypeRules` (only the Redis catalogue mocked, with the real seeded `SSD_DOCUMENT`):
   - a connector key creating `SSD_DOCUMENT` gets enforcement `ok: true`, then 201 (at base: `ok: false`, 403);
   - a connector key creating a `standard` type gets 403 `INSUFFICIENT_VERIFICATION_LEVEL`, and the workflow is never called;
   - control: a STANDARD human on the same type gets 201;
   - control: an unregistered type gets 400 `UNKNOWN_DOCUMENT_TYPE`, so the catalogue is live and this is not the empty-catalogue pass-through.
4. `:557`, `POST /api/documents/:id/verify` (stub originate):
   - a connector key on a standard-gated type gets 403, `requiredLevel standard`, `currentLevel api_key`;
   - control: a STANDARD human gets 200;
   - control: a connector key on a verifier-`none` type gets 200.
5. The widening tamper (TW: unknown satisfies everything) reds 4 cells.
6. KS-1190: a cell pins "an off-canonical required level passes every authenticated principal" (12 users x 3 levels = 36 rows). The fail-closed tamper TR reds exactly that one cell.

**Tamper table** (whole api-gateway suite per row, 49 files / 423 cells run, 0 pending; restores asserted by sha256 against the HEAD blob and by `git diff --quiet HEAD`; every red an AssertionError, 0 load failures):

| Row | Tamper | Reds | Which | tsc rc |
|---|---|---|---|---|
| T0 | none | 0 | | 0 |
| TA | fix reverted | 3 | A none; A unknown; D connector SSD_DOCUMENT | 0 |
| TW | unknown satisfies everything | 4 | A above-none; A unknown; D connector standard; E connector gated | 0 |
| TK | `>` for `>=` | 8 | A none; A unknown; B parity (33 rows); D SSD; D human; E human; enforcement.test "equals the requirement"; enforcement.test "empty as none" | 0 |
| TR | unknown required fails closed | 1 | C (KS-1190 pin) | 0 |
| TI | inert comment | 0 | | 0 |

**Test Evidence summary:**
- Host: macOS arm64 worktree raise-0916-a, node v24.7.0, in-process vitest over loopback. No stack (0 docker images, 0 containers).
- Baselines at e0f41a8fa: api-gateway 48/410, shared 44/851, auth 61/745. 0 failed, 0 skipped. tsc rc 0 for api-gateway and for auth.
- At the head: api-gateway 49/423, shared 44/851, tsc api-gateway rc 0.
- eslint: 0 problems on both files. Control: 93 rules resolved, and a stdin sample reported its warning.
- Docs (§4): neither HTML doc affected; 7 KS-1176 terms have 0 hits in both (control: Schemathesis 37 and 61).
- Schemathesis, Akto, Playwright, k6: not run. Measured reason: no stack. No spec change; the published contract already lists 403 INSUFFICIENT_VERIFICATION_LEVEL.

**NOT done / NOT covered:**
- The live half: a Platform-S upload under a connector key against a seeded Platform K, then `POST /api/verification/verify` resolving it (§5f; KS-1176 stays In Progress on merge).
- Real Redis catalogue population; the gateway behind nginx.
- The auth `requireVerificationLevel`, shared `requireVerificationLevel` and shared `policy-engine` copies: recorded in the body, not edited. All three have 0 production callers by census.
- The frontend copy (`frontend/issuer/src/components/DocumentUpload.tsx:74-78`): reported only; not my partition.
- KS-1190's two measurements.

**Accommodations:** none. This was not a READY-file apply. The shape was ruled in your ANSWER (19:52:15Z).

**Filed this round:** KS-1190 (Backlog, Medium, board account, related KS-1176, not built). Searches quoted in it:
- meetsVerificationLevel: 2 fuzzy / 2 literal
- creatorVerificationLevel: 3 / 3
- reqIdx: 0 / 0
- document-types: 121 / 13
It carries the READ chain:
- originate `adminConfig.ts:156-172` stores any level string;
- gateway `platform.ts:880-894` clones template levels;
- the Redis fill at `services/redis.ts:511` `setDocumentType` is UNTRACED.
It also carries the two measurements needed before any fix.

**Records:**
- Branch cut with `switch --no-track`; the shared .git/config sha256 was unchanged across the switch; the branch has no upstream.
- Local commit 616c766a5, identity kamil.kreiser@secuura.ai (repo-local).
