"""QA-DAEMON-NOTES helpers: real coagentd / coagent / coagent-mcp processes, loopback only, every data
folder under the given work dir. Import with sys.path set to this folder; run with python3 -B."""
import json, os, signal, socket, subprocess, time


class Q:
    def __init__(self, bindir, root):
        self.bin = bindir
        self.root = root
        os.makedirs(root, exist_ok=False)
        self.home = os.path.join(root, "home")
        self.tmp = os.path.join(root, "tmp")
        os.makedirs(self.home)
        os.makedirs(self.tmp)
        self.procs = {}   # name -> Popen
        self.extra = []   # other Popen (outside relays)
        self.seen_pids = set()
        self.log = []

    def env(self):
        return {"PATH": "/usr/bin:/bin", "HOME": self.home, "TMPDIR": self.tmp}

    def dir(self, name):
        return os.path.join(self.root, name)

    def errf(self, name):
        return os.path.join(self.root, name + ".stderr")

    def stderr(self, name):
        try:
            return open(self.errf(name), encoding="utf-8", errors="replace").read()
        except FileNotFoundError:
            return ""

    def start(self, name, extra=(), wait=True):
        f = open(self.errf(name), "ab")
        argv = [os.path.join(self.bin, "coagentd"), "--data-dir", self.dir(name), "--coagent",
                os.path.join(self.bin, "coagent"), "--idle-exit-secs", "600"] + list(extra)
        p = subprocess.Popen(argv, env=self.env(), stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=f)
        self.procs[name] = p
        if wait:
            self.until(f"{name} IPC ready", 15, lambda: self.ctl_raw(name, {"v": 1, "id": 1, "cmd": "status"}) is not None)
        return p

    def ctl_raw(self, name, req):
        r = subprocess.run([os.path.join(self.bin, "coagentd"), "ctl", "--data-dir", self.dir(name), json.dumps(req)],
                           env=self.env(), capture_output=True, timeout=30)
        if r.returncode != 0 and not r.stdout:
            return None
        try:
            return json.loads(r.stdout)
        except Exception:
            return None

    def ctl(self, name, cmd, args=None):
        req = {"v": 1, "id": 1, "cmd": cmd}
        if args is not None:
            req["args"] = args
        v = self.ctl_raw(name, req)
        if v is None:
            raise RuntimeError(f"ctl {cmd} on {name}: no answer")
        return v

    def status(self, name):
        r = self.ctl(name, "status")["result"]
        rel = r.get("relay") or {}
        for k in ("relay_pid", "guard_pid"):
            if isinstance(rel.get(k), int):
                self.seen_pids.add(rel[k])
        return r

    def until(self, what, t, f, step=0.1):
        t0 = time.time()
        while time.time() - t0 < t:
            if f():
                return time.time() - t0
            time.sleep(step)
        raise AssertionError(f"timed out after {t}s waiting for: {what}")

    def pair(self, a, b, delay=0.0):
        inv = self.ctl(a, "invite", {})
        assert inv.get("ok") is True, f"invite: {inv}"
        self.status(a)
        if delay:
            time.sleep(delay)
        j = self.ctl(b, "join", {"blob": inv["result"]["line"]})
        assert j.get("ok") is True, f"join: {j}"
        self.wait_connected(a, b)

    def wait_connected(self, a, b, t=60):
        return self.until("both connected", t, lambda: self.status(a).get("session", {}).get("connected") is True
                          and self.status(b).get("session", {}).get("connected") is True)

    def crash(self, name):
        p = self.procs.pop(name)
        p.kill()
        p.wait()

    def stop(self, name):
        p = self.procs.pop(name)
        p.send_signal(signal.SIGTERM)
        try:
            return p.wait(20)
        except subprocess.TimeoutExpired:
            p.kill()
            p.wait()
            return "killed"

    def outside_relay(self, listen="127.0.0.1:0"):
        f = open(os.path.join(self.root, f"outside{len(self.extra)}.stderr"), "ab")
        p = subprocess.Popen([os.path.join(self.bin, "coagent"), "relay", "--listen", listen, "--status-secs", "0"],
                             env={"HOME": self.home}, cwd="/", stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=f)
        url = pin = None
        t0 = time.time()
        while url is None or pin is None:
            l = p.stdout.readline().decode()
            if not l:
                raise RuntimeError("outside relay exited")
            if l.startswith("url: "):
                url = l[5:].strip()
            elif l.startswith("fingerprint: "):
                pin = l[13:].strip()
            assert time.time() - t0 < 10
        self.extra.append(p)
        return p, url, pin

    def cleanup(self):
        for n in list(self.procs):
            try:
                self.stop(n)
            except Exception:
                pass
        for p in self.extra:
            if p.poll() is None:
                p.kill()
                p.wait()
        time.sleep(0.5)
        left = [p for p in self.seen_pids if alive(p)]
        for p in left:
            os.kill(p, signal.SIGKILL)
        return left


def alive(pid):
    try:
        os.kill(pid, 0)
        return True
    except ProcessLookupError:
        return False
    except PermissionError:
        return True


def port_of(url):
    hp = url.split("://", 1)[1].split("/", 1)[0]
    return int(hp.rsplit(":", 1)[1])


def keypaths(v, pre=""):
    """Every key path of a JSON value (arrays: their elements' paths under [])."""
    out = set()
    if isinstance(v, dict):
        for k, x in v.items():
            out.add(pre + "." + k)
            out |= keypaths(x, pre + "." + k)
    elif isinstance(v, list):
        for x in v:
            out |= keypaths(x, pre + "[]")
    return out
