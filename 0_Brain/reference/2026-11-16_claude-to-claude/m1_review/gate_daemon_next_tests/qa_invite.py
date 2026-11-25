#!/usr/bin/env python3
"""QA-DAEMON-NOTES item 4(c) and scope call (ii)/(iii): an invitation whose relay died, through the real
coagentd. Usage: python3 -B qa_invite.py <bin dir> <work dir (new)>"""
import os, signal, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from qa_lib import Q, alive

STOPPED = "the relay stopped while the invitation waited; create a new invitation"
LEFT = "the other side left the mailbox"
q = Q(sys.argv[1], sys.argv[2])
fail = []


def pairing(n):
    return q.status(n).get("pairing")


def invite(n):
    r = q.ctl(n, "invite", {})
    if r.get("ok") is not True:
        return r, None, None
    s = q.status(n)
    rel = s.get("relay") or {}
    return r, rel.get("relay_pid"), rel.get("guard_pid")


def wait_failed(n, t=15):
    t0 = time.time()
    while time.time() - t0 < t:
        p = pairing(n)
        if p and p.get("state") == "failed":
            return p, time.time() - t0
        time.sleep(0.05)
    return pairing(n), None


def check(name, cond, detail):
    print(("OK  " if cond else "BAD ") + f"{name} | {detail}", flush=True)
    if not cond:
        fail.append(name)


def gone(pids, t=15):
    t0 = time.time()
    while time.time() - t0 < t:
        if not any(alive(p) for p in pids if p):
            return True
        time.sleep(0.1)
    return False


try:
    q.start("a")
    j = 0

    def next_invite_pairs(case):
        global j
        j += 1
        nm = f"j{j}"
        q.start(nm)
        q.pair("a", nm)
        check(f"{case}: next invite without end pairs", True, f"paired with {nm}")
        q.ctl("a", "end", {})
        q.ctl(nm, "end", {})
        q.stop(nm)
        time.sleep(0.5)

    # C1 natural order: SIGKILL the RELAY (not the guard).
    r, relay, guard = invite("a")
    p, dt = wait_failed("a", 0.01)
    t0 = time.time()
    os.kill(relay, signal.SIGKILL)
    p, dt = wait_failed("a")
    check("C1 relay SIGKILL (natural order)", p.get("error") == STOPPED and dt is not None and dt < 2,
          f"pairing={p} after {dt and round(dt,2)}s; relay/guard gone={gone([relay, guard])}; status.relay={q.status('a').get('relay')}")
    next_invite_pairs("C1")

    # C2 exit first: SIGKILL the guard (relay alive until the daemon kills the orphan).
    r, relay, guard = invite("a")
    os.kill(guard, signal.SIGKILL)
    p, dt = wait_failed("a")
    check("C2 guard SIGKILL (exit notice first)", p.get("error") == STOPPED and dt is not None and dt < 2,
          f"pairing={p} after {dt and round(dt,2)}s; relay/guard gone={gone([relay, guard])}")
    next_invite_pairs("C2")

    # C3 drop first, exit within the grace (guard stopped 1.5 s).
    r, relay, guard = invite("a")
    os.kill(guard, signal.SIGSTOP)
    os.kill(relay, signal.SIGKILL)
    time.sleep(1.5)
    mid = pairing("a")
    os.kill(guard, signal.SIGCONT)
    p, dt = wait_failed("a")
    check("C3 mailbox drop first, exit after 1.5 s", mid.get("state") == "waiting" and p.get("error") == STOPPED,
          f"at 1.5 s: {mid}; then {p} {dt and round(dt,2)}s after the continue; gone={gone([relay, guard])}")
    next_invite_pairs("C3")

    # C4 exit notice later than the grace (guard held 8 s): the old text after ~3 s; nothing hangs.
    r, relay, guard = invite("a")
    os.kill(guard, signal.SIGSTOP)
    t0 = time.time()
    os.kill(relay, signal.SIGKILL)
    lat = []
    p = None
    while time.time() - t0 < 8:
        a0 = time.time()
        p = pairing("a")
        lat.append(time.time() - a0)
        if p.get("state") == "failed" and "tf" not in dir():
            tf = time.time() - t0
        time.sleep(0.1)
    os.kill(guard, signal.SIGCONT)
    g = gone([relay, guard])
    time.sleep(0.5)
    after = pairing("a")
    check("C4 exit notice 8 s late: old text after the grace; daemon answers meanwhile",
          p.get("error") == LEFT and 3.0 <= tf <= 4.5 and max(lat) < 1.0 and after.get("error") == LEFT,
          f"failed at {round(tf,2)}s with {p}; max status latency {round(max(lat),3)}s; after late exit: {after}; gone={g}; status.relay={q.status('a').get('relay')}")
    del tf
    next_invite_pairs("C4")

    # C5 healthy: an invitation that completes normally with a joiner delayed 6 s (beyond the grace).
    q.start("slow")
    q.pair("a", "slow", delay=6.0)
    check("C5 joiner delayed 6 s: pairs", True, f"pairing={pairing('a')}")
    q.ctl("a", "end", {})
    q.ctl("slow", "end", {})
    q.stop("slow")

    # C6 a daemon pointed at an OUTSIDE relay: its relay's death is the old path, at once.
    op, url, pin = q.outside_relay()
    q.start("x", ["--relay-url", url, "--relay-pin", pin])
    r = q.ctl("x", "invite", {})
    assert r["ok"] is True, r
    t0 = time.time()
    op.kill(); op.wait()
    p, dt = wait_failed("x")
    check("C6 outside relay killed: old text, no grace", p.get("error") == LEFT and dt is not None and dt < 1.5,
          f"pairing={p} after {dt and round(dt,2)}s; status.relay={q.status('x').get('relay')}")
    q.stop("x")

    # C7 scope call (iii): --relay-url holding only 'sha256:' / ':::' starts; invite fails, told how.
    for u in ("sha256:", ":::"):
        nm = "u" + str(len(u))
        q.start(nm, ["--relay-url", u, "--relay-pin", "sha256:" + ":".join(["ab"] * 32)])
        r = q.ctl(nm, "invite", {})
        s = q.status(nm)
        files = sorted(os.listdir(q.dir(nm)))
        code = q.stop(nm)
        log = [l for l in q.stderr(nm).splitlines() if "mailbox" in l or "invite" in l]
        check(f"C7 --relay-url {u!r}: invite refused, nothing running", r.get("ok") is False and s.get("relay") is None and s.get("pairing") in (None, {}) or r.get("ok") is False,
              f"reply={r}; status.relay={s.get('relay')}; status.pairing={s.get('pairing')}; data folder={files}; exit on TERM={code}; log={log}")

    # C8 a non-empty pin that is not a fingerprint: zero usable candidates (the NO_CANDIDATE text).
    q.start("np", ["--relay-url", "wss://127.0.0.1:9/v1", "--relay-pin", "xyz"])
    r = q.ctl("np", "invite", {})
    q.stop("np")
    log = [l for l in q.stderr("np").splitlines() if "mailbox" in l]
    check("C8 --relay-pin xyz: invite fails naming why", "coagentd: mailbox open failed: no usable relay candidate" in log,
          f"reply={r}; log={log}")

    # C9 url with surrounding spaces (legitimate value, accepted at start): what invite does.
    op, url, pin = q.outside_relay()
    q.start("sp", ["--relay-url", "  " + url + "  ", "--relay-pin", "  " + pin + "  "])
    r = q.ctl("sp", "invite", {})
    q.stop("sp")
    log = [l for l in q.stderr("sp").splitlines() if "mailbox" in l]
    print(f"INFO C9 url/pin with surrounding spaces: invite reply={r.get('ok')} {r.get('error')}; log={log}", flush=True)
    op.kill(); op.wait()

    # Host stderr lines of the diagnosis aid seen in this run.
    aid = [l for l in q.stderr("a").splitlines() if "relay guard" in l or "relay-guard" in l or "stop not confirmed" in l]
    for l in sorted(set(aid)):
        print("AID: " + l)
    for l in sorted(set(l for l in q.stderr("a").splitlines() if "pairing FAILED" in l)):
        print("FAILED-LINE: " + l)
finally:
    left = q.cleanup()
    print(f"processes left and killed by cleanup: {left}")
print("ALL OK" if not fail else "FAILURES: " + "; ".join(fail))
