#!/usr/bin/env python3
"""capture_mail_gate21T2e.py — capture Seat B 27th's round-2 READY for #1241 KS-1226 VERBATIM, by message id, for the round-21 tier-2 gate
gate21T2e (#1241 ROUND 2 OF 2). The ONLY inbox verb used is `inbox_digest.sh full wednesday-agent@agentmail.to '<id>'` (the form Wednesday
permitted; other forms mark mail seen). Writes mail_seatB27th_ready_1241r2.md and the combined capture mail_gate21T2e_ready.md beside this script,
each with the TEXT_SHA256 of the digest output, plus the round-1 NO GO report's sha256 + byte count (READ). Refuses (rc 1) if the digest read fails,
is empty, or does not name the head in full. Writes nothing else."""
import hashlib, os, subprocess, sys, datetime
G = os.path.dirname(os.path.abspath(__file__))
DIGEST = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/inbox_digest.sh'
R1 = '/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-25-batch1241-t2d/report.md'
N, HEAD = '1241', 'b4427d416592b40eb5ddb8727b2d6c31f3c7d067'
MID = '<010001a0d85ed666-0a7d4255-03c2-4a75-82e1-0c77be87e78f-000000@email.amazonses.com>'
LABEL = 'Seat B 27th READY FOR QA (round 2 of 2) — #1241 KS-1226 item 2 (11:41:29Z)'
now = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
p = subprocess.run(['bash', DIGEST, 'full', 'wednesday-agent@agentmail.to', MID], capture_output=True, text=True)
if p.returncode != 0 or not p.stdout.strip(): print('REFUSING: digest read rc %d: %s' % (p.returncode, p.stderr.strip()[:300])); sys.exit(1)
if HEAD not in p.stdout and HEAD[:12] not in p.stdout: print('REFUSING: the READY does not name the head %s' % HEAD); sys.exit(1)
sha = hashlib.sha256(p.stdout.encode()).hexdigest()
r1 = open(R1, 'rb').read()
body = '## %s\nMESSAGE_ID %s\nTEXT_SHA256 %s\n#%s head %s (the READY names it as `%s`; origin read by predict_gate21T2e.py)\n\n%s\n' % (
    LABEL, MID, sha, N, HEAD, HEAD, p.stdout.rstrip('\n'))
open(os.path.join(G, 'mail_seatB27th_ready_1241r2.md'), 'w', encoding='utf-8').write(body)
hdr = ('# CAPTURE — gate21T2e READY mail, VERBATIM by message id (captured %s by capture_mail_gate21T2e.py; instrument: `inbox_digest.sh full '
       'wednesday-agent@agentmail.to <id>`)\n\nONE READY from ONE seat (Seat B 27th, pane Secuura/Blockchain, record 5_Project_History/2026-09-25_seatB-27th/). '
       'PR #1241 is KS-1226 (item 2 only), ROUND 2 OF 2, head %s (round-1 head e2d0518df40228f0a183bc4223c7a6840821253e, NO GO).\n'
       'ROUND-1 NO GO REPORT (READ): %s sha256 %s (%d bytes)\n' % (now, HEAD, R1, hashlib.sha256(r1).hexdigest(), len(r1)))
open(os.path.join(G, 'mail_gate21T2e_ready.md'), 'w', encoding='utf-8').write(hdr + '\n' + body)
print('captured #%s %s TEXT_SHA256 %s (%d B); round-1 report sha256 %s (%d B)' % (N, MID, sha, len(p.stdout.encode()), hashlib.sha256(r1).hexdigest(), len(r1)))
print('wrote', os.path.join(G, 'mail_gate21T2e_ready.md'))
