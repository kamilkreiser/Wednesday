#!/bin/bash
# kam_msgs.sh — read Kam's recent panel messages WITH their metadata.
#
# WHY THIS EXISTS (2026-09-10, twice in one hour, both costing Kam):
#   1. His 08:58 message carried view="tuesday" — it was typed at the TUESDAY tab.
#      Wednesday read only .text, answered it as its own, and had to retract.
#   2. His 09:09 message was the four characters "now?" WITH the document he had
#      been asked for ATTACHED. Wednesday read only .text and told him a
#      four-character message could not tell it anything. He then exported a PDF
#      he did not need to make.
#
# Both are one failure: a panel message is a STRUCTURED RECORD (text + view +
# attachments) and reading one field of it is not reading the message. The
# routing data existed and was correct both times; the CONSUMER was missing —
# which is the same sentence the 2026-09-09 lesson wrote about `view`, and it
# was still true a day later because nothing was built.
#
# Usage: kam_msgs.sh [n]        last n Kam messages (default 6), full text
#        kam_msgs.sh [n] --brief   one line each
set -u
N="${1:-6}"; case "$N" in --*) N=6;; esac
MODE="${2:-${1:-}}"
ROOT="$(cd -P "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
python3 - "$ROOT" "$N" "$MODE" <<'PY'
import json,sys,os
root,n,mode=sys.argv[1],int(sys.argv[2]),sys.argv[3]
p=os.path.join(root,'0_Brain/dashboard/data/chat_log.json')
d=json.load(open(p)); msgs=d if isinstance(d,list) else d.get('messages',d)
ks=[m for m in msgs if m.get('role')=='kam'][-n:]
if not ks: print('no Kam messages found'); raise SystemExit(0)
for m in ks:
    ts=m.get('ts','')
    view=m.get('view') or '(none)'
    atts=m.get('attachments') or []
    text=str(m.get('text',''))
    # THE TWO FLAGS THAT WERE MISSED. Loud, because the failure was quiet.
    warn=''
    if view and view not in ('wednesday','', None): warn += '  *** view=%s — NOT addressed to Wednesday; route it, do not answer it ***' % view
    if atts: warn += '  *** %d ATTACHMENT(S) — the message is not only its text ***' % len(atts)
    print('%s | view=%-10s | chars=%-5d | att=%d%s' % (ts, view, len(text), len(atts), warn))
    for a in atts:
        print('      -> %s   %s' % (a.get('name','?'), a.get('path','?')))
    if mode != '--brief':
        print('  ' + (text if len(text) < 4000 else text[:4000] + ' …[TRUNCATED IN DISPLAY]'))
    print()
# A cap on the store is a frame: say so rather than let a full-length message read as complete.
capped=[m for m in ks if len(str(m.get('text','')))>=2000]
if capped: print('WARNING: %d of these are >=2000 chars — the OLD input cap was exactly 2000. If one ends mid-sentence it was truncated at source.' % len(capped))
PY
