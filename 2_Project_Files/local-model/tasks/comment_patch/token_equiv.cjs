#!/usr/bin/env node
// token_equiv.cjs — the comment_patch tier's lexical instrument (2026-09-17, HARNESS_WIDEN_PROPOSAL_2026-09-17b §3).
//
// Runs under a TypeScript package given BY PATH (the prepared clone's own node_modules/typescript, or the source
// checkout's for the builder's read-only self-check). Never a hand regex for code.
//
// WHY THE PARSER AND NOT A BARE `ts.createScanner` PASS: a raw scanner has no syntactic context. It reads the text after
// a `${...}` inside a template literal as identifiers and a `//` there as a COMMENT, and a regex literal such as `/\/\*/`
// as a slash followed by a comment opener — so a code edit inside either would hide as "trivia" and a token-equivalence
// gate built on it would PASS a code change. The parser drives the same scanner WITH context (reScanTemplateToken,
// reScanSlashToken). The token stream is every LEAF of the syntax tree (getChildren(), JSDoc nodes skipped — they are
// comments), and the text BETWEEN consecutive leaves is re-scanned and must be trivia only (whitespace, newlines,
// comments, a shebang). If a gap holds anything else the instrument cannot account for the file and says so (rc 3):
// fail closed, never a PASS.
//
// Modes (JSON on stdout):
//   compare <typescript dir> <before file> <after file> [<name for the script kind>]
//       → {equal, n_before, n_after, first_diff, parse_errors_before, parse_errors_after, directives_before, directives_after, ts_version}
//   lines   <typescript dir> <file> [<name>]
//       → {code_lines:[1-based lines any code token touches], n_lines, directives:[{line,text}], parse_errors, ts_version}
// rc 0 = measured (compare: equal or not is in the JSON) · 2 usage · 3 the instrument cannot account for a file.
'use strict';
const fs = require('fs');
const path = require('path');

function die(rc, msg) { process.stdout.write(JSON.stringify({ error: msg }) + '\n'); process.exit(rc); }
const [mode, tsDir, ...rest] = process.argv.slice(2);
if (!mode || !tsDir) die(2, 'usage: token_equiv.cjs compare|lines <typescript dir> <file(s)>');
let ts;
try { ts = require(path.resolve(tsDir)); } catch (e) { die(3, `typescript not loadable from ${tsDir}: ${e.message}`); }

function kindFor(name) {
  const n = name.toLowerCase();
  if (n.endsWith('.tsx')) return ts.ScriptKind.TSX;
  if (n.endsWith('.jsx')) return ts.ScriptKind.JSX;
  if (n.endsWith('.js') || n.endsWith('.mjs') || n.endsWith('.cjs')) return ts.ScriptKind.JS;
  return ts.ScriptKind.TS;
}

// A directive is a comment LINE whose content (after `//`, `/*`, `*`, `/` and whitespace) BEGINS with one of these.
// Line-start only: prose that merely mentions "eslint" is not a directive (TypeScript's own @ts-expect-error rule is
// line-start too).
const DIRECTIVE_RE = /^(@ts-(?:expect-error|ignore|nocheck|check)\b|eslint(?:-disable(?:-next-line|-line)?|-enable|-env)?\b|global\s|globals\s|<reference\b|<amd-|istanbul\s+ignore\b|c8\s+ignore\b|@[\w-]+-environment\b|prettier-ignore\b|@jsx\b|@jsxImportSource\b|@jsxFrag\b)/;
function directivesIn(commentText, startLine) {
  const out = [];
  commentText.split('\n').forEach((raw, i) => {
    let s = raw.replace(/\*\/\s*$/, '').replace(/^\s*(?:\/\*+|\/\/+|\*+)?\s*/, '');
    if (DIRECTIVE_RE.test(s)) out.push({ line: startLine + i, text: s.trim() });
  });
  return out;
}

function analyse(file, name) {
  const text = fs.readFileSync(file, 'utf8');
  const kind = kindFor(name || file);
  const sf = ts.createSourceFile(name || file, text, ts.ScriptTarget.Latest, /*setParentNodes*/ true, kind);
  const lineOf = (pos) => sf.getLineAndCharacterOfPosition(pos).line + 1;
  const leaves = [];
  const isJSDoc = (n) => n.kind >= ts.SyntaxKind.FirstJSDocNode && n.kind <= ts.SyntaxKind.LastJSDocNode;
  (function walk(node) {
    if (isJSDoc(node)) return;
    const kids = node.getChildren(sf);
    if (kids.length === 0) {
      if (node.kind === ts.SyntaxKind.SyntaxList) return; // an empty list carries no text
      leaves.push(node);
      return;
    }
    for (const k of kids) walk(k);
  })(sf);
  // gaps between leaves must be trivia only
  const scanner = ts.createScanner(ts.ScriptTarget.Latest, /*skipTrivia*/ false, kind === ts.ScriptKind.TSX || kind === ts.ScriptKind.JSX ? ts.LanguageVariant.JSX : ts.LanguageVariant.Standard);
  const TRIVIA = new Set([ts.SyntaxKind.WhitespaceTrivia, ts.SyntaxKind.NewLineTrivia, ts.SyntaxKind.SingleLineCommentTrivia,
    ts.SyntaxKind.MultiLineCommentTrivia, ts.SyntaxKind.ShebangTrivia, ts.SyntaxKind.ConflictMarkerTrivia]);
  const directives = [];
  const tokens = [];
  let prevEnd = 0;
  for (const leaf of leaves) {
    const start = leaf.kind === ts.SyntaxKind.EndOfFileToken ? leaf.getStart(sf) : leaf.getStart(sf);
    if (start < prevEnd) die(3, `${name || file}: overlapping leaves at ${lineOf(start)} (instrument cannot partition the file)`);
    const gap = text.slice(prevEnd, start);
    if (gap.length) {
      scanner.setText(text, prevEnd, start - prevEnd);
      let t;
      while ((t = scanner.scan()) !== ts.SyntaxKind.EndOfFileToken) {
        if (!TRIVIA.has(t)) die(3, `${name || file}: non-trivia ${ts.SyntaxKind[t]} ${JSON.stringify(scanner.getTokenText().slice(0, 40))} between syntax leaves at line ${lineOf(scanner.getTokenPos ? scanner.getTokenPos() : scanner.getTokenStart())} (instrument cannot account for it — fail closed)`);
        if (t === ts.SyntaxKind.SingleLineCommentTrivia || t === ts.SyntaxKind.MultiLineCommentTrivia) {
          const cpos = scanner.getTokenPos ? scanner.getTokenPos() : scanner.getTokenStart();
          directives.push(...directivesIn(scanner.getTokenText(), lineOf(cpos)));
        }
      }
    }
    if (leaf.kind !== ts.SyntaxKind.EndOfFileToken) {
      const end = leaf.getEnd();
      tokens.push({ kind: ts.SyntaxKind[leaf.kind], text: text.slice(start, end), line: lineOf(start), endLine: lineOf(Math.max(start, end - 1)) });
      prevEnd = end;
    } else {
      prevEnd = start;
    }
  }
  if (prevEnd < text.length) {
    // trailing text after EOF token start is impossible; guard anyway
    scanner.setText(text, prevEnd, text.length - prevEnd);
    let t;
    while ((t = scanner.scan()) !== ts.SyntaxKind.EndOfFileToken) {
      if (!TRIVIA.has(t)) die(3, `${name || file}: non-trivia after the last token (fail closed)`);
    }
  }
  const parseErrors = (sf.parseDiagnostics || []).map((d) => `${lineOf(d.start)}: ${ts.flattenDiagnosticMessageText(d.messageText, ' ')}`);
  return { tokens, directives, parseErrors, nLines: text.split('\n').length };
}

if (mode === 'lines') {
  const [file, name] = rest;
  if (!file) die(2, 'usage: lines <ts dir> <file> [name]');
  const a = analyse(file, name);
  const code = new Set();
  for (const t of a.tokens) for (let l = t.line; l <= t.endLine; l++) code.add(l);
  process.stdout.write(JSON.stringify({ code_lines: [...code].sort((x, y) => x - y), n_lines: a.nLines, n_tokens: a.tokens.length,
    directives: a.directives, parse_errors: a.parseErrors, ts_version: ts.version }) + '\n');
} else if (mode === 'compare') {
  const [bf, af, name] = rest;
  if (!bf || !af) die(2, 'usage: compare <ts dir> <before> <after> [name]');
  const b = analyse(bf, name || bf), a = analyse(af, name || af);
  let first = null;
  const n = Math.max(b.tokens.length, a.tokens.length);
  for (let i = 0; i < n; i++) {
    const x = b.tokens[i], y = a.tokens[i];
    if (!x || !y || x.kind !== y.kind || x.text !== y.text) {
      first = { index: i, before: x ? { kind: x.kind, text: x.text.slice(0, 80), line: x.line } : null, after: y ? { kind: y.kind, text: y.text.slice(0, 80), line: y.line } : null };
      break;
    }
  }
  const dk = (d) => d.map((x) => x.text).sort();
  process.stdout.write(JSON.stringify({ equal: first === null, n_before: b.tokens.length, n_after: a.tokens.length, first_diff: first,
    parse_errors_before: b.parseErrors, parse_errors_after: a.parseErrors,
    directives_before: b.directives, directives_after: a.directives,
    directives_equal: JSON.stringify(dk(b.directives)) === JSON.stringify(dk(a.directives)), ts_version: ts.version }) + '\n');
} else die(2, `unknown mode ${mode}`);
