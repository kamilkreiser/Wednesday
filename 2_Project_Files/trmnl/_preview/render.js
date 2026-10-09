// render.js — APPROXIMATE local preview, NOT the official renderer.
// Liquid engine: liquidjs (TRMNL renders with Ruby Liquid + its own filters; markup.liquid
// uses no TRMNL filters, so plain Liquid semantics apply). Page shell: copied from the
// official trmnlp web/views/render_html.erb (github.com/usetrmnl/trmnlp), with the official
// framework 3.4.0 CSS/JS from https://trmnl.com/css/3.4.0/plugins.css and /js/3.4.0/plugins.js.
// Usage: node render.js <markup.liquid> <payload.json> <out.html> [screen classes]
const fs = require("fs");
const path = require("path");
const { Liquid } = require(path.join(__dirname, "node_modules", "liquidjs"));
const [markupPath, payloadPath, outPath, screen = "screen screen--og screen--1bit"] = process.argv.slice(2);
if (!markupPath || !payloadPath || !outPath) {
  console.error("usage: node render.js <markup.liquid> <payload.json> <out.html> [screen classes]");
  process.exit(2);
}
const vars = JSON.parse(fs.readFileSync(payloadPath, "utf8")).merge_variables;
const engine = new Liquid({ strictVariables: true, strictFilters: true });
const body = engine.parseAndRenderSync(fs.readFileSync(markupPath, "utf8"), vars);
const page = `<!DOCTYPE html>
<html><head>
<script>window.I18n = { andXMore: (c) => "and " + c + " more" };</script>
<link rel="stylesheet" href="https://trmnl.com/css/3.4.0/plugins.css" />
<script type="module" src="https://trmnl.com/js/3.4.0/plugins.js"></script>
<link href="https://fonts.googleapis.com/css2?family=Inter:ital,opsz,wght@0,14..32,100..900;1,14..32,100..900&display=swap" rel="stylesheet">
</head>
<body class="environment trmnl">
  <div class="${screen}">
    <div class="view view--full">
${body}
    </div>
  </div>
</body></html>`;
fs.writeFileSync(outPath, page);
console.log("wrote " + outPath + " (" + page.length + " bytes)");
