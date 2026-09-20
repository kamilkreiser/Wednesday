#!/bin/bash
# Arms for doctor.sh's root-folder check (2026-09-20 21:4x).
#
# WHY: doctor printed "✓ root folder: only rules, portability and launchers" while
# the root held BOTH a unison conflict copy of the launcher AND a stray logs/ dir.
# Two holes: `Launch_*.command` matched the conflict copy, and `[ -f ]` skipped
# directories. Fixed; these arms prove the fix fires and that the OLD code did not
# (the negative control), per 2026-08-06_exercise-mechanisms-before-arming and
# 2026-09-08_a-false-absence rule 11 (a control must fail independently).
#
# It runs the REAL block extracted by line range from doctor.sh — never a
# re-implementation of it (2026-09-08_a-false-absence rule 7).
set -u
W="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
NEW="$W/2_Project_Files/doctor.sh"
OLD="$W/2_Project_Files/doctor.sh.pre-0920-2145-rootcheck"
TMP="$(mktemp -d)"; trap 'rm -rf "$TMP"' EXIT
PASS=0; FAIL=0

# Extract the block from a doctor by locating its own markers — no typed line numbers.
extract() { # <doctor file> -> stdout; from ROOT_STRAYS="" through the fi that CLOSES
  # the verdict if/else. Truncating at the warn line left the block unterminated and
  # every arm then "passed" on a syntax error — caught on the first run, 2026-09-20.
  awk '/^ROOT_STRAYS=""$/{f=1} f{print} f&&/root folder holds stray/{g=1} g&&/^fi$/{exit}' "$1"
}

run_block() { # <doctor file> <root dir> -> stdout of the block
  local blk="$TMP/blk.sh"
  { echo 'ok(){ echo "OK: $*"; }; warn(){ echo "WARN: $1"; }'
    echo "PROJECT_DIR=\"\$1\""
    extract "$2"
  } > "$blk"
  bash "$blk" "$3" 2>&1
}

mkroot() { # <dir> — a legitimate, clean project root
  local d="$1"; mkdir -p "$d"/{0_Brain,1_Project_Definition,2_Project_Files,3_Access_Keys,4_Credentials,5_Project_History,.git,.claude}
  touch "$d/CLAUDE.md" "$d/PORTABILITY.md" "$d/.gitignore" "$d/Launch_Wednesday.command"
}

check() { # <arm> <expect: OK|WARN> <must-contain or -> <output>
  local arm="$1" expect="$2" needle="$3" out="$4"
  # THE DISCRIMINATOR: a block that did not RUN prints neither marker. Without this,
  # "no WARN" reads as OK and a syntax error scores as a pass — which is exactly what
  # happened on this harness's first run (4 hollow passes).
  if ! echo "$out" | /usr/bin/grep -qE '^(OK|WARN):'; then
    echo "  ✗ $arm: the block did not RUN (no OK:/WARN: marker)  [$out]"; FAIL=$((FAIL+1)); return
  fi
  local got=OK; echo "$out" | /usr/bin/grep -q '^WARN:' && got=WARN
  if [ "$got" != "$expect" ]; then echo "  ✗ $arm: expected $expect, got $got  [$out]"; FAIL=$((FAIL+1)); return; fi
  if [ "$needle" != "-" ] && ! echo "$out" | /usr/bin/grep -qF "$needle"; then
    echo "  ✗ $arm: $expect but did not name '$needle'  [$out]"; FAIL=$((FAIL+1)); return; fi
  echo "  ✓ $arm"; PASS=$((PASS+1))
}

# ARM1 — CLEAN root must stay OK (the legitimate shape; a guard that warns here is noise)
R="$TMP/a1"; mkroot "$R"
check ARM1-clean OK - "$(run_block x "$NEW" "$R")"

# ARM2 — THE FOUNDING CASE: a conflict copy of the launcher must WARN
R="$TMP/a2"; mkroot "$R"; touch "$R/Launch_Wednesday (conflict_on_2026-09-18).command"
check ARM2-conflict-copy WARN "conflict_on" "$(run_block x "$NEW" "$R")"

# ARM3 — a stray DIRECTORY must WARN
R="$TMP/a3"; mkroot "$R"; mkdir -p "$R/logs"; touch "$R/logs/combined.log"
check ARM3-stray-dir WARN "logs/" "$(run_block x "$NEW" "$R")"

# ARM4 — a stray FILE must still WARN (the behaviour that already worked — regression arm)
R="$TMP/a4"; mkroot "$R"; touch "$R/screenshot.png"
check ARM4-stray-file WARN "screenshot.png" "$(run_block x "$NEW" "$R")"

# ARM5 — the documented EXCEPTION: a .pre-* backup beside a launcher must NOT warn
R="$TMP/a5"; mkroot "$R"; touch "$R/Launch_Wednesday.command.pre-0907-vaultheal"
check ARM5-pre-backup-allowed OK - "$(run_block x "$NEW" "$R")"

# ARM6/7 — NEGATIVE CONTROLS: the PRE-FIX block must MISS both, or these arms prove nothing
R="$TMP/a6"; mkroot "$R"; touch "$R/Launch_Wednesday (conflict_on_2026-09-18).command"
check ARM6-old-MISSES-conflict OK - "$(run_block x "$OLD" "$R")"
R="$TMP/a7"; mkroot "$R"; mkdir -p "$R/logs"
check ARM7-old-MISSES-dir OK - "$(run_block x "$OLD" "$R")"

# ARM8 — the old block DID catch a stray file; the fix must not have broken that path
R="$TMP/a8"; mkroot "$R"; touch "$R/screenshot.png"
check ARM8-old-catches-file WARN "screenshot.png" "$(run_block x "$OLD" "$R")"

# ARM9/10 — THE DISCRIMINATING PAIR for the gitignore-keyed directory rule.
# Same scratch repo, two directories: one gitignored (a recorded state drawer -> allowed),
# one not (a filing miss -> flagged). One arm alone could not tell the rule from
# "directories are never flagged" (2026-09-08_a-false-absence rule 11: a control must
# be able to fail independently of the thing it tests).
R="$TMP/a9"; mkroot "$R"
git -C "$R" init -q 2>/dev/null
printf '/logs/\n' > "$R/.gitignore"
mkdir -p "$R/logs" "$R/notignored"
out="$(run_block x "$NEW" "$R")"
check ARM9-gitignored-dir-allowed WARN "notignored/" "$out"
if echo "$out" | /usr/bin/grep -qF " logs/"; then
  echo "  ✗ ARM10-gitignored-dir-not-flagged: 'logs/' was flagged despite being gitignored  [$out]"; FAIL=$((FAIL+1))
else
  echo "  ✓ ARM10-gitignored-dir-not-flagged"; PASS=$((PASS+1))
fi

echo
echo "doctor root-check arms: $PASS pass, $FAIL fail"
[ "$FAIL" -eq 0 ]
