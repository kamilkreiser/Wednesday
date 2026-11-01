# Stub GitHub API for the umbrella-gate red-proofs. usage: stub_github.py <port> <config.json>
# config: {"<num>": {"state":"open","merged":false,"files":["path",...],"files_status":200}}
import json, sys, re
from http.server import BaseHTTPRequestHandler, HTTPServer
port, cfg = int(sys.argv[1]), json.load(open(sys.argv[2]))
class H(BaseHTTPRequestHandler):
    def log_message(self, *a): sys.stderr.write("stub: " + (a[0] % a[1:]) + "\n")
    def _send(self, code, obj):
        b = json.dumps(obj).encode(); self.send_response(code); self.send_header("Content-Type","application/json"); self.send_header("Content-Length",str(len(b))); self.end_headers(); self.wfile.write(b)
    def do_GET(self):
        m = re.match(r"^/repos/[^/]+/[^/]+/pulls/(\d+)(/files)?(\?.*)?$", self.path)
        if not m: return self._send(404, {"message":"Not Found"})
        # PR numbers not in the config are the ticket's REAL attached PRs: answer them as merged so only the planted PRs matter
        c = cfg.get(m.group(1), {"state":"closed","merged":True,"files":[]})
        if m.group(2):
            if c.get("files_status", 200) != 200: return self._send(c["files_status"], {"message":"stubbed files API failure"})
            return self._send(200, [{"filename": f} for f in c["files"]])
        self._send(200, {"state": c["state"], "merged": c["merged"]})
HTTPServer(("127.0.0.1", port), H).serve_forever()
