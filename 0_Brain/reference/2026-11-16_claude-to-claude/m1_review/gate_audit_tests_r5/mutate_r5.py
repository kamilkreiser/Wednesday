#!/usr/bin/env python3
"""Gate r5 mutation driver: the NEW code of addendum 5/6 at 5f4577c (payer selection, hold-back,
all-or-nothing order per path, anchor). One mutant at a time on a copy; the whole coagent-audit suite
(--no-fail-fast; the copy also registers tests/gate_r5.rs). File restored with `git checkout`.

usage: mutate_r5.py <workdir> <n-workers> <out.json> [ids...]   (copies <workdir>/mut1..N)
       mutate_r5.py --check <repo>                              (every pattern occurs exactly once)
"""
import json, os, re, subprocess, sys, threading, time

SRC = "crates/coagent-audit/src/"
S = SRC + "session.rs"
A = SRC + "anchor.rs"
C = SRC + "chain.rs"
CP_ROOM = ("                self.own_room(\n"
           "                    payer.map_or(Part::OwnHead, |s| Part::OwnEvent(Some(s))),\n"
           "                    size,\n                    true,\n                )?;\n")
MUTANTS = [
    ("R01", "I-A11 newest requested event pays (mutant: oldest)", S,
     "self.own_req\n            .range(prev + 1..=n)\n            .next_back()", "self.own_req\n            .range(prev + 1..=n)\n            .next()"),
    ("R02", "coverage starts after the previous own checkpoint (mutant: from 1)", S, "range(prev + 1..=n)", "range(1..=n)"),
    ("R03", "coverage excludes the previous checkpoint's last event (mutant: prev..=n)", S, "range(prev + 1..=n)", "range(prev..=n)"),
    ("R04", "I-A13 hold-back, bytes", S,
     "(CLOSING_CHECKPOINT_BYTES, CLOSING_CHECKPOINT_RECORDS)\n                },\n            ),",
     "(0, CLOSING_CHECKPOINT_RECORDS)\n                },\n            ),"),
    ("R05", "I-A13 hold-back, records", S,
     "(CLOSING_CHECKPOINT_BYTES, CLOSING_CHECKPOINT_RECORDS)\n                },\n            ),",
     "(CLOSING_CHECKPOINT_BYTES, 0)\n                },\n            ),"),
    ("R06", "an allowance-paid checkpoint uses the held room (mutant: asks for a second hold-back)", S,
     CP_ROOM, CP_ROOM.replace("                    true,\n", "                    false,\n")),
    ("R07", "rule (c): never the free part instead (mutant: free part as fallback)", S,
     CP_ROOM, "                self.own_room(payer.map_or(Part::OwnHead, |s| Part::OwnEvent(Some(s))), size, true)\n                    .or_else(|_| self.own_room(Part::OwnHead, size, true))?;\n"),
    ("R08", "room asked of the PAYING part (mutant: always the free part)", S,
     CP_ROOM, CP_ROOM.replace("payer.map_or(Part::OwnHead, |s| Part::OwnEvent(Some(s)))", "Part::OwnHead")),
    ("R09", "R4-m1 own record: store, then apply", S,
     "        self.write(key, &r)?;\n        match self.own.commit(e) {",
     "        let seq0 = self.own.commit(e.clone())?;\n        self.write(key, &r)?;\n        match Ok::<u64, AuditError>(seq0) {"),
    ("R10", "R4-m1 own checkpoint: store, then apply", S,
     "                self.write(key, &rec)?;\n                if let Err(x) = self.own.commit_head(&h, now) {",
     "                self.own.commit_head(&h, now)?;\n                self.write(key, &rec)?;\n                if let Err(x) = Ok::<(), AuditError>(()) {"),
    ("R11", "R4-m1 received event: store, then apply", S,
     "        self.write(key, &r)?;\n        if !early {",
     "        if let Some(c) = self.peers.get_mut(&author) {\n            c.commit(e, a);\n        }\n        self.write(key, &r)?;\n        if false {"),
    ("R12", "R4-m1 joiner's anchor: store, then apply", S,
     ["        // R4-m1: stored first, then applied.\n        self.write(\n            StoreKey {\n                part: Part::Fixed(Table::Anchor),",
      "        )?;\n        self.peers.insert(anchor.author, c);\n        Ok(())"],
     ["        self.peers.insert(anchor.author, c);\n        self.write(\n            StoreKey {\n                part: Part::Fixed(Table::Anchor),",
      "        )?;\n        Ok(())"]),
    ("R13", "R4-m1 countersignature: put back on a failed write", S,
     "            self.own.restore_countersig(cs, before);", "            let _ = before;"),
    ("R14", "R4-m1 roster version: store, then apply", S,
     "let early = !cfg!(coagent_audit_red = \"commit_before_write\") && next.body.version > cur;", "let early = false;"),
    ("R15", "a refused newer roster version is removed again", S,
     "        if early && !matches!(applied, Ok(Applied::Advanced { .. })) {", "        if false {"),
    ("R16", "anchor: a shorter run is Behind", A, "            if have < run.count {", "            if false {"),
    ("R17", "anchor: a run's newest record Missing", A, "            if !held.contains_key(&key) {", "            if false {"),
    ("R18", "anchor: a replaced slot must be strictly newer (mutant: >=)", A,
     ".map(|r| slot_order(&r) > slot.order)", ".map(|r| slot_order(&r) >= slot.order)"),
    ("R19", "anchor: an older replaced slot is refused (mutant: any different order)", A,
     ".map(|r| slot_order(&r) > slot.order)", ".map(|r| slot_order(&r) != slot.order)"),
    ("R20", "anchor: session checked", S,
     "        if anchor.session_id != session_id {", "        if false {"),
    ("R21", "anchor(): run count", S, "            r.0 += 1;\n            r.1 = r.1.max(k.n);", "            r.0 = 1;\n            r.1 = r.1.max(k.n);"),
    ("R22", "anchor: from_bytes entry bounds", A,
     "if w.runs.len() > MAX_ANCHOR_RUNS || w.slots.len() > MAX_ANCHOR_SLOTS {",
     "if w.runs.len() > MAX_ANCHOR_RUNS + 1 || w.slots.len() > MAX_ANCHOR_SLOTS + 1 {"),
    ("R23", "anchor: from_bytes byte bound", A, "        if b.len() > MAX_ANCHOR_BYTES {", "        if false {"),
    ("R24", "restore_countersig puts the earlier one back", C,
     "        if let Some(b) = before {", "        let _ = before;\n        if let Some(b) = None::<Countersignature> {"),
    ("R25", "anchor digests kept on write", S,
     "        if !anchor::numbered(key.part) {\n            self.fixed_digests\n                .insert(key, (anchor::digest(&bytes), anchor::slot_order(r)));",
     "        if false {\n            self.fixed_digests\n                .insert(key, (anchor::digest(&bytes), anchor::slot_order(r)));"),
    ("R26", "anchor digests dropped on delete", S, "        self.fixed_digests.remove(&key);\n", ""),
    ("R27", "R4-m2 seat check keeps the part's hold-back", S,
     "if s_b + size + reserve.0 > l_b || s_r + 1 + reserve.1 > l_r {", "if s_b + size > l_b || s_r + 1 > l_r {"),
]

def apply(path, old, new, write=True):
    if isinstance(old, list):
        for o, n in zip(old, new):
            apply(path, o, n, write)
        return
    s = open(path).read()
    n = s.count(old)
    if n != 1:
        raise SystemExit(f"{path}: expected exactly one occurrence, found {n}: {old!r}")
    if write:
        open(path, "w").write(s.replace(old, new))

def run(copy, target, mid, rule, f, old, new, env, results, lock):
    apply(os.path.join(copy, f), old, new)
    t0 = time.time()
    out = subprocess.run(["cargo", "test", "--offline", "--locked", "-j", "2", "-p", "coagent-audit", "--no-fail-fast"],
                         cwd=copy, env=dict(env, CARGO_TARGET_DIR=target, R5_CASES="48"),
                         capture_output=True, text=True)
    subprocess.run(["git", "checkout", "--", f], cwd=copy, check=True)
    log = out.stdout + out.stderr
    open(os.path.join(os.path.dirname(copy), "mutlogs", mid + ".log"), "w").write(log)
    bins = re.split(r"Running (?:unittests )?\S*?(?:tests/)?([a-z0-9_]+)\.rs", log)
    by_bin = {}
    for i in range(1, len(bins) - 1, 2):
        for t in re.findall(r"^test (\S+) \.\.\. FAILED", bins[i + 1], re.M):
            by_bin.setdefault(bins[i], []).append(t)
    ce = "error[E" in log or "could not compile" in log
    seat = {b: v for b, v in by_bin.items() if b != "gate_r5"}
    mine = by_bin.get("gate_r5", [])
    with lock:
        results[mid] = dict(rule=rule, file=f, rc=out.returncode, compile_error=ce,
                            seat_failed=seat, r5_failed=mine, seconds=round(time.time() - t0))
        print(f"{mid} {rule}: rc={out.returncode} compile_error={ce} seat={sum(len(v) for v in seat.values())} "
              f"r5={len(mine)} ({round(time.time()-t0)} s)", flush=True)

def main():
    if sys.argv[1] == "--check":
        for m in MUTANTS:
            apply(os.path.join(sys.argv[2], m[2]), m[3], m[4], write=False)
        print(f"all {len(MUTANTS)} patterns unique"); return
    work, nw, outp = sys.argv[1], int(sys.argv[2]), sys.argv[3]
    ids = set(sys.argv[4:])
    queue = [m for m in MUTANTS if not ids or m[0] in ids]
    os.makedirs(os.path.join(work, "mutlogs"), exist_ok=True)
    env, results, lock = dict(os.environ), {}, threading.Lock()
    def worker(i):
        while True:
            with lock:
                if not queue: return
                m = queue.pop(0)
            run(os.path.join(work, f"mut{i}"), os.path.join(work, f"target_mut{i}"), *m, env, results, lock)
    ths = [threading.Thread(target=worker, args=(i + 1,)) for i in range(nw)]
    for t in ths: t.start()
    for t in ths: t.join()
    json.dump(results, open(outp, "w"), indent=1, sort_keys=True)

if __name__ == "__main__":
    main()
