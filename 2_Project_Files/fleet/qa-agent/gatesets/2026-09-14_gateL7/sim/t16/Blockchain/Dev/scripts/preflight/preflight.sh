#!/usr/bin/env bash
# =============================================================================
# Pre-push preflight (KS-380) — the ritual before you push a feature branch
# =============================================================================
# One command that runs the cheap, high-value checks the last few builds were
# missing. Each corresponds to a real slip:
#
#   1. OpenAPI spec drift   -> generated spec must match the Zod source
#                              (a stale spec makes every downstream check lie)
#   2. Lockfile clean-room  -> KS-374/376/#399 (locks that only work hoisted)
#   3. Spec-auth conformance-> KS-375 (spec promises auth the code doesn't enforce)
#                              — only when the local stack is up on :6882
#                              (also installs the scripts/preflight member's deps)
#   4. Path resolvability   -> KS-473 (spec publishes a path the gateway can't
#                              route — authed probe, "Route ... not found" = FAIL)
#                              — only when the local stack is up on :6882
#   5. audit-contract suites-> KS-763 (the validator both audit gates import had
#                              NO runner — CI calls the gates, not their tests.
#                              CANNOT skip: an offline run still reaches every
#                              case, because exit 2 satisfies their
#                              notEqual(code, 3). It does touch the network —
#                              the positive controls run each gate to completion
#                              — so the older "no network" justification for the
#                              cannot-skip was wrong; the rule survives it.)
#   6. npm-audit gate       -> KS-470 (ambient audit is off; a NEW or lapsed
#                              advisory outside scripts/audit/audit-baseline.json
#                              fails — skipped when the registry is unreachable)
#   7. standalone-lock audit-> KS-531 (step 6 audits the HOISTED root tree, which
#                              dedupes away versions a service's own lock still
#                              pins and ships in its image; this reads every
#                              lockfile directly — same baseline, same rules)
#   8. served-spec consistency-> KS-656 (every other spec check reads the HOST
#                              file and probes the runtime separately; none
#                              fetches the spec the gateway actually SERVES, so
#                              a half-dead docs surface stayed green everywhere.
#                              /api/docs/openapi.json and .yaml must agree)
#                              — only when the local stack is up on :6882
#   9. no tracked credentials-> KS-646 (a `!test-wallet.env` negation in
#                              .gitignore made the path explicitly UN-ignorable,
#                              so a later `git add -A` re-committed a deleted
#                              credential file and gave no signal it had. Also
#                              refuses any NEW negation that re-enables one.)
#  10. bare-path script modes-> KS-667 F-16 (`npm run test:migrations` was
#                              committed 100644 and invoked by bare path, so the
#                              wired entry point exited 126 on every fresh clone
#                              while the author's runs passed. Reads the mode
#                              from `git ls-files -s`, never the filesystem —
#                              `core.fileMode=false` makes the working tree
#                              blind to exactly this class.)
#  11. pinned-action labels -> KS-751 ask 4 (a SHA-pinned `uses:` says nothing
#                              about WHAT it pins; the label must be present so a
#                              reader can tell a pin from a typo.)
#
# THE ORDER IS LOAD-BEARING between 5 and its install, not merely cosmetic — see
# the block above leg 5. This list was scrambled (two entries numbered 9, one
# missing) by two branches inserting legs independently; renumbered to 11 when
# #781 and #796 met.
#
# It does NOT replace the per-package quality gates (systemTest, service tests)
# — it's the fast structural sweep that catches the cross-cutting mistakes those
# gates miss. Run from Blockchain/Dev. Exits non-zero on the first failure.
#
# Usage:  bash scripts/preflight/preflight.sh
#
# Invoke via `bash` — this file is tracked mode 100644, in line with every
# script in `scripts/preflight/` (4 of 4, measured) and with how CI runs them.
#
# ⚠ NARROWED TWICE (KS-667 F-16 / KS-751). The scope of this sentence is the
# point of it, so here is what each version claimed and what the census says:
#
#   v1 "in line with every other script here (22 of them)" — reads as a
#      repo-wide convention. FALSE: 64 of 100 tracked `.sh` in the repo are
#      100755 (Blockchain/Dev: 45 of 71). The count 22 was never reproducible
#      against any directory and is quoted here only as the superseded text.
#   v2 "…in `scripts/preflight/` and `scripts/`" — still FALSE for `scripts/`,
#      which is an even 24/24 split of 100644 and 100755; `scripts/smoke-test.sh`
#      and every `scripts/__tests__/*.sh` are 100755.
#   v3 (this one) `scripts/preflight/` only — 4 of 4 at 100644.
#
# Reading the narrow convention as a wide one is exactly what left
# `migrations/__tests__/ks667-044-scenarios.sh` committed 100644 while its npm
# script invoked it by bare path, so it exited 126 for everyone but its author.
# Leg 10 now enforces the actual invariant rather than relying on any convention:
# a bare-path invocation requires 100755; an interpreter-invoked script may be
# either. A convention in a comment cannot fail; a gate can.
# (`run: bash scripts/...` in pr-security-gates.yml, pr-lockfiles.yml,
# security-scan.yml). This script calls its own sibling the same way at line 69.
# The bare-path form the docs used to show reads as a direct exec and fails with
# "permission denied" (KS-487 session note).
# =============================================================================
set -uo pipefail

cd "$(dirname "$0")/../.."   # Blockchain/Dev
GATEWAY="${GATEWAY_URL:-http://localhost:6882}"
fail=0
env_fail=0   # KS-991: leg 1 could not RUN (no workspace install) vs a real finding

# --- KS-1046: the verdict must not outlive its corpus -------------------------
# `PREFLIGHT PASSED.` used to be printed identically whether 13 legs ran or 10:
# a leg that SKIPped contributed nothing to `fail`, and the final line named
# neither the count nor the omission. Proven by control on 2026-09-09 — same
# tree, same commit, `GATEWAY_URL` pointed at a closed port: three legs SKIP,
# zero FAIL, and the output was byte-identical at the verdict.
#
# That is the KS-773 defect one level up, and it matters more: this is the line
# quoted into PR Test Evidence blocks, so a reader cannot tell a full run from a
# partial one. Legs 3 and 4 — "unauth requests to bearer-authed ops must
# 401/403" and "every published path must route" — are among the three that
# disappear when the local stack is down.
#
# The shape follows the two precedents already in this corpus rather than
# inventing a third: `run-shell-suites.sh` refuses the vacuous pass in terms
# ("'all 0 are reached' is not a pass"), and `check-production-guard.sh` reports
# a RATIO ("23 / 23 services"), never "all".
#
# Two skip classes, because this script already draws the distinction in its own
# vocabulary and the verdict now honours it:
#   SKIP —            the developer can clear it (start the stack).
#   SKIP (advisory) — the developer cannot (offline, registry down).
# NEITHER BLOCKS BY DEFAULT. Both are reported, and both keep the run from being
# called a PASS; the verdict names the ratio instead. See the reasoning at the
# foot of this file — it is a contract `.githooks/pre-push` owns, not this one.
#
# KS-1046 / QA F-925-1: an earlier draft of this comment said SKIP "BLOCKS" and
# named an escape `PREFLIGHT_ALLOW_INCOMPLETE=1`. Neither was ever true — that
# variable occurred exactly ONCE in the whole tree, in the comment that
# documented it, so a reader of this file learned the opposite of the truth
# inside the fix for exactly that class. The implemented control is
# PREFLIGHT_STRICT_LEGS=1, defaulted OFF.
TOTAL_LEGS=16
SKIPPED_STACK=""      # space-separated leg numbers
SKIPPED_ADVISORY=""   # space-separated leg numbers
RAN_LEGS=""           # space-separated leg numbers — OBSERVED, not derived
CURRENT_LEG="?"

# KS-1046 / QA F-925-2: `n_ran` used to be TOTAL_LEGS - n_skipped. That is a
# claim about arithmetic, not about execution: a leg that no-opped inside its own
# sub-script never called skip_advisory, so it was counted as having RUN.
# Measured instance: in a non-git checkout, leg 12's `run-shell-suites.sh`
# printed "SKIP (advisory) — not a git checkout" and exited 0; the verdict said
# ten of thirteen when NINE legs had run.
#
# So a leg is now marked RAN by observation — it reached its own conclusion
# without declaring a skip. _leg_concluded() runs when the NEXT step() starts and
# once more before the verdict, so the last leg is not lost.
#
# ⚠ Residual, stated rather than papered over: a leg whose body silently does
# nothing AND prints no skip is still counted as run. The known instance of that
# (a delegating leg whose sub-script skips) is closed by run_delegated() below;
# a future one would need the same treatment.
_leg_concluded() {
    [ "$CURRENT_LEG" = "?" ] && return 0
    case " $SKIPPED_STACK $SKIPPED_ADVISORY " in
        *" $CURRENT_LEG "*) return 0 ;;   # it declared a skip — not a run
    esac
    _note_skip RAN_LEGS "$CURRENT_LEG"    # dedupes; the list is what it appends to
}

# KS-1046 / QA F-925-3: TOTAL_LEGS is checked, not trusted. Every step()
# header carries `N/TOTAL`; if a header's TOTAL disagrees with TOTAL_LEGS the
# run ABORTS naming the header, so a leg pasted in with a stale denominator
# cannot count under one total and print another. Same exit as a failed leg.
step() {
    _leg_concluded
    CURRENT_LEG="${1%%/*}"
    _hdr_total="${1#*/}"; _hdr_total="${_hdr_total%% *}"
    if [ "$_hdr_total" != "$TOTAL_LEGS" ]; then
        echo ""
        echo "PREFLIGHT ABORTED — step header \"$1\" says /$_hdr_total but TOTAL_LEGS=$TOTAL_LEGS."
        echo "  The header and the count disagree, so the verdict's ratio would be wrong."
        echo "  Fix the header or TOTAL_LEGS in scripts/preflight/preflight.sh, then push again."
        echo "  (step header $CURRENT_LEG/$_hdr_total disagrees with TOTAL_LEGS $TOTAL_LEGS)"
        exit 1
    fi
    printf '\n=== %s ===\n' "$1"
}

# A leg that DELEGATES to a sub-script cannot see that sub-script's own advisory
# skip, because the sub-script exits 0 either way. Capture the output, show it
# unchanged, and propagate the skip upward so the verdict counts the leg as
# skipped rather than run. (QA F-925-2's "give delegating legs a way to report a
# sub-script's advisory skip upward".)
run_delegated() {
    _rd_out=$("$@" 2>&1); _rd_rc=$?
    printf '%s\n' "$_rd_out"
    case "$_rd_out" in
        *"SKIP (advisory)"*)
            _rd_reason=$(printf '%s\n' "$_rd_out" | grep -m1 'SKIP (advisory)' | sed 's/.*SKIP (advisory) — *//')
            _note_skip SKIPPED_ADVISORY "$CURRENT_LEG"
            echo "  ^ leg $CURRENT_LEG counted as SKIPPED (advisory), not run: $_rd_reason"
            ;;
    esac
    return $_rd_rc
}

# Record a skip AND print it. Dedupe per leg so a leg cannot be counted twice.
_note_skip() {  # $1 = list-var name, $2 = leg
    case " $(eval "printf '%s' \"\$$1\"") " in
        *" $2 "*) : ;;
        *) eval "$1=\"\${$1} \$2\"" ;;
    esac
}
skip_stack() {
    echo "SKIP — local stack not up on $GATEWAY (start it to run this leg)"
    _note_skip SKIPPED_STACK "$CURRENT_LEG"
}
skip_advisory() {
    echo "SKIP (advisory) — $1"
    _note_skip SKIPPED_ADVISORY "$CURRENT_LEG"
}

step "1/15  OpenAPI spec drift (generated spec vs Zod source)"
# KS-691: this leg needs BOTH the root install (tsx) and packages/shared's NESTED
# one (its own @types/node ^20). With the root present and the nested absent —
# what an interrupted `npm ci` or a hand-symlinked node_modules leaves — tsc
# resolves the hoisted @types/node 26, which dropped crypto.JsonWebKey, and fails
# in packages/shared/src/crypto/jwks.ts. That is a successful compile producing a
# TYPE error, so it matches none of the install-failure signatures below and fell
# through to "FAIL — spec drifted" on a spec that had not drifted. Establish the
# precondition first: no install is an install problem, never drift.
if ! bash scripts/preflight/deps-present.sh; then
    # KS-991: an absent workspace install is an ENVIRONMENT condition, not a gate
    # result. deps-present.sh says so in its own words ("This is NOT spec drift")
    # and names the remedy — but that text is 13 legs above the verdict, and the
    # run still ends on the generic "PREFLIGHT FAILED", which reads as a real red
    # to anyone who does not scroll back. A fresh `git worktree` is a normal thing
    # to push from and ALWAYS produces this, so the shape is common and the wrong
    # reading is `--no-verify`. Tracked separately so the summary can name it.
    fail=1
    env_fail=1
else
    drift_out=$(npm run --silent check:openapi 2>&1)
    drift_rc=$?
    if [ "$drift_rc" -eq 0 ]; then
        echo "OK — spec is in sync"
    elif printf '%s' "$drift_out" | grep -q 'does not match binary version\|Cannot start service: Host version\|installed esbuild for another platform'; then
        # KS-376: the root esbuild lock is inconsistent, so host tsx (which
        # generate-openapi runs on) crashes before it can compare anything. That's
        # a tooling defect, not spec drift — advise, don't block. CI gates the real
        # drift once KS-376 unblocks host tsx.
        skip_advisory "host tsx is broken by the KS-376 esbuild lock inconsistency; cannot check drift locally."
        echo "  Fix: see KS-376. This leg works again once the root esbuild lock is repaired."
    elif printf '%s' "$drift_out" | grep -q "TS2307: Cannot find module\|command not found\|Cannot find package\|Cannot find module"; then
        # KS-469: a stale/absent host workspace install fails the check:openapi
        # chain (tsc missing a dep, or tsx itself absent) long before any spec is
        # compared — announcing that as "spec drifted" cost a 45-min hunt on a
        # green platform (2026-07-16). git pull updates the locks but installs
        # nothing, and image builds run npm ci INSIDE Docker, so the host tree
        # silently rots. This IS a blocker for this leg — but the fix is an
        # install, not a spec regen.
        echo "STALE — host workspace install is behind package-lock.json; this is an install problem, NOT spec drift."
        echo "  Fix: (cd Blockchain/Dev && npm ci) then re-run preflight."
        printf '%s\n' "$drift_out" | tail -5
        fail=1
    else
        echo "FAIL — spec drifted; run 'npm run generate-openapi' and commit"
        printf '%s\n' "$drift_out" | tail -5
        fail=1
    fi
fi

step "2/15  Lockfile clean-room (npm ci --dry-run per standalone lock)"
if run_delegated bash scripts/preflight/lockfile-cleanroom.sh; then
    echo "OK — all locks clean-room-installable"
else
    echo "FAIL — see regeneration commands above"
    fail=1
fi

step "3/15  Spec-auth conformance (unauth requests to bearer-authed ops must 401/403)"
if curl -sf -o /dev/null "$GATEWAY/health" 2>/dev/null; then
    # The sweep imports `yaml` from its own standalone member (ESM resolves
    # node_modules upward from the script file — NODE_PATH is not an option).
    # First run on a clone: install the member's deps; never the root lock (KS-376).
    if [ ! -d scripts/preflight/node_modules/yaml ]; then
        echo "(first run — installing scripts/preflight deps)"
        (cd scripts/preflight && npm ci --ignore-scripts --no-audit --no-fund >/dev/null 2>&1)
    fi
    if [ ! -d scripts/preflight/node_modules/yaml ]; then
        skip_advisory "could not install scripts/preflight deps (offline?); CI runs this leg regardless."
        echo "  Fix: cd scripts/preflight && npm ci"
    elif node scripts/preflight/spec-auth-conformance.mjs --base "$GATEWAY"; then
        echo "OK — auth enforcement matches the spec"
    else
        echo "FAIL — a bearer-authed operation answered unauthenticated (KS-375 class)"
        fail=1
    fi
else
    skip_stack
fi

step "4/15  Path resolvability (every spec'd path must route — KS-473 class)"
if curl -sf -o /dev/null "$GATEWAY/health" 2>/dev/null; then
    if [ ! -d scripts/preflight/node_modules/yaml ]; then
        skip_advisory "scripts/preflight deps missing (see step 3)."
    elif node scripts/preflight/path-resolvability.mjs --base "$GATEWAY"; then
        echo "OK — every published path routes to a handler"
    else
        echo "FAIL — a published path is unroutable (KS-473 class)"
        fail=1
    fi
else
    skip_stack
fi

# --- scripts/audit deps, installed ONCE and BEFORE the first leg that needs them ---
# Peter's #796 review: this install lived at the standalone-lock leg, but the
# audit-contract leg runs BEFORE it and spawns
# audit-locks.mjs (via gate-exit-codes.test.mjs) and that imports `semver` from
# scripts/audit/node_modules. So leg 5 ran BEFORE the thing it depends on was
# installed, and on a fresh clone or a per-ticket worktree it failed 3 of 54 with
# "expected exit 3, got 1" — the module-not-found throws before the baseline
# validation the cases are actually about. Measured: 54/51/3 on a clean worktree
# at 486372571, 54/54/0 with the deps installed and nothing else changed.
#
# THE CLASS, because this is the second instance in one day: a gate — like a
# remedy — is executed by someone standing where the READER stands, or it is
# untested. The leg passed for everyone whose deps were already installed, which
# is the author and nobody else. The other instance was a rotation script whose
# documented remedy silently no-opped for anyone but its author (F-731-01).
#
# Installed once here rather than at each consumer, so the two legs cannot drift
# apart on which one is responsible for it.
if [ ! -d scripts/audit/node_modules/semver ]; then
    echo "(first run — installing scripts/audit deps)"
    (cd scripts/audit && npm ci --ignore-scripts --no-audit --no-fund >/dev/null 2>&1)
fi
if [ -d scripts/audit/node_modules/semver ]; then
    audit_deps=1
else
    audit_deps=0
fi

step "5/15  Audit-contract suites (the validator BOTH gates import — KS-763)"
# QA finding A: `npm run audit:contract` — the cases that hold the baseline
# contract and the lockfile corpus honest — was run by NOTHING. Not by CI (the
# workflows invoke the gates, not their tests), not by preflight, not by any
# other npm script. A suite no runner reaches is a suite nobody has seen fail:
# it can rot to zero cases, or start throwing at import, and every gate that
# leans on the contract it guards goes on reporting OK.
#
# This leg CANNOT skip: if it cannot run, that is itself the finding.
#
# Peter's #796 review, note 1 — correcting this comment rather than leaving it:
# it used to justify the cannot-skip by saying the leg "touches no network", and
# that stopped being true when the QA F2 change gave the gates POSITIVE CONTROL
# cases. Those run each gate to completion, which means a real `npm audit` and a
# registry bulk fetch. So the leg does touch the network — twice, at 120s
# timeouts, on top of legs 6 and 7 doing the same work.
#
# The cannot-skip stands anyway, on the better ground: an offline run still
# reaches every case, because exit 2 satisfies the cases' `notEqual(code, 3)`.
# There is no red offline. The reason changed; the rule did not.
# security-scan.yml's `NOT continue-on-error` rests on this same corrected
# ground. The duplicated audit work is real and is filed, not fixed here.
contract_out=$(npm run audit:contract --silent 2>&1)
contract_rc=$?
# A run that exits 0 having executed ZERO cases is a launch fault wearing a
# pass's costume, so the count is asserted rather than the exit code alone.
#
# KS-763 QA F1: this used to assert a FLOOR OF 1 — `-lt 1` — which the suites
# clear with a single surviving case. The failure it was written to catch is
# suite ROT, and rot from 54 cases to 1 passed it while printing
# "OK — 1 audit-contract cases pass". The count is now compared for EQUALITY
# against a committed expectation.
#
# Why a committed number and not a derived one: the count can only be derived
# from the same suite files that produce it, and any such derivation shrinks
# exactly when they do — so it cannot detect the thing this check exists to
# detect. A stored expectation is the only value that survives the files being
# gutted. The cost is that adding a case fails this leg until the number is
# updated; that is deliberate. Changing it is one line in a reviewed diff, next
# to the cases that justify it, which is the point.
contract_cases=$(printf '%s\n' "$contract_out" | grep -oE ' tests [0-9]+' | tail -1 | grep -oE '[0-9]+')
contract_expected=$(tr -d '[:space:]' < scripts/audit/expected-case-count 2>/dev/null)
if [ "$audit_deps" -eq 0 ]; then
    # NOT a skip, and deliberately not the "suites are red" line below: the suites
    # were never reached. Naming the missing dependency is the whole point — the
    # old failure mode reported a launch fault as three red assertions about exit
    # codes, which points the reader at the gate instead of at their tree.
    echo "FAIL — scripts/audit deps are missing, so the contract suites cannot run."
    echo "  gate-exit-codes.test.mjs spawns audit-locks.mjs, which imports semver from"
    echo "  scripts/audit/node_modules. Without it the spawn exits 1 (ERR_MODULE_NOT_FOUND)"
    echo "  and three cases report 'expected exit 3, got 1' — a launch fault, not a verdict."
    echo "  Fix: (cd Blockchain/Dev/scripts/audit && npm ci)"
    fail=1
elif [ "$contract_rc" -ne 0 ]; then
    echo "FAIL — the audit-contract suites are red; the gates' validator cannot be trusted until they pass"
    printf '%s\n' "$contract_out" | tail -20
    fail=1
elif [ -z "$contract_expected" ]; then
    echo "FAIL — scripts/audit/expected-case-count is missing or empty; the case count cannot be asserted"
    fail=1
elif [ -z "$contract_cases" ]; then
    echo "FAIL — the audit-contract suites reported no case count; a suite that runs zero cases has not passed"
    printf '%s\n' "$contract_out" | tail -20
    fail=1
elif [ "$contract_cases" -ne "$contract_expected" ]; then
    echo "FAIL — the audit-contract suites ran $contract_cases cases, expected $contract_expected."
    echo "  FEWER means cases were lost or stopped registering — the gates' validator is less guarded than the number claims."
    echo "  MORE means cases were added: update scripts/audit/expected-case-count to $contract_cases in the same commit."
    fail=1
else
    echo "OK — $contract_cases audit-contract cases pass (expected $contract_expected)"
fi

step "6/15  npm-audit gate (advisories vs triaged baseline — KS-470)"
node scripts/audit/audit-gate.mjs
audit_rc=$?
if [ "$audit_rc" -eq 0 ]; then
    echo "OK — no advisories outside the triaged baseline"
elif [ "$audit_rc" -eq 3 ]; then
    # Exit 3 = the gate REFUSED to report a verdict on an input it cannot trust:
    # a malformed or unparseable baseline, or (KS-763 QA F4) an `npm audit`
    # report whose shape it cannot read. That last one used to exit 2, which this
    # table reads as SKIP — so a broken audit tool produced PREFLIGHT PASSED.
    # The gate's own line above names which cause; this branch must not assert
    # one of them, or it will confidently misreport the other two.
    echo "FAIL — the audit gate REFUSED to report a verdict (see its line above: a malformed or"
    echo "  unparseable baseline, or an unreadable npm-audit report). Not a skip: nothing was"
    echo "  established, and an entry missing its fields suppresses an advisory silently."
    fail=1
elif [ "$audit_rc" -eq 2 ]; then
    skip_advisory "npm audit could not run (offline / registry unreachable)"
else
    echo "FAIL — new or lapsed advisories; triage them (fix, or reasoned baseline entry with a ticket)"
    fail=1
fi

step "7/15  standalone-lock advisories (each service's OWN lock — KS-531)"
# KS-691: audit-locks.mjs imports `semver`, which NO package.json in the tree
# declared — it resolved only as a hoisted transitive of the ROOT install. So in
# any tree without that install (a fresh git worktree, a fresh clone) the leg died
# with ERR_MODULE_NOT_FOUND and the FAIL below announced it as a standalone-lock
# advisory finding: a different problem entirely, pointing at the locks instead of
# at a missing dev dependency. semver is now declared by scripts/audit's own
# standalone member — outside the workspaces list, so installing it never touches
# the root lock (KS-376) — and this installs it on first run exactly as step 3
# does for scripts/preflight. An offline install failure is a SKIP, matching this
# leg's own exit-2 semantics: it cannot reach the registry either way.
# The install itself now runs ONCE, above leg 5 — the first leg that needs it.
# This leg keeps its own exit-2 SKIP semantics unchanged for the offline case;
# it just reads the result instead of repeating the install.
if [ "$audit_deps" -eq 0 ]; then
    skip_advisory "could not install scripts/audit deps (offline?); this leg needs semver."
    echo "  Fix: (cd Blockchain/Dev/scripts/audit && npm ci)"
    locks_rc=2
else
    node scripts/audit/audit-locks.mjs
    locks_rc=$?
fi
if [ "$locks_rc" -eq 0 ]; then
    echo "OK — no standalone-lock advisories outside the triaged baseline"
elif [ "$locks_rc" -eq 3 ]; then
    # As leg 6, plus (KS-763 QA F9) a corpus that could not be established — a
    # malformed OUT_OF_SCOPE_LOCKS entry, a lapsed exclusion fuse, or a zero
    # corpus. Those used to throw uncaught and exit 1, which this table reported
    # as "a standalone lock pins an advisory" — pointing the reader at the locks
    # when the broken thing was the exclusion list.
    echo "FAIL — the lock-advisory gate REFUSED to report a verdict (see its line above: a malformed"
    echo "  or unparseable baseline, or a corpus/exclusion list that cannot be trusted). Not a skip:"
    echo "  a baseline that cannot carry its own reasons is not a baseline."
    fail=1
elif [ "$locks_rc" -eq 2 ]; then
    skip_advisory "lock audit could not run (offline / registry unreachable / unreadable lock)"
else
    echo "FAIL — a standalone lock pins an advisory the root audit cannot see; triage it (bump the pin, or a reasoned baseline entry with a ticket)"
    fail=1
fi

step "8/15  Served-spec consistency (/api/docs/openapi.json vs .yaml — KS-656)"
if curl -sf -o /dev/null "$GATEWAY/health" 2>/dev/null; then
    if [ ! -d scripts/preflight/node_modules/yaml ]; then
        skip_advisory "scripts/preflight deps missing (see step 3)."
    else
        node scripts/preflight/spec-endpoint-consistency.mjs --base "$GATEWAY"
        spec_rc=$?
        if [ "$spec_rc" -eq 0 ]; then
            :
        elif [ "$spec_rc" -eq 2 ]; then
            skip_advisory "gateway unreachable for the served-spec probe"
        else
            echo "FAIL — the served spec routes disagree (KS-656 class)"
            fail=1
        fi
    fi
else
    skip_stack
fi

step "9/15  No tracked credentials (KS-646 — negation made the hardening unable to hold)"
if ! bash scripts/preflight/no-tracked-credentials.sh; then
    fail=1
fi

step "10/15  Bare-path shell scripts must be executable in the INDEX (KS-667 F-16 / KS-751)"
if ! bash scripts/preflight/bare-path-scripts-executable.sh; then
    fail=1
fi

step "11/15  Pinned actions must say what is pinned (KS-751 ask 4)"
if ! bash scripts/preflight/action-pins-labelled.sh; then
    fail=1
fi

step "12/15  Every shell test suite must be REACHED by the runner (KS-731 / QA F-800-07)"
# QA F-800-07: a 114-line suite shipped with ZERO invocations, inside the very PR
# whose purpose was to stop a checker silently re-opening — and the hole it was
# written to guard (F-800-05) was live at the same time. Third occurrence of the
# class, second inside a commit written to close the first.
#
# Measured on that branch: of 9 tracked *.test.sh, 5 were invoked and 4 were not,
# and the 4 held 126 passing cases protecting nothing. Per-file wiring had failed
# on nearly half its instances, so this leg enforces the PROPERTY instead: a
# tracked suite the runner cannot reach fails the push, by name.
#
# It asks `run-shell-suites.sh` rather than re-globbing, so the runner stays the
# single definition of "reached" and this leg cannot drift from what CI runs —
# the same reason `check-slot-credentials.sh` now sources .env instead of
# re-implementing a shell parser.
if ! run_delegated bash scripts/run-shell-suites.sh --check-unreached; then
    fail=1
fi

step "13/15  The runtime stage must re-link @secuura/shared (KS-921 + the KS-490 sibling)"
# `@secuura/shared` is a hand-made, UNDECLARED symlink that every Dockerfile
# consuming the shared-builder stage creates itself. Nothing in any package.json
# declares it, so no dependency tool can notice when a stage stops creating it —
# and it has already failed once: #851's second commit exists because
# `npm prune --omit=dev` removed the link and three runtime stages copied the
# pruned tree without re-creating it, shipping images that crashed on start.
# governance re-linked; nft-certificate, referral and staking did not. A reviewer
# reading four Dockerfiles side by side caught it, which is not a control.
#
# The guard carries a second, REPORT-ONLY assertion (the KS-490 dev-tree
# invariant). Report-only is deliberate: a guard that goes in red teaches
# everyone to ignore the guard. It blocks under SHARED_RELINK_STRICT=1, which is
# what its own suite asserts against, so the non-blocking clause still has a
# red-proof with an exit code behind it.
if ! bash scripts/check-shared-relink.sh; then
    fail=1
fi

step "14/15  Every shell test suite must actually RUN (KS-731 / QA FR-800-03)"
# Leg 12 proves every suite is FINDABLE. Nothing proved any of them RUNS, and
# those are different properties. Measured at e26cfce2b:
#
#   - GitHub Actions is retired for this repository (Kam, 2026-08-27; see
#     CONTRIBUTING.md), so BOTH `run: bash scripts/run-shell-suites.sh` workflow
#     steps are dormant.
#   - `npm test` is `npm run test --workspaces`, which runs each WORKSPACE's test
#     script. `test:shell` is a ROOT script and is not a workspace, so npm test
#     never reaches it.
#   - Leg 12 is `--check-unreached`, which exits before the run block.
#
# So the pre-push hook was the only gate that executed at all, and it ran no
# suite. The net effect of the F-7 fix on EXECUTION was zero: the suites became
# findable, not run — which left `check_slot_credentials.test.sh`, the guard for
# the F-800-05 hole, executing only when a human remembered to type a command.
#
# THE COST IS A NUMBER, NOT AN ARGUMENT. Full set of 10 suites: 38-39s
# wall-clock, measured 2026-09-04 on an M-series laptop over two runs.
#
# QA R2-5/R2-8: the figure shipped here was "9 suites: 40.0s", taken on a tree
# that no longer exists — this branch forked at 0332df892 and both #800's later
# commits and this one add suites. A cost quoted for a different tree is the
# kind of number a reviewer checks once and then trusts forever, so it is
# re-measured here and given as a RANGE over repeated runs rather than a single
# reading, which is all a wall-clock on a shared laptop can honestly support.
#
# It is printed on every run below anyway, so whoever next asks "is this too
# slow for a hook?" argues with a measurement taken on their own machine rather
# than with an impression — and that printed number, not this comment, is the
# one to trust.
#
# THE SUITES RUN IN A DE-SLOTTED ENVIRONMENT, and that is load-bearing.
# `.githooks/pre-push` sources `systemTest/slot-target.sh` before calling this
# script (KS-691, so the stack-dependent legs probe THIS slot's gateway). That
# sourcing EXPORTS AKTO_PREFIX, SECUURA_ARTIFACT_SUFFIX and ~20 more. Two of the
# suites — stack_env.test.sh and slot_target.test.sh — are unit tests of how
# those values are DERIVED from a slot number, and they read them as
# `${AKTO_PREFIX:-akto-s$SLOT}`, so an ambient value wins and the assertion
# compares the shell's answer with itself.
#
# Measured: sourcing slot-target.sh and then running the two suites reproduces
# the hook's exact numbers, 24/1 and 61/5, against 25/0 and 66/0 in a clean
# shell. Running a derivation test inside an already-targeted shell is a
# category error, not a flake — this clears the targeting for the suite run
# only, and leaves it in place for every other leg.
#
# The clear-list is MEASURED, not listed. Sourcing slot-target.sh in a throwaway
# subshell and diffing the environment before against after names every variable
# it actually adds — 39 of them here (QA R2-8: this said 40 while the sentence
# thirteen lines below said 39; re-measured against the real slot-target.sh, it
# is 39, and the leg prints the count it actually cleared on every run anyway).
# A hand-written list, or one grepped from
# its `export` lines, misses the ones it sets indirectly: GATEWAY_PORT,
# STACK_PREFIX, POSTGRES_EXTERNAL_PORT and the CARDANO_* ports appear on no
# `export` line at all, and a grep-derived list left stack_env still red at 24/1.
# The subshell keeps the sourcing out of THIS process, so the other legs keep the
# slot targeting they need — and it runs under `env -i` because by the time this
# leg executes the hook has ALREADY sourced slot-target.sh into our environment.
# Diffing from a polluted parent measures nothing: everything is already set, the
# `${VAR:-default}` forms keep their existing values, and the before/after delta
# comes back EMPTY. Measured: 0 variables from a polluted parent, 39 from a clean
# one. `env -i` makes the measurement independent of who is calling us.
slot_target_src="../../systemTest/slot-target.sh"
slot_polluted=$(cd ../.. 2>/dev/null && env -i HOME="$HOME" PATH="$PATH" bash -c '
    b=$(mktemp); a=$(mktemp)
    env | sort > "$b"
    . systemTest/slot-target.sh >/dev/null 2>&1 || true
    env | sort > "$a"
    comm -13 "$b" "$a" | cut -d= -f1
    rm -f "$b" "$a"
  ' 2>/dev/null | grep -E '^[A-Z_][A-Z0-9_]*$' | grep -vE '^(OLDPWD|PWD|SHLVL|_|HOME|PATH)$' | sort -u)
# POSITIVE CONTROL. An empty list would mean the measurement stopped working (the
# file moved, or sourcing failed) and the suites would then run in the polluted
# environment while this leg still printed a pass — the precise shape this leg
# exists to close. Refuse instead of degrading quietly.
if [ -z "$slot_polluted" ]; then
    echo "FAIL — could not measure what $slot_target_src exports."
    echo "       Refusing to run the shell suites without de-slotting: two of them"
    echo "       are derivation tests and would compare the shell's answer with"
    echo "       itself. Fix the measurement, do not skip the de-slotting."
    fail=1
else
    env_clear=()
    while IFS= read -r v; do [ -n "$v" ] && env_clear+=( -u "$v" ); done <<< "$slot_polluted"
    echo "de-slotted $(printf '%s\n' "$slot_polluted" | grep -c .) variable(s) for the suite run"
    shell_suites_started_at=$SECONDS
    if ! env "${env_clear[@]}" bash scripts/run-shell-suites.sh; then
        fail=1
    fi
    printf 'shell suites wall-clock: %ss\n' "$((SECONDS - shell_suites_started_at))"
fi

step "15/15  Every check-*.sh guard must have a HOME, and the wired ones must pass (KS-926)"
# KS-926: of the 20 `check-*.sh` guards, THREE ran from a live entry point and
# seventeen ran from NONE — including check-no-sql-injection.sh and
# check-no-trust-header-reads.sh. A guard nothing invokes is a check that CANNOT
# FAIL, and it is worse than no guard: twenty named checks read as coverage to
# anyone auditing the tree. Four were not rotten — they were wired to
# pr-security-gates.yml / security-scan.yml and their RUNNER was switched off
# when Actions was retired, and nobody re-homed them.
#
# This leg does TWO things and the census is the more important one:
#   --check-unreached  every tracked guard must sit in exactly one bucket
#                      (wired here / homed elsewhere / deferred WITH a reason).
#                      A guard in no bucket fails the push, naming the file.
#   (run)              the 14 guards measured green and static at fe0fd640c.
#
# The census is the property KS-926 says did not exist for guards.
# `run-shell-suites.sh --check-unreached` already enforces exactly this for
# SUITES (leg 12), and its absence for guards is precisely why this went unseen.
#
# THREE guards are deliberately NOT wired, each for a measured reason recorded
# in run-code-guards.sh: check-no-trust-header-reads.sh is red with 9 real
# findings and defaults to `fail`; check-no-demo-mutation.sh diffs against
# origin/main, which under Git Flow makes every branch look like it changed the
# demo; check-container-isolation.sh reads whole-machine Docker state and reds
# on another session's stale containers. Wiring any of those today would be the
# `--no-verify` generator KS-926 itself warns about.
if ! bash scripts/run-code-guards.sh --check-unreached; then
    fail=1
fi
if ! bash scripts/run-code-guards.sh; then
    fail=1
fi

echo ""
# =============================================================================
# KS-1046 — THE VERDICT NAMES THE CORPUS IT ACTUALLY COVERED
# =============================================================================
# Counting is done here rather than at each leg so there is ONE place the
# summary can be read against, and so a new leg cannot be added without
# TOTAL_LEGS disagreeing with the N-of-TOTAL in its own step() header.
#
# NOT counted here: leg 2's per-lock SKIPs. Those are inside one leg's own
# corpus and are named by that leg's own summary line (KS-773 / #924). This
# level counts LEGS.
n_stack=$(printf '%s' "$SKIPPED_STACK" | wc -w | tr -d ' ')
n_adv=$(printf '%s' "$SKIPPED_ADVISORY" | wc -w | tr -d ' ')
n_skipped=$((n_stack + n_adv))
# OBSERVED, not TOTAL_LEGS - n_skipped — see _leg_concluded above (QA F-925-2).
_leg_concluded
n_ran=$(printf '%s' "$RAN_LEGS" | wc -w | tr -d ' ')

if [ "$fail" -ne 0 ]; then
    # KS-991: distinguish "your tree is not installed" from "your change is bad".
    # Same exit code — this still blocks, because a leg that cannot run has not
    # passed — but the operator is told which of the two happened, at the END of
    # the output where the verdict is actually read.
    if [ "${env_fail:-0}" -ne 0 ]; then
        echo "PREFLIGHT FAILED — but leg 1 could not RUN: this working tree has no"
        echo "  workspace install. That is an environment condition, not a finding"
        echo "  about your change, and it is what a fresh git worktree always gives."
        echo ""
        echo "  Fix:  (cd Blockchain/Dev && npm ci)   then push again."
        echo ""
        echo "  Do NOT reach for --no-verify: the gate has not judged your change yet."
        echo "  Any OTHER failures above are real and still need fixing."
        exit 1
    fi
    echo "PREFLIGHT FAILED — fix the above before pushing. ($n_ran/$TOTAL_LEGS legs ran)"
    exit 1
fi

if [ "$n_skipped" -eq 0 ] && [ "$n_ran" -eq "$TOTAL_LEGS" ]; then
    echo "PREFLIGHT PASSED — $TOTAL_LEGS/$TOTAL_LEGS legs ran."
    exit 0
fi

# Nothing skipped, yet the observed count disagrees with TOTAL_LEGS. Under the
# old subtraction this state was unrepresentable, which is why it was never
# noticed; now it is visible and must not be spent as a PASS.
if [ "$n_skipped" -eq 0 ]; then
    echo "PREFLIGHT INCOMPLETE — $n_ran/$TOTAL_LEGS legs ran and NONE declared a skip."
    echo "  Legs observed to run:$RAN_LEGS"
    echo "  A leg reached no conclusion, or TOTAL_LEGS disagrees with the step() headers."
    echo "  This is NOT a pass."
    exit 1
fi

# Some legs never ran, so nothing was established about them. Say that, and do
# not spend the word PASSED on it.
echo "PREFLIGHT INCOMPLETE — $n_ran/$TOTAL_LEGS legs ran, $n_skipped SKIPPED. Nothing failed."
if [ "$n_stack" -gt 0 ]; then
    echo "  legs$SKIPPED_STACK — local stack not up; you can clear this by starting it."
fi
if [ "$n_adv" -gt 0 ]; then
    echo "  legs$SKIPPED_ADVISORY — environment (offline / registry unreachable / deps missing)."
fi
echo "  This is NOT a pass. Do not quote it as one — say which legs ran."

# DELIBERATELY NOT BLOCKING BY DEFAULT, and the reason is a contract this file
# does not own. `.githooks/pre-push` states its own design property in terms:
#   "The preflight itself skips any leg whose deps aren't up ... so a normal
#    push is never blocked by infrastructure being off — CI is the hard gate."
# Exiting non-zero on a skip would silently invert that for every developer
# whose stack happens to be down, which is a workflow decision for whoever owns
# that contract — not a side effect of fixing a summary line. The defect this
# change was filed for is that the verdict was UNFALSIFIABLE, and naming the
# ratio fixes exactly that.
#
# PREFLIGHT_STRICT_LEGS=1 makes a skipped leg block, for CI or for anyone who
# wants the stronger property. Escape-hatch shape follows
# check-production-guard.sh's CI_ENFORCE_PRODUCTION_GUARD, defaulted the other
# way for the reason above.
if [ "${PREFLIGHT_STRICT_LEGS:-0}" = "1" ]; then
    echo "  PREFLIGHT_STRICT_LEGS=1 — refusing to pass on legs that did not run."
    exit 1
fi
exit 0
