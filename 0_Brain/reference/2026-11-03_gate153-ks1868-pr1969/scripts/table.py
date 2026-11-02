import json, glob, os
W = '/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate153-ks1868-pr1969'
rs = [json.load(open(f)) for f in sorted(glob.glob(W + '/logs/probe/*.result.json'))]
order = ['none', 'ordinary', 'string', 'revokedProxy', 'throwingGetter']
rs.sort(key=lambda r: (r['scen'], r['mr'], r['tag'].split('__')[0], order.index(r['kind'])))
def cell(r):
  s = r['scen']; o = {}
  o['boot_exit'] = r['exitedAtBoot']; o['fraudLoadRan'] = r['fraudLoadRan']; o['inj'] = r['injected']
  if 'apply' in r: o['apply'] = r['apply']; sa = r.get('storeAfterApply') or {}; o['BADrewards'] = [x for x in sa.get('rewards', []) if x['user'] == 'BAD']; o['BADref'] = sa.get('referralsForBAD')
  if 'check1' in r:
    o['check1'] = r['check1'].get('newMilestones', r['check1']) if isinstance(r['check1'], dict) else r['check1']; o['c1status'] = r['check1'].get('status')
    o['check2'] = r['check2'].get('newMilestones', r['check2']) if isinstance(r['check2'], dict) else r['check2']
    st = r.get('storeAfterCheck2') or {}; o['msRewardsREF'] = st.get('milestoneRewardsREF'); o['msRow'] = st.get('msRow'); o['msRewardsREF2'] = st.get('milestoneRewardsREF2'); o['msRowREF2'] = st.get('msRowREF2')
    o['rewardsView'] = r.get('rewardsView'); o['byOther'] = r.get('checkByOtherUser'); o['achievedLines'] = r.get('milestoneAchievedLines')
  if 'gen' in r: o['gen'] = r['gen']; o['genCustom'] = r['genCustom']; o['codesByGEN'] = r['storeAfterGen']['codesByGEN']
  if s == 'rewards_read': o['rewardsView'] = r.get('rewardsView')
  o['health'] = [r['health'], r['healthEnd']]; o['lines'] = [l for l in r['lines'] if 'Milestone achieved' not in l][:6]; o['unmodelled'] = r['unmodelled']
  return o
for r in rs:
  print(f"### {r['scen']} mr={r['mr']} {r['tag'].split('__')[0]} {r['kind']}")
  print(json.dumps(cell(r)))
