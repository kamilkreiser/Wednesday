// stdin: compose config json of the ROOT entry; argv: NM devEnvFile. Says whether root-entry auth ADMIN equals dev .env's
// (dotenv read) and whether ALLOW is exactly "true" — never a value.
const [nm, f] = process.argv.slice(2); const d = require(nm + "/dotenv"); const c = require("crypto");
const h = (s) => c.createHash("sha256").update(String(s ?? "")).digest("hex");
const ch = []; process.stdin.on("data", (x) => ch.push(x)).on("end", () => {
  let j; try { j = JSON.parse(Buffer.concat(ch).toString()); } catch (e) { console.log("root-entry: ERR"); return; }
  const a = ((j.services || {}).auth || {}).environment || {}; const dv = d.parse(require("fs").readFileSync(f)).ADMIN_USER_PASSWORD;
  console.log("root-entry auth ADMIN " + (a.ADMIN_USER_PASSWORD ? "set" : "blank") + "; equals dev .env ADMIN: " + (h(a.ADMIN_USER_PASSWORD) === h(dv) ? "yes" : "NO") + "; ALLOW exact-true: " + (a.ALLOW_DEFAULT_SEED_PASSWORDS === "true" ? "yes" : "NO"));
});
