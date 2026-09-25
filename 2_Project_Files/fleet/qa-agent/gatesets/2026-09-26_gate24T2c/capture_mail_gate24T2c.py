#!/usr/bin/env python3
"""capture_mail_gate24T2c.py — capture the FIVE mails behind gate24T2c's SEVEN PRs VERBATIM by message id: #1245 round 2 (Seat L6), #1256 (Seat B 28th),
#1257-#1260 (ONE Seat L5 mail), #1261 (Seat B 28th), and Seat L5's DECLARED COUNTS mail. The ONLY inbox verb used is
`inbox_digest.sh full wednesday-agent@agentmail.to '<id>'` (the form Wednesday permitted; other forms mark mail seen). Writes mail_ready_<tag>.md per
mail, mail_l5_declared_counts.md, and the combined mail_gate24T2c_ready.md beside this script, each with the TEXT_SHA256 of the digest output, plus
the sha256 + byte count of the prior reports the gate must read (READ). Refuses (rc 1) if a read fails, is empty, or does not name each of its heads
(in full or as the 12-hex prefix). Writes nothing else."""
import hashlib, os, subprocess, sys, datetime
G = os.path.dirname(os.path.abspath(__file__))
DIGEST = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/inbox_digest.sh'
R = '/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/'
PRIOR = [R + '2026-09-26-batch1243-t2a/report.md', R + '2026-09-25-batch1241-t2d/report.md', R + '2026-09-25-batch1241-t2e/report.md',
         R + '2026-09-14-ks1061-931-795307023-tier2-r1/report.md', R + '2026-09-25-batch1215-t2-r1/report.md',
         R + '2026-09-13-ks877-977-aede93117-tier2-r2/report.md', R + '2026-09-22-batch1180-1197-r1/report.md',
         R + '2026-09-06-s140b-ks859-858-87055ea1e-tier2/report.md', R + '2026-09-17-ks528-1025-9954a7069-tier2-r1/report.md']
MAILS = [
    ('1245r2', [('1245', 'KS-1313', '65eb964271b0d6895e90fe8f5ffcbbbb9a484050')], '<010001a0d940353e-4a4680f7-3312-43b7-8856-821ea78b7c2c-000000@email.amazonses.com>',
     'Seat L6 READY FOR QA — #1245 KS-1313 ROUND 2 OF 2 (15:47:38Z)'),
    ('1256', [('1256', 'KS-1159', '5a41ed7fea96ab77ed1dc263ae0c7d25c9846440')], '<010001a0d9350164-941d2684-08e6-4439-a0ba-bac27ad84dad-000000@email.amazonses.com>',
     'Seat B 28th READY FOR QA — #1256 KS-1159 (15:35:24Z)'),
    ('1257_1260', [('1257', 'KS-1201', 'd1db0d41ac52359c231cd22abf11124204645d97'), ('1258', 'KS-1296', 'ff90fbf9d7e351104404e3eaad505a673e656c1e'),
                   ('1259', 'KS-906', '8a2a28f50eb3453db7284da0f098f6a819d40145'), ('1260', 'KS-1139', '62e69d23b2507780316f1930123c7d57ebba3ae2')],
     '<010001a0d93a67d7-c6ccc405-6a68-4e9d-af7e-1bff484d8ce5-000000@email.amazonses.com>', 'Seat L5 READY FOR QA — #1257 #1258 #1259 #1260 (15:41:18Z)'),
    ('1261', [('1261', 'KS-1293', 'eab8d7031b1b19071a66715ca0aabd9c5cb29c6d')], '<010001a0d9510d1e-c4cee50d-0d4a-4b3e-b2f1-83fa56ba7a24-000000@email.amazonses.com>',
     'Seat B 28th READY FOR QA — #1261 KS-1293 (16:06:02Z)'),
]
DECL = ('<010001a0d908983b-1d9957c7-1c7d-497d-a4ec-ed29a0401559-000000@email.amazonses.com>', 'Seat L5 DECLARED COUNTS for items 2, 5, 6, 7 (14:46:54Z) — the declaration of record for #1257-#1260')
now = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
def read(mid):
    p = subprocess.run(['bash', DIGEST, 'full', 'wednesday-agent@agentmail.to', mid], capture_output=True, text=True)
    if p.returncode != 0 or not p.stdout.strip(): print('REFUSING: digest read of %s rc %d: %s' % (mid, p.returncode, p.stderr.strip()[:300])); sys.exit(1)
    return p.stdout
parts = []
for tag, rows, mid, label in MAILS:
    txt = read(mid); sha = hashlib.sha256(txt.encode()).hexdigest(); names = []
    for n, key, head in rows:
        if head not in txt and head[:12] not in txt: print('REFUSING: the %s mail does not name #%s\'s head %s' % (tag, n, head)); sys.exit(1)
        names.append('#%s %s head %s (the READY names it %s)' % (n, key, head, 'in full' if head in txt else 'as its 12-hex prefix `%s` only' % head[:12]))
    body = '## %s\nMESSAGE_ID %s\nTEXT_SHA256 %s\n%s\n\n%s\n' % (label, mid, sha, '\n'.join(names), txt.rstrip('\n'))
    open(os.path.join(G, 'mail_ready_%s.md' % tag), 'w', encoding='utf-8').write(body)
    parts.append(body); print('captured %s %s TEXT_SHA256 %s (%d B)' % (tag, mid, sha, len(txt.encode())))
txt = read(DECL[0]); sha = hashlib.sha256(txt.encode()).hexdigest()
body = '## %s\nMESSAGE_ID %s\nTEXT_SHA256 %s\n\n%s\n' % (DECL[1], DECL[0], sha, txt.rstrip('\n'))
open(os.path.join(G, 'mail_l5_declared_counts.md'), 'w', encoding='utf-8').write(body); parts.append(body)
print('captured L5 DECLARED COUNTS %s TEXT_SHA256 %s' % (DECL[0], sha))
pr = []
for f in PRIOR:
    b = open(f, 'rb').read(); pr.append('PRIOR REPORT (READ): %s sha256 %s (%d bytes)' % (f, hashlib.sha256(b).hexdigest(), len(b)))
hdr = ('# CAPTURE — gate24T2c READY mails, VERBATIM by message id (captured %s by capture_mail_gate24T2c.py; instrument: `inbox_digest.sh full '
       'wednesday-agent@agentmail.to <id>`)\n\nSEVEN PRs from THREE seats in FIVE mails. PR #1245 is KS-1313 (ROUND 2 OF 2, THE CAP ROUND), head '
       '65eb964271b0d6895e90fe8f5ffcbbbb9a484050; PR #1256 is KS-1159, head 5a41ed7fea96ab77ed1dc263ae0c7d25c9846440; PR #1257 is KS-1201, head '
       'd1db0d41ac52359c231cd22abf11124204645d97; PR #1258 is KS-1296, head ff90fbf9d7e351104404e3eaad505a673e656c1e; PR #1259 is KS-906, head '
       '8a2a28f50eb3453db7284da0f098f6a819d40145; PR #1260 is KS-1139, head 62e69d23b2507780316f1930123c7d57ebba3ae2; PR #1261 is KS-1293, head '
       'eab8d7031b1b19071a66715ca0aabd9c5cb29c6d. The batch is FROZEN at seven. Seat L5\'s DECLARED COUNTS mail is captured last, as the declaration of record.\n%s\n' % (now, '\n'.join(pr)))
open(os.path.join(G, 'mail_gate24T2c_ready.md'), 'w', encoding='utf-8').write(hdr + '\n' + '\n'.join(parts))
for l in pr: print(l)
print('wrote', os.path.join(G, 'mail_gate24T2c_ready.md'))
