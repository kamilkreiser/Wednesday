#!/usr/bin/env python3
"""Arms for spark_review.py (no Spark needed; a local mock server stands in). Prints ARMn PASS/FAIL lines, exits non-zero on any FAIL.
Arms: 1 22x-repeated finding caught · 2 normal review passes unchanged · 3 dedupe collapses repeats · 4 mock server loops: the stream is
aborted early (well under the cap) and the retry is NOT the looping text, carries the anti-repetition hint and a lower cap ·
5 --pr-body-file reaches the prompt (dry run) · 6 a clean mock review is accepted in one attempt."""
import http.server, json, os, subprocess, sys, tempfile, threading
HERE = os.path.dirname(os.path.abspath(__file__)); GATE = os.path.dirname(HERE)
sys.path.insert(0, GATE)
import spark_review as sr
fails = 0
def arm(n, ok, msg):
    global fails
    print(f"ARM{n} {'PASS' if ok else 'FAIL'}: {msg}"); fails += 0 if ok else 1

def finding(i, claim=None):
    return {"severity": "Minor", "claim": claim or f"distinct problem number {i} in the handler ordering", "evidence": f"a.ts:{i} `const x{i} = {i}`", "test_or_reason": f"unique reasoning for item {i} about ordering and scope"}
NORMAL = {"findings": [finding(i) for i in range(1, 5)], "comment_sentences_overstated": [{"sentence": "It fixes everything.", "why": "unmeasured"}], "verdict": "GO WITH NOTES"}
LOOP = {"findings": [finding(1, "the cancel is unbounded and may hang forever") for _ in range(22)], "comment_sentences_overstated": [], "verdict": "NO GO"}

arm(1, sr.detect_repetition(json.dumps(LOOP, indent=1)) is not None, "22x repeated finding detected")
arm(2, sr.detect_repetition(json.dumps(NORMAL, indent=1)) is None and not sr.validate(NORMAL), "normal review: no repetition flag, schema-valid")
import copy; L = copy.deepcopy(LOOP); n = sr.dedupe_findings(L)
arm(3, n == 21 and len(L["findings"]) == 1 and not sr.validate(L), f"dedupe removed {n} of 22, leaving 1 valid finding")
N = copy.deepcopy(NORMAL); arm("3b", sr.dedupe_findings(N) == 0 and N == NORMAL, "dedupe leaves a normal review untouched")

# ---- mock OpenAI-style streaming server ---------------------------------------------------------------------------------
REQS = []; MODE = {"loop_first": True}
class H(http.server.BaseHTTPRequestHandler):
    def log_message(self, *a): pass
    def do_POST(self):
        body = json.loads(self.rfile.read(int(self.headers["Content-Length"]))); REQS.append(body)
        looping = MODE["loop_first"] and len(REQS) == 1
        text = (json.dumps(LOOP, indent=1) * 40) if looping else json.dumps(NORMAL)  # looping reply would be ~hundreds of KB
        self.send_response(200); self.send_header("Content-Type", "text/event-stream"); self.end_headers()
        sent = 0
        try:
            for i in range(0, len(text), 200):
                self.wfile.write(("data: " + json.dumps({"choices": [{"delta": {"content": text[i:i+200]}}]}) + "\n\n").encode()); self.wfile.flush(); sent += 200
            self.wfile.write(("data: " + json.dumps({"choices": [{"delta": {}, "finish_reason": "stop"}], "usage": {"prompt_tokens": 10, "completion_tokens": 5}}) + "\n\ndata: [DONE]\n\n").encode())
        except (BrokenPipeError, ConnectionResetError):
            pass
        H.sent.append(sent)
H.sent = []
srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), H); threading.Thread(target=srv.serve_forever, daemon=True).start()
url = f"http://127.0.0.1:{srv.server_address[1]}"

tmp = tempfile.mkdtemp(prefix="sr_arms_", dir=os.environ.get("ARM_SCRATCH") or None)
repo = os.path.join(tmp, "repo"); os.makedirs(repo)
g = lambda *a: subprocess.run(["git", "-C", repo, *a], capture_output=True, text=True, check=True).stdout.strip()
g("init", "-q"); open(os.path.join(repo, "a.ts"), "w").write("const x1 = 1\n"); g("add", "."); g("-c", "user.name=t", "-c", "user.email=t@t", "commit", "-qm", "c"); sha = g("rev-parse", "HEAD")
facts = {"touched_files": [{"status": "M", "path": "a.ts"}]}
json.dump(facts, open(os.path.join(tmp, "facts.json"), "w")); open(os.path.join(tmp, "diff.patch"), "w").write("+const x1 = 1\n")
open(os.path.join(tmp, "body.md"), "w").write("PR BODY MARKER_9f3a: this fixes all the things.")
def run(*extra, out="o"):
    env = dict(os.environ, SPARK_URL=url, SPARK_NO_LOCK="1")
    return subprocess.run([sys.executable, os.path.join(GATE, "spark_review.py"), "--repo", repo, "--head-sha", sha, "--facts", os.path.join(tmp, "facts.json"),
        "--diff", os.path.join(tmp, "diff.patch"), "--ticket", "KS-1", "--linear-env", "/nonexistent", "--out", os.path.join(tmp, out), *extra], capture_output=True, text=True, env=env)

# 5: PR body flag reaches the prompt
r = run("--pr-body-file", os.path.join(tmp, "body.md"), "--dry-run", out="dry")
pu = open(os.path.join(tmp, "dry", "prompt_user.txt")).read()
arm(5, r.returncode == 0 and "MARKER_9f3a" in pu and "(not provided)" not in pu.split("PR DESCRIPTION")[1][:40], "--pr-body-file text appears under PR DESCRIPTION")
r = run("--dry-run", out="dry2"); pu2 = open(os.path.join(tmp, "dry2", "prompt_user.txt")).read()
arm("5b", "MARKER_9f3a" not in pu2 and "PR DESCRIPTION =====\n(not provided)" in pu2, "without the flag the prompt says (not provided)")

# 4: looping first reply
r = run("--max-tokens", "8000", out="loop"); rj = json.load(open(os.path.join(tmp, "loop", "review.json")))
att = rj["meta"]["attempts"]
arm(4, r.returncode == 0 and att[0]["finish"] == "repetition_abort" and H.sent[0] < 60000 and len(att) == 2 and att[1]["max_tokens"] == 4000 and rj["meta"]["valid"],
    f"loop aborted early after ~{H.sent[0]} bytes streamed of a ~{len(json.dumps(LOOP, indent=1))*40} byte loop; retry cap {att[1]['max_tokens']}; valid={rj['meta']['valid']}")
retry_msgs = REQS[1]["messages"]
arm("4b", len(retry_msgs) == 3 and "looped" in retry_msgs[-1]["content"] and "distinct problem" not in json.dumps(retry_msgs) and "unbounded" not in json.dumps(retry_msgs),
    "retry = original prompt + anti-repetition hint, looping text NOT resent")
# 6: clean
REQS.clear(); MODE["loop_first"] = False
r = run(out="clean"); rj = json.load(open(os.path.join(tmp, "clean", "review.json")))
arm(6, r.returncode == 0 and len(rj["meta"]["attempts"]) == 1 and rj["review"]["verdict"] == "GO WITH NOTES" and len(rj["review"]["findings"]) == 4, "clean mock review accepted in 1 attempt, 4 findings unchanged")
srv.shutdown()
print(f"spark_review arms: {fails} failed"); sys.exit(1 if fails else 0)
