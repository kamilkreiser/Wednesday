# READY — KS-1135-MANIFESTQUARANTINESTDERR-1 (Ornith, briefed, test_only, modify · bash) — PASS 8/8 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-21_ks1135-ornith35b-night/out.md.checker/patch.diff`** (from `ls` at 16:13 2026-09-21). Checker T3: **applied with the --recount ACCOMMODATION, NOT strict** — `apply_strict.out` reads `error: corrupt patch at line 7`; checker.out: `PASS T3 diff applies at the tip — with an accommodation: --recount (miscounted header: hunk @@ -32,3 +32,3 @@ TMP="$(mktemp -d)" declared old=3 new=3 actual old=2 new=2 ); every line byte-exact` — the raise seat applies this patch WITH `--recount` and asserts the resulting blob (corrected by Wednesday 16:1x from the checker's own artefact: hold_ready.py had templated 'strict PASS' — the 03:3x row class; tool fix OWED); the run's patch DIFFERS from the drafter's golden at `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-21_gate1119rows-drafter-precheck/MANIFESTQUARANTINESTDERR/out.md.checker/patch.diff` (`cmp` rc 1) — read the diff before raising.

**Held 16:13 2026-09-21 by Wednesday 13:5x seat, 2026-09-21 after a source read (hold_ready.py — every clause below is built from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-21_ks1135-ornith35b-night/out.md.checker`, not typed).** Tip `9f0265eb06ecf24d4de18149ce862ad2330a61ee`. Touches ONE file: `systemTest/__tests__/manifest_quarantine.test.sh` (modify). `+` lines 1 ordered-equal to the brief's `expected_plus` (ASCII); `-` lines 1 == `must_remove`. Green at the tip: 14/14 cells. Tampers (1), each red exactly its declared set with controls green and the product file restored by bytes (T6/T7/T8):
- `DRIVERTHROWS` → red exactly ['a second quarantine at the same stamp does not clobber the f', 'a superseded copy exists', "slot 3's copy carries slot3, so the same stamp on two slots ", 'the copy is named for the rejecting run AND its slot', 'the first quarantine still holds its own content', 'the stale manifest is gone from the path consumers read', 'the superseded copy still carries the stale content (moved, ']

**PR NOTES for the raise seat:** TEST-ONLY — zero product bytes; one file, apply `patch.diff` strictly at the tip (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` and state it). Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-21_ks1135-ornith35b-night/input.json`. Brief: `night/briefs/KS-1135-MANIFESTQUARANTINESTDERR-1.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-21_ks1135-ornith35b-night/checker.out`.

```diff
--- a/systemTest/__tests__/manifest_quarantine.test.sh
+++ b/systemTest/__tests__/manifest_quarantine.test.sh
@@ -32,3 +32,3 @@ TMP="$(mktemp -d)"
-cleanup() { rm -rf "$TMP"; }
+cleanup() { if [ "$FAIL" -gt 0 ] && [ -s "$TMP/driver.err" ]; then echo "  driver stderr (tail -40 of driver.err, shown because $FAIL cell(s) failed; the EXIT trap removes it next):"; tail -40 "$TMP/driver.err" | sed 's/^/     | /'; fi; rm -rf "$TMP"; }
 trap cleanup EXIT
```
