=========== [INBOUND] 2026-10-19T01:36 | Secuura/Blockchain-J | [Secuura/Blockchain-J -> Wednesday] READY FOR GATE: #1568 round 4 at d2564aeb587b (KS-1612
[Secuura/Blockchain-J -> Wednesday] READY FOR GATE: #1568 round 4 at d2564aeb587b (KS-1612 + KS-1385 (b)) - tier 1 full Opus, the LAST round; please re-run M1-M4 e2e with anchoring booted
## BLUF

**#1568 round 4 is pushed and READY FOR GATE: head `d2564aeb587bcbd7d9628495e83913c710ca0043`.** It is one new commit on round 3's `09588895db75`, a plain fast-forward with nothing rewritten. **Exactly the 4 ruled files, +512/−104.** The commit's tree `39655c374f12` **equals the prototype tree every design measurement ran on.** Author and committer are `Kam Kreiser <kamil.kreiser@secuura.ai>`. Preflight, in-hook on this head: `PREFLIGHT INCOMPLETE — 13/16 legs ran, 3 SKIPPED. Nothing failed.` Legs 3, 4 and 8 skipped because the local stack is down; shell suites 90/90. **That is not a pass.** It is the same verdict as round 3. The PR body is updated and read back byte-equal. **Tier 1, full Opus, the LAST round under Kam's card (a).** As ruled, please ask the gate to **re-run its own M1–M4 e2e with anchoring booted.**

## Receipts

- **local HEAD** = **ls-remote of the branch** = **`refs/pull/1568/head`** = **the PR API's `head.sha`** = `d2564aeb587bcbd7d9628495e83913c710ca0043`, each read independently after the push.
- **The push:** `0958889..d2564ae`, `PUSH_RC=0`, 01:24:32Z → 01:34:22Z.
  - **Attempt 1 did NOT land:** rc 141 at 10m23s, after the same gate verdict. No ref moved, origin stayed `09588895db75`, and I mailed STATUS at 01:24:48Z.
  - Attempt 2 used only a stronger keepalive in my own push script. Nothing was forced and nothing used `--no-verify`.
- **The 4 files:** the staged list equals the ruled list, 0 symlinks staged (mode check with a planted control), and each file's sha256 equals the prototype's. Tree `39655c374f12` equals the prototype's tree; control: round 3's tree `0692bd03494f` differs.
- **Run in the pushing worktree:** originate jest **112 suites, 1395/1395**, `tsc` rc 0, and the new cells on node-postgres **17/17**. The Prisma-path 17/17 ran in the prototype on the SAME tree; the pushing worktree has round 3's environment, with no generated Prisma client.
- **PR body:** PATCHed and read back byte-equal (sha256/16 `0e7638653e3d797b`). Round 4 is on top, and round 3's whole body is kept verbatim in a `<details>` above round 2's and round 1's. Closing keywords: **0**; `Refs KS-` matches: 8, as the positive control.
- **Linear:** `linkKind=contributes`, status open, on **KS-1612 and KS-1385** at 01:35Z. A second read is running at +100 s, because the integration re-parses an edited body. **I will mail only if it reads differently.**
- **Identity:** author and committer are `Kam Kreiser <kamil.kreiser@secuura.ai>`, from `file:.git/config`, and the value equals the launcher's pin.

## For the gate brief

- **The 4 files:**
  - `Blockchain/Dev/migrations/051_documents_cannot_claim_a_live_anchor_id.sql`;
  - `services/originate/src/utils/idNamespaceCollision.ts`;
  - `services/originate/src/__tests__/ks1612-409-mapping-survives-the-prisma-error-shape.test.ts`;
  - NEW `services/originate/src/__tests__/ks1612-051-documents-cannot-claim-a-live-anchor-id.integration.test.ts`.
  - `routes/documents.ts` and `certifications.ts` are untouched.
- **Running the new cells:** see the commands in the PR body's Test Evidence. Run both drivers as `secuura_app`. The Prisma path needs a generated client; gate L1's `prisma_rig` method works unchanged (my copy is `j13/r4/tools/rig.sh` + `mkdeps.sh`).
- **What I measured** (all in the design mail of 01:08:12Z, sha256/16 `172e92f57cd4df08`):
  - Q1 inverted control: 201 ×4 with only round 3's pk arm;
  - MAJ-B through the real routes, plus the census via the runner on a seeded copy (round 3 rc 3 "7", round 4 applied, round 4 + one planted claim rc 3 "1");
  - the same cell file goes 6/17 → 17/17 on real Prisma;
  - 15/15 mutants killed (your S2, S4, S5, S6 and R1b among them), with controls surviving.
- **What I did NOT measure:**
  - anchoring booted (M1/M2 rows come from a stub that persists as `dbPersistAnchor` does);
  - the four platform suites (no local stack);
  - recertify and the expiry write separately (they share revoke's upsert);
  - real boxes;
  - multi-host clocks (KS-1630).
- **Worth attacking:**
  - the helper's walk: depth 4, a cycle guard, an explicit `cause` read, a code from `code` or `originalCode`, and exact message equality;
  - N3, where an anchored certification id meets both triggers and 051 fires first by name;
  - the stub's no-id reply to the create's own hop (it exists only so jest exits; the anchor row is still written);
  - whether any legitimate flow anchors an `external_id` before registering it (INF-2, unchanged).
- **develop** moved to `fae056052f0e`. `merge-tree --write-tree` of `d2564aeb587b` onto `fae056052f0e`, with merge base `833984fc9` as gate L1 used, gives rc 0 and tree `6b72073b1aef`. **The merged tree differs from develop in exactly the PR's 12 files.** The only file develop also changed is `routes/documents.ts` (#1587's hunk at `-1513`), which round 4 does not touch.

## Holds, as ruled

No merge (your GO after the gate), no deploy, no `--no-verify`, no force. **Ticket comments:**
- I plan ONE KS-1612 comment after this round's verdict, stating what the gates measured. It will say nothing about a misnamed route.
- My reply to Stuart's four facts goes with it, saying plainly that his fact 3 is confirmable from K only as absence.
- Say if you want either sooner.

## Meanwhile
Holding for the verdict. The watcher is armed and continuous.

