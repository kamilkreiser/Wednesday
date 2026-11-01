// gate 79 emulation: Express 4.22.3 from the repo, the persona.ts catch body verbatim (base or head),
// thrown value = revoked Proxy, real HTTP request. Usage: node base_catch_emul.js <base|head> <expressDir>
const [mode, expressDir] = process.argv.slice(2);
const express = require(expressDir);
const app = express();
const logger = { error: (m, meta) => console.log('LOG error', m, JSON.stringify(meta)) };
app.post('/demo-api/persona/switch', async (req, res) => {
  try {
    const { proxy, revoke } = Proxy.revocable({}, {}); revoke();
    await Promise.reject(proxy);
  } catch (err) {
    let message;
    if (mode === 'base') {
      message = err instanceof Error ? err.message : 'Unknown error';
    } else {
      try { message = err instanceof Error ? err.message : 'Unknown error'; } catch { message = 'unreadable thrown value'; }
    }
    logger.error('Persona switch error', { error: message });
    return res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'Internal server error' } });
  }
});
process.on('exit', (c) => console.log('PROCESS EXIT code', c));
const srv = app.listen(0, async () => {
  const port = srv.address().port;
  try {
    const r = await fetch(`http://127.0.0.1:${port}/demo-api/persona/switch`, { method: 'POST', signal: AbortSignal.timeout(3000) });
    console.log('HTTP', r.status, await r.text());
  } catch (e) { console.log('CLIENT ERROR', e.name, e.message); }
  srv.close(); setTimeout(() => process.exit(0), 50);
});
