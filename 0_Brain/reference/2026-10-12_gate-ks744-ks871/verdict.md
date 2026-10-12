# QA gate: KS-744 and KS-871 Done decisions (seat K 4th), 2026-10-12

Independent Opus gate. Read-only on the repo and the box. I re-ran everything myself in my own clone:
`<scratchpad>/g`, cloned `--no-hardlinks` from the seat's clone, because the shared repo does not hold
`65d7722f83a6`. Commits are content-addressed, so that clone cannot alter a SHA.
I made no Kintsugi calls. The box facts below come from the seat's saved outputs, checked against my own build.

## Verdicts

| Ticket | Verdict |
|---|---|
| **KS-744** | **GO WITH NOTE** |
| **KS-871** | **GO WITH NOTE** |

Neither ticket has a Major defect. I could not refute any of the seat's load-bearing claims.

## (a) Ancestry: CONFIRMED

- **Develop tip.** `git ls-remote origin refs/heads/develop` returns `65d7722f83a61b7a18cf9dc0b4aeccd4fe1af6b9`, which matches the claim.
- **Both fixes are on develop and on Kintsugi.** `merge-base --is-ancestor` answers YES for each of these four pairs:
  - `0a2b1603fe52` → `65d7722f83a6`
  - `0a2b1603fe52` → `69f2045af2a4`
  - `523f283c6cd2` → `65d7722f83a6`
  - `523f283c6cd2` → `69f2045af2a4`
- **Control.** The reverse check (`65d7722` an ancestor of `0a2b160`) answers NO.
- **Kintsugi is behind develop.** Kintsugi's revision `69f2045` is an ancestor of develop, 72 commits behind it.
- **Same source at both revisions.** These files have the same blob at `69f2045` and at `65d7722`:
  - `auth.ts`: `bf09d315a644`
  - `audit.ts`: `052131de06c3`

  The 11 api-gateway files that differ between the two revisions are tests and routes. None of them is middleware.
- **No later edits.** The last commit to touch `auth.ts` after the fix is `a105cd32b` (KS-1215), and it leaves lines 407-408 intact. Nothing has touched `audit.ts` since `523f283c6`.

## (b) Code against the acceptance text: CONFIRMED

- **KS-744.** At `services/api-gateway/src/middleware/auth.ts:407-408`, the header is set only when the claim is truthy, and is otherwise deleted.
  - No service outside the gateway reads `x-verification-level`. `git grep` over `services/*/src` and `packages/*/src` finds no non-test hits beyond `auth.ts:337, 369, 407-408`.
  - So the "real upstream" item the ticket said was owed carries no reader risk.
- **KS-871.** In `middleware/audit.ts`:
  - `:224` sets `auditPath = req.path` at entry.
  - `:244` calls `deriveAction(req, auditPath)`.
  - `:294` writes `details.path: auditPath`.

## (c) Tests and my own planted-red: CONFIRMED

Counts below are read from the vitest JSON report. No test file finished with zero assertions.

| Run | Result |
|---|---|
| ks744 green | 7/7 pass |
| ks744 tamper A: the ticket's original unguarded line | **4 red** (R2, R3, R4, R5). R2 and R3 fail with `[500, 0, null]`, so the cells reproduce the ticket's 500. Matches the seat. |
| ks744 tamper B: guard kept, `else delete` removed (my own discriminator) | **1 red** (R3). The delete is pinned too. |
| ks744 restored | 7/7 pass, `git status` clean |
| ks871 green | 9/9 pass, 3 files |
| ks871 tamper T1: `details.path` set back to `req.path` | **2 red**. Matches the seat. |
| ks871 tamper T2: `deriveAction` given `req.path` | **3 red**. Matches the seat. |
| ks871 tamper T3: both sites reverted (mine) | **4 red** |
| ks871 restored | 9/9 pass, clean |
| Whole api-gateway suite at `65d7722` | 97 files / 876 tests, 876 pass. Matches the seat's baseline JSON. |

My first ks871 runs passed all three file names as a single argument. They loaded **0 files**, and the zero-file control caught it before I read any result. I re-ran them correctly, and the rows above are from that re-run.

## (d) Deployment: CONSISTENT

- **My clean build matches the box.** My own `npm ci` plus `tsc` build at `65d7722` gives **10 of 10** middleware sha256 values equal to the running container's values in `box/kin2.out`. These include:
  - `auth.js`: `f11812c0…`
  - `audit.js`: `7536b1f0…`
- **Hash-differs control.** Rebuilding with tamper A gives `auth.js` = `b75f2904…`, which differs. Restoring and rebuilding gives `f11812c0…` again.
- **Live KS-871 row.** `box/kin6.out` holds a real Postgres row: `gdpr.create | gdpr | /api/gdpr/erasures | POST | f | ks-l02-k4-871-probe`. This lines up with `live/live1.out` E1, which shows `403 INSUFFICIENT_SCOPE` at 05:03:47Z. So the middleware is live and writing rows, which settles the ticket's "latent or live" question.

## Defects

**KS-744**

1. **Minor, evidence.** The seat's saved marker grep contradicts its claim that the fix is deployed:
   - `box/kin2.out:15` reads `KS-744 delete x-verification-level when claim absent   0`. The cause is a nested-quote bug in `box/kin2.sh:6-7`: `'$2'` contains single quotes, so the pattern loses its brackets.
   - I reproduced it against the byte-identical `auth.js`: the kin2-style grep returns 0 and a direct grep returns 1.
   - `box/kin3.sh` was written to settle this, but **no `kin3.out` was saved**. So the seat's line "guard is at compiled lines 345-347 on the box" has no saved receipt. The hash equality does settle it.
2. **Minor, evidence.** These claims have scripts but **no saved output**:
   - "Kintsugi has 20 users, 0 NULL `verification_level`" (`box/kin10.sh`)
   - "0 restarts" (`box/kin8.sh`)
   - "a tampered copy differs"

   My hash-differs control covers the last one.
3. **Note, acceptance.** On Kintsugi only the truthy branch was exercised (`live1.out` L1 shows `verificationLevel=present`). The ticket's 09-17 comment said a claimless token "minted by auth" was owed before Done.
   - That path stays unexercised on the box.
   - The code is proven byte-identical to the tested code, and no downstream service reads the header.
   - The suggested `NOT NULL` pairing was not done. The ticket made it optional.
4. **Note, test shape.** The ks744 cells use a test-local express app with its own error handler (`ks744-…test.ts:59-64`), not the real gateway mount. The real-app coverage is the earlier gate's 135 http-proxy cells, which I did not re-run.

**KS-871**

5. **Note, acceptance.** The GET clause ("and the GET with its full path") is **not met as written**.
   - `AUDITED_METHODS` at `audit.ts:58` covers POST, PUT, PATCH and DELETE only, so a refused GET writes no audit row.
   - A cell pins that no row is written.
   - This was already ruled at merge (R-2), but it is still a literal acceptance line that is not delivered.
6. **Note, acceptance.** "Admitted requests unchanged" is literally untrue for non-canonical spellings.
   - At merge, 256 test-mode rows and 574 production-mode rows changed `action` / `details.path` (for example `v1.*` → canonical), by design.
   - No cell measures the out-of-repo consumers.
7. **Minor, residue.** These lines still read `req.path` inside `finish` (out of scope, already on KS-1189):
   - `audit.ts:261` and `audit.ts:288`: the login special case and `attemptedEmail`.
   - `audit.ts:333`: the write-failure log.

   So "every `router.use` gate benefits" holds only for `action` and `details.path`.
8. **Note, weak zero.** In `box/kin6.out`, "pre-fix signature, all-time: 0" has no positive control showing that a refused POST happened on Kintsugi before the fix. It shows absence only. The positive evidence is the 05:03:47Z row.
9. **Note.** Kintsugi runs `NODE_ENV=development` (`box/kin4.out`), so the production `/api/v1` 307 path rests on the in-repo production cell, which I ran green.

## Not checked

- I did not query the box myself.
- I did not re-run the earlier gate's 135-cell real-gateway or 1115-request census.
