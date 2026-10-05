Raised from a Wednesday-held Spark pass, re-proved end to end by Seat B 60th. One ticket, one commit.

**Refs KS-1345**
https://linear.app/secuura/issue/KS-1345

## What this pins

`GET /api/webhooks` chained `.catch()` onto its list query and returned
`200 { success: true, webhooks: [] }` on failure, so a database error was indistinguishable from
"this organisation has no webhooks" — to the client, and on this route to the log as well. That
`.catch` is removed, so a rejected query reaches the route's existing `fail500`: a constant 500
body, the error logged once server-side, never a 200 with an empty list.

The change also **flips an existing control into a red cell**. What was `control KS 1341 A0`,
pinning the swallow as pre-existing behaviour, is now `RED KS-1345 A0`. A new `control KS-1345 C`
pins that a query which *resolves* still answers 200 with its rows and logs nothing — without it,
A0 would be satisfied by the route answering 500 unconditionally.

## Behaviour change, stated plainly

A rejected list query now answers a **constant 500** where it answered `200 []`. A second case
follows from the same removal: a non-UUID `userId` makes Postgres raise 22P02 on the `::uuid` cast,
which was swallowed the same way and now answers 500. **Which principals can carry a non-UUID
organisation id is UNMEASURED** here, and is the part of this change most worth a second look.

## Test Evidence

**Touched**
- `services/originate/src/routes/webhooks.ts` (+4/-2)
- `services/originate/src/__tests__/ks1341a-webhooks-500-never-answers-err-message.test.ts` (+22/-9)
- `Projects Documents/API_Security_Functional_Testing_Architecture_Flow_Diagrams.html` (+91/-0)
- `Projects Documents/QA_Tool_Cheat_Sheet_Secuura_API_Testing.html` (+37/-0)

**Ran**
- `jest` 29.7.0 by named binary in `services/originate`, full suite, base and head:
  **1062 → 1063 tests, 0 failed at both ends, 0 new reds, 90/90 suites.**
- The nine cells: 9/9 green, 1.169–2.537 s reported (1.47–3.26 s wall) over three consecutive runs,
  2026-10-05, host Kamil's Mac Studio (2), node v24.7.0.
- **Red-first, by assertion.** With the test section applied and the product change withheld, the
  file runs **1 failed / 9**, and the red is `RED KS-1345 A0` failing on its own assertion:
  `status: 500` expected, `200` received — which is the swallow itself. The four load-failure
  signatures (`Cannot find module`, `SyntaxError`, `Failed to load`, `Transform failed`) are each
  **0** in that run, so it is an assertion red and not a file that failed to load. Applying the
  product section takes it to **9/9**.
- **Applied == held, proved on files rather than diffs.** The held patch carries no-op blank
  `-`/`+` pairs, so git regenerates it as `webhooks.ts` **+4/-2** and the test **+22/-9** where the
  source declares +5/-3 and +23/-10; the two are therefore not `cmp`-equal as diffs. An independent
  strict apply of the same sections onto the same base blobs, in a separate repository, produced
  byte-identical files — `sha256` `2f8828ba0246…` and `bca6c7da5118…` on both sides — with a firing
  control showing both differ from the base blob.
- Both sections `--check -v` strict rc 0, no `--recount`, no fuzz. Tamper control (hunk header
  corrupted) rc 128 `corrupt patch`. Modes 100644, unchanged.
- `tsc` 5.9.3 by named binary, `-p services/originate --noEmit`: **rc 0 at base and rc 0 at head**,
  with a positive control (a one-line type error) returning rc 2 and TS2322 — so the rc 0 is a
  result, not a binary that does nothing.
- `pathgate55` **PASS**: 6 assertions over 4 measured paths, 0 failed, its own must-hit controls
  firing. Firing control: this head against the other PR's declared set FAILS, naming the missing
  and the extra paths.

**NOT run**
- No live sweep (skill §5f), so **KS-1345 does not move to Done on this change's account**.
- `tsconfig.json:19` excludes `src/__tests__` and `src/**/*.test.ts`, so **tsc never typechecks the
  test file this PR edits**.
- No deploy, no migration, no Docker, no `az`, no running stack.
- The **deliveries half** of the ticket (`webhooks.ts:412`) is untouched, as is `dispatchEvent`'s
  `.catch` at `:513`. Both swallow in the same shape and stay open on the ticket.
- Which principals can carry a non-UUID organisation id: UNMEASURED, as above.

**Migrations + config**
- None. No migration, no schema change, no environment variable, no dependency, lockfile, manifest
  or baseline edit. The KS 466 `::uuid` cast comment is amended in wording only.

## Skill §4 — both platform-k documents, same commit

A new self-contained block in each: flow `<h2>13.`, and the cheat sheet's own unnumbered
`div class="section"` convention. Both doc edits are **pure appends** — 0 replaced and 0 deleted
lines in either document, measured by a line-level diff.

**On the numbering.** The flow document here has no block **12**. That is deliberate and is stated
in the block itself: block numbers belong to tickets, not to merge order. 12 is reserved for
KS 1333, raised separately; whichever lands first, each block sits in number order and nothing is
renumbered.

**Timing, stated rather than added.** Measured at the base SHA `3ce8cd4026a6`:
`services/originate` **0** occurrences and `jest` **0** in both documents, against a must-hit
control of `auth` at **70** (flow) and **69** (cheat sheet). So the zeroes are measurements, not a
blind grep, and no stated timing row is amended.

## Merge-in note

This branch is cut from `3ce8cd4026a6`. If the KS 1333 PR lands first, this one needs a merge of
`develop` **into** the branch (never a rebase, never a force push) resolving only the two documents
by placing each block in number order. That merge-in tree is **predicted** as
`fb53feacdf1d03e3e949f7cf3a607254e8e5d9c6`, computed in a scratch clone: the conflict is on exactly
the two `Projects Documents` files and every other path auto-merges, and the resolved tree differs
from the conflicted tree in exactly those two paths.
