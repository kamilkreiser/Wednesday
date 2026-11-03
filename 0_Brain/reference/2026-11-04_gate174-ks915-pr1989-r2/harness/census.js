// Gate 174 independent census: prints KEY NAMES (and counts) only, never a value.
// argv: FILE.json [MODE]  MODE=broad (default) | pin (the PR's regex, re-typed from the suite for comparison only)
const fs = require("fs"); const [f, mode = "broad"] = process.argv.slice(2);
const j = JSON.parse(fs.readFileSync(f, "utf8")); const k = new Map(); let nsvc = 0;
const nameRe = mode === "pin" ? /(DATABASE|POSTGRES|^PG|(^|_)DB($|_)|SQL|MONGO)/i : /(HOST|PORT|DB|DATABASE|^PG|PGB|POSTGRES|URL|URI|ADDR|DSN|SERVICE|CONN|SQL|MONGO|PRISMA|REPLICA|UPSTREAM)/i;
const valRe = mode === "pin" ? /^postgres(ql)?:\/\/|(^|\s)(host|hostaddr|dbname|service)=/i : /postgres|(^|\s)(host|hostaddr|dbname|service)=|:\/\/[^\s]*@|pgbouncer/i;
for (const [sn, s] of Object.entries(j.services || {})) { nsvc++; for (const [n, v] of Object.entries(s.environment || {})) { const x = String(v ?? "");
  if (nameRe.test(n) || valRe.test(x)) { const e = k.get(n) || { svc: 0, pgval: 0 }; e.svc++; if (/postgres|pgbouncer|host=/i.test(x)) e.pgval++; k.set(n, e); } } }
console.log("services " + nsvc);
for (const [n, e] of [...k].sort()) console.log(n + " svc=" + e.svc + " pg_like_values=" + e.pgval);
