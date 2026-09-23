#!/usr/bin/env python3
"""spark_run.py - send ONE brief to the local DeepSeek V4 Flash endpoint and capture the answer.

Usage:
  spark_run.py --brief <brief.md> --repo <git working copy> --out <run dir>
               [--max-tokens N] [--dry-run] [--system <system prompt .md>]
               [--base-url URL] [--model ID]

Refuses (non-zero exit) when: the brief is missing, it has no Tip:, the repo HEAD is not at the Tip,
a File: named in the brief does not exist at the tip, or the built input exceeds 300000 tokens
(bytes/4). A brief-less run is a refusal, never a fallback.

Exit codes:
  0  a single fenced diff block was extracted to answer.diff (candidate only - run spark_check.py)
  2  refusal before calling the endpoint (bad brief / repo / size) or bad arguments
  3  the model's answer is not exactly one fenced diff block (includes a STOP refusal)
  4  harness/budget issue: finish_reason == "length" or empty content
  5  transport error (HTTP / timeout / unparseable response)

Python 3 stdlib only. One request, never parallel. Thinking is always OFF.
"""
import argparse
import json
import os
import re
import subprocess
import sys
import time
import urllib.error
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_BASE = "http://127.0.0.1:8888/v1"
DEFAULT_MODEL = "deepseek-v4-flash-0731"
DEFAULT_SYSTEM = os.path.normpath(os.path.join(
    HERE, "..", "..", "..", "0_Brain", "reference", "2026-09-22_spark-deepseek-v4-flash",
    "spark-kit_2026-09-23", "01_FOR_THE_LOCAL_MODEL.md"))
TOKEN_LIMIT = 300000
HTTP_TIMEOUT = 900

FILE_RE = re.compile(r"^\s*File:\s*`([^`]+)`", re.MULTILINE)
TIP_RE = re.compile(r"^\s*Tip:\s*`?\s*([0-9a-fA-F]{4,64})\s*`?", re.MULTILINE)


class Refusal(Exception):
    pass


def log_open(out_dir):
    path = os.path.join(out_dir, "run.log")
    fh = open(path, "a", encoding="utf-8")

    def log(msg):
        line = "%s  %s" % (time.strftime("%Y-%m-%dT%H:%M:%S%z"), msg)
        fh.write(line + "\n")
        fh.flush()
        print(line)
    return log, fh


def git(repo, *args):
    p = subprocess.run(["git", "-C", repo] + list(args), capture_output=True)
    return p.returncode, p.stdout, p.stderr


def parse_brief(text):
    files = []
    for m in FILE_RE.finditer(text):
        path = m.group(1).strip()
        if path and path not in files:
            files.append(path)
    tips = [m.group(1).lower() for m in TIP_RE.finditer(text)]
    return files, tips


def number_lines(content_bytes):
    text = content_bytes.decode("utf-8", errors="surrogateescape")
    lines = text.split("\n")
    if lines and lines[-1] == "":
        lines = lines[:-1]  # trailing newline does not make an extra line
    width = max(4, len(str(len(lines))))
    body = "\n".join("%s| %s" % (str(i).zfill(width), ln) for i, ln in enumerate(lines, 1))
    return body, len(lines)


def extract_fenced_blocks(content):
    """Line-based fence scan. Returns list of (lang, body_text)."""
    blocks = []
    lines = content.split("\n")
    i = 0
    while i < len(lines):
        m = re.match(r"^\s*(```+|~~~+)\s*([A-Za-z0-9_+-]*)\s*$", lines[i])
        if m:
            fence = m.group(1)
            lang = m.group(2).lower()
            body = []
            j = i + 1
            closed = False
            while j < len(lines):
                if lines[j].strip() == fence:
                    closed = True
                    break
                body.append(lines[j])
                j += 1
            blocks.append((lang, "\n".join(body), closed))
            i = j + 1
            continue
        i += 1
    return blocks


def looks_like_diff(lang, body):
    if lang in ("diff", "patch", "udiff"):
        return True
    return bool(re.search(r"^--- ", body, re.M) and re.search(r"^\+\+\+ ", body, re.M)
                and re.search(r"^@@ ", body, re.M))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--brief", required=True)
    ap.add_argument("--repo", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--max-tokens", type=int, default=8192)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--system", default=DEFAULT_SYSTEM)
    ap.add_argument("--base-url", default=DEFAULT_BASE)
    ap.add_argument("--model", default=DEFAULT_MODEL)
    a = ap.parse_args()

    out_dir = os.path.abspath(a.out)
    os.makedirs(out_dir, exist_ok=True)
    log, fh = log_open(out_dir)
    log("spark_run start brief=%r repo=%r out=%r dry_run=%s max_tokens=%d"
        % (a.brief, a.repo, out_dir, a.dry_run, a.max_tokens))
    try:
        return run(a, out_dir, log)
    except Refusal as e:
        log("REFUSED: %s" % e)
        return 2
    finally:
        fh.close()


def run(a, out_dir, log):
    # ---- brief -------------------------------------------------------------
    if not os.path.isfile(a.brief):
        raise Refusal("brief not found: %r (a brief-less run is a refusal, never a fallback)" % a.brief)
    with open(a.brief, "rb") as f:
        brief_bytes = f.read()
    brief = brief_bytes.decode("utf-8", errors="surrogateescape")
    if not brief.strip():
        raise Refusal("brief is empty: %r" % a.brief)
    files, tips = parse_brief(brief)
    if not tips:
        raise Refusal("brief has no `Tip:` line - cannot pin the commit the file was read at")
    if len(set(tips)) > 1:
        raise Refusal("brief has conflicting Tip: lines: %s" % ", ".join(sorted(set(tips))))
    tip = tips[0]
    if len(tip) < 7:
        raise Refusal("Tip %r is shorter than 7 hex chars - too ambiguous to pin" % tip)
    if not files:
        raise Refusal("brief has no File: `path` line")
    log("brief: files=%s tip=%s" % (files, tip))

    # ---- repo / tip --------------------------------------------------------
    if not os.path.isdir(a.repo):
        raise Refusal("repo not found: %r" % a.repo)
    rc, out, err = git(a.repo, "rev-parse", "HEAD")
    if rc != 0:
        raise Refusal("git rev-parse HEAD failed in %r: %s" % (a.repo, err.decode(errors="replace").strip()))
    head = out.decode().strip().lower()
    if not head.startswith(tip):
        raise Refusal("repo HEAD %s is NOT at brief Tip %s - check out the tip or rebrief" % (head, tip))
    log("repo HEAD %s matches Tip %s" % (head, tip))
    rc, out, _ = git(a.repo, "status", "--porcelain")
    dirty = out.decode(errors="replace").strip()
    if dirty:
        log("WARNING: working copy is dirty; file content is taken from the COMMIT (git show), not disk:\n"
            + dirty)

    # ---- system prompt -----------------------------------------------------
    if not os.path.isfile(a.system):
        raise Refusal("system prompt file not found: %r" % a.system)
    with open(a.system, "r", encoding="utf-8") as f:
        system_prompt = f.read()

    # ---- user message ------------------------------------------------------
    parts = [brief.rstrip("\n"), "", "---", "",
             "# Files at Tip %s (read whole; each line is prefixed `NNNN| `, which is NOT part of the file)" % head,
             ""]
    for path in files:
        rc, content, err = git(a.repo, "show", "%s:%s" % (head, path))
        if rc != 0:
            raise Refusal("named file %r does not exist at tip %s: %s"
                          % (path, head, err.decode(errors="replace").strip()))
        body, n = number_lines(content)
        parts.append("=== FILE: %s — %d lines (at %s) ===" % (path, n, head[:12]))
        parts.append(body)
        parts.append("=== END FILE: %s ===" % path)
        parts.append("")
        log("included %s: %d lines, %d bytes" % (path, n, len(content)))
    user_msg = "\n".join(parts)

    approx_tokens = (len(system_prompt.encode("utf-8", "surrogateescape"))
                     + len(user_msg.encode("utf-8", "surrogateescape"))) // 4
    log("approx input tokens (bytes/4, system+user): %d (limit %d)" % (approx_tokens, TOKEN_LIMIT))
    if approx_tokens > TOKEN_LIMIT:
        raise Refusal("built input is ~%d tokens > %d limit - NOT truncating; split the brief"
                      % (approx_tokens, TOKEN_LIMIT))

    payload = {
        "model": a.model,
        "max_tokens": a.max_tokens,
        "temperature": 0,
        "chat_template_kwargs": {"thinking": False},
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_msg},
        ],
    }
    req_path = os.path.join(out_dir, "request.json")
    with open(req_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)
    log("wrote %s" % req_path)
    if a.dry_run:
        log("DRY RUN: endpoint not called")
        return 0

    # ---- call (one request, never parallel) --------------------------------
    url = a.base_url.rstrip("/") + "/chat/completions"
    req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"),
                                 headers={"Content-Type": "application/json"})
    t0 = time.time()
    log("POST %s (timeout %ds)" % (url, HTTP_TIMEOUT))
    try:
        raw = urllib.request.urlopen(req, timeout=HTTP_TIMEOUT).read()
    except urllib.error.HTTPError as e:
        body = e.read().decode(errors="replace")
        log("TRANSPORT ERROR: HTTP %s after %.1fs: %s" % (e.code, time.time() - t0, body[:2000]))
        return 5
    except Exception as e:  # timeout, connection refused, ...
        log("TRANSPORT ERROR after %.1fs: %r" % (time.time() - t0, e))
        return 5
    dt = time.time() - t0
    resp_path = os.path.join(out_dir, "response.json")
    with open(resp_path, "wb") as f:
        f.write(raw)
    try:
        body = json.loads(raw)
        choice = body["choices"][0]
    except Exception as e:
        log("TRANSPORT ERROR: unparseable response after %.1fs: %r" % (dt, e))
        return 5
    finish = choice.get("finish_reason")
    content = (choice.get("message") or {}).get("content") or ""
    usage = body.get("usage") or {}
    log("response in %.1fs finish_reason=%s usage=%s" % (dt, finish, json.dumps(usage)))
    with open(os.path.join(out_dir, "answer.md"), "w", encoding="utf-8", errors="surrogateescape") as f:
        f.write(content)

    if finish == "length":
        log("HARNESS/BUDGET ISSUE: finish_reason=length - output truncated at max_tokens=%d. "
            "This is NOT a model verdict; raise --max-tokens or check thinking is off." % a.max_tokens)
        return 4
    if not content.strip():
        log("HARNESS/BUDGET ISSUE: empty content (finish_reason=%s). This is NOT a model verdict." % finish)
        return 4

    # ---- extract ----------------------------------------------------------
    stripped = content.strip()
    first = stripped.split("\n", 1)[0].strip()
    if re.match(r"^\**\s*STOP\b", first, re.I):
        log("MODEL REFUSED (STOP): %s" % stripped)
        return 3
    blocks = extract_fenced_blocks(content)
    diffs = [b for b in blocks if looks_like_diff(b[0], b[1])]
    # UNFENCED WHOLE-ANSWER DIFF (measured 2026-09-23 smoke run 1: DeepSeek V4 Flash returned a correct unified
    # diff with NO fences). Accepted ONLY when there are zero fences, the answer starts with '--- ', and EVERY
    # non-empty line is unified-diff grammar. Any prose anywhere keeps the refusal below. Logged as a breach.
    if not blocks and stripped.startswith("--- "):
        grammar = re.compile(r"^(--- |\+\+\+ |@@ -\d+(,\d+)? \+\d+(,\d+)? @@| |\+|-|\\ No newline)")
        bad = [l for l in stripped.split("\n") if l.strip() and not grammar.match(l)]
        if not bad:
            log("CONTRACT BREACH (format): the answer is an UNFENCED diff. Accepted because the WHOLE answer is "
                "unified-diff grammar (%d lines, 0 non-diff lines). See kit 04, failure mode 8." % stripped.count("\n"))
            blocks = [("diff", stripped, True)]; diffs = list(blocks)
        else:
            log("UNFENCED answer rejected: %d non-diff line(s), first: %r" % (len(bad), bad[0][:120]))
    if len(blocks) != 1 or len(diffs) != 1:
        desc = ", ".join("%s(%s,%d lines%s)" % ("diff" if looks_like_diff(l, bd) else "non-diff",
                                                  l or "no-lang", bd.count("\n") + 1,
                                                  "" if c else ",UNCLOSED")
                         for l, bd, c in blocks) or "no fenced blocks"
        log("NOT EXACTLY ONE FENCED DIFF BLOCK: found %d fenced block(s), %d diff-like: %s. "
            "answer.diff NOT written." % (len(blocks), len(diffs), desc))
        return 3
    lang, diff_body, closed = diffs[0]
    if not closed:
        log("NOT EXACTLY ONE FENCED DIFF BLOCK: the only block is UNCLOSED. answer.diff NOT written.")
        return 3
    # text outside the block is a contract breach worth flagging, but the diff is still a candidate
    outside = content
    fence_start = content.find(diff_body)
    if fence_start >= 0:
        outside = (content[:fence_start] + content[fence_start + len(diff_body):])
    outside = re.sub(r"(```+|~~~+)[A-Za-z0-9_+-]*", "", outside).strip()
    if outside:
        log("WARNING: %d chars of text OUTSIDE the diff block (contract says nothing outside): %r"
            % (len(outside), outside[:300]))
    diff_path = os.path.join(out_dir, "answer.diff")
    with open(diff_path, "w", encoding="utf-8", errors="surrogateescape") as f:
        f.write(diff_body if diff_body.endswith("\n") else diff_body + "\n")
    log("wrote %s (%d lines). CANDIDATE ONLY - run spark_check.py." % (diff_path, diff_body.count("\n") + 1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
