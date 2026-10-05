#!/usr/bin/env python3
"""Arms for fleet/hooks/receiptguard.py — every arm must PASS before the hook clause is trusted.
Run: python3 2_Project_Files/tests/receiptguard_arms.py   (exit 0 = all pass)"""
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
GUARD = os.path.join(HERE, "..", "fleet", "hooks", "receiptguard.py")
T = "/Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files"

ARMS = [
    # (name, expected clause or "", command)
    ("R1 the real 06:13 shape: send && tap; note says sent", "receipt-chain",
     f"bash {T}/fleet/send_brief.sh --kind answer x y && bash {T}/fleet/cockpit/cockpit.sh say %6 'ptr' --mail 'GO'\n"
     f"bash {T}/tools/note_entry.sh --stdin <<'EOF'\nGO to N. Mail sent, tap verified.\nEOF"),
    ("R2 the 10-03 shape: chat_reply then note says posted (201)", "receipt-chain",
     f"bash {T}/tools/chat_reply.sh 'brief'; bash {T}/tools/note_entry.sh --stdin <<'EOF'\nBrief posted (HTTP 201).\nEOF"),
    ("R3 decision_queue add + note says delivered", "receipt-chain",
     f"bash {T}/tools/decision_queue.sh add x; bash {T}/tools/note_entry.sh --stdin <<'EOF'\ncard delivered\nEOF"),
    ("P1 note alone quoting a send's output line (the correct shape)", "",
     f"bash {T}/tools/note_entry.sh --stdin <<'EOF'\nthe send printed \"sent: ...\"; tap delivered.\nEOF"),
    ("P2 send in the same command, note body has NO receipt word", "",
     f"bash {T}/fleet/send_brief.sh x; bash {T}/tools/note_entry.sh --stdin <<'EOF'\nBrief drafted for N; the send is the next action.\nEOF"),
    ("P3 a brief BODY mentions note_entry.sh and 'sent' (prose in a heredoc)", "",
     f"cat > /tmp/b.md <<'EOF'\nrun note_entry.sh after send_brief.sh; never write sent first\nEOF\nbash {T}/fleet/send_brief.sh --file /tmp/b.md"),
    ("R4 the 10-05 shape: redirect to $R/../file", "dotdot-write",
     "R=/Volumes/KK_T9_External_HDD/TUESDAY; curl -s https://x > $R/../TUESDAY_scratch_mail.json"),
    ("R5 the 09-30 shape: append redirect via ..", "dotdot-write",
     "bash x.sh >> $T/../TUESDAY_sb.out 2>&1"),
    ("R6 mv into ..", "dotdot-write", "mv /tmp/a.json /Volumes/KK_T9_External_HDD/TUESDAY/../a.json"),
    ("R7 tee -a into ..", "dotdot-write", "echo hi | tee -a $R/../log.txt"),
    ("P4 2>&1 and a plain scratchpad redirect", "",
     "bash x.sh > /private/tmp/claude-501/s/out.txt 2>&1"),
    ("P5 .. used in a READ (cat / ls), not a write", "",
     "ls $R/..; cat $R/../README"),
    ("P6 a heredoc body talking about $R/../x redirects", "",
     "cat > /private/tmp/n.md <<'EOF'\nnever write > $R/../x again\nEOF"),
    ("P7 a file name with two dots that is not a .. segment", "",
     "cp /tmp/a..b /tmp/c..d; echo x > /tmp/v1..2.txt"),
]

fails = 0
for name, want, cmd in ARMS:
    r = subprocess.run([sys.executable, GUARD], input=cmd, capture_output=True, text=True)
    got = r.stdout.strip().split("|")[0]
    ok = (got == want) and r.returncode == 0 and not r.stderr
    fails += 0 if ok else 1
    print(("PASS" if ok else "FAIL"), name, "->", repr(r.stdout.strip() or "(allowed)"),
          ("stderr:" + r.stderr.strip()) if r.stderr else "")
print("arms: %d, failed: %d" % (len(ARMS), fails))
sys.exit(1 if fails else 0)
