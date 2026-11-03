// Gate 174 classifier (gate 173's, plus MARKER_IN=<keys>: any other key whose value carries the remote marker): prints LABELS only, never a value.
// argv: MODE NM MARKER [FILE]. MODE dotenv FILE | bashvals (stdin NUL fields DATABASE_URL NODE_ENV PGHOST PGHOSTADDR PGSERVICE POSTGRES_HOST)
// | compose (stdin = docker compose config json) ; output e.g. "DB=REMOTE NE=PRODUCTION PGB=REMOTE"
const [mode, nm, marker, file] = process.argv.slice(2);
const pg = require(nm + "/pg-connection-string");
const hostOf = (u) => { try { const c = pg.parse(u); return [c.host, c.hostaddr, c.service].map(String).join("|"); } catch (e) { return "THROWS"; } };
const rem = (s) => (s != null && String(s).includes(marker));
function cls(env) {
  let db = "local", ne = (env.NODE_ENV != null && String(env.NODE_ENV).trim().toLowerCase() === "production") ? "PRODUCTION" : "other";
  for (const [k, v] of Object.entries(env)) if (/DATABASE_URL$/.test(k) && v) if (rem(hostOf(String(v)))) db = "REMOTE";
  const pgh = ["PGHOST", "PGHOSTADDR", "PGSERVICE"].some((k) => rem(env[k])) ? "REMOTE" : "local";
  const pgb = rem(env.POSTGRES_HOST) ? "REMOTE" : "local";
  const other = Object.entries(env).filter(([k, v]) => k !== "POSTGRES_HOST" && !/DATABASE_URL$/.test(k) && !/^PG(HOST|HOSTADDR|SERVICE)$/.test(k) && rem(v)).map(([k]) => k).sort();
  return `DB=${db} NE=${ne} PG*=${pgh} POSTGRES_HOST=${pgb}` + (other.length ? " MARKER_IN=" + other.join("+") : "");
}
if (mode === "dotenv") { const d = require(nm + "/dotenv"); console.log(cls(d.parse(require("fs").readFileSync(file)))); process.exit(0); }
const ch = []; process.stdin.on("data", (d) => ch.push(d)).on("end", () => {
  const b = Buffer.concat(ch).toString("utf8");
  if (mode === "bashvals") { const f = b.split("\0"); const env = {}; ["DATABASE_URL","NODE_ENV","PGHOST","PGHOSTADDR","PGSERVICE","POSTGRES_HOST"].forEach((k,i)=>env[k]=f[i]); console.log(cls(env)); return; }
  if (mode === "compose") {
    let j; try { j = JSON.parse(b); } catch (e) { console.log("compose=ERR(no json)"); return; }
    const hits = new Set(); for (const [n, s] of Object.entries(j.services || {})) { const c = cls(s.environment || {}); for (const p of c.split(" ")) if (/REMOTE|PRODUCTION/.test(p)) hits.add(p.split("=")[0] + "@" + n); }
    console.log(hits.size ? "compose:" + [...hits].sort().join(",") : "compose:all-local"); return; }
});
