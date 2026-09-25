#!/usr/bin/env python3
"""capture_mail_gate24T2a.py — capture Seat L6's four READY mails (#1243, #1244, #1245, #1248 — the batch WIDENED to four and FROZEN by Wednesday) VERBATIM, by message id, for the round-24 first tier-2
batch gate24T2a. The ONLY inbox verb used is `inbox_digest.sh full wednesday-agent@agentmail.to '<id>'` (the form Wednesday permitted; other forms
mark mail seen). Writes mail_seatL6_ready_<n>.md per PR and the combined capture mail_gate24T2a_ready.md beside this script, each with the
TEXT_SHA256 of the digest output, plus the sha256 + byte count of the prior reports the gate must read (READ). Refuses (rc 1) if a digest read fails,
is empty, or does not name its head (in full or as its 12-hex prefix). Writes nothing else."""
import hashlib, os, subprocess, sys, datetime
G = os.path.dirname(os.path.abspath(__file__))
DIGEST = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/inbox_digest.sh'
R = '/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/'
PRIOR = [R + '2026-09-25-batch1241-t2d/report.md', R + '2026-09-25-batch1241-t2e/report.md', R + '2026-09-25-batch1218-t2c/report.md']
READY = [
    ('1243', 'KS-1117 + KS-1300 items 2-4', '0c89e2b503d9333829c277c50ad3b1a33f03cb96',
     '<010001a0d8c01e24-082d81ba-d275-4c68-8ab5-86b7e9feb020-000000@email.amazonses.com>', 'Seat L6 READY FOR QA — #1243 KS-1117 + KS-1300 items 2-4 (13:27:44Z)'),
    ('1244', 'KS-1111', '146b620fda53f008b3384334a474b06a16235af3',
     '<010001a0d8c74067-8e668428-c32b-4f46-bc60-9d724dc0a608-000000@email.amazonses.com>', 'Seat L6 READY FOR QA — #1244 KS-1111 (13:35:31Z)'),
    ('1245', 'KS-1313', '1700b5ae7dd56ad3e30602a40b20ae6469c35350',
     '<010001a0d8d70655-f820c101-0634-4057-921f-9de8a97f9fc0-000000@email.amazonses.com>', 'Seat L6 READY FOR QA — #1245 KS-1313 (13:52:45Z)'),
    ('1248', 'KS-1143 GF-2', '2b4960172644b5ef0414b94d46d11974012c2007',
     '<010001a0d8e71829-fbd4bcac-0c0d-4357-a096-40b4006d1429-000000@email.amazonses.com>', 'Seat L6 READY FOR QA — #1248 KS-1143 GF-2 (14:10:18Z)'),
]
now = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
parts = []
for n, key, head, mid, label in READY:
    p = subprocess.run(['bash', DIGEST, 'full', 'wednesday-agent@agentmail.to', mid], capture_output=True, text=True)
    if p.returncode != 0 or not p.stdout.strip(): print('REFUSING: #%s digest read rc %d: %s' % (n, p.returncode, p.stderr.strip()[:300])); sys.exit(1)
    if head not in p.stdout and head[:12] not in p.stdout: print('REFUSING: the #%s READY does not name the head %s' % (n, head)); sys.exit(1)
    sha = hashlib.sha256(p.stdout.encode()).hexdigest()
    named = 'in full' if head in p.stdout else 'as its 12-hex prefix `%s` only' % head[:12]
    body = '## %s\nMESSAGE_ID %s\nTEXT_SHA256 %s\n#%s %s head %s (the READY names it %s; origin read by predict_gate24T2a.py)\n\n%s\n' % (
        label, mid, sha, n, key, head, named, p.stdout.rstrip('\n'))
    open(os.path.join(G, 'mail_seatL6_ready_%s.md' % n), 'w', encoding='utf-8').write(body)
    parts.append(body)
    print('captured #%s %s TEXT_SHA256 %s (%d B)' % (n, mid, sha, len(p.stdout.encode())))
pr = []
for f in PRIOR:
    b = open(f, 'rb').read(); pr.append('PRIOR REPORT (READ): %s sha256 %s (%d bytes)' % (f, hashlib.sha256(b).hexdigest(), len(b)))
hdr = ('# CAPTURE — gate24T2a READY mails, VERBATIM by message id (captured %s by capture_mail_gate24T2a.py; instrument: `inbox_digest.sh full '
       'wednesday-agent@agentmail.to <id>`)\n\nFOUR READYs from ONE seat (Seat L6, pane Secuura/Blockchain). PR #1243 is KS-1117 + KS-1300 (items 2-4), head '
       '0c89e2b503d9333829c277c50ad3b1a33f03cb96; PR #1244 is KS-1111, head 146b620fda53f008b3384334a474b06a16235af3; PR #1245 is KS-1313, head '
       '1700b5ae7dd56ad3e30602a40b20ae6469c35350; PR #1248 is KS-1143 GF-2, head 2b4960172644b5ef0414b94d46d11974012c2007 (a cherry-pick of Seat L3\'s a40cb9eea049). '
       'The batch was WIDENED to four and FROZEN by Wednesday. #1241 (KS-1226, open, capped, unmerged) is NOT in this batch; KS-1144 (to branch from #1248\'s head) is NOT in it either.\n%s\n' % (now, '\n'.join(pr)))
open(os.path.join(G, 'mail_gate24T2a_ready.md'), 'w', encoding='utf-8').write(hdr + '\n' + '\n'.join(parts))
for l in pr: print(l)
print('wrote', os.path.join(G, 'mail_gate24T2a_ready.md'))
