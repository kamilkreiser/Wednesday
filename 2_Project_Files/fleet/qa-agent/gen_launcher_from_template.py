#!/usr/bin/env python3
"""gen_launcher_932.py — derive launch_qa_secuura_ks1062_932.sh from the #966 tier-1 launcher by
ASSERTED substitutions (every anchor must occur exactly as often as stated, or the generator refuses),
then a RESIDUAL GUARD: any token of the source gate (966, 1020, its head, its merge-base, its branch,
its service) left anywhere in the output is a refusal — nothing is written on refusal.

Usage: gen_launcher_932.py <template launcher> <output launcher>
Exit: 0 written · 1 an anchor count disagreed · 2 a residual token survived
"""
import re
import sys

src_path, out_path = sys.argv[1], sys.argv[2]
s = open(src_path, encoding="utf-8").read()

NEW_HEADER = """#!/bin/bash
# launch_qa_secuura_ks1062_932.sh — cross-project QA agent, TIER 1 (through code; a boot-path
# loader/migration counter on api-gateway — data integrity; no rendered surface, so the real-browser half
# of tier 1 does not apply) gate ROUND 1 on Secuura KS-1062 / PR #932 @ c72607d58, merge-base d4cf7e3cf.
#
# QA finding F-928-4 of the 2026-09-09 s161 batch gate, ticketed as KS-1062: api-gateway's
# `migrateDatabase` catches every per-statement error and never throws, so the tenant loop's `migrated++`
# ran on every return and a tenant whose database did not exist was logged as migrated. The fix returns
# { applied, failed, firstError } and counts a tenant as migrated only when failed === 0, with a warn line
# and a warn-level summary otherwise. ONE file, no test in the PR. #932 is gated ALONE: PR #928 (KS-950,
# HELD) overlaps it on the same hunks and is rebased on top of it by a builder seat AFTER this gate.
# Adapted from launch_qa_secuura_ks1020_966.sh by gen_launcher_932.py (asserted substitutions + residual
# guard): same guards and exit codes, re-pointed at #932.
#
# The merge-base guard stays valid while develop moves: #932 branched at d4cf7e3cf, 93 commits behind
# origin develop at cut time, so its merge-base with any descendant develop is still d4cf7e3cf (the file
# it touches is byte-identical at the base and at develop's tip at cut).
#
# Written by the generator because it contains a legitimate `cd`.
#
# Usage: launch_qa_secuura_ks1062_932.sh [--check]
# Exit: 0 launched (or guards passed under --check) · 2..17 a guard refused
"""

# 1. Replace the header (everything before `set -u`) wholesale.
marker = "set -u\n"
assert s.count(marker) == 1, "header marker"
s = NEW_HEADER + s[s.index(marker):]

# 2. Asserted substitutions: (old, new, expected count in the post-header text).
subs = [
    ("QA966_BRIEF", "QA932_BRIEF", 2),
    ("QA966_PROMPT", "QA932_PROMPT", 2),
    ("QA966_HEAD", "QA932_HEAD", 2),
    ("2026-09-13_secuura-966-ks1020-tier1", "2026-09-13_secuura-932-ks1062-tier1", 3),
    ("refs/heads/feature/ks-1020-security-get-apipresentationsid-returns-a-real-stored",
     "refs/heads/feature/ks-1062-tenant-migration-counter", 1),
    ("1f0d08841780059f68c420bf7a43ac3682dea9ad", "c72607d586971180f1a33c5765e403df5677933c", 1),
    ("721b333a6a58d7b45fd59946b8561432bf55d01a", "d4cf7e3cf73e91422a229b7d0767cf6c3a04fe57", 1),
]
for old, new, n in subs:
    c = s.count(old)
    if c != n:
        print(f"REFUSING: anchor {old!r} occurs {c} times, expected {n}", file=sys.stderr)
        sys.exit(1)
    s = s.replace(old, new)

# 3. Residual guard: tokens of the SOURCE gate that must not survive anywhere (header included).
#    The header's one mention of the template file name is allowed by name; everything else is not.
residual = ["1f0d08841", "721b333a6", "1020", "KS-1020", "ks-1020", "presentations", "vc-issuer", "s198",
            "getPresentation", "F-5"]
body_for_guard = s.replace("launch_qa_secuura_ks1020_966.sh", "")  # the one permitted mention
hits = []
for tok in residual:
    for m in re.finditer(re.escape(tok), body_for_guard):
        line = body_for_guard.count("\n", 0, m.start()) + 1
        hits.append((tok, line))
# "966" is guarded on its own, after the permitted template-name mention is stripped.
for m in re.finditer(r"966", body_for_guard):
    hits.append(("966", body_for_guard.count("\n", 0, m.start()) + 1))
if hits:
    for tok, line in hits:
        print(f"REFUSING: residual token {tok!r} at line {line}", file=sys.stderr)
    sys.exit(2)

# 4. Positive controls on the output: the new pins must each occur exactly once as assignments.
for needle, n in [("HEAD_SHA=\"${QA932_HEAD:-c72607d586971180f1a33c5765e403df5677933c}\"", 1),
                  ("MERGE_BASE='d4cf7e3cf73e91422a229b7d0767cf6c3a04fe57'", 1),
                  ("BRANCH='refs/heads/feature/ks-1062-tenant-migration-counter'", 1),
                  ("grep -q 'TIER 1'", 2), ("grep -q 'ROUND 1'", 2)]:
    c = s.count(needle)
    if c != n:
        print(f"REFUSING: output control {needle!r} occurs {c} times, expected {n}", file=sys.stderr)
        sys.exit(1)

open(out_path, "w", encoding="utf-8").write(s)
print(f"written {out_path} ({len(s)} bytes); {len(subs)} substitutions asserted; residual guard clean")
