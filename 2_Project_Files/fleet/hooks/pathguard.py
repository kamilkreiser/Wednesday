#!/usr/bin/env python3
"""pathguard.py — the FILE-write half of the two-agent boundary (Phase 2).

WHY THIS IS A SEPARATE FILE. Its sibling `pretooluse_no_cd.sh` carries its logic in a
single-quoted shell string, so an apostrophe anywhere in it ends the string and BRICKS the
hook — which blocks every Bash call in the session, including the one that would repair it.
That happened twice in two days (2026-09-07, and again 2026-09-08 while writing a comment
about it). Code that has to be edited under pressure does not belong in that string.

WHAT IT ENFORCES (Kam's 2026-09-08 11:50 commission: "there's got to be a strong gate
between agents acting between the two"). The git-verb half already refuses `git -C <outside>
<write>`. This is the rest: a shell command that WRITES to a path belonging to another
client or to the sister agent's tree.

FORBIDDEN, for either agent, minus its own root:
    /Volumes/*/!CODING/**          every client project — hard rule 1, read-only for a
                                   coordinator; "manage, don't do"
    /Volumes/*/WEDNESDAY/**        the sister tree, when this seat is Tuesday
    /Volumes/*/TUESDAY/**          the sister tree, when this seat is Wednesday
    /Volumes/*/Notes (MASTER)/**   the shared vault; write-allowed folders are the named
                                   exception and are handled by asking, not by this gate

HONEST LIMITS, stated rather than discovered later:
  * A gate on writes says nothing about READS. Nothing here stops a `cat`. On the travel
    drive both clients are mounted for both agents and the physical separation disappears,
    so that is the mode where discipline is ALL there is — the strongest mode is two
    machines, and this gate is what remains when there is one.
  * It matches COMMANDS at command positions, not intent. A write through a wrapper script
    it does not know is not caught.
  * It fails CLOSED on unresolved $VAR paths only when they literally name a forbidden
    root; a bare variable is invisible here, exactly as it is to the git clause.

DELIBERATE OVERRIDE: WED_ALLOW_CROSS_TREE=1 passes everything. It exists because
provisioning the sister tree IS a legitimate coordinator task — Kam asked for exactly that
on 2026-09-08 ("copy across and sync to that drive") — and a gate that blocks a standing
task is a gate that gets switched off permanently instead of once. Every use of it belongs
in the session note, named.

Usage:  <command on stdin>; prints "cmd|path" and exits 0 on a hit, prints nothing otherwise.
"""
import os
import re
import sys

# Commands that write. `sed` only counts with -i; `git` is the sibling clause's job.
WRITE_CMDS = (
    "rm", "mv", "cp", "tee", "mkdir", "rmdir", "touch", "chmod", "chown", "chgrp",
    "ln", "truncate", "dd", "rsync", "install", "unlink", "shred", "gzip", "gunzip",
    "tar", "unzip", "zip", "patch",
)

FORBIDDEN = re.compile(
    r"^/Volumes/[^/]+/(?:!CODING|WEDNESDAY|TUESDAY|Notes \(MASTER\))(?:/|$)")


def strip_heredocs(text):
    """Prose about a command is not a command. Every heredoc line starts at a newline,
    which is a command position, so anchoring alone cannot tell them apart — the sibling
    hook learned this from three false positives."""
    out, i = [], 0
    lines = text.split("\n")
    while i < len(lines):
        line = lines[i]
        out.append(line)
        m = re.search(r"<<-?\s*(['\"]?)([A-Za-z_][A-Za-z0-9_]*)\1", line)
        i += 1
        if not m:
            continue
        delim = m.group(2)
        while i < len(lines) and lines[i].strip() != delim:
            i += 1
        if i < len(lines):
            out.append(lines[i])
            i += 1
    return "\n".join(out)


def quoted_mask(text):
    """Positions that sit INSIDE a quoted string.

    Added before arming, because the first live run refused this file's own test harness:
    a `for c in "echo hi > /Volumes/.../x"` list has a redirect at what looks like a
    command position, and briefs, notes and test matrices are full of example commands.
    A gate with false positives gets routed around — this hook family has learned that
    three times already, so the narrowing ships WITH the clause and not after it.

    A COMMAND is only a command when its own name (or the `>`) is outside quotes; a
    quoted PATH argument is normal and still matches, because the match anchors on the
    command, not on the argument."""
    mask = bytearray(len(text))
    q = None
    esc = False
    for i, ch in enumerate(text):
        if esc:
            esc = False
            if q:
                mask[i] = 1
            continue
        if ch == "\\":
            esc = True
            if q:
                mask[i] = 1
            continue
        if q:
            mask[i] = 1
            if ch == q:
                q = None
            continue
        if ch in "'\"":
            q = ch
    return mask


def unquote(tok):
    if len(tok) >= 2 and tok[0] == tok[-1] and tok[0] in "'\"":
        return tok[1:-1]
    return tok


def forbidden(path, own):
    """A path is forbidden when it is inside one of the protected families and NOT inside
    this seat's own root. The own-root test comes second on purpose: Wednesday's own tree
    IS /Volumes/<drive>/WEDNESDAY, so the family test alone would refuse every write she
    makes to herself."""
    if not path.startswith("/Volumes/"):
        return False
    if own and (path == own or path.startswith(own.rstrip("/") + "/")):
        return False
    return bool(FORBIDDEN.match(path))


CMD_POS = r"(?:^|[;&|(`\n]|\$\(|\bthen\s|\bdo\s|&&|\|\|)\s*"
TOKEN = r"""(?:"[^"]*"|'[^']*'|[^\s;&|<>()]+)"""


def main():
    if os.environ.get("WED_ALLOW_CROSS_TREE") == "1":
        return
    own = os.environ.get("HOOK_OWN_ROOT") or "/Volumes/DevMASTER/WEDNESDAY"
    cmd = strip_heredocs(sys.stdin.read())
    inq = quoted_mask(cmd)

    # (a) a write COMMAND whose arguments include a forbidden path
    for m in re.finditer(CMD_POS + r"(?P<cmd>[a-z][a-z0-9_-]*)(?P<args>(?:\s+" + TOKEN + r")*)",
                         cmd, re.M):
        if inq[m.start("cmd")]:
            continue                      # a command name inside quotes is a quotation
        name = m.group("cmd")
        if name not in WRITE_CMDS:
            continue
        args = m.group("args") or ""
        if name == "sed" and " -i" not in args:
            continue
        for tok in re.findall(TOKEN, args):
            p = unquote(tok)
            if forbidden(p, own):
                print("%s|%s" % (name, p))
                return

    # (b) output redirection into a forbidden path — `> f`, `>> f`, `2> f`
    for m in re.finditer(r"\d?>>?\s*(?P<path>" + TOKEN + r")", cmd):
        if inq[m.start()]:
            continue                      # a redirect inside quotes is a quotation
        p = unquote(m.group("path"))
        if forbidden(p, own):
            print("redirect|%s" % p)
            return


if __name__ == "__main__":
    main()
