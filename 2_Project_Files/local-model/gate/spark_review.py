#!/usr/bin/env python3
"""spark_review.py — the LLM half of the Spark gate. ONE request to the local Spark, strict JSON back.

usage: spark_review.py --repo CLONE --head-sha SHA --facts facts.json --diff diff.patch --ticket KS-1719 \
                       [--comment draft.md] [--pr-body-file file] [--dry-run] --out DIR [--linear-env /path/.env]
Needs the deterministic half's outputs (facts.json, diff.patch). Python 3 stdlib only. SPARK_THINK=0 by default.

Client: spark_call.py (lib/) is NOT reused: it is bound to the coding-task contract (it injects the kit's 'produce a diff'
system prompt and reads task.md/input.json files). The payload below is the same one it sends (OpenAI chat/completions,
temperature 0, chat_template_kwargs.thinking=false), so the Spark sees the same server settings.
Repetition guard (2026-10-26): the reply is STREAMED and cut off the moment a finding (or a 12-word run) repeats; a retry
never resends the looping text — it resends the original prompt plus a short anti-repetition instruction at a lower token
cap; findings are de-duplicated before schema validation. --pr-body-file supplies the PR description (--pr-body is an alias).
Queue discipline: waits while spark/state/round.lock exists (the box takes one request at a time).
"""
import argparse, json, os, re, subprocess, sys, time, urllib.request, urllib.error

HERE = os.path.dirname(os.path.abspath(__file__))
LOCK = os.path.normpath(os.path.join(HERE, "..", "spark", "state", "round.lock"))
URL = os.environ.get("SPARK_URL", "http://127.0.0.1:47788").rstrip("/")
MODEL = os.environ.get("SPARK_MODEL", "deepseek-v4-flash-0731")
THINK = os.environ.get("SPARK_THINK", "0") not in ("0", "", "false", "off")
SEV = {"Major", "Minor", "Note"}; VERD = {"GO", "GO WITH NOTES", "NO GO"}


def git(repo, *a):
    return subprocess.run(["git", "-C", repo, *a], capture_output=True, text=True).stdout


def ticket_text(ident, envfile):
    key = None
    try:
        for l in open(envfile):
            if l.startswith("LINEAR_API_KEY="):
                key = l.split("=", 1)[1].strip().strip('"').strip("'")
    except OSError:
        pass
    if not key:
        return f"(ticket {ident}: no LINEAR_API_KEY found; ticket text unavailable)"
    team, num = ident.split("-")
    q = {"query": "query($t:String!,$n:Float!){issues(filter:{team:{key:{eq:$t}},number:{eq:$n}}){nodes{identifier title description state{name} comments{nodes{body user{name} createdAt}}}}}",
         "variables": {"t": team, "n": float(num)}}
    req = urllib.request.Request("https://api.linear.app/graphql", data=json.dumps(q).encode(),
                                 headers={"Content-Type": "application/json", "Authorization": key})
    try:
        d = json.load(urllib.request.urlopen(req, timeout=60))
        n = d["data"]["issues"]["nodes"][0]
    except Exception as e:  # never echo the key
        return f"(ticket {ident}: fetch failed: {type(e).__name__})"
    cm = "\n".join(f"- [{c['createdAt']}] {c['user']['name'] if c.get('user') else '?'}: {c['body']}" for c in n["comments"]["nodes"])
    # Ticket COMMENTS are excluded by default: in a calibration replay they include comments posted AFTER the round under test.
    return f"{n['identifier']} — {n['title']} [{n['state']['name']}]\n\n{n['description']}" + (f"\n\nCOMMENTS:\n{cm}" if os.environ.get("GATE_TICKET_COMMENTS") == "1" else "")


CITE = re.compile(r"([\w./-]+\.(?:ts|py|md|js|toml|yml|yaml|sh)):(\d+)(?:-(\d+))?")


def cited_lines(repo, sha, *texts):
    tree = git(repo, "ls-tree", "-r", "--name-only", sha).splitlines()
    out, seen = [], set()
    for t in texts:
        for m in CITE.finditer(t or ""):
            f, a, b = m.group(1), int(m.group(2)), int(m.group(3) or m.group(2))
            if (f, a, b) in seen:
                continue
            seen.add((f, a, b))
            cands = [p for p in tree if p == f or p.endswith("/" + f)]
            if not cands:
                out.append(f"### {f}:{a}-{b} — NOT FOUND in the tree at {sha[:8]}"); continue
            for p in cands[:2]:
                lines = git(repo, "show", f"{sha}:{p}").splitlines()
                seg = "\n".join(f"{i}: {lines[i-1]}" for i in range(max(1, a - 1), min(len(lines), b + 1) + 1))
                out.append(f"### {p}:{a}-{b} (cited as {m.group(0)})\n{seg}")
    return "\n\n".join(out) or "(none)"


def wait_for_box():
    t0 = time.time()
    while os.path.exists(LOCK):
        if time.time() - t0 > 3600:
            sys.exit("spark_review: round.lock still present after 60 min — not calling")
        print(f"spark_review: {LOCK} present, waiting...", file=sys.stderr, flush=True); time.sleep(20)


def _norm(x):
    return re.sub(r"\s+", " ", x.lower()).strip()


def detect_repetition(text, claim_n=3, gram_n=4, gram_len=12):
    """Return a reason string if the text loops, else None. Looks at (a) the same "claim" value >= claim_n times,
    (b) any gram_len-word run occurring >= gram_n times. A normal review reaches neither."""
    claims = [_norm(c) for c in re.findall(r'"claim"\s*:\s*"((?:[^"\\]|\\.)*)"', text)]
    for c, k in __import__("collections").Counter(claims).items():
        if k >= claim_n:
            return f"claim repeated {k}x: {c[:80]!r}"
    w = _norm(text).split(" ")
    if len(w) >= gram_len * gram_n:
        cnt = {}
        for i in range(len(w) - gram_len + 1):
            g = " ".join(w[i:i + gram_len])
            cnt[g] = cnt.get(g, 0) + 1
            if cnt[g] >= gram_n:
                return f"{gram_len}-word run repeated {cnt[g]}x: {g[:80]!r}"
    return None


def dedupe_findings(o):
    """Drop findings whose normalised claim already appeared. Returns the number removed (mutates o)."""
    if not isinstance(o, dict) or not isinstance(o.get("findings"), list):
        return 0
    seen, keep = set(), []
    for f in o["findings"]:
        k = _norm(f.get("claim", "")) if isinstance(f, dict) and isinstance(f.get("claim"), str) else None
        if k is not None and k in seen:
            continue
        if k is not None:
            seen.add(k)
        keep.append(f)
    n = len(o["findings"]) - len(keep); o["findings"] = keep
    return n


def call(messages, max_tokens):
    """Streamed chat completion. Returns (text, finish_reason, usage, seconds, repetition_reason_or_None).
    Stops reading (closing the connection, which frees the box) as soon as detect_repetition fires."""
    wait_for_box()
    body = {"model": MODEL, "messages": messages, "max_tokens": max_tokens, "temperature": 0, "stream": True,
            "stream_options": {"include_usage": True}, "chat_template_kwargs": {"thinking": THINK}}
    req = urllib.request.Request(URL + "/v1/chat/completions", data=json.dumps(body).encode(), headers={"Content-Type": "application/json"})
    t0 = time.time(); parts, fin, usage, rep, nchunks, last_chk = [], None, {}, None, 0, 0
    resp = urllib.request.urlopen(req, timeout=1800)
    try:
        for raw in resp:
            line = raw.decode("utf-8", "replace").strip()
            if not line.startswith("data:"): continue
            data = line[5:].strip()
            if data == "[DONE]": break
            try: j = json.loads(data)
            except ValueError: continue
            if j.get("usage"): usage = j["usage"]
            for c in j.get("choices") or []:
                d = (c.get("delta") or {}).get("content")
                if d: parts.append(d); nchunks += 1
                if c.get("finish_reason"): fin = c["finish_reason"]
            txt_len = sum(map(len, parts))
            if txt_len - last_chk >= 1500:  # re-check every ~1500 chars
                last_chk = txt_len; rep = detect_repetition("".join(parts))
                if rep: fin = "repetition_abort"; break
    finally:
        resp.close()
    text = "".join(parts).strip()
    if not rep: rep = detect_repetition(text)
    if rep and fin != "repetition_abort": fin = fin or "repetition"
    if not usage: usage = {"completion_tokens": nchunks, "note": "aborted stream; completion_tokens = chunks received (approx)"}
    return text, fin, usage, time.time() - t0, rep


def extract_json(s):
    s = re.sub(r"^```(?:json)?\s*|\s*```$", "", s.strip())
    a, b = s.find("{"), s.rfind("}")
    return json.loads(s[a:b + 1])


def validate(o):
    errs = []
    if not isinstance(o, dict): return ["top level is not an object"]
    if set(o) - {"findings", "comment_sentences_overstated", "verdict"}: errs.append(f"extra keys {sorted(set(o) - {'findings','comment_sentences_overstated','verdict'})}")
    if o.get("verdict") not in VERD: errs.append(f"verdict must be one of {sorted(VERD)}")
    if not isinstance(o.get("findings"), list): errs.append("findings must be a list")
    else:
        for i, f in enumerate(o["findings"]):
            if not isinstance(f, dict): errs.append(f"findings[{i}] not an object"); continue
            if f.get("severity") not in SEV: errs.append(f"findings[{i}].severity must be Major|Minor|Note")
            for k in ("claim", "evidence", "test_or_reason"):
                if not isinstance(f.get(k), str) or not f[k].strip(): errs.append(f"findings[{i}].{k} must be a non-empty string")
    c = o.get("comment_sentences_overstated")
    if not isinstance(c, list): errs.append("comment_sentences_overstated must be a list")
    else:
        for i, x in enumerate(c):
            if not (isinstance(x, dict) and isinstance(x.get("sentence"), str) and isinstance(x.get("why"), str)): errs.append(f"comment_sentences_overstated[{i}] needs sentence+why strings")
    return errs


def main():
    ap = argparse.ArgumentParser()
    for a in ("repo", "head-sha", "facts", "diff", "ticket", "out"): ap.add_argument("--" + a, required=True)
    ap.add_argument("--comment"); ap.add_argument("--pr-body", "--pr-body-file", dest="pr_body"); ap.add_argument("--dry-run", action="store_true"); ap.add_argument("--max-tokens", type=int, default=8000)
    ap.add_argument("--linear-env", default="/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env")
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    facts = json.load(open(a.facts)); diff = open(a.diff).read()
    comment = open(a.comment).read() if a.comment else ""
    prbody = open(a.pr_body).read() if a.pr_body else ""
    tk = ticket_text(a.ticket, a.linear_env)
    files = []
    for t in facts["touched_files"]:
        if t["status"].startswith("D"): continue
        files.append(f"### FILE AT HEAD: {t['path']}\n" + "\n".join(f"{i}: {l}" for i, l in enumerate(git(a.repo, "show", f"{a.head_sha}:{t['path']}").splitlines(), 1)))
    cites = cited_lines(a.repo, a.head_sha, comment, prbody, diff)
    sections = [("TICKET", tk), ("DIFF (merge-base..head)", diff), ("TOUCHED FILES, FULL TEXT AT HEAD (line-numbered)", "\n\n".join(files)),
                ("SOURCE LINES CITED BY THE PR / COMMENT (line-numbered)", cites),
                ("PR DESCRIPTION", prbody or "(not provided)"), ("DRAFTED CLIENT COMMENT", comment or "(none)"),
                ("facts.json (deterministic runner output)", json.dumps(facts, indent=1))]
    user = "\n\n".join(f"===== {n} =====\n{b}" for n, b in sections)
    json.dump({n: len(b) for n, b in sections}, open(os.path.join(a.out, "prompt_sections_chars.json"), "w"), indent=1)
    open(os.path.join(a.out, "prompt_user.txt"), "w").write(user)
    system = open(os.path.join(HERE, "REVIEW_CHECKLIST.md")).read()
    msgs = [{"role": "system", "content": system}, {"role": "user", "content": user}]
    if a.dry_run:
        print(f"spark_review: dry run — prompt written to {a.out}/prompt_user.txt, no call made"); return 0
    ANTI = ("IMPORTANT: your previous attempt looped and repeated itself. List each DISTINCT finding exactly once, at most 8 findings, "
            "keep every field to 1-2 sentences, and stop. Reply with ONE JSON object only.")
    base_msgs = msgs
    attempts, tot_pt, tot_ct, tot_s, result, errs, dups = [], 0, 0, 0.0, None, None, 0
    cap = a.max_tokens
    for n in (1, 2):
        txt, fin, usage, secs, rep = call(msgs, cap)
        tot_pt += usage.get("prompt_tokens", 0); tot_ct += usage.get("completion_tokens", 0); tot_s += secs
        open(os.path.join(a.out, f"raw_attempt{n}.txt"), "w").write(txt)
        o = None
        try:
            o = extract_json(txt); dups += dedupe_findings(o); errs = validate(o)
        except Exception as e:
            errs = [f"not parseable JSON: {e}"]
        if rep and not errs and fin != "repetition_abort":
            pass  # parsed and de-duplicated cleanly: accept
        elif rep and fin == "repetition_abort":
            errs = (errs or []) + [f"repetition abort: {rep}"]
        attempts.append({"attempt": n, "finish": fin, "usage": usage, "seconds": round(secs, 1), "schema_errors": errs,
                         "repetition": rep, "max_tokens": cap})
        if not errs: result = o; break
        # retry: NEVER resend the looping text. Original prompt + a short instruction, lower cap.
        hint = ANTI + (" Schema problems last time: " + "; ".join(e for e in errs if not e.startswith("repetition"))[:400] if any(not e.startswith("repetition") for e in errs) else "")
        msgs = base_msgs + [{"role": "user", "content": hint}]
        cap = min(cap, 4000)
    if result:  # deterministic evidence check: does every backticked/quoted fragment appear in the material given?
        corpus = user
        for f in result["findings"]:
            q = re.findall(r"`([^`]{6,})`", f["evidence"]) or re.findall(r'"([^"]{6,})"', f["evidence"])
            f["evidence_quote_found_in_input"] = bool(q) and all(x.strip() in corpus for x in q)
    meta = {"attempts": attempts, "prompt_tokens": tot_pt, "completion_tokens": tot_ct, "seconds": round(tot_s, 1), "think": THINK, "valid": result is not None, "duplicate_findings_removed": dups}
    json.dump({"meta": meta, "review": result}, open(os.path.join(a.out, "review.json"), "w"), indent=1)
    print(json.dumps(meta)); print(json.dumps(result, indent=1) if result else "SCHEMA FAILURE x2")
    return 0 if result else 4


if __name__ == "__main__":
    sys.exit(main())
