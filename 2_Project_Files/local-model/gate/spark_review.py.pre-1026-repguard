#!/usr/bin/env python3
"""spark_review.py — the LLM half of the Spark gate. ONE request to the local Spark, strict JSON back.

usage: spark_review.py --repo CLONE --head-sha SHA --facts facts.json --diff diff.patch --ticket KS-1719 \
                       [--comment draft.md] [--pr-body file] --out DIR [--linear-env /path/.env]
Needs the deterministic half's outputs (facts.json, diff.patch). Python 3 stdlib only. SPARK_THINK=0 by default.

Client: spark_call.py (lib/) is NOT reused: it is bound to the coding-task contract (it injects the kit's 'produce a diff'
system prompt and reads task.md/input.json files). The payload below is the same one it sends (OpenAI chat/completions,
temperature 0, chat_template_kwargs.thinking=false), so the Spark sees the same server settings.
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
    for l in open(envfile):
        if l.startswith("LINEAR_API_KEY="):
            key = l.split("=", 1)[1].strip().strip('"').strip("'")
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


def call(messages, max_tokens):
    wait_for_box()
    body = {"model": MODEL, "messages": messages, "max_tokens": max_tokens, "temperature": 0,
            "chat_template_kwargs": {"thinking": THINK}}
    req = urllib.request.Request(URL + "/v1/chat/completions", data=json.dumps(body).encode(), headers={"Content-Type": "application/json"})
    t0 = time.time()
    j = json.load(urllib.request.urlopen(req, timeout=1800))
    c = j["choices"][0]
    return (c["message"].get("content") or "").strip(), c.get("finish_reason"), j.get("usage", {}), time.time() - t0


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
    ap.add_argument("--comment"); ap.add_argument("--pr-body"); ap.add_argument("--max-tokens", type=int, default=8000)
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
    attempts, tot_pt, tot_ct, tot_s, result, errs = [], 0, 0, 0.0, None, None
    for n in (1, 2):
        txt, fin, usage, secs = call(msgs, a.max_tokens)
        tot_pt += usage.get("prompt_tokens", 0); tot_ct += usage.get("completion_tokens", 0); tot_s += secs
        open(os.path.join(a.out, f"raw_attempt{n}.txt"), "w").write(txt)
        try:
            o = extract_json(txt); errs = validate(o)
        except Exception as e:
            o, errs = None, [f"not parseable JSON: {e}"]
        attempts.append({"attempt": n, "finish": fin, "usage": usage, "seconds": round(secs, 1), "schema_errors": errs})
        if not errs: result = o; break
        msgs = msgs + [{"role": "assistant", "content": txt}, {"role": "user", "content": "Your reply failed schema validation: " + "; ".join(errs) + ". Reply again with ONE JSON object in exactly the required shape and nothing else."}]
    if result:  # deterministic evidence check: does every backticked/quoted fragment appear in the material given?
        corpus = user
        for f in result["findings"]:
            q = re.findall(r"`([^`]{6,})`", f["evidence"]) or re.findall(r'"([^"]{6,})"', f["evidence"])
            f["evidence_quote_found_in_input"] = bool(q) and all(x.strip() in corpus for x in q)
    meta = {"attempts": attempts, "prompt_tokens": tot_pt, "completion_tokens": tot_ct, "seconds": round(tot_s, 1), "think": THINK, "valid": result is not None}
    json.dump({"meta": meta, "review": result}, open(os.path.join(a.out, "review.json"), "w"), indent=1)
    print(json.dumps(meta)); print(json.dumps(result, indent=1) if result else "SCHEMA FAILURE x2")
    return 0 if result else 4


if __name__ == "__main__":
    sys.exit(main())
