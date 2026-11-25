#!/usr/bin/env python3
"""QA-DAEMON-NOTES item 4(b): a changed relay certificate through the real coagentd.
Usage: python3 -B qa_cert.py <bin dir> <work dir (new)>
Host a (own relay, saved identity at first), guest b. Steps, each recording b's
status.session.relay_identity_changed, the number of design-06 lines and of each Down reason in b's log."""
import os, socket, sys, threading, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from qa_lib import Q, port_of

TEXT = "The relay's identity changed. That happens when the host restarted it without a saved identity. It also happens when something is impersonating the relay. Ask the host for a new invitation; do not retry."
TEXT_LINE = "coagentd: " + TEXT + "\n"
CHANGED = "session link down (relay identity changed (pin mismatch)); reconnecting"
UNREACH = "session link down (relay unreachable"

q = Q(sys.argv[1], sys.argv[2])
rows = []
fail = []


def snap(step, want_field, want_text):
    s = q.status("b")["session"]
    log = q.stderr("b")
    f = s.get("relay_identity_changed", "ABSENT")
    nt = log.count(TEXT)
    nl = log.count(TEXT_LINE)
    row = (step, f, nt, nl, log.count(CHANGED), log.count(UNREACH), s.get("connected"), s.get("reconnects"))
    rows.append(row)
    ok = f == want_field and nt == want_text and nl == want_text
    if not ok:
        fail.append(f"{step}: field {f} (want {want_field}), text {nt}/{nl} (want {want_text})")
    print(("OK  " if ok else "BAD ") + f"{step} | field={f} | text_count={nt} whole_lines={nl} | changed_lines={row[4]} | unreachable_lines={row[5]} | connected={row[6]} | reconnects={row[7]}", flush=True)


def wait_more(pat, n, t=180):
    base = q.stderr("b").count(pat)
    q.until(f"{n} more '{pat}' lines", t, lambda: q.stderr("b").count(pat) >= base + n, 0.2)


class Listener:
    """A plain TCP listener on the relay's port: 'close' accepts and closes at once; 'garbage' writes
    an HTTP line and closes. Neither is TLS: a refused handshake for a reason that is NOT a pin."""
    def __init__(self, port, mode):
        self.s = socket.socket()
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.bind(("127.0.0.1", port))
        self.s.listen(16)
        self.s.settimeout(0.2)
        self.mode, self.n, self.go = mode, 0, True
        self.t = threading.Thread(target=self.run, daemon=True)
        self.t.start()

    def run(self):
        while self.go:
            try:
                c, _ = self.s.accept()
            except socket.timeout:
                continue
            self.n += 1
            if self.mode == "garbage":
                try:
                    c.sendall(b"HTTP/1.1 400 Bad Request\r\nContent-Length: 0\r\n\r\n")
                except OSError:
                    pass
            c.close()

    def close(self):
        self.go = False
        self.t.join()
        self.s.close()


try:
    q.start("a", ["--keep-relay-identity"])
    q.start("b")
    q.pair("a", "b")
    url0 = q.status("a")["session"]["relays"][0]["url"]
    pin0 = q.status("a")["session"]["relays"][0]["pin"]
    port = port_of(url0)
    print(f"host relay port {port}", flush=True)
    snap("S0 attached", False, 0)

    # S1: the host and its relay merely down (port closed: tcp connect refused).
    q.crash("a")
    wait_more(UNREACH, 2)
    snap("S1 relay down (unreachable), 2 retries", False, 0)

    # S2/S3: something on the port that refuses the TLS handshake for another reason.
    for mode in ("close", "garbage"):
        L = Listener(port, mode)
        before = q.stderr("b")
        wait_more(UNREACH, 2)
        L.close()
        new = q.stderr("b")[len(before):]
        reasons = sorted(set(l for l in new.splitlines() if "session link down" in l))
        print(f"   listener '{mode}' accepted {L.n} connection(s); reasons seen: {reasons}", flush=True)
        snap(f"S{2 if mode == 'close' else 3} non-TLS listener '{mode}' on the port, 2 retries", False, 0)

    # S4: the host back WITH its saved identity: reconnects, field false.
    q.start("a", ["--keep-relay-identity"])
    assert q.status("a")["session"]["relays"][0]["pin"] == pin0
    q.wait_connected("a", "b", 180)
    snap("S4 restart with saved identity, reattached", False, 0)

    # S5: an impersonator: another relay (another certificate) on the same port.
    q.crash("a")
    time.sleep(0.5)
    imp, iurl, ipin = q.outside_relay(f"127.0.0.1:{port}")
    print(f"   impersonator up at {iurl} (pin differs: {ipin.replace(':','').lower() != pin0.replace(':','').lower()})", flush=True)
    t5 = q.until("field true", 180, lambda: q.status("b")["session"].get("relay_identity_changed") is True)
    print(f"   field true {t5:.1f}s after the impersonator started", flush=True)
    snap("S5 impersonator on the port: named", True, 1)
    wait_more(CHANGED, 3)
    snap("S5b three more mismatching retries: still one line", True, 1)

    # S6: the impersonator gone (port closed again): the last failure is no longer a mismatch.
    imp.kill(); imp.wait()
    wait_more(UNREACH, 1)
    snap("S6 port closed again: field back to false, no new line", False, 1)

    # S7: the host restarted WITHOUT its saved identity (a new certificate): a new change, one more line.
    q.start("a", [])
    pin1 = q.status("a")["session"]["relays"][0]["pin"]
    print(f"   host restarted without identity; new pin: {pin1 != pin0}; same url: {q.status('a')['session']['relays'][0]['url'] == url0}", flush=True)
    t7 = q.until("field true again", 180, lambda: q.status("b")["session"].get("relay_identity_changed") is True)
    print(f"   field true {t7:.1f}s after the host's restart", flush=True)
    snap("S7 host restart without saved identity: named", True, 2)
    wait_more(CHANGED, 3)
    snap("S7b three more retries: still one more line only", True, 2)

    # S8: a successful attach clears it (the guest follows the host's relay.moved line).
    line = q.status("a")["relay_moved_line"]
    assert q.ctl("b", "join", {"blob": line})["ok"] is True
    q.wait_connected("a", "b", 120)
    snap("S8 joined the relay.moved line, attached: cleared", False, 2)
    host_field = q.status("a")["session"].get("relay_identity_changed")
    print(f"   host's own field: {host_field}", flush=True)
    if host_field is not False:
        fail.append(f"host field {host_field}")
finally:
    left = q.cleanup()
    print(f"processes left and killed by cleanup: {left}")

# Exact line form of the design-06 line in b's log.
for l in q.stderr("b").splitlines():
    if TEXT in l:
        print("LINE: " + l)
print("ALL OK" if not fail else "FAILURES: " + "; ".join(fail))
