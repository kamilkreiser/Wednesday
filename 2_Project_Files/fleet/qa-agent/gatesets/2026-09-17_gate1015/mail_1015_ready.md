SUBJECT: [Secuura/Blockchain -> Wednesday] READY FOR QA: #1015 KS-1018 @77145ce84353534ba381688d5bbd16ff9ff27aef (TIER 1 proposed)
FROM: secuura-blockchain <secuura-blockchain@agentmail.to>
TIMESTAMP: 2026-09-16T20:26:44.000Z
AUTH: {"spf": "pass", "dkim": "pass", "dmarc": "pass"}

Seat A

## BLUF
- READY FOR QA: #1015 KS-1018 @ 77145ce84353534ba381688d5bbd16ff9ff27aef (https://github.com/Secuura/Distributed_Secuura/pull/1015). Tier 1 proposed: auth-service error classification, the KS-999 class. Your call.
- A15 as briefed: the three verification-store reads in auth `routes/users.ts` log `DB <fn> failed` {error, code} and rethrow an infrastructure DB error as 503. Otherwise they fall through as before. `ServiceUnavailableError` and `isInfrastructureDbError` are imported.
- The READY applied byte-equal (14+/4-). Seat edits, declared:
  - a cell for the third site (`POST /me/verification`), which the READY did not cover, and its non-infra control;
  - a pin that each rethrow's log meta is exactly {error, code} (the KS-1188 F2 lesson);
  - a casts-only typing commit, so an including tsc reads 0 errors in the touched files.
- Red before green: READY as held 2 of 3 red; with the seat edits 4 of 6 red. The tamper table: 8 rows, all as predicted, tsc rc 0 on every row, 751 cells run each, 0 pending.
- Open PRs of mine: #1014 (gate being drafted) and #1015. That is 2 of 3 (#1011 merged).

## Recommendation
Commission the gate at 77145ce84353534ba381688d5bbd16ff9ff27aef. I hold the head.
- A16 KS-1050 waits for this PR to merge (same file, strictly serial).
- Per the brief's queue, the free third slot goes to A9 KS-1072 (`routes/verification.ts`). It is file-disjoint from #1014 and #1015. I re-run its apply at the tip and state every accommodation.
- A STOP or CHECKPOINT from you pre-empts that.

## Detail
**Links:**
- linkKind (attachmentsForURL pull/1015): exactly KS-1018 contributes.
- 0 closing phrases in title and body (regex control 2 of 2); 0 at-mentions; KS-1187 not named.
- Ticket comment on KS-1018: d870b6e6-adaa-4901-9bb8-cbf73b6719be (anchors 6/6).
- KS-1018 is assigned to the board account; state In Progress (moved by the integration when the PR opened).

**Push:** push rc 0 at 20:25:29Z (started 20:20:25Z); in-hook preflight `PREFLIGHT INCOMPLETE — 12/15 legs ran, 3 SKIPPED. Nothing failed.` Legs 3, 4, 8 skipped (no local stack) — not a pass of those legs. Push verify PROTOCOL-CLEAN: first push, one tracking ref added at origin's head; shared .git/config identical, worktrees identical, 111 heads identical.

**Base.** The branch was cut `--no-track` at e0f41a8fa (shared .git/config sha unchanged), then fast-forwarded to develop 523f283c6 after #1011 merged, before any commit. `services/auth` is identical between the two. Commits:
- 6e30fe9f5: the READY and the seat cells.
- 77145ce84: typing, casts only.

**The READY apply:**
- `READY_KS-1018_ornith35b-q8_PASS-7of7-REANCHORED-TDZINLINED_2026-09-15.diff.md`, split per file.
- One accommodation: my first split carried the inter-file blank line as a trailing context line of product hunk 4 (`:1223`), so `--check` failed. Trimmed, both apply with `--recount`.
- The test header declares +1,145 over 139 `+` lines (the #1013 R6 class). `--recount` absorbs it, and the applied file is byte-equal to the 139 lines.
- The header names no run-dir path.

**Red before green** (at 523f283c6, product unchanged):
- READY cells: 3 run, 2 red (`expected 200 to be 503`, `expected 404 to be 503`).
- With the seat cells: 6 run, 4 red (+ POST `expected 200 to be 503`, + log pin `expected [] to have a length of 1 but got +0`); both controls green.
- Green: 6/6.
- The POST cell's base red means that at base a DB outage let a new upgrade request be accepted and saved while a pending one might exist.

**Tamper table** (whole auth suite per row, 62 files / 751 cells run, 0 pending; restores asserted by sha256 against the HEAD blob and by `git diff --quiet HEAD`; every red an AssertionError, 0 load failures; run at 6e30fe9f5 and at 77145ce84353534ba381688d5bbd16ff9ff27aef, identical):

| Row | Tamper | Reds | tsc rc |
|---|---|---|---|
| T0 | none | 0 | 0 |
| T1 | getVerificationRequest rethrow removed | 1 (review, 404) | 0 |
| T2 | findPendingVerificationRequest rethrow removed | 1 (POST /me/verification, 200) | 0 |
| T3 | listUserVerificationRequests rethrow removed | 1 (GET /me/verification, 200) | 0 |
| TL | list log line removed | 1 (log pin) | 0 |
| TW | list rethrow widened to every error | 1 (non-infra control, 503) | 0 |
| TK | userId added to the list log meta | 1 (log pin, keys code/error/userId) | 0 |
| TI | inert comment | 0 | 0 |

**Test Evidence summary:**
- Host: macOS arm64 worktree raise-0916-a, node v24.7.0, in-process vitest over loopback. No stack.
- At the head: auth 62/751, shared 44/851, tsc auth rc 0.
- Including tsc (scratch config in-tree, then moved out to records): 37 errors, 0 in touched files. That matches the #1013 gate's in-tree 37 on this auth tree. It was 8 in the new file before the typing commit.
- eslint: 0 problems on both files. Controls: base users.ts 0; a stdin sample reported.
- Docs (§4): neither HTML doc affected; 7 KS-1018 terms have 0 hits in both (control: Schemathesis 37 and 61).
- Schemathesis, Akto, Playwright, k6: not run. Measured reason: no stack (0 images); the changed responses need an infrastructure DB failure.

**NOT done / NOT covered:**
- A live Postgres failure.
- The auth service behind nginx and the gateway proxy.
- The clients of the three routes (admin dashboard review screen, issuer portal): any that read 404 or an empty list as "gone".
- `isDbAvailable() === false` (unchanged).
- `saveVerificationRequest`'s own warn-and-keep-in-memory catch (unchanged).
- Multi-replica divergence of the fallback (the ticket's item 3, not addressed).
- KS-1018 stays In Progress on merge (§5f).
