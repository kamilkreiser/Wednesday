def b64_windows(key, win=18):
    out = set()
    for i in range(0, len(key) - win):
        w = key[i:i + win]
        for enc in (base64.b64encode, base64.urlsafe_b64encode):
            s = enc(w).decode().rstrip("=")
            out.add(s[4:-4])  # inner part is alignment-independent
    return out


def needles(key):
    n = []
    for i in range(0, len(key) - 16, 4):
        w = key[i:i + 16]
        n.append(("hex", w.hex())); n.append(("HEX", w.hex().upper()))
        n.append(("dec", ", ".join(str(x) for x in w)))
        n.append(("dec-nospace", ",".join(str(x) for x in w)))
    for s in b64_windows(key):
        n.append(("b64", s))
    return n


def scan_text(text, key):
    for kind, s in needles(key):
        if s and s in text:
            return kind
    # base64 of the whole key at any of 3 offsets (control for long runs)
    return None


def sec_scan():
    log(f"== SCAN: {len(ALL_OUTPUT)} captured outputs against {len(KEYS)} keys")
    # positive controls
    if KEYS:
        k = KEYS[0]
        ctl = {"hex": k.hex(), "HEX": k.hex().upper(), "b64": base64.b64encode(k).decode(), "b64url": base64.urlsafe_b64encode(k[1:]).decode(),
               "dec": "[" + ", ".join(str(x) for x in k) + "]"}
        log("SCAN positive controls:", {n: scan_text("prefix " + t + " suffix", k) for n, t in ctl.items()})
    hits = []
    for label, text in ALL_OUTPUT:
        for k in KEYS:
            kind = scan_text(text, k)
            if kind:
                hits.append((label, kind))
    log(f"SCAN hits: {len(hits)} {hits[:10]}")
