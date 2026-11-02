# Spark operator 76, 2026-11-02: screen of the High + dependency AGENT-BUILDABLE rows, 2 HELD (0 failed after 1 control fix + 1 rebrief)

## BLUF
- HELD 2 passes, both PASS 10/10, golden BYTE-IDENTICAL, strict=True (bash_patch2): O76-P1 KS-1413 (demo issuer password echoed in two startup banners), O76-P2 KS-1081 (five compose keys missing from env.example). Both TIER 2 (shell/config, no auth or money).
- The screen (screen.md) found only these two Spark-suitable: ~35 candidates read; the rest are design/policy tickets, held or in-flight files (oauth.ts O73-P4, kyc index.ts O71, api-gateway admin.ts O72, security index.ts, tenant-provisioning index.ts), real-DB or CI-config work, or already merged.
- Tip: develop fcfa5dfdba9b at start (tip_start.out); c0f9af13f94b when rounds ran; 968f17070208 at end (ls-remote). Drift fcfa5df..c0f9af1 on my files EMPTY (drift_files.out). Drift to 968f170 UNMEASURED.
- Open-PR scan start 21 PRs / 122 files, end 20 PRs / 114 files; planted control (services/auth) = 7 each time; no PR lists any of my files (prscan_end2_hits.out empty).

## Held (ls night | grep O76)
READY_KS-1081-KS-1081-O76-P2_spark-dsv4flash_BRIEFED-BASHPATCH2-ENV-EXAMPLE-FIVE-COMPOSE-KEYS-PASS-10of10-PASS-10of10_2026-11-02.diff.md
READY_KS-1413-KS-1413-O76_P1_spark-dsv4flash_BRIEFED-BASHPATCH2-START-BANNERS-NO-DEMO-PASSWORD-PASS-10of10-PASS-10of10_2026-11-02.diff.md

## Per pass
- P1 `golden: BYTE-IDENTICAL; touched=4 products=2 tests=2 red=1 support=1 sibs=8 strict=True`. Start_Up/start-secuura.sh :711 and Blockchain/Dev/scripts/start-local.sh :284 print "(password: the published demo default - see CLAUDE.md)" instead of the demo password; new suite ks1413_start_banners_print_no_demo_password.test.sh (2 RED + 2 CONTROL); existing start_secuura_banner.test.sh CELL 3 loosened to "Issuer line still names the account" (SUPPORT, green on old and new script). BEHAVIOUR CHANGE for the PR: banner text only. NOT in the diff (state in the PR): the curl login literal at start-secuura.sh :603, the start-local.sh Admin line (admin123) and Grafana line, KS-951 gate extension. PR says "Refs KS-1413".
- P2 `golden: BYTE-IDENTICAL; touched=2 products=1 tests=1 red=1 support=0 sibs=88 strict=True`. Blockchain/Dev/env.example gains a comment block + ADMIN_USER_PASSWORD=, ENABLE_DEMO_SEED=, ALLOW_DEFAULT_SEED_PASSWORDS=, TSA_URL=, TSA_AUTH_KEY= (all EMPTY = compose's own `${KEY:-}` default; the sibling .env.example's `false` values deliberately NOT copied). New suite ks1081_env_example_declares_compose_keys.test.sh (5 RED + 2 CONTROL). BEHAVIOUR CHANGE: none intended (compose already passes empty); unmeasured on a stack. PR says "Refs KS-1081"; the 38-var divergence / KS-1077 decision is not in it. Raise seat: note KS-1081 is In Progress with a KS-1077 joint decision pending.
- Raise-seat notes: both strict (plain git apply); recommended tier 2 (P1 touches only echo text; P2 is a template, security-relevant gate NAMES but no values). P2's control B6 runs 88 sibling suites (813 s each time): its checker holds the Spark ~14 min per round.

## Round log (spark/done.md rows, AEDT 2026-11-02)
- P1: control CONTROL-FAIL 13:47:58 (B6: existing start_secuura_banner.test.sh CELL 3 pins the old Issuer line; fixed by adding it as a test, harness not a model round); control CONTROL-FAIL 13:51:48 (B4: a SUPPORT edit must be green alone; CELL 3 rewritten to a pattern green on both); CONTROL-PASS 13:55:44 (154 s); model PASS 10/10 14:00:48 (241 s, 54.5 s model, original brief, 0 rebriefs).
- P2: original: CONTROL-PASS 14:14:22 (813 s); model FAIL 14:16:42 (B3x: model turned `\$` into `$` in one dictated grep line; model 37.9 s). Rebrief (the one allowed) `_r2`: test matcher changed to `grep -qxF "$1="`; CONTROL-PASS 14:31:39 (817 s); model PASS 10/10 14:48:28 (949 s, 37.4 s model).
- hold_ready P1 ~14:01, P2 ~14:49. Queue discipline: one control until the first CONTROL-PASS (P1); later model/control lines only after the relevant CONTROL-PASS. No recursive grep over spark/ or night/.

## UNMEASURED
Whole-suite CI; GNU/Linux behaviour of the new suites; whether anything parses the old banner text; whether an empty ENABLE_DEMO_SEED equals unset in the app on a bootstrapped .env; drift of my files between c0f9af1 and 968f170.
Evidence: this folder (screen.md, desc/*.json, tip/, gen/, prscan_*, open_prs_*.json, lint_*, dry_*, hold_*, tree.out).
