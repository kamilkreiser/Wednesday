#!/usr/bin/env python3
"""Seat X 8th: PRE-RUN RECORD + QUALIFICATION for the card secuura-push-queue-prerun-preflight-1106 (option a). Derived from Seat X 5th's prerun_x5.py after gate 227 (F1, F4, F5, F9, F12, F14).
Subcommands:
  run      <worktree> <outdir> [--max-load 12] [--preflight-cmd CMD --read-every N (TEST ONLY: marks the record stub)]   hold a slot, record sha, run the hook's checks outside the lock, write record.json
  qualify  <record.json> <push_sha> --branch B --worktree W --cells-file F [--max-age 7200] [--now EPOCH]                exit 0 = the pre-run counts; exit 5 = refused, rules named
  pr-line  <record.json>                                                                                                the --no-verify line, generated from the record
Rules, each refused independently (a test turns one off by qualify(disabled=...), never by the environment):
  wellformed stub output_hash output_binding binding slot tip tree_stable rc verdict skipped_set leg_headers signal_env cells suites_line format_gate age
F1 (Wednesday's ANSWER 08:30:32Z, option 2 re-sourced): no rule reads a per-leg table or a `legs timed` line. What they proved is read from develop's own text:
  the verdict ratio; the two named-skip lines directly under the LAST verdict (skipped_set); the printed `=== n/N ... ===` headers, exactly 1..N in order, above that verdict (leg_headers).
X8 (gate 237): N is the legs pin beside the tool (prerun_expected_legs_x8.txt, 16 at develop a65ae7ed), read once; every tree read honours git's exit code (N1); `run` checks the three pins before any leg (N5);
  the slot holder names its worktree, so the push driver can see a pre-run live in its tree (N4b, `live_in_tree`)."""
import argparse, datetime as dt, hashlib, json, os, re, signal, subprocess, sys, time

CARD = "secuura-push-queue-prerun-preflight-1106"
HERE = os.path.dirname(os.path.abspath(__file__))
STACK_LEGS = {3, 4, 8}          # legs that need a booted local stack; the only legs allowed to be skipped
N_SLOTS = 3                     # Kam's "at most 3-4 at once"; Wednesday's ANSWER to X 5th set 3. Enforced here, not by a note (F12).
READ_EVERY = 60                 # F9: seconds between reads of HEAD and the tree during a pre-run
RULES = "wellformed stub output_hash output_binding binding slot tip tree_stable rc verdict skipped_set leg_headers signal_env cells suites_line format_gate age".split()
VERDICT = re.compile(r"(?m)^(PREFLIGHT (?:PASSED|FAILED|INCOMPLETE|ABORTED).*)$")
STACK_LINE = re.compile(r"  legs((?: \d+)+) — local stack not up; you can clear this by starting it\.")
ENV_LINE = re.compile(r"  legs((?: \d+)+) — environment \(offline / registry unreachable / deps missing\)\.")
# X8 (gate 237 N5): ONE source for the leg count, a pin file beside the tool (Wednesday edits it, like the hook pin). Read once; unreadable or not one positive integer -> None, and then no record qualifies
# (verdict and leg_headers refuse) and `run` refuses fast. Used at every site that once said 16: the header pattern, the verdict rule, leg_headers, and the PR line.
LEGS_PIN_FILE = os.path.join(HERE, "prerun_expected_legs_x8.txt")
CELLS_PIN_FILE = os.path.join(HERE, "prerun_expected_cells_x8.txt")
HOOK_PIN_FILE = os.path.join(HERE, "prerun_expected_hook_x8.txt")
SUITE_FILE = "Blockchain/Dev/scripts/__tests__/run_shell_suites.test.sh"      # the file whose cells the cells pin counts
PREFLIGHT_FILE = "Blockchain/Dev/scripts/preflight/preflight.sh"             # states its own total once, `TOTAL_LEGS=16` (line 185 at develop a65ae7ed)


def read_legs_pin():
    try:
        t = open(LEGS_PIN_FILE).read().split()
    except OSError:
        return None
    return int(t[0]) if len(t) == 1 and t[0].isdigit() and int(t[0]) > 0 else None


N_LEGS = read_legs_pin()
HEADER = re.compile(rf"(?m)^=== (\d+)/{N_LEGS}\b.*===$" if N_LEGS else r"(?!)")


def read_cells(path):
    """-> (count, blob or None). Line 1 is the expected run_shell_suites count (decide and qualify read only this); line 2, `blob <40 hex> <path>`, is the test file that count came from (`run` checks it at HEAD).
    A one-line file still gives the count. Raises on an unreadable file or a first line that is not one integer."""
    lines = open(path).read().splitlines()
    count = int(lines[0].strip())
    m = re.fullmatch(r"blob ([0-9a-f]{40}) (\S+)", lines[1].strip()) if len(lines) > 1 else None
    return count, (m.group(1) if m and m.group(2) == SUITE_FILE else None)


def pin_reasons(wt, sha):
    """X8 (gate 237 N5): the three pins, checked against the commit BEFORE any leg runs, so a seat whose pre-run could never qualify is told in seconds, not after ~20 minutes on a slot.
    It saves time only: a seat refused here has no record, and its push takes the hook at the turn, exactly as a stale pin already sent it there."""
    why = []
    try:
        want = open(HOOK_PIN_FILE).read().strip()
    except OSError:
        want = ""
    h = subprocess.run(["git", "--no-optional-locks", "-C", wt, "show", f"{sha}:.githooks/pre-push"], capture_output=True)
    if h.returncode != 0:
        why.append(f"hook pin: cannot read .githooks/pre-push at {sha[:12]} (rc {h.returncode})")
    elif hashlib.sha256(h.stdout).hexdigest() != want:
        why.append(f"hook pin: .githooks/pre-push at {sha[:12]} is sha256 {hashlib.sha256(h.stdout).hexdigest()[:16]}..., the pin in {HOOK_PIN_FILE} is [{want[:16]}]")
    try:
        _, blob = read_cells(CELLS_PIN_FILE)
    except (OSError, ValueError, IndexError) as e:
        blob = None; why.append(f"cells pin: {CELLS_PIN_FILE} is unreadable ({type(e).__name__})")
    b = git(wt, "rev-parse", f"{sha}:{SUITE_FILE}")
    if blob is None and not any(w.startswith("cells pin") for w in why):
        why.append(f"cells pin: {CELLS_PIN_FILE} names no `blob <sha> {SUITE_FILE}` line")
    elif blob and (b.returncode != 0 or b.stdout.strip() != blob):
        why.append(f"cells pin: {SUITE_FILE} at {sha[:12]} is blob [{b.stdout.strip()[:12]}] (rc {b.returncode}), the cells pin counted blob {blob[:12]}")
    pf = git(wt, "show", f"{sha}:{PREFLIGHT_FILE}")
    tot = re.findall(r"(?m)^TOTAL_LEGS=(\d+)\s*$", pf.stdout) if pf.returncode == 0 else []
    if N_LEGS is None:
        why.append(f"legs pin: {LEGS_PIN_FILE} is missing or not one positive integer")
    elif len(tot) != 1:
        why.append(f"legs pin: {PREFLIGHT_FILE} at {sha[:12]} states no single TOTAL_LEGS line ({len(tot)} found, rc {pf.returncode}); the pin is {N_LEGS}")
    elif int(tot[0]) != N_LEGS:
        why.append(f"legs pin: {PREFLIGHT_FILE} at {sha[:12]} says TOTAL_LEGS={tot[0]}, the pin is {N_LEGS}")
    return why


def parse_output(text):
    """Everything is judged relative to the LAST verdict line. Suite output above it can print a verdict-shaped line; it cannot feed the named-skip lines, which are read only directly after that last verdict."""
    vs = list(VERDICT.finditer(text))
    last = vs[-1] if vs else None
    above = text[:last.start()] if last else text
    stack, envl = [], []
    for line in (text[last.end():].split("\n")[1:] if last else []):
        a, b = STACK_LINE.fullmatch(line), ENV_LINE.fullmatch(line)
        if a:
            stack += [int(x) for x in a.group(1).split()]
        elif b:
            envl += [int(x) for x in b.group(1).split()]
        else:
            break
    sig = re.search(r"(?m)^ *\(signal environment: INT installable=(\w+), TERM installable=(\w+)\)$", above)
    cells = re.findall(r"(?m)^run_shell_suites: (\d+) passed, (\d+) failed", above)
    suites = re.findall(r"(?m)^shell suites: (\d+) passed, (\d+) failed, (\d+) skipped \(of (\d+)\)$", above)
    return dict(verdict=last.group(1) if last else None, stack_skips=stack, env_skips=envl, headers=[int(x) for x in HEADER.findall(above)],
                signal_env=dict(int_=sig.group(1), term=sig.group(2)) if sig else None,
                run_shell_suites=[int(cells[-1][0]), int(cells[-1][1])] if cells else None, suites_line=[int(x) for x in suites[-1]] if suites else None)


def load1(): return float(subprocess.run(["sysctl", "-n", "vm.loadavg"], capture_output=True, text=True).stdout.split()[1])


def slot_base(): return os.path.join(HERE, "slots")          # fixed: derived from the tool's own path, so every seat using this copy shares one cap


def proc_start(pid):
    r = subprocess.run(["ps", "-o", "lstart=", "-p", str(pid)], capture_output=True, text=True)
    return r.stdout.strip() if r.returncode == 0 else ""


def holder_live(d):
    """Is this slot's holder alive? Pid AND its start time (pid reuse), or the pre-run's own process group. A holder file not written yet is live while the slot is young."""
    try:
        h = json.load(open(d + "/holder"))
    except (OSError, ValueError):
        try:
            return time.time() - os.path.getmtime(d) < 60
        except OSError:
            return True
    pid, start, pgid = h.get("pid"), h.get("start"), h.get("pgid")
    if isinstance(pid, int) and start and proc_start(pid) == start:
        return True
    if isinstance(pgid, int):
        try:
            os.killpg(pgid, 0)
            return True
        except (ProcessLookupError, PermissionError):
            pass
    return False


def reclaim(d):
    """A slot whose holder is dead is moved aside by one atomic rename, under a per-slot reclaim lock, and only after re-reading the holder under that lock: two reclaimers cannot both win, and a slot just re-taken by another seat is not moved. Returns True if the slot is free now."""
    lk = d + ".reclaim"
    try:
        os.mkdir(lk)
    except FileExistsError:
        try:
            if time.time() - os.path.getmtime(lk) > 300:      # a reclaimer that died mid-way; this attempt only clears it, the next one reclaims
                os.rmdir(lk)
        except OSError:
            pass
        return False
    try:
        if holder_live(d):
            return False
        os.rename(d, f"{d}.dead.{time.time_ns()}.{os.getpid()}")
        return True
    except OSError:
        return False
    finally:
        os.rmdir(lk)


def acquire_slot(wt=None):
    """-> (n, dir) or None. An own successful mkdir per slot, holder written only after it succeeded (STANDING_LINES lock rules). X8 (N4b): the holder names the worktree."""
    base = slot_base()
    os.makedirs(base, exist_ok=True)
    for i in range(1, N_SLOTS + 1):
        d = f"{base}/.prerun-slot-{i}"
        try:
            os.mkdir(d)
        except FileExistsError:
            if not reclaim(d):
                continue
            try:
                os.mkdir(d)
            except FileExistsError:
                continue
        write_holder(d, wt=wt)
        return i, d
    return None


def write_holder(d, pgid=None, wt=None):
    tmp = f"{d}/holder.tmp"
    json.dump(dict(pid=os.getpid(), start=proc_start(os.getpid()), pgid=pgid, worktree=wt, at=dt.datetime.now(dt.timezone.utc).isoformat()), open(tmp, "w"))   # X8 (gate 237 N4b): the worktree, so a push driver can see a pre-run live in ITS tree
    os.rename(tmp, d + "/holder")


def live_in_tree(wt):
    """X8 (gate 237 N4b): -> [(n, pid)] of the slots, in THIS tool's slots/ folder, whose holder names this worktree and is alive (holder_live: pid and its start time, or the pre-run's group).
    BOUND: a pre-run run from another copy of the tool uses another slots/ folder and is not seen; a slot whose holder file is not written yet names no worktree and is not counted."""
    want, out = os.path.realpath(wt), []
    base = slot_base()
    for i in range(1, N_SLOTS + 1):
        d = f"{base}/.prerun-slot-{i}"
        try:
            h = json.load(open(d + "/holder"))
        except (OSError, ValueError):
            continue
        if h.get("worktree") == want and holder_live(d):
            out.append((i, h.get("pid")))
    return out


def release_slot(d):
    os.remove(d + "/holder"); os.rmdir(d)        # holder first, then rmdir; either failing raises (a failed release is loud)


def git(wt, *a): return subprocess.run(["git", "--no-optional-locks", "-C", wt] + list(a), capture_output=True, text=True)     # no index.lock: a leg running git at the same moment must not lose a race to this read


def hook_changed_set_COPY(wt, tip):
    """THIS IS A COPY, named as one for the gate (Wednesday's ANSWER 08:30:32Z). It re-implements _judge_ref in .githooks/pre-push at 35bcfa000, NEW-BRANCH CASE ONLY, because the hook cannot be called part way. Returns (all_changed, st_all, st_base_stale).
    What guards the copy against drift: the hook's sha is pinned (prerun_expected_hook_x8.txt, F10); a different hook takes the hook path, so this copy only ever answers for the hook it was copied from. Test: test_tools_x8 compares it with the REAL hook on the same commits."""
    g = lambda *a: git(wt, "-c", "core.quotePath=false", *a)
    br = git(wt, "rev-parse", "--abbrev-ref", "HEAD").stdout.strip()
    up = git(wt, "rev-parse", "--abbrev-ref", f"{br}@{{upstream}}")
    if up.returncode == 0 and up.stdout.strip():
        upn = up.stdout.strip()
        return g("diff", "--no-renames", "--name-only", upn, tip).stdout.strip("\n"), 0, (1 if upn.split("/", 1)[-1] != br else 0)
    base, informative, all_changed = "", 0, ""
    refs = ["refs/heads/develop", "refs/remotes/origin/develop"]
    ld, od = git(wt, "rev-parse", "--verify", "--quiet", "refs/heads/develop"), git(wt, "rev-parse", "--verify", "--quiet", "origin/develop")
    if ld.returncode == 0 and od.returncode == 0 and ld.stdout != od.stdout and git(wt, "merge-base", "--is-ancestor", "refs/heads/develop", "origin/develop").returncode == 0:
        refs = ["refs/remotes/origin/develop"]         # KS-991: local develop is behind origin/develop
    for ref in refs:
        if git(wt, "show-ref", "--verify", "--quiet", ref).returncode != 0:
            continue
        mb = git(wt, "merge-base", ref, tip)
        b = mb.stdout.strip() if mb.returncode == 0 else ""
        if not b:
            continue
        base = b
        if b == tip:
            continue
        informative = 1
        files = g("diff", "--no-renames", "--name-only", b, tip).stdout.rstrip("\n")
        all_changed = f"{all_changed}\n{files}\n"
        if any(f.startswith("Blockchain/Dev/") for f in files.split("\n")):
            break
    return all_changed.rstrip("\n"), (1 if (base and not informative) or not base else 0), 1


def format_gate(wt, tip, outdir):
    """F5: the hook's own mode against the branch's changed set, with the FORMAT_GATE_TREE the hook passes. The output is KEPT, hashed in the record, and any named SKIP reaches the PR line."""
    script = os.path.join(wt, "systemTest/scripts/check-package-format.sh")
    out = f"{outdir}/format_gate.out"
    changed, st_all, stale = hook_changed_set_COPY(wt, tip)
    env = dict(os.environ, FORMAT_GATE_TREE=tip)
    if not os.path.exists(script):                     # the hook refuses this too (lines 311-319)
        text, rc, mode = f"[format-gate] REFUSED — the KS-989 formatting gate is missing at: {script}\n", 1, "missing"
    else:
        if st_all:
            p = subprocess.run(["bash", script, "--all"], cwd=wt, stdin=subprocess.DEVNULL, env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True); mode = "--all (the hook's own choice: no informative base)"
        else:
            env["FORMAT_GATE_BASE_MAY_BE_STALE"] = str(stale)
            p = subprocess.run(["bash", script], cwd=wt, input=changed + "\n", env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True); mode = "hook stdin"
        text, rc = p.stdout, p.returncode
    open(out, "w").write(text)
    named = [l[:200] for l in text.splitlines() if "[format-gate]" in l and re.search(r"SKIP|REFUSED|NOTHING CHECKED|package\(s\) checked", l)]
    return dict(ran=True, rc=rc, mode=mode, st_all=st_all, base_may_be_stale=stale, output=out, output_sha256=hashlib.sha256(open(out, "rb").read()).hexdigest(), named=named)


def tree_look(wt, sha):
    # X8 (gate 237 N1): each read's exit code is read. A read that fails is NOT a clean read: it is recorded as moved, so qualify refuses tree_stable and the push takes the hook.
    h, s = git(wt, "rev-parse", "HEAD"), git(wt, "status", "--porcelain")
    now = dt.datetime.now(dt.timezone.utc).strftime('%H:%M:%SZ')
    if h.returncode != 0 or s.returncode != 0:
        why = "; ".join(x for x in ((f"HEAD read FAILED rc {h.returncode}" if h.returncode else ""), (f"status FAILED rc {s.returncode}" if s.returncode else "")) if x)
        return f"{now} {why}: {(s.stderr if s.returncode else h.stderr).strip()[:160]}"
    head, st = h.stdout.strip(), s.stdout.strip()
    return None if head == sha and not st else f"{now} HEAD {head[:12]} status [{st[:200]}]"


def run(wt, outdir, max_load, stub_cmd, read_every):
    os.makedirs(outdir, exist_ok=True)
    if signal.getsignal(signal.SIGINT) == signal.SIG_IGN: sys.exit("REFUSE: SIGINT is ignored in this launcher; a pre-run must keep default signal dispositions")
    l = load1()
    if l >= max_load: sys.exit(f"REFUSE: launch gate, load1 {l} is not below {max_load}")
    got = acquire_slot(os.path.realpath(wt))
    if got is None: sys.exit(f"REFUSE: no pre-run slot free ({N_SLOTS} in use, cap in {slot_base()})")
    n, slot = got; p = None

    def die(signum, _frame): raise SystemExit(128 + signum)         # so the finally below runs: the pre-run's group goes down and the slot is released
    signal.signal(signal.SIGTERM, die)
    try:
        hp = git(wt, "rev-parse", "HEAD")                            # X8 (gate 237 N1): every start read honours git's exit code
        if hp.returncode != 0 or not re.fullmatch(r"[0-9a-f]{40}", hp.stdout.strip()): sys.exit(f"REFUSE: cannot read HEAD (git rev-parse rc {hp.returncode})")
        sha = hp.stdout.strip()
        br = git(wt, "symbolic-ref", "--short", "-q", "HEAD").stdout.strip()
        if not br: sys.exit("REFUSE: HEAD is detached; a pre-run belongs to a named branch")
        sp = git(wt, "status", "--porcelain")
        if sp.returncode != 0: sys.exit(f"REFUSE: cannot read the working tree: git status rc {sp.returncode} ({sp.stderr.strip()[:160]}); a tree that cannot be read is not clean")
        if sp.stdout.strip(): sys.exit("REFUSE: working tree is not clean")
        if not stub_cmd:                                               # X8 (gate 237 N5): the pins first, before the format gate and before any leg; a stub run (test only) never qualifies anyway
            why = pin_reasons(wt, sha)
            if why: sys.exit("REFUSE fast, before any leg: this pre-run could not qualify, so it would only cost a slot; push on the hook path. " + " | ".join(why))
        rec = dict(schema=2, card=CARD, stub=bool(stub_cmd), launch="python-subprocess", worktree=os.path.realpath(wt), branch=br, sha=sha, load1_start=l, slot=dict(base=slot_base(), n=n, pid=os.getpid()), read_every=read_every,
                   started_utc=dt.datetime.now(dt.timezone.utc).isoformat(), tmpdir=os.environ.get("TMPDIR", ""))
        out = f"{outdir}/preflight.out"
        rec["format_gate"] = format_gate(wt, sha, outdir) if not stub_cmd else dict(ran=True, rc=0, mode="stub", named=[])
        cmd = stub_cmd or 'cd "$(git rev-parse --show-toplevel)" || exit 1; . systemTest/slot-target.sh >/dev/null 2>&1 || true; cd Blockchain/Dev && bash scripts/preflight/preflight.sh'
        moved, reads = [], 0
        with open(out, "w") as f:
            f.write(f"PRERUN sha={sha} branch={br}\n"); f.flush()      # F14: the output the record hashes names the commit
            p = subprocess.Popen(["bash", "-c", cmd], cwd=wt, stdin=subprocess.DEVNULL, stdout=f, stderr=subprocess.STDOUT, start_new_session=True)
            write_holder(slot, pgid=p.pid, wt=os.path.realpath(wt))     # a killed `run` leaves a live group behind: the slot stays held until that group is gone
            while True:
                try:
                    p.wait(timeout=read_every); break
                except subprocess.TimeoutExpired:
                    reads += 1; seen = tree_look(wt, sha)              # F9: BOUND: an edit made and restored inside one interval is not seen
                    if seen: moved.append(seen)
        he, se = git(wt, "rev-parse", "HEAD"), git(wt, "status", "--porcelain")     # X8 (gate 237 N1): a failed end read is not clean and names no sha
        rec.update(rc=p.returncode, output_sha256=hashlib.sha256(open(out, "rb").read()).hexdigest(), finished_utc=dt.datetime.now(dt.timezone.utc).isoformat(), output=out,
                   sha_end=he.stdout.strip() if he.returncode == 0 else "", tree_clean_end=se.returncode == 0 and not se.stdout.strip(), tree_end_status_rc=se.returncode, tree_reads=reads, tree_moved=moved,
                   parsed=parse_output(open(out, errors="replace").read()))
        json.dump(rec, open(f"{outdir}/record.json", "w"), indent=1)
        print(f"record {outdir}/record.json sha {sha[:12]} rc {rec['rc']} stub {rec['stub']} slot {n}/{N_SLOTS} tree_reads {reads} tree_moved {len(moved)} format_gate rc {rec['format_gate']['rc']}")
    finally:
        if p is not None and p.poll() is None:
            try:
                os.killpg(p.pid, signal.SIGTERM)
            except ProcessLookupError:
                pass
        release_slot(slot)


def qualify(rec, push_sha, now, max_age, cells, branch=None, worktree=None, disabled=frozenset()):
    """Return the list of rules that REFUSE this pre-run for this push. Empty list = it counts. `disabled` is for tests, by import only (F4: nothing here reads the environment)."""
    dis, bad = set(disabled), []
    def chk(rule, ok, why):
        if rule not in dis and not ok: bad.append(f"{rule}: {why}")
    try:
        fin = dt.datetime.fromisoformat(rec["finished_utc"]).timestamp()
        ok_shape = all(k in rec for k in ("sha", "sha_end", "tree_clean_end", "rc", "format_gate", "launch", "branch", "worktree", "output", "output_sha256")) and rec.get("schema") == 2
    except Exception:
        fin, ok_shape = 0, False
    chk("wellformed", ok_shape, "record is missing fields or is not schema 2")
    if not ok_shape and "wellformed" not in dis: return bad
    chk("stub", not rec.get("stub"), "a stub record (test only) never counts")
    # the parsed values come from the OUTPUT FILE, re-read here; rec["parsed"] is for humans and is ignored. A missing file parses to nothing, so every output rule refuses.
    try:
        raw = open(rec["output"], "rb").read(); text = raw.decode(errors="replace"); pr = parse_output(text); hash_ok = hashlib.sha256(raw).hexdigest() == rec["output_sha256"]
    except OSError:
        text, pr, hash_ok = "", {}, False
    chk("output_hash", hash_ok, f"output file {rec['output']} is missing or its sha256 differs from the record's")
    first = text.split("\n", 1)[0]
    chk("output_binding", first == f"PRERUN sha={rec['sha']} branch={rec['branch']}", f"the output's first line is [{first[:90]}], the record says sha {rec['sha'][:12]} branch {rec['branch']}")
    chk("binding", branch is not None and worktree is not None and rec["branch"] == branch and rec["worktree"] == os.path.realpath(worktree),
        f"record is for branch {rec['branch']} in {rec['worktree']}, asked for branch {branch} in {worktree}")
    sl = rec.get("slot")
    chk("slot", isinstance(sl, dict) and sl.get("base") == slot_base() and sl.get("n") in range(1, N_SLOTS + 1) and isinstance(sl.get("pid"), int), f"the record did not hold a pre-run slot here ({sl}); the cap is in {slot_base()}")
    chk("tip", rec["sha"] == push_sha and rec["sha_end"] == push_sha and rec["tree_clean_end"], f"judged {rec['sha'][:12]} (end {rec['sha_end'][:12]}, clean {rec['tree_clean_end']}), pushing {push_sha[:12]}")
    chk("tree_stable", rec.get("tree_moved") == [], f"HEAD or the tree moved during the pre-run: {str(rec.get('tree_moved'))[:200]}")
    chk("rc", rec["rc"] == 0, f"preflight rc {rec['rc']}")
    v = pr.get("verdict") or ""
    mp = re.fullmatch(rf"PREFLIGHT PASSED — {N_LEGS}/{N_LEGS} legs ran\.", v) if N_LEGS else None; mi = re.fullmatch(rf"PREFLIGHT INCOMPLETE — (\d+)/{N_LEGS} legs ran, (\d+) SKIPPED\. Nothing failed\.", v) if N_LEGS else None
    chk("verdict", bool(mp) or bool(mi and int(mi.group(1)) + int(mi.group(2)) == N_LEGS), f"verdict line is [{v[:70]}] (legs pin {N_LEGS})")
    k = 0 if mp else (int(mi.group(2)) if mi else None)
    st, en = pr.get("stack_skips", []), pr.get("env_skips", [])
    chk("skipped_set", k is not None and set(st) <= STACK_LEGS and not en and len(st) + len(en) == k and len(set(st)) == len(st), f"verdict says {k} skipped; named stack legs {st}, named environment legs {en} (only stack-down legs {sorted(STACK_LEGS)} may skip, and the names must add up)")
    hd = pr.get("headers", [])
    chk("leg_headers", N_LEGS is not None and hd == list(range(1, N_LEGS + 1)), f"printed leg headers are {hd if len(hd) < 20 else str(len(hd)) + ' lines'}, not 1..{N_LEGS} in order (legs pin {N_LEGS})")
    se = pr.get("signal_env") or {}
    chk("signal_env", se.get("int_") == "yes" and se.get("term") == "yes", f"signal environment {se}")
    rs = pr.get("run_shell_suites") or [0, 99]
    chk("cells", cells is not None and rs[0] == cells and rs[1] == 0, f"run_shell_suites {rs}, expected {cells} passed, 0 failed (the expected figure comes from the cells file)")
    s = pr.get("suites_line") or [0, 99, 0, 0]
    chk("suites_line", s[1] == 0 and s[2] == 0 and s[0] == s[3] and s[3] > 0, f"shell suites line {s}")
    fg = rec.get("format_gate", {}) if isinstance(rec.get("format_gate"), dict) else {}
    try:
        fg_ok = hashlib.sha256(open(fg["output"], "rb").read()).hexdigest() == fg["output_sha256"]
    except (OSError, KeyError, TypeError):
        fg_ok = False
    chk("format_gate", fg.get("ran") and fg.get("rc") == 0 and fg_ok, f"format gate rc {fg.get('rc')}, ran {fg.get('ran')}, its kept output matches its hash: {fg_ok}")
    chk("age", 0 <= now - fin <= max_age, f"pre-run finished {int(now - fin)} s ago, limit {max_age} s")
    return bad


def pr_line(rec):
    """Kam's ruling: each PR states --no-verify and which checks ran. Generated from the record; a format-gate SKIP is named, never lost."""
    pr = parse_output(open(rec["output"], errors="replace").read()); s = pr["suites_line"]; ran = re.search(rf"(\d+)/{N_LEGS} legs ran", pr["verdict"]).group(1)
    fg = rec["format_gate"]; skips = pr["stack_skips"]
    named = "; ".join(fg.get("named", [])) or "no format-gate summary line"
    return (f"Pushed with --no-verify under Kam's ruling on card {CARD} (option a, 2026-11-06). The checks ran BEFORE the push, outside the push lock, on {rec['sha'][:12]}, the commit pushed: preflight {ran}/{N_LEGS} legs ran"
            f"{(', legs ' + ' '.join(map(str, skips)) + ' skipped (stack down)') if skips else ''}, {pr['verdict'].rstrip('.')}; shell suites {s[0]} passed, {s[1]} failed, {s[2]} skipped (of {s[3]}); "
            f"run_shell_suites {pr['run_shell_suites'][0]} cells; signal environment INT installable={pr['signal_env']['int_']}; systemTest format gate rc {fg['rc']} ({fg['mode'].split(' (')[0]}): {named}; "
            f"HEAD and tree read {rec.get('tree_reads', 0)} times during the run, nothing moved; finished {rec['finished_utc'][:19]}Z. Record: {rec['output']}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(); sp = ap.add_subparsers(dest="cmd", required=True)
    a = sp.add_parser("run"); a.add_argument("wt"); a.add_argument("outdir"); a.add_argument("--max-load", type=float, default=12); a.add_argument("--preflight-cmd"); a.add_argument("--read-every", type=int)
    b = sp.add_parser("qualify"); b.add_argument("record"); b.add_argument("push_sha"); b.add_argument("--branch"); b.add_argument("--worktree"); b.add_argument("--max-age", type=int, default=7200); b.add_argument("--cells-file"); b.add_argument("--now", type=float)
    c = sp.add_parser("pr-line"); c.add_argument("record")
    o = ap.parse_args()
    if o.cmd == "run":
        if o.read_every is not None and not o.preflight_cmd: sys.exit("REFUSE: --read-every is test only and needs --preflight-cmd (which marks the record stub)")
        run(o.wt, o.outdir, o.max_load, o.preflight_cmd, o.read_every or READ_EVERY)
    elif o.cmd == "qualify":
        cells, cerr = None, None
        try: cells = read_cells(o.cells_file)[0]                      # X8 (N5): line 1 is the count; a blob line may follow
        except Exception as e: cerr = f"cells: expected cell count file {o.cells_file!r} is missing, unreadable or not one integer ({type(e).__name__}); a stale or absent file REFUSES, it never passes"
        try: bad = qualify(json.load(open(o.record)), o.push_sha, o.now or time.time(), o.max_age, cells, o.branch, o.worktree)
        except Exception as e: bad = [f"wellformed: record unreadable ({type(e).__name__}: {e})"]
        if cerr: bad = [b for b in bad if not b.startswith("cells:")] + [cerr]
        print("QUALIFIES" if not bad else "REFUSED"); [print("  " + x) for x in bad]; sys.exit(0 if not bad else 5)
    else:
        print(pr_line(json.load(open(o.record))))
