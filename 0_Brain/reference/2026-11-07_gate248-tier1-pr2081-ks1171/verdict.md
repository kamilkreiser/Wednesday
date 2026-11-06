# Gate 248, tier 1, round 1 of 2: verdicts

| PR | Ticket | Head | Verdict |
|---|---|---|---|
| 2081 | KS-1171 8k | 17c453253d68206d9d3fcbb723a7ffc9d9291a3d | **GO WITH NOTES** |
| 2085 | KS-2074 | 4d4726ca41d99d5eab8c4a5a27b3a4317917beb8 | **GO WITH NOTES** |

A GO is a statement about these SHAs only. Neither verdict covers a deploy.

Origin readings, by ls-remote (develop / 2081 / 2085 / 2066):
- Start, 20:25:16Z: b27f5fb30f4a / 17c453253d68 / 4d4726ca41d9 / baf577c78e7f
- End, 20:56:51Z: the same four. Nothing moved.

Evidence words on any finding that recommends an action: MEASURED AT RUNTIME, PROBED, READ ONLY. Logs and probe sources are in /private/tmp/g248/logs and /private/tmp/g248/tools.

---

# PR 2081, KS-1171 8k (anchoring)

## Chain cost, stated first (ask 3)

**A wrong answer here can be irreversible.** A false ABSENT lets guard 3 schedule the ordinary retry, which is a second fee-paying Cardano transaction. Its fee and its on-chain record cannot be undone.

**This PR cannot add that outcome.** Real poller and real `definitelyAbsent`, every attempt sequence of length 1 to 5 over {404, no client, throw, found}, 1,364 sequences, at develop and at the head:
- Head absent where develop was not: **0**.
- Develop absent where head is not: 268, every one containing a no-client attempt.
- Sequences with no no-client attempt that differ in any field read: **0 of 363**. `confirmed` differs in 0 of 1,364.

The failure direction this PR adds is a row resting, which the reconciler can still settle. MEASURED AT RUNTIME (probe `g248-prop.test.ts`, stubbed `getTransaction`).

**The deploy hold.** The PR body says it, three times: line 29 "does NOT go out without Kam's word (the card's option text)", the card detail quoted at line 33, and line 98. The card text matches `decision_queue.sh show`. The ticket comment says it too. This verdict does not cover that word.

## BLUF

The change does what card b and Wednesday's design ANSWER say, and nothing I could find beyond that. Red proof, whole suite, sampled tampers and my own plants all held. No finding here blocks a merge. F1 and F2 are real but are not caused by this PR; both need routing, and F1 may need Kam.

## What was tested against what

| Attack | FAIL condition stated first | Result |
|---|---|---|
| Red proof at develop b27f5fb30f4a (0 anchoring files moved since c5c26b2835df) | a RED cell passes, or reds by crash | 13 of 13 RED by AssertionError, 15 of 15 controls pass |
| Whole anchoring at head | anything but the one known red | 855 of 856, 63 files |
| Same at develop, compared by name | a cell lost or changed | 827 of 828, 62 files; 0 lost, 0 changed, 28 added |
| Trial merge with develop (tree 61b315f8397d) | a cell changes | 855 of 856, 0 changed against the head; 8k cells pass |
| tsc, eslint, docs check on the merge | non-zero rc | tsc rc 0 at head and merge; eslint rc 0 on 4 files (a planted defect in the 2085 run gave rc 1); docs OK |
| Other callers moved | reconciler, `lookup`, `txInfo` read differently | C3, C6, C7 hold; my plant P3 widening the reconciler reds C6 |

All of these ran on Node v26.8.1, as the seat's did.

## Ask 1: does the second commit change what the tampers prove? No.

- `vi.setConfig({ testTimeout: 60_000 })` can only change a red that was a timeout. I parsed the seat's 16 tamper JSONs: every red is an assertion or an error, **0 timeouts**. So no tamper's result depended on the old limit.
- The vitest config sets no `isolate` override, so the call does not reach other files (READ ONLY); the by-name compare of the whole suite found 0 changed (MEASURED).
- Six seat tampers re-run at the head. Red counts equal the seat's table: provider-no-client-null 7, poller-loose-test 6, rule-reads-polled 3, voiding-rule 2, boundary-exclusive 3, poller-last-answered-moves 2. Each anchor asserted once, all files restored, 62 of 62 clean before and after.
- Seven plants of mine:

| Plant | Result |
|---|---|
| P1 `pollMember` reads `polled` | 8k-3 red |
| P2 only the first attempt counts as no client | 8 red, 8k-1 and 8k-4 among them |
| P3 reconciler widened | C6 red |
| P4 provider normalises undefined to null | 8k-9 red |
| P7 subtract one, not the count | B5 among 2 red |
| P5 an empty body is not an answer | survives, 0 red; the seat disclosed this ("No cell pins that"); see F1 |
| P6 a found transaction does not move `lastAnswered*` | survives, 0 red; no reader on the confirmed path by read, so a gap with no consequence today |

The seat's own control for the limit (the planted 6 s delay, 26 versus 28) was not re-run.

## Ask 2: is the threadTokenMint red unrelated? Yes to this PR. See F2 for why "known" is not the end of it.

- At develop and at the head, same cell, same message, "Could not serialize the data: Error: Unsupported type". 2 of 2 alone in each tree; once more each in the whole suite.
- The cell imports only `@lucid-evolution/*`. None of the PR's three product files is in its import graph (READ ONLY).

## Findings

**F1. Medium. Pre-existing, not caused by this PR. Needs routing; may need Kam's ruling.** `services/anchoring/src/cardano/confirmation.ts:94-103`. With a **configured** client, a 200 or 204 whose body is empty or JSON `null` counts as the chain answering, and reads ABSENT.
- FOUND: the real blockfrost-js 6.1.1 on a loopback listener returns `''` for an empty 200 and a 204, `null` for a body of `null`, and `{}` for a body of `{}`. This also confirms the seat's by-read claim about got. HTML on a 200 throws; a 404 and a 502 throw with their status.
- TESTED: real provider and real poller on the production schedule, at develop and at the head, with `txs` resolving each body. `''` and `null`: `polled` 30, `definitelyAbsent` **true**. `{}`: `confirmed` **true** with no block hash.
- WHY IT MATTERS: the code's own comment defines an answer as "the transaction or not found". An empty 200 is neither, and this is the same second-fee harm as 8k, on the configuration that really pays fees, where 8k itself has no route. The PR's sentence "An empty 200 is '', so it still counts as an answer, as it does today" is true, but no reader would learn from it that it reaches guard 3.
- LIKELIHOOD: low; it needs an upstream or proxy answering 2xx with no body. Not seen in service; no box was read.
- Evidence: MEASURED AT RUNTIME for the client and the poller result; guard 3's retry from this input follows from cell C1's path and was not driven end to end. Probes: `tools/bf.cjs`, `g248-empty.test.ts`.
- Fix shape, for the owner: decide whether the poller counts only `null` and a real transaction as answers, and pin it. That touches Kam's 09-25 definition of "answered", so whether to do it is his call.

**F2. Medium, unconfirmed. Not caused by this PR. Route it.** The known red has a measured cause, and the product has the same shape.
- FOUND: `lucid.Constr` comes from one copy of `@lucid-evolution/plutus` (0.1.31) and `applyParamsToScript` serialises with another (0.1.33 here). `l.Constr === p.Constr` is **false**; the same call with the other copy's `Constr` succeeds (MEASURED, `logs/lucid.json`).
- `services/anchoring/src/cardano/threadTokenMint.ts:92` and :267-269 and the `applyParamsToScript` call below them use the same pairing, so the real thread-token mint may throw the same error. The failing line is before signing, so by read no fee is at risk.
- The image installs from the service's own `services/anchoring/package-lock.json`, which also splits plutus (0.1.31 and 0.1.36) (READ ONLY).
- NOT measured: the mint on any image or box, with any key. I did not read KS-562 (no Linear access in this gate), so it may already say this.
- Also: this cell **goes green if the blueprint is absent** (`console.warn` and `return`). My own first run read 856 of 856 for exactly that reason; see Conduct. Same for a failed lucid import. Fix shape: a missing blueprint fails the cell.

**F3. Low. PR body line 95** puts in quotation marks, as card `secuura-ks1171-when-is-an-anchor-absent` = c, the words "absent only after 2 answered polls and an answer at least 60 s after the node's 400". The card's option text is "Both conditions (strictest, fewest double submissions)". The quoted words are the BLUF of the later card, not Kam's. Substance is right; the quotation is not.

**F4. Low. PR body line 64**, "so the count today is 0 rows", is an inference from the routes, stated as a count. No box or table was read. My read of the routes agrees: `blockfrost` has one assignment, `initProvider`; `initCardano` has one caller; DEMO_MODE returns before it and its mock never throws, so guard 3 cannot fire. The word "count" is what overstates it.

**Note for Kam, not a defect.** The design (Option A, a no-client attempt counts toward neither condition in a mixed window) is **Wednesday's**, under the 10-27 design grant, not Kam's card. It touches two more files than the card's "touches the re-poll only"; the body says so plainly at line 35. Behaviour stayed inside the re-poll as far as I could break it. By read, a mixed window cannot occur in production, and the whole fix guards a route with no reach today. The body says that too, and it is the premise of option c, so Kam can still weigh it.

**Note for later PRs.** Controls C5 and C7 pin literal lines of `index.ts`, the file KS 2045 and KS 2046 will edit. They will red there if those lines move, by design.

## PR body and ticket comment

Read at line level, against code and my own runs. Everything else I could check holds: every count at lines 73-76 and 81, the 14 commits and 78 files, 0 anchoring and 0 lock files moved, two `packages/shared` files moved, DEMO_MODE and the compose default, `submitAnchor` and `submitTransaction` throwing, the `error` text having 0 readers. Exceptions are F3 and F4.

## Merge

Merge-tree on develop rc 0. No path shared with 2085. Merge order between the two is free. Open PRs outside this batch: not enumerated by me (git fetch only); the seat's `evidence/open_prs_anchoring.txt` was not re-derived.

## NOT tested

A real Blockfrost, a real node, a real unreachable chain; any box, image or gateway path; the four platform suites; hook legs; Node 24; 10 of the seat's 16 tampers; the seat's 6 s delay control; its committed-nowhere DEMO_MODE probe (I walked that path by read only); the live PR body and live ticket comment as GitHub and Linear hold them (I read the seat's local copies; `pr_record.json`'s `body_sha1` matches the local body with its trailing newline stripped, which ties the file to the seat's record, not to what is live now); residue search lines against Linear.

---

# PR 2085, KS-2074 (security)

## BLUF

The refusal does what the PR says, on every door I could enumerate, and on the stubbed store I could not get an acknowledged-and-lost write out of it. No regression found. Two of its client-read sentences are false, one because a test cell is blind. The rulings are Wednesday's and go beyond Kam's card, as the PR itself states.

## Kam's scope

Card `secuura-ks888-revoke-validate-on-failed-save` = a rules "Revoke: 503 + keep in-memory revoke" for a save that failed. **What this PR adds is wider than the card:** a skipped save read as a failed one, the mint, the rotate, and the uncached revoke's 404 to 503 are all **Wednesday's rulings or readings, not Kam's.** The PR says this honestly at lines 44-48. Whether he reads a skipped save as a failed one is unmeasured. The body names the deploy as owed and demo as frozen; unlike 2081 it does not say a deploy waits for Kam's word, and nothing commissioned here says it must.

## Doors, enumerated from the code

Every writer of a key: `dbSaveApiKey` (2 callers, both pass `rethrow`), `saveKeyAndRetirePriors` (1). Routes: `POST /api/keys`, `DELETE /api/keys/:id`. Validate's two memory writes do not persist. `PUT /api/keys/admin-scopes/:userId` already answers 503 with the flag down.

| Attack | FAIL condition stated first | Result, MEASURED on the stubbed store |
|---|---|---|
| Red proof, base route and config | a RED passes, or reds by crash | 21 of 38 by AssertionError, 17 pass, matching the seat's list |
| Whole security unit, no URL and with one exported | any red | 552 of 552, both |
| Repeat revoke in the race, three times | any 200 | 503, 503, 503, 0 writes |
| No token / wrong role / bad body / not JSON / foreign mint / foreign cached revoke | 503 before these | 401 / 403 / 400 / 400 / 403 / 403, and the key stays active |
| Hostile ids: NUL, traversal, 4,000 chars, SQL, emoji | a crash or a write | 503 each, 0 writes |
| `connectorId` without rotate; rotate with a grace window | a key issued, or the prior retired | 503, 503; prior unchanged, still valid |
| State D: validate holds its read, revoke refused meanwhile | `valid:true` | `Key revoked`, then and after |
| Refused rotate, then recovery, then retry | lost or double retire | 503, then 201, count 1, prior row false |
| Mint with the flag flipping mid-request (the wrong-tenant harm the PR cites) | an await between the skipped lookup and the save | none on a platform mint; no `await` from the skipped lookup to the save except a scoped admin's scope read, which is flag-gated (READ ONLY). Attack failed. |

Sampled seat tampers: T01 12 red, T04 4, T07 8, T09 2, each equal in count to its declared set, the named cells I checked among them. Nine plants of mine: seven red as declared, two survived, G1 and G5. Anchor asserted, bytes restored, 38 of 38 before and after.

**Who loses access.** During a boot race: anyone minting, rotating or revoking. Gateway register-connector answers 502 (`platform.ts:849`, READ). Tenant provisioning stays 201 with a null metering key (`meteringKey.ts:52`, `index.ts:329`, READ). Admin UI through the proxy sees the failure. Those are the only three callers my search of services, scripts, deploy, docker, connectors, admin and packages found. Validate is unaffected (`auth.ts:288`, `internal.ts:43`). **One to know:** with a URL set and a database that stays unreachable, the refusal lasts as long as the outage, not 30 s; memory no longer stands in. Line 50's "at most 30 s" is about a database that could have taken the write, so it is true, but that is the larger case and no stack was read for it. A whitespace-only `DATABASE_URL` also reads as configured and refuses (503, MEASURED); db.ts treats it the same way.

## Findings

**G1. Minor. PR body line 11 is false for the mint, because cell LOG is blind there.** `ks2074-boot-race-writes-are-refused.test.ts`, the LOG cells.
- The body says "Cell LOG pins that no key and no hash reach a log on the refused mint and revoke". The cell looks only for the **warmed** key and its hash, `KEY` and `hashOf(KEY)`. A refused mint has a different, freshly generated key.
- TESTED: I planted `plantedKey: keyValue, plantedHash: keyHash` in the refused mint's log line. Under the same spies the log **does** carry the full minted key and hash (`mintedKeyInLog: true`, `mintedHashInLog: true`), and LOG-C and LOG-D **stay green**, on 3 separate runs. The hash-only plant also stayed green.
- The product is clean: unplanted, both read false. This is a guard pointing the wrong way, not a leak. MEASURED AT RUNTIME.
- Fix shape: assert the mint's log text has no `sk_` followed by 64 hex and no 64-hex hash, with the same spies. Regression test: this plant must red it.

**G2. Medium as a behaviour, pre-existing; the sentence is the PR's.** `services/security/src/index.ts`, `dbGetApiKey`'s catch (about :607) with `if (!apiKey)` at :1670. PR body line 27, "A database lost later leaves the flag up and already reached the 503", is false for an uncached revoke.
- TESTED: flag up, URL set, stored read throwing, key not in memory: **404 `API key not found`**. Control: the same fault with the key cached and a failing save answers 503. MEASURED on the stubbed store (`probe2085.json`, PR1, PR2).
- That is exactly what the coordinator's ruling at line 48 says must not happen: "an operator revoking a compromised key must not be told it does not exist". `dbGetApiKey`'s catch falls to memory and this PR does not touch it, so develop answers the same by read. No cell pins it: A-404 is a key with no row and a read that works.
- The seat listed it as candidate 2 in its READY to Wednesday; it is not in the PR body, which a client reads.
- Recommendation: correct the sentence; route the behaviour. Evidence: MEASURED AT RUNTIME on a stub; the real driver's error was not used.

**G3. Low. PR body line 59**, "5 in 30 s opens it for 60 s". The breaker counts 5 **consecutive** failures with no time window (`circuit-breaker.ts:20,206-215`). The 30 s comes from a stale comment at `proxy.ts:62`. READ ONLY.

**G4. Low. PR body line 36**, "400, then 403, then 503". A foreign admin revoking a key not in memory gets **503**, not 403: the key's tenant cannot be judged yet (MEASURED, PR4). It was 404 on develop by read, so it gives away no more about the key. The role-level 403 still comes first.

**G5. Info.** The comment at `dbSaveApiKey` says the refusal sits after the memory write "on purpose", so a revoke keeps its copy. Moving it before the write reds 0 of 38. With the flag down `dbGetApiKey` hands the route the map's own object, so the copy is already revoked by read, and the mint's catch deletes it anyway. The line order is not load-bearing and no cell could tell.

**G6. Low, could not resolve.** Body line 80 says "14 open PRs into develop", and line 81 quotes the push driver's "40 open PRs". They look like different moments, the seat's earlier overlap read (`evidence/overlap_boot.out`) and the push driver's at push time, but the body does not say so, and a client reads both. I did not count open PRs.

## Merge, including the grant

- **PR 2066 at baf577c78e7f: merge-tree rc 0, tree 284e3322c0e5**, equal to the seat's. Its only shared path with this PR is `services/security/src/index.ts`. The grant's exact name equals the branch at that head: `feature/ks-2032-security-a-demoted-deleted-or-gone-user-whose-token-still`. On that merged tree: security unit 571 of 571, tsc rc 0. 2066's integration suites were not run.
- Develop b27f5fb30f4a: merge-tree rc 0; security unit 552 of 552; docs OK; eslint rc 0, 2 warnings.
- PR 2081: rc 0, no shared path. Merge order free among the three.
- The seat's other merge-trees (KS 1152, KS 2063, PR 2071) were not re-run.
- A `fragment_modified` declaration is owed at merge for the KS 1377 flow fragment; the edit is in the diff, and the coordinator's grant was read in the body, not in its mail.

## Other PR body sentences

Checked and true: the state table against my runs, the 6 files and +682 -4, one commit, the callers, the `closeDb` and probe claims, 552 of 552 both ways, the red list. Exceptions: G1, G2, G3, G4, G6. The ticket comment read clean against the same runs.

## NOT tested

Integration suites, and the seat's real-row scratch run; any real PostgreSQL, relay, real flag flip or pgbouncer; a live stack, and the callers against a live service; four platform suites; hook legs; Node 24; any box; 25 of the seat's 29 tampers; the live PR body and comment, as for 2081; the KS-2074 state move the seat reports; candidates 1, 3, 4, 5 in its READY.

---

# My own conduct

- **Retraction.** My first whole-anchoring run read **856 of 856**, against the seat's 855. It was my error: my sparse checkout left out `contracts/secuura`, so the cell took its skip branch and returned green. I saw the 2 of 2 passes in a bang-path experiment, found the blueprint missing, added it, and re-ran. All figures above are the corrected runs. The 856 figure is void. It did yield half of F2.
- A first security run read 536 of 540 because that sparse checkout also lacked migrations and docs. Full checkout: 552 of 552. Void as well.
- An eslint run with an absolute path printed "File ignored because outside of base path", so it measured nothing. Re-run with the working directory set by a Python subprocess, with a planted control. Only the re-run is cited.
- **Rules.** No `cd`. No `rm`. No post, no box, no docker, no chain. The one correction in the commission decides against the common file: **clone left in place at /private/tmp/g248, 18 GiB by `du`**. Most of that is APFS clones sharing blocks; boot-volume free space moved about 6 GiB across the session, with other seats live.
- **Network, one to weigh.** Git fetch and ls-remote only, as ruled. The Blockfrost probe used a listener on 127.0.0.1 in my own process, no outside host. "Network only for git fetch" did not name loopback; I judged it not network and say so here. `gh` and Linear were not used, which is why live bodies are unread.
- **Reads outside my folder, no writes:** node_modules cloned from /private/tmp/g245 and copied from the seat's `worktrees/s-aa5-base`. Three probe merge commits exist as objects in my clone only, no refs, never pushed. All probes and tampers ran on copies inside the clone; worktrees read clean at the end.
- **Hooks.** `pretooluse_no_cd.sh` refused `git -C $G` write verbs twice, because the variable hid the path. I re-ran them with the literal /private/tmp/g248 path, which it allowed; that is my own clone, the place the commission sends me. A slow `git grep` on the blobless clone was stopped and replaced by a sparse worktree.
- Load stayed under 8 (peak read 7.38). The session's result file for that command sits in the harness's scratchpad, outside my gate folder, by the tool's own doing.
- I read the charter as well as the template. The charter's "environment confirmed with a human" is carried by Wednesday's commission; no running target was used.
- Severity is mine. Priority is not.
