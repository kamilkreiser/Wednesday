KS-1179 safeOutboundRequest tests: no cell pins DNS-layer classification, ks932 cells depend on 203.0.113.7 hanging, DNS timer left armed (KS-932 gate F-1/F-2/F-3/F-6)
state In Progress

## BLUF

Test-quality follow-up to KS-932 (PR #1004, merged as `40fe4db69`). The fix is correct: the tier-1 QA gate measured **fail-open: NO**. But the tests around `safeOutboundRequest` leave four holes:

* **F-1 (Minor):** no cell pins DNS-layer classification. Under a tamper that skips classifying the raced lookup, the ks932 file stays 3/3 and the whole shared suite 842/842, while private answers reach a socket.
* **F-2 (Minor):** ks932 cells 2–3 rely on `203.0.113.7` hanging. They go red falsely, or green vacuously, on a host that refuses fast.
* **F-3:** a TS2345 in the new test file.
* **F-6:** the DNS timer stays armed when the race rejects.
  Plus two Polish docblock drifts (F-4, F-5). All in `packages/shared`, one logical path.

## Recommendation

One test pass on `packages/shared/src/security/ssrf-guard.ts` and its tests:

* add the DNS-classification regression cell (F-1), with a connect counter and a public positive control;
* give the ks932 cells a deterministic connect seam (F-2);
* fix the TS2345 (F-3);
* clear the DNS timer when the race rejects (F-6);
* bring the `blocked` and `timeoutMs` docblocks up to date (F-4, F-5).

## Detail

Source: tier-1 QA gate on PR #1004 at `6d077d3fe35cd5f3c09d394553d320e97b1abe32`, verdict 2026-09-16 13:43:51Z. Report: `Testing Agent MAIN/projects/secuura/reports/2026-09-16-ks932-1004-6d077d3fe-tier1-r1/report.md`. The findings, verbatim from its table:

| \# | title | evidence class | severity | target | SHIPS-WITH / TICKET | oracle |
| -- | -- | -- | -- | -- | -- | -- |
| F-1 | `safeOutboundRequest`'s DNS-layer classification is pinned by no cell (TG: seat 3/3, whole 842/842 while private answers connect) | MEASURED AT RUNTIME | Minor | #1004's test file (the carried #873 Record (a), widened) | SHIPS-WITH; TICKET for the pin | Purpose; History |
| F-2 | ks932 cells 2–3 depend on `203.0.113.7` hanging: false red (cell 3) and vacuous green (cell 2, green under its own tamper) on a fast-RST network | MEASURED AT RUNTIME | Minor | #1004's test file | SHIPS-WITH | Purpose; Comparable (`ks914-shipped-path:112`) |
| F-3 | TS2345 at `ks932-timeout-bounds-dns.test.ts:49` (mock resolves an array into `Promise<{address,family}>`), invisible to vitest and to `tsc -p packages/shared` | MEASURED (including program + control) | Polish | #1004's test file | SHIPS-WITH | Statutes & standards |
| F-6 | the DNS timer stays armed for `timeoutMs` when the race rejects (clearTimeout sits after the await) | MEASURED AT RUNTIME (L-4, by handle) | Polish | #1004 | SHIPS-WITH | Product consistency |

Polish, carried here per Wednesday's ruling (not a separate ticket):

| \# | title | evidence class | severity | target | SHIPS-WITH / TICKET | oracle |
| -- | -- | -- | -- | -- | -- | -- |
| F-4 | `blocked` docblocks `ssrf-guard.ts:421-425` and `:519-523` do not cover an unresolved or slow-resolving host, now reachable on a working-but-slow resolver | READ + MEASURED (C-1) | Polish | owner (pre-existing drift, made reachable by #1004) | SHIPS-WITH; TICKET | Claims |
| F-5 | `timeoutMs` docblock `:460-463` says "DNS-free" and the deadline error says "(connect, transfer and drain)" although DNS now spends the same budget | READ + MEASURED (B-1) | Polish | #1004 | SHIPS-WITH | Claims |

**F-1, the regression cell the gate describes (report section 7, verbatim):**

* **The regression cell the owner should add (prose):** in the ks932 file (or `ks914-shipped-path.test.ts`), mock `lookup` to answer `[{address:'10.0.0.5', family:4}]` for `https://rebind.example.com/x`, with a connect counter (or `https.request` spy). Assert `ok false`, `reason 'blocked'`, `error` matches `/resolves to 10\.0\.0\.5, which is forbidden/`, and **0 connects**. Pair it with the public positive control (`203.0.113.7` → exactly 1 connect, through the deterministic seam of §5). Under TG it reds (measured: my R-D 10.0.0.5 cell).

**F-2, the deterministic shape the gate describes (report section 5, verbatim):**

* **Deterministic shape the owner could adopt (prose; nothing written into their tree):**
  * Give the cells a connect seam instead of relying on the internet: a `net.Socket.prototype.connect` wrapper (or an injected agent) that redirects to a 127.0.0.1 listener which accepts and never answers. That makes the hang deterministic, as in F-2.
  * Assert cell 2's bound against `timeoutMs` plus a small margin.
  * Let the control accept the transport error the way `:112` does, or assert `/deadline/` only under the deterministic seam.
  * Count the connect in cell 2, so a vacuous RST cannot pass.

Dedupe before filing (seat A, 2026-09-16): literal matches over Linear `searchIssues` (archived and comments included), title + description + comments:

* `ssrf-guard`: 7 of 98 results (KS-1160, KS-485, KS-487, KS-678, KS-914, KS-927, KS-931);
* `safeOutboundRequest`: 10 of 10 (KS-1061, KS-1160, KS-485, KS-681, KS-914, KS-927, KS-928, KS-931, KS-932, KS-934).
  None is about DNS-layer classification coverage, the ks932 cells' network dependence, or the armed DNS timer. KS-914 (the rebind pin) is the nearest neighbour and a different defect. Filed new.
