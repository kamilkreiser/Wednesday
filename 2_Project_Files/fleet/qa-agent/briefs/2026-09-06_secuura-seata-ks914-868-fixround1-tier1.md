# QA Agent Invocation Brief — Secuura / Blockchain (Platform K), SEAT A: PR #868, KS-914 FIX ROUND 1

**Charter first, in full:** `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/QA_AGENT_CHARTER.md`.
Findings only. You never fix, never file a ticket, never touch a builder's tree.

**TARGET — PR #868, KS-914, FIX ROUND 1 OF 2. TIER 1** (a security guard's surface, and the round
that answers a NO-GO). head `babdbd4c2590acca661e126d55e6495e119d53d2`; its parent is the previously
gated head `6f0e145e4cdc14ef1c2c12467f53542ec58db7d9` — **nothing rebased, nothing amended**, so the
delta you are gating is one commit.

**A different tester gated round 0 and issued the NO-GO.** Its two Majors were: a declared timeout
that had become a socket-IDLE timer (75 s measured against an unroutable destination where the base
returned in 10 s), and a red-proof that bound the helper rather than the shipped path (stripping
`lookup:` from the two agents inside `safeOutboundRequest` left 778 tests green). **Your job is to
decide whether those are actually closed, and whether the closing broke anything.**

## 2. Spec / DoD for THIS round
Four items, ruled by me in this order: **A-1** restore a deadline over the WHOLE operation;
**A-2** bind the SHIPPED path with the strip-`lookup:` tamper as its red-proof; **A-5+A-4** make the
blocked-vs-failed distinction TRUE rather than correcting the prose (it surfaces on the persisted
`svc_webhook_deliveries.error` and on the test-send response); **A-3** document the redirect change,
both halves, in the PR body and the module header. A-6 needed nothing; A-7 was the same inert-timer
shape in a test cell.

## 3. Scope — claims to measure. Each is a CLAIM UNDER TEST.
1. **A-1, both of the previous gate's cases.** Builder's table, with the idle timer restored by
   inverse edit: unroutable TEST-NET-3 at a declared 400 ms → **30003 ms, killed by vitest**; a
   drip-feed of one byte every 40 ms → **30004 ms, killed**; both bounded with the deadline in place.
   Re-derive both. **Then press the part the table does not cover:** is the deadline armed BEFORE the
   connection is attempted, does it cover connect, TLS, request, response AND drain, and is it
   cleared on EVERY exit path (success, transport error, deadline, guard refusal)?
2. **HUNT — a leaked timer. Name the assertion first.** A deadline implemented with a timer that is
   never cleared, or never `unref`'d, keeps a process alive after the work is done. Drive the shipped
   function to each of its outcomes and say whether the event loop drains — a webhook dispatch loop
   runs this per row.
3. **A-2 with the previous gate's own tamper.** Strip `lookup:` from both agents inside
   `safeOutboundRequest`, leave `pinnedLookup` untouched. Builder's claim:
   `ks914-shipped-path.test.ts` → **1 failed**, and `ks914-pinned-address.test.ts` → **6 passed**
   (the original blind spot, reproduced). Verify the new cell asserts the agent HANDED TO
   `https.request` carries a lookup, and that the lookup **ignores the hostname it is asked about** —
   that last property is the one that defeats a rebind.
4. **HUNT — did the new cells pass for the wrong reason?** The builder reports that its first draft
   used `http://` URLs and got `blocked` for the SCHEME, not the address, because the guard is
   https-only. It says every failure cell is now pinned to its own message. **Check each one**, and
   check the claim that TEST-NET-3 literals are returned without DNS and passed by `classifyIPv4`
   while `192.0.2.0/24` is refused as a documentation range — that asymmetry is load-bearing and
   means there is **no test-only hole in the guard**.
5. **A-5 + A-4 made true.** The error arm now carries `reason: 'blocked' | 'request_failed'`, both
   call sites read it, and `blocked by SSRF guard: ` is restored verbatim at the webhook surface.
   `deliverWebhook` has its **first unit test at any SHA** (4 cells), each pinned by both the returned
   string and the log line, red-proofed by making the call site ignore the discriminator so that
   **exactly one cell reds and the other three stay green**. Re-derive that count — "exactly one"
   is the claim that makes them pinned rather than merely present.
6. **HUNT — the m365 call site.** Its loop iterates every active row inside the request handler and,
   at the previous head, passed no `timeoutMs`. **Does it pass one now?** If not, say what bounds
   that loop today, since the per-request deadline is only as good as the value it is given.
7. **A-3 is documentation only** — confirm both halves are in the PR body AND the module header (the
   security half: the base followed `Location` with a fresh unvalidated resolution; the availability
   half: a subscriber answering 3xx used to be delivered to), and that no behaviour changed with them.
8. **The pre-existing red, independently.** The builder reports `services/originate` at 478 passed /
   2 failed, and says the 2 are develop's: it replaced `routes/webhooks.ts` with `origin/develop`'s
   own copy, got an identical 2/2, restored its own and proved byte-identity by sha256 (`2a623172…`).
   **Re-derive that control.** Its diagnosis: the suite mocks `@secuura/shared` with a factory
   omitting `assertSafeOutboundUrl`, which `webhooks.ts:170` calls, and **the two dead cells are the
   POSITIVE ones** — a guard suite with only its negative half alive cannot tell "the boundary
   rejects bad input" from "the route is broken and rejects everything". Confirm or refute.
9. **The builder's own stated caveat, and it asked to be held to it:** it piped the push through
   `tail -25`, so preflight legs 1–6 scrolled off its capture; legs 7–12 and `PREFLIGHT PASSED` are
   in it. **A banner is not a result.** It is re-running the preflight unpiped on my instruction —
   if its addendum has not arrived, verify the legs yourself. Note this branch carries the **12**-leg
   preflight; leg 13 is KS-921's and lives on a different branch.
10. **Suite totals:** `packages/shared` 784 passed / 41 files (778 at the base + 6 new);
    m365 38 passed; `npm run build` green for shared, originate and m365 — the builder used the full
    build rather than `--noEmit` because the build compiles `__tests__`. Verify by SET where you can,
    not only by count.
11. **Merge-tree against the `develop` you read AT THE TIME, in YOUR OWN copy.** Develop moves —
    seat B is live. I ran none; nothing here is predicted.
12. **Secret gate:** no canary in the repo. Build a fabricated pair from RANDOM tokens (not a
    documented example pair — gitleaks allowlists those and you would get a false clean), prove it
    FIRES in the same scan mode, quarantine by rename, then scan the real range.

## 4. Credentials
Pointer only: the project's own `4_Credentials/.env`. You should need none. **If `gh` under that
project's `GH_CONFIG_DIR` is not authenticated, do NOT fall back to the global config** — the
previous pass hit exactly this and refused correctly; report the PR-body items as UNVERIFIED instead.

## 5. State-mutation & cleanup
Your own `mktemp` checkout with its own index. **Never touch seat A's tree (`2_Project_Files`) or
seat B's worktree (`worktrees/seat-b`)** — both are live, and seat A's checkout also carries the
KS-921 branch. Never the demo VM, the shared local stack, or Docker. **No prune of any kind, and
build no containers.** Restore any tamper by INVERSE EDIT, proven by sha256 — never `git checkout`.
Quarantine by rename, never delete. Report the LISTEN set before and after; you will be standing up
local servers, so that count matters.

## 6. Output boundary
Findings only, one verdict, evidence class on every finding that recommends an action, NOT-TESTED at
the same prominence as the findings. **This is round 1 of 2 under the cap:** if you return a NO-GO,
say explicitly which findings are BLOCKING and which would ship as tickets, because a second NO-GO
ships the closed instances and tickets the residue.

## 7. Known-fragile / known-changed
- **Every tamper prediction NAMES THE ASSERTION it trips**, or is written as "measure what moves".
  Hold me to it — the last two passes each caught one of mine.
- **An instrument is not evidence until it has produced the other answer in the same batch.** Four
  silent instruments on this project today.
- **A red-proof harness names its own subject in its output** — a sibling suite here was found able
  to grade the shipped file and print a transcript byte-identical to a genuine proof run.
- **`vi.spyOn(https,'request')` fails on an ESM namespace** (`Cannot redefine property`); the module
  registry is the only interception point, which is why the new cells live in their own file.
- The end-to-end DNS rebind is **deliberately not constructed** — it needs the classifier to accept
  loopback, and a permanent test-only hole in the guard is not a trade worth making. Do not treat it
  as a gap you must close; it is the stated boundary of the claim.
- `git grep -a` / `git diff -a`. `core.fileMode` is false. `env bash` is 3.2; `/bin/dash` present;
  Docker linux/arm64. Linux timing is unmeasured everywhere on this ticket — darwin figures only.

## 8. Logistics
Report to `wednesday-agent@agentmail.to`, subject
`[QA -> Wednesday] Secuura SEAT A KS-914 fix round 1 (#868)`, verdict in the first line. Report path
under the QA project's own `projects/secuura/reports/`. Budget ~40 minutes.

PROVENANCE:
- the new head, its parent, the four items and every figure quoted above | the builder's READY mail 2026-09-06T11:27:32Z, read whole | read 2026-09-06 21:3x
- the two Majors this round answers, and their measurements (75014 ms; 778 passed under the strip-lookup tamper) | the previous gate's verdict mail 2026-09-06T11:03:07Z, read whole | read 2026-09-06 21:0x
- the four ruled items and their order | Wednesday's ruling to the builder 2026-09-06 21:05, sent through the gate | read 2026-09-06 21:05
- develop a821bd0aa and the open PR heads | `git -C worktrees/seat-b ls-remote` (READ verbs only; no fetch, no merge-tree, no worktree add in either seat's checkout) | read 2026-09-06 20:4x
- NOT READ by me: the #868 fix-round diff itself — I have read only the builder's description of it | not read | read 2026-09-06
