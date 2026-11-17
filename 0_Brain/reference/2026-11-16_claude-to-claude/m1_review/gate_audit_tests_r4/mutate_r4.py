#!/usr/bin/env python3
"""Gate r4 mutation driver for coagent-audit at 52d12e9 (design 07 rules).

Each mutant removes or inverts ONE design-07 rule in the source (plain code, no red-control cfg),
is applied alone to a pristine copy, and the whole coagent-audit suite runs (--no-fail-fast; the
copy also holds the gate's own tests/gate_r4.rs). The failing tests are recorded, split into the
seat's tests and gate_r4's. The file is restored with `git checkout` after each mutant.

usage: mutate_r4.py <workdir-with-copies> <n-workers> <out.json> [ids...]
Copies: <workdir>/mut1 .. mutN (each a full copy of the repository with gate_r4 registered).
"""
import json, os, re, subprocess, sys, threading, time

SRC = "crates/coagent-audit/src/"
S = SRC + "session.rs"
B = SRC + "budget.rs"

# id, design-07 rule, file, old, new, nth occurrence (0 = must be unique)
MUTANTS = [
    ("M01", "1.4b seat byte limit (exact size)", S, "if u_b + size > l_b && !cfg", "if u_b > l_b && !cfg", 0),
    ("M02", "1.4b seat record limit", S, "if u_r + 1 > l_r && !cfg", "if u_r > l_r && !cfg", 0),
    ("M03", "1.4b closing checkpoint held back in the free part", S, "used.0 + size + reserve.0 > limit.0", "used.0 + size > limit.0", 0),
    ("M04", "1.4b requested allowance = one seventh of the requested half", S, "                self.limits.requested_allowance(),\n", "                self.limits.free_part(),\n", 0),
    ("M05", "4.2 replacing a slot releases the old charge (store = accounting)", S, "if let Some(old) = self.index.insert(key, size) {\n            self.unaccount_size(key, old);\n        }", "self.index.insert(key, size);", 0),
    ("M06", "1.9 release deletes from the store", S, "self.store.remove(&self.session_id, &key)?;", "let _ = &key;", 0),
    ("M07", "1.7 step 5 space check on a received event", S, "        let slot = slot.ok_or(AuditError::NotMember(author))?;\n        self.seat_room(slot, size)?;\n", "        let slot = slot.ok_or(AuditError::NotMember(author))?;\n", 0),
    ("M08", "1.5 D / 1.8 checkpoint beyond a full seat goes to the fixed slot", S, "&& self.seat_room(slot, size).is_ok();", ";", 0),
    ("M09", "P27 evidence cap is four", S, "if held >= cap {", "if held > cap {", 0),
    ("M10", "1.4a cross-check: two slots per reporter (broadcast, addressed)", S, "n: u64::from(hs.to.is_some()),", "n: 0,", 0),
    ("M11", "1.4a roster lifetime backstops (256 versions, 32 keys)", S, "if next.body.version > MAX_ROSTER_VERSIONS as u64 || keys.len() > MAX_KEYS_EVER {", "if false {", 0),
    ("M12", "1.10 start refuses a used store", S, "if !store.list(&session_id)?.is_empty() && !cfg", "if false && !cfg", 0),
    ("M13", "1.10 resume charges each record to its own part", S, "                a.account(k, size);\n", "                a.account(StoreKey { part: if matches!(k.part, Part::OwnEvent(_)) { Part::OwnEvent(None) } else { k.part }, ..k }, size);\n", 0),
    ("M14", "1.4b one requester cannot use another's allowance", S, "self.commit_own(e, Part::OwnEvent(Some(slot)))", "self.commit_own(e, Part::OwnEvent(Some(slot.min(0))))", 0),
    ("M15", "1.4b a record is charged to its author's seat", S, "                part: Part::PeerEvent(slot),\n", "                part: Part::PeerEvent(0),\n", 0),
    ("M16", "1.11 / R2-M1 nothing kept from a removed reporter", S, "let reporter_current = self.roster.current().role_of(&hs.from).is_some()", "let reporter_current = true", 0),
    ("M17", "1.9 release only for a key not in the roster", S, "if self.roster.current().role_of(key).is_some() {", "if false {", 0),
    ("M18", "1.7 step 3 a forked event's evidence is stored", S, "                self.store_evidence(&ev, Some(author))?;\n                return Err(AuditError::Receive(ReceiveError::Fork(ev)));", "                return Err(AuditError::Receive(ReceiveError::Fork(ev)));", 1),
    ("M19", "1.7 step 3 a forked checkpoint's evidence is stored", S, "                self.store_evidence(&ev, Some(author))?;\n                return Err(AuditError::Receive(ReceiveError::Fork(ev)));", "                return Err(AuditError::Receive(ReceiveError::Fork(ev)));", 2),
    ("M20", "R2-M1 no countersignature from a removed member", S, "if self.roster.current().role_of(&cs.by).is_none()", "if false", 0),
    ("M21", "4.2 a non-advancing cross-check record is NotNewer", S, ".is_none_or(|last| advances(last, hs))", ".is_none_or(|_| true)", 0),
    ("M22", "4.1 the FIRST roster conflict is kept", S, "if self.conflict.is_none() {", "if true {", 0),
    ("M23", "1.4b own checkpoints are charged to the free part (space checked)", S, "            self.own_room(Part::OwnHead, size, true)?;\n", "", 0),
    ("M24", "1.7 step 5 exact framed size (4-byte frame counted)", S, "Ok(4 + canonical::encode(r)?.len())", "Ok(canonical::encode(r)?.len())", 0),
    ("M25", "1.4b own seat = seat minus one byte per record (P7)", B, "(seat.0.saturating_sub(seat.1), seat.1)", "(seat.0, seat.1)", 0),
    ("M26", "1.10 resume rebuilds the cross-check slots", S, "                    a.hs_slots.insert((hs.from, hs.to), hs);\n", "                    let _ = hs;\n", 0),
    ("M27", "1.10 resume rebuilds the evidence table", S, "                    a.evidence.entry(ev.author()).or_default().push(ev);\n", "                    let _ = ev;\n", 0),
    ("M28", "1.10 resume rebuilds the roster conflict slot", S, "                    a.conflict = Some(x);\n", "                    let _ = x;\n", 0),
    ("M29", "1.4b seat limit is one eighth (per_peer)", S, "        let (l_b, l_r) = self.limits.per_peer();\n", "        let (l_b, l_r) = self.limits.peer_pool();\n", 0),
    ("M30", "(R4-M1 check) own checkpoints charged outside the free part", S, "                    part: Part::OwnHead,\n", "                    part: Part::OwnEvent(Some(7)),\n", 0),
    ("M31", "(R4-m1 check) own event stored before the chain advances", S, ["        let seq = self.own.commit(e)?;\n", "            &r,\n        )?;\n        Ok(seq)\n    }\n\n    /// The store."], ["        let seq = self.own.seq() + 1;\n        let e2 = e.clone();\n", "            &r,\n        )?;\n        self.own.commit(e2)?;\n        Ok(seq)\n    }\n\n    /// The store."], 0),
    ("M32", "(R4-m1 check) received event stored before the chain advances", S, ["        if let Some(c) = self.peers.get_mut(&author) {\n            c.commit(e, a);\n        }\n        self.write(\n            StoreKey {\n                part: Part::PeerEvent(slot),\n                author,\n                n: a.seq,\n            },\n            &r,\n        )?;\n"], ["        self.write(\n            StoreKey {\n                part: Part::PeerEvent(slot),\n                author,\n                n: a.seq,\n            },\n            &r,\n        )?;\n        if let Some(c) = self.peers.get_mut(&author) {\n            c.commit(e, a);\n        }\n"], 0),
    ("M33", "(R4-m2 check) own records also count the own slot's peer records", S, "let mut used = self.free_usage();", "let mut used = Self::add(self.free_usage(), Self::add(self.part(Part::PeerEvent(self.local_slot())), self.part(Part::PeerHead(self.local_slot()))));", 0),
]

def apply(path, old, new, nth):
    if isinstance(old, list):
        for o, n in zip(old, new):
            apply(path, o, n, nth)
        return
    s = open(path).read()
    n = s.count(old)
    if nth == 0:
        if n != 1:
            raise SystemExit(f"{path}: expected exactly one occurrence, found {n}: {old!r}")
        s = s.replace(old, new)
    else:
        if n < nth:
            raise SystemExit(f"{path}: occurrence {nth} not found ({n})")
        i = -1
        for _ in range(nth):
            i = s.index(old, i + 1)
        s = s[:i] + new + s[i + len(old):]
    open(path, "w").write(s)

def run(copy, target, mid, rule, f, old, new, nth, env, results, lock):
    p = os.path.join(copy, f)
    apply(p, old, new, nth)
    t0 = time.time()
    out = subprocess.run(
        ["cargo", "test", "--offline", "--locked", "-p", "coagent-audit", "--no-fail-fast"],
        cwd=copy, env=dict(env, CARGO_TARGET_DIR=target, R4_CASES="48"),
        capture_output=True, text=True)
    subprocess.run(["git", "checkout", "--", f], cwd=copy, check=True)
    log = out.stdout + out.stderr
    open(os.path.join(os.path.dirname(copy), "mutlogs", mid + ".log"), "w").write(log)
    failed = sorted(set(re.findall(r"^test (\S+) \.\.\. FAILED", log, re.M)))
    # which test binary each failure came from
    bins = re.split(r"Running (?:unittests )?\S*?(?:tests/)?([a-z0-9_]+)\.rs", log)
    by_bin = {}
    for i in range(1, len(bins) - 1, 2):
        for t in re.findall(r"^test (\S+) \.\.\. FAILED", bins[i + 1], re.M):
            by_bin.setdefault(bins[i], []).append(t)
    compile_error = "error[E" in log or "could not compile" in log
    seat = {b: v for b, v in by_bin.items() if b != "gate_r4"}
    mine = by_bin.get("gate_r4", [])
    with lock:
        results[mid] = dict(rule=rule, file=f, old=old, new=new, rc=out.returncode,
                            compile_error=compile_error, seat_failed=seat, r4_failed=mine,
                            seconds=round(time.time() - t0))
        print(f"{mid} {rule}: rc={out.returncode} compile_error={compile_error} "
              f"seat={sum(len(v) for v in seat.values())} r4={len(mine)} ({round(time.time()-t0)} s)", flush=True)

def main():
    work, nw, outp = sys.argv[1], int(sys.argv[2]), sys.argv[3]
    ids = set(sys.argv[4:])
    todo = [m for m in MUTANTS if not ids or m[0] in ids]
    os.makedirs(os.path.join(work, "mutlogs"), exist_ok=True)
    env = dict(os.environ)
    results, lock = {}, threading.Lock()
    queue = list(todo)
    def worker(i):
        copy = os.path.join(work, f"mut{i}")
        target = os.path.join(work, f"target_mut{i}")
        while True:
            with lock:
                if not queue:
                    return
                m = queue.pop(0)
            run(copy, target, *m, env, results, lock)
    ths = [threading.Thread(target=worker, args=(i + 1,)) for i in range(nw)]
    for t in ths: t.start()
    for t in ths: t.join()
    json.dump(results, open(outp, "w"), indent=1, sort_keys=True)

if __name__ == "__main__":
    main()
