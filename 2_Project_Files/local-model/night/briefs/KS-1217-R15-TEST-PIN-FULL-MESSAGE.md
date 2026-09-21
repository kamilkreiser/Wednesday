# KS-1217 R15-TEST-PIN-FULL-MESSAGE - re-brief of the held READY at develop 9f0265eb0 (written 20:35 on 2026-09-21 by Wednesday's census15 drafter from the file at the tip - 185 lines read whole)
File: `Blockchain/Dev/services/auth/src/__tests__/ks1050-profile-update-zero-rows-is-not-success.test.ts`
Tip: `9f0265eb06ecf24d4de18149ce862ad2330a61ee`
Runner: `vitest`

## Premises (measured by the census15 drafter at 20:35:38 AEST, in a `--shared` scratchpad clone detached at the tip; Wednesday re-derives before queueing)
- Source READY: `night/READY_KS-1217_ornith35b-q4_TEST-PIN-FULL-503-MESSAGE-PASS-7of7_2026-09-17.diff.md` (its checker PASS was at an OLDER tip; run dir exists: `runs/2026-09-17_ks1217-ornith35b-night`); canonical patch 1228 B sha256[:16] `af73030d1ec5d713`, +2/-1.
- The old patch at the tip: strict rc 0 / --recount rc 0 / --directory=Blockchain/Dev rc 1 / -R rc 1 -> effective mode **strict**; the old READY's + lines PRESENT at the tip: NO (content absent - un-merged).
- The test file `Blockchain/Dev/services/auth/src/__tests__/ks1050-profile-update-zero-rows-is-not-success.test.ts` at the tip: EXISTS (185 lines) - MODIFY IN PLACE. Mode: **MODIFY**.
- Tamper source: the old brief `night/briefs/KS-1217.md` (its `## Tamper` line/from/to, converted to the current `### ID` shape). Each From located at the tip by exact whole-line match (count in the Tampers section).
- Ticket KS-1217: Backlog, assignee kamil.kreiser@secuura.ai, PR attachments none (all merged); briefs already on disk: KS-1217.md.
- Generator notes: no new it() in the + lines (a modify of an EXISTING cell): reds = the enclosing cell title(s) at the tip ['🔴 KS-1050 — a 0-row UPDATE answers 503 "Profile update could not be confirmed", never a not-applied claim'] - INFERRED; reds INFERRED as every non-CONTROL/COMPLETENESS cell (1) - no RED-prefixed title in the old patch; Wednesday confirms the set against the old READY header; the run input.json is the older code_patch shape (no tampers key) - tampers taken from the old brief instead; CONTROL INFERRED: the file's first existing cell '🔴 KS-1050 — a 0-row UPDATE never answers success: true, and ' (green on both trees by construction; the old READY declared no control); Runner: vitest from the old brief header.

## What is wrong (one paragraph)
The held READY's own summary, verbatim from its header (the model wrote these cells once and the checker passed them at tip 2026-09-17; the run is re-done at the CURRENT tip so the checker verdicts it fresh):
> # READY — KS-1217 (test-only, auth ks1050 test :146 — pin the WHOLE 503 helper message, the dash built by code point, so an appended not-applied claim reds)
> # Source read by Wednesday 22:13: the model's 3 +/- lines IDENTICAL to the brief's fence (python sequence compare; a mutated copy unequal); checker RESULT PASS (7/7) first sample, apply_mode=LENIENT (the model's hunk-header dialect: `@@ -143,9 +143,10 @@` vs the brief's `-143,7 +143,8`); A4 red by assertion under the :973 tamper; A5 4/4; A6 auth 762 -> 762 no new red; A7 tsc rc 0. Tip = develop 75ad0e55c.
> # PR NOTES: `Closes KS-1217` is defensible once merged (the ticket's recommendation is exactly this edit; confirm at raise); KS-1050 stays In Progress (§5f). TIER 2 (coverage pin, in-process). Re-derive the hunk header at raise with `git diff` after applying (lenient apply). Develop has moved to 0a2b1603f since the brief: re-apply strict at raise. Run: runs/2026-09-17_ks1217-ornith35b-night/out.md.
This task asks for the SAME cells, re-derived at develop `9f0265eb0`. Nothing in the product changes. The old diff still applies at the tip in mode strict - emit the same cells, anchored on the lines quoted below.

## THE MODE - read this twice
TEST-ONLY, MODIFY IN PLACE: your diff contains EXACTLY ONE file, the EXISTING test file above, as the hunk(s) below (context lines byte-for-byte from the tip; no blank context line; no blank + line; a pure insertion ends with a context line). No product hunk. 

## The exact change
```
@@ -143,10 +143,11 @@
     expect(res.status).toBe(503);
     expect(res.body.success).toBe(false);
     expect(res.body.error.code).toBe('SERVICE_UNAVAILABLE');
-    expect(res.body.error.message).toMatch(/^Profile update could not be confirmed\. Please retry/);
+    // KS-1217: the WHOLE message, so an appended not-applied claim in any words reds (the dash is U+2014, built by code point).
+    expect(res.body.error.message).toBe('Profile update could not be confirmed. Please retry ' + String.fromCharCode(0x2014) + ' if you already succeeded, you may not need to.');
     // The helper's docblock forbids asserting the change did not land: null has two causes.
     expect(res.text).not.toMatch(/not applied|matched no row|did not persist/i);
     // The null came from the 0-row arm: one UPDATE issued, and no read-back after it.
     expect(updates()).toHaveLength(1);
     expect(readBacksAfterUpdate()).toHaveLength(0);
   });
```

## Cells (every cell RED or CONTROL; the names below are the EXACT it() titles)
- `🔴 KS-1050 — a 0-row UPDATE answers 503 "Profile update could not be confirmed", never a not-applied claim`
- `🔴 KS-1050 — a 0-row UPDATE never answers success: true, and the success line is not logged`  (CONTROL - green on both trees)

## Tampers
### TESTPINFULLMESSAGE
File: `Blockchain/Dev/services/auth/src/repositories/userRepo.ts`
Line: 973
From:
```
      `${operation} could not be confirmed. Please retry — if you already succeeded, you may not need to.`,
```
To:
```
      `${operation} could not be confirmed. Please retry — if you already succeeded, you may not need to. The write did NOT take effect.`, // TAMPER: KS-1217 red-proof, an appended not-applied claim (the #1018 r2 gate row Q-D1-DENYLIST)
```
Reds: `🔴 KS-1050 — a 0-row UPDATE answers 503 "Profile update could not be confirmed", never a not-applied claim`
(From located at the tip: 1 match(es); the old brief/input said line 973)

## Controls
- `🔴 KS-1050 — a 0-row UPDATE never answers success: true, and the success line is not logged`

## Output
Exactly ONE ```diff block; paths repo-relative (`Blockchain/Dev/services/auth/src/__tests__/ks1050-profile-update-zero-rows-is-not-success.test.ts`); correct hunk counts; no `\$` / `\u` / backslash escapes in a `+` line; the cell titles EXACTLY as listed (the checker matches the full title).
