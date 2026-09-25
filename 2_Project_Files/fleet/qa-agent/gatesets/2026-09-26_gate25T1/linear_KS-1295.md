KS-1295 vc-issuer credentialRepo.store() falls back to memory SILENTLY when the database is unavailable — the caller is told it was stored
state In Progress

## BLUF

`credentialRepo.store()` **in vc-issuer writes to the in-memory map and returns SILENTLY when the database is unavailable.** The caller is told the credential was stored. Nothing is logged, so there is no artefact anywhere that the write did not reach PostgreSQL — and on restart the credential is simply gone.

**Pre-existing, and deliberately NOT counted against PR #1231** (merged 2026-09-25 as `b83f986fd3e4`). That PR made the *table-absent* fallback LOUD — two WARNs per store. **This is the sibling path it did not touch:** `store()` then `if (!isDbAvailable()) return;` with no log at all. Raised by the tier-2b QA gate as **P-1** and ruled by the coordinator to be tracked separately rather than folded into #1231's scope.

## Why it matters, stated without overclaiming

A silent success on a durability-critical write is the failure mode that cannot be investigated after the fact: there is no line to grep, no counter, no artefact. The credential is served from memory for the life of the process and then disappears. Every other symptom (a verifier 404, a revoke that finds nothing) surfaces far from the cause.

**What is NOT claimed here:** that this is currently happening in any deployed environment. It is a code path, found by reading, with the trigger condition (`isDbAvailable()` false) unmeasured in Azure or on kintsugi.

## UNMEASURED — stated rather than glossed

Carried verbatim from the gate's findings on #1231, because they bound what this ticket knows:

* **Azure reach UNMEASURED.** Whether this path is reachable in the deployed environment was not measured; the Azure role and the table's state were not read.
* **The least-privilege SELECT is UNMEASURED.** Whether the runtime role can even perform the existence check that gates the fallback is unknown.
* The **kintsugi log observation** owed against KS-1281 would, if done, also say whether the loud sibling path fires there. That observation has not been made.

So the *severity* of this ticket rests on an unmeasured reach. **Measure the reach before choosing a fix shape** — if the path is unreachable in every deployed environment, a log line is the whole fix; if it is reachable, the question is whether a silent memory write is acceptable at all for credentials.

## Fix shapes, not chosen here

1. **Log it** — match what #1231 did for the table-absent path: a WARN naming the credential id and the reason. Smallest change; makes the event investigable.
2. **Refuse it** — treat a store with no database as an error the caller must handle, rather than a success. Correct if credentials must be durable, and a behaviour change that needs its own decision.

(1) is strictly an improvement and does not foreclose (2).

## Board search before filing (team Secuura-PK, 1,284 issues incl. archived, 3,620 comments, literal match on titles, descriptions and comments)

* `isDbAvailable` -> 14 total / 7 open (KS-1120, KS-1018, KS-953, KS-871, KS-851, KS-843, KS-577). Read for overlap; all concern other services or other call sites.
* `credentialRepo` -> 7 total / 5 open. The two nearest were read in full and are **NOT** duplicates: **KS-1121** is `getById` resolving by SUBSTRING (a disclosure defect, different function); **KS-1120** is presentations test-coverage gaps from #966.
* `vc_credentials_store` -> 3 total / 2 open (KS-1281, KS-1121). `services/vc-issuer` -> 30 total / 14 open. `memory fallback` -> 13 total / 5 open, none on this path. `falls back to memory` -> 0.
* Controls that fire: `KS-1281` -> 1; `consumeResetToken` -> 2. So the search discriminates.

## Provenance

Tier-2b QA gate `2026-09-25-batch1225-t2-r1` on PR #1231, finding **P-1**, at head `bd1d2daec2bf`. Filed at the merge of #1231 onto `develop` `b83f986fd3e47b66054d23a350e5aef6d80d0550`, on the coordinator's instruction. `Refs KS-1281`; it does not close it.
