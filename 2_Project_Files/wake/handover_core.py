#!/usr/bin/env python3
"""handover_core.py — the engine behind handover.sh (never called directly by a seat).

handover.sh resolves the seat and reads the clock; this file validates the block, asserts
conservation and writes. Standard library only. Never discards stderr.

Exit codes: 0 ok; 1 nothing to show / check found a fault; 2 usage or seat; 3 the block was refused;
4 conservation or I/O fault (nothing renamed into place); 5 the write lock is held, stale, or was taken away
before a rename (the message says what, if anything, was renamed); 6 both files were replaced but the lock was
no longer this process's at release: the write is NOT acknowledged.

THE LOCK (round 3, the checker's Blocker B1): two writes at once could both pass the changed-on-disk check
and the second pair of renames then overwrote the first writer's block. The WHOLE write, from the first read
of the state file to the second rename, now runs under an exclusive lock: a directory made with mkdir (atomic)
at 0_Brain/tasks/STATE-<seat>.lock.d, holding an `owner` file with the pid, host and start time. A second
writer WAITS (HANDOVER_LOCK_WAIT seconds, default 20) and then REFUSES with rc 5; it never proceeds unlocked.
A lock whose holder is no longer running is reported at once with the exact recovery line; this tool never
removes a lock it did not take.

ROUND 4 (the second checker's N2, N3, N4), what the lock now guarantees and how:
  (a) STALE is reported only after a SECOND LOOK: the mkdir is retried, the lock is read again, and the very
      same thing (same owner file, same dead pid, same directory) must still be there. A holder that finished
      normally between "read the owner" and "is that pid alive" is therefore never called dead.
  (b) Both temp files are written INSIDE the lock directory, under this call's token. A rename out of a lock
      directory that has been moved away (the recovery line run while this writer is alive) fails in the
      kernel, so a displaced writer renames nothing; before each rename the owner file is also re-read and
      must still carry this call's token. Either way: rc 5.
  (c) A writer whose lock is not its own at release exits rc 6 and does not print "written".
  An OWNER-LESS lock (no usable owner file) older than OWNERLESS_STALE_SECONDS is reported as stale with the
  recovery line (a writer killed between mkdir and the owner file, or between removing it and rmdir).
  An owner pid that is not a pid (0, or beyond a C int) is "no usable owner": a plain refusal, no traceback.
"""
import argparse
import binascii
import hashlib
import os
import re
import socket
import sys
import time

PARTS = ["FLOOR", "FIRST WORK", "OWED", "OPEN CARDS", "GRANTS IN PLAY"]
PART_HINT = {
    "FLOOR": "who is running",
    "FIRST WORK": "the first work of the next session",
    "OWED": "what is owed, to whom",
    "OPEN CARDS": "cards waiting on Kam",
    "GRANTS IN PLAY": "grants this state relies on",
}
# The same pattern as tools/note_entry.sh (X-DIGIT CLOCK GUARD, 2026-11-23): no instrument prints 11:4x.
XCLOCK = re.compile(r"(?:^|[^0-9A-Za-z:])((?:[01]?[0-9]|2[0-3]):(?:[0-5]x|xx))(?:[^0-9A-Za-z]|$)", re.I | re.M)
XCLOCK_MIN_REASON = 15
# The same seat -> legacy pickup mapping the launcher holds (PICKUP_FILE). Read by `seed` only; never written.
LEGACY_PICKUP = {"wednesday": "NEXT-PICKUP.md", "tuesday": "NEXT-PICKUP-TUESDAY.md", "friday": "NEXT-PICKUP-FRIDAY.md"}
SEED_REASON = "seeded verbatim from the legacy pickup's newest block"
LOCK_WAIT_DEFAULT = 20.0
OWNERLESS_STALE_SECONDS = 60.0
PID_MAX = 2 ** 31 - 1
# Test seams (HANDOVER_TREE, HANDOVER_TEST_STAMP, HANDOVER_TEST_BREAK) are honoured ONLY when the target tree is
# under one of these system temp / scratch roots. The list is fixed here on purpose: TMPDIR is not consulted,
# because a variable the caller sets must not be able to switch a seam on for a real tree.
TEMP_ROOTS = ("/tmp", "/private/tmp", "/var/folders", "/private/var/folders")
ZW = "\u200b\u200c\u200d\u2060\ufeff"
HEADING = re.compile(r"^[\s%s]*#{1,6}(?:[\s%s]|$)" % (ZW, ZW))
HEAD_OPEN = b"---\n"
HEAD_CLOSE = b"\n---\n"


def eprint(*a):
    print(*a, file=sys.stderr)


def sha(b):
    return hashlib.sha256(b).hexdigest()


def read_bytes(path):
    """-> bytes, or None when the file does not exist. Any other failure is a ReadFault (a refusal naming the
    path), never 'absent': an unreadable state file treated as absent would skip archiving its block."""
    if not os.path.lexists(path):
        return None
    try:
        with open(path, "rb") as f:
            return f.read()
    except OSError as e:
        raise ReadFault(path, e)


class ReadFault(Exception):
    def __init__(self, path, err):
        Exception.__init__(self, "cannot read %s: %s" % (path, err))


class LockBusy(Exception):
    pass


class LockLost(Exception):
    """The lock stopped being this call's while the write ran. .renamed: what had been renamed by then."""
    def __init__(self, when, renamed):
        Exception.__init__(self, when)
        self.renamed = renamed


def under_temp(path):
    rp = os.path.realpath(path)
    for r in TEMP_ROOTS:
        rr = os.path.realpath(r)
        if rp == rr or rp.startswith(rr.rstrip("/") + "/"):
            return True
    return False


def lock_dir(tasks_dir, seat):
    return os.path.join(tasks_dir, "STATE-%s.lock.d" % seat)


def lock_wait():
    try:
        w = float(os.environ.get("HANDOVER_LOCK_WAIT", LOCK_WAIT_DEFAULT))
    except ValueError:
        w = LOCK_WAIT_DEFAULT
    return max(0.2, min(w, 300.0))


def lock_owner(lock):
    """-> dict of the owner file's fields ({} when it is missing or half-written)."""
    out = {}
    try:
        with open(os.path.join(lock, "owner"), encoding="utf-8", errors="replace") as f:
            for line in f.read().split("\n"):
                if ":" in line:
                    k, v = line.split(":", 1)
                    out[k.strip()] = v.strip()
    except OSError:
        pass
    return out


def owner_pid(o):
    """-> the owner's pid as an int, or None when the owner file gives no usable one: missing, not a plain
    number, 0, or beyond a C int (N4: such a number is not a pid; asking the kernel about it is a traceback)."""
    v = o.get("pid", "")
    if not re.fullmatch(r"[0-9]{1,10}", v):
        return None
    n = int(v)
    return n if 0 < n <= PID_MAX else None


def pid_alive(pid):
    try:
        os.kill(pid, 0)
        return True
    except ProcessLookupError:
        return False
    except OSError:
        return True  # it exists but is not ours to signal


def recovery_line(lock):
    return "mv -n '%s' '%s.stale-%s'" % (lock, lock, time.strftime("%Y%m%d-%H%M%S"))


def stale_look(lock, host):
    """ONE look at a lock this call did not take. -> None when nothing proves it stale, else a tuple naming
    exactly what was seen: (kind, owner fields, directory inode, directory mtime). Two looks that return the
    same tuple saw the same lock, untouched, both times.
      'dead'       the owner file names a pid on THIS host and that process is not running
      'ownerless'  no usable owner file, and the directory has not changed for OWNERLESS_STALE_SECONDS
    The owner is read BEFORE the pid is tested, so a 'dead' answer says only "the pid I read is dead now";
    whether that pid still OWNS the lock is what the second look in acquire_lock settles."""
    o = lock_owner(lock)
    try:
        st = os.lstat(lock)
    except OSError:
        return None  # gone: the caller's next mkdir decides
    seen = (tuple(sorted(o.items())), st.st_ino, st.st_mtime_ns)
    pid = owner_pid(o)
    if pid is not None:
        if o.get("host") == host and not pid_alive(pid):
            return ("dead",) + seen
        return None
    if time.time() - st.st_mtime > OWNERLESS_STALE_SECONDS:
        return ("ownerless",) + seen
    return None


def take(lock, host, stamp):
    """mkdir is the lock. -> this call's token, or None when the directory is already there."""
    try:
        os.mkdir(lock)
    except FileExistsError:
        return None
    token = "%d-%s" % (os.getpid(), binascii.hexlify(os.urandom(8)).decode("ascii"))
    with open(os.path.join(lock, "owner"), "w", encoding="utf-8") as f:
        f.write("pid: %d\nhost: %s\nstarted: %s\nepoch: %d\ntoken: %s\n" % (os.getpid(), host, stamp, int(time.time()), token))
    return token


def acquire_lock(lock, stamp):
    """-> this call's token. Waits a bounded time; raises LockBusy (never proceeds unlocked, never removes a lock)."""
    deadline = time.monotonic() + lock_wait()
    host = socket.gethostname()
    while True:
        token = take(lock, host, stamp)
        if token:
            return token
        seen = stale_look(lock, host)
        if seen is not None:
            # THE SECOND LOOK (N2a). The pid read a moment ago is dead, or the lock is owner-less and old. That
            # alone is not "stale": the holder may have finished normally in between and the path may now be
            # another writer's live lock. So: try the mkdir again, and only if the SAME thing is still there
            # (same owner file with the same token, same directory, unchanged) is it reported.
            token = take(lock, host, stamp)
            if token:
                return token
            if stale_look(lock, host) == seen:
                o = dict(seen[1])
                if seen[0] == "dead":
                    what = ("is held by pid %s on %s since %s, and that process is no longer running (looked twice: the "
                            "same owner file was still there after the pid was found dead). A write died part-way"
                            % (o.get("pid"), o.get("host"), o.get("started")))
                else:
                    what = ("has no usable owner file and has not changed for over %d s (a write was killed just after "
                            "taking the lock or just before removing it; looked twice). A write died" % OWNERLESS_STALE_SECONDS)
                raise LockBusy("STALE LOCK — the write lock %s %s; the state file and the archive are each whole, because "
                               "both are replaced by rename. Nothing was written by this call. Recovery (a seat may run it "
                               "itself; no person is needed), once you have checked that no handover write is running "
                               "(pgrep -fl handover_core.py):\n  %s\nthen run the write again." % (lock, what, recovery_line(lock)))
        if time.monotonic() >= deadline:
            o = lock_owner(lock)
            who = (("pid %s on %s since %s" % (o.get("pid"), o.get("host"), o.get("started"))) if owner_pid(o) is not None
                   else "no usable owner file")
            raise LockBusy("LOCK BUSY — another handover write holds %s (%s) and did not finish within %.0f s "
                           "(HANDOVER_LOCK_WAIT). Nothing was written by this call; run it again. ONLY if no handover "
                           "write is running anywhere (pgrep -fl handover_core.py; a lock from another machine cannot be "
                           "judged from here) is the lock stale; recovery then:\n  %s" % (lock, who, lock_wait(), recovery_line(lock)))
        time.sleep(0.05)


def holds(lock, token):
    """Is the lock at this path still the one THIS call took? (the owner file carries this call's token)"""
    return bool(token) and lock_owner(lock).get("token") == token


def release_lock(lock, token):
    """Remove the lock THIS call took (its own owner file, then the directory). -> True when it was still this
    call's and is now gone; False when it was not (moved away, or another owner's: left exactly as it is)."""
    try:
        o = lock_owner(lock)
        if not token or o.get("token") != token:
            eprint("handover: WARNING — the lock at %s is not this process's any more (%s); left in place"
                   % (lock, ("owner pid %s" % o.get("pid")) if o else "no lock or no owner file there"))
            return False
        os.remove(os.path.join(lock, "owner"))
        os.rmdir(lock)
        return True
    except OSError as e:
        eprint("handover: WARNING — could not release the lock at %s: %s" % (lock, e))
        return False


def split_header(data):
    """-> (header_bytes, body_bytes, fields). header None when the file does not start with one."""
    if data is None:
        return None, b"", {}
    if not data.startswith(HEAD_OPEN):
        return None, data, {}
    end = data.find(HEAD_CLOSE, len(HEAD_OPEN) - 1)
    if end < 0:
        return None, data, {}
    cut = end + len(HEAD_CLOSE)
    fields = {}
    for line in data[len(HEAD_OPEN):end].decode("utf-8", "replace").split("\n"):
        if ":" in line:
            k, v = line.split(":", 1)
            fields[k.strip()] = v.strip()
    return data[:cut], data[cut:], fields


def part_of(line):
    """A heading line of ANY level, indented or not -> the PARTS name when it is exactly '## <PART>', else '?'.
    None for a line that is not a heading. (m5: a second block could hide under '# ', '### ' or an indented
    '## '; a zero-width space after a part name made a look-alike part.)"""
    if not HEADING.match(line):
        return None
    plain = line.rstrip(" \t")
    for p in PARTS:
        if plain == "## " + p:
            return p
    return "?"


def analyse(block):
    """-> (faults, sizes). faults: list of strings; sizes: bytes per part."""
    text = block.decode("utf-8", "replace")
    faults = []
    seen = {}
    sizes = {}
    body = {}
    cur = None
    for line in text.split("\n"):
        p = part_of(line)
        if p == "?":
            faults.append("a heading line that is not exactly one of the five parts: %r. Inside a block the only "
                          "headings are '## FLOOR', '## FIRST WORK', '## OWED', '## OPEN CARDS', '## GRANTS IN PLAY', "
                          "written exactly so, at the left margin. Any other heading (any level, indented or not) is "
                          "refused: write it as a bold line or a bullet. A second dated block is a stack; the previous "
                          "block is archived for you." % line.strip()[:80])
            cur = None
            continue
        if p:
            seen[p] = seen.get(p, 0) + 1
            cur = p
            sizes[p] = sizes.get(p, 0) + len(line.encode("utf-8")) + 1
            continue
        if cur:
            sizes[cur] = sizes.get(cur, 0) + len(line.encode("utf-8")) + 1
            if line.strip():
                body[cur] = True
    for p in PARTS:
        n = seen.get(p, 0)
        if n == 0:
            faults.append("part missing: '## %s' (%s)." % (p, PART_HINT[p]))
        elif n > 1:
            faults.append("part '## %s' appears %d times: one block has each part once. Two blocks in one write is a stack." % (p, n))
        elif not body.get(p):
            faults.append("part '## %s' has no text under it. Write 'none' if there is none." % p)
    return faults, sizes


def xclocks(block):
    return sorted(set(m.group(1) for m in XCLOCK.finditer(block.decode("utf-8", "replace"))))


def clock_fault(block, reason):
    """-> (fault or '', reason actually used or ''). The override is note_entry.sh's shape: an owned reason."""
    clocks = xclocks(block)
    if not clocks:
        return "", ""
    reason = " ".join((reason or "").split())
    if len(reason) >= XCLOCK_MIN_REASON:
        return "", reason
    if reason:
        return ("a clock with an x digit: %s. HANDOVER_ALLOW_XCLOCK is set but its reason is %d characters; it needs at least %d "
                "(say why the text is quoted, not composed)." % (", ".join(clocks), len(reason), XCLOCK_MIN_REASON)), ""
    return ("a clock with an x digit: %s. A time is pasted from the command that read it, or left out (the block is stamped "
            "for you). Quoting text that already carries one: HANDOVER_ALLOW_XCLOCK='<why, %d characters or more>' "
            "handover.sh write --stdin; the reason is recorded in the block's header and in its archive heading."
            % (", ".join(clocks), XCLOCK_MIN_REASON)), ""


def validate(block, cap, reason=""):
    """-> (faults, sizes, reason used for an x-clock override or '')."""
    if not block.strip():
        return ["the block is empty."], {}, ""
    faults, sizes = analyse(block)
    cf, used = clock_fault(block, reason)
    if cf:
        faults.append(cf)
    if len(block) > cap:
        order = sorted(sizes.items(), key=lambda kv: -kv[1])
        detail = ", ".join("%s %d B" % kv for kv in order) or "no part found"
        faults.insert(0, "the block is %d bytes; the cap is %d (HANDOVER_CAP_BYTES). Over by %d. Parts, largest first: %s. "
                         "Cut the largest part: history and reasoning belong in the daily note, a pointer here."
                      % (len(block), cap, len(block) - cap, detail))
    return faults, sizes, used


def state_header(seat, stamp, block, tool, archive_name, xclock_reason=""):
    lines = [
        "---",
        "type: seat-state",
        "seat: " + seat,
        "written: " + stamp,
        "block_bytes: %d" % len(block),
        "block_sha256: " + sha(block),
    ]
    if xclock_reason:
        lines.append("xclock_override: " + xclock_reason)
    lines += [
        "source: WRITTEN ONLY by %s write --stdin. ONE block. The previous block is in %s. Never hand-edit, never append."
        % (tool, archive_name),
        "---",
    ]
    return ("\n".join(lines) + "\n").encode("utf-8")


def archive_header(seat, tool):
    lines = [
        "---",
        "type: seat-state-archive",
        "seat: " + seat,
        "source: entries are added ONLY by %s, newest first, each the previous block verbatim. Nothing here is edited or deleted."
        % tool,
        "---",
        "",
    ]
    return ("\n".join(lines) + "\n").encode("utf-8")


def compose_archive(prev, old_body, old_fields, seat, stamp, tool):
    """-> (new_archive, prefix_len, entry_head, sep). new = prefix + entry_head + old_body + sep + rest."""
    if prev is None:
        prefix, rest = archive_header(seat, tool), b""
        prev_len = 0
    else:
        head, body, _ = split_header(prev)
        if head is None:
            prefix, rest = b"", prev
        else:
            # keep the one blank line after the header in the prefix when it is there
            extra = 1 if body.startswith(b"\n") else 0
            prefix, rest = head + body[:extra], body[extra:]
        prev_len = len(prev)
    over = old_fields.get("xclock_override", "")
    entry_head = ("# ARCHIVED %s | block written %s | %d bytes | sha256 %s%s\n\n"
                  % (stamp, old_fields.get("written", "unknown (the state file had no header)"),
                     len(old_body), sha(old_body)[:16],
                     (" | x-clock override: " + over) if over else "")).encode("utf-8")
    sep = b"\n" if old_body.endswith(b"\n") else b"\n\n"
    new = prefix + entry_head + old_body + sep + rest
    return new, len(prefix), entry_head, sep, prev_len


def assert_conserved(new_archive, prev, old_body, prefix_len, entry_head, sep):
    """Independent of compose_archive's arithmetic: returns a fault string, or '' when conserved."""
    off = prefix_len + len(entry_head)
    got = new_archive[off:off + len(old_body)]
    if got != old_body:
        return ("the previous block is not byte-identical in the new archive at offset %d (%d bytes in, %d bytes found equal-length slice differs)"
                % (off, len(old_body), len(got)))
    grown = len(entry_head) + len(old_body) + len(sep)
    if prev is not None:
        if len(new_archive) != len(prev) + grown:
            return ("archive growth is %d bytes, expected %d (heading %d + block %d + separator %d)"
                    % (len(new_archive) - len(prev), grown, len(entry_head), len(old_body), len(sep)))
        without = new_archive[:prefix_len] + new_archive[prefix_len + grown:]
        if without != prev:
            return "earlier archive bytes changed: removing the new entry does not give back the archive that was read"
    else:
        if len(new_archive) != prefix_len + grown:
            return "new archive size is %d bytes, expected %d" % (len(new_archive), prefix_len + grown)
    return ""


def write_tmp(tmp, data):
    with open(tmp, "wb") as f:
        f.write(data)
        f.flush()
        os.fsync(f.fileno())
    return tmp


def cmd_write(a, state_path, arch_path, block=None, reason=None, must_be_first=False):
    if block is None:
        block = sys.stdin.buffer.read()
    if reason is None:
        reason = os.environ.get("HANDOVER_ALLOW_XCLOCK", "")
    if block.strip() and not block.endswith(b"\n"):
        block += b"\n"
    faults, sizes, used = validate(block, a.cap, reason)
    if faults:
        eprint("handover: REFUSED — nothing written (%d fault%s):" % (len(faults), "" if len(faults) == 1 else "s"))
        for f in faults:
            eprint("  - " + f)
        return 3
    if a.dry:  # a dry run reads and prints; it takes no lock and writes nothing
        return write_locked(a, state_path, arch_path, block, sizes, used, must_be_first, None, None)
    lock = lock_dir(a.tasks_dir, a.seat)
    try:
        token = acquire_lock(lock, a.stamp)
    except LockBusy as e:
        eprint("handover: REFUSED — %s" % e)
        return 5
    except OSError as e:
        eprint("handover: REFUSED — cannot take the write lock at %s: %s. Nothing written." % (lock, e))
        return 4
    if not token:  # cannot happen through acquire_lock; stated so that "no lock, no write" does not rest on that
        eprint("handover: REFUSED (rc 5) — no write lock was taken for this call. Nothing written.")
        return 5
    a.said = []
    rc = 4
    try:
        rc = write_locked(a, state_path, arch_path, block, sizes, used, must_be_first, lock, token)
    finally:
        released = release_lock(lock, token)
    if rc == 0 and not released:
        # (c) both renames were made while the lock was this call's, but it is not this call's now: another
        # write may have run beside the end of this one. Never say "written" for that.
        eprint("handover: NOT ACKNOWLEDGED (rc 6) — the state file was replaced by this call, but the write lock was no "
               "longer this process's at release (it was moved away or retaken while this write ran), so another write "
               "may have overlapped it. Look: handover.sh show. If the block shown is not the one you just gave, write it again.")
        return 6
    if rc == 0:
        print("\n".join(a.said))
    return rc


def write_locked(a, state_path, arch_path, block, sizes, used, must_be_first, lock, token):
    """Everything from the first read to the second rename. Called with the lock held (or dry: lock None)."""
    cur = read_bytes(state_path)
    prev_arch = read_bytes(arch_path)
    if must_be_first and cur is not None:
        eprint("handover: REFUSED — a state file already exists at %s. seed writes only the FIRST block; "
               "replace an existing one with: handover.sh write --stdin" % state_path)
        return 3
    head, old_body, old_fields = split_header(cur)
    notes = []
    if cur is not None and head is None:
        notes.append("the state file had no tool header: its WHOLE content (%d bytes) is archived as the previous block" % len(old_body))
    elif cur is not None and old_fields.get("block_sha256") not in (None, sha(old_body)):
        notes.append("the state file was changed outside this tool since it was written: what is on disk (%d bytes) is archived verbatim" % len(old_body))
    arch_name = os.path.basename(arch_path)
    new_state = state_header(a.seat, a.stamp, block, a.tool, arch_name, used) + block
    new_arch = None
    if old_body:
        new_arch, prefix_len, entry_head, sep, _ = compose_archive(prev_arch, old_body, old_fields, a.seat, a.stamp, a.tool)
        if os.environ.get("HANDOVER_TEST_BREAK") == "archive-truncate":  # test seam (temp trees only): proves the assert below can fail
            new_arch = new_arch[:prefix_len + len(entry_head)] + old_body[:-2] + b"\n" + new_arch[prefix_len + len(entry_head) + len(old_body):]
        fault = assert_conserved(new_arch, prev_arch, old_body, prefix_len, entry_head, sep)
        if fault:
            eprint("handover: REFUSED — conservation failed, nothing written: " + fault)
            return 4
    plan = ["handover: seat %s" % a.seat,
            "  state:   %s  (%s -> %d bytes; block %d bytes, cap %d)"
            % (state_path, "absent" if cur is None else "%d" % len(cur), len(new_state), len(block), a.cap),
            "  parts:   " + ", ".join("%s %d B" % (p, sizes.get(p, 0)) for p in PARTS)]
    if new_arch is not None:
        plan.append("  archive: %s  (%s -> %d bytes; previous block %d bytes moved to the top)"
                    % (arch_path, "absent" if prev_arch is None else "%d" % len(prev_arch), len(new_arch), len(old_body)))
    else:
        plan.append("  archive: untouched (no previous block)")
    if used:
        plan.append("  x-clock override recorded in the header (and later in this block's archive heading): " + used)
    for n in notes:
        plan.append("  NOTE: " + n)
    if a.dry:
        print("\n".join(plan))
        print("handover: DRY — nothing written")
        return 0
    # THE TEMP FILES LIVE INSIDE THE LOCK DIRECTORY (N2b), under this call's token. If the lock directory is moved
    # away while this writer is alive (the recovery line run by mistake), the temp files go with it and the
    # rename below fails in the kernel: a displaced writer cannot rename anything into place.
    tmps = []          # (temp path inside the lock, where it is moved for inspection after a fault)
    renamed = []

    def guarded_replace(tmp, dest, what):
        if not holds(lock, token):
            raise LockLost("before the %s rename the lock was no longer this process's" % what, list(renamed))
        try:
            os.replace(tmp, dest)
        except FileNotFoundError:
            if holds(lock, token):
                raise
            raise LockLost("the %s rename found the lock directory gone" % what, list(renamed))
        renamed.append(what)

    def set_aside():
        """Move this call's temp files out of the lock directory (to STATE-*.md.tmp.<pid> beside the state file), so
        the lock can be released, and so nothing of this call's is left inside a directory another writer may now own.
        -> where they are now. When the lock directory was moved away they went with it and there is nothing to move."""
        left = []
        for t, aside in tmps:
            if os.path.exists(t):
                try:
                    os.replace(t, aside)
                    left.append(aside)
                except OSError:
                    left.append(t)
        return left

    try:
        if new_arch is not None:
            t = os.path.join(lock, "archive.tmp." + token)
            tmps.append((t, "%s.tmp.%d" % (arch_path, os.getpid())))
            write_tmp(t, new_arch)
            if read_bytes(t) != new_arch:
                raise IOError("archive temp file %s does not read back as written" % t)
        t2 = os.path.join(lock, "state.tmp." + token)
        tmps.append((t2, "%s.tmp.%d" % (state_path, os.getpid())))
        write_tmp(t2, new_state)
        if read_bytes(t2) != new_state:
            raise IOError("state temp file %s does not read back as written" % t2)
        if read_bytes(state_path) != cur or read_bytes(arch_path) != prev_arch:
            raise IOError("the state or archive file changed on disk while this write was being prepared "
                          "(an edit made outside this tool; the lock keeps other handover writes out)")
        # ARCHIVE FIRST, STATE SECOND: a death between the two leaves the old block in BOTH files, never in neither.
        if new_arch is not None:
            guarded_replace(tmps[0][0], arch_path, "archive")
        guarded_replace(t2, state_path, "state")
    except LockLost as e:
        if e.renamed:
            done = ("The ARCHIVE had already been replaced (it now also holds the block that is still the state block: "
                    "one duplicate archive entry after the next write, never a gap); the STATE file was NOT replaced")
        else:
            done = "NOTHING was renamed: the state file and the archive are exactly as they were"
        eprint("handover: REFUSED (rc 5) — LOCK LOST: %s (it was moved away or retaken while this write ran: the recovery "
               "line was run while this writer was alive). %s. This block is NOT written; run the write again." % (e, done))
        left = set_aside()
        if left:
            eprint("  this call's temp file(s) were moved out of the lock directory, for inspection (never deleted by this tool): " + ", ".join(left))
        return 5
    except (IOError, OSError, ReadFault) as e:
        left = set_aside()
        eprint("handover: REFUSED — I/O fault, the state file was not replaced: %s" % e)
        if left:
            eprint("  temp file(s) left for inspection (never deleted by this tool): " + ", ".join(left))
        return 4
    a.said = plan + ["handover: written %s" % a.stamp]
    return 0


def seed_part(label):
    """Which of the five parts a legacy bullet's leading bold label belongs to; None = unmapped."""
    u = label.upper()
    if u.startswith("FLOOR"):
        return "FLOOR"
    if "OWED" in u:
        return "OWED"
    if u.startswith("FIRST WORK") or u.startswith("NEXT"):
        return "FIRST WORK"
    if u.startswith("CARD") or u.startswith("OPEN CARD") or "FOR KAM" in u:
        return "OPEN CARDS"
    if "GRANT" in u:
        return "GRANTS IN PLAY"
    return None


def heading_text(line):
    return line[3:].strip().lstrip("\U0001F534\U0001F7E1\U0001F7E2⚠️*_ ").strip()


def seed_block(legacy_text, legacy_name):
    """-> (block bytes or None, report lines, carried sections). Built from the legacy pickup's newest '## '
    block PLUS every standing section of the file whose heading starts with OWED or STANDING (M5: those were
    left behind in silence). Nothing taken is reworded; every line taken is named by line number in the report."""
    lines = legacy_text.split("\n")
    idx = [i for i, l in enumerate(lines) if l.startswith("## ")]
    if not idx:
        return None, ["no '## ' block found in %s" % legacy_name], []
    end = idx[1] if len(idx) > 1 else len(lines)
    body = lines[idx[0] + 1:end]
    while body and not body[-1].strip():
        body.pop()
    parts = dict((p, []) for p in PARTS)
    took = dict((p, []) for p in PARTS)
    parts["FLOOR"].append("- Seeded from the newest block of the legacy pickup `%s` (lines %d to %d of %d): %s"
                          % (legacy_name, idx[0] + 1, idx[0] + 1 + len(body), len(lines), lines[idx[0]][3:].strip()))
    cur, mapped, unmapped = "FLOOR", 0, 0
    for n, l in enumerate(body, idx[0] + 2):
        m = re.match(r"- \*\*(.+?)\*\*", l)
        if m:
            tgt = seed_part(m.group(1))
            if tgt is None:
                tgt = "FIRST WORK"
                unmapped += 1
            else:
                mapped += 1
            cur = tgt
        elif l.startswith("- "):
            cur = "FIRST WORK"
            unmapped += 1
        parts[cur].append(l)
        if l.strip():
            took[cur].append(n)
    carried, mentioned = [], []
    for k in range(1, len(idx)):
        h = heading_text(lines[idx[k]])
        stop = idx[k + 1] if k + 1 < len(idx) else len(lines)
        sect = lines[idx[k] + 1:stop]
        while sect and not sect[-1].strip():
            sect.pop()
        kind = "OWED" if h.upper().startswith("OWED") else ("STANDING" if h.upper().startswith("STANDING") else None)
        if kind is None:
            if re.search(r"\b(OWED|STANDING)\b", h):
                mentioned.append((idx[k] + 1, h))
            continue
        size = sum(len(x.encode("utf-8")) + 1 for x in sect)
        first, last = idx[k] + 1, idx[k] + 1 + len(sect)
        carried.append((kind, h, first, last, size, sum(1 for x in sect if x.strip())))
        tgt = "OWED" if kind == "OWED" else "FIRST WORK"
        if parts[tgt] and parts[tgt][-1].strip():
            parts[tgt].append("")
        parts[tgt].append("- **%s, carried from the legacy file's standing section (`%s` line %d, heading: %s):**"
                          % (kind, legacy_name, first, h))
        parts[tgt].extend(sect)
    out, empty = [], []
    for p in PARTS:
        while parts[p] and not parts[p][-1].strip():
            parts[p].pop()
        if not any(x.strip() for x in parts[p]):
            parts[p] = ["- none stated in the legacy block"]
            empty.append(p)
        out.append("## %s\n%s\n" % (p, "\n".join(parts[p])))

    def span(ns):
        return ("lines " + ", ".join(str(x) for x in ns)) if ns else "nothing"

    report = ["taken from `%s` (%d lines in the file), by line number:" % (legacy_name, len(lines)),
              "  newest block: heading line %d, body lines %d to %d (%d bullets mapped by their label, %d unknown or plain bullets placed under FIRST WORK)"
              % (idx[0] + 1, idx[0] + 2, idx[0] + 1 + len(body), mapped, unmapped)]
    for p in PARTS:
        report.append("    -> %s: %s" % (p, span(took[p])))
    for kind, h, first, last, size, nonblank in carried:
        report.append("  standing section at line %d (`## %s`): lines %d to %d, %d non-blank lines, %d bytes -> %s"
                      % (first, h, first + 1, last, nonblank, size, "OWED" if kind == "OWED" else "FIRST WORK (as a named STANDING line)"))
    if not carried:
        report.append("  standing sections (a '## ' heading starting OWED or STANDING outside the newest block): none in the file")
    for ln, h in mentioned:
        report.append("  NOT carried: line %d, `## %s` mentions OWED or STANDING but is a dated block, not a standing section; read it yourself"
                      % (ln, h))
    report.append("  every other '## ' block of the file (%d) is history and is NOT carried" % (len(idx) - 1 - len(carried)))
    if empty:
        report.append("  parts with nothing to carry (written as 'none stated'): " + ", ".join(empty))
    return "\n".join(out).encode("utf-8"), report, carried


def cmd_seed(a, state_path, arch_path):
    name = LEGACY_PICKUP.get(a.seat)
    if not name:
        eprint("handover: REFUSED — no legacy pickup is known for seat %r" % a.seat)
        return 2
    legacy = os.path.join(a.tasks_dir, name)
    if os.path.lexists(state_path):
        eprint("handover: REFUSED — a state file already exists at %s. seed writes only the FIRST block; "
               "replace an existing one with: handover.sh write --stdin" % state_path)
        return 3
    data = read_bytes(legacy)
    if data is None:
        eprint("handover: REFUSED — no legacy pickup at %s to seed from" % legacy)
        return 3
    block, report, carried = seed_block(data.decode("utf-8", "replace"), name)
    if block is None:
        eprint("handover: REFUSED — " + report[0])
        return 3
    reason = SEED_REASON if xclocks(block) else ""
    faults, _, used = validate(block, a.cap, reason)

    def by_hand():
        eprint("  The standing sections the seed tried to carry (place them by hand if the block must shrink):")
        for kind, h, first, last, size, nonblank in carried:
            eprint("    - `## %s`: %s lines %d to %d (%d non-blank lines, %d bytes)" % (h, name, first + 1, last, nonblank, size))
        if not carried:
            eprint("    - none")
        eprint("  Print the block (seed without --run), edit it, and write it yourself: handover.sh write --stdin")

    if not a.run:
        sys.stdout.buffer.write(block)
        eprint("handover: seed, DRY — nothing written. The block above (%d bytes) is what `handover.sh seed --from-legacy --run` would write to %s."
               % (len(block), state_path))
        for n in report:
            eprint("  " + n)
        if used:
            eprint("  the legacy text carries x-digit clocks (%s): --run records the reason %r" % (", ".join(xclocks(block)), used))
        if faults:
            eprint("  --run WOULD BE REFUSED (%d fault%s):" % (len(faults), "" if len(faults) == 1 else "s"))
            for f in faults:
                eprint("    - " + f)
            by_hand()
        eprint("  The legacy file is read, never written.")
        return 0
    if faults:
        eprint("handover: seed REFUSED — the seeded block is not a valid block, nothing written (%d fault%s):"
               % (len(faults), "" if len(faults) == 1 else "s"))
        for f in faults:
            eprint("  - " + f)
        by_hand()
        return 3
    for n in report:
        print("handover: seed: " + n)
    return cmd_write(a, state_path, arch_path, block=block, reason=reason, must_be_first=True)


def cmd_show(state_path):
    cur = read_bytes(state_path)
    if cur is None:
        eprint("handover: no state file at %s" % state_path)
        return 1
    _, body, _ = split_header(cur)
    sys.stdout.buffer.write(body)
    return 0


def check_faults(cur, seat, cap):
    """What `handover.sh check` refuses in a state file's bytes. -> (faults, body, fields). The wake pack's state
    part calls this same function (N6), so the pack cannot carry a state file that `check` would refuse."""
    head, body, fields = split_header(cur)
    faults = []
    if head is None:
        faults.append("no tool header: the file was not written by handover.sh")
    else:
        if fields.get("block_sha256") != sha(body):
            faults.append("the block does not match the header's sha256: it was edited or appended to outside the tool")
        if fields.get("block_bytes") != str(len(body)):
            faults.append("the block is %d bytes, the header says %s" % (len(body), fields.get("block_bytes")))
        if fields.get("seat") != seat:
            faults.append("the header names seat %r, this tree is %r" % (fields.get("seat"), seat))
    f2, _, _ = validate(body, cap, fields.get("xclock_override", "") if head is not None else "")
    faults.extend(f2)
    return faults, body, fields


def cmd_check(a, state_path):
    cur = read_bytes(state_path)
    if cur is None:
        print("handover: ABSENT — no state file at %s (not a fault before the cut-over)" % state_path)
        return 0
    faults, body, fields = check_faults(cur, a.seat, a.cap)
    if faults:
        for f in faults:
            print("FAULT: " + f)
        print("handover: NOT one clean block — rewrite it through handover.sh write --stdin (%s)" % state_path)
        return 1
    print("handover: OK — one block, %d bytes of %d, written %s" % (len(body), a.cap, fields.get("written", "?")))
    return 0


def main():
    ap = argparse.ArgumentParser(description="engine behind handover.sh")
    ap.add_argument("cmd", choices=["write", "show", "where", "check", "seed"])
    ap.add_argument("--seat", required=True)
    ap.add_argument("--tasks-dir", required=True)
    ap.add_argument("--stamp", default="")
    ap.add_argument("--cap", type=int, default=10000)
    ap.add_argument("--tool", default="2_Project_Files/wake/handover.sh")
    ap.add_argument("--dry", action="store_true")
    ap.add_argument("--run", action="store_true")
    a = ap.parse_args()
    state_path = os.path.join(a.tasks_dir, "STATE-%s.md" % a.seat)
    arch_path = os.path.join(a.tasks_dir, "STATE-%s-archive.md" % a.seat)
    tree = os.path.dirname(os.path.dirname(os.path.abspath(a.tasks_dir)))
    if os.path.basename(tree).lower() != a.seat or os.path.basename(os.path.dirname(os.path.abspath(a.tasks_dir))) != "0_Brain":
        eprint("handover: REFUSED — the engine was given seat %r for the tree %s; the seat is the tree's own "
               "(call handover.sh, which resolves it)" % (a.seat, tree))
        return 2
    if os.environ.get("HANDOVER_TEST_BREAK") and not under_temp(a.tasks_dir):
        eprint("handover: REFUSED — HANDOVER_TEST_BREAK is a test seam and is honoured only for a tree under a "
               "system temp or scratch directory (%s); this tree is %s. Unset it." % (", ".join(TEMP_ROOTS), tree))
        return 2
    if a.cmd == "where":
        print("seat:    " + a.seat)
        print("state:   " + state_path + ("" if os.path.exists(state_path) else "  (absent)"))
        print("archive: " + arch_path + ("" if os.path.exists(arch_path) else "  (absent)"))
        print("lock:    " + lock_dir(a.tasks_dir, a.seat) + ("  (HELD: %r)" % lock_owner(lock_dir(a.tasks_dir, a.seat)) if os.path.isdir(lock_dir(a.tasks_dir, a.seat)) else ""))
        print("cap:     %d bytes (HANDOVER_CAP_BYTES)" % a.cap)
        print("parts:   " + ", ".join("## " + p for p in PARTS))
        return 0
    if not os.path.isdir(a.tasks_dir):
        eprint("handover: REFUSED — no tasks directory at %s" % a.tasks_dir)
        return 2
    if a.cmd == "show":
        return cmd_show(state_path)
    if a.cmd == "check":
        return cmd_check(a, state_path)
    if a.cmd == "seed" and not a.run:
        return cmd_seed(a, state_path, arch_path)
    if not a.stamp:
        eprint("handover: REFUSED — no stamp given (handover.sh reads the clock; do not call the engine directly)")
        return 2
    if a.cmd == "seed":
        return cmd_seed(a, state_path, arch_path)
    return cmd_write(a, state_path, arch_path)


if __name__ == "__main__":
    try:
        sys.exit(main())
    except ReadFault as e:
        eprint("handover: REFUSED — %s. Nothing written." % e)
        sys.exit(4)
