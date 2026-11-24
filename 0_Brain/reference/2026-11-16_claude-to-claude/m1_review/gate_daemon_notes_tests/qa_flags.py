#!/usr/bin/env python3
"""QA-DAEMON-NOTES item 4(a): coagentd's relay flags through the real binary.
Usage: python3 -B qa_flags.py <bin dir> <work dir>
For each case: exit code, exact stderr, and whether the data folder (or anything in the case's own
HOME/TMPDIR) was created. Positive cases are started, checked for IPC, then stopped by ctl/SIGTERM."""
import json, os, signal, subprocess, sys, time

BIN, WORK = sys.argv[1], sys.argv[2]
COAGENTD = os.path.join(BIN, "coagentd")
URL_EMPTY = "coagentd: --relay-url is empty"
PIN_EMPTY = 'coagentd: --relay-pin is empty after removing "sha256:" and colons'
TOGETHER = "coagentd: --relay-url and --relay-pin go together"
GOOD_URL = "wss://127.0.0.1:9/v1"
GOOD_PIN = "sha256:" + ":".join(["ab"] * 32)

n = 0
results = []


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
    p.send_signal(signal.SIGTERM)
    try:
        code = p.wait(15)
    except subprocess.TimeoutExpired:
        p.kill()
        code = "killed"
    err = open(os.path.join(root, "stderr")).read()
    bad_lines = [l for l in err.splitlines() if "is empty" in l or "go together" in l]
    ok = up and not bad_lines
    results.append((name, args, f"started={up} exit_on_term={code}", "; ".join(bad_lines) or "(no refusal)", None, ok))


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

allok = True
for name, args, code, err, created, ok in results:
    allok &= ok
    print(f"{'OK ' if ok else 'BAD'} | {name} | args={json.dumps(args)} | exit={code} | stderr={json.dumps(err)} | created={created}")
print("ALL OK" if allok else "SOME BAD")
