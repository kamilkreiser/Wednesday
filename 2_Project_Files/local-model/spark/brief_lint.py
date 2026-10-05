#!/usr/bin/env python3
"""brief_lint.py <brief_dir> [pin=value ...] — the Spark round's brief gate (2026-10-05).

Reads ONE brief dir (exactly one `KS-<n>.md` inside it), refuses a brief the round cannot run, and on success prints
shell assignments (shlex-quoted) for round.sh to `eval`:

  B_TICKET  B_BRIEF  B_TIER  B_FILE  B_TEST_FILE  B_BRIEF_TIP  B_RUNNER  B_PINS (display)  B_PINS_ARR (bash array)
  B_ALLOW_DRIFT  B_GOLDEN (path or empty)  B_DRIFT_PATHS (repo paths whose drift makes the brief stale)

Pins: `<brief_dir>/spark.pins` (lines of `key=value` tokens; a line starting `#` is a comment; no spaces inside a value) then the CLI pins (CLI wins per key).
Round-only keys (`tier`, `allow_drift`) are consumed here; every other key is passed to the builder untouched.

REFUSES (rc 2, one `REFUSED <reason>` line per reason on stderr):
  - not exactly one KS-<n>.md in the dir;
  - a required header line or heading is missing (kit 03_BRIEF_TEMPLATE; case-insensitive);
  - the brief names a client other than Secuura (a `Client:` line that is not Secuura, a `!CODING/<other>/` path,
    or another client's name) — the Spark takes Secuura work under Kam's 2026-09-25 ruling, one client per task;
  - the tier is not one round.sh runs (code_patch, bash_patch); test_only has its own builder and is not wired here;
  - bash_patch B-mode without a `ref=` pin (build_bash_input.sh requires one).
rc 0 ok · 2 refused · 1 usage. Read-only. Python 3 stdlib.
"""
import os
import re
import shlex
import sys

REQUIRED_HEADER = [
    ("File:", r"^File:\s*`[^`]+`"),
    ("Tip:", r"^Tip:\s*`[0-9a-f]{7,40}`"),
    ("Runner:", r"^Runner:\s*\S"),
]
REQUIRED_HEADINGS = [
    ("## The mode", r"^##+\s*The mode\b"),
    ("## What is wrong", r"^##+\s*What is wrong\b"),
    ("## The exact change", r"^##+\s*The exact change\b"),
    ("## The test (or ## Self-testing)", r"^##+\s*(The test\b|Self-testing\b)"),
    ("## UNMEASURED", r"^##+\s*UNMEASURED\b"),
    ("## Scope", r"^##+\s*Scope\b"),
    ("## Output", r"^##+\s*Output\b"),
]
# Other clients of this workspace (CLAUDE.md hard rule 2). Word-bounded, case-insensitive. A false refusal is the safe
# direction; a Secuura brief has no reason to name any of these.
OTHER_CLIENTS = [r"datasec", r"nexus\s*ai", r"vision sales portal", r"cypherkey", r"mypki", r"lead_bot",
                 r"task_dispatcher", r"feedback_system"]
ROUND_ONLY = {"tier", "allow_drift"}


def read_pins(path):
    pins = {}
    if os.path.isfile(path):
        for raw in open(path, encoding="utf-8"):
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            for tok in line.split():
                if "=" in tok:
                    k, v = tok.split("=", 1)
                    pins[k] = v
    return pins


def main():
    if len(sys.argv) < 2:
        print("usage: brief_lint.py <brief_dir> [pin=value ...]", file=sys.stderr)
        return 1
    bdir = os.path.abspath(sys.argv[1])
    reasons = []
    if not os.path.isdir(bdir):
        print(f"REFUSED brief dir does not exist: {bdir}", file=sys.stderr)
        return 2
    briefs = sorted(f for f in os.listdir(bdir) if re.fullmatch(r"KS-[0-9]+\.md", f))
    if len(briefs) != 1:
        print(f"REFUSED expected exactly one KS-<n>.md in {bdir}, found {len(briefs)}: {briefs} "
              f"(the brief file is named for its ticket; the builder reads <ticket>.md)", file=sys.stderr)
        return 2
    bfile = os.path.join(bdir, briefs[0])
    ticket = briefs[0][:-3]
    text = open(bfile, encoding="utf-8").read()

    # --- client ---
    m_client = re.search(r"(?im)^Client:\s*(.+)$", text)
    if m_client and not re.search(r"(?i)\bsecuura\b", m_client.group(1)):
        reasons.append(f"CLIENT: the brief's Client: line names {m_client.group(1).strip()!r}, not Secuura — "
                       f"round.sh runs Secuura briefs only (one client per task)")
    for m in re.finditer(r"!CODING/([^/\s`'\"]+)/", text):
        if m.group(1).lower() != "secuura":
            reasons.append(f"CLIENT: the brief names a path under !CODING/{m.group(1)}/ — not Secuura")
            break
    for pat in OTHER_CLIENTS:
        m = re.search(r"(?i)\b" + pat + r"\b", text)
        if m:
            reasons.append(f"CLIENT: the brief names another client ({m.group(0)!r}) — round.sh runs Secuura briefs only")
            break
    title = text.split("\n", 1)[0]
    if not re.match(r"^#\s+KS-[0-9]+\b", title):
        reasons.append(f"HEADER: line 1 must be `# KS-<n> ...` (Secuura's Linear team is KS); got {title[:80]!r}")

    # --- required shape ---
    for name, rx in REQUIRED_HEADER + REQUIRED_HEADINGS:
        if not re.search(rx, text, re.M | re.I):
            reasons.append(f"SHAPE: missing {name} (spark-kit 03_BRIEF_TEMPLATE)")

    # --- pins ---
    pins = read_pins(os.path.join(bdir, "spark.pins"))
    for a in sys.argv[2:]:
        if "=" not in a:
            reasons.append(f"USAGE: argument {a!r} is not a key=value pin")
            continue
        k, v = a.split("=", 1)
        pins[k] = v

    # --- tier ---
    m_file = re.search(r"^File:\s*`([^`]+)`", text, re.M)
    m_test = re.search(r"(?im)^Test file:\s*`([^`]+)`", text)
    m_tip = re.search(r"^Tip:\s*`([0-9a-f]{7,40})`", text, re.M)
    m_run = re.search(r"^Runner:\s*`?([A-Za-z0-9_.-]+)", text, re.M)
    runner = (m_run.group(1).lower() if m_run else "")
    tier = pins.get("tier")
    if not tier:
        m_tier = re.search(r"(?i)\bTier:\s*\**`?(code_patch|bash_patch|test_only|doc_patch)\b", text)
        if m_tier:
            tier = m_tier.group(1).lower()
        elif re.search(r"^##+\s*Tampers?\b", text, re.M | re.I):
            tier = "test_only"
        elif runner == "bash":
            tier = "bash_patch"
        elif runner in ("vitest", "jest"):
            tier = "code_patch"
    if tier not in ("code_patch", "bash_patch"):
        reasons.append(f"TIER: {tier or 'undetermined'} — round.sh runs code_patch and bash_patch only "
                       f"(test_only has its own builder, tasks/test_only/build_test_only_input.sh; not wired here). "
                       f"Pin tier= or add `Tier: \\`<tier>\\`` to the brief")
    selftest = bool(re.search(r"^##+\s*Self-testing\b", text, re.M | re.I))
    if tier == "bash_patch" and not selftest and not pins.get("ref"):
        reasons.append("PINS: bash_patch B-mode needs ref=<existing *.test.sh whose shape the model copies> "
                       "(build_bash_input.sh requires it) — put it in <brief_dir>/spark.pins or on the queue line")

    if reasons:
        for r in reasons:
            print(f"REFUSED {r}", file=sys.stderr)
        return 2

    builder_pins = {k: v for k, v in pins.items() if k not in ROUND_ONLY}
    if "product" not in builder_pins and not (tier == "bash_patch" and selftest):
        builder_pins["product"] = m_file.group(1)
    drift = [m_file.group(1)]
    if m_test:
        drift.append(m_test.group(1))
    if builder_pins.get("ref"):
        drift.append(builder_pins["ref"])
    if builder_pins.get("test_file"):
        drift.append(builder_pins["test_file"])
    golden = os.path.join(bdir, "golden.diff")
    out = {
        "B_TICKET": ticket,
        "B_BRIEF": bfile,
        "B_TIER": tier,
        "B_FILE": m_file.group(1),
        "B_TEST_FILE": m_test.group(1) if m_test else "",
        "B_BRIEF_TIP": m_tip.group(1),
        "B_RUNNER": runner,
        "B_PINS": " ".join(f"{k}={v}" for k, v in builder_pins.items()),  # display only; B_PINS_ARR is what runs
        "B_ALLOW_DRIFT": "1" if pins.get("allow_drift") in ("1", "yes", "true") else "0",
        "B_GOLDEN": golden if os.path.isfile(golden) else "",
        "B_DRIFT_PATHS": " ".join(dict.fromkeys(drift)),
    }
    for k, v in out.items():
        print(f"{k}={shlex.quote(v)}")
    print("B_PINS_ARR=(" + " ".join(shlex.quote(f"{k}={v}") for k, v in builder_pins.items()) + ")")
    return 0


if __name__ == "__main__":
    sys.exit(main())
