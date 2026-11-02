const { createRequire } = require('module'); const path = require('path'); const fs = require('fs');
const ver = p => { let d = path.dirname(p); while (!fs.existsSync(path.join(d,'package.json')) || JSON.parse(fs.readFileSync(path.join(d,'package.json'))).name === undefined) d = path.dirname(d); const j = JSON.parse(fs.readFileSync(path.join(d,'package.json'))); return `${j.name}@${j.version} (${path.relative(process.argv[2], d)})`; };
for (const from of process.argv.slice(3)) {
  const r = createRequire(from);
  const out = [from.split('/Dev/')[1]];
  for (const m of ['@azure/msal-node','@azure/identity']) { try { const p = r.resolve(m); out.push(m+' -> '+ver(p)); if (m==='@azure/identity') { const r2 = createRequire(p); out.push('   identity -> '+ver(r2.resolve('@azure/msal-node'))); } } catch (e) { out.push(m+' -> '+e.code); } }
  console.log(out.join('\n  '));
}
