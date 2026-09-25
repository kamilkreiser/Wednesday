#!/usr/bin/env python3
"""a2a_anchor.py — kit clause 1's ANCHOR CHECK for a code_patch run (2026-09-25, the Spark backend).

WHY (spark-kit 04, failure mode 9 — measured by Friday on the Spark 2026-09-23): `git apply` relocates a hunk by
searching for its context, so a header naming a line that does not exist (`@@ -902,3` on a 17-line file) still
"applies strict". checker.sh's A2 audits the hunk header's COUNTS (hunk_audit) and the apply MODE, but never the
header's START line, so the kit's deliberate break 2 ("point the brief at a line number that does not exist — clause 1
must fail") cannot fail there. This tool is that clause, run AFTER checker.sh by tasks/code_patch/spark_checker.sh.
checker.sh itself is not edited: the Ornith path is unchanged.

WHAT: for every section the checker split out of the model's diff (out.md.checker/sections.json → section_<k>.diff,
the model's AS-WRITTEN hunks, before any reanchor/context-ws rebuild), and every hunk in it whose file exists at the
pinned tip (`--- /dev/null` sections are new files — skipped, named), the hunk's OLD side (context ' ' + removed '-'
lines, an empty line read as an empty context line) must sit at EXACTLY the header's old-start line of the file at the
tip (`git -C <clone> show <tip>:<path>`, a read verb). Compared per line with trailing whitespace stripped (placement is
what is asserted here; exact bytes are A2's modes + A3i). A hunk with an empty old side (a pure insertion) is placed by
its start alone: N must be within 0..len(file).

Output: one line per hunk (`OK` / `BAD`), then `SUMMARY hunks=… ok=… bad=… skipped_newfile=…`.
Usage: a2a_anchor.py <input.json> <clone-dir> <sections.json>
rc 0 every checked hunk anchored · 1 at least one BAD · 2 usage/measure error · 5 nothing to check (no sections).
Read verbs only. Python 3 stdlib.
"""
import json
import re
import subprocess
import sys


def main():
    if len(sys.argv) != 4:
        print("usage: a2a_anchor.py <input.json> <clone-dir> <sections.json>")
        return 2
    inp_p, clone, secs_p = sys.argv[1:4]
    try:
        inp = json.load(open(inp_p, encoding="utf-8"))
        tip, subdir = inp["tip"], inp.get("repo_subdir", "")  # a doc_patch input is repo-rooted: no subdir
        secs = json.load(open(secs_p, encoding="utf-8"))
    except Exception as e:
        print(f"MEASURE ERROR: {e!r}")
        return 2
    if not secs:
        print("NOTHING TO CHECK: sections.json is empty")
        return 5
    n_h = n_ok = n_bad = n_new = 0
    for s in secs:
        path = s.get("path") or ""
        lines = open(s["file"], encoding="utf-8", errors="replace").read().split("\n")
        while lines and lines[-1] == "":
            lines.pop()  # the file's trailing newline / fence artefact (checker.sh strips these too) — not a context line
        minus_hdr = next((l for l in lines if l.startswith("--- ")), "")
        if minus_hdr.startswith("--- /dev/null"):
            n_new += 1
            print(f"SKIP section {s['n']} {path}: new file (--- /dev/null) — nothing at the tip to anchor to")
            continue
        rel = path if (not subdir or path.startswith(subdir + "/")) else f"{subdir}/{path}"
        r = subprocess.run(["git", "-C", clone, "show", f"{tip}:{rel}"], capture_output=True, text=True)
        if r.returncode != 0:
            print(f"BAD  section {s['n']} {rel}: not at the tip {tip[:12]} ({r.stderr.strip()[:160]})")
            n_bad += 1
            continue
        flines = r.stdout.split("\n")
        if flines and flines[-1] == "":
            flines = flines[:-1]
        i = 0
        while i < len(lines):
            m = re.match(r"^@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@", lines[i])
            if not m:
                i += 1
                continue
            n_h += 1
            start = int(m.group(1))
            old = []
            j = i + 1
            while j < len(lines) and not lines[j].startswith("@@") and not lines[j].startswith("--- "):
                l = lines[j]
                if l.startswith(" ") or l.startswith("-"):
                    old.append(l[1:])
                elif l == "":
                    old.append("")
                j += 1
            if not old:
                ok = 0 <= start <= len(flines)
                (n_ok, n_bad) = (n_ok + 1, n_bad) if ok else (n_ok, n_bad + 1)
                print(f"{'OK  ' if ok else 'BAD '} {rel} hunk {n_h} @@ -{start}: pure insertion, start {'within' if ok else 'OUTSIDE'} 0..{len(flines)}")
                i = j
                continue
            at = [x.rstrip() for x in flines[start - 1:start - 1 + len(old)]] if start >= 1 else []
            want = [x.rstrip() for x in old]
            if at == want:
                n_ok += 1
                print(f"OK   {rel} hunk {n_h} @@ -{start},{m.group(2) or 1}: old side ({len(old)} lines) is at line {start}")
            else:
                n_bad += 1
                found = [k + 1 for k in range(len(flines) - len(want) + 1)
                         if [x.rstrip() for x in flines[k:k + len(want)]] == want]
                where = (f"the old side actually sits at line(s) {found[:5]} — git would place it by context search, off by "
                         f"{found[0] - start:+d}") if found else "the old side is not found anywhere in the file (context not copied from the file)"
                print(f"BAD  {rel} hunk {n_h} @@ -{start},{m.group(2) or 1}: old side ({len(old)} lines) is NOT at line {start} "
                      f"(file has {len(flines)} lines); {where}")
            i = j
    print(f"SUMMARY hunks={n_h} ok={n_ok} bad={n_bad} skipped_newfile={n_new}")
    return 1 if n_bad else 0


if __name__ == "__main__":
    sys.exit(main())
