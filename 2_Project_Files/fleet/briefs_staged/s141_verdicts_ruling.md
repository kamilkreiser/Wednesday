## BLUF
**Both verdicts are in. #867 (KS-913): PASS — one line to correct, then it merges. #868 (KS-914):
NO-GO on two Majors — a fix round, and it is round 1 of the two-round cap. The SSRF property itself
is DELIVERED and measured four ways; the NO-GO is about what rides alongside it. Finish KS-921 to
its READY first, then take the #868 fix round, then KS-920.**

## #867 — PASS, with one correction before the merge
The gate measured every DoD line and met it: the census (21 files at the base, 20 at the head, set
difference exactly one file removed and none added), the SQL gate byte-identical at both SHAs
(sha256 `a63aaabe…`, 23 lines), the row id appearing in exactly one place in the tree, the seed-gate
suite 24/24 at both SHAs, and `example.com` confirmed as a NULL-MX domain (RFC 7505) that accepts no
mail at all.

**Correct B-1 before you merge.** The rewritten paragraph says *"Three of the fourteen are seeded
`ORG_ADMIN`"*. **It is four.** I counted it myself rather than relaying the gate: over the fourteen
rows carrying `hash: ADMIN123`, the roles are **4 `ORG_ADMIN` and 10 `OWNER`** (control in the same
batch: a role that is not present returns 0, and the OWNER count is the other answer). The number is
the blast radius of the takeover primitive that paragraph describes, and the PR rewrote that exact
sentence, so it is ours to get right. One word, on the branch, then mail me the new head SHA and the
one-line diff — **I will verify the count myself and send the GO; no re-gate for a comment.**

**Also record B-2 on KS-913 before you merge — it is a state change the PR does not mention.**
The old row was a permanent no-op on the demo: `ON CONFLICT (email) DO NOTHING`, and
`kam@secuura.ai` already exists there because the two runtime seeders create it.
`org.admin@example.com` exists nowhere and collides with nothing, so **the next `/seed-demo-users`
run WILL insert it — one additional live `ORG_ADMIN` carrying the `admin123` hash printed in that
file.** Behind the two-flag gate and the same class as three sibling rows, so it does not stop the
merge; but it must be a recorded decision rather than a side effect of a privacy edit. Put it on the
ticket in those terms, and note it as an addition to the context of Kam's open card — I will carry
it to him.

**B-3 (the gate the comment points at has zero tests) is a real gap**, and the gate's own reading is
right that two different gates share a name in the prose. **File it as its own P3** — do not widen
this PR. **B-4 is pre-existing and not yours**: record it on the ticket as a curio with the gate's
measurement, nothing more.

## #868 — NO-GO, fix round 1 of 2
**Say this to yourself first, because it is true and it is the part that matters: the security
property is delivered.** The gate measured it four ways — the pinned socket, TLS identity (through
the real function, with the server's SNI callback seeing the hostname and a wrong-SAN certificate
correctly refused), IPv6 answering family 6, and the `.invalid` discriminator. The 59 inherited
cells were proven untouched BY SET, not by count, and proven still to BIND the refactored resolver.
After this PR there are exactly two service-side uses of `assertSafeOutboundUrl` and both are the
registration sites, so **zero in-tree instances of the validate-then-fetch gap remain.** That is the
ticket's whole purpose and it holds.

Four things to fix, in this order.

**1. A-1 (Major) — restore a TOTAL deadline. This is the one that matters.**
`AbortSignal.timeout(10000)` bounded the whole operation; `req.setTimeout(ms)` is a socket-idle
timer that is not armed until the socket connects. Measured on the real exported function against
`https://198.51.100.1/` (TEST-NET-2 — the classifier passes it and it is unroutable):
**declared 3000 ms, elapsed 75014 ms.** The base returned in 10005 ms. Second manifestation: a
server dripping one byte every 1.5 s holds it open indefinitely, because the head also drains the
body and waits for `end` for a body no caller reads. Live on `POST /webhooks/:id/test` and on
`POST /api/teams/notify`, which loops over every active row inside the request handler.
**The fix carries a ceiling on the whole operation — connect, transfer and drain — not only on
idleness.** Red-proof it with the gate's own two cases: the TEST-NET-2 destination must return
within the declared bound, and the drip-feed must be bounded. The gate's honest qualifier stands and
belongs in your PR body: for m365 this is **not** a regression, since the base called `fetch` with
no signal at all — what the head adds is a parameter that READS like a bound.

**2. A-2 (Major, coverage) — bind the SHIPPED path, not the helper.**
All six new cells build their own agent and call `pinnedLookup` directly; **no cell anywhere in the
repo calls `safeOutboundRequest`.** The gate stripped `lookup:` from the two agents inside it,
left `pinnedLookup` untouched, and got **778 passed, 0 failed** — the pinning gone from the only
shipped path and nothing noticed. Add the wiring assertion the gate described: that the agent handed
to `mod.request` carries a lookup answering with `resolved.addresses[0]`. **Red-proof it with that
same tamper** — strip `lookup:` and the new cell must red. No test-only hole in the guard is needed
for it, which is why this one is worth doing and the end-to-end rebind still is not.

**3. A-5 + A-4 (Minor, together) — make the distinction real or stop claiming it.**
Two comments say blocked and failed *"stay distinguishable at the call site"*. The return type has
one `{ok: false; error: string}` arm with no discriminator, and the call site proves it: same
branch, same `status 0 / success false`, same log line. Meanwhile `blocked by SSRF guard` went from
two files to zero, and the loss shows on two operator-facing surfaces — the persisted
`svc_webhook_deliveries.error` and the `delivery.error` field of the test-send response. **Prefer
making it true over correcting the prose:** carry a discriminator on the error arm and restore the
distinction at the call site, so an operator can tell "we refused to send" from "their endpoint was
down". If you judge that too wide for this round, say so and correct both comments instead — but
then the distinction is a ticket, not a silence.

**4. A-3 (Minor) — document the redirect change, both halves.**
`fetch` followed redirects; `http.request` does not. **The security half is real and favours your
change**: the base guard ran once on the original URL and then followed the `Location` with a fresh
unvalidated resolution — the gate drove `Location: http://169.254.169.254/latest/meta-data/` and the
base stalled its full abort window on an address the guard refuses as a direct target. The
availability half is also real: a subscriber answering 3xx used to be delivered to. Nothing in the
repo asserts following, so CI is silent and a real subscriber is not. **Both halves go in the PR
body and the module header.** No behaviour change requested.

**A-6 needs nothing** — the header already discloses the single-address behaviour accurately, and
the gate said so. **A-7:** the load-bearing cell's own `req.setTimeout(4000)` guard is inert; the
~5004 ms figure in your predecessor's mail was vitest's `testTimeout`, not a connect timeout. Fix
the cell's guard while you are in the file, and note that the same shape ships in
`safeOutboundRequest` where there is no vitest — which is item 1.

## Sequencing
1. **Finish KS-921 to its READY** — you have the census and the fixture; do not leave a guard
   half-built.
2. **Then the #868 fix round** — one branch, one round. **This is round 1 of 2 under the cap:** a
   second NO-GO on this class ships what is closed and tickets the residue, and a third needs Kam's
   word. Say the round count in your READY.
3. **Then #867's one-line correction** if it is not already done in passing, then KS-920.

## What the gate did NOT test — carry it, do not re-litigate it
The end-to-end DNS rebind against `safeOutboundRequest` was not constructed, and I agree with both
of you that a permanent test-only hole in the guard is not a trade worth making. The mechanism is
proven; the end-to-end rebind is not, and that sentence belongs in the PR body. Linux timing for
A-1 was not measured (Docker is out of bounds) — the 75 s is a darwin floor, and `tcp_syn_retries=6`
would make it worse there. `deliverWebhook` has no unit test at either SHA, which is why A-1 would
have been caught by nothing.

## Standing
`develop` `a821bd0aa` when last read; **the local `refs/heads/develop` is STALE at `b77b20bf6`** —
the gate flagged it, so read `origin/develop`, never the branch name. Seat B is live and merging.
Kam's card is open at default HOLD and B-2 above is now part of its context. Kam's direction is the
sort key once these are done.

-- Wednesday
