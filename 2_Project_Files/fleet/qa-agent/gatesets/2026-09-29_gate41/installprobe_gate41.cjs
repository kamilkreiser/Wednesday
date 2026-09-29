// installprobe_gate41.cjs <install dir> — the drafter's MEASURED probe inside ONE standalone `npm ci --ignore-scripts` of a service lock
// (the Dockerfile's own install line). Prints ONE JSON line. Local only: an http server on 127.0.0.1 port 0, nodemailer's streamTransport
// (builds the RFC822 message, opens NO socket) and createTransport with the call site's SMTP option SHAPE (never connected).
const path = require('path'); const http = require('http');
const dir = process.argv[2]; const req = (m) => require(require.resolve(m, { paths: [dir] }));
const out = { dir: path.basename(dir), node: process.version };
const ver = (m) => { try { return { version: req(m + '/package.json').version, resolved: path.relative(dir, require.resolve(m, { paths: [dir] })) }; } catch (e) { return { error: String(e.message).slice(0, 120) }; } };
out.nodemailer = ver('nodemailer'); out.morgan = ver('morgan'); out.types_nodemailer = (() => { try { return req('@types/nodemailer/package.json').version; } catch (e) { return null; } })();
(async () => {
  if (!out.nodemailer.error) {
    const nm = req('nodemailer');
    // the call site's shape (services/<svc>/src/services/email.ts: createTransport({host, port, secure: port === 465, auth: {user, pass}}) — never connected)
    const t = nm.createTransport({ host: 'smtp.invalid', port: 465, secure: true, auth: { user: 'u', pass: 'p' } });
    out.smtp_transport = { name: t.transporter && t.transporter.name, host: t.options && t.options.host, secure: t.options && t.options.secure, has_sendMail: typeof t.sendMail };
    // the call site's sendMail option shape (from, to, subject, text, html) through streamTransport: the message is BUILT, nothing is sent
    const s = nm.createTransport({ streamTransport: true, buffer: true, newline: 'unix' });
    try {
      const info = await s.sendMail({ from: 'Secuura <noreply@example.invalid>', to: 'kam@example.invalid', subject: 'probe', text: 'plain body', html: '<p>html body</p>' });
      const msg = info.message.toString();
      out.sendMail = { ok: true, envelope: info.envelope, has_from: /^From: Secuura <noreply@example\.invalid>$/m.test(msg), multipart_alt: /multipart\/alternative/.test(msg), bytes: msg.length };
    } catch (e) { out.sendMail = { ok: false, error: String(e.message).slice(0, 160) }; }
  }
  if (!out.morgan.error) {
    const morgan = req('morgan'); const lines = [];
    const mw = morgan('combined', { stream: { write: (l) => lines.push(l) } });
    const srv = http.createServer((q, r) => mw(q, r, () => { r.end('ok'); })); await new Promise((ok) => srv.listen(0, '127.0.0.1', ok));
    const port = srv.address().port;
    const hit = (ua) => new Promise((ok, ko) => { const c = http.request({ host: '127.0.0.1', port, path: '/p', headers: { 'User-Agent': ua, Referer: 'http://r.invalid/' } }, (r) => { r.resume(); r.on('end', ok); }); c.on('error', ko); c.end(); });
    await hit('plain-agent/1.0'); await hit('evil" 200 999 "injected');
    await new Promise((ok) => setTimeout(ok, 50)); srv.close();
    out.morgan_combined = { lines: lines.map((l) => l.trimEnd()), control_logs: lines.length >= 1 && /"plain-agent\/1\.0"$/.test(lines[0].trimEnd()),
      planted_quote_escaped: lines.length >= 2 && !lines[1].includes('"evil" 200 999 "injected"'), planted_raw_present: lines.length >= 2 && lines[1].includes('evil" 200 999 "injected') };
  }
  console.log(JSON.stringify(out));
})().catch((e) => { out.fatal = String(e && e.stack || e).slice(0, 300); console.log(JSON.stringify(out)); process.exit(1); });
