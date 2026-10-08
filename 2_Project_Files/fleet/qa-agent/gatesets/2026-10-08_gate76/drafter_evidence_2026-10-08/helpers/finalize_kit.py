#!/usr/bin/env python3
"""finalize_kit.py — adds the MEASURED predictions to kit.json (the default-order chain from composed_2026-10-08/chain.json, the reverse
order's chain from the drafter's scratch chain, the staged merge inputs, the builder probe) and pins every launcher-REQUIRED file's sha256.
Usage: finalize_kit.py <kit dir> <reverse-order chain.json> <builder probe_result.json>"""
import hashlib, json, os, sys
KD, REV, BP = sys.argv[1:4]
p = os.path.join(KD, 'kit.json'); K = json.load(open(p, encoding='utf-8'))
c = json.load(open(os.path.join(KD, 'composed_2026-10-08', 'chain.json'))); r = json.load(open(REV))
strip = lambda s: {k: s[k] for k in ('step', 'pr', 'head', 'onto', 'tree', 'merge_in_needed', 'tree_equals_end_tree', 'flow_blob', 'cheat_blob', 'sim_commit')}
K['predicted_chain'] = {'develop': c['develop'], 'order': c['order'], 'steps': [strip(s) for s in c['steps']],
    'composed_dir': 'composed_2026-10-08/', 'NOTE': 'c4_docs_gate76.py chain at develop 0a6177ea5482 (drafter 07:40:52Z): step 1 no merge-in (== END_TREE); step 2 docs-only keep-both merge-in, guard 12/0 at both steps, FINAL one-pass composition == step-2 blobs, every code path == its own head blob; merge-tree cross-check rc 1 on exactly the two docs (never picked); `git merge-file --union` DIFFERS on the FLOW doc (drops one `</td></tr></table>`: table/td/tr each +1 open) and AGREES on the cheat. SIM commits are deterministic (fixed author/committer/date in c4 SIM_ENV), so the gate reproduces the same SIM shas.',
    'merge_in_push_delta': {'OURS..M (paths)': 9, 'DEV..M (paths)': 6, 'OURS..M stat': '9 files, +421/-4 (all of #1428 incl. 7 Blockchain/Dev/services/originate paths)', 'DEV..M stat': '6 files, +94/-8'}}
K['predicted_reverse_order'] = {'order': r['order'], 'steps': [strip(s) for s in r['steps']], 'merge_in_push_delta': {'OURS..M (paths)': 6, 'DEV..M (paths)': 9}}
K['merge_inputs'] = json.load(open(os.path.join(KD, 'merge_inputs', 'MERGE_INPUTS.json'), encoding='utf-8'))
K['builder_probe'] = {'tool': "Seat R 17th's build_addendumra17_gate75.py (sha256/16 04ed62b4ff18b3d3, 386 lines), a byte copy read into the drafter's scratchpad",
                      'results': {k: {'rc': v[0], 'line': v[1].split('/scratchpad/')[-1]} for k, v in json.load(open(BP)).items()}}
REQ = ['lib_gate76.py', 'composee5_copy.py', 'c1_pin_gate76.py', 'c3_redgreen_gate76.py', 'c3_preflight_gate76.py', 'c4_docs_gate76.py', 'gh_gate76.py',
       'fixture_body_1427_at_draft.md', 'fixture_body_1428_at_draft.md', 'prompt_gate76.txt', 'launch_qa_secuura_gate76.sh', 'repin_and_launch_gate76.sh']
K['script_sha256'] = {f: hashlib.sha256(open(os.path.join(KD, f), 'rb').read()).hexdigest() for f in REQ}
json.dump(K, open(p, 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
print('kit.json finalized:', len(K['script_sha256']), 'pins;', 'chain', [s['tree'][:12] for s in K['predicted_chain']['steps']], 'reverse', [s['tree'][:12] for s in K['predicted_reverse_order']['steps']])
