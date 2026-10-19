# Gate brief: GATE AB1 = PR #1616 (KS-1645 item 3), Opus, tier 1, round 1 of 2

Commissioned by Wednesday after Seat R 54th's READY FOR GATE of 08:13Z. The author's CLAIM is beside this brief: `R54_READY_0813Z.txt`. Secuura only.

**Project:** `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files` is READ ONLY (ls-remote, show, diff, cat-file, log). Every write verb runs in your own clone in your scratch: `/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/dd32393e-b87e-4d51-ac65-b22e5897a2c1/scratchpad/ab1/`.

**What it is:**
- **The defect:** api-gateway `routes/audit-export.ts` cast `req.query.type` straight to `AuditType` and forwarded it to the security service, so an unknown or REPEATED `type` got a 200 whose filename and `meta.type` named a filter that was never applied.
- **The fix:** a runtime `AUDIT_TYPES` list (the type is derived from it), and 400 `BAD_REQUEST` BEFORE the upstream call for an unknown or repeated type.
- **Tests:** 5 cells in a new file (T1-T3 red, C1-C2 controls).
- **Scope:** Refs KS-1645, item 3 only; items 1, 2 and 4 stay open. The export was switched on by #1608, so this is one of four pre-deploy repairs.
- **Heads:** #1616 head `09e67d9ccd23f8200653001c94dc3bebe6f17fac`; develop `80868551e67934cb951d28eec44ce3bdf835944c` (Wednesday ls-remote 19:1x AEDT). The author predicts landing tree `b8d59ffc7351`.
- **Origin of the product hunk:** a Spark pass (night/READY_KS-1645-AUDITTYPE-1_*), held after Wednesday read it at source. The gate judges the code, not its origin.

## Questions (each with its instrument; name what you did NOT run)
1. **Does it refuse exactly the right set?**
   - every known type passes, and is forwarded unchanged;
   - an absent type means `all`;
   - unknown, repeated (an array), empty string, case variants (`AUTH`), and a type given with surrounding whitespace: say what each does, and whether that is defensible;
   - nothing reaches the security service on a refusal (count the fetch calls).
   Does `AUDIT_TYPES` match what the SECURITY service actually accepts? Read its handler. A list that refuses a type security supports is a regression; a list that admits one security rejects is a mismatch.
2. **Response shape and auth order:**
   - the 400 body follows the gateway's error envelope (compare with a sibling route);
   - no `content-disposition` on a refusal in csv format;
   - the refusal does not change who may call the route (auth/role checks still run first, or the order is harmless; state which).
3. **Red-first is real:** the three red cells fail at develop's copy of audit-export.ts with the test file present, and the two controls pass at both ends. Plant one mutation of your own (for example, drop the array check) that must red a cell.
4. **Landing:** merge-tree onto the LIVE develop (re-read ls-remote at start and before the verdict). Run the api-gateway suite on the landing tree (claim: 1158/1158 in 118 files), and tsc. The three-dot diff must be exactly the 2 files. Build `packages/shared` before any suite (`npm run build --workspace=packages/shared`), or the suite false-reds.
5. **OpenAPI:** if the route has a spec entry, does it declare `type` as an enum matching `AUDIT_TYPES`? If it does not, that is a note, not a blocker, unless conformance tests fail.

**Verdict file:** `verdict.md` in this folder.
- First line: `VERDICT: <GO|GO WITH NOTE|NO GO> at head 09e67d9ccd23... (tier 1, round 1 of 2; landing tree <sha> on develop <sha>; N blockers, M notes)`.
- Last line: the sha256 of `sed '1d;$d' verdict.md | shasum -a 256`.

**Rules:**
- Findings only: no fixes, no GitHub or Linear writes, nothing under `!CODING`.
- No `cd`, no `rm`, no stderr to /dev/null, no Docker.
- Every zero gets a positive control.
- The shell is zsh: no PIPESTATUS.
