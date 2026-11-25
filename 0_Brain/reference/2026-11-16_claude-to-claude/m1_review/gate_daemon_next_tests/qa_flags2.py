#!/usr/bin/env python3
"""QA-DAEMON-NEXT (d), a copy of the DAEMON-NOTES check's qa_flags.py (a1-a7) extended: every started case
also runs `invite` (its answer, the url carried in the invitation line, the `mailbox open failed` lines),
plus the url whitespace cases and an OUTSIDE `coagent relay` (qa_lib.outside_relay) padded / unpadded.
Original header: QA-DAEMON-NOTES item 4(a): coagentd's relay flags through the real binary.
Usage: python3 -B qa_flags.py <bin dir> <work dir>
For each case: exit code, exact stderr, and whether the data folder (or anything in the case's own
HOME/TMPDIR) was created. Positive cases are started, checked for IPC, then stopped by ctl/SIGTERM."""
import base64, json, os, signal, subprocess, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from qa_lib import Q

BIN, WORK = sys.argv[1], sys.argv[2]
COAGENTD = os.path.join(BIN, "coagentd")
URL_EMPTY = "coagentd: --relay-url is empty"
PIN_EMPTY = 'coagentd: --relay-pin is empty after removing "sha256:" and colons'
TOGETHER = "coagentd: --relay-url and --relay-pin go together"
GOOD_URL = "wss://127.0.0.1:9/v1"
GOOD_PIN = "sha256:" + ":".join(["ab"] * 32)

n = 0
results = []


def _relays(blob):
    """The relay entries an invitation carries (whatever key holds url/pin)."""
    out = []
    def walk(v):
        if isinstance(v, dict):
            if "url" in v:
                out.append({k: v[k] for k in ("url", "pin") if k in v})
            for x in v.values():
                walk(x)
        elif isinstance(v, list):
            for x in v:
                walk(x)
    walk(blob)
    return out if out else blob


def case(name, args, want_code, want_err, start_ok=False):
    global n
    n += 1
    root = os.path.join(WORK, f"f{n:02d}")
    os.makedirs(root)
    home, tmp = os.path.join(root, "h"), os.path.join(root, "t")
    os.makedirs(home)
    os.makedirs(tmp)
    data = os.path.join(root, "d")
    env = {"PATH": "/usr/bin:/bin", "HOME": home, "TMPDIR": tmp}
    argv = [COAGENTD, "--data-dir", data, "--idle-exit-secs", "300"] + args
    if not start_ok:
        try:
            p = subprocess.run(argv, env=env, capture_output=True, timeout=5)
        except subprocess.TimeoutExpired:  # a build that accepts the value starts and keeps running (killed by run())
            created = os.path.exists(data)
            results.append((name, args, "STARTED (still running at 5 s; killed)", "", bool(created), False))
            return
        err = p.stderr.decode()
        created = os.path.exists(data) or os.listdir(home) or os.listdir(tmp)
        ok = p.returncode == want_code and err == want_err + "\n" and not created
        results.append((name, args, p.returncode, err.rstrip("\n"), bool(created), ok))
        return
    errf = open(os.path.join(root, "stderr"), "wb")
    p = subprocess.Popen(argv, env=env, stdout=subprocess.DEVNULL, stderr=errf)
    up = False
    for _ in range(150):
        if p.poll() is not None:
            break
        r = subprocess.run([COAGENTD, "ctl", "--data-dir", data, '{"v":1,"id":1,"cmd":"status"}'],
                           env=env, capture_output=True, timeout=20)
        if r.returncode == 0 and json.loads(r.stdout or b"{}").get("ok"):
            up = True
            break
        time.sleep(0.1)
    inv_s = "n/a"
    if up:
        r = subprocess.run([COAGENTD, "ctl", "--data-dir", data, '{"v":1,"id":1,"cmd":"invite","args":{}}'],
                           env=env, capture_output=True, timeout=30)
        v = json.loads(r.stdout or b"{}")
        if v.get("ok"):
            line = v["result"]["line"]
            b64 = line.split()[-1]
            try:
                blob = json.loads(base64.urlsafe_b64decode(b64 + "=" * (-len(b64) % 4)))
            except Exception as e:
                blob = f"(undecodable: {e})"
            inv_s = "ok relays_in_line=" + json.dumps(_relays(blob), ensure_ascii=True)
        else:
            inv_s = v.get("error", {}).get("code", str(v))
        time.sleep(0.5)
    p.send_signal(signal.SIGTERM)
    try:
        code = p.wait(15)
    except subprocess.TimeoutExpired:
        p.kill()
        code = "killed"
    err = open(os.path.join(root, "stderr")).read()
    bad_lines = [l for l in err.splitlines() if "is empty" in l or "go together" in l]
    mb = [l for l in err.splitlines() if "mailbox open failed" in l]
    ok = up and not bad_lines
    results.append((name, args, f"started={up} invite={inv_s} mailbox_lines={json.dumps(mb)} exit_on_term={code}", "; ".join(bad_lines) or "(no refusal)", None, ok))


# Refusals
for v, label in [("", "empty"), ("  ", "spaces"), ("\t", "tab"), ("\t \n", "tab+space+newline"),
                 (" ", "no-break space")]:
    case(f"url {label}", ["--relay-url", v, "--relay-pin", GOOD_PIN], 2, URL_EMPTY)
for v, label in [("", "empty"), ("  ", "spaces"), ("\t", "tab"), ("sha256:", "sha256: only"),
                 (":::", "colons only"), (" sha256::: ", "sha256 + colons + spaces"),
                 ("sha256:sha256:", "sha256: twice"), ("\tsha256:\t", "tab-wrapped sha256:")]:
    case(f"pin {label}", ["--relay-url", GOOD_URL, "--relay-pin", v], 2, PIN_EMPTY)
case("both empty (url named first)", ["--relay-url", "", "--relay-pin", ""], 2, URL_EMPTY)
case("pin first on the line, both empty", ["--relay-pin", "", "--relay-url", ""], 2, URL_EMPTY)
case("url given twice, last empty", ["--relay-url", GOOD_URL, "--relay-url", "", "--relay-pin", GOOD_PIN], 2, URL_EMPTY)
case("pin given twice, last empty", ["--relay-url", GOOD_URL, "--relay-pin", GOOD_PIN, "--relay-pin", ":"], 2, PIN_EMPTY)
case("url alone empty", ["--relay-url", ""], 2, TOGETHER)
case("pin alone empty", ["--relay-pin", ""], 2, TOGETHER)
case("url with no value", ["--relay-url"], 2,
     "coagentd: --relay-url needs a value\n" + subprocess.run([COAGENTD, "--help"], capture_output=True).stdout.decode().rstrip("\n"))
# Starts
case("well-formed pair", ["--relay-url", GOOD_URL, "--relay-pin", GOOD_PIN], 0, "", start_ok=True)
case("url and pin with surrounding spaces", ["--relay-url", "  " + GOOD_URL + "  ", "--relay-pin", "  " + GOOD_PIN + "\t"], 0, "", start_ok=True)
case("url given twice, last good", ["--relay-url", "", "--relay-url", GOOD_URL, "--relay-pin", GOOD_PIN], 0, "", start_ok=True)
case("url sha256: only (scope call iii)", ["--relay-url", "sha256:", "--relay-pin", GOOD_PIN], 0, "", start_ok=True)
case("url ::: only (scope call iii)", ["--relay-url", ":::", "--relay-pin", GOOD_PIN], 0, "", start_ok=True)
case("pin without sha256: prefix", ["--relay-url", GOOD_URL, "--relay-pin", "ab" * 32], 0, "", start_ok=True)
case("no relay flags at all", [], 0, "", start_ok=True)

# (d) url whitespace cases, each started and given `invite` (port 9: closed)
U = GOOD_URL
for v, label in [(" " + U, "leading blank"), (U + "\t", "trailing tab"), (" " + U + "\t", "leading blank and trailing tab"),
                 (U + "\n", "trailing line feed"), (U + "\r", "trailing carriage return"),
                 ("\u00a0" + U, "leading U+00A0"), (U + "\u3000", "trailing U+3000"), ("\ufeff" + U, "leading U+FEFF"),
                 ("wss://127.0.0.1:9/v 1", "blank INSIDE the url")]:
    case(f"URL {label}", ["--relay-url", v, "--relay-pin", GOOD_PIN], 0, "", start_ok=True)
case("URL only blanks (refused)", ["--relay-url", " \t \u3000", "--relay-pin", GOOD_PIN], 2, URL_EMPTY)
case("URL and pin both blank-padded", ["--relay-url", " " + U + "\t", "--relay-pin", "\t" + GOOD_PIN + " "], 0, "", start_ok=True)
# OUTSIDE relay (qa_lib.outside_relay, this build's own `coagent relay`, loopback)
oq = Q(BIN, os.path.join(WORK, "outside"))
try:
    _, OURL, OPIN = oq.outside_relay()
    case("OUTSIDE relay, url as printed", ["--relay-url", OURL, "--relay-pin", OPIN], 0, "", start_ok=True)
    case("OUTSIDE relay, url with a leading blank and a trailing tab", ["--relay-url", " " + OURL + "\t", "--relay-pin", OPIN], 0, "", start_ok=True)
    case("OUTSIDE relay, url with a trailing U+3000", ["--relay-url", OURL + "\u3000", "--relay-pin", OPIN], 0, "", start_ok=True)
    case("OUTSIDE relay, url with a leading U+FEFF", ["--relay-url", "\ufeff" + OURL, "--relay-pin", OPIN], 0, "", start_ok=True)
finally:
    oq.cleanup()

allok = True
for name, args, code, err, created, ok in results:
    allok &= ok
    print(f"{'OK ' if ok else 'BAD'} | {name} | args={json.dumps(args, ensure_ascii=True)} | exit={code} | stderr={json.dumps(err)} | created={created}")
print("ALL OK" if allok else "SOME BAD")
