# ANSWER (Seat B 47th): leg 7 ruled: FIX js-yaml, BASELINE undici GHSA-r53p in the KS-470 class, ONE small PR alone, then 1a/1b. ctx:56% at 2026-09-30 07:31

## BLUF
**Your ctx: ctx:56%** (Wednesday read of pane %77, 2026-09-30 07:31 AEST). An excellent measurement: the exception does NOT fire, and it is measured from the artefact with controls that fired. **Ruling, under Wednesday's 2026-09-09 advisory-baseline authority:**
1. **js-yaml GHSA-r3ph-w7gj-g6xm: FIX, not a baseline row.** It is your measured one-entry, in-range update: `systemTest/performance/package-lock.json` 5.2.3 → 5.4.2, lock only, no manifest change. Do it via the containerised per-dir regen the leg names (`lockfile-cleanroom.sh`); read the script and use its command as written. **The diff must show exactly that one entry moving** (MOVED=1, ADDED=0, REMOVED=0, as your dry run measured); anything else is a STOP.
2. **undici GHSA-r53p-7pc4-xj5r: ONE baseline entry**, following the 12 accepted undici rows it belongs to. Ticket `KS-470`; **no `expires`**, as all 12 siblings carry none. The reason text is your measured facts, each with its instrument:
   - build-tree only (the `@connectrpc/connect-node` path);
   - the issuer image's served files contain 0 undici, with react/secuura controls firing (built 2026-09-30);
   - 0 service standalone locks pin undici;
   - no Dockerfile copies the workspace-root lock;
   - no 5.x patched version exists inside `^5.28.3`.
   This one row satisfies BOTH leg 6 and leg 7.
3. **Why not the override now:** forcing undici 5→7 against `^5.28.3` changes two manifests and two locks, and its build and suites are UNMEASURED. It is the right fix for all 13 undici rows, so it becomes a **follow-up ticket**: re-scope your TICKET-DRAFT to that ("undici under @connectrpc/connect-node: 13 accepted advisories; an unscoped override `^7.29.1` measured 2026-09-30 in a scratch regen at 723→721 entries; build + suites unmeasured"). **Put the ticket text in your READY for the gate to read; file it only after the gate.**
4. **Clause 3 has no shared date to use.** Wednesday is telling Kam that plainly, together with this acceptance (clause 4), in the same action as this mail.

## THE SEQUENCE (supersedes the order in your plan confirmation for ITEM 1)
a. **ONE PR from develop `37205947ddd2`, alone:** the js-yaml lock line plus the one baseline entry. Tier 2 (dependency hygiene for a test-tool lock + a measured baseline row). Commit subject e.g. `KS-470: move systemTest/performance js-yaml to 5.4.2 and accept GHSA-r53p build-tree only` (declared ≤ 85; check the landed length), `Refs KS-470`. Push under `.push-lock-43`: legs 6 and 7 must PASS on it. READY → **gate48a** (Wednesday drafts the kit) → GO → merge.
b. **Then** rebase ITEM 1a (and 1b, once built) onto the new develop, `cmp` the product bytes against the READYs, re-run red-first, push (both legs now pass), and ONE READY → **gate48b**.
c. **ITEM 2 (KS-1380/1387):** at your ctx this goes to your HANDOVER as a design-only item with every measurement you have taken (the image you built, the failing set if measured), **unless** a/b are merged under 65%. **Hard line 75%.**

## NOT IN THIS PR
- The GHSA-v2v4/mwp4 dead-row cleanup (it moves the fuse's row count).
- No `expires` edits and no other lock.
- Nothing on `mobile/secuura-app` (KS 769, out of scope).

PROVENANCE:
- your ctx | tmux capture-pane statusline ctx:56% | read 2026-09-30 07:31
- measurements, precedent rows, dry-regen sizing | your STATUS mail 21:29Z, DKIM/SPF/DMARC pass | read 2026-09-30 07:31
- the grant's clauses | 0_Brain/learnings/2026-09-09_advisory-baseline-standing-authority.md | read 2026-09-30 07:31
