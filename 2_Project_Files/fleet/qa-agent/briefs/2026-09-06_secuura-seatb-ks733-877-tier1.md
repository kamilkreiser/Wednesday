# QA Agent Invocation Brief — Secuura/Blockchain SEAT B · KS-733 · PR #877 · TIER 1

**TIER 1 — a rate limiter on an AUTHENTICATED MFA surface.** `/api/users/me/mfa/*` was unthrottled
while its twin `/api/auth/mfa/*` is capped at 10 per 15 min. The exposure is POST-CREDENTIAL (the
stolen-session case, which is the case MFA exists for, and `/me/mfa/disable` switches it off).

## Charter (read first, in full)
`/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/QA_AGENT_CHARTER.md`. Findings-only.

## 1. Target
- Repo `/Volumes/DevMASTER/!CODING/Secuura/Blockchain` (Platform K).
- **PR #877, head `73f7e2b2b20ba48f6f7045da8127ba2b304a4438`, base develop `066cff67554a5bd5398fcc9fb4b9ade422fbbd5b`.**
  Both read by Wednesday with `ls-remote` in the same action as writing this.
- **Your own clone/worktree, pinned to the LITERAL SHAs.** In a clone taken from the local project
  repo, `origin/develop` resolves to the SOURCE's stale local develop (`ff5218867`). Pin
  `refs/qa/head` and `refs/qa/base` and use only those. The previous two gates both hit this.

## 2. Spec / DoD
`/api/users/me/mfa` is mounted at PARITY with `/api/auth/mfa` (same window, same max), the three spec
ops carry the annotation, the generated yaml matches, and nothing else moved.

## 3. Scope — AIM HERE FIRST. The builder named its own weakest point; it is item 1.
**(1) THE SEPARATE-STORES PROPERTY — the builder's words, and the reason this is tier 1:**
> The assertion is on the MOUNT TABLE, following the KS-689 precedent: no gateway test boots
> `index.ts`. So it asserts the mount exists IN SOURCE — not that express applies it to a given
> request path, and **NOT that the two limiters keep separate stores. That separate-store property is
> load-bearing and is guaranteed here only structurally, by the two `rateLimit({...})` calls being
> distinct object literals. That is the weakest point of this PR and the place I would aim a tier-1
> gate.**
So: **establish what actually happens if the two limiters SHARE a store.** Does `express-rate-limit`
default to a per-instance MemoryStore, or can two `rateLimit({...})` calls collide? If they share,
traffic to `/api/auth/mfa` would consume the budget for `/api/users/me/mfa` and vice versa — which
would make the parity fix partly illusory. Drive it if you can (two mounts, exhaust one, probe the
other); if you cannot boot the gateway, say so and establish it from the library's own source in your
copy. **A structural guarantee that nothing asserts is exactly this fleet's recurring defect.**

**(2) REPRODUCE TAMPER 2 FIRST — it is the row that earns the suite.**
```
  fix present                4 passed, 0 failed
  TAMPER 1  mount removed    2 passed, 2 failed   (mount cell + parity cell)
  TAMPER 2  mounted, max: 5000   3 passed, 1 failed   (PARITY CELL ONLY)
```
The defect is an **ASYMMETRY, not an absence**: a mount with a laxer max satisfies "is a limiter
attached" and leaves the 450x gap exactly where it was. **Without the parity cell a fix that looks
identical ships green and the ticket closes on nothing.** Confirm the parity cell alone reds under
TAMPER 2. Both of the builder's controls should hold (the extractor finds a real mount; returns null
for a prefix that has none) — check that, because "found" must be information rather than a matcher
that says yes to everything.

**(3) THE MOUNT'S POSITION.** A limiter mounted after the route it is meant to protect, or after a
body parser that already did the expensive work, protects less than it claims. Establish where in
`index.ts` the new `app.use` sits relative to the `/api/users` routes and to the existing
`/api/auth/mfa` limiter at :986.

**(4) THE SPEC.** Three ops annotated at `auth.openapi.ts` :2132/:2161/:2191 via the shared
`...rateLimit('mfa')` spread; the yaml **regenerated, not hand-edited** — confirm by regenerating in
your copy and diffing. Confirm no path, method, schema, status or `security` block changed: the claim
is +12 annotation lines on three ALREADY-DECLARED operations.

**(5) `index.ts` restored byte-identical `1d5f66f7ea411af5…` after both tampers, and re-run.**
Re-derive that hash yourself at the head.

**(6) Suites:** api-gateway 268/268 and auth 595/595 claimed green. Re-run both.

## 4. Credentials (POINTER ONLY)
`4_Credentials/.env`. You should not need any.

## 5. State-mutation & cleanup
- **Two builder seats are LIVE** (`worktrees/seat-a`, `worktrees/seat-b`). Touch neither.
- No `rm`; quarantine by rename. **Restore by INVERSE EDIT verified with sha256 — never checkout —
  and then RE-RUN: a hash proves the bytes, only a run proves the file still works.**
- Report the LISTEN set and Docker container count before and after.

## 6. Output boundary
One mail to Wednesday, subject `[QA -> Wednesday] Secuura SEAT B KS-733 (#877, tier 1)`.
Findings-only; severity yours, priority Wednesday's. NOT-TESTED at equal prominence.

## 6a. Evidence class on every finding that recommends an action
Oracle, measurement, control, and what you did NOT establish.

## 7. Known-fragile — read this before you conclude anything from a zero
**EMPTY OUTPUT IS NOT A RESULT — it is an ABSENCE, and an absence has at least two causes. Read the
command's EXIT STATUS, not the shape of its output.** Four instances in this fleet tonight:
1. an unquoted `--include=*.ts` tripped zsh `nomatch` — **the command never ran**;
2. a search term that **could not match** the way the code is written — a real zero read as confirmation;
3. **truncated output** — `head -8` over eleven `vi.mock` calls hid the only one that mattered;
4. `--reporter=basic` is not a valid vitest 4 reporter — **startup error, the runs never happened**,
   read twice as "no output".
Capture `rc=$?` on its own line; never branch on the presence or absence of output. Where you search a
corpus, **PLANT** what you are looking for and find it with the same command.
Also: **a RED that proves nothing is as blind as a green that proves nothing**, and more dangerous
because red is the colour you were hoping for — a tamper that reds by timeout, crash, syntax error or
setup failure is the run failing to happen. State WHICH assertion tripped.
And: **a measurement travels; an explanation of it does not.** Every mechanism above is the builder's,
quoted, and is the thing under test — including Wednesday's framing of it.
Env: darwin, bash 3.2.57, `core.fileMode` false. A fresh worktree has no `node_modules`; `npm ci` from
`Blockchain/Dev` is the documented fix for preflight leg 1, never `--no-verify`.

## 8. Bounds the builder already declared — these are NOT findings
- **Gateway-only:** `services/auth` has 0 limiters of its own (measured with a discriminating
  control), so any path reaching auth directly is unaffected. Stated on the ticket as a bound.
- **No behavioural rate-limit test**, following the KS-689 precedent. Declared, not hidden.
- The served spec was not checked; the yaml is BIND-MOUNTED so a change publishes on container
  RESTART, not rebuild. Nothing was deployed and no claim is made about the running demo.

## 9. Logistics
Wednesday reads your verdict whole and rules. Box ~35 minutes. If short, do (1) and (2) first and say
plainly what you did not reach.

---

PROVENANCE:
- PR #877 head 73f7e2b2b20ba48f6f7045da8127ba2b304a4438 and base develop 066cff67554a5bd5398fcc9fb4b9ade422fbbd5b | `git ls-remote origin` from Wednesday's seat (READ verb only) | read 2026-09-06
- the three tamper rows, both controls, the separate-stores weakness quoted verbatim, the restore hash, the two bounds and the not-done list | seat B's READY mail `[Secuura/Blockchain -> Wednesday] READY: KS-733 PR #877 @ 73f7e2b2b` 2026-09-06T13:13Z, read whole by Wednesday | read 2026-09-06
- the corrected pointers (users.openapi.ts does not exist; the source mechanism is a `...rateLimit('mfa')` spread; the generated yaml DOES carry x-ratelimit keys) | seat B's BY-PATH mail 13:05Z and its own correction in the READY | read 2026-09-06
- the empty-output taxonomy | seat B's mails 13:01Z and 13:13Z, adopted into fleet/specs/brief-standing-lines.md | read 2026-09-06
- the stale `origin/develop` trap | the launcher verdict 12:18:53Z and the #874 verdict 13:16Z, which both hit it | read 2026-09-06
- NOT READ by me: `index.ts`, `auth.openapi.ts`, the generated yaml and the #877 diff. I have opened none of them and run nothing; every mechanism in §3 is the builder's and is under test | not read | read 2026-09-06
