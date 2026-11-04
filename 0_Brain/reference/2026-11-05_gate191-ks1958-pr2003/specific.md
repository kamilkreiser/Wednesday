# Gate 191 commission — Secuura / Blockchain, PR 2003 (KS-1958: a revoked credential verifies as valid when the credential store read fails), TIER 1, ROUND 1 of 2

Written by Wednesday 2026-11-05 07:0x AEDT. Model: Opus (routing v1.0 tier-1 gate: a credential-revocation / verify path). Spark shadow: NOT run (Kam 2026-11-04 16:42 "ignore the spark until further notice").

## What was ruled, so what this PR must be
- The defect (gate 152 G152-F1, `/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate152-ks1868-pr1968/verdict.md` lines 29-38 and 68; ticket KS-1958): in vc-issuer, when this process's memory copy is stale-unrevoked and the DB READ throws, `getById` falls back to memory and the verifier returns verified TRUE for a revoked credential.
- Authority: Wednesday's reading of Kam's fail-closed rulings (cards secuura-auth-lockout-failopen-redis-down-1103 = a, secuura-pr1970-gateway-failopen-1103 = a), reported to Kam on morning card wed-morning-fleet-activity-1105. Gate 152 had said "needs Kam's ruling"; the PR body states that conflict and the availability cost. If you find the fail-closed choice has a consequence the PR body does NOT state (anything beyond "verify reads false while the DB read fails"), that is HOLD-FOR-KAM.
- Accepted design (Wednesday's ANSWER to the seat, 19:32Z): `getById(id, {failClosedOnReadError})`; with the option, DB available and the read THROWS -> a NEW CredentialStoreReadError with a FIXED message (no DB text reaches a public response); without it, unchanged. Only `revocationResolvers.ts:55` passes it; `revoke()` keeps the old read. Boundary 1 (no DB: memory only) unchanged. Boundary 2 (DB healthy, zero rows, then memory) deliberately OUT of scope (the seat measured 0 DELETE/TRUNCATE on vc_credentials_store at the base). The five 'unreadable thrown value' guards must stay byte-equal.

## Questions (tier 1: measure, do not take the READY's word)
1. **Scope:** `git diff --name-only <merge-base> <head>` = the 5 files in the READY; name any other.
2. **Base vs head, the full matrix:** gate 152's scenarios A, B, B-control, C, D x the three thrown shapes (ordinary Error, revoked Proxy, getter-throws message) x both routes that wire revocationVerifierConfig (credentials, presentations). Predicate: any head cell verified TRUE where base was FALSE = a Major. Count it yourself ("N of M"); do not reuse the seat's table.
3. **Leak:** the verify response at head for a failed read: does any DB error text, stack or driver message appear anywhere in the serialized body or headers? Planted distinctive DB error message + a positive control that shows your search finds it in a log or in base's behaviour.
4. **revoke() and the siblings unchanged:** prove `revoke()` with a failing SELECT behaves exactly as at base, and getRecordById / getByHash / getReadableByHash unchanged (diff + one cell each).
5. **Boundary 2 reasoning:** re-measure "0 DELETE/TRUNCATE on vc_credentials_store" at the head (git grep with a positive control); state whether ANY code path can leave a row missing while memory holds it (store()'s failed INSERT is the seat's named case). If you find one, say whether it reopens the fail-open; that is a finding, not a block, unless it is the SAME exploit shape.
6. **Availability cost, measured:** with the DB read failing, an UNREVOKED credential: head verified false (the stated cost). Anything else changed (latency, retries, an exception escaping a route as 500)? An uncaught throw becoming a 500 is a finding.
7. **Red-proof:** reproduce at least 3 of the seat's 4 mutants against the committed bytes (m1 mandatory), plus ONE of your own; name survivors.
8. **Suites:** whole vc-issuer workspace at head (the seat: 758 of 758), tsc incl. tests, eslint on the touched files, docs-fragments check with a planted defect.
9. **Title/body:** title starts "Refs KS-1958:" and is <= 92 chars (count); no close-word before a key; the body carries the authority line, the CONFLICT and the availability cost (read the body via the API).
10. **Merge:** merge-tree of the head onto develop 035685291b9d58ae6ea8ba5f05adf9379f9c2944 (rc + full tree id) for the merge seat.

## Subjects (re-pin yourself at start and end)
- Repo Secuura/Distributed_Secuura; read-only checkout to clone from: `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files` (fetch the PR ref into YOUR clone only; never write to the checkout).
- **PR 2003** head `8b140178276457116714892fe0cf73b9f1e92c8c`, develop `035685291b9d58ae6ea8ba5f05adf9379f9c2944` (Wednesday's ls-remote 07:0x AEDT, 20:0xZ).
- F 31st's READY saved here as `ready_2003_batch.txt` (the second mail in that file; read it whole). The seat's record: `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-11-05_seatF-31st/`.
- Workdir: `/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-05_gate191-ks1958-pr2003/`. Dependencies only from an install matching the lock at the head; never link from the shared checkout's node_modules. DevMASTER ~135 GiB free.
- Live seats: D 52nd (demo deploy, box only), F 31st (wrapping; its PR-B worktree s-f31-ks1986 is NOT yours). Do not touch their worktrees, processes, ports or clusters. No contact with demo or kintsugi.
- NOT TESTED by design unless you do it: Node 24, a real deploy, a real second replica. Say so.

## Verdict
Line 1 per gate_common section 6, for PR 2003, and the merge tree on 035685291b9d for the merge seat. Then FOUND / TESTED / HOW with controls.

