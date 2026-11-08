#!/usr/bin/env python3
"""build_tier_input.py <tier> <ticket> <out input.json> <brief.md> <brief_dir> [pin=value ...] — the input builder for
tiers test_only_input and doc_only (2026-10-31). Env NIGHT_SOURCE_CHECKOUT = the cache clone checked out at the tip
(round.sh sets it). Read-only on that clone (git rev-parse / show).

Prints `WEDNESDAY BRIEF:` + the brief on stdout (round.sh refuses an input whose builder did not use the brief as the
prompt), then one summary line. rc 0 ok · 2 REFUSED (a brief/pin fault, same convention as night/build_input.sh) ·
1 harness (no checkout, git failure).

Pins consumed: subdir= (default Blockchain/Dev), service_dir= (default: services/<x>|packages/<x>|frontend/<x> read off the
first test path), siblings=auto|none (test_only_bash: the sibling-suite no-worse leg), shared_pkg_dir= / shared_pkg_name= (defaults packages/shared, @secuura/shared; `none` = a package with no
shared build, prepare_clone.sh's "tool mode"), runner= (default: the brief's `Runner:` line), doc_check_cwd=.
"""
import json
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tier_brief as tb  # noqa: E402


def refuse(msg):
    print(f"REFUSED {msg}")
    sys.exit(2)


def git(src, *a):
    return subprocess.run(["git", "-C", src, *a], capture_output=True, text=True)


def main():
    if len(sys.argv) < 6:
        print("usage: build_tier_input.py <tier> <ticket> <out> <brief.md> <brief_dir> [pin=value ...]", file=sys.stderr)
        return 1
    tier, ticket, out, bfile, bdir = sys.argv[1:6]
    pins = dict(a.split("=", 1) for a in sys.argv[6:] if "=" in a)
    src = os.environ.get("NIGHT_SOURCE_CHECKOUT", "")
    if not src or not os.path.isdir(os.path.join(src, ".git")):
        print(f"build_tier_input: NIGHT_SOURCE_CHECKOUT is not a git checkout: {src!r}")
        return 1
    tip = git(src, "rev-parse", "HEAD").stdout.strip()
    if not re.fullmatch(r"[0-9a-f]{40}", tip):
        print("build_tier_input: cannot read the checkout's HEAD")
        return 1
    text = open(bfile, encoding="utf-8").read()
    products, tests = tb.header_files(text)
    subdir = pins.get("subdir", "Blockchain/Dev")
    m_run = re.search(r"^Runner:\s*`?([A-Za-z0-9_.-]+)", text, re.M)
    runner = pins.get("runner") or (m_run.group(1).lower() if m_run else "")

    def show(p):
        r = git(src, "show", f"{tip}:{p}")
        return r.stdout if r.returncode == 0 else None

    inp = {"tier": tier, "tip": tip, "source_checkout": src, "brief": text,
           "ticket": {"id": ticket, "brief_file": os.path.basename(bfile)}}
    if tier == "test_only_input":
        if not tests:
            refuse("test_only_input: no `Test file:` header line")
        m = re.match(r"^(?:" + re.escape(subdir) + r"/)?((?:services|packages|frontend)/[^/]+)/", tests[0])
        svc = pins.get("service_dir") or (m.group(1) if m else "")
        if not svc:
            refuse(f"test_only_input: cannot derive service_dir from {tests[0]} — pin service_dir=<services/x>")
        svc_root = f"{subdir}/{svc}/"
        for t in tests:
            if not t.startswith(svc_root):
                refuse(f"test_only_input: test {t} is not under {svc_root} (one service per round)")
        spd = pins.get("shared_pkg_dir", "packages/shared")
        spn = pins.get("shared_pkg_name", "@secuura/shared")
        if spd.lower() == "none":
            spd, spn = "", ""
        if not runner:
            refuse("test_only_input: no Runner: line / runner= pin")
        groups, perrs = tb.parse_plant(text)
        pdiff = os.path.join(bdir, "golden_red.diff")
        plant_diff = open(pdiff, encoding="utf-8").read() if os.path.isfile(pdiff) else None
        if perrs or (bool(groups) == bool(plant_diff)):
            refuse("test_only_input: need exactly one of a complete `## Plant` block or golden_red.diff"
                   + (f" ({'; '.join(perrs)})" if perrs else ""))
        cells = tb.parse_red_cells(text)
        if not cells:
            refuse("test_only_input: `## Red cells` names no cell")
        for g in groups:
            if show(g["file"]) is None:
                refuse(f"test_only_input: plant file {g['file']} is not at the tip {tip[:12]}")
        files = {p: show(p) for p in tests + products}
        for p in products:
            if files[p] is None:
                refuse(f"test_only_input: product file {p} is not at the tip {tip[:12]}")
        inp.update({"repo_subdir": subdir, "service_dir": svc, "shared_pkg_dir": spd, "shared_pkg_name": spn,
                    "repo": {"tip": tip, "repo_subdir": subdir, "service_dir": svc, "test_runner": runner},
                    "product_files": products, "test_files": tests, "files": files,
                    "new_test_files": [t for t in tests if files[t] is None],
                    "red_cells": cells, "plant": groups, "plant_diff": plant_diff})
    elif tier == "doc_only":
        if tests:
            refuse("doc_only: a `Test file:` header line — a doc_only brief touches docs/comments only")
        if not products:
            refuse("doc_only: no `File:` header line")
        items, eerrs = tb.parse_expect(text)
        if eerrs or not items or not any(i["kind"] == "absent" for i in items):
            refuse("doc_only: `## Expect` needs >= 1 expect_absent: `<text>`" + (f" ({'; '.join(eerrs)})" if eerrs else ""))
        files = {p: show(p) for p in products}
        inp.update({"repo_subdir": "", "tool_subdir": subdir, "repo": {"tip": tip, "repo_subdir": "", "service_dir": "", "test_runner": "docs"},
                    "doc_files": products, "files": files, "new_doc_files": [p for p in products if files[p] is None],
                    "expect": items, "doc_checks": tb.parse_doc_checks(text), "doc_check_cwd": pins.get("doc_check_cwd", "")})
    elif tier == "test_only_bash":
        # 2026-11-09: a bash TEST SUITE hardening ticket. The suite is the model's file; every other file is read-only.
        if not tests:
            refuse("test_only_bash: no `Test file:` header line")
        if not products:
            refuse("test_only_bash: no `File:` header line (the read-only code the suite exercises or reads)")
        for t in tests:
            if not tb.is_bash_suite_path(t):
                refuse(f"test_only_bash: test {t} is not a bash suite (*.test.sh, or a .sh/.bash under a __tests__ dir)")
            if t in products:
                refuse(f"test_only_bash: {t} is both a `File:` (read-only) and a `Test file:` (editable)")
        if runner != "bash":
            refuse(f"test_only_bash: the Runner: line must be `bash` (got {runner!r})")
        groups, perrs = tb.parse_plant(text)
        pdiff = os.path.join(bdir, "golden_red.diff")
        plant_diff = open(pdiff, encoding="utf-8").read() if os.path.isfile(pdiff) else None
        items, eerrs = tb.parse_expect(text)
        has_plant = bool(groups) or plant_diff is not None
        has_expect = items is not None
        if perrs or eerrs or has_plant == has_expect or (has_plant and bool(groups) == bool(plant_diff)) or (has_expect and not items):
            refuse("test_only_bash: need exactly one red proof: a complete `## Plant` block or golden_red.diff (plant shape), OR "
                   "a `## Expect` block with >= 1 expect_present/expect_absent (expectations shape)"
                   + (f" ({'; '.join(perrs + eerrs)})" if perrs or eerrs else ""))
        cells = tb.parse_red_cells(text)
        if has_plant and not cells:
            refuse("test_only_bash: the plant shape needs `## Red cells` naming (in backticks) a substring of each cell's label")
        for g in groups:
            if show(g["file"]) is None:
                refuse(f"test_only_bash: plant file {g['file']} is not at the tip {tip[:12]}")
        files = {p: show(p) for p in tests + products}
        for p in products:
            if files[p] is None:
                refuse(f"test_only_bash: File {p} is not at the tip {tip[:12]}")
        inp.update({"repo_subdir": "", "service_dir": "", "repo": {"tip": tip, "repo_subdir": "", "service_dir": "", "test_runner": "bash"},
                    "mode": "plant" if has_plant else "expect", "siblings": pins.get("siblings", "auto"),
                    "product_files": products, "test_files": tests, "files": files,
                    "new_test_files": [t for t in tests if files[t] is None],
                    "red_cells": cells or [], "plant": groups, "plant_diff": plant_diff, "expect": items or []})
    else:
        refuse(f"build_tier_input: tier {tier!r} is not one of test_only_input, test_only_bash, doc_only")
    json.dump(inp, open(out, "w", encoding="utf-8"), indent=1)
    print("WEDNESDAY BRIEF: (the brief is carried whole in input.json `brief`)")
    print(f"built {tier} input for {ticket} at {tip[:12]}: {len(inp['files'])} file(s) shown")
    return 0


if __name__ == "__main__":
    sys.exit(main())
