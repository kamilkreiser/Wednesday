import json, sys, threading, subprocess, http.server
SP, S = sys.argv[1], sys.argv[2]
diff = open(SP + "/runs/2026-09-23_smoke/run1/answer.md").read()
cases = [("A pure unfenced diff", diff, 0), ("B diff + prose line", diff + "\nThis fixes the path.\n", 3), ("C prose only", "The fix is to change line 3.\n", 3)]
cur = {"c": ""}
class H(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        self.rfile.read(int(self.headers["Content-Length"]))
        b = json.dumps({"choices": [{"finish_reason": "stop", "message": {"content": cur["c"]}}], "usage": {}}).encode()
        self.send_response(200); self.send_header("Content-Type", "application/json"); self.end_headers(); self.wfile.write(b)
    def log_message(self, *a): pass
srv = http.server.HTTPServer(("127.0.0.1", 18999), H); threading.Thread(target=srv.serve_forever, daemon=True).start()
ok = True
for name, content, want in cases:
    cur["c"] = content
    r = subprocess.run([sys.executable, SP + "/spark_run.py", "--brief", SP + "/briefs/SMOKE-arms-path.md", "--repo", S + "/smoke_repo",
                        "--out", S + "/arms_" + name[0], "--base-url", "http://127.0.0.1:18999/v1"], capture_output=True, text=True)
    res = "PASS" if r.returncode == want else "FAIL"; ok &= r.returncode == want
    print(f"{res}  {name}: rc={r.returncode} want={want}")
srv.shutdown(); sys.exit(0 if ok else 1)
