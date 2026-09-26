#1285 KS-766: red-prove the base-image-watch DB-age producer, not only its consumer
head c7779a33031813cac9dab62abd0cb8fd9d73f2f9

## BLUF
`base-image-watch.sh`'s self-test could red on the **consumer** of the DB-age value but not on the
**producer**, so the QA F-5 fix was half-guarded: reverting `decide()`'s future arm reds the suite,
reverting the producer clamp did **not**. The gate would have gone back to printing *"the vulnerability
DB is 0.0h old"* immediately before telling an operator to run the ACR leg against the live registry,
with the suite green throughout.

The age computation was inline `$( python3 -c '...' )` command substitution rather than a callable
unit, so no case could reach it. It is now an isolated function the self-test drives with a synthetic
trivy metadata timestamp, and two cases pair a **future** stamp against a past one.

## Provenance, stated plainly
**The patch was produced by the local model under a Wednesday brief** and checked by her harness. It
is **re-verified independently here**, and every figure below is this seat's own run, not a quoted
harness figure.

## Test Evidence
Base this worktree **CONTAINS**: `00de57baeb40` — **develop's current tip**, with this commit directly
on it (`merge-base --is-ancestor` YES; `git log` shows `c7779a330` on `00de57bae`).

| proof | result |
|---|---|
| `git apply --check` — **strict, no recount, no fuzz** | **rc 0** |
| self-test at the tip, patch NOT applied | **20 PASS / 0 FAIL, rc 0** |
| **the test hunk ALONE** | **rc 12** — 20 PASS / **2 FAIL** |
| all three hunks | **22 PASS / 0 FAIL, rc 0** |

**The red is the point of the ticket, and it names itself.** With only the self-test hunk applied, the
two failures are
`FAIL  a FUTURE UpdatedAt yielded '', not the future sentinel` and
`FAIL  a past UpdatedAt yielded '', not a numeric age` — i.e. the new checks *cannot* pass without the
extraction, which is exactly the coverage the ticket says is missing today. The two PASS lines added by
the full patch are those same two cases:
`PASS  a FUTURE UpdatedAt yields the future sentinel` and
`PASS  a past UpdatedAt yields a numeric age (59040.92h)`.

**Counting note.** The self-test **indents** its result lines, so a line-anchored `grep -c '^PASS'`
returns **0** and reads as "no checks ran". Every figure above is counted unanchored, with the anchored
count kept alongside as a control. An under-count here would look like a broken suite rather than a
broken parser.

**Modes after `git apply`** — restored and asserted, not assumed: the subject and `.githooks/pre-push`
are both executable, index mode `100755`. A rewritten hook silently losing its exec bit is how an
ungated push has happened before.

**Push gate:** `pre_push_hook_base` **28/0**, `fixture_guard` **6/0**, `run_shell_suites` **49/0**,
shell suites **60 passed, 0 failed, 0 skipped (of 60)**. Preflight **12/15 legs ran, 3 SKIPPED
(3, 4, 8 — local stack not up), nothing failed** — not quoted as a pass.

## NOT covered
- **No docker or network run of the real trivy path.** The self-test drives the producer on JSON only.
- `shellcheck` is not installed here.
- Legs 3, 4 and 8 NOT run (no local stack). No database. No deploy.
- The consumer half (`decide()`'s future arm) was already guarded; this PR adds the producer half only.

Refs KS-766

