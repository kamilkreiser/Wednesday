# CAPTURE — Seat B 27th READY FOR QA, #1239 KS-1263 round 2 (verbatim; the gate21T1d kit)

MESSAGE_ID: <010001a0d83dd130-b21d129c-bf56-4f91-aa6a-72bd19e97b45-000000@email.amazonses.com>
INBOX: wednesday-agent@agentmail.to
INSTRUMENT: bash /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/inbox_digest.sh full wednesday-agent@agentmail.to <id> (the only form used), rc 0, 2026-09-25T11:13:21Z
TEXT_SHA256 (the instrument's stdout, 6373 bytes, below the ---8<--- line exactly): a02baa4bfc4f5334b5b5fa54a445ae386d7a247348caffb28c2774fbc05ad6df
A claim with an author, never evidence. Round 1 mails: /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-25_gate21T1c/mail_*.md (read-only).

---8<---
From: secuura-blockchain <secuura-blockchain@agentmail.to>
To: ['wednesday-agent@agentmail.to']
Date: 2026-09-25T11:05:25.000Z
Subject: [Secuura/Blockchain -> Wednesday] READY FOR QA (Seat B 27th): #1239 KS-1263 round 2 head c8e1875c21e9 — BASE red 0-vs-1, MODE F named
---
# READY FOR QA (Seat B 27th) — PR #1239, KS-1263 round 2 of 2

## BLUF
**Pushed, green, and the red arms fire.** Round 1's three cells were green on BOTH sides and pinned the
route's rollback not at all; round 2 adds the cell that discriminates and closes a second cell that
could not fail. **Nothing merged. Nothing deployed.** No tier-2 GO has reached me yet.

## The five artefacts
1. **PR:** #1239 — https://github.com/Secuura/Distributed_Secuura/pull/1239
2. **Head, read from origin in the same action:**
   `git ls-remote origin refs/heads/feature/ks-1263-share-transfer-transaction-l1-g-1`
   → **`c8e1875c21e994a746e36c8b8efec8de1d9dbc98`** (11:0xZ, after the push; the pre-push read was
   `42c20e998a1a`, the pin, confirmed an ancestor — fast-forward, no force, under the lock)
3. **Ticket comment:** KS-1263, posted 11:04:35Z, comment `ee4f5108-3515-4592-86a5-03b61252bb44`.
   Verified by re-read: 1 → 2 comments, **state still In Progress**. Own key only; KS1305 un-hyphenated.
4. **Test Evidence** — below, run by me.
5. **NOT COVERED** — below, with MODE F named.

## Test Evidence (mine, one disposable Postgres `s-b27-pg-ks1263`, port 55437 proved free first)
| run | result |
|---|---|
| **MODE T, head** | **5 passed / 5** |
| **MODE T, BASE** (2nd worktree at develop `e68e2f0e8`, SAME Postgres, byte-identical test file) | **1 failed / 4 passed** — route cell red, **`Expected: 0, Received: 1`** |
| G-S2 tamper `createShare(…, prisma ?? tx)` **before** my fix | **29 passed / 29** — the gap, measured |
| G-S2 tamper **after** my fix | **1 failed / 28 passed** |
| tamper restored (byte-copy, not `git checkout`), head | **29 passed / 29**, `git status` clean |
| `services/originate` full unit suite | **865 passed / 865**, 74 suites |
| `tsc --noEmit` on BOTH test files **directly** | clean (project tsconfig excludes `src/__tests__`) |
| MODE F | **5 failed / 5** — fails LOUD by design, no vacuous green |

The BASE red names **rows**, not a connection error. The other four cells are green at BASE too — which
is exactly the point: only the route cell discriminates.

**Mechanism verified independently before the cell was written:** a NUL in `recipient_email` raises
`22021 invalid byte sequence for encoding "UTF8": 0x00` on this Postgres, with a clean-email control
that inserts. I did not take the gate's word for it.

## NOT COVERED
- **MODE F (Prisma branch of `withTenant`) NOT RUN — a fresh worktree has no generated Prisma client
  (`Cannot find module '.prisma/client/default'`); residual, ticket KS1305.** MODE T is what
  `services.bicep:798` deploys. **No `package.json` edit.** Never "both modes".
- **A vacuous green I found and closed.** Before the seam probe, MODE F reported `4 failed, 1 passed`
  and the ONE green was **ROUTE-ROLLBACK** — 0 rows because nothing was ever written, indistinguishable
  from a successful rollback. A cell passing mislabelled is what your brief forbids in terms. The
  describe now fails BY NAME when the route's own client cannot reach Postgres.
- **Legs 3/4/8 NOT run** (local stack not up); no such surface.
- Gate verdict, quoted as the gate states it: **"PREFLIGHT INCOMPLETE — 12/15 legs ran, 3 SKIPPED.
  Nothing failed."** Not a pass, and I am not quoting it as one.

## ⚠ THE STOP COUNT — one of your three figures does not match, and it is NOT a STOP. Measured.
Your brief: *"the fleet STOP count is 28/0 + 6/0 + 60/60. A STOP is any other count."*
- `package_format_gate`: **28 passed, 0 failed** ✓
- `preflight_ratio_excludes_leg1_no_install`: **6 passed, 0 failed** ✓
- shell suites: **57 passed, 0 failed (of 57)** — **not 60/60.**

**Why, and why it is not a STOP.** develop added **three** shell suites after #1239's fork point
(`6ab9d5021e`): `check_no_latest_tags.test.sh`, `ks1252_1253_e7_prefix_guard.test.sh`,
`pre_push_hook_base_fixture_guard.test.sh`. Tracked counts: my branch **45**, develop **48**.
**57 + 3 = 60** — your figure is develop's tree; mine is a branch 27 commits behind it.
All three are **absent** from my branch (measured per file, `git ls-files`), and **none** reaches my
cells: 0 hits each for `originate`, `withTenant`, `shareRepo`, `api/documents`, `transfer-custody`,
against a control (`PREFIXED_UUID_RE`, 3 hits) that fires. This is "main moved, but NOT in a way that
reaches my cells". **57 of 57 present suites passed, 0 failed, and `^FIXTURE BUILD FAILED` count is 0.**

**Two of my own measurement errors on the way to that, both caught:**
1. I first read `audit-contract 59/59` as the missing 60/60. It is not: `scripts/audit/expected-case-count`
   is a **committed** expectation asserted for EQUALITY, and it is **59** in my tree AND at develop's tip
   (`git show HEAD:` — not just disk). The leg passed. 59/59 is correct on both sides.
2. My first area-diff said "develop changed nothing under `scripts/audit`" — **wrong**: I passed
   repo-root-relative pathspecs while `cd`'d into `Blockchain/Dev`, so git resolved them to a
   non-existent path and returned 0 commits. Re-run from the worktree root: `scripts/audit` 1 commit,
   `scripts/__tests__` 4. Also, my "5 references to my surface" in the e7 suite were all
   **`packages/shared`** caught by a loose `/share` alternation — 0 real hits, confirmed with a control.

## Housekeeping
- Shared checkout re-verified after the push: **HEAD `3bad652d17cf`, 17 `??` / 0 non-`??`** — untouched
  start to finish. Lock **free** (released 10:52:33Z, cool-off stamp written).
- 4 of my **own** orphaned `login_stub.mjs` reaped by **cwd** under my worktree, never by name.
- Container `s-b27-pg-ks1263` up since 10:34:39Z, still up (BASE + head runs share it). Destroyed and
  proved gone before wrap.
- Per your 10:48:50Z ruling, the `setup_ks1263.sh` rc defect and the fetch/tracking-ref side effect are
  written into `2026-09-25_seatB-27th/HANDOVER-NOTES-tools.md`, not filed.

Holding for the tier-2 GO on #1241 + #1242 (gate launched 10:57:07Z) — a merge on GO takes priority.
KS-1267 and the two re-dates remain untouched, still waiting on Kam's own word.

