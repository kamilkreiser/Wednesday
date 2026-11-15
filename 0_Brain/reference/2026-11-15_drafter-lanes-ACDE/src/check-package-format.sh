#!/usr/bin/env bash
# =============================================================================
# The systemTest/* formatting gate (KS-989)
# =============================================================================
# THE DEFECT THIS EXISTS FOR: nothing between a developer's keyboard and
# `develop` ran the per-package format gates for `systemTest/*`. So a docs-only
# or test-only edit under `systemTest/` could turn `npm run format:check` red in
# a package, the author who made it never saw a failure, and the next unrelated
# author to touch that package inherited the red — usually days later, with no
# link back to the commit that caused it.
#
# Three places could have caught it and none of them looked:
#   * `.githooks/pre-push` scopes itself to `^Blockchain/Dev/` — DELIBERATELY,
#     and its own header says so ("skips instantly for vault-only / docs-only /
#     systemTest-only pushes"). The design priced a systemTest-only push as
#     costless. It is not.
#   * `preflight.sh` is invoked BY that hook, so it never ran for these pushes.
#   * GitHub Actions is retired (Kam, 2026-08-27, KS-685), so there was no backstop.
#
# SIX instances in nine days, three of them found and fixed by someone other
# than the author who caused them (KS-702/#754, KS-706/#755, KS-711/#758,
# KS-707, instance 5 on the trunk at 400517aaf, instance 6 on the trunk at
# 986c592d5). Instance 6 is the one that earned this script: it entered on
# `42e778203` and rode to develop in merge `512480ef1` (#892) — a merge whose
# whole PR lived under `systemTest/`, so the hook skipped it exactly as designed
# and a red sat on the trunk for three hours with nothing looking at it.
#
# --- WHY `format:check` AND NOT `quality` (KS-990) ---------------------------
# `npm run quality` CANNOT PASS in `systemTest/performance` or `systemTest/akto`
# today, for pre-existing reasons unrelated to formatting (a TS2540 read-only
# assignment; two unused knip exports). Wiring `quality` here would produce a
# gate that can never pass — and a gate that can never pass gets bypassed, which
# is the behaviour this ticket exists to stop. It would manufacture it.
# `format:check` is the leg that fires in every instance above, it is green in
# every package as of this commit, and it costs 0–2s per package.
# When KS-990 is closed, widening this to `quality` is a one-word change here.
#
# --- USAGE -------------------------------------------------------------------
#     printf '%s\n' "$paths" | bash systemTest/scripts/check-package-format.sh
#     bash systemTest/scripts/check-package-format.sh --all
#     bash systemTest/scripts/check-package-format.sh --list
#
# Paths on stdin are repo-relative (what `git diff --name-only` emits). Only the
# packages those paths land in are checked. `--all` checks every package and is
# what the caller uses when it cannot compute a reliable changed set — see the
# KS-854/KS-882 note in the hook: an uncomputable base is not a clean tree.
#
# --- PACKAGES ARE DISCOVERED, NOT LISTED -------------------------------------
# Any `systemTest/*/package.json` carrying a `format:check` script is in scope.
# A hardcoded list is a second implementation that something has to keep in
# agreement with reality, and nothing would — the same reasoning that makes
# `run-shell-suites.sh` a glob rather than three pasted copies. Add a package
# with a `format:check` script and it is gated automatically.
# =============================================================================

# --- KS-998 ITEM 1: AN ABSENT node_modules IS INSTALLED, NOT SKIPPED ----------
# Kam's card (secuura-ks998-formatting-gate-fails-open-on-missing-prettier, option
# a): "Hard-fail only when a tracked file of the package is in the push" - and
# "install it also". Before this, a package whose deps were absent was a named
# SKIP, and a push could pass having checked nothing in it. Now:
#
#   node_modules ABSENT   -> `npm ci` runs in a STAGING DIR on the same filesystem
#                            (systemTest/.format-gate-stage.<pid>.<random>, gitignored),
#                            and node_modules is RENAMED into the package only if the
#                            install succeeded and prettier is executable. A failed,
#                            timed-out or KILLED install therefore never leaves a
#                            partial node_modules in the package for the next push to
#                            read as "present, no prettier". Four named outcomes:
#                              INSTALLED
#                              could not install  -> SKIP (--all) / REFUSED (normal)
#                              install timed out after <n>s -> SKIP / REFUSED
#                              install not attempted (the breaker, below) -> SKIP / REFUSED
#   node_modules PRESENT, no prettier -> NEVER reinstalled over (`npm ci` wipes it):
#                            REFUSED in normal mode with the command printed, a named
#                            SKIP in --all mode.
#
# WHY normal mode REFUSES and --all SKIPS. In normal mode every selected package was
# selected BECAUSE a path of it is in the push - that is Kam's condition, evaluated.
# --all is what the hook uses when the changed set cannot be computed (KS-854/KS-882:
# no base, or a base that contains HEAD). There the condition "a tracked file of the
# package is in the push" CANNOT BE EVALUATED, so the named SKIP stays and only
# KS-1063 refuses, when NOTHING was checked.
#
# THE WATCHDOG. A wall-clock ceiling (default 120 s, FORMAT_GATE_INSTALL_TIMEOUT to
# override) kills the install. It is not redundant with `--fetch-timeout=20000`:
# measured on npm 11.5.1 against a registry that ACCEPTS the connection and never
# answers, that flag did NOT end the install (it ran to a 100 s cap and was TERMed).
# The ceiling is the only bound for that shape; nothing is claimed for the flag. (The shape
# was a listener that accepts TCP connections and sends nothing; tarball fetches and the
# update check both stalled on it.) The
# outcome is keyed on the EXIT CODE and on the artefact (prettier executable), never
# on what npm printed. `--fetch-retries=0` is what makes a plainly-unreachable
# registry fail in under two seconds: npm's own retry schedule took 70.4 s for the
# same install. `--no-update-notifier` is a deliberate addition to the ruled command
# line: with a cold cache against the real registry, default `npm ci` makes exactly ONE
# request outside the lockfile's resolved set in each of the four packages -
# `GET https://registry.npmjs.org/npm`, the update check, made even with stdout not a
# TTY - and with the flag that count is 0 in all four. It also removes one place to stall.
#
# THE BREAKER. One install that TIMES OUT means the registry is silent, and every
# further install would wait out the ceiling too (4 packages x 120 s = 8 minutes, on
# top of a preflight that already takes ~8 and an SSH idle cutoff near 6). After a
# timeout the remaining absent packages are NOT attempted, and say so. A fast failure
# does not trip it.
#
# WHAT THE INSTALL RUNS. `npm ci` with no --ignore-scripts, so the lockfile-pinned
# dependencies' lifecycle scripts run on the developer's push (fsevents in all four
# lockfiles; esbuild in performance and playwright; tsx/esbuild in akto) - exactly what
# the printed remedy `npm ci` does by hand. --ignore-scripts was not added because a
# node_modules whose scripts never ran looks complete and is not. The stage holds only
# package.json, the lockfile and .npmrc, so a root lifecycle script or a dependency that
# resolves relative to the package directory cannot be installed there; none of the four
# packages has either (a relative link to ../../observability resolves identically from
# the stage, which sits at the same depth as a package).
#
# INTERRUPTION. SIGTERM / SIGINT / SIGHUP / SIGQUIT kill npm's whole process group and remove the
# stage; any other fatal signal (USR1, ALRM, PIPE...) reaches the same cleanup through the EXIT trap.
# SIGKILL (or the machine dying) cannot be trapped: what survives is one orphaned, gitignored
# stage dir - never a partial node_modules in a package - and the next run sweeps a
# stage whose pid is dead.
#
# THE PROCESS GROUP (gate review of #1532, Minor 2). npm runs as the leader of its OWN process group
# (`perl -e 'setpgrp; exec @ARGV'`), and the watchdog, the traps and the timeout path signal the GROUP:
# signalling npm's pid left a lifecycle script's child running with ppid 1 and its cwd inside the
# deleted stage (measured with a real npm and a hanging postinstall: esbuild's install.js has a
# direct-download fallback with no timeout). A child that ignores TERM is ended by the group KILL.
# Without perl the gate cannot promise that, so it does not start the install: REFUSED (normal) /
# SKIP (--all), saying why. The tree-mode format:check is not an install and runs ungrouped without perl.
#
# THE RENAME (Minor 1). node_modules is moved into the package with rename(2) (via node), not `mv`: the
# look for an existing node_modules is not atomic with the move, and BSD `mv` onto a directory moves the
# source INSIDE it (onto a symlink, THROUGH it). rename(2) refuses a non-empty directory (ENOTEMPTY /
# EEXIST) and a symlink or file (ENOTDIR); those are `raced`: the one that arrived is kept. An EMPTY
# directory that arrives in that window is replaced - the stated residual. A marker file is put in the
# staged tree first. The move BACK (an install whose prettier does not run from the package) re-checks the
# marker INSIDE the stage after the rename (gate review of #1540, Minor 3): there is a window of about 40 ms
# (measured: the node process that renames) in which another actor can replace node_modules, so a tree
# without the marker is not ours - it is put back where it was found, or LEFT in a gitignored
# systemTest/.format-gate-aside.* dir and named, and never deleted.
#
# THE HOOK TELLS THE GATE WHEN THE BASE MAY BE STALE (KS-1422): FORMAT_GATE_BASE_MAY_BE_
# STALE=1 means the changed set was computed against a ref that is not the pushed
# branch's own remote counterpart (a stale origin/develop then names packages the
# author never touched). A refusal then says so and what to do. It changes no decision.
#
# --- KS-998 ITEM 3: WHAT THE INSTALL MAY RUN, AND WHAT IT IS HANDED (gate review of #1532, Minor 3) --------
# `npm ci` runs the dependency install scripts from the lockfile, on the developer's push, for a package the developer may not have
# touched (a stale base, a merge). The review's fixture: a lock entry whose `resolved` pointed at a local HTTP listener was fetched,
# INSTALLED, and its postinstall ran and wrote outside the repository; that script also saw NPM_TOKEN, GH_TOKEN, SSH_AUTH_SOCK and ~/.npmrc.
#   * THE LOCKFILE IS CHECKED FIRST (_check_lock_sources; package-lock.json AND npm-shrinkwrap.json): every `resolved` must start with an
#     allowed URL prefix (default https://registry.npmjs.org/) and carry an `integrity`; a `link` and a local entry must resolve INSIDE
#     the repository; bundled entries are allowed; anything else - git+, http:, file:, an unreadable lock, an unknown format - is REFUSED
#     (normal mode) / SKIPPED (--all) naming the entry, and NOTHING is fetched or run.
#   * FORMAT_GATE_LOCK_ALLOW (space-separated URL prefixes, REPLACES the default) is for a registry mirror. FORMAT_GATE_INSTALL_ENV_PASS
#     (space-separated variable NAMES) hands the install more variables. Both are read from the DEVELOPER'S ENVIRONMENT ONLY, never from
#     a file in the repository (a repo file could carry the attacker's allow-list). THREAT MODEL: lockfile content that arrives on a
#     branch or in a merge the developer did not author - not the developer's own shell, who can always `git push --no-verify`.
#   * THE INSTALL RUNS UNDER AN ALLOW-LIST ENVIRONMENT (_build_install_env) with a private HOME inside the stage: PATH, TERM=dumb, TMPDIR,
#     LANG/LC_*, the proxy and CA variables, and npm_config_*/NPM_CONFIG_* except names that look like credentials (auth, token, pass,
#     secret, cert, key). ~/.npmrc is therefore not read: a developer whose registry or proxy lives only there opts back in with
#     npm_config_userconfig=<file> (the refusal says so). The developer's default cache (~/.npm) is passed as npm_config_cache unless one
#     is set, so a warm cache and an offline push still work.
#   * STATED LIMIT: this reduces what an install script is HANDED; it is NOT a sandbox (a script can still read files by absolute path),
#     lifecycle scripts still run (no --ignore-scripts, ruled), and a malicious package hosted on an allowed registry still runs its script.
#   * Small hardenings from the same review: `_rm_stage` refuses an empty prefix and a relative path (Info 3); prettier must be a regular
#     file AND executable, not a directory (Info 5).
#
# --- KS-998 ITEM 2 (variant A'): THE GATE JUDGES THE PUSHED COMMIT, NOT THE WORKING TREE -------
# `format:check` used to run in the WORKING TREE, so a red commit whose fix was left uncommitted
# passed and landed red, and a ref that was not checked out was judged by whatever was. With
# FORMAT_GATE_TREE=<commit> (the hook sets it per pushed ref) the gate instead:
#   * DISCOVERS the packages from that commit's tree (a package the push adds is seen; one it
#     removes is not selected);
#   * ARCHIVES that commit's `systemTest/<pkg>` - plus whichever prettier config / .editorconfig /
#     .prettierignore exists at the repo root or in systemTest/ at that commit - into a gitignored
#     `systemTest/.format-gate-tree.<pid>.<random>`. The tree dir sits UNDER systemTest/ on purpose:
#     its ancestors are then the working tree's own, so the gate sees what the developer's own
#     `npm run format:check` sees (measured: a parent .editorconfig flips prettier's verdict on
#     identical bytes), and the archived ancestor config SHADOWS the working tree's where it exists;
#   * SYMLINKS the working tree's node_modules in (after item 1's install) and runs the package's own
#     `npm run format:check` UNCHANGED there.
# RESIDUALS, stated: the prettier BINARY (and the installed dependency set) come from the working
# tree's node_modules while config and sources come from the push, so a push that changes the prettier
# pin is checked with the installed version; an ancestor config the pushed commit LACKS but the
# working tree has still applies; a `prettier` key in an ancestor package.json is not archived (none
# exists today: systemTest/package.json has none); a package that exists at the commit but not in
# the checked-out tree cannot have its deps installed or borrowed and is REFUSED (normal) / skipped
# (--all) with "check out what you push". Without FORMAT_GATE_TREE the gate behaves exactly as before.
#
set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

MODE="stdin"
case "${1:-}" in
    --all)   MODE="all" ;;
    --list)  MODE="list" ;;
    "")      MODE="stdin" ;;
    *) echo "usage: check-package-format.sh [--all|--list]  (default: repo-relative paths on stdin)" >&2; exit 2 ;;
esac

# --- KS-998 item 1: the install ceiling, validated rather than guessed at ----------
# Unset or set-but-empty is the default. Anything else must be a whole number of
# seconds >= 1 (no leading zero: `08` is an octal error in bash arithmetic).
INSTALL_CEILING=120
if [ -n "${FORMAT_GATE_INSTALL_TIMEOUT:-}" ]; then
    case "$FORMAT_GATE_INSTALL_TIMEOUT" in
        *[!0-9]*|0*) _bad=1 ;;
        *)           _bad=0; [ "${#FORMAT_GATE_INSTALL_TIMEOUT}" -gt 6 ] && _bad=1 ;;
    esac
    if [ "$_bad" -ne 0 ]; then
        echo "[format-gate] FORMAT_GATE_INSTALL_TIMEOUT must be a whole number of seconds, 1 or more (got '${FORMAT_GATE_INSTALL_TIMEOUT}')." >&2
        exit 2
    fi
    INSTALL_CEILING="$FORMAT_GATE_INSTALL_TIMEOUT"
fi
# KS-998 item 3 (gate review of #1532, Minor 3). Both are read from the DEVELOPER'S ENVIRONMENT ONLY - never from a file in the
# repository, because a repository file could carry the attacker's allow-list. THREAT MODEL: lockfile content that arrives on a branch
# or in a merge the developer did not author - not the developer's own shell (who can always `git push --no-verify`).
#   FORMAT_GATE_LOCK_ALLOW        space-separated URL prefixes a lockfile entry may be fetched from; REPLACES the default
#                                 https://registry.npmjs.org/ (unset or empty = the default). Needed for a registry mirror.
#   FORMAT_GATE_INSTALL_ENV_PASS  space-separated variable NAMES the install is also handed (it runs under an allow-list environment).
LOCK_ALLOW="${FORMAT_GATE_LOCK_ALLOW:-https://registry.npmjs.org/}"
INSTALL_ENV_PASS="${FORMAT_GATE_INSTALL_ENV_PASS:-}"
for _n in $INSTALL_ENV_PASS; do
    case "$_n" in
        [A-Za-z_]*) case "$_n" in *[!A-Za-z0-9_]*) _bad=1 ;; *) _bad=0 ;; esac ;;
        *) _bad=1 ;;
    esac
    if [ "$_bad" -ne 0 ]; then
        echo "[format-gate] FORMAT_GATE_INSTALL_ENV_PASS must be space-separated variable names (letters, digits, underscore) (got '${_n}')." >&2
        exit 2
    fi
done
# Set by the hook (see the header): the changed set came from a ref that may be stale.
BASE_MAY_BE_STALE=0
[ "${FORMAT_GATE_BASE_MAY_BE_STALE:-0}" = "1" ] && BASE_MAY_BE_STALE=1
# KS-998 item 2: the commit to judge. Unset or set-but-empty is the working tree (the old behaviour).
# Anything else must resolve to a commit: a value that does not is REFUSED, never silently ignored,
# because "ignore it and judge the working tree" is exactly the defect this variable exists to remove.
TREE_SHA=""
if [ -n "${FORMAT_GATE_TREE:-}" ]; then
    TREE_SHA="$(git -C "$REPO_ROOT" rev-parse --verify --quiet "${FORMAT_GATE_TREE}^{commit}" 2>/dev/null)" || TREE_SHA=""
    if [ -z "$TREE_SHA" ]; then
        echo "[format-gate] FORMAT_GATE_TREE must name a commit that exists in this repository (got '${FORMAT_GATE_TREE}')." >&2
        exit 2
    fi
fi

# --- the toolchain, or an honest skip ----------------------------------------
# npm/node missing is an ENVIRONMENT condition, not a finding. KS-991 exists
# because an environment condition was presented as a gate failure and cost a
# diagnosis five times in one day. Say which it is.
if ! command -v npm >/dev/null 2>&1 || ! command -v node >/dev/null 2>&1; then
    echo "[format-gate] SKIP (advisory) — node/npm not on PATH; cannot check systemTest formatting."
    exit 0
fi

# --- KS-998 item 1: the install machinery --------------------------------------
now_ms()    { node -e 'process.stdout.write(String(Date.now()))'; }
fmt_secs()  { printf '%d.%d' $(( $1 / 1000 )) $(( ($1 % 1000) / 100 )); }

# KS-998 item 2 (gate review, Minor 2): npm and the tree-mode check run as the LEADER OF THEIR OWN PROCESS GROUP, and a
# timeout or an interrupt signals the group, not the pid. Signalling npm's pid left a lifecycle script's child running (ppid 1,
# its cwd inside the deleted stage): measured with a real npm and a hanging postinstall. perl's `setpgrp; exec` is used because
# bash 3.2's `set -m` would also change the terminal's foreground group of a hook that runs under git.
HAVE_PERL=0
command -v perl >/dev/null 2>&1 && HAVE_PERL=1
# _run_grouped <cmd...>: exec <cmd> as a process-group leader (its pid is its pgid). Use inside `( cd ... && _run_grouped ... ) &`
# so that $! is that leader. Without perl it runs the command ungrouped; the caller that must not (the install) refuses first.
_run_grouped() {
    if [ "$HAVE_PERL" -eq 1 ]; then
        exec perl -e 'setpgrp(0, 0); exec @ARGV or die "format-gate: cannot exec $ARGV[0]: $!\n"' -- "$@"
    fi
    exec "$@"
}
# _kill_proc <SIG> <pid>: the pid's whole process group, then the pid itself. If the pid is not a group leader no group has
# its number, so the first kill finds nothing and the second is the old behaviour.
_kill_proc() {
    kill -"$1" -- "-$2" 2>/dev/null
    kill -"$1" "$2" 2>/dev/null
    return 0
}
# _rename_dir <from> <to>: rename(2), atomically, via node. Prints nothing on success and the errno NAME on failure. rename(2)
# onto a non-empty directory fails (ENOTEMPTY/EEXIST) and onto a symlink or file fails (ENOTDIR); BSD `mv` would have moved <from>
# INSIDE the directory, or through the symlink into its target (gate review, Minor 1). An EMPTY target directory is replaced:
# that is the stated residual.
_rename_dir() {
    node -e 'try { require("fs").renameSync(process.argv[1], process.argv[2]); } catch (e) { process.stdout.write(String(e.code || "EUNKNOWN")); process.exit(1); }' "$1" "$2"
}

# Staging dirs live in systemTest/ (same filesystem as every package, so the final
# move is a rename, not a copy) and are gitignored. A leading dot keeps them out of
# the `systemTest/*/package.json` discovery glob above (bash's `*` skips dotfiles).
STAGE_PREFIX="$REPO_ROOT/systemTest/.format-gate-stage."
TREE_PREFIX="$REPO_ROOT/systemTest/.format-gate-tree."      # KS-998 item 2: the pushed commit's package, extracted
ASIDE_PREFIX="$REPO_ROOT/systemTest/.format-gate-aside."    # KS-998 item 3: a stage holding a tree that is NOT ours and could not be put back; never swept, never deleted

# The ONLY place this script deletes a directory, and it deletes only what it made:
# the path must be a single component under systemTest/ with exactly that prefix,
# must exist, and must not be a symlink (a symlink is never followed).
_rm_stage() {
    local d="${1:-}" rest
    # An empty prefix matches every path, and a relative path would be taken relative to the cwd: refuse both (gate review, Info 3;
    # unreachable today - the prefixes are assigned once, absolute - but this function is the ONE deletion, so it does not rely on that).
    [ -n "$STAGE_PREFIX" ] && [ -n "$TREE_PREFIX" ] || return 1
    case "$d" in /*) ;; *) return 1 ;; esac
    case "$d" in
        "$STAGE_PREFIX"*) rest="${d#"$STAGE_PREFIX"}" ;;
        "$TREE_PREFIX"*)  rest="${d#"$TREE_PREFIX"}" ;;
        *) return 1 ;;
    esac
    case "$rest" in ''|*/*|*..*) return 1 ;; esac
    [ -d "$d" ] && [ ! -L "$d" ] || return 1
    rm -rf "$d"
}

# A stage whose pid is DEAD was left by a run that was killed (SIGKILL cannot be
# trapped). Swept, with the same guards. A live pid, a non-numeric pid (death cannot
# be proved) and a symlink are all left alone. `ps -p` rather than `kill -0`: the
# latter reports EPERM, i.e. "failed", for a live process owned by someone else.
_sweep_dead_stages() {
    local d rest pid
    for d in "$REPO_ROOT"/systemTest/.format-gate-stage.* "$REPO_ROOT"/systemTest/.format-gate-tree.*; do
        [ -L "$d" ] && continue
        [ -d "$d" ] || continue
        [ -e "$d/.format-gate-keep" ] && continue         # holds a tree that is not ours (gate 1540 Minor 3): never swept
        case "$d" in
            "$STAGE_PREFIX"*) rest="${d#"$STAGE_PREFIX"}" ;;
            "$TREE_PREFIX"*)  rest="${d#"$TREE_PREFIX"}" ;;
            *) continue ;;
        esac
        pid="${rest%%.*}"
        case "$pid" in ''|*[!0-9]*) continue ;; esac
        ps -p "$pid" >/dev/null 2>&1 && continue
        _rm_stage "$d"
    done
}

# A prettier that is a regular file (or a symlink to one) AND executable. `-x` alone is true for a DIRECTORY named prettier (gate review,
# Info 5; npm never produces one).
_prettier_ok() { [ -f "$1/node_modules/.bin/prettier" ] && [ -x "$1/node_modules/.bin/prettier" ]; }

# _check_lock_sources <package dir> <repo root> <allowed URL prefix...>: prints NOTHING and returns 0 if every lockfile `npm ci` could
# use here (package-lock.json AND npm-shrinkwrap.json, whichever exist) is installable from the allowed sources; otherwise prints the
# first offending entry and why, and returns 1. Rules: an entry's `resolved` must start with an allowed prefix and it must carry an
# `integrity`; a `link` (and a local, non-node_modules entry such as its target) must resolve INSIDE the repository; `inBundle` /
# `bundled` entries come from their parent's tarball, which is checked; anything else - git+, http:, file:, a missing source, an
# unreadable lock, an unknown format - is refused. Nothing is run and nothing is fetched.
_check_lock_sources() {
    local dir="$1" repo="$2"
    shift 2
    node -e '
        const fs = require("fs"), path = require("path");
        const dir = process.argv[1], repo = path.resolve(process.argv[2]), allow = process.argv.slice(3);
        const bad = (what, why) => { process.stdout.write(what + ": " + why); process.exit(1); };
        const inside = (p) => {
            const r = path.relative(repo, path.resolve(p));
            return r !== "" && r !== ".." && !r.startsWith(".." + path.sep) && !path.isAbsolute(r);
        };
        const okSource = (r) => typeof r === "string" && allow.some((p) => p !== "" && r.startsWith(p));
        const source = (what, e) => {
            if (!okSource(e.resolved)) bad(what, "resolved " + String(e.resolved) + " is not under an allowed source prefix");
            if (typeof e.integrity !== "string" || e.integrity === "") bad(what, "has no integrity");
        };
        for (const name of ["package-lock.json", "npm-shrinkwrap.json"]) {
            const f = path.join(dir, name);
            if (!fs.existsSync(f)) continue;
            let lock;
            try { lock = JSON.parse(fs.readFileSync(f, "utf8")); } catch (err) { bad(name, "is not valid JSON"); }
            if (!lock || typeof lock !== "object") bad(name, "is not a lockfile object");
            if (lock.packages && typeof lock.packages === "object") {
                for (const [key, e] of Object.entries(lock.packages)) {
                    if (key === "") continue;
                    const what = name + " " + key;
                    if (!e || typeof e !== "object") bad(what, "entry is not an object");
                    if (e.link === true) {
                        if (typeof e.resolved !== "string" || !inside(path.resolve(dir, e.resolved))) {
                            bad(what, "link resolves outside the repository (" + String(e.resolved) + ")");
                        }
                        continue;
                    }
                    if (e.inBundle === true) continue;
                    if (e.resolved === undefined) {
                        const local = !/(^|\/)node_modules\//.test(key);
                        if (local && inside(path.resolve(dir, key))) continue;
                        bad(what, local ? "local entry resolves outside the repository" : "has no resolved source");
                    }
                    source(what, e);
                }
            } else if (lock.dependencies && typeof lock.dependencies === "object") {
                const walk = (deps, trail) => {
                    for (const [n, e] of Object.entries(deps)) {
                        const what = name + " " + trail + n;
                        if (!e || typeof e !== "object") bad(what, "entry is not an object");
                        if (e.bundled !== true) {
                            if (e.resolved === undefined) bad(what, "has no resolved source (version " + String(e.version) + ")");
                            source(what, e);
                        }
                        if (e.dependencies && typeof e.dependencies === "object") walk(e.dependencies, trail + n + " > ");
                    }
                };
                walk(lock.dependencies, "");
            } else {
                bad(name, "has neither packages nor dependencies (unknown lockfile format)");
            }
        }
    ' "$dir" "$repo" "$@"
}

# _build_install_env <stage>: fills INSTENV (an array of NAME=VALUE) for `env -i`. THE INSTALL RUNS UNDER AN ALLOW-LIST ENVIRONMENT
# with a private HOME inside the stage, so a dependency's install script is not handed NPM_TOKEN / GH_TOKEN / SSH_AUTH_SOCK / any
# other secret from the developer's shell, and ~/.npmrc is not read. Passed: PATH, TERM=dumb, TMPDIR, LANG/LC_*, the proxy and CA
# variables, and the npm_config_* variables EXCEPT any whose name looks like a credential (auth, token, pass, secret, cert, key);
# anything else only if FORMAT_GATE_INSTALL_ENV_PASS names it. The developer's default npm cache (~/.npm) is passed as npm_config_cache
# unless one is set, so a warm cache (and an offline push) still works. STATED LIMIT: this reduces what an install script is HANDED;
# it is NOT a sandbox (a script can still read files by absolute path), lifecycle scripts still run, and a malicious package hosted on
# the allowed registry still runs its script.
INSTENV=()
_build_install_env() {
    local stage="$1" n lc
    mkdir -p "$stage/.home" 2>/dev/null
    INSTENV=("PATH=$PATH" "HOME=$stage/.home" "TERM=dumb")
    [ -n "${TMPDIR:-}" ] && INSTENV[${#INSTENV[@]}]="TMPDIR=$TMPDIR"
    for n in $(compgen -e); do
        case "$n" in
            PATH|HOME|TERM|TMPDIR) continue ;;
            LANG|LC_*|HTTP_PROXY|HTTPS_PROXY|NO_PROXY|ALL_PROXY|http_proxy|https_proxy|no_proxy|all_proxy|SSL_CERT_FILE|SSL_CERT_DIR|NODE_EXTRA_CA_CERTS) ;;
            npm_config_*|NPM_CONFIG_*)
                lc="$(printf '%s' "$n" | tr 'A-Z' 'a-z')"
                case "$lc" in *auth*|*token*|*pass*|*secret*|*cert*|*key*) continue ;; esac ;;
            *) case " $INSTALL_ENV_PASS " in *" $n "*) ;; *) continue ;; esac ;;
        esac
        [ -n "${!n}" ] || continue             # an empty value says nothing (and would hide the cache fallback below)
        INSTENV[${#INSTENV[@]}]="$n=${!n}"
    done
    case " ${INSTENV[*]:-} " in *" npm_config_cache="*) ;; *) [ -n "${HOME:-}" ] && [ -d "$HOME/.npm" ] && INSTENV[${#INSTENV[@]}]="npm_config_cache=$HOME/.npm" ;; esac
    return 0
}

_FG_NPM_PID=""; _FG_WD_PID=""; _FG_STAGE=""; _FG_CHK_PID=""; _FG_TREE=""
_fg_cleanup() {
    local i=0
    if [ -n "$_FG_CHK_PID" ]; then
        _kill_proc TERM "$_FG_CHK_PID"
        while kill -0 "$_FG_CHK_PID" 2>/dev/null && [ "$i" -lt 20 ]; do sleep 0.1; i=$((i + 1)); done
        _kill_proc KILL "$_FG_CHK_PID"
        _FG_CHK_PID=""; i=0
    fi
    if [ -n "$_FG_TREE" ]; then _rm_stage "$_FG_TREE"; _FG_TREE=""; fi
    if [ -n "$_FG_WD_PID" ]; then kill "$_FG_WD_PID" 2>/dev/null; _FG_WD_PID=""; fi
    if [ -n "$_FG_NPM_PID" ]; then
        _kill_proc TERM "$_FG_NPM_PID"
        while kill -0 "$_FG_NPM_PID" 2>/dev/null && [ "$i" -lt 20 ]; do sleep 0.1; i=$((i + 1)); done
        _kill_proc KILL "$_FG_NPM_PID"       # always: the leader may be gone while a child that ignores TERM is not
        _FG_NPM_PID=""
    fi
    if [ -n "$_FG_STAGE" ]; then _rm_stage "$_FG_STAGE"; _FG_STAGE=""; fi
}
trap '_fg_cleanup' EXIT
trap '_fg_cleanup; exit 130' INT
trap '_fg_cleanup; exit 143' TERM
trap '_fg_cleanup; exit 129' HUP
trap '_fg_cleanup; exit 131' QUIT      # bash 3.2 does not run the EXIT trap for SIGQUIT (gate review, Minor 6)

# run_install <pkg> <dir>
# Sets INST_STATE: ok | raced | noprettier | mvfail | failed | timeout
#      INST_RC, INST_MS, INST_TAIL (the last lines npm printed - shown, never read).
run_install() {
    local p="$1" dir="$2" stage marker log f wd t0 t1 tag rn rrc keep_stage=0
    INST_STATE="failed"; INST_RC=0; INST_MS=0; INST_TAIL=""; LOCK_REASON=""; ASIDE_PATH=""
    # KS-998 item 3: look at the lockfile BEFORE anything is created, fetched or run.
    read -r -a _allow <<< "$LOCK_ALLOW"
    LOCK_REASON="$(_check_lock_sources "$dir" "$REPO_ROOT" "${_allow[@]+"${_allow[@]}"}")" || {
        INST_STATE="lockbad"; INST_RC=1; return 0
    }
    if [ "$HAVE_PERL" -ne 1 ]; then
        INST_STATE="nopgrp"; INST_RC=1; return 0       # cannot promise to end what the install starts: do not start it
    fi
    stage="$(mktemp -d "${STAGE_PREFIX}$$.XXXXXX" 2>/dev/null)" || {
        INST_STATE="nostage"; INST_RC=1; return 0
    }
    _FG_STAGE="$stage"
    for f in package.json package-lock.json npm-shrinkwrap.json .npmrc; do
        [ -f "$dir/$f" ] && cp "$dir/$f" "$stage/$f"
    done
    marker="$stage/.timed-out"
    log="$stage/.npm-ci.log"
    t0="$(now_ms)"
    # `exec` so $! is npm itself; stdin from /dev/null so a child that reads stdin cannot
    # swallow the package list this script is looping over (KS-998 robustness note).
    _build_install_env "$stage"
    ( cd "$stage" && _run_grouped env -i "${INSTENV[@]}" npm ci --no-audit --no-fund --no-update-notifier --fetch-retries=0 --fetch-timeout=20000 ) </dev/null >"$log" 2>&1 &
    _FG_NPM_PID=$!
    # The watchdog polls once a second and exits on its own when npm does; its stdio is
    # closed so it can never hold a caller's $(...) pipe open.
    (
        _i=0
        while [ "$_i" -lt "$INSTALL_CEILING" ]; do
            sleep 1
            kill -0 "$_FG_NPM_PID" 2>/dev/null || exit 0
            _i=$((_i + 1))
        done
        : > "$marker"
        _kill_proc TERM "$_FG_NPM_PID"
        sleep 2
        _kill_proc KILL "$_FG_NPM_PID"
    ) </dev/null >/dev/null 2>&1 &
    _FG_WD_PID=$!
    wait "$_FG_NPM_PID" 2>/dev/null; INST_RC=$?
    kill "$_FG_WD_PID" 2>/dev/null; wait "$_FG_WD_PID" 2>/dev/null
    # On the timeout path npm (the leader) may exit on the watchdog's TERM before the watchdog's own KILL, which stopping the
    # watchdog above prevents: end the whole group here, so a child that ignores TERM does not outlive the stage.
    [ -e "$marker" ] && _kill_proc KILL "$_FG_NPM_PID"
    _FG_NPM_PID=""; _FG_WD_PID=""
    t1="$(now_ms)"; INST_MS=$((t1 - t0))

    if [ "$INST_RC" -ne 0 ] && [ -e "$marker" ]; then
        INST_STATE="timeout"
    elif [ "$INST_RC" -ne 0 ]; then
        INST_STATE="failed"
    elif ! _prettier_ok "$stage"; then
        INST_STATE="noprettier"
    elif [ -e "$dir/node_modules" ] || [ -L "$dir/node_modules" ]; then
        # Someone made node_modules while we installed: keep the one that arrived.
        INST_STATE="raced"
    else
        # The look above is not atomic with the rename, so the rename must itself refuse a target that appeared in between:
        # rename(2) does (a non-empty directory: ENOTEMPTY/EEXIST; a symlink or a file: ENOTDIR), `mv` did not (it moved the
        # tree INSIDE the directory, or through the symlink into its target - gate review, Minor 1).
        tag=".format-gate-moved.$$"
        : > "$stage/node_modules/$tag" 2>/dev/null          # proves, after the rename, that what is there is the tree WE moved
        rn="$(_rename_dir "$stage/node_modules" "$dir/node_modules")"; rrc=$?
        if [ "$rrc" -ne 0 ]; then
            case "$rn" in
                ENOTEMPTY|EEXIST|ENOTDIR) INST_STATE="raced" ;;
                *)                        INST_STATE="mvfail" ;;
            esac
        elif _prettier_ok "$dir"; then
            rm -f "$dir/node_modules/$tag"
            INST_STATE="ok"
        elif [ ! -f "$dir/node_modules/$tag" ]; then
            # Not our tree any more (another actor replaced it after the rename): it is not ours to move or delete.
            INST_STATE="raced"
        else
            # Prettier ran from the stage and does not run from here: the install embeds its own path (an absolute symlink,
            # say). Leaving this node_modules in the package would be the very state staging exists to prevent - "present,
            # no prettier" - so rename it BACK into the stage, which is then removed. Not reproduced for any of the four
            # lockfiles (0 files embed the stage path).
            rn="$(_rename_dir "$dir/node_modules" "$stage/node_modules")"; rrc=$?
            if [ "$rrc" -ne 0 ]; then
                INST_STATE="mvstuck"
            elif [ -f "$stage/node_modules/$tag" ]; then
                INST_STATE="mvbroken"
            else
                # The marker was checked BEFORE that rename, and the two steps are about 40 ms apart (measured by the gate review of
                # #1540, not "microseconds"): another actor replaced the package's node_modules in between, and THEIR tree is now
                # inside the stage, which is about to be deleted. Put it back where it was found; if that cannot be done (node_modules
                # exists again) LEAVE it - the stage is renamed aside, gitignored and never swept - and say where. Never delete it.
                rn="$(_rename_dir "$stage/node_modules" "$dir/node_modules")"; rrc=$?
                if [ "$rrc" -eq 0 ]; then
                    INST_STATE="mvforeign"
                else
                    ASIDE_PATH="${ASIDE_PREFIX}${stage##*/.format-gate-stage.}"
                    # If even the rename fails the stage stays where it is, and a keep marker stops the next run's sweep from
                    # taking it for the garbage of a dead run.
                    mv -- "$stage" "$ASIDE_PATH" 2>/dev/null || { ASIDE_PATH="$stage"; : > "$stage/.format-gate-keep"; }
                    keep_stage=1; _FG_STAGE=""
                    INST_STATE="mvaside"
                fi
            fi
        fi
    fi
    if [ "$INST_STATE" != "ok" ] && [ "$INST_STATE" != "raced" ] && [ -f "$log" ]; then
        INST_TAIL="$(tail -n 6 "$log" 2>/dev/null)"
    fi
    if [ "$keep_stage" -ne 1 ]; then _rm_stage "$stage"; fi
    _FG_STAGE=""
    return 0
}

# first_path_under <pkg>: the first changed path that selected this package (normal mode)
first_path_under() {
    printf '%s\n' "$changed_paths" | awk -v pre="systemTest/$1/" 'index($0, pre) == 1 { print; exit }'
}

# The prettier-config files that can sit ABOVE a package (repo root, systemTest/). Only those that EXIST at the
# commit are extracted: a single missing pathspec failed the whole `git archive` (measured, rc 128), so the list
# is filtered through `git ls-tree` first.
ANC_CANDIDATES=""
for _n in .editorconfig .prettierrc .prettierrc.json .prettierrc.yaml .prettierrc.yml .prettierrc.json5 \
          .prettierrc.js .prettierrc.cjs .prettierrc.mjs .prettierrc.toml prettier.config.js prettier.config.cjs \
          prettier.config.mjs prettier.config.ts .prettierignore; do
    ANC_CANDIDATES="$ANC_CANDIDATES $_n systemTest/$_n"
done

# run_check <pkg> <dir>: the package's own `npm run format:check`; sets `out` and `rc`.
# Working-tree mode is the original foreground command. With FORMAT_GATE_TREE the pushed commit's package is
# archived into a tree dir, the working tree's node_modules is symlinked in, and the same command runs THERE.
# That runs as a background job + wait, so a SIGTERM/SIGINT/SIGHUP reaches the trap at once (a foreground
# $(...) would defer it until the check returned) and the tree dir is removed.
run_check() {
    local p="$1" dir="$2" tree anc
    if [ -z "$TREE_SHA" ]; then
        out="$(cd "$dir" && npm run --silent format:check < /dev/null 2>&1)"
        rc=$?
        return 0
    fi
    tree="$(mktemp -d "${TREE_PREFIX}$$.XXXXXX" 2>/dev/null)" || {
        out="could not create a tree dir under systemTest/ - is it writable?"; rc=125; return 0
    }
    _FG_TREE="$tree"
    anc="$(git -C "$REPO_ROOT" ls-tree --name-only "$TREE_SHA" -- $ANC_CANDIDATES 2>/dev/null)"
    # The commit's files are put on disk with `read-tree` into a PRIVATE index + `checkout-index`, NOT `git archive`: archive honours
    # `export-ignore` (a pushed .gitattributes, a developer-local .git/info/attributes, core.attributesFile), which silently dropped
    # files from the check - format:check said OK where working-tree mode said FAILED (gate 1540 Minor 2). checkout-index applies the
    # same working-tree conversions (eol) as the developer's own checkout and ignores export-ignore. The temp index keeps the real
    # index (and its lock) out of it.
    # shellcheck disable=SC2086
    if ! { GIT_INDEX_FILE="$tree/.idx" git -C "$REPO_ROOT" -c core.sparseCheckout=false read-tree "$TREE_SHA" &&
           GIT_INDEX_FILE="$tree/.idx" git -C "$REPO_ROOT" ls-files -z -- "systemTest/$p" $anc |
               GIT_INDEX_FILE="$tree/.idx" xargs -0 git -C "$REPO_ROOT" checkout-index -f -q --prefix="$tree/" -- &&
           [ -d "$tree/systemTest/$p" ]; } 2>"$tree/.archive.err"; then
        out="could not extract systemTest/$p at ${TREE_SHA}: $(cat "$tree/.archive.err" 2>/dev/null)"; rc=125
        _rm_stage "$tree"; _FG_TREE=""
        return 0
    fi
    ln -s "$dir/node_modules" "$tree/systemTest/$p/node_modules"
    ( cd "$tree/systemTest/$p" && _run_grouped npm run --silent format:check ) </dev/null >"$tree/.check.log" 2>&1 &
    _FG_CHK_PID=$!
    wait "$_FG_CHK_PID" 2>/dev/null; rc=$?
    _FG_CHK_PID=""
    out="$(cat "$tree/.check.log" 2>/dev/null)"
    _rm_stage "$tree"; _FG_TREE=""
    return 0
}

# emit_refusal <pkg> <what>: normal mode, Kam's condition (KS-998, 2026-09-22: "a tracked file of the
# package is in the push") evaluated and met; the gate could not run on the package.
emit_refusal() {
    local p="$1" what="$2" sel
    sel="$(first_path_under "$p")"
    {
        echo "[format-gate] REFUSED — systemTest/$p: ${what}, and a file of this package is in the push."
        echo "[format-gate]   selected by: ${sel}"
        echo "[format-gate]   This is NOT a formatting failure: the gate could not run on this package."
        if [ -n "${INST_TAIL:-}" ]; then
            echo "[format-gate]   npm output (last lines, shown as printed, not interpreted):"
            printf '%s\n' "$INST_TAIL" | sed 's/^/[format-gate]   | /'
        fi
        if [ "${INST_STATE:-}" = "notintree" ]; then
            echo "[format-gate]   fix: check out what you push (git checkout <the branch>), then push again"
        else
            echo "[format-gate]   fix: (cd systemTest/$p && npm ci)"
        fi
        if [ "${INST_STATE:-}" = "lockbad" ]; then
            echo "[format-gate]   The gate installs only from the allowed sources (default https://registry.npmjs.org/) and runs nothing else. If the source is intended, install by hand ((cd systemTest/$p && npm ci)), or allow it for this push: FORMAT_GATE_LOCK_ALLOW=<url prefix> [...] (read from your environment only, replaces the default list), together with the npm_config_* settings for that registry (npm_config_registry, npm_config_userconfig=<file>)."
        fi
        if [ "${INST_STATE:-}" = "failed" ] || [ "${INST_STATE:-}" = "timeout" ]; then
            echo "[format-gate]   The install runs with a private HOME and without your shell's secrets, so it does not read ~/.npmrc: if your registry or proxy is configured only there, set npm_config_userconfig=\$HOME/.npmrc (or the npm_config_* variables; for a mirror also FORMAT_GATE_LOCK_ALLOW=<url prefix>) and push again; FORMAT_GATE_INSTALL_ENV_PASS=\"NAME ...\" hands the install more variables."
        fi
        if [ "${INST_STATE:-}" = "nopgrp" ]; then
            echo "[format-gate]   install perl (macOS ships it; elsewhere your package manager), or run the command above by hand."
        fi
        if [ "${INST_STATE:-}" = "timeout" ]; then
            echo "[format-gate]   a slow link needs longer: FORMAT_GATE_INSTALL_TIMEOUT=<seconds> (now ${INSTALL_CEILING})"
        fi
        if [ "$BASE_MAY_BE_STALE" -eq 1 ]; then
            echo "[format-gate]   If you did not touch systemTest/$p, your origin/develop may be stale: run git fetch origin and push again."
        fi
    } >&2
}

# --- discover the packages ----------------------------------------------------
# bash 3.2 (what macOS ships, and what the pre-push hook runs) has no
# associative arrays and no mapfile. Plain arrays and a newline-delimited string
# only.
packages=()
if [ -n "$TREE_SHA" ]; then
    # KS-998 item 2: discovered from the COMMIT, not the working tree.
    while IFS= read -r -d '' ent; do
        name="${ent#systemTest/}"
        [ -n "$name" ] || continue
        git -C "$REPO_ROOT" show "${TREE_SHA}:systemTest/${name}/package.json" 2>/dev/null | node -e '
            let s = "";
            process.stdin.on("data", (d) => { s += d; }).on("end", () => {
                try { process.exit(((JSON.parse(s).scripts) || {})["format:check"] ? 0 : 1); } catch (e) { process.exit(1); }
            });
        ' >/dev/null 2>&1 || continue
        packages+=("$name")
    done < <(git -C "$REPO_ROOT" ls-tree -z --name-only "$TREE_SHA" systemTest/ 2>/dev/null)
else
    for pj in "$REPO_ROOT"/systemTest/*/package.json; do
        [ -e "$pj" ] || continue          # an empty glob expands to itself
        dir="$(dirname "$pj")"
        node -e '
            const s = (require(process.argv[1]).scripts) || {};
            process.exit(s["format:check"] ? 0 : 1);
        ' "$pj" >/dev/null 2>&1 || continue
        packages+=("$(basename "$dir")")
    done
fi

# `"${arr[@]}"` on an EMPTY array under `set -u` raises "unbound variable" on
# bash 3.2 — and inside a command substitution that error goes to stderr,
# nothing reads it, and the assignment silently yields "". Same trap
# run-shell-suites.sh carries at QA R2-2. Use the +alternate form throughout.
if [ "${#packages[@]}" -eq 0 ]; then
    echo "[format-gate] SKIP (advisory) — no systemTest package declares a format:check script."
    exit 0
fi

if [ "$MODE" = "list" ]; then
    printf '%s\n' "${packages[@]+"${packages[@]}"}"
    exit 0
fi

# --- select the packages this run covers --------------------------------------
changed_paths=""
selected=""
if [ "$MODE" = "all" ]; then
    for p in "${packages[@]+"${packages[@]}"}"; do
        selected="${selected}${p}
"
    done
else
    changed_paths="$(cat)"
    for p in "${packages[@]+"${packages[@]}"}"; do
        if printf '%s\n' "$changed_paths" | grep "^systemTest/${p}/" > /dev/null; then
            selected="${selected}${p}
"
        fi
    done
fi

selected="$(printf '%s' "$selected" | grep -v '^$' || true)"
if [ -z "$selected" ]; then
    exit 0                            # nothing under a gated package — say nothing, cost nothing
fi

# --- run it -------------------------------------------------------------------
[ -n "$TREE_SHA" ] && echo "[format-gate] judging commit ${TREE_SHA:0:12} (the pushed content), not the working tree."
failed=0
skipped=0
checked=0
refused=0          # KS-998 item 1: could not be checked, and a file of it is in the push
installed=0        # KS-998 item 1: node_modules was absent and was installed this run
BREAKER_PKG=""      # KS-998 item 1: set to the first package whose install TIMED OUT

# A stage whose run was SIGKILLed is garbage; remove it before making new ones.
_sweep_dead_stages

# Read the selection line by line rather than relying on word splitting: this
# file is bash, but the same loop pasted into a zsh shell would not split at all
# and would run zero packages while reporting a clean pass.
while IFS= read -r p; do
    [ -n "$p" ] || continue
    dir="$REPO_ROOT/systemTest/$p"

    # Deps absent. KS-991: an environment condition, never presented as a formatting
    # red. KS-1063: if EVERY selected package is skipped the run examined nothing and
    # is refused below. KS-998 item 1: an ABSENT node_modules is now INSTALLED first;
    # only when that cannot be done does the package fall to the SKIP (--all) or the
    # REFUSAL (normal mode, where a path of the package is in the push by construction).
    if ! _prettier_ok "$dir"; then
        unready=""                       # set to a state name when the package cannot be checked
        INST_STATE=""; INST_RC=0; INST_MS=0; INST_TAIL=""
        if [ -n "$TREE_SHA" ] && [ ! -f "$dir/package.json" ]; then
            unready="notintree"          # KS-998 item 2: exists at the pushed commit, not in the checked-out tree
        elif [ -e "$dir/node_modules" ] || [ -L "$dir/node_modules" ]; then
            unready="hollow"             # present: `npm ci` would WIPE it, so never install over it
        elif [ -n "$BREAKER_PKG" ]; then
            unready="notattempted"
        else
            echo "[format-gate] systemTest/$p has no node_modules — installing with npm ci in a staging dir (ceiling ${INSTALL_CEILING}s). This runs the dependency install scripts from the lockfile, exactly as a manual npm ci does."
            run_install "$p" "$dir"
            case "$INST_STATE" in
                ok)
                    installed=$((installed + 1))
                    echo "[format-gate] INSTALLED — systemTest/$p: npm ci succeeded in $(fmt_secs "$INST_MS")s and node_modules was moved into place."
                    ;;
                raced)
                    echo "[format-gate] systemTest/$p: node_modules appeared during the install; keeping the one already there, not replacing it."
                    _prettier_ok "$dir" || unready="hollow"
                    ;;
                timeout)
                    unready="timeout"; BREAKER_PKG="$p"
                    ;;
                *)
                    unready="$INST_STATE"
                    ;;
            esac
        fi

        if [ -n "$unready" ]; then
            secs_txt="$(fmt_secs "$INST_MS")"
            case "$unready" in
                failed)       why_ref="could not install its deps (npm ci exited ${INST_RC} after ${secs_txt}s)"
                              why_skip=" and could not be installed (npm ci exited ${INST_RC} after ${secs_txt}s)" ;;
                noprettier)   why_ref="could not install its deps (npm ci exited 0 after ${secs_txt}s but node_modules/.bin/prettier is still absent or not executable)"
                              why_skip=" and could not be installed (npm ci exited 0 after ${secs_txt}s but node_modules/.bin/prettier is still absent or not executable)" ;;
                nostage)      why_ref="could not install its deps (a staging directory could not be created under systemTest/ - is it writable?)"
                              why_skip=" and could not be installed (a staging directory could not be created under systemTest/ - is it writable?)" ;;
                mvbroken)     why_ref="could not install its deps (the install embeds its staging path: prettier is not executable after the move, so node_modules was moved back out)"
                              why_skip=" and could not be installed (the install embeds its staging path: prettier is not executable after the move, so node_modules was moved back out)" ;;
                lockbad)      why_ref="the lockfile has a source the gate will not install from: ${LOCK_REASON}"
                              why_skip=" and could not be installed (the lockfile has a source the gate will not install from: ${LOCK_REASON})" ;;
                mvforeign)    why_ref="could not install its deps (the install embeds its staging path, and another actor replaced node_modules while the gate was moving ours back: their tree was put back where it was found and nothing of theirs was deleted)"
                              why_skip=" and could not be installed (the install embeds its staging path, and another actor replaced node_modules while the gate was moving ours back: their tree was put back where it was found and nothing of theirs was deleted)" ;;
                mvaside)      why_ref="could not install its deps (the install embeds its staging path, and another actor replaced node_modules while the gate was moving ours back: their tree could not be put back because node_modules exists again, and was LEFT, not deleted, at ${ASIDE_PATH})"
                              why_skip=" and could not be installed (the install embeds its staging path, and another actor replaced node_modules while the gate was moving ours back: their tree was LEFT, not deleted, at ${ASIDE_PATH})" ;;
                mvstuck)      why_ref="could not install its deps (the install embeds its staging path: prettier is not executable after the move, and node_modules could not be moved back out - npm ci in the package replaces it)"
                              why_skip=" and could not be installed (the install embeds its staging path: prettier is not executable after the move, and node_modules could not be moved back out - npm ci in the package replaces it)" ;;
                nopgrp)       why_ref="could not install its deps (perl was not found on PATH, and the install must run in its own process group so that a timeout or an interrupt ends every process it started)"
                              why_skip=" and could not be installed (perl was not found on PATH, and the install must run in its own process group so that a timeout or an interrupt ends every process it started)" ;;
                mvfail)       why_ref="could not install its deps (the staged node_modules could not be moved into place)"
                              why_skip=" and could not be installed (the staged node_modules could not be moved into place)" ;;
                timeout)      why_ref="install timed out after ${INSTALL_CEILING}s"
                              why_skip=": install timed out after ${INSTALL_CEILING}s" ;;
                notattempted) why_ref="install not attempted: the install of systemTest/${BREAKER_PKG} timed out after ${INSTALL_CEILING}s, so the registry is treated as unreachable for the rest of this run"
                              why_skip=": install not attempted: the install of systemTest/${BREAKER_PKG} timed out after ${INSTALL_CEILING}s, so the registry is treated as unreachable for the rest of this run" ;;
                notintree)    why_ref="exists at the pushed commit but is not in the checked-out tree, so its dependencies cannot be installed or borrowed here"
                              why_skip=": it exists at the pushed commit but is not in the checked-out tree, so its dependencies cannot be installed or borrowed here" ;;
                hollow)       why_ref="node_modules exists but has no prettier, so it was not reinstalled over"
                              why_skip=" (node_modules exists but has no prettier; not reinstalled over it)" ;;
            esac
            if [ "$MODE" = "all" ]; then
                # --all has no changed set, so Kam's condition (KS-998) cannot be evaluated: named SKIP.
                echo "[format-gate] SKIP — systemTest/$p deps not installed${why_skip} — skipped; --all: there is no changed set, so \"a file of this package is in the push\" cannot be evaluated. Remedy: npm ci in systemTest/$p."
                skipped=$((skipped + 1))
            else
                INST_STATE="$unready"
                emit_refusal "$p" "$why_ref"
                refused=$((refused + 1))
            fi
            continue
        fi
    fi

    # KS-998: `< /dev/null`. This loop reads its package list from the
    # here-string at its `done` on stdin, and npm hands its stdin to the script:
    # a format:check that reads stdin would swallow every package after it.
    run_check "$p" "$dir"
    checked=$((checked + 1))
    if [ "$rc" -eq 0 ]; then
        echo "[format-gate] systemTest/$p — format:check OK"
        continue
    fi

    failed=$((failed + 1))
    echo "[format-gate] systemTest/$p — format:check FAILED" >&2

    warns="$(printf '%s\n' "$out" | grep '^\[warn\] ' | grep -v 'Code style issues' || true)"

    # A non-zero exit with NO warn lines is not "no problems found" — it is an
    # unexplained failure, and reporting it as clean is the exact shape of a
    # check that cannot fail. Print what actually came back.
    if [ -z "$warns" ]; then
        echo "[format-gate]   prettier exited $rc but named no files. Raw output:" >&2
        printf '%s\n' "$out" | sed 's/^/[format-gate]   | /' >&2
        continue
    fi

    printf '%s\n' "$warns" | while IFS= read -r w; do
        rel="${w#\[warn\] }"
        full="systemTest/$p/$rel"
        # Whose red is this? The whole point of the ticket is that the bill
        # lands on the wrong person. If the file is not in this push, say so —
        # the reader should not have to work that out.
        # KS-998: -qxF, not -qx — before, "$full" was read as a PATTERN, so a path
        # containing a regex metacharacter could match the wrong line or none at all,
        # and the "(in this push)" label was not a literal statement about this push.
        if [ "$MODE" != "all" ] && printf '%s\n' "$changed_paths" | grep -xF "$full" >/dev/null; then  # KS-1728 b2: was `grep -q` after a printf pipe (closes early; EPIPE under pipefail); grep reads to EOF now, matching unchanged
            echo "[format-gate]   $full   (in this push)" >&2
        elif [ "$MODE" = "all" ]; then
            echo "[format-gate]   $full" >&2
        else
            echo "[format-gate]   $full   (NOT in this push — inherited red)" >&2
        fi
    done

    # KS-998 item 2 (the ticket's own note): the remedy printed here edits the WORKING TREE, and pushing without
    # committing that edit is how the old gate came to pass a tree that was not what was being sent. In tree mode
    # the gate judges the COMMIT, so an uncommitted fix does not help - say so.
    if [ -n "$TREE_SHA" ]; then
        echo "[format-gate]   fix: (cd systemTest/$p && npm run format) — then COMMIT it: this gate judges the pushed commit, not your working tree" >&2
    else
        echo "[format-gate]   fix: (cd systemTest/$p && npm run format)" >&2
    fi
# A here-string, NOT a pipe: `... | while read` puts the loop in a SUBSHELL, so
# every counter below would be incremented in a child and read back as 0 here —
# a gate that always reports "0 failed" no matter what prettier said.
done <<< "$selected"

trailer="${checked} package(s) checked, ${skipped} skipped, ${failed} failed"
[ "$refused" -gt 0 ]   && trailer="${trailer}, ${refused} refused"
[ "$installed" -gt 0 ] && trailer="${trailer}, ${installed} installed"
echo "[format-gate] ${trailer}"

# KS-1063 (Peter, 2026-09-29): a gate that examined NOTHING must not pass. This
# used to fall through to `[ "$failed" -eq 0 ]` and exit 0 on "0 checked, N
# skipped" — the same observable as a clean check, on exactly the systemTest-only
# pushes where this is the only gate that applies (the hook skips the platform
# preflight for them by design). It now refuses, and says in words that nothing
# was checked and that this is NOT a formatting failure, with the command that
# fixes it — the shape preflight leg 1 uses for DEPS MISSING. A run that checked
# at least one package still passes on its own verdict; the skips stay named above.
# A REFUSED package already said, in words, why the gate could not run; do not also claim
# that "every selected package was skipped" when one was refused.
if [ "$checked" -eq 0 ] && [ "$skipped" -gt 0 ] && [ "$refused" -eq 0 ]; then
    {
        echo "[format-gate] NOTHING CHECKED — every selected package was skipped, so no file's formatting was examined."
        echo "[format-gate]   This is NOT a formatting failure: the gate could not run. Install the deps it names above"
        echo "[format-gate]   (npm ci in each skipped systemTest/<package>), then push again."
    } >&2
    exit 1
fi
[ "$failed" -eq 0 ] && [ "$refused" -eq 0 ]
