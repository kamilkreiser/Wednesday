#!/bin/bash
# frontend_admin_vitest_arms.sh — arms for the HARNESS-SUPPLIED vitest config on frontend/admin (Spark o136, 2026-11-11). No model call;
# four round.sh runs against the real Secuura tip in the cache clone (needs the tunnel only for round.sh's endpoint probe), ~2 min.
#   F1 control, KS-1913 brief (R1/R2 red-first, C1 control): CONTROL-PASS
#   F2 control, fixture brief whose R2 is ALREADY green at the tip: CONTROL-FAIL naming A4 RED-FIRST
#   F3 the same brief with the pin pointing OUTSIDE spark/tiers/vitest_configs: REFUSED
#   F4 the same brief with NO vitest_config pin: REFUSED (frontend/admin has no vitest config at the tip)
# Prints "ARM Fn PASS|FAIL" lines and a total; exit 1 on any FAIL. bash 3.2, no cd.
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"; SPARK="$(dirname "$HERE")"; LM="$(dirname "$SPARK")"
B1="$(ls -d "$LM"/night/briefs/ks_1913_o136_p1_* | head -1)"; B2="$HERE/fixtures/frontend_admin_arm_notred"
T="${TMPDIR:-/tmp}/fe_admin_arms.$$"; mkdir -p "$T/nopin" "$T/evil"
FAILS=0
chk() { if [ "$2" = ok ]; then echo "ARM $1 PASS — $3"; else echo "ARM $1 FAIL — $3"; FAILS=$((FAILS+1)); fi; }
o="$(bash "$SPARK/round.sh" "$B1" --control 2>&1 | tail -1)"; case "$o" in *CONTROL-PASS*) chk F1 ok "control PASS";; *) chk F1 bad "$o";; esac
o="$(bash "$SPARK/round.sh" "$B2" --control 2>&1 | tail -1)"; case "$o" in *CONTROL-FAIL*) chk F2 ok "already-green red cell refused";; *) chk F2 bad "$o";; esac
for k in nopin evil; do cp "$B1/KS-1913.md" "$B1/golden.diff" "$T/$k/"; grep -v '^vitest_config=' "$B1/spark.pins" > "$T/$k/spark.pins"; done
echo "vitest_config=/etc/hosts" >> "$T/evil/spark.pins"
o="$(bash "$SPARK/round.sh" "$T/evil" --dry-run 2>&1 | tail -1)"; case "$o" in *REFUSED*"only place a harness-supplied vitest config may live"*) chk F3 ok "outside pin refused";; *) chk F3 bad "$o";; esac
o="$(bash "$SPARK/round.sh" "$T/nopin" --dry-run 2>&1 | tail -1)"; case "$o" in *REFUSED*"no vitest config at the tip"*) chk F4 ok "no pin refused";; *) chk F4 bad "$o";; esac
echo "frontend_admin_vitest_arms: $((4-FAILS))/4 PASS (scratch $T)"; [ "$FAILS" -eq 0 ]
