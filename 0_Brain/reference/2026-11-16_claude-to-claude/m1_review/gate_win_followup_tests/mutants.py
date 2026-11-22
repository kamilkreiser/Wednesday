#!/usr/bin/env python3
"""QA-WIN-FOLLOWUP mutants. Each mutant: its own worktree m_<name> inside the QA clone at a given
commit, one or more exact text replacements (each must match exactly once), its own target dir
(an APFS clone of the head's, so only workspace crates rebuild), then the named cargo test run.
Usage: mutants.py <spec.json> [name ...]   spec: [{name, sha, edits:[[file, old, new]], cmd:[...]}]
Writes logs to /private/tmp/claude-501/qwf/logs/mut/<name>.log and prints one line per mutant."""
import json, os, re, subprocess, sys

W = "/private/tmp/claude-501/qwf"
CLONE = f"{W}/clone"
LOGS = f"{W}/logs/mut"
os.makedirs(LOGS, exist_ok=True)


def sh(args, **kw):
    return subprocess.run(args, capture_output=True, text=True, **kw)


def main():
    specs = json.load(open(sys.argv[1]))
    only = set(sys.argv[2:])
    for s in specs:
        if only and s["name"] not in only:
            continue
        name = s["name"]
        tree = f"{W}/m_{name}"
        if not os.path.exists(tree):
            r = sh(["git", "-C", CLONE, "worktree", "add", "-q", "--detach", tree, s["sha"]])
            if r.returncode:
                print(f"{name}: WORKTREE ERROR {r.stderr.strip()}")
                continue
        else:
            sh(["git", "-C", tree, "checkout", "-q", "--", "."])
        ok = True
        for f, old, new in s["edits"]:
            p = f"{tree}/{f}"
            src = open(p, encoding="utf-8").read()
            n = src.count(old)
            if n != 1:
                print(f"{name}: ANCHOR ERROR {f}: {n} matches of {old[:60]!r}")
                ok = False
                break
            open(p, "w", encoding="utf-8").write(src.replace(old, new))
        if not ok:
            continue
        diff = sh(["git", "-C", tree, "diff", "--stat"]).stdout.strip().splitlines()
        tgt = f"{W}/t/m_{name}"
        if not os.path.exists(tgt):
            sh(["cp", "-c", "-R", f"{W}/t/{s.get('from_target', 'h')}", tgt])
        env = dict(os.environ)
        env.update(s.get("env", {}))
        log = f"{LOGS}/{name}.log"
        with open(log, "w") as fh:
            fh.write("== diff\n" + sh(["git", "-C", tree, "diff"]).stdout + "\n== run\n")
            fh.flush()
            rc = subprocess.run([f"{W}/run.sh", tree, f"m_{name}"] + s["cmd"], stdout=fh, stderr=subprocess.STDOUT, env=env).returncode
        text = open(log, encoding="utf-8", errors="replace").read()
        failed = re.findall(r"^test (\S+) \.\.\. FAILED$", text, re.M)
        results = re.findall(r"^test result: .*$", text, re.M)
        errs = re.findall(r"^error(\[E\d+\])?: .*$", text, re.M)
        if failed:
            first = re.search(r"panicked at [^\n]*\n([^\n]*)", text)
            verdict = f"KILLED by {', '.join(failed)}; first text: {first.group(1)[:220] if first else '?'}"
        elif rc != 0 and errs:
            verdict = f"BUILD FAILED rc={rc}: {errs[0][:200] if isinstance(errs[0], str) else ''}"
            m = re.search(r"^error.*$", text, re.M)
            verdict = f"BUILD FAILED rc={rc}: {m.group(0)[:200] if m else ''}"
        elif rc == 0:
            verdict = f"SURVIVED (all green: {'; '.join(r[:60] for r in results)})"
        else:
            verdict = f"rc={rc} (see log)"
        print(f"{name}: {verdict}  [{diff[-1] if diff else 'no diff'}]")
        sys.stdout.flush()


if __name__ == "__main__":
    main()
