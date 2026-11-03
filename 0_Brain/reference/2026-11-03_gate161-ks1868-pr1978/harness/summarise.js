// G161: compare every head cell (and every base cell) to base+ordinaryError for the same env+path.
const fs = require('fs'); const path = require('path');
const W = path.resolve(__dirname, '..');
const file = process.argv[2] || path.join(W, 'logs/matrix_all.json');
const rs = JSON.parse(fs.readFileSync(file, 'utf8'));
const SITE = { verify: /argon2 verify failed/, hibp: /HIBP lookup failed/, acsNoSmtp: /\[Email\/ACS\] Send threw/, acsSmtpOk: /\[Email\/ACS\] Send threw/,
  smtp: /\[Email\/SMTP\] Failed to send/, oauthGetdel: /Redis command failed/, oauthMulti: /Redis command failed/, sweepMark: /markExpiredCerts failed/,
  sweepFind7: /findExpiringSoon\(7d\) failed/, sweepPubExpired: /ISSUER_CERT_EXPIRED failed/, sweepPubSoon: /ISSUER_CERT_EXPIRING_SOON failed/ };
const state = (r) => { const x = r.result || {}; const done = (x.logs || []).find((l) => /Issuer cert sweep complete/.test(l));
  return JSON.stringify({ alive: !!x.alive, died: !!x.died, exit: r.exit, outcome: x.outcome, calls: x.calls, stored: x.stateStillStored, replay: x.replay,
    complete: done ? (done.match(/"expired\\?":\\?\d+/) || [''])[0] + '|' + ((done.match(/"expiringSoon\\?":\{[^}]*\}/) || [''])[0]).replace(/\\/g, '') : undefined }); };
const siteLines = (r) => ((r.result || {}).logs || []).filter((l) => SITE[r.path] && SITE[r.path].test(l));
const ref = {}; for (const r of rs) if (r.version === 'base' && r.kind === 'ordinaryError') ref[r.env + '|' + r.path] = r;
const permissive = (r, f) => { const x = r.result || {}; const y = f.result || {};
  if (/^verify$|^oauth/.test(r.path) && x.outcome === 'resolved:true') return 'ACCEPTED';
  if (/^oauth/.test(r.path) && x.replay === 'resolved:true') return 'REPLAY-ACCEPTED';
  
  if (/^sweep/.test(r.path)) { const c = (a) => (a || []).filter((s) => /^markExpired|^find/.test(s)).length; if (c(x.calls) < c(y.calls)) return 'SWEEP-SKIPPED-STEPS'; if (x.died && !y.died) return 'DIED'; }
  return null; };
const tally = { head: { eq: 0, ne: 0, perm: 0, oneLine: 0 }, base: { eq: 0, ne: 0, perm: 0 } };
const rows = []; const diffs = []; const perm = [];
for (const r of rs) {
  if (/Up$/.test(r.path)) { rows.push(['CONTROL', r.env, r.path, r.version, r.result && r.result.outcome, (r.result && r.result.calls || []).join(',')].join('\t')); continue; }
  const f = ref[r.env + '|' + r.path]; const same = state(r) === state(f); const p = permissive(r, f);
  const t = tally[r.version]; same ? t.eq++ : t.ne++; if (p) { t.perm++; perm.push([r.version, r.env, r.path, r.kind, p].join(' ')); }
  const sl = siteLines(r); if (r.version === 'head' && sl.length === 1) t.oneLine++;
  if (!same) diffs.push([r.version, r.env, r.path, r.kind, state(r)].join('\t'));
  rows.push([r.env, r.path, r.kind, r.version, same ? 'EQ' : 'DIFF', r.result && r.result.outcome, r.result && r.result.died ? 'DIED' : 'alive', (sl[0] || '-').replace(/^\S+ \S+ /, '').slice(0, 140)].join('\t'));
}
console.log('tally', JSON.stringify(tally));
console.log('permissive cells (vs base+ordinaryError):', perm.length); perm.forEach((l) => console.log('  ', l));
console.log('reference states:'); for (const k of Object.keys(ref).sort()) if (!/Up$/.test(k)) console.log('  ', k, state(ref[k]));
console.log('non-EQ cells:', diffs.length);
const byKey = {}; for (const d of diffs) { const [v, e, p, k] = d.split('\t'); const key = v + ' ' + e + ' ' + p; (byKey[key] = byKey[key] || []).push(k); }
for (const k of Object.keys(byKey).sort()) console.log('  ', k, byKey[k].length, byKey[k].join(','));
fs.writeFileSync(file.replace(/\.json$/, '.tsv'), rows.join('\n') + '\n');
