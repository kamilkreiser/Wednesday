#!/bin/bash
# md2pdf.sh — render a Markdown report to a well-structured A4 PDF in the house style.
#
# WHY (Kam, 2026-08-28 09:51, verbatim in the prompt log): "The PDF looks great.
# Keep this style going forward." A style kept in memory lapses; a style kept in
# a script does not. Same seam as speak.sh: change the look here, everywhere follows.
#
# Pipeline: pandoc (gfm → html5, CSS embedded) → headless Google Chrome print-to-pdf.
# Conventions the CSS keys on: the file's own `# H1` is the title (pandoc's title
# block is hidden); `## BLUF` gets a callout; any `## Sources…` heading starts a new
# page in smaller type. Never discards stderr.
#
# Usage: md2pdf.sh <input.md> [output.pdf]     (default: same name, .pdf, beside it)
# Exit: 0 rendered + page count printed · 1 render failed · 2 usage/tool missing
set -uo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
IN="${1:-}"; [ -f "$IN" ] || { echo "md2pdf: usage: md2pdf.sh <input.md> [output.pdf]" >&2; exit 2; }
OUT="${2:-${IN%.md}.pdf}"
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
command -v pandoc >/dev/null || { echo "md2pdf: pandoc missing (brew install pandoc)" >&2; exit 2; }
[ -x "$CHROME" ] || { echo "md2pdf: Google Chrome not found at $CHROME" >&2; exit 2; }
TMP="$(mktemp -d)"; trap 'rm -rf "$TMP"' EXIT
pandoc "$IN" -f gfm -t html5 -s --metadata title="$(basename "${IN%.md}")" --css "$HERE/report.css" --embed-resources -o "$TMP/report.html" || { echo "md2pdf: pandoc failed" >&2; exit 1; }
sed -i '' 's#<header id="title-block-header">#<header id="title-block-header" style="display:none">#' "$TMP/report.html"
OUT_ABS="$(cd "$(dirname "$OUT")" && pwd)/$(basename "$OUT")"
"$CHROME" --headless=new --disable-gpu --no-sandbox --no-pdf-header-footer --print-to-pdf="$OUT_ABS" "file://$TMP/report.html" >"$TMP/chrome.log" 2>&1 || { echo "md2pdf: chrome failed:" >&2; cat "$TMP/chrome.log" >&2; exit 1; }
[ -s "$OUT_ABS" ] || { echo "md2pdf: no output produced" >&2; cat "$TMP/chrome.log" >&2; exit 1; }
PAGES=$(python3 -c 'import re,sys; print(len(re.findall(rb"/Type\s*/Page[^s]", open(sys.argv[1],"rb").read())))' "$OUT_ABS")
echo "rendered: $OUT_ABS ($PAGES pages, $(stat -f %z "$OUT_ABS") bytes) — eyeball a page before delivering (pdftoppm -r 70 -png)"
