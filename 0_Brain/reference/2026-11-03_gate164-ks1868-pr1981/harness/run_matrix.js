// G164: run every cell serially (host load is high). argv: outJson [builds comma list, default base,head] [sites] [kinds]
const { spawnSync } = require('child_process');
const fs = require('fs');
const path = require('path');
const KINDS = ['ordinaryError','plainString','number42','null','undefined','revokedProxy','messageGetterThrows','symbolMessage','bigintMessage','bigintValue','messageToJSONThrows','errToJSONThrows','objToStringThrows','messageToStringThrows','messageIsRevokedProxy','cyclicMessage','numberMessage','nullMessage','nullProtoMessage'];
const [outFile, builds = 'base,head', sites = 'route,direct,routeUp,directUp', kinds = KINDS.join(',')] = process.argv.slice(2);
const res = [];
for (const env of ['development', 'production'])
  for (const v of builds.split(','))
    for (const s of sites.split(','))
      for (const k of (/Up$/.test(s) ? ['ordinaryError'] : kinds.split(','))) {
        const extra = v.includes('/') ? { G164_BUILD: v } : {};
        const r = spawnSync('node', [path.join(__dirname, 'cell.js'), v.includes('/') ? 'mut' : v, s, k], { env: { ...process.env, NODE_ENV: env, ...extra }, encoding: 'utf8', timeout: 90000 });
        const line = (r.stdout || '').split('\n').find((l) => l.startsWith('G164RESULT '));
        const o = line ? JSON.parse(line.slice(11)) : { version: v, site: s, kind: k, env, noResult: true, status: r.status, stderr: (r.stderr || '').slice(0, 300) };
        o.exit = r.status; if (v.includes('/')) o.version = v;
        res.push(o);
      }
fs.writeFileSync(outFile, JSON.stringify(res, null, 1));
console.log('cells', res.length);
