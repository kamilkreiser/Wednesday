#!/usr/bin/env python3
"""capture_mail_gate21T2d.py — capture Seat B 26th's two READY mails VERBATIM, by message id, for the round-21 FOURTH tier-2 batch gate (#1241 KS-1226
item 2, #1242 KS-980). The ONLY inbox verb used is `inbox_digest.sh full wednesday-agent@agentmail.to '<id>'` (the form Wednesday permitted; other
forms mark mail seen). Writes mail_seatB26th_ready_<n>.md per mail and the combined capture mail_gate21T2d_ready.md beside this script, each with the
TEXT_SHA256 of the digest output; refuses (rc 1) if a digest read fails, is empty, or does not name its PR's head in full. Writes nothing else."""
import hashlib, os, subprocess, sys, datetime
G = os.path.dirname(os.path.abspath(__file__))
DIGEST = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/inbox_digest.sh'
MAILS = [('1241', 'e2d0518df40228f0a183bc4223c7a6840821253e', '<010001a0d78409d5-38b1a5db-bb92-418e-948f-80ca7b5d4596-000000@email.amazonses.com>',
          'Seat B 26th READY FOR QA 2 — #1241 KS-1226 item 2 (07:42:29Z)'),
         ('1242', 'a35569aa020e63b2660b60e48b4f0286c46b27fc', '<010001a0d796d5e3-944c6737-2294-4d1d-9b04-cfb4af1b0580-000000@email.amazonses.com>',
          'Seat B 26th READY FOR QA 3 — #1242 KS-980 (08:03:01Z)')]
now = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
parts = ['# CAPTURE — gate21T2d READY mails, VERBATIM by message id (captured %s by capture_mail_gate21T2d.py; instrument: `inbox_digest.sh full '
         'wednesday-agent@agentmail.to <id>`)\n' % now,
         'Two READYs from ONE seat (Seat B 26th, pane Secuura/Blockchain, record 5_Project_History/2026-09-25_seatB-26th/). '
         'PR #1241 is KS-1226 (item 2 only). PR #1242 is KS-980.\n']
for n, head, mid, label in MAILS:
    p = subprocess.run(['bash', DIGEST, 'full', 'wednesday-agent@agentmail.to', mid], capture_output=True, text=True)
    if p.returncode != 0 or not p.stdout.strip(): print('REFUSING: digest read rc %d for #%s: %s' % (p.returncode, n, p.stderr.strip()[:300])); sys.exit(1)
    if head not in p.stdout: print('REFUSING: the READY for #%s does not name its head %s in full' % (n, head)); sys.exit(1)
    sha = hashlib.sha256(p.stdout.encode()).hexdigest()
    body = '## %s\nMESSAGE_ID %s\nTEXT_SHA256 %s\n#%s head %s\n\n%s\n' % (label, mid, sha, n, head, p.stdout.rstrip('\n'))
    open(os.path.join(G, 'mail_seatB26th_ready_%s.md' % n), 'w', encoding='utf-8').write(body)
    parts.append(body)
    print('captured #%s %s TEXT_SHA256 %s (%d B)' % (n, mid, sha, len(p.stdout.encode())))
open(os.path.join(G, 'mail_gate21T2d_ready.md'), 'w', encoding='utf-8').write('\n'.join(parts))
print('wrote', os.path.join(G, 'mail_gate21T2d_ready.md'))
