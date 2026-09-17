#!/usr/bin/env python3
"""a3b_line.py <input.json> <clone> <section.diff> <product repo path> [git apply opts ...]

A3b/A3e LINE-KEYED sites (2026-09-17, KS-1186: four of its five '-' lines are byte-identical at the tip, so a
TEXT match cannot tell which duplicate a diff edited — one edit satisfies all four). A site whose input entry
carries `"key": "line+text"` (written by night/build_input.sh when the brief's heading is `## Where (line-keyed …)`)
is proven edited only when the diff REMOVES the tip line AT THAT NUMBER and that line's tip text equals the
brief's text (`text_in_brief`). Sites without the key are NOT graded here: the checker's text predicates (PY3B /
PY3E) keep grading them exactly as before — the fallback.

How the removed line numbers are measured (never from the model's hunk headers, which drift, reanchor or apply
at an offset): the tip's product file is written into a fresh temp directory OUTSIDE any git repository, the
section is applied there with the SAME opts the checker recorded for it (strict / --recount / -C1 / reanchored
file), and `git diff --no-index -U0 <tip copy> <patched copy>` names the tip lines that actually changed. The clone
is only READ (`git show <tip>:<product>`). Consequence, stated: a byte-identical `-x`/`+x` re-emit is not an edit.

Prints one line per finding:
  MISMATCH :<n> <must_change|stays> brief=`…` tip=`…`   (the brief's text is not the tip's line at that number)
  MISSED :<n> `<text>`                                   (a must_change line-keyed site the diff did not remove)
  REMOVED :<n> `<text>`                                  (a stays line-keyed site the diff removed)
  REMOVED_LINES <n,n,…>                                  (every tip line the diff removed — the measurement)
rc 0 all line-keyed sites satisfied · 1 MISSED · 4 REMOVED (no MISSED) · 3 MISMATCH · 2 measure error.
"""
import json, os, re, subprocess, sys, tempfile

def main():
    if len(sys.argv) < 5:
        print(__doc__.split("\n")[0]); return 2
    inp, clone, section, product = sys.argv[1:5]
    opts = [o for o in sys.argv[5:] if o]
    d = json.load(open(inp, encoding="utf-8"))
    tip = d["tip"]
    sites = [s for s in (d.get("defect_line") or {}).get("sites", []) if s.get("key") == "line+text"]
    if not sites:
        print("REMOVED_LINES "); print("no line-keyed sites"); return 0
    r = subprocess.run(["git", "-C", clone, "show", f"{tip}:{product}"], capture_output=True)
    if r.returncode != 0:
        print(f"MEASURE ERROR: git show {tip[:9]}:{product} rc={r.returncode}: {r.stderr.decode(errors='replace')[:200]}"); return 2
    tip_bytes = r.stdout
    tip_lines = tip_bytes.decode("utf-8", errors="replace").split("\n")
    mismatch = []
    for s in sites:
        n = int(s["line"]); kind = "must_change" if s.get("must_change") else "stays"
        want = (s.get("text_in_brief") if s.get("text_in_brief") is not None else s.get("text_at_tip")) or ""
        have = tip_lines[n - 1] if 1 <= n <= len(tip_lines) else None
        bad = have is None or have.strip() != want.strip() or not want.strip()
        if not bad and s.get("text_at_tip") is not None and s["text_at_tip"].strip() != have.strip():
            bad = True
        if bad:
            mismatch.append(f"MISMATCH :{n} {kind} brief=`{want.strip()[:70]}` tip=`{(have or '<beyond EOF>').strip()[:70]}`")
    if mismatch:
        print("\n".join(mismatch)); return 3
    tmp = tempfile.mkdtemp(prefix="a3b_line.")
    try:
        dst = os.path.join(tmp, "tree", product)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        open(dst, "wb").write(tip_bytes)
        tipcopy = os.path.join(tmp, "tip_copy")
        open(tipcopy, "wb").write(tip_bytes)
        env = dict(os.environ, GIT_CEILING_DIRECTORIES=tmp)
        for k in ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE"):
            env.pop(k, None)
        a = subprocess.run(["git", "apply", "-p1", *opts, os.path.abspath(section)], cwd=os.path.join(tmp, "tree"),
                           capture_output=True, env=env)
        if a.returncode != 0:
            print(f"MEASURE ERROR: the product section did not apply to a copy of the tip (opts {opts}): {a.stderr.decode(errors='replace')[:300]}"); return 2
        g = subprocess.run(["git", "diff", "--no-index", "--no-color", "-U0", tipcopy, dst], capture_output=True, env=env, cwd=tmp)
        if g.returncode not in (0, 1):
            print(f"MEASURE ERROR: git diff --no-index rc={g.returncode}: {g.stderr.decode(errors='replace')[:200]}"); return 2
        removed = set()
        for m in re.finditer(r"^@@ -(\d+)(?:,(\d+))? \+\d+(?:,\d+)? @@", g.stdout.decode("utf-8", errors="replace"), re.M):
            start = int(m.group(1)); cnt = int(m.group(2)) if m.group(2) is not None else 1
            removed.update(range(start, start + cnt))
    finally:
        # quarantine, never delete: the temp dir is left for the OS temp reaper (it holds only a tip copy + patched copy)
        pass
    print("REMOVED_LINES " + ",".join(str(x) for x in sorted(removed)))
    missed = [f"MISSED :{s['line']} `{tip_lines[int(s['line'])-1].strip()[:70]}`" for s in sites
              if s.get("must_change") and int(s["line"]) not in removed]
    gone = [f"REMOVED :{s['line']} `{tip_lines[int(s['line'])-1].strip()[:70]}`" for s in sites
            if not s.get("must_change") and int(s["line"]) in removed]
    if missed: print("\n".join(missed))
    if gone: print("\n".join(gone))
    return 1 if missed else (4 if gone else 0)

if __name__ == "__main__":
    sys.exit(main())
