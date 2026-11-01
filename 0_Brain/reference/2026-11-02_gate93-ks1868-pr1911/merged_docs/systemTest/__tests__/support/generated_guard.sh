# generated_guard.sh — snapshot fixtures/generated/ before driving the SHIPPED pre-suite step,
# and put it back exactly afterwards. Source it; it installs an EXIT trap.
#
# WHY (KS-969 F-2, KS-992, restated here rather than a fourth copy left to drift — KS-1167):
# the step's DEGRADED path calls quarantineManifest(), an `fs.renameSync` of the LIVE manifest.
# A cell that drives that path from a developer's checkout would move their actors.json aside
# and still report every cell passing. `pre_suite.test.sh` and `quarantine_call_sites.test.sh`
# carry this guard inline; this file is the same guard for suites written after them.
#
# KS-992: a guard that could not SAVE must not DELETE. `generated_guard_snapshot_ok` records
# whether a copy is actually held; an ABSENT generated/ is fine (nothing to lose); only a cp
# that was attempted and FAILED flips it, and then restore refuses to delete and says so.
#
# KS-1735: restore's OWN cp was still unchecked, and `rm -rf $GENERATED_GUARD_TMP` ran either
# way — so a failed restore left generated/ empty or partial, deleted the only copy, said
# nothing, and left the suite's exit status alone. Both failure paths now KEEP the scratch
# directory and name it, and a failed restore exits non-zero (the suite's own status when it had
# one). The cost, as the inline copies accepted under KS 1027: on a failure the scratch directory
# survives the run, and the sourcing suite's temp files survive with it. That is the trade — a
# leaked temp directory is recoverable, a deleted snapshot is not.
#
# KS-1738: ANYTHING CHAINED IN FRONT OF THIS GUARD MUST PRESERVE $?.
# `generated_guard_restore` captures the suite's own exit status as its first statement so a
# failed restore can re-raise it. That works when the guard IS the EXIT trap. It does NOT work
# when a suite chains its own cleanup in front of it --
#   trap 'stop_stub; generated_guard_restore' EXIT
# -- because the chained command runs first and overwrites $?. A succeeding cleanup leaves $? 0,
# the guard then takes its "the suite itself passed" branch, and a suite that exited 3 is
# reported as 1. Nothing becomes green and the runner still scores the suite as failed, so this
# is LOW -- only the distinction between "the suite failed" and "the restore failed" is lost.
# Chaining is the natural thing for the next suite to do, which is why this is written here.
#
# The fix is opt-in and costs a plain caller nothing: restore now PREFERS a status passed as its
# first argument over $?. A chained call site keeps its own cleanup first and hands the status in:
#   trap 'rc=$?; stop_stub; generated_guard_restore "$rc"' EXIT
# Do NOT instead put the guard first (`generated_guard_restore $?; stop_stub`): on a failed
# restore the guard EXITS, so the chained cleanup would never run on exactly the path the guard
# exists for.
#
# Requires: $FIXTURES (absolute path to systemTest/fixtures). Provides: $GENERATED_GUARD_TMP,
# a scratch directory removed on exit, for the sourcing suite's own temp files.

GENERATED_GUARD_GEN="$FIXTURES/generated"
GENERATED_GUARD_TMP="$(mktemp -d)"
GENERATED_GUARD_STASH="$GENERATED_GUARD_TMP/stash"
generated_guard_snapshot_ok=1
generated_guard_existed=0
mkdir -p "$GENERATED_GUARD_STASH"
if [ -d "$GENERATED_GUARD_GEN" ]; then
  generated_guard_existed=1
  cp -R "$GENERATED_GUARD_GEN/." "$GENERATED_GUARD_STASH/" 2>/dev/null || generated_guard_snapshot_ok=0
fi

generated_guard_restore() {
  local rc=$?
  # KS-1738: an explicitly passed status WINS over $?. `local rc=$?` has to stay the first
  # statement -- any command before it, including `[`, overwrites $? -- so the argument is
  # applied immediately after. With no argument this is exactly the old behaviour, which is why
  # every existing plain-trap caller is unaffected. A non-numeric argument is refused rather
  # than used, because `exit "$rc"` on a non-number is a shell error and would replace a wrong
  # status with no status at all.
  if [ "$#" -ge 1 ]; then
    case "$1" in
      ''|*[!0-9]*)
        printf '  !! KS-1738: ignoring a non-numeric status argument [%s]; falling back to $?.\n' "$1" >&2
        ;;
      *) rc="$1" ;;
    esac
  fi
  if [ "$generated_guard_snapshot_ok" -ne 1 ]; then
    printf '  !! KS-992: the snapshot of %s FAILED, so this suite will not restore it.\n' "$GENERATED_GUARD_GEN" >&2
    printf '  !! generated/ is being left exactly as the run left it — a guard that\n' >&2
    printf '  !! cannot restore must not delete. Check it by hand.\n' >&2
    printf '  !! KS-1027: the partial snapshot is KEPT at: %s\n' "$GENERATED_GUARD_STASH" >&2
    return
  fi
  # Put back exactly what was there: the snapshot if the directory existed, nothing if it did not.
  rm -rf "$GENERATED_GUARD_GEN"
  if [ "$generated_guard_existed" -eq 1 ]; then
    mkdir -p "$GENERATED_GUARD_GEN"
    if ! cp -R "$GENERATED_GUARD_STASH/." "$GENERATED_GUARD_GEN/" 2>/dev/null; then
      printf '  !! KS-1027: restoring %s FAILED — it may now be EMPTY.\n' "$GENERATED_GUARD_GEN" >&2
      printf '  !! the snapshot is KEPT at: %s — copy it back by hand.\n' "$GENERATED_GUARD_STASH" >&2
      if [ "$rc" -eq 0 ]; then exit 1; fi
      exit "$rc"
    fi
  fi
  rm -rf "$GENERATED_GUARD_TMP"
}
trap generated_guard_restore EXIT
