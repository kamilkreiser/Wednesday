# READY — KS-1019-1019LEAVEUNTYPED-R16B (Ornith, briefed, comment_patch) — PASS (8/8) apply_mode=strict first sample — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks1019-ornith35b-night/out.md.checker/patch.diff`** (the run dir from `done.md`'s row; run done 2026-09-22 19:22).

**Held 19:36 2026-09-22 by the 18:3x Wednesday seat after a source read.** Tip `3bad652d17cf111c1e2e1bed1ae7686894637487` (from `input.json`). Product file `Blockchain/Dev/services/originate/src/originate.openapi.ts` (from `input.json`). Brief: `2_Project_Files/local-model/night/briefs/KS-1019-R16B-LEAVEUNTYPED.md` — headline: # KS-1019 R16B-LEAVEUNTYPED - comment_patch: record Kam's "leave untyped" ruling as ONE comment line at the head of the schema that publishes the document match's `blockchain` block as `z.unknown()` (originate `originate.openapi.ts`, the block at `:615` at the tip - the ticket's `:601` at its own tip e559f7bb)
**Golden:** the drafter's precheck patch `2_Project_Files/local-model/runs/2026-09-22_feed16-drafter-precheck/LEAVEUNTYPED/out.md.checker/patch.diff` is **BYTE-IDENTICAL** to the canonical patch (python byte compare in the action that wrote this file).
**Kam's ruling:** card `secuura-ks1019-blockchain-block-untyped` → **a — "Leave untyped; record the reason at"** [the line] (live board 2026-09-22 18:10). **Placement (a known deviation, told to Kam on the live board):** the harness cannot anchor a comment beside a code line (builder R4 + cp_gates C5), so the line sits at the schema head (`:589` at this tip) naming the property (`blockchain:` is `:615` at this tip, not the ticket's `:601`); a one-line move to the property's own line is Kam's to ask for and a Claude seat's to make.

⚠ **WEDNESDAY'S RULING FOR THE RAISE:** raise as `Refs KS-1019`, never a closing word (the standing rule, 2026-09-19). Tier 2 (a comment-only change; C4 proves no behaviour change) — the gate may run through-code only.

**HELD. Not raised.**

---
## Checker verdict (verbatim tail of `2_Project_Files/local-model/runs/2026-09-22_ks1019-ornith35b-night/checker.out`)
PASS C1 output is exactly one fenced ```diff block, nothing outside it
PASS C2 diff applies at the tip (strict)
PASS C3 touched-file set == { Blockchain/Dev/services/originate/src/originate.openapi.ts }
PASS C4 token equivalence: 17679 code tokens (kind + text, literals included) identical before and after (typescript 5.9.3 parser leaves; gaps proven trivia-only)
PASS C4b directive comments unchanged (0 before, 0 after)
PASS C5 every changed line lies inside the named lines (:589-589)
PASS C7 every brief '+' line (1) is in the file after, byte-exact
RESULT: PASS (8/8) apply_mode=strict

## Diff (the canonical patch, verbatim)
```diff
--- a/Blockchain/Dev/services/originate/src/originate.openapi.ts
+++ b/Blockchain/Dev/services/originate/src/originate.openapi.ts
@@ -588,3 +588,4 @@
 );
 
+// KS-1019 (Kam 2026-09-22: leave untyped). The blockchain property below is z.unknown() on purpose: its shape varies by anchoring mode (real / simulated / failed), so every drift guard is blind to it by construction; typing it is a discriminated-union product change for Peter to review, not a widening.
 const V2VerifyMatchSchema = sharedRegistry.register(
```
