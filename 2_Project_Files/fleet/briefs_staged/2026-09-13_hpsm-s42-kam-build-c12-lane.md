# KAM RULED build-c12: commission a new lane for engine C12 mapping plus fenced synthetic adapter rows

**BLUF.** **For session 42 (seat hpsm-3e04).**
- **Kam, on Tuesday's panel tab, card tap, 2026-09-13 14:04:45 AEST, verbatim:** *"Decision hpsm-composer-demo-release-unreachable-c12: build-c12 — Commission engine C12 mapping plus fenced synthetic adapter rows now (new lane, may not land by Monday)"*.
- **Tuesday had recommended `proofread-drafts`. Kam chose `build-c12`. This mail is the commission.**
- **Nothing here pauses S40's switch-on or lane R's proofreading fixes.** The new lane runs in parallel under Kam's standing rule.

1. **New lane C12: `packages/engine` + `content/release-demo`**, plus `packages/db` content registration ONLY if C12 rows need it (lane G is merged, so that path is free).
   - It is disjoint from Q (`apps/api`), W (`apps/web`) and R (`packages/renderers`).
   - It merges through you with the usual chain: seat checks, the upgrade proof from `7135dec`, then clean-clone CI.
2. **Engine.** `contentFromBundle` today refuses rows in `hpsm_adapter_metadata` (C12), `baseline_values` and `device_capabilities`.
   - **Map C12.**
   - **Map the other two ONLY if a measurement shows release needs them.** Name that measurement in the READY.
   - **RED-first with mutants:**
     - well-formed C12 rows are accepted, and malformed ones are still refused;
     - on real content (`release-draft`, C12 empty) UNSUPPORTED_HPSM_VERSION is **unchanged**;
     - on the demo release, with the switch ON and a synthetic tenant targeting a synthetic supported version, UNSUPPORTED_HPSM_VERSION clears.
3. **Fences. Kam's synthetic-content ruling is still in force in full:**
   - adapter rows live in `content/release-demo` ONLY, and every row carries SYNTHETIC `source_refs`, citing *"synthetic demo fixture, Kam ruling 14:04:45"*;
   - **`release-draft` stays byte-identical** (`content:check` hash unchanged);
   - **no invented real-HP facts:** a synthetic supported-version list is never presented as HP's real support matrix, and every output that shows it carries the SYNTHETIC mark;
   - a real tenant still can never take synthetic content (lane G's DB guard and lane E's 422 unchanged, re-run as regression).
4. **Measure honestly, and never force a release.** After C12, list EVERY remaining release blocker on the demo, measured on a seat stack. At the ON proof those were: EXCEPTION_REQUIRED ×24, technical review, customer approval, material exceptions.
   - **Do NOT write exceptions, approvals or reviews into content or fixtures to make release pass.**
   - If release is reachable through the product's own workflow (a consultant records exceptions and approvals in the UI or API), prove it on a seat stack and open the released Preview. It must be marked "Not signed" and SYNTHETIC, with no approved-manifest claim unless lane R's truth table allows it.
   - **If it is not reachable, report exactly what remains.** A content decision goes to Tuesday, who puts it on a card for Kam.
5. **Live stacks.** C12 reaches `pc-lane-a` and Azure only at a later upgrade, after the merge.
   - The upgrade message to S40 names the new demo `CONTENT_HASH` (migrate registers a new synthetic release) and any new env (none expected).
   - The D1 and object-store checks stay at the top of that message.
6. **Kam's own framing: "may not land by Monday".** Do not cut a fence or a check to make Monday. **The priority order for merges:**
   1. S40's switch-on (running);
   2. lane R (proofreading fixes);
   3. lane C12;
   4. Q and W.
   The lanes build in parallel; you sequence the merges.
7. **New gate targets:**
   - the C12 mapping;
   - the synthetic adapter fences;
   - `release-draft` unchanged;
   - the honest-blocker list;
   - no fabricated approvals.

## RULED BY KAM, NOT YET IN AN ARTEFACT
- **`hpsm-composer-demo-release-unreachable-c12` → `build-c12`** (card tap 14:04:45 AEST, verbatim above). It lands in lane C12's brief and your seat history record.
- **`hpsm-composer-synthetic-demo-content-for-monday` → `demo-content`** (11:19:24 AEST): still in force; the fences above are its fences.
- **`hpsm-credential-bearing-prd-outside-every-snapshot` → structural-look** (2026-09-09). A BACKLOG item. **Not this commission's work.**

## Unchanged
- No push. Switch state as S40 reports. A combined tier-1 gate is due before any push. Lanes G (merged), Q, W and R stand as confirmed.

PROVENANCE:
Kam's build-c12 ruling verbatim | panel relay mail "[Kam -> Tuesday] panel message 2026-09-13T14:04:45.261476+10:00" + 0_Brain/dashboard/data/chat_kam.json row at that ts (view tuesday), read by Tuesday s11 | read 2026-09-13
contentFromBundle refuses C12, baseline_values and device_capabilities rows | S41 lane F mail 2026-09-13T02:16:35Z, read whole by Tuesday s11 | read 2026-09-13
ON-proof blockers UNSUPPORTED_HPSM_VERSION + EXCEPTION_REQUIRED x24 + release terms false | S42 STATUS mail 2026-09-13T04:02:55Z read whole + on-proof evidence files present (qa-s42/on-proof/), checked by Tuesday s11 | read 2026-09-13
main 7135dec with lane G merged | git rev-parse + merge-base in Datasec/HPSM 6_Policy_Composer, run by Tuesday s11 14:01 | read 2026-09-13

SELF-CHECK: re-read end-to-end for contradictions | 2026-09-13 14:07

Tuesday
