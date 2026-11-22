GATE B1929: GO WITH FINDINGS @ af26f80 on main 83683af

# B1929, READER 2 (adversarial on D5 and D7 only), lane A1 the sign-in state machine, head af26f801e23b4bc495acf34ee90f265d574ef290

Reader: in-session Opus, READ-ONLY, written 2026-11-22 22:48 AEDT. Scope is D5 (the binding rule) and D7 (the stale-tap guard) only. I write no landing text. The whole lane, the merge, the mutants and the hosted run belong to reader 1 (B1928).

**Main moved after the commission.** At 22:34 Tuesday read `main` = 0fc3344a. My `gh api -X GET` at about 22:45 read `refs/heads/main` = `83683af4be3fb39612153c103f922fc2febf7acc`, which is pull request 22 (lane U). `compare/0fc3344a...83683af4`: ahead 1, 8 files, all under `src|tests/Datasec.Suite.UniversalPrint/Registration/`, none of them a SignIn path. `compare/83683af4...af26f801`: diverged, ahead 1, behind 2. The branch ref still reads `af26f801`. Reader 1 owns the merge question. I only record the move here.

## BOTTOM LINE
- **D5 holds. I found no path that signs a user in on the printer or in the broker when the token's object id or the grant's subject is not the card user's.** `_broker.SignIn` (`SignInActor.cs:390`) and `_held =` (`:400`) are reachable on one straight path, and only after both checks (`:346`, `:352`). The supersede check and `_attempt = null` (`:358-366`) run under one lock and come after both checks. Every probe I aimed at a bypass stayed refused (25 probe cases; 50 x 82 runs green; evidence below).
- **D7 holds as worded.** The age runs from arrival to the turn. The limit edges, future stamps and absurd stamps are all `StaleTap` with 0 lookups. A clock that jumps forward fails safe.
- **Two findings, both LOW, neither blocking.** Both can be fixed forward, and both were shown fixable in my scratch without turning a seat cell red. I also have three informational notes and one plain statement of what the D7 named limit costs.

## FINDINGS
| # | Sev | What | Evidence |
|---|---|---|---|
| R2-1 | LOW | **One throwing `Audit` subscriber hides the refusal from every subscriber after it.** `RaiseAudit` (`SignInActor.cs:411-427`) calls the whole multicast delegate inside one `try`. When an earlier handler throws, the later handlers never run. So a refusal can go unaudited at the real audit sink even though `02:432` says "refused and audited". The refusal itself stands (`BindingRefused`), so this is not a sign-in. Cell B07 passes only because the kit's recorder is subscribed BEFORE the throwing handler (`Kit.cs:21`, then `BindingTests.cs:120`). The drafter's prototype has the same shape (`Audit?.Invoke` inside one try, prototype `SignInActor.cs:438`). Fix forward: call each entry of `GetInvocationList()` inside its own try. | probe P05 (`evidence/ZProbes.cs.txt`), green at head = the subscriber after the thrower sees 0 audits; red under the control fix (`evidence/probes-under-control-fix.log`, `evidence/control-fix.diff.txt`) |
| R2-2 | LOW | **`Guid.Empty` binds.** A card user whose object id is `00000000-0000-0000-0000-000000000000` gets a `SignedIn`, with a session in the broker. That happens when the token object id is also the empty identifier, in any form (D or N). The rule only asks that both parse and are equal. An identity service that falls back to `default(Guid)` when it cannot read a token, paired with a store record whose object id was never filled, passes the binding rule. That needs two upstream defects (C7's) and lets no OTHER real user in. Still, the empty identifier is never a real user's. Fix forward: refuse `Guid.Empty` at `:300` (as `LookupFailed`) and/or at `:346` (as `BindingRefused`). | probes P01, P01b green at head (`SignedIn`, store 1); red under the control fix (`evidence/probes-under-control-fix.log`) |

## INFORMATIONAL (no finding; for the record)
- **I-1 (D5) An early-disposed grant reaches the printer.** An `IdentityGrant` whose `TokenGrant` the identity service disposed before handing it over passes both binding checks. `Subject` stays readable after dispose (`TokenGrant.cs`). So `CompleteSignInAsync` runs, the broker then refuses (`InvalidArgument`, `TokenBroker.cs:78`), and the result is `SessionRefused` with one sign-out, no audit and an empty store. The user shown is the RIGHT user, so there is no identity exposure. But the printer briefly shows a sign-in the broker refuses, which is the very thing D5 (2)'s "check first" was meant to prevent. Possible cheap pre-check, Tuesday's call: refuse before the printer when `GetAccessToken()` throws or is empty. Probe P04 (calls `complete, signout`).
- **I-2 (D5) Forms the rule accepts.** `Guid.TryParse` accepts the N, D, B, P and X forms and surrounding spaces (P02, 4 rows `SignedIn`). Near misses are refused with no printer call: one hex digit off, a trailing NUL, two ids joined, a short group (P02b, 4 rows). A grant wholly for another user (object id and subject both B's) is refused by part 1 before part 2 (P03). A subject that differs only in case is `SessionRefused` (P03b): the asymmetry with the object-id compare is per D5's words and matches the broker's ordinal check. Null is refused at every constructor (`CardUser`, `IdentityGrant`, `TokenGrant`). The empty string is `LookupFailed` (user, A06) or `BindingRefused` (token, B02).
- **I-3 (D5) Races and retries.**
  - A late lookup answer of ANOTHER user after a time-out is never used, and the next tap looks up afresh (P07). Lookups have no `abandon` and no cache.
  - A handler that taps again from inside the audit cannot bypass the rule: the refusal stands and the inner tap runs its own lookup, acquire and binding (P06).
  - The supersede raced against the acquire's answer (P08, 40 races per run x 50 runs = 2000) always gave one of the two legal D8 orders: either the first is `Superseded` and B signs in once, or the first passes the lock and B then switches with `complete, signout, complete`. Every grant was disposed, the store held 1, and no third shape appeared.
  - One run of an earlier, stricter P08 failed. That probe assumed only the first order, so the defect was in my probe, not the product (`evidence/loop20-run7-P08-probe-defect.log`). I corrected the probe to the two D8 orders and re-ran it 50 of 50 (`evidence/loop50.log`).

## D7, ATTACKED
- **Edges and stamps:**
  - The limit minus 1 tick, the limit and the limit plus 1 tick are covered by S01; a 1-tick future stamp by S02.
  - Age 0 is taken (P12).
  - `long.MinValue`, `long.MaxValue`, 0 and -1 are all `StaleTap` with 0 lookups (P09, 4 rows). I found no overflow that makes a stale tap look young: the unchecked subtraction in `GetElapsedTime` wraps those stamps to negative or very large ages, and both are refused.
- **A tap queued behind a slow step:** `StaleTap` once its arrival age reaches the limit at its turn (S03, P12). Such a tap is not reported to the printer (choice (c) of the seat), so the person who tapped sees nothing.
- **A clock that jumps forward (3 h during an acquire):** `TimedOut` at once, the late grant is disposed and nothing is kept (P11). A backward jump makes the age negative, which is `StaleTap`: it fails safe by reading `:235`, and S02 covers it. Whether the host's real monotonic clock advances across a host suspend is UNMEASURED.
- **I-4 (D7) The age is checked ONCE, at the start of the turn, and the steps after it are bounded only by `StepTimeout`.** A tap taken at age 5 s minus 1 tick, followed by a 29 s lookup, a 29 s acquire and a 29 s printer step, still ends `SignedIn` more than 90 s after it arrived (P10). With a switch's sign-out step added, the worst case is about `MaxTapAge + 4 x StepTimeout`, which is 125 s at the defaults (DERIVED from `:234-235` and the four `StepAsync` calls on the path). This conforms to D7 ("At the tap's turn"). But `MaxTapAge` bounds the queue wait, not the time until the tap takes effect, and the README's `## Limits` does not say so. FOR-RECORDS item 3.

## WHAT THE NAMED LIMIT COSTS (a re-delivered tap after an outage), plainly
A tap the printer re-delivers after a server outage arrives with a fresh stamp. The actor treats it as a new tap and acts on it in full: no guard of this library can tell it apart (probe P13, DERIVED from `:232-238`). The binding rule still holds, so it can only sign in the CARD'S OWN user, never anyone else. What it can do:
1. **Nobody signed in:** it signs the card's user in on the printer when that person may already have walked away. Their session then stays open on an unattended printer until the printer's own inactivity or the broker's idle timeout (30 min by default). Anyone who walks up acts as that user, for example releasing their print jobs or scanning to their mail.
2. **Another user at the printer:** it SWITCHES. The person standing there is signed out, and the absent card user is signed in in front of them (P13: `SignedIn`, `EndedPrevious` true, the details are user A's). This is the sharpest cost: one user's session handed to another person.
3. **The same user signed in again since the outage:** the stale re-delivery of the same card signs them OUT (path a) mid-task.

Whether and how a printer re-delivers is UNMEASURED (spike S1). The adapters' read-sequence guard (pull request 13) may catch some of it; that is UNMEASURED for this path.

## WHAT I RAN (all in my scratch clone `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s311/g1929/clone`)
- **The clone:** made by `git clone --no-local` of the seat's clone at `af26f801`, push URL `invalid://no-push`. The branch ref was confirmed by `gh api -X GET matching-refs/heads/b1914` (one row, `af26f801...`).
- **The tools:** `gate/` copied by `cp -Rc`, 7 of 7 sha256 equal to THE TOOLS.
- **Heavy jobs, all through `heavy.py`, one at a time:**
  - restore, locked, `CI=true`: rc 0;
  - builds: rc 0, `0 Warning(s)`, `0 Error(s)` (build1 rc 1 on an analyzer rule `xUnit1051` in my probe file, fixed);
  - probes at head: `Total: 82, Failed: 0` (57 seat cases + 25 probe cases);
  - control fix: `Total: 82, Failed: 3`, exactly P01, P01b and P05;
  - undo by `cp` from the saved original (sha256 `bd4e7b13...`, equal to the seat's), proved by `cmp`;
  - loop20: 19 of 20 (the P08 defect in my probe, above);
  - the corrected probe file (sha256 `af53e319...`), loop50: `LOOP: 50 of 50 passed, 0 failed`.
- **Not run by me:** the whole solution, the mutants, the hosted run and the merge (reader 1's).
- **Nothing written outside my two folders.** My probe file lives in my scratch clone only and is never committed or pushed.
