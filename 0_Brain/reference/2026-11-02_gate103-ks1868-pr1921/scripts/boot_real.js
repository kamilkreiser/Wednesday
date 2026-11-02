// Real `node` process boot of services/kyc/src/index.ts via tsx, only pg replaced (boot_preload.cjs). Per kind:
// exit code / still alive after 8 s, and the stdout/stderr lines naming the probe.
const { spawn } = require('child_process'); const fs = require('fs');
const G = '/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate103-ks1868-pr1921';
const A = G + '/repo/Blockchain/Dev/services/kyc';
const label = process.argv[2];
const SCR = '/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/6737ee07-39e0-4a0c-b588-61b97461401d/scratchpad/gate103_bootcwd';
fs.mkdirSync(SCR, { recursive: true });
const kinds = ['none', 'ordinary', 'string', 'plainObject', 'revokedProxy', 'throwingGetter'];
(async () => {
  for (const kind of kinds) {
    const env = { PATH: process.env.PATH, HOME: process.env.HOME, NODE_ENV: 'development', KYC_PROVIDER: 'mock', PORT: '0',
      DATABASE_URL: 'postgres://gate103:stub@127.0.0.1:1/gate103', PII_ENCRYPTION_KEY: 'ab'.repeat(32), BOOT_KIND: kind,
      NODE_OPTIONS: `--require ${G}/scripts/boot_preload.cjs`, TMPDIR: SCR };
    const p = spawn(process.execPath, ['--import', 'file://' + G + '/repo/Blockchain/Dev/node_modules/tsx/dist/loader.mjs', A + '/src/index.ts'], { cwd: SCR, env });
    let out = ''; p.stdout.on('data', (d) => (out += d)); p.stderr.on('data', (d) => (out += d));
    const res = await new Promise((resolve) => {
      const t = setTimeout(() => { p.kill('SIGTERM'); resolve({ alive8s: true, code: null }); }, 8000);
      p.on('exit', (code, sig) => { clearTimeout(t); resolve({ alive8s: false, code, sig }); });
    });
    await new Promise((r) => setTimeout(r, 300));
    const lines = out.split('\n').map((l) => l.replace(/\u001b\[[0-9;]*m/g, ''));
    const pick = lines.filter((l) => /KYC DB|GATE103|Unhandled|unhandled|TypeError|KYC Service started|DB init/.test(l)).map((l) => l.replace(/^\d{4}-\d\d-\d\d \d\d:\d\d:\d\d\.\d+ /, '').slice(0, 220));
    const rec = { version: label, kind, ...res, lines: pick };
    fs.appendFileSync(`${G}/logs/boot_real_${label}.jsonl`, JSON.stringify(rec) + '\n');
    fs.writeFileSync(`${G}/logs/boot_real_${label}_${kind}.out`, out);
    console.log(JSON.stringify(rec));
  }
})();
