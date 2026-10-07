#!/usr/bin/env bash
# =============================================================================
# The two test-estate HTML documents keep their table-matrix form (KS-571, 2026-10-06)
# =============================================================================
# THE DEFECT: `Projects Documents/API_Security_Functional_Testing_Architecture_Flow_Diagrams.html`
# laid long gate descriptions out as flex rows (`.ck-item`), so every bold word, code span and
# text run rendered as its own column — unreadable (Peter's screenshot, 2026-10-06). Both pages
# were then converted to Topic | Detail matrices. Nothing tested either page, and the
# conversion broke them three ways before it was right (dropped text, merged words, comments
# made visible), each caught by hand.
#
# THE RULE (support/html_docs_check.mjs): no prose (<p>, <li>, notes, combo/pitfall/url rows,
# or any long text run) outside a table; no long text in a flex `.ck-item`; every Mermaid block
# starts with a diagram type and balances its brackets and quotes; no placeholder text.
#
# STATIC ONLY: it does not render CSS or run Mermaid (systemTest carries no dependencies —
# KS-993). The browser render check is still a manual step.
#
# Positive controls plant each defect in a scratch page and require a finding, so a checker
# that stopped looking cannot pass.
# =============================================================================

set -uo pipefail

SELF_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SELF_DIR/../.." && pwd)"
CHECK="$SELF_DIR/support/html_docs_check.mjs"
DOCS=(
    "$REPO_ROOT/Projects Documents/API_Security_Functional_Testing_Architecture_Flow_Diagrams.html"
    "$REPO_ROOT/Projects Documents/QA_Tool_Cheat_Sheet_Secuura_API_Testing.html"
)
pass=0
fail=0
ok() { echo "  ok   $1"; pass=$((pass + 1)); }
bad() { echo "  FAIL $1"; fail=$((fail + 1)); }

SCRATCH="$(mktemp -d)"
trap 'rm -rf "$SCRATCH"' EXIT

echo "== html_docs_matrix"

# 1. The real documents pass.
for doc in "${DOCS[@]}"; do
    name="$(basename "$doc")"
    if [[ ! -f "$doc" ]]; then
        bad "$name is missing"
        continue
    fi
    if out="$(node "$CHECK" "$doc" 2>&1)"; then
        ok "$name has no prose outside a table, sane Mermaid, no placeholders"
    else
        bad "$name:"
        printf '%s\n' "$out" | sed 's/^/         /'
    fi
done

# 2. Positive controls — each planted defect must be reported.
# expect_finding <label> <grep-pattern> <html>
expect_finding() {
    local label="$1" pattern="$2" html="$3" f="$SCRATCH/page.html" out
    printf '<html><head><title>t</title></head><body>%s</body></html>\n' "$html" >"$f"
    out="$(node "$CHECK" "$f" 2>&1)"
    if [[ $? -ne 0 ]] && grep -q -- "$pattern" <<<"$out"; then
        ok "control: $label is reported"
    else
        bad "control: $label was NOT reported (got: ${out:-nothing})"
    fi
}

expect_finding "a bare paragraph" "prose outside a table in <p>" \
    '<p><strong>Lead.</strong> A sentence of prose that should sit in a matrix.</p>'
expect_finding "a list item" "prose outside a table in <li>" \
    '<ul><li>One bullet of prose outside any table.</li></ul>'
expect_finding "a note" "prose outside a table in <div.note>" \
    '<div class="note">A callout written as running text.</div>'
expect_finding "a combo row" "prose outside a table in <div.combo-row>" \
    '<div class="combo-row"><span class="combo-tools">A</span><span class="combo-desc">B does C.</span></div>'
expect_finding "long text in a flex ck-item (the screenshot defect)" "flex .ck-item" \
    "<div class=\"ck-row\"><div class=\"ck-item\"><span class=\"ck-sw ck-live\"></span><strong>Gate</strong> — $(printf 'word %.0s' {1..40})</div></div>"
expect_finding "a long unwrapped text run" "long text outside a table" \
    "<div>$(printf 'prose %.0s' {1..40})</div>"
expect_finding "a placeholder row" "placeholder text left" \
    '<table><tr><td>x</td></tr></table><span>to be filled from the final run</span>'
expect_finding "a mermaid block with no diagram type" "does not start with a diagram type" \
    '<div class="mermaid">A --> B</div>'
expect_finding "a mermaid block with an unbalanced bracket" "unbalanced \[\]" \
    '<div class="mermaid">graph TD\n A[Start --> B[End]</div>'

# 3. Negative control — a correct page reports nothing.
printf '%s\n' '<html><body><h2>Heading text is fine</h2><table class="pmatrix"><tr><td class="pm-topic"><strong>Lead.</strong></td><td>Detail sentence.</td></tr></table><div class="mermaid">graph TD
 A["Start (x)"] --> B{ok?}</div><pre>long code '"$(printf 'x %.0s' {1..100})"'</pre></body></html>' >"$SCRATCH/clean.html"
if out="$(node "$CHECK" "$SCRATCH/clean.html" 2>&1)"; then
    ok "control: a correct page reports nothing"
else
    bad "control: a correct page was flagged: $out"
fi

echo "  $pass passed, $fail failed"
[[ $fail -eq 0 ]]
