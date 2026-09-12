# QA GATE — TIER 1, round 1 — Datasec / HPSM — Policy Composer WP3 rules engine @ 0523193

**The commission.** Kam ruled at 15:24:26 AEST on 2026-09-12: *"build the full website and fully functioning engine"*. At about 15:30 he added, in Tuesday's terminal: *"start the buld. Claude credits resume in 12 hours so even if we run out it will be temporary"*. **He reviews the platform on Monday 2026-09-14. This gate is on the ENGINE, the product's core.**

**Head under test:** `052319342974fc05aabdf056da73558182b871f0`, on local `main` of `/Volumes/KK_T9_External_HDD/!CODING/Datasec/HPSM/6_Policy_Composer`.

**Range:** `afc10e9..0523193`, 8 commits:
- `3c6fc74` canonical + deps
- `7b4a2ef` catalogue/expressions/domains
- `a75d6cb` resolve S0–S10
- `0fba6fd` lane B's workspace deps, package files only
- `032cfd8` validate / releaseAllowed / bundle adapter
- `68ed478` goldens and mechanics
- `083407e` strict and assessment-only posture tests
- `0523193` §1.12 context fingerprints

NOT pushed; HPSM-light `main` is still `afc10e9`.

**The builder, seat hpsm-c7, is still committing WP6 onto the same local `main`.** `main` WILL move past `0523193` while you work. You gate `0523193` by SHA in your own clone. A moved `main` is expected, not a finding.

PRIOR ROUND: none on WP3 — this is its first gate. The last Composer gate (round 4, the WP2 database layer, GO WITH FINDINGS) is at `/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/hpsm/reports/2026-09-12-composer-afc10e9-tier1r4/report.md`. Read its §0 and §6 for how this codebase has failed before.
Carried forward: nothing from WP2 is re-opened here. Its residue is listed under KNOWN below.

## Target, how to reach it, the shared daemon
Round 2's brief, "Target" section, still applies: `/Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-09-11_hpsm-composer-0c3078e-tier1r2.md`. These changes apply:
- **Checkout:** check out `052319342974fc05aabdf056da73558182b871f0`, **plus `afc10e98c51505be1f1943335370cf2de3b47d44` for red controls**.
- **Stack:** compose project `policy-composer-qa-wp3`, edge port `18480`. The builder's lanes use 18180, 18280 and 18380.
- **Hooks:** run `scripts/install-hooks.sh` in your clone.
- **Builder evidence** (read it, never write there; it is a claim, not evidence you rely on): `/Volumes/KK_T9_External_HDD/!CODING/Datasec/HPSM/1_Project_Definition/Architecture/2026-09-10_policy-composer/qa-wp3/README.md`, with `evidence/` and `red/` beside it.
- **The architecture is the spec:** `/Volumes/KK_T9_External_HDD/!CODING/Datasec/HPSM/1_Project_Definition/Architecture/2026-09-10_policy-composer/2026-09-10_policy-composer_ARCHITECTURE.md`. §1 whole, §6.1's WP3 row, and §A/§Q for A-10, A-33, A-35, A-50 and Q-19/Q-20.
- **The Docker daemon is shared with two live builder lanes.** Never stop a container or remove a volume you did not create. Count the daemon's volumes at START and END and report both numbers. The builder reports 82 dangling at 06:49Z, all record-only for you.

## THE BUILDER'S CLAIMS — verify each, relay none (READY FOR QA 2026-09-12T06:49:22Z, spf/dkim/dmarc pass)
1. **Golden E1–E3:** 13 semantic tests, plus 6 stored canonical manifests compared byte for byte and validated against the engine's schema copy. All 6 failed as "golden missing" before generation.
2. **§1.13 properties** (fixed seeds): order independence, idempotence, monotonicity under added framework minimums, and a secret fuzz (credential shapes never reach the manifest or lineage).
3. **RFC 8785:** 5 reference vectors byte-exact; `values.json` refused (floats, A-33). SHA-256 via `@noble/hashes` 2.4.0: NIST vectors, plus 2,000 seeded strings against `node:crypto`.
4. **No I/O:** the purity lint now covers `packages/canonical`. A transitive import-closure test uses a positive control: the whole `@pc/content` entry reaching `fs`.
5. **Performance:** under 1 s for 123 controls × 10 groups. Host medians 75.3 / 78.5 / 67.9 ms (M2, node 26). **Under node 22 in CI the number is NOT captured.**
6. **Every §1.16 code:** the 22 engine-emitted codes each have a named triggering test, and an `afterAll` fails if one is untriggered. The other 4 are D3.
7. **Fix-removal mutants 22/22 RED at head.** M06 (strict posture High→ON) survived at `68ed478`; the test was added in `083407e`.
8. **Real content `47ea3e7c…`:** 55 items, 57 fields, every value null, 57 NEEDS_TARGET, severities as derived, unsupported `fail`, CONTENT_PROVISIONAL + UNSUPPORTED_HPSM_VERSION, release blocked, hash stable.
9. **Found and fixed before commit:**
   - F-01: a manual decision on an L4–L7 field was silently ignored.
   - F-02: prettier rewrote the vendored vectors.
   - F-03: a test expectation changed to §1.7's "m.value in D".
   - Step 7: §1.12 context fingerprints were accepted but never checked.
10. **Clean-clone `scripts/ci.sh` GREEN 13/13 at head.**

## DEPARTURES — Tuesday received them; whether they are correct is YOUR question (full list D1–D18 in the builder README)
- **D3:** of 26 codes, POLICY_ALREADY_EXISTS belongs to WP4, and the three Bridge codes are NOT TESTED.
- **D6:** a candidate manifest may carry nulls; a releasable one has none.
- **D7:** `release_label` is NOT in the hashed manifest. The builder's reason: hashed, the release step would change the hash the approvals bind to. **Decide whether leaving it out lets anything that matters change after approval without the hash moving.**
- **D8:** expression grammar. The seed contract's `{"gte":["fact.e8.maturity",2]}` must be written `{"gte":[{"fact":"fact.e8.maturity"},2]}`. **Decide whether the contract's own form is REFUSED loudly or silently MISREAD (e.g. the string compared as a literal). A silent misread is a Major.**
- **D9 / F-03:** §1.7 read as `m.value ∈ D`, and a manual decision is then governed like L3. **Tuesday read architecture §1.7 line 330, which says exactly `m.value ∈ D` and "then governed like L3". The TEXT supports the reading; whether the CODE does is your question.**
- D10–D18 as listed in the README. D17 in particular: `contentFromBundle` REFUSES a bundle whose typed tables have rows, rather than guessing.

## 🔴 WHAT TO ATTACK FIRST
1. **§1.7 against the code, clause by clause:**
   - L3 beats L4–L6 only inside D;
   - an empty S gives FRAMEWORK_CONFLICT vs UNSATISFIABLE (A-10: an active conflict BLOCKS);
   - the baseline default inside S wins;
   - ordered fields pick the weakest value at least as strong as the baseline, else the strongest plus BASELINE_OVERRIDDEN_BY_FRAMEWORK;
   - the L6 fallback and the L7 template default;
   - NEEDS_TARGET;
   - L8 only on a fingerprint match AND `m.value ∈ D`.

   Build your OWN deciding fixtures for each clause (not the builder's), and plant your OWN fix-removal mutants.
2. **Determinism and the hash, with an independent implementation.** Canonicalise and hash the six golden manifests with a DIFFERENT implementation (e.g. Python: your own RFC 8785 serialisation plus `hashlib.sha256`), controlled against the vendored RFC vectors first. A mismatch means one of the two is wrong; find which.
3. **Invented is not legal (Q-19).** On real content and on fixtures, show that no value reaches a manifest that the content or an explicit decision does not carry. Check the resolution record, lineage and issue payloads too, not only the manifest. Do the same for secrets, beyond the builder's fuzz corpus.
4. **Q-20 and its reach** (§1.9 as amended): High + remediable → ON; high-impact High → ON + approval; the strict and assessment-only postures. The builder found M06 surviving once. **Look for the next gap of that shape.**
5. **§1.12 decisions:** a stale fingerprint gives DECISION_STALE and is never silently applied or dropped; CONTENT_VERSION_CHANGED.
6. **The guards that guard the tests:**
   - remove one trigger test and show the `afterAll` fails;
   - plant a transitive `node:fs` import and show the closure test fails;
   - confirm the purity lint fires on `packages/canonical`.
7. **Performance under node 22 inside the CI container** (the builder did not capture it). Report the median, the fixture size and the machine.
8. **Clean-clone CI at head.**

## KNOWN — do NOT report as new (all BACKLOG)
- **Database / WP4 residue:** R4-m1 · R4-m2 · R4-p1 · R4-f1 · R4-L1 · U-0005 · S3-F1…S3-F5 · R2-m1, R2-m3, R2-m5 · the WP4 PK oracle · R3-m1.
- **R3-m2** (the `test-db.sh` volume leak; fixed on lane B, not in this head).
- **The running stack still connects as the superuser** (WP4, lane B, not in this head).
- **Builder NOT TESTED:** C12 per-version domains; constraints on certificate composites; set_enum disjunctions over 12 options (refused); ORDER edges in resolution (WP6); REQUIRES_ONE_OF per group; firmware and HPSM version ranges (exact match only); JCS in a browser; the perf median under node 22.
- **What you still owe on that list:** if one of those limits produces a WRONG VALUE SILENTLY on inputs MVP A can reach, rather than a refusal or an issue code, that IS a finding. Say which.

## Output, controls, logistics
- **Findings-only.** Every finding carries FOUND / TESTED / HOW plus an evidence class (MEASURED AT RUNTIME · PROBED · READ ONLY). Every zero gets a control. Never `rm`.
- **Head readings at start, mid and end:** `0523193` reachable from local `main`, plus `main`'s current SHA. `main` moving is expected.
- **Run long commands in the FOREGROUND. Never end a turn waiting on a background notice.**
- **Report:** `/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/hpsm/reports/2026-09-12-composer-0523193-wp3-tier1/report.md`.
- **MAIL YOUR VERDICT** to `tuesday-agent@agentmail.to`, subject `[QA/Datasec-HPSM -> Tuesday] GATE VERDICT — Policy Composer WP3 rules engine @ 0523193 (tier 1)`. Lead with GO, GO WITH FINDINGS or NO GO. **Never `wednesday-agent@`.** You have no inbox.

PROVENANCE:
- Kam's commission verbatim (15:24:26 note; ~15:30 terminal line) | panel relay mail to tuesday-agent@ 2026-09-12T15:24:26 and Tuesday's own terminal | read 2026-09-12
- head 0523193, range 8 commits, afc10e9 ancestor, commit subjects, 71 files | git rev-parse / rev-list / log / diff --shortstat on the Composer repo, run by Tuesday s11 at 16:5x | read 2026-09-12
- HPSM-light main == afc10e9 | git ls-remote origin on the Composer repo, run by Tuesday s11 at 16:5x | read 2026-09-12
- claims 1-10, D1-D18 headlines, NOT TESTED, ports 18180/18280/18380, 82 dangling volumes | datasec-hpsm READY FOR QA 2026-09-12T06:49:22Z, spf/dkim/dmarc pass | read 2026-09-12
- §1.7 line 330 text (m.value ∈ D, then governed like L3) | architecture file lines 296-343, read by Tuesday s11 | read 2026-09-12
- builder evidence folder present (README.md, evidence/, red/) | ls on qa-wp3, run by Tuesday s11 | read 2026-09-12
- last Composer gate report path and verdict | Testing Agent MAIN projects/hpsm/reports listing + round-4 brief | read 2026-09-12

SELF-CHECK: re-read end-to-end for contradictions (main moving is expected; head pinned by SHA) | 2026-09-12 16:53
