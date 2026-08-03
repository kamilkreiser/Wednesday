from http.server import BaseHTTPRequestHandler, HTTPServer
import os, urllib.parse
DEST = "/Volumes/KK_T9_External_HDD/WEDNESDAY/0_Brain/reference/tac-course/transcripts"
class H(BaseHTTPRequestHandler):
    def _cors(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
    def do_OPTIONS(self):
        self.send_response(204); self._cors(); self.end_headers()
    def do_POST(self):
        n = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(n).decode("utf-8", "replace")
        q = urllib.parse.urlparse(self.path).query
        name = urllib.parse.parse_qs(q).get("name", ["unnamed"])[0]
        name = os.path.basename(name)
        if not name.endswith(".txt"): name += ".txt"
        with open(os.path.join(DEST, name), "w") as f: f.write(body)
        self.send_response(200); self._cors()
        self.send_header("Content-Type", "text/plain"); self.end_headers()
        self.wfile.write(f"saved {name} {len(body)}".encode())
    def log_message(self, *a): pass
HTTPServer(("127.0.0.1", 8899), H).serve_forever()
