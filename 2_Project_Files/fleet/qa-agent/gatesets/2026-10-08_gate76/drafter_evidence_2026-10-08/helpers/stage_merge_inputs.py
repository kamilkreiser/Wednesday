#!/usr/bin/env python3
"""stage_merge_inputs.py — the gate76 drafter's staging of the two squash-body DRAFTS and subjects from the REAL PR bodies (fixtures read by
GET at draft). Every edit asserts its anchor count first; the outputs are measured (bytes, sha256, hyphenated keys, closing adjacency under
BOTH the kit regex and the R-lane builder's broader CLOSING regex, attribution lines). Usage: stage_merge_inputs.py <kit dir>"""
import hashlib, json, os, re, sys

KD = sys.argv[1]; K = json.load(open(os.path.join(KD, 'kit.json'), encoding='utf-8'))
BUILDER_CLOSING = re.compile(r"(close[sd]?|closing|fix(e[sd])?|fixing|resolve[sd]?|resolving|complete[sd]?|completing)[\s:,—-]*(KS-\d+|#\d+"
                             r"|https://linear\.app/\S*KS-\d+)", re.I)   # build_addendumra17_gate75.py's CLOSING, copied by reading


def edit(s, a, b, n=1):
    c = s.count(a)
    if c != n: raise SystemExit('anchor count %d != %d for %r' % (c, n, a[:80]))
    return s.replace(a, b)


body = {r: open(os.path.join(KD, 'fixture_body_%s_at_draft.md' % r), encoding='utf-8').read() for r in K['rows']}
out = {}
# #1427: strip the attribution line only (Q-ATTR76); nothing else is changed
b = edit(body['1427'], '\n\n🤖 Generated with [Claude Code](https://claude.com/claude-code)', '')
out['1427'] = (b, 'KS-1274: job 04 fails a scan when trivy reports neither Results nor ArtifactName',
               ['attribution line `🤖 Generated with [Claude Code](…)` removed (Q-ATTR76)'])
# #1428: two corrections the drafter MEASURED (Q-CLAIMS593); the gate re-reads every sentence and may correct more
b = body['1428']
b = edit(b, '9 paths, +336/-4.', '9 paths, +421/-4.')
b = edit(b, '**No authorisation decision moves.** Every guard runs after authentication, the role/scope gate and the tenant-scoped read, and before any write transaction — so nothing is persisted on a refused request.',
         '**No authorisation decision moves.** Every guard runs after authentication (and, where the route has one, its role/scope gate) and before any database read or write, so nothing is read or persisted on a refused request; in the share handler it also runs after the tenant-scoped document read.')
out['1428'] = (b, K['rows']['1428']['pr_title'],
               ['`+336/-4` -> `+421/-4` (numstat sum over the 9 paths, c1 P3 / API A3)',
                'the authorisation sentence: the two adminConfig guards and the signatories validators run BEFORE any read (there is no tenant-scoped read before them); only the share guard runs after one'])
res = {}
for r, (b, subj, edits) in out.items():
    R = K['rows'][r]
    p = os.path.join(KD, 'merge_inputs', '%s.squash_body.DRAFT.txt' % r)
    open(p, 'w', encoding='utf-8').write(b)
    raw = b.encode()
    hy = sorted(set(re.findall(r'\bKS-\d+\b', b + '\n' + subj)))
    cl1 = re.findall(K['closing_rx'], b + '\n' + subj, re.I); cl2 = BUILDER_CLOSING.findall(b + '\n' + subj)
    ctl = BUILDER_CLOSING.findall(b + '\nThis does not close %s.\n' % R['ticket'])
    res[r] = {'file': p, 'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest(), 'edits': edits, 'subject': subj, 'subject_len': len(subj),
              'subject_ascii': subj.isascii(), 'subject_opens_own_key': subj.startswith(R['ticket'] + ': '), 'subject_has_paren_hash': '(#' in subj,
              'hyphenated_keys_subject_plus_body': hy, 'closing_kit_rx': len(cl1), 'closing_builder_rx': len(cl2),
              'CONTROL_builder_rx_on_planted_residue': len(ctl), 'merged_by': b.count('Merged by '),
              'generated_with': len(re.findall(r'(?im)generated with \[claude code\]', b)), 'co_authored_by': len(re.findall(r'(?im)^co-authored-by:', b))}
    open(os.path.join(KD, 'merge_inputs', '%s.squash_subject.DRAFT.txt' % r), 'w', encoding='utf-8').write(subj + '\n')
json.dump(res, open(os.path.join(KD, 'merge_inputs', 'MERGE_INPUTS.json'), 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
for r, v in res.items():
    print(r, {k: v[k] for k in v if k not in ('file', 'edits')})
