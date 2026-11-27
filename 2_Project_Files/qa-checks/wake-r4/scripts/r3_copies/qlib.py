# qlib.py — shared helpers for the round-3 re-check. Everything is built under the scratch base (a system temp path).
import glob, hashlib, os, shutil, subprocess, sys
sys.dont_write_bytecode = True
R = "/Volumes/DevMASTER/WEDNESDAY"
LANE = R + "/2_Project_Files/wake"
REAL = R + "/2_Project_Files"
BASE = "/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/435f0b28-fa4c-43b1-8811-a27f707f05c7/scratchpad/qa-wake-r4/r3"  # ADAPTED by the round-4 checker: scratch path only
PACK_SRC = ["CLAUDE.md", "0_Brain/CLAUDE.md", "0_Brain/identity/persona.md", "0_Brain/identity/voice-protocol.md", "0_Brain/people/kam.md",
            "0_Brain/learnings/_rules_card_wednesday.md", "0_Brain/learnings/_ledger.md", "0_Brain/tasks/EXPIRING-GRANTS.md",
            "0_Brain/tasks/NEXT-PICKUP.md", "0_Brain/tasks/TASKS.md", "0_Brain/tasks/WEEK-INSTRUCTION.md", "0_Brain/projects_index/INDEX.md",
            "2_Project_Files/tools/rules_card.py", "2_Project_Files/tools/kam_msgs.sh", "2_Project_Files/tools/kam_rulings_today.sh",
            "1_Project_Definition/Architecture/2026-11-27_fleet-structure-v2-design.md"]


def ENV(extra=None, keep_wait=False):
    e = dict(os.environ)
    for k in ("WED_AGENT", "HANDOVER_TREE", "HANDOVER_CAP_BYTES", "HANDOVER_TEST_BREAK", "HANDOVER_TEST_STAMP", "HANDOVER_ALLOW_XCLOCK",
              "HANDOVER_LOCK_WAIT", "WED_SEAT"):
        e.pop(k, None)
    e["PYTHONDONTWRITEBYTECODE"] = "1"
    e.update(extra or {})
    return e


def mk(name, sub="", folder="WEDNESDAY", tools_from=LANE):
    """A scratch tree with a COPY of the handover tools and the two seat libraries (the tree's own folder name is the seat)."""
    root = os.path.join(BASE, sub, name, folder) if sub else os.path.join(BASE, name, folder)
    for rel in ("tools/seat_note.sh", "fleet/cockpit/seat_resolve.sh"):
        d = os.path.join(root, "2_Project_Files", rel)
        os.makedirs(os.path.dirname(d), exist_ok=True)
        shutil.copy(os.path.join(REAL, rel), d)
    os.makedirs(os.path.join(root, "2_Project_Files", "wake"), exist_ok=True)
    for f in ("handover.sh", "handover_core.py", "wake_pack.py", "wake_census.sh"):
        shutil.copy(os.path.join(tools_from, f), os.path.join(root, "2_Project_Files", "wake", f))
    os.makedirs(os.path.join(root, "0_Brain", "tasks"), exist_ok=True)
    return root


def mk_real(name, sub=""):
    """mk() plus COPIES of the Wednesday seat's real pack sources (read from the real tree, written only to scratch)."""
    root = mk(name, sub)
    for rel in PACK_SRC:
        d = os.path.join(root, rel)
        os.makedirs(os.path.dirname(d), exist_ok=True)
        if os.path.exists(os.path.join(R, rel)):
            shutil.copy(os.path.join(R, rel), d)
    fd = os.path.join(root, "0_Brain/learnings/families")
    os.makedirs(fd, exist_ok=True)
    for p in glob.glob(os.path.join(R, "0_Brain/learnings/families/*.md")):
        shutil.copy(p, fd)
    return root


def ho(root, *args, data=b"", env=None):
    p = subprocess.run(["/bin/bash", os.path.join(root, "2_Project_Files", "wake", "handover.sh")] + list(args), input=data,
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=ENV(env))
    return p.returncode, p.stdout.decode("utf-8", "replace"), p.stderr.decode("utf-8", "replace")


def wp(root, *args, seat="wednesday", env=None):
    p = subprocess.run([sys.executable, os.path.join(root, "2_Project_Files/wake/wake_pack.py"), "--seat", seat, "--root", root] + list(args),
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=ENV(env))
    return p.returncode, p.stdout.decode("utf-8", "replace"), p.stderr.decode("utf-8", "replace")


def blk(tag, pad=0):
    if isinstance(tag, str):
        tag = tag.encode()
    b = b"\n".join([b"## FLOOR", b"floor " + tag, b"## FIRST WORK", b"first " + tag, b"## OWED", b"owed " + tag, b"## OPEN CARDS",
                    b"cards " + tag, b"## GRANTS IN PLAY", b"grants " + tag])
    return b + b"y" * pad + b"\n"


def rd(p):
    return open(p, "rb").read() if os.path.exists(p) else None


def T(root):
    return os.path.join(root, "0_Brain", "tasks")


def st(root, seat="wednesday"):
    return os.path.join(T(root), "STATE-%s.md" % seat)


def ar(root, seat="wednesday"):
    return os.path.join(T(root), "STATE-%s-archive.md" % seat)


def lockd(root, seat="wednesday"):
    return os.path.join(T(root), "STATE-%s.lock.d" % seat)


def body(root, seat="wednesday"):
    d = rd(st(root, seat))
    if d is None:
        return None
    i = d.find(b"\n---\n", 3)
    return d[i + 5:]


def sha(b):
    return hashlib.sha256(b).hexdigest()[:16] if b is not None else "NONE"
