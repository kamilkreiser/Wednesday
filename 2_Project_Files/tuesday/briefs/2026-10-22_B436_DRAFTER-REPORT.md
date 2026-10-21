# B436 DRAFTER REPORT (round 2 of 2, tier 1 gate, HPSM-POC telemetry 224)

Brief: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-22_B436_SEAT-G33_hpsmpoc-telemetry-gate-round2-tier1.md` (58 long lines). Read-only drafter: nothing tested, built, mailed or posted.

## Measured by me (read verbs only)
- `ls-remote`: `b429/telemetry-224` = `39d4d1a25294bf5059cf7a088ac3e7ca5fd8efcf`, main = `35b2b73ebf570878be3aea999e0af08a3fcbbfbf`, no `b436*` ref (control `b386*` printed).
- Ports 8060-8069: `lsof` rc 1, nothing listening. `.tools/b436` absent (control `.tools/b198` exists).
- Slot count in the brief: 2 (Stamp paragraph, final `READ-WHOLE-BY-TUESDAY` line), by `grep -o -E '@[A-Z]+@' | wc -l`.
- The 26-file and 35-file counts are RELAYED from your 07:42 compare check; I did not re-run them.

## Fill before launch
- Both `@STAMP@` slots (Stamp: seat, READ-whole, times, heads, launch authority, hard stop).
- Launch line is in the brief with `<this brief's absolute path>` left for you.

## Things I found that you should know (each is in the brief as an instruction to the gate)
1. **Gitleaks count mismatch.** Q2 ruling 1 said "9 fingerprints"; B432 says "8 fingerprints (9 findings)" and you asked for exactly 8 lines. The brief says exactly 8 + one comment and tells the gate to state which is true from the gitleaks JSON and whether any finding is left unignored.
2. **Web resource not cleared.** B432 cleared the resource detectors on the API only (`ResourceBuilder.Clear()`); B432's STATUS does not say the web's resource was touched. The brief makes the gate dump the web resource key by key (host, process, os) and treat an identifying key as a Blocker. This is the likeliest round-1-class gap left.
3. **Connection-string check is stricter than the distro** (B432's own words). Risk: it could refuse the real resource's string and silently turn telemetry off in UAT. The brief tells the gate to read the exact form `infra/**` sets and test that shape (Blocker if refused).
4. **Existing expectations were edited**, by ruling (Q2 4): API `TelemetryWiringTests`, `B429_request_path_rule` rows (2 theory names renamed), web `scrub.test.ts:103,139`, `setup.test.ts:89`; plus class declarations. The round-1 "0 edited existing lines" check is replaced by "each edit matches a ruled item".
5. **Instrument under test.** The B431-6 fix is a fixture ordering (`TelemetryRuns`), and B432 itself measured a first-host effect that moved fixtures twice. The brief adds an order-independence probe and a "skip the stock run" mutant on the 14 control rows.
6. **`web-settings.test.ts` +1** is outside ruling 2's wording; B432 asks you to ratify it. The gate confirms it is only the `LISTS` line; the ratification stays yours (FOR TUESDAY 1 of B432).
7. **Instance id** is read from an environment variable; the brief asks what App Service puts there and what the code does with a hostile 10 000-char value (class hunt).
8. B432's "web census" is unit-level through the real exporter, and the route-table read on the real standalone server was not tested by the builder (its own NOT TESTED). The brief puts both on the real standalone server and adds the missing-manifest case.

## Cap wording
Brief states in the opening and in Severity that a NO GO on the same class stops the work and goes to the product owner as a card, with no round 3 suggested.

## Not done / judgment calls
- I did not open any `.tools/b4*` tree, `fleet/briefs_staged/`, the scoreboard or `Notes (MASTER)`.
- Mutant count: the gate must re-prove at least 8 of B432's 13 (named) plus 3 own; the verdict line carries "n of 11+".
- B432's evidence folder was not read (claims only).

Paths:
- /Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-22_B436_SEAT-G33_hpsmpoc-telemetry-gate-round2-tier1.md
- /Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-22_B436_DRAFTER-REPORT.md
