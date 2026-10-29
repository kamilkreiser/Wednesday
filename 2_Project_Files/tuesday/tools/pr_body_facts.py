#!/usr/bin/env python3
"""pr_body_facts.py <owner/repo> <base> <head> --gh-config <dir> [--pr N]

Prints every NUMBER and LOCATION a PR body states about its diff, computed from GitHub's own compare of
base...head, so the body is assembled by pasting this output and never by counting or reading by eye.
GET only (`gh api repos/<repo>/compare/<base>...<head>`, or `pulls/<N>/files` with --pr); nothing is written.

WHY (ledger _ledger_laptop_datasec.md, w=3 in ONE seat on 2026-10-29, promoted the same day): three PR bodies
I wrote stated a figure the diff did not hold, each caught by its gate —
  Composer #103  "lines 218-239 of the new file"   the changed lines are 223-244 (hunk +220,28 with 3 context
                 lines each side: an @@ header's start is a CONTEXT line, not a changed one);
  Composer #104  "after line 28 ... after line 276" the insertions sit after OLD lines 30 and 278 (same shape);
  HPSM-POC #241  "eight new test files"            the diff adds nine (+ one e2e spec): tallied by eye.
So this walks every patch line by line: a run of '+' lines is reported by its NEW-side range and, when nothing
was removed beside it, as "after old line N" (N = the last old line read before the run). Counts are by GitHub
status (added/modified/removed/renamed) crossed with kind (spec = *.spec.* or under e2e/; test = *.test.*,
__tests__/, test/ or tests/ dirs; else product).

REFUSES (rc 2, prints no figure) when a figure could be silently short: the compare lists >= 300 files (the API
cap), or a non-binary file with changes has no patch (GitHub truncates large patches). A count printed beside
a cap is the 2026-08-14 board-count fault.
Arms: tests/pr_body_facts_arms.sh (the three 2026-10-29 cases above: each red claim is contradicted by the output).
"""
import argparse, json, os, re, subprocess, sys

HUNK = re.compile(r"^@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@")
CAP = 300


def gh(args, cfg):
    env = dict(os.environ, GH_CONFIG_DIR=cfg)
    r = subprocess.run(["gh", "api"] + args, capture_output=True, text=True, env=env)
    if r.returncode != 0:
        sys.exit(f"pr_body_facts: gh api {' '.join(args)} failed rc {r.returncode}: {r.stderr.strip()[:300]}")
    return r.stdout


def kind(path):
    p = "/" + path
    name = path.rsplit("/", 1)[-1]
    if ".spec." in name or "/e2e/" in p:
        return "spec"
    if ".test." in name or re.search(r"/(__tests__|tests?)/", p):
        return "test"
    return "product"


def runs(patch):
    """Yield (op, new_lo, new_hi, old_lo, old_hi, after_old) for each contiguous run of changed lines."""
    out, old, new, cur = [], 0, 0, None

    def close():
        nonlocal cur
        if cur:
            out.append(cur)
        cur = None

    for line in patch.split("\n"):
        m = HUNK.match(line)
        if m:
            close()
            # a zero-count side (-30,0) names the line AFTER which the change sits, not the first one read
            old = int(m.group(1)) + (1 if m.group(2) == "0" else 0)
            new = int(m.group(3)) + (1 if m.group(4) == "0" else 0)
            continue
        if line.startswith("\\"):
            continue
        tag = line[:1]
        if tag and tag in "+-":  # "" is in every string: a trailing blank must not count as a change
            if cur is None:
                cur = {"add": [], "del": [], "after_old": old - 1}
            if tag == "+":
                cur["add"].append(new); new += 1
            else:
                cur["del"].append(old); old += 1
        else:
            close()
            old += 1; new += 1
    close()
    return out


def describe(r):
    a, d = r["add"], r["del"]
    rng = lambda xs: f"{xs[0]}" if len(xs) == 1 else f"{xs[0]}-{xs[-1]}"
    if a and not d:
        return f"+{len(a)} new lines {rng(a)} (inserted after old line {r['after_old']})"
    if d and not a:
        return f"-{len(d)} old lines {rng(d)} removed"
    return f"+{len(a)} new lines {rng(a)} replacing -{len(d)} old lines {rng(d)}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("repo"); ap.add_argument("base"); ap.add_argument("head")
    ap.add_argument("--gh-config", required=True)
    ap.add_argument("--pr", type=int, help="read pulls/<N>/files instead (the PR's own merge-base diff)")
    a = ap.parse_args()
    if a.pr:
        files = json.loads(gh(["--paginate", "--slurp", f"repos/{a.repo}/pulls/{a.pr}/files?per_page=100"], a.gh_config))
        files = [f for page in files for f in page]
        src = f"pulls/{a.pr}/files"
    else:
        c = json.loads(gh([f"repos/{a.repo}/compare/{a.base}...{a.head}"], a.gh_config))
        files = c.get("files", [])
        src = f"compare {a.base}...{a.head} (ahead {c.get('ahead_by')} behind {c.get('behind_by')}, merge-base {c.get('merge_base_commit', {}).get('sha', '?')[:8]})"
    if len(files) >= CAP:
        print(f"REFUSED rc 2: {len(files)} files listed = the API cap {CAP}; a count here could be short.")
        sys.exit(2)
    short = [f["filename"] for f in files if f.get("changes", 0) and "patch" not in f and f["status"] != "removed"
             and not re.search(r"\.(png|jpe?g|gif|ico|pdf|woff2?|ttf|zip|gz)$", f["filename"], re.I)]
    if short:
        print("REFUSED rc 2: GitHub returned no patch for: " + ", ".join(short) + " (truncated?); read those locally.")
        sys.exit(2)
    print(f"# pr_body_facts — {a.repo} — source: {src}")
    tally = {}
    for f in files:
        tally.setdefault(f["status"], {}).setdefault(kind(f["filename"]), 0)
        tally[f["status"]][kind(f["filename"])] += 1
    tot_a = sum(f.get("additions", 0) for f in files); tot_d = sum(f.get("deletions", 0) for f in files)
    print(f"FILES: {len(files)} total, +{tot_a} -{tot_d}")
    for st in sorted(tally):
        parts = ", ".join(f"{n} {k}" for k, n in sorted(tally[st].items()))
        print(f"  {st}: {sum(tally[st].values())} ({parts})")
    for f in files:
        extra = f" (from {f['previous_filename']})" if f.get("previous_filename") else ""
        print(f"\n{f['status'].upper()} {kind(f['filename'])} {f['filename']}{extra}  +{f.get('additions', 0)} -{f.get('deletions', 0)}")
        if f["status"] == "added":
            print(f"  new file, lines 1-{f.get('additions', 0)}")
            continue
        for r in runs(f.get("patch", "")):
            print("  " + describe(r))


if __name__ == "__main__":
    main()
