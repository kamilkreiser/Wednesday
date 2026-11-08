#!/usr/bin/env python3
# LINEAGE (Seat X 7th, 2026-11-06): re-keyed from Seat V 24th's launch_driver_v24.py (sha256 b4f4c3cd...) by tools/rekey_push_x7.py: RECORD and CELLSFILE arguments, X7_ knobs scrubbed from the driver's env, TMPDIR /private/tmp/prt. Gate logic unchanged.
# LINEAGE (Seat V 24th, 2026-11-06): re-keyed from Seat V 23rd's launch_driver_v23.py by COUNT-ASSERTED token pairs (tools/rekey_push_v24.py); gate logic unchanged; two path-value deviations declared in evidence/declared_changes_push.md.
# LINEAGE (Seat V 24th, 2026-11-06 ~13:55 AEDT): TMPDIR changed from <record folder>/evidence/tmp_v24 to /private/tmp/v24t (count-asserted: 1). The long path made tsx's IPC socket path 121 bytes, over macOS's 104-byte sun_path limit, so leg 1 of the real pre-push hook failed (the KS-1509 push, 02:53Z, rehearsal skips the hook so could not see it). The family's own short convention is restored.
# LINEAGE (Seat V 23rd, 2026-11-05): re-keyed from Seat V 22nd's launch_driver_v22.py by COUNT-ASSERTED token pairs (tools/rekey_push_v23.py). Logic unchanged.
# LINEAGE (Seat V 22nd, 2026-11-05): re-keyed from Seat V 21st's launch_driver_v21.py by COUNT-ASSERTED token pairs (tools/rekey_push_v22.py). Logic unchanged.
# LINEAGE (Seat V 21st, 2026-11-05): re-keyed from Seat V 20th's launch_driver_v20.py by COUNT-ASSERTED token pairs (tools/rekey_newbranch_v21.py). Logic unchanged.
# LINEAGE (Seat V 20th, 2026-11-05): derived from Seat F 31st's launch_driver_f31.py by tools/rekey_push_w28.py (explicit counted pairs; no logic line changed; see evidence/declared_changes.md).
# LINEAGE (Seat F 31st, 2026-11-05): re-keyed copy of Seat F 29th's launch_driver_f29.py by named replacements (counts: {'Seat F 29th': 1, 'launch_driver_f29': 1, '2026-11-04_seatF-29th': 1, 'pushlock_f29_': 1, 'F29_': 3, '/private/tmp/f29t': 1}); logic unchanged.
# LINEAGE (Seat F 29th, 2026-11-04): re-keyed from Seat R 81st's launch_driver_r81.py by NAMED edits (each replacement count-checked, listed in evidence/rekey_push.out); logic unchanged.
# LINEAGE (Seat R 81st, 2026-11-04): re-keyed from Seat R 80th's launch_driver_r80.py by NAMED edits read one by one (tools/rekey_named_r81.py, diff in evidence/rekey/launch_driver.diff): the docstring seat name and usage name; DRIVER now points at my pushlock_r81_newbranch_v3.sh; the env names R80_NETMAX / R80_ADOPT_PREFIX -> R81_ and TMPDIR /private/tmp/r81t. Logic unchanged.
# LINEAGE (Seat R 80th, 2026-11-03): re-keyed from Seat R 79th's launch_driver_r79.py by NAMED edits read one by one (tools/rekey_named_r80.py, diff in evidence/rekey/launch_driver.diff): the docstring seat name and usage name; DRIVER now points at my pushlock_r80_newbranch_v3.sh; the env names R80_NETMAX / R80_ADOPT_PREFIX and TMPDIR /private/tmp/r80t (short, per STANDING_LINES 532). Logic unchanged.
# LINEAGE (Seat R 79th, 2026-11-03): copy of Seat R 78th's launch_driver_r78.py with the r78 tokens on matching lines changed to r79 by rekey_r79.py (a named-file pass, the diff read line by line, no logic line changed). Earlier seats' LINEAGE lines are left exactly as they were written.
# LINEAGE (Seat R 78th, 2026-11-03): copy of Seat R 77th's launch_driver_r77.py with the r77 tokens on matching lines changed to r78 by rekey_r78.py (a named-file pass, the diff read line by line, no logic line changed). Earlier seats' LINEAGE lines are left exactly as they were written.
# LINEAGE (Seat R 77th, 2026-11-03): copy of Seat R 76th's launch_driver_r76.py with the r76 tokens on matching lines changed to r77 by rekey_r77.py (a named-file pass, the diff read line by line, no logic line changed). Earlier seats' LINEAGE lines are left exactly as they were written.
# LINEAGE (Seat R 76th, 2026-11-03): copy of Seat R 75th's launch_driver_r75.py (itself re-keyed from Seat W 17th's) with the r75 tokens on matching lines changed to r76 by rekey_r76.py (a named-file pass, the diff read line by line, no logic line changed). Older LINEAGE lines below were written by earlier seats and carry the new seat token only because of this pass.
# LINEAGE (Seat R 76th, 2026-11-03): re-keyed copy of Seat W 17th's launch_driver_w17.py by READING it: only the seat token, the env-var prefix W17_ -> R76_, tool names, paths and the planted-control path changed; every gate is unchanged. Remaining mentions of W 17th are historical comments, listed in evidence/rekey_batch3.out.
"""LINEAGE (Seat V 20th, 2026-11-05): copy of Seat W 28th's launch_driver_w28.py with counted named replacements ({'Seat W 28th': 2, '2026-11-05_seatW-28th': 1, 'pushlock_w28_newbranch_v3.sh': 1, 'W28_': 3, 'w28t': 1}); no logic line changed.
Seat X 8th: launch ONE v3 push driver DETACHED (own session, ppid 1, stdin /dev/null) so a harness task limit cannot take its queue place.
usage: launch_driver_x8.py SEATNAME WORKTREE BRANCH HEAD BASE OUTDIR PATHSFILE RECORD CELLSFILE [ADOPT_PREFIX]
ADOPT_PREFIX (<epoch>.<nanos>, the join-time part of an existing ticket of mine): the successor does not join; the caller re-keys its own ticket to <prefix>-<successor pid>.
Refuses if the worktree head differs from HEAD, if OUTDIR already holds a driver.pid (never two drivers for one PR), or if PATHSFILE is empty. The shared lock, queue, queue tool and key are fixed below."""
import os, re, subprocess, sys
if len(sys.argv) < 10: print("usage: launch_driver_x8.py SEATNAME WORKTREE BRANCH HEAD BASE OUTDIR PATHSFILE RECORD CELLSFILE [ADOPT_PREFIX]"); sys.exit(2)   # X7: 6 -> 9 required
SEAT, WT, BR, HEAD, BASE, OUT, PATHS, RECORD, CELLS = sys.argv[1:10]
ADOPT = sys.argv[10] if len(sys.argv) > 10 else ""
if not re.fullmatch(r"Seat [A-Z]+ \d+(st|nd|rd|th)", SEAT): print(f"STOP: SEATNAME must read like Seat X 8th, got [{SEAT}]"); sys.exit(2)
P = "/Volumes/DevMASTER/!CODING/Secuura/Blockchain"
DRIVER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "pushlock_x8_newbranch_v3.sh")
LOCK, QUEUE = f"{P}/worktrees/.push-lock", f"{P}/worktrees/.push-queue"
QTOOL, KEY = "/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/push_queue.sh", f"{P}/3_Access_Keys/github_deploy_rw"
head = subprocess.run(["git", "-C", WT, "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
if head != HEAD: print(f"STOP: worktree head {head[:12]} != {HEAD[:12]}"); sys.exit(2)
if os.path.exists(os.path.join(OUT, "driver.pid")): print("STOP: driver.pid already exists in", OUT); sys.exit(2)
if not os.path.exists(PATHS) or os.path.getsize(PATHS) == 0: print("STOP: PATHSFILE missing or empty"); sys.exit(2)
os.makedirs(OUT, exist_ok=True)
cmd = ["bash", DRIVER, WT, BR, HEAD, BASE, OUT, LOCK, QUEUE, QTOOL, "6000", "1200", "real", KEY, PATHS, RECORD, CELLS, SEAT]
TMP = "/private/tmp/prt"; os.makedirs(TMP, mode=0o700, exist_ok=True)   # X7: its own short directory (tsx makes a unix socket under it), created here so a cleared one cannot meet the first fallback's preflight
env = {k: v for k, v in os.environ.items() if not k.startswith("X8_") and k not in ("GIT_SSH_COMMAND", "PRERUN_DISABLE")}   # X7: a stray export in the seat's shell must not reach a production driver: by prefix, so no knob can be missed
env.update(X8_NETMAX="5", TMPDIR=TMP)
if ADOPT: env["X8_ADOPT_PREFIX"] = ADOPT
f = open(os.path.join(OUT, "driver.stdout"), "w")
p = subprocess.Popen(cmd, stdin=subprocess.DEVNULL, stdout=f, stderr=subprocess.STDOUT, start_new_session=True, env=env)
open(os.path.join(OUT, "driver.pid"), "w").write(str(p.pid) + "\n")
print(f"LAUNCHED detached driver pid {p.pid} head {HEAD[:12]} status {OUT}/status.txt")
