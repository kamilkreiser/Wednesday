import os, json, urllib.request, re
env = {}
for l in open('/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env'):
    m = re.match(r'(LINEAR_API_KEY|LINEAR_TEAM_ID)=(.*)', l.strip())
    if m: env[m.group(1)] = m.group(2).strip().strip('"\'')
Q = '''query($after:String){ issues(first:100, after:$after, filter:{number:{gte:1840}, team:{id:{eq:"%s"}}}, orderBy:createdAt){ pageInfo{hasNextPage endCursor} nodes{ identifier title createdAt state{name} labels{nodes{name}} description } } }''' % env['LINEAR_TEAM_ID']
after = None; out = []
while True:
    req = urllib.request.Request('https://api.linear.app/graphql', data=json.dumps({'query': Q, 'variables': {'after': after}}).encode(), headers={'Content-Type': 'application/json', 'Authorization': env['LINEAR_API_KEY']})
    r = json.load(urllib.request.urlopen(req))
    if 'errors' in r: print(r['errors']); break
    d = r['data']['issues']; out += d['nodes']
    if not d['pageInfo']['hasNextPage']: break
    after = d['pageInfo']['endCursor']
json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ks_screen.json'), 'w'), indent=1)
for i in out: print(i['identifier'], i['state']['name'], i['createdAt'][:16], i['title'][:110])
