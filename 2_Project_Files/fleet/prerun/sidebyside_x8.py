#!/usr/bin/env python3
"""Seat X 8th: the SIDE-BY-SIDE harness (gate 227's F7), round 3 after gate 237's N2, N3 and N15. Kam's card: "Two pre-runs in scratch copies must match a normal run. If they do, ..."
It runs `prerun_x8.py run` (the tool seats will use, not stubbed) on ONE NAMED sha, once or twice AT THE SAME TIME in separate checkouts, then the REAL hook once, directly (no push, no network).
It prints NO bare MATCH (N2). For each pre-run it computes gate 237's Q8 checklist against the one hook output, row by row, and says HOLDS only if every row of every pre-run is true:
  rc           pre-run rc 0 AND hook rc 0                                        (A2: two runs failing the same way are not "it holds")
  format_gate  the pre-run's format gate rc 0 AND its [format-gate] lines equal the hook's   (A4)
  unknown      no unknown differing line, after same-text pairs are read off (N3)
  known        at most 2 known residual lines, each printed                    (A6)
  tree         tree_moved == [] AND tree_reads >= --min-tree-reads (default 15: about a 20-minute run at the 60 s read)   (A8)
  clean_end    tree_clean_end true
  legs         the legs pin's N headers, 1..N in order, and a verdict line, in BOTH outputs
  decide       prerun_decide_x8.py beside the tool, on this record and sha: QUALIFIES, `DECISION path=no-verify`, no reason lines  (A3; what the rehearsal's gatetest prints as PUSH PATH: --no-verify)
N3: the hook runs with stderr merged INTO stdout in order, the way the pre-run writes its output file, so like is compared with like; and a differing line whose same text appears on the other side
    is listed as a same-text pair (moved, not different) before anything is called unknown. A real difference (one changed word) still reads as unknown: tested.
usage: sidebyside_x8.py --sha SHA --worktree-a WT_A --worktree-b WT_B --out OUTDIR [--second-worktree WT_C] [--tool PRERUN.py] [--min-tree-reads N]
  WT_A (and WT_C) take the pre-runs, WT_B takes the hook; each is a clean checkout of SHA on a named branch, prepared by the caller, all different trees. SHA must be an UNPUSHED commit on a
  named branch that changes Blockchain/Dev (gate 237 Q8 item 2): a develop sha is refused, because the hook skips a commit already on the remote and runs no preflight.
  exit 0 HOLDS, 1 DOES NOT HOLD, 2 could not compare (a precondition failed; nothing was concluded).
THE REAL RUN IS NOT THIS SEAT'S: it belongs after a GO, by a separate mail from Wednesday. This seat proves the harness on scratch only (test_sidebyside_x8.py)."""
import argparse, collections, importlib.util, json, os, re, subprocess, sys, time

ZERO = "0" * 40
# Gate 227's residual classes, and only these, each as an exact pattern. The count allowed is the gate's: 0 to 2 lines in all (row "known").
KNOWN = [("setpgid", re.compile(r"^.*child setpgid .*Operation not permitted.*$")), ("KS-1401 postmaster", re.compile(r"^.*WARNING.*postmaster.*$"))]
KNOWN_MAX = 2
VOLATILE = [re.compile(p) for p in (r"^PRERUN sha=", r"\b\d+(\.\d+)?m?s\b", r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}", r"/private/tmp/\S+", r"/var/folders/\S+", r"\bpid \d+\b")]
HOOK_ONLY = re.compile(r"^(\[pre-push\]|\[format-gate\]|remote: |To |To github| \* \[new branch\])")
ROWS = ["rc", "format_gate", "unknown", "known", "tree", "clean_end", "legs", "decide"]


def norm(line):
    """Volatile parts of a line (timings, temp paths, the pre-run's own header) are masked, the words stay, so a changed check still shows."""
    for rx in VOLATILE[1:]:
        line = rx.sub("<v>", line)
    return line


def body(text):
    return [norm(l) for l in text.splitlines() if not VOLATILE[0].match(l) and not HOOK_ONLY.match(l)]


def diff_uncapped(a, b):
    import difflib
    out = []
    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes():
        if tag != "equal":
            out += [("pre", l) for l in a[i1:i2]] + [("hook", l) for l in b[j1:j2]]
    return out


def classify(rows):
    """-> (known, pairs, unknown). N3: a pre line and a hook line with the same text are a PAIR (the line moved, it did not differ). Pairs are read off first, once per side (a multiset
    intersection), and printed; only what is left can be known or unknown."""
    pre = collections.Counter(l for s, l in rows if s == "pre"); hook = collections.Counter(l for s, l in rows if s == "hook")
    paired = pre & hook
    left = {"pre": collections.Counter(paired), "hook": collections.Counter(paired)}
    rest = []
    for side, l in rows:
        if left[side][l] > 0:
            left[side][l] -= 1; continue
        rest.append((side, l))
    known, unknown = [], []
    for side, l in rest:
        hit = next((n for n, rx in KNOWN if rx.match(l)), None)
        (known if hit else unknown).append((side, hit or "", l))
    return known, sorted(paired.elements()), unknown


def git(wt, *a): return subprocess.run(["git", "--no-optional-locks", "-C", wt, *a], capture_output=True, text=True)


def load_tool(path):
    s = importlib.util.spec_from_file_location("prerun_tool", path); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m


def fg_lines(text): return sorted(l.strip() for l in text.splitlines() if l.startswith("[format-gate]"))


def checklist(P, rec, pre_text, hook_text, hook_rc, rows, decide_out, decide_rc, sha, branch, min_reads):
    known, pairs, unknown = classify(rows)
    pp, hp = P.parse_output(pre_text), P.parse_output(hook_text)
    n = P.N_LEGS
    legs_ok = lambda p: n is not None and p.get("headers") == list(range(1, n + 1)) and bool(p.get("verdict"))
    try:
        pre_fg = open(rec["format_gate"]["output"], errors="replace").read()
    except (OSError, KeyError, TypeError):
        pre_fg = ""
    dl = decide_out.strip().splitlines()
    r = dict(rc=rec.get("rc") == 0 and hook_rc == 0,
             format_gate=rec.get("format_gate", {}).get("rc") == 0 and fg_lines(pre_fg) == fg_lines(hook_text) and bool(fg_lines(hook_text)),
             unknown=not unknown, known=len(known) <= KNOWN_MAX,
             tree=rec.get("tree_moved") == [] and isinstance(rec.get("tree_reads"), int) and rec["tree_reads"] >= min_reads,
             clean_end=rec.get("tree_clean_end") is True, legs=legs_ok(pp) and legs_ok(hp),
             decide=decide_rc == 0 and bool(dl) and dl[0] == "QUALIFIES" and dl[-1] == f"DECISION path=no-verify sha={sha} branch={branch}" and not any(l.startswith("  ") for l in dl))
    detail = dict(pre_rc=rec.get("rc"), hook_rc=hook_rc, format_gate_rc=rec.get("format_gate", {}).get("rc"), pre_format_lines=fg_lines(pre_fg), hook_format_lines=fg_lines(hook_text),
                  known=[list(x) for x in known], same_text_pairs=pairs, unknown=[list(x) for x in unknown], tree_reads=rec.get("tree_reads"), tree_moved=rec.get("tree_moved"),
                  min_tree_reads=min_reads, tree_clean_end=rec.get("tree_clean_end"), legs_pin=n, pre_headers=len(pp.get("headers") or []), hook_headers=len(hp.get("headers") or []),
                  pre_verdict=pp.get("verdict"), hook_verdict=hp.get("verdict"), decide_rc=decide_rc, decide_out=dl)
    return r, detail


def main():
    ap = argparse.ArgumentParser(usage="sidebyside_x8.py --sha SHA --worktree-a WT_A --worktree-b WT_B --out OUTDIR [--second-worktree WT_C] [--tool PRERUN.py] [--min-tree-reads N]")
    ap.add_argument("--sha", required=True); ap.add_argument("--worktree-a", required=True); ap.add_argument("--worktree-b", required=True); ap.add_argument("--out", required=True)
    ap.add_argument("--second-worktree"); ap.add_argument("--min-tree-reads", type=int, default=15)
    ap.add_argument("--tool", default=os.path.join(os.path.dirname(os.path.abspath(__file__)), "prerun_x8.py"))
    o = ap.parse_args()
    os.makedirs(o.out, exist_ok=True); report = dict(sha=o.sha, started=time.strftime("%FT%TZ", time.gmtime()), min_tree_reads=o.min_tree_reads)
    def stop(msg):
        report["result"] = "COULD NOT COMPARE: " + msg; json.dump(report, open(o.out + "/sidebyside.json", "w"), indent=1); print(report["result"]); sys.exit(2)
    if not re.fullmatch(r"[0-9a-f]{40}", o.sha): stop("--sha must be 40 hex")
    pres = [o.worktree_a] + ([o.second_worktree] if o.second_worktree else [])
    trees = pres + [o.worktree_b]
    for wt in trees:
        h, s = git(wt, "rev-parse", "HEAD"), git(wt, "status", "--porcelain")          # X8 (N1 sweep): each read's exit code is read
        if h.returncode != 0 or h.stdout.strip() != o.sha: stop(f"{wt} is not at {o.sha[:12]} (rev-parse rc {h.returncode})")
        if s.returncode != 0: stop(f"{wt}: git status failed rc {s.returncode}, so it cannot be shown clean")
        if s.stdout.strip(): stop(f"{wt} is not clean")
        if not git(wt, "symbolic-ref", "--short", "-q", "HEAD").stdout.strip(): stop(f"{wt} is on a detached HEAD")
    if len({os.path.realpath(t) for t in trees}) != len(trees): stop("the worktrees must all differ: no two runs may share a tree")
    # the hook skips a commit any refs/remotes/origin/ ref contains (its 'onremote' case), and then runs no preflight: a develop sha cannot be compared (gate 237 Q8 item 2, A1)
    fe = git(o.worktree_b, "for-each-ref", "--contains", o.sha, "refs/remotes/origin/")
    if fe.returncode != 0 or fe.stdout.strip(): stop(f"{o.sha[:12]} is already on the remote per {o.worktree_b}'s refs/remotes/origin (or that read failed, rc {fe.returncode}): the hook would not gate it")
    if not os.path.exists(o.tool): stop(f"--tool {o.tool} does not exist")
    P = load_tool(o.tool); dec = os.path.join(os.path.dirname(os.path.abspath(o.tool)), "prerun_decide_x8.py"); cells = os.path.join(os.path.dirname(os.path.abspath(o.tool)), "prerun_expected_cells_x8.txt")
    # ---- the pre-runs, AT THE SAME TIME (Kam's card: two pre-runs), each holding its own slot, through the tool seats will use
    procs = [(wt, f"{o.out}/pre{i + 1}", subprocess.Popen(["python3", "-I", o.tool, "run", wt, f"{o.out}/pre{i + 1}", "--max-load", "1000"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, stdin=subprocess.DEVNULL)) for i, wt in enumerate(pres)]
    runs = []
    for wt, out, p in procs:
        txt = p.communicate()[0]
        if p.returncode != 0 or not os.path.exists(out + "/record.json"): stop(f"the pre-run in {wt} did not write a record: {txt[-300:]}")
        rec = json.load(open(out + "/record.json")); runs.append((wt, out, rec, open(rec["output"], errors="replace").read()))
    # ---- the hook, the real file at this sha, called directly: no push, no network. N3: stderr merged into stdout IN ORDER, as the pre-run's output file holds it
    br = git(o.worktree_b, "symbolic-ref", "--short", "-q", "HEAD").stdout.strip(); hook = os.path.join(o.worktree_b, ".githooks/pre-push")
    if not os.access(hook, os.X_OK): stop(f"{hook} is not executable")
    h = subprocess.run([hook, "origin", git(o.worktree_b, "config", "--get", "remote.origin.url").stdout.strip()], cwd=o.worktree_b, input=f"refs/heads/{br} {o.sha} refs/heads/{br} {ZERO}\n", stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    hook_text = f"HOOKRUN sha={o.sha} branch={br}\n" + h.stdout; open(o.out + "/hook.out", "w").write(hook_text)
    if "running preflight gate" not in hook_text and not h.returncode: stop("the hook ran no preflight on this commit (no Blockchain/Dev change, or a skip): there is nothing to compare against")
    b_sha = (re.match(r"HOOKRUN sha=([0-9a-f]{40}) ", hook_text) or [None, None])[1]
    allrows, holds = [], True
    for i, (wt, out, rec, pre_text) in enumerate(runs, 1):
        a_sha = (re.match(r"PRERUN sha=([0-9a-f]{40}) ", pre_text) or [None, None])[1]
        if not (a_sha == b_sha == o.sha): stop(f"the outputs do not both name {o.sha[:12]}: pre-run {i} [{a_sha}], hook [{b_sha}]")
        d = subprocess.run(["python3", "-I", dec, "decide", out + "/record.json", o.sha, "--branch", rec.get("branch", ""), "--worktree", wt, "--cells-file", cells, "--out", out + "/decision.json"], capture_output=True, text=True)
        rows = diff_uncapped(body(pre_text), body("\n".join(hook_text.splitlines()[1:])))
        r, det = checklist(P, rec, pre_text, hook_text, h.returncode, rows, d.stdout, d.returncode, o.sha, rec.get("branch", ""), o.min_tree_reads)
        ok = all(r[k] for k in ROWS); holds = holds and ok
        allrows.append(dict(pre_run=i, worktree=wt, holds=ok, rows=r, diff_lines=len(rows), **det))
    report.update(sha_in_both=True, pre_runs=allrows, result="HOLDS" if holds else "DOES NOT HOLD")
    json.dump(report, open(o.out + "/sidebyside.json", "w"), indent=1)
    print(f"{report['result']} on {o.sha}: {len(runs)} pre-run(s) against one hook run (hook rc {h.returncode}); HOLDS only if every row below is true for every pre-run")
    for a in allrows:
        print(f"  pre-run {a['pre_run']} ({'holds' if a['holds'] else 'DOES NOT HOLD'}): " + "  ".join(f"{k}={'true' if a['rows'][k] else 'FALSE'}" for k in ROWS))
        print(f"    rc pre {a['pre_rc']} hook {a['hook_rc']}; format gate rc {a['format_gate_rc']}; {a['diff_lines']} differing lines: {len(a['same_text_pairs'])} same-text pairs, {len(a['known'])} known (max {KNOWN_MAX}), {len(a['unknown'])} unknown; "
              f"tree read {a['tree_reads']} times (min {a['min_tree_reads']}), moved {len(a['tree_moved'] or [])}; headers pre {a['pre_headers']} hook {a['hook_headers']} of {a['legs_pin']}; decide rc {a['decide_rc']}")
        for l in a["same_text_pairs"]: print(f"    same-text pair (moved, both sides): {l[:200]}")
        for side, kind, l in a["known"]: print(f"    known [{kind}] ({side}): {l[:180]}")
        for side, kind, l in a["unknown"]: print(f"    UNKNOWN ({side}): {l[:220]}")
        if not a["rows"]["decide"]: print(f"    decide said: {' | '.join(a['decide_out'])[:300]}")
    sys.exit(0 if holds else 1)


if __name__ == "__main__":
    main()
