#!/usr/bin/env node
// =============================================================================
// Static checks for the two test-estate HTML documents in `Projects Documents/` (KS-571, 2026-10-06)
// =============================================================================
// WHY: on 2026-10-06 the flow-diagrams and cheat-sheet pages were converted from prose to
// Topic | Detail table matrices, because long text laid out as flex rows rendered every
// inline node as its own column (Peter's screenshot). Nothing tested these pages before, and
// the conversion itself broke them three ways on its way to green — dropped text, merged
// words, comments turned into visible text — each caught only by hand. This pins the
// properties the pages must keep.
//
// Zero dependencies on purpose (systemTest/package.json carries none — KS-993). So this is a
// STATIC check, not a renderer: it cannot compute CSS, and it does not parse Mermaid with
// Mermaid. It checks what can be checked from the source; the browser render check stays a
// manual step (systemTest/CLAUDE.md, HTML visual check).
//
// Usage: node html_docs_check.mjs <file.html>...   → one `file: finding` line each; exit 1 if any.
// =============================================================================
import { readFileSync } from 'node:fs';

const VOID = new Set(['br', 'img', 'hr', 'meta', 'link', 'input', 'wbr', 'col', 'source', 'area', 'base']);
// Text inside these is not prose: diagrams, code, headings, existing tables, controls.
const OPAQUE_TAGS = new Set(['table', 'pre', 'script', 'style', 'svg', 'code', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'button', 'nav', 'label', 'title', 'head']);
const OPAQUE_CLASSES = new Set(['mermaid', 'ck-matrix', 'pmatrix']);
// Deliberately NOT converted on 2026-10-06, and named here so the choice is visible rather than
// silent: the cheat sheet's page subtitle, its status tiles (st-body, st-tag) and its colour-key
// legend descriptions (mode-desc). They are labels on a dashboard grid, not prose; Peter was told
// they were left as they are. Converting one later means deleting it from this set.
const LABEL_CLASSES = new Set(['subtitle', 'st-body', 'st-tag', 'mode-desc']);
// Elements that HOLD prose and therefore must sit inside a table after the conversion.
const PROSE_TAGS = new Set(['p', 'li']);
const PROSE_CLASSES = new Set(['note', 'ck-note', 'combo-row', 'pitfall-row', 'url-row']);
// Any visible run this long outside a table is prose, whatever its wrapper is called.
const LONG_TEXT = 160;
const MERMAID_START = /^(graph|flowchart|sequenceDiagram|classDiagram|stateDiagram(-v2)?|erDiagram|gantt|pie|journey|gitGraph|mindmap|timeline|quadrantChart|sankey-beta|xychart-beta|block-beta)\b/;
const PLACEHOLDER = /\bto be filled\b|\bPLACEHOLDER\b|\bTODO: fill\b/i;

const decode = (s) =>
    s
        .replace(/&nbsp;/g, ' ')
        .replace(/&(lt|gt|amp|quot|#39);/g, (_, e) => ({ lt: '<', gt: '>', amp: '&', quot: '"', '#39': "'" })[e])
        .replace(/&[a-z]+;|&#\d+;/gi, '·');

/** Tokenise just enough HTML to keep an ancestor stack: comments, raw-text blocks, tags, text. */
export function* tokens(html) {
    const re = /<!--[\s\S]*?-->|<(script|style)\b[^>]*>[\s\S]*?<\/\1\s*>|<\/?([a-zA-Z][\w-]*)([^>]*)>|[^<]+|</g;
    for (const m of html.matchAll(re)) {
        const raw = m[0];
        if (raw.startsWith('<!--')) yield { kind: 'comment', raw };
        else if (m[1]) yield { kind: 'raw', tag: m[1].toLowerCase(), raw };
        else if (m[2]) {
            const cls = /\bclass\s*=\s*"([^"]*)"/.exec(m[3] || '');
            yield { kind: raw.startsWith('</') ? 'close' : 'open', tag: m[2].toLowerCase(), classes: cls ? cls[1].split(/\s+/) : [], selfClosing: /\/\s*>$/.test(raw), raw };
        } else yield { kind: 'text', raw };
    }
}

export function check(html) {
    const findings = [];
    const stack = [];
    const opaque = () =>
        stack.some((e) => OPAQUE_TAGS.has(e.tag) || e.classes.some((c) => OPAQUE_CLASSES.has(c) || LABEL_CLASSES.has(c)));
    const proseHolder = () => stack.find((e) => PROSE_TAGS.has(e.tag) || e.classes.some((c) => PROSE_CLASSES.has(c)));
    let mermaid = null;
    const reported = new Set();
    let ckItem = null;
    for (const t of tokens(html)) {
        if (t.kind === 'open') {
            if (VOID.has(t.tag) || t.selfClosing) continue;
            stack.push(t);
            if (t.classes.includes('mermaid')) mermaid = { text: '' };
            if (t.classes.includes('ck-item')) ckItem = { text: '' };
        } else if (t.kind === 'close') {
            const i = stack.map((e) => e.tag).lastIndexOf(t.tag);
            if (i < 0) continue;
            const closed = stack.splice(i);
            if (mermaid && closed.some((e) => e.classes.includes('mermaid'))) {
                findings.push(...checkMermaid(decode(mermaid.text)));
                mermaid = null;
            }
            if (ckItem && closed.some((e) => e.classes.includes('ck-item'))) {
                // The exact 2026-10-06 defect: a long entry in a flex `ck-item` splits into columns.
                const len = ckItem.text.replace(/\s+/g, ' ').trim().length;
                if (len > 120) findings.push(`long text (${len} chars) in a flex .ck-item renders as columns — use a table`);
                ckItem = null;
            }
        } else if (t.kind === 'text') {
            if (mermaid) { mermaid.text += t.raw; continue; }
            if (ckItem) ckItem.text += decode(t.raw);
            const text = decode(t.raw).replace(/\s+/g, ' ').trim();
            if (!text || opaque()) continue;
            if (PLACEHOLDER.test(text)) findings.push(`placeholder text left: "${text.slice(0, 60)}"`);
            const holder = proseHolder();
            const where = holder ? `<${holder.tag}${holder.classes.length ? '.' + holder.classes.join('.') : ''}>` : null;
            if (holder && !reported.has(holder)) {
                reported.add(holder);
                findings.push(`prose outside a table in ${where}: "${text.slice(0, 60)}"`);
            } else if (!holder && text.length >= LONG_TEXT) {
                findings.push(`long text outside a table: "${text.slice(0, 60)}"`);
            }
        }
    }
    return findings;
}

/** Structural Mermaid check — a known diagram type and balanced brackets/quotes. Not a full parse. */
export function checkMermaid(src) {
    const body = src.replace(/^\s*%%.*$/gm, '').trim();
    const out = [];
    if (!MERMAID_START.test(body)) out.push(`mermaid block does not start with a diagram type: "${body.slice(0, 40)}"`);
    const unquoted = body.replace(/"[^"\n]*"/g, '""');
    if ((unquoted.match(/"/g) || []).length % 2) out.push(`mermaid block has an unbalanced quote near "${body.slice(0, 40)}"`);
    for (const [o, c] of [['[', ']'], ['(', ')'], ['{', '}']]) {
        const n = (s) => unquoted.split(s).length - 1;
        if (n(o) !== n(c)) out.push(`mermaid block has unbalanced ${o}${c} (${n(o)} vs ${n(c)}) near "${body.slice(0, 40)}"`);
    }
    return out;
}

if (import.meta.url === `file://${process.argv[1]}`) {
    let bad = 0;
    for (const file of process.argv.slice(2)) {
        for (const f of check(readFileSync(file, 'utf8'))) {
            console.log(`${file}: ${f}`);
            bad++;
        }
    }
    process.exit(bad ? 1 : 0);
}
