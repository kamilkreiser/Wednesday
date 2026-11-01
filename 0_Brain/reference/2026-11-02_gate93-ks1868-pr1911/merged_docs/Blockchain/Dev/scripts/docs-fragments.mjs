#!/usr/bin/env node
/**
 * DOCS FRAGMENTS: one small file per entry, one step builds the two pages (KS-1887)
 * =============================================================================
 * THE DEFECT: every PR that changes tests appended a numbered section to each of the
 * two shared pages in `Projects Documents/`. Every merge took the next number, so every
 * other open PR went DIRTY on those two files alone, and each needed a docs-only
 * merge-in plus a ~15-20 minute push through the serial push queue. Measured on
 * 2026-10-31: 44 open PRs, 28 of them appending to both pages, all 28 DIRTY.
 *
 * THE SHAPE (Kam, 2026-10-31 09:44:40, card secuura-docs-section-collision-dirties-every-pr-1030):
 * each PR adds its own small fragment file; this one step renders the two pages.
 *
 *   Projects Documents/fragments/<flow|cheat>/
 *     head.html              everything before the first entry (fixed)
 *     tail.html              the closing lines (fixed)
 *     legacy/NNNN-<slug>.html  the entries that existed when this was introduced: FROZEN, raw,
 *                            literal numbers, in the page's own order (which is not number order:
 *                            the Flow page has gaps at 17, 32-34 and six backward pairs)
 *     KS-NNNN-<slug>.html    one NEW entry. Raw HTML, no header; the ticket key and slug are the name.
 *
 * Flow fragments carry two tokens instead of a number:  <!--n-->  is this entry's section number
 * (in the <h2> and in <h3> N.M), and  <!--ref:KS-NNNN-slug-->  is another new entry's number.
 * The Cheat Sheet is unnumbered, so its fragments are plain HTML.
 *
 * ORDER AND NUMBERS: new entries are ordered by the commit that FIRST added them, in
 * `git rev-list --first-parent --reverse HEAD` (develop is squash-merged, so that is merge order);
 * ties inside one commit go by file name; a not-yet-committed fragment sorts last. A new Flow entry's
 * number is (highest literal number in head + legacy) + its rank. Numbers are provisional on a branch
 * and final once merged, because a later merge only appends.
 *
 * WHO WRITES THE PAGES: PRs commit fragments ONLY. If every PR also rebuilt the two pages, two PRs
 * would both append at the end of each page and conflict again. The committed pages are refreshed by
 * one separate step (`build --base <develop sha>`), so they may LAG the fragments between refreshes.
 *
 * Usage (paths relative to the repo root; --root DIR points elsewhere, --html-check FILE overrides the checker):
 *   node Blockchain/Dev/scripts/docs-fragments.mjs check [--committed]
 *   node Blockchain/Dev/scripts/docs-fragments.mjs build --base <40-hex develop sha>
 *   node Blockchain/Dev/scripts/docs-fragments.mjs build --out DIR          (a preview; touches no committed page)
 *   node Blockchain/Dev/scripts/docs-fragments.mjs adopt [--from-ref REF [--against DEVELOP_SHA]]   (absorb a hand-appended entry)
 *   node Blockchain/Dev/scripts/docs-fragments.mjs legacy-hash              (sha256 of head + legacy + tail, per page)
 *
 * check            HARD: fragment lint (name, tag balance, tokens, one entry per file, no literal numbers in a
 *                  new Flow entry, legacy files carry no tokens) and the rendered pages passing
 *                  systemTest/__tests__/support/html_docs_check.mjs (called, never copied or edited).
 *                  ADVISORY: how the committed page relates to the render (current, lagging, hand-appended,
 *                  edited), printed loudly and exit 0 (Wednesday's ruling A1: a hand edit by an author outside
 *                  our seats must not stop every seat's push).
 * check --committed  the same, and additionally exit 1 unless both committed pages are current.
 * adopt            turns an entry hand-appended to a committed page (after the last rendered entry) into a
 *                  new fragment, with its number turned into the tokens, and says what number it will render
 *                  as. --from-ref REF reads the page from that commit instead of the working tree. Add
 *                  --against DEVELOP_SHA and it takes what the PR appended since its OWN merge-base with that
 *                  develop (the PR transition: a PR's page is stale, so comparing it with today's render would
 *                  see other PRs' edits as the PR's). An entry whose heading already exists, with the same text
 *                  apart from its number, is skipped as already there (a stacked PR repeats its base's entries).
 *
 * Exit 0 = fine, 1 = a finding (or, with --committed, a page that is not current), 2 = cannot run
 * (usage, no git, shallow clone, a committed fragment with no add commit). "0 ordered" is never a pass.
 * Deterministic: no timestamps, no network, no dependencies.
 */

import { spawnSync } from 'node:child_process';
import { createHash } from 'node:crypto';
import { existsSync, mkdirSync, mkdtempSync, readFileSync, readdirSync, rmSync, statSync, writeFileSync } from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const DEFAULT_ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../../..');
const FRAG_DIR = 'Projects Documents/fragments';
const PAGES = {
    flow: { page: 'Projects Documents/API_Security_Functional_Testing_Architecture_Flow_Diagrams.html', numbered: true },
    cheat: { page: 'Projects Documents/QA_Tool_Cheat_Sheet_Secuura_API_Testing.html', numbered: false },
};
// A new fragment is named by its ticket key plus a slug. The key alone is NOT unique: 11 keys appear in more
// than one Cheat Sheet heading and three open PRs share KS-1410. `adopted-` is for a hand entry with no key.
const NAME_RE = /^(?:[A-Z]{2,4}-\d+|adopted)-[a-z0-9][a-z0-9-]{0,80}\.html$/;
const LEGACY_RE = /^(\d{4})-[a-z0-9][a-z0-9-]*\.html$/;
// A single-line comment, or a bare wrapper-open line, directly above an <h2> belongs to that entry. Without
// this rule 11 of the 111 Cheat Sheet entries are unbalanced on their own (the wrapper straddles entries).
const LEAD_RE = /^(\s*<!--.*-->\s*|<div class="section">\s*)$/;
const COMMENT_RE = /<!--[\s\S]*?-->/g;
const TAGS = ['table', 'tr', 'td', 'th', 'tbody', 'thead', 'pre', 'div', 'ul', 'ol', 'li', 'details', 'summary',
    'h2', 'h3', 'code', 'strong', 'em', 'a', 'span', 'p'];
const TAG_COUNTERS = TAGS.map((t) => ({ t, open: new RegExp(`<${t}(?=[\\s>/])`, 'g'), close: new RegExp(`</${t}>`, 'g') }));
const GIT_ENV_DROP = ['GIT_DIR', 'GIT_WORK_TREE', 'GIT_INDEX_FILE', 'GIT_COMMON_DIR', 'GIT_PREFIX'];

class Refusal extends Error {}
const refuse = (msg) => { throw new Refusal(msg); };
const sha256 = (s) => createHash('sha256').update(Buffer.from(s, 'utf8')).digest('hex');
const count = (s, re) => (s.match(re) || []).length;

// --- arguments -------------------------------------------------------------
function parseArgs(argv) {
    const [cmd, ...rest] = argv;
    const o = { cmd, root: DEFAULT_ROOT, committed: false, base: null, out: null, fromRef: null, against: null, htmlCheck: null };
    for (let i = 0; i < rest.length; i++) {
        const a = rest[i];
        const value = () => { if (i + 1 >= rest.length) refuse(`${a} needs a value`); return rest[++i]; };
        if (a === '--root') o.root = path.resolve(value());
        else if (a === '--committed') o.committed = true;
        else if (a === '--base') o.base = value();
        else if (a === '--out') o.out = path.resolve(value());
        else if (a === '--from-ref') {
            o.fromRef = value();
            // it becomes the front of a `git show <ref>:<path>` argument, so a value that looks like an option is refused
            if (o.fromRef.startsWith('-')) refuse('--from-ref must be a commit, tag or branch name, not an option');
        }
        else if (a === '--against') {
            o.against = value();
            if (o.against.startsWith('-')) refuse('--against must be a commit, tag or branch name, not an option');
        }
        else if (a === '--html-check') o.htmlCheck = path.resolve(value());
        else refuse(`unknown argument ${a}`);
    }
    return o;
}

// --- git (never inherits the caller's repository environment) ----------------
function git(root, args, { allowFail = false } = {}) {
    const env = { ...process.env };
    for (const k of GIT_ENV_DROP) delete env[k];
    const r = spawnSync('git', ['-C', root, '-c', 'core.quotePath=false', ...args], { encoding: 'utf8', env, maxBuffer: 512 * 1024 * 1024 });
    if (r.error) refuse(`cannot run git: ${r.error.message}`);
    if (r.status !== 0 && !allowFail) refuse(`git ${args.join(' ')} failed: ${(r.stderr || '').trim().split('\n')[0]}`);
    return { status: r.status, out: r.stdout || '' };
}

// --- loading ----------------------------------------------------------------
const readText = (p) => readFileSync(p, 'utf8');
const listDir = (d) => (existsSync(d) ? readdirSync(d).sort() : null);

function loadPage(root, key) {
    const rel = `${FRAG_DIR}/${key}`;
    const dir = path.join(root, rel);
    const findings = [];
    const add = (file, msg) => findings.push(`${file}: ${msg}`);
    const p = { key, ...PAGES[key], rel, dir, findings, add, head: '', tail: '', legacy: [], fresh: [] };
    if (!existsSync(dir)) { add(rel, 'the fragment directory is missing'); return p; }
    for (const part of ['head', 'tail']) {
        const fp = path.join(dir, `${part}.html`);
        if (existsSync(fp)) p[part] = readText(fp); else add(`${rel}/${part}.html`, 'is missing');
    }
    const lnames = listDir(path.join(dir, 'legacy'));
    if (lnames === null) add(`${rel}/legacy`, 'the legacy directory is missing');
    (lnames || []).forEach((name, i) => {
        const lrel = `${rel}/legacy/${name}`;
        const m = LEGACY_RE.exec(name);
        if (!m) { add(lrel, 'is not a legacy file name (NNNN-slug.html)'); return; }
        if (Number(m[1]) !== i + 1) add(lrel, `legacy numbering has a gap or a duplicate (expected ${String(i + 1).padStart(4, '0')})`);
        p.legacy.push({ name, rel: lrel, text: readText(path.join(dir, 'legacy', name)) });
    });
    for (const name of listDir(dir) || []) {
        if (['head.html', 'tail.html', 'legacy'].includes(name)) continue;
        const frel = `${rel}/${name}`;
        if (!NAME_RE.test(name) || !statSync(path.join(dir, name)).isFile()) { add(frel, 'is not a fragment name (KS-NNNN-slug.html, or adopted-slug.html)'); continue; }
        p.fresh.push({ name, base: name.replace(/\.html$/, ''), rel: frel, text: readText(path.join(dir, name)) });
    }
    return p;
}

// --- lint ---------------------------------------------------------------------
function unbalanced(text) {
    const t = text.replace(COMMENT_RE, '');
    const bad = [];
    for (const { t: tag, open, close } of TAG_COUNTERS) {
        const o = count(t, open), c = count(t, close);
        if (o !== c) bad.push(`<${tag}> opened ${o}, closed ${c}`);
    }
    return bad.join('; ');
}

const innerText = (html) => html.replace(COMMENT_RE, '').replace(/<[^>]+>/g, '').replace(/\s+/g, ' ').trim();

function lintOne(p, item, kind, flowBases) {
    const { add } = p;
    const t = item.text;
    if (kind !== 'head' && kind !== 'tail' && t === '') add(item.rel, 'is empty');
    if (t.includes('\r')) add(item.rel, 'contains a carriage return (LF line ends only)');
    if (t !== '' && !t.endsWith('\n')) add(item.rel, 'does not end with a newline');
    const bad = unbalanced(t);
    if (bad) add(item.rel, `tags are not balanced: ${bad}`);
    const nTokens = count(t, /<!--n-->/g);
    const refs = [...t.matchAll(/<!--ref:([^>\s]*?)-->/g)].map((m) => m[1]);
    if (kind !== 'fresh' || !p.numbered) {
        if (nTokens || refs.length) add(item.rel, 'carries a number token (<!--n--> or <!--ref:...-->), which only a new Flow fragment may');
        if (kind !== 'fresh') return;
    }
    // a NEW fragment: exactly one entry, starting with its <h2>
    if (count(t.replace(COMMENT_RE, ''), /<h2\b/g) !== 1) add(item.rel, 'must hold exactly one entry (one <h2>)');
    const lines = t.split('\n');
    let i = 0;
    while (i < lines.length && LEAD_RE.test(lines[i])) i++;
    if (!(lines[i] || '').startsWith('<h2')) add(item.rel, 'must start with the <h2> of its entry (a single-line comment or a <div class="section"> line may sit above it)');
    if (!p.numbered) return;
    const h2 = /<h2\b[^>]*>([\s\S]*?)<\/h2>/.exec(t);
    if (h2 && !/^\s*<!--n-->\.\s*\S/.test(h2[1])) add(item.rel, 'the <h2> must start with <!--n-->. (the build numbers new entries)');
    // a copied-over "127.1 ..." would print a number that is not this entry's; the token comment is removed first
    for (const m of t.matchAll(/<h[23]\b[^>]*>([\s\S]*?)<\/h[23]>/g)) {
        if (/^\s*\d+\./.test(m[1].replace(COMMENT_RE, ''))) add(item.rel, `heading "${innerText(m[1]).slice(0, 40)}" carries a literal section number; write <!--n-->. instead`);
    }
    for (const r of refs) if (!flowBases.has(r)) add(item.rel, `<!--ref:${r}--> names no new Flow fragment`);
}

function lintPage(p, flowBases) {
    lintOne(p, { rel: `${p.rel}/head.html`, text: p.head }, 'head', flowBases);
    lintOne(p, { rel: `${p.rel}/tail.html`, text: p.tail }, 'tail', flowBases);
    for (const l of p.legacy) lintOne(p, l, 'legacy', flowBases);
    for (const f of p.fresh) lintOne(p, f, 'fresh', flowBases);
}

// --- ordering, numbering, rendering ------------------------------------------
function orderFresh(root, pages) {
    const all = pages.flatMap((p) => p.fresh);
    if (all.length === 0) return;
    const inside = git(root, ['rev-parse', '--is-inside-work-tree'], { allowFail: true });
    if (inside.status !== 0 || inside.out.trim() !== 'true') refuse('not a git work tree: new fragments are ordered by the commit that added them');
    if (git(root, ['rev-parse', '--is-shallow-repository']).out.trim() === 'true') refuse('shallow clone: the commit that added each fragment is not all here (fetch the full history)');
    const rank = new Map(), tracked = new Set(), added = new Map();
    if (git(root, ['rev-parse', '--verify', '--quiet', 'HEAD'], { allowFail: true }).status === 0) {
        git(root, ['rev-list', '--first-parent', '--reverse', 'HEAD']).out.split('\n').filter(Boolean).forEach((sha, i) => rank.set(sha, i));
        const dirs = pages.map((p) => p.rel);
        for (const f of git(root, ['ls-tree', '-r', '--name-only', 'HEAD', '--', ...dirs]).out.split('\n')) if (f) tracked.add(f);
        let cur = null;
        // newest first, so the last write for a path is the OLDEST add: that is the first-add commit
        for (const line of git(root, ['log', '--first-parent', '--no-renames', '--diff-filter=A', '--name-only', '--format=%x01%H', '--', ...dirs]).out.split('\n')) {
            if (line.startsWith('\x01')) cur = line.slice(1); else if (line && cur) added.set(line, cur);
        }
    }
    for (const fr of all) {
        if (!tracked.has(fr.rel)) { fr.rank = Infinity; continue; }
        const sha = added.get(fr.rel);
        if (!sha || !rank.has(sha)) refuse(`${fr.rel} is committed but its add commit is not in this checkout's first-parent history`);
        fr.rank = rank.get(sha);
    }
    for (const p of pages) p.fresh.sort((a, b) => (a.rank === b.rank ? (a.name < b.name ? -1 : a.name > b.name ? 1 : 0) : a.rank < b.rank ? -1 : 1));
}

function numberAndExpand(p) {
    const numOf = new Map();
    let n = 0;
    if (p.numbered) {
        for (const t of [p.head, ...p.legacy.map((l) => l.text)]) for (const m of t.matchAll(/<h2\b[^>]*>\s*(\d+)\./g)) n = Math.max(n, Number(m[1]));
        for (const fr of p.fresh) { n += 1; fr.number = n; numOf.set(fr.base, n); }
    }
    for (const fr of p.fresh) {
        fr.expanded = p.numbered
            ? fr.text.replace(/<!--n-->/g, String(fr.number)).replace(/<!--ref:([^>\s]*?)-->/g, (m, name) => (numOf.has(name) ? String(numOf.get(name)) : m))
            : fr.text;
    }
}

// `source` is what the entry is written as in its file; `text` is what it renders as (tokens replaced).
const entriesOf = (p) => [
    ...p.legacy.map((l) => ({ text: l.text, source: l.text, fresh: false })),
    ...p.fresh.map((f) => ({ text: f.expanded, source: f.text, fresh: true })),
];
const renderPage = (p) => p.head + entriesOf(p).map((x) => x.text).join('') + p.tail;

function firstDiff(a, b) {
    const x = a.split('\n'), y = b.split('\n');
    let i = 0;
    while (i < x.length && i < y.length && x[i] === y[i]) i++;
    const clip = (s) => JSON.stringify((s === undefined ? '(end of page)' : s).slice(0, 70));
    return `line ${i + 1}: committed ${clip(x[i])} vs render ${clip(y[i])}`;
}

// The heading of an entry without its number, to tell "the same entry" from "another entry".
const headingKey = (entry) => {
    const h = /<h2\b[^>]*>([\s\S]*?)<\/h2>/.exec(entry);
    return h ? innerText(h[1]).replace(/^[\d\s]*\.\s*/, '') : null;
};

// How the committed page relates to the render of the fragments. A lagging page is the normal state between
// refreshes; "extras" is an entry appended by hand after the last rendered one; "differs" is an edit elsewhere.
// Where the page stops matching at entry j with entries still to come, what follows is an appended entry only if
// its heading is NOT entry j's: the same heading with other content is an EDIT of entry j (measured by the first
// run of this file's tests, which had called an edited entry "hand-appended" and let adopt write a bogus fragment).
// The one exception is a stacked PR's page that repeats a fragment already on develop under another number: that
// is the same entry, so it stays "extras" and adopt skips it as already a fragment.
function compareCommitted(p, committed) {
    const e = entriesOf(p);
    const differs = () => ({ state: 'differs', where: firstDiff(committed, renderPage(p)) });
    if (!committed.startsWith(p.head)) return differs();
    let pos = p.head.length, j = 0;
    while (j < e.length && committed.startsWith(e[j].text, pos)) { pos += e[j].text.length; j++; }
    const rest = committed.slice(pos);
    if (rest === p.tail) return { state: j === e.length ? 'current' : 'lagging', rendered: j, total: e.length };
    if (!(rest.endsWith(p.tail) && rest.length > p.tail.length)) return differs();
    const extra = rest.slice(0, rest.length - p.tail.length);
    if (j < e.length) {
        const first = (splitEntries(extra) || [extra])[0];
        if (headingKey(first) === headingKey(e[j].text)) {
            const L = (/<h2\b[^>]*>\s*(\d+)\./.exec(first) || [])[1];
            const sameFragment = e[j].fresh && (p.numbered && L ? tokenise(first, L) : first) === e[j].source;
            if (!sameFragment) return differs();
        }
    }
    return { state: 'extras', rendered: j, total: e.length, extra };
}

function committedText(o, p, ref) {
    if (ref) return git(o.root, ['show', `${ref}:${p.page}`]).out;
    const fp = path.join(o.root, p.page);
    if (!existsSync(fp)) { p.add(p.page, 'the committed page is missing'); return null; }
    return readText(fp);
}

// --- shared preparation: load, lint, order, number ----------------------------
function prepare(o) {
    const pages = Object.keys(PAGES).map((k) => loadPage(o.root, k));
    const flowBases = new Set(pages.find((p) => p.key === 'flow').fresh.map((f) => f.base));
    for (const p of pages) lintPage(p, flowBases);
    const findings = pages.flatMap((p) => p.findings);
    if (findings.length === 0) {
        orderFresh(o.root, pages);
        for (const p of pages) numberAndExpand(p);
    }
    return { pages, findings };
}

function runHtmlCheck(o, pages) {
    const exe = o.htmlCheck || path.join(o.root, 'systemTest/__tests__/support/html_docs_check.mjs');
    if (!existsSync(exe)) refuse(`html_docs_check.mjs not found at ${exe}`);
    const tmp = mkdtempSync(path.join(os.tmpdir(), 'docs-fragments-'));
    try {
        const files = pages.map((p) => { const f = path.join(tmp, path.basename(p.page)); writeFileSync(f, renderPage(p)); return f; });
        const r = spawnSync(process.execPath, [exe, ...files], { encoding: 'utf8' });
        if (r.status === 0) return [];
        const lines = `${r.stdout}${r.stderr}`.split('\n').filter(Boolean).map((l) => `render: ${l.split(tmp + '/').join('')}`);
        return lines.length ? lines : ['render: html_docs_check exited non-zero with no output'];
    } finally {
        rmSync(tmp, { recursive: true, force: true });
    }
}

const summary = (pages) => pages.map((p) => `${p.key} ${p.legacy.length} legacy + ${p.fresh.length} new`).join(', ');

// --- commands -----------------------------------------------------------------
function cmdCheck(o) {
    const { pages, findings } = prepare(o);
    if (findings.length) { findings.forEach((f) => console.log(f)); console.log(`FAIL — ${findings.length} finding(s) in the fragments`); return 1; }
    const render = runHtmlCheck(o, pages);
    if (render.length) { render.forEach((f) => console.log(f)); console.log(`FAIL — the rendered pages do not pass html_docs_check (${render.length} line(s))`); return 1; }
    const states = [];
    for (const p of pages) {
        const text = committedText(o, p, null);
        if (text === null) { p.findings.forEach((f) => console.log(f)); return 1; }
        const c = compareCommitted(p, text);
        states.push(c.state);
        if (c.state === 'current') console.log(`${p.key}: committed page is current (${c.total} of ${c.total} entries rendered)`);
        else if (c.state === 'lagging') console.log(`${p.key}: committed page is lagging, ${c.rendered} of ${c.total} entries rendered (the refresh step brings it current)`);
        else if (c.state === 'extras') console.log(`${p.key}: ADVISORY the committed page has content after its last rendered entry (hand-appended); run: node Blockchain/Dev/scripts/docs-fragments.mjs adopt`);
        else console.log(`${p.key}: ADVISORY the committed page differs from the render inside the rendered range, at ${c.where}; adopt cannot absorb an edit inside it, so it is a hand step`);
    }
    console.log(`docs-fragments: ${summary(pages)}; lint clean, render passes html_docs_check`);
    if (o.committed && states.some((s) => s !== 'current')) { console.log('FAIL — --committed needs both committed pages current; run the refresh step'); return 1; }
    console.log('OK');
    return 0;
}

function cmdBuild(o) {
    const { pages, findings } = prepare(o);
    if (findings.length) { findings.forEach((f) => console.log(f)); console.log(`FAIL — ${findings.length} finding(s) in the fragments`); return 1; }
    if (o.out) {
        mkdirSync(o.out, { recursive: true });
        for (const p of pages) {
            const fp = path.join(o.out, path.basename(p.page));
            writeFileSync(fp, renderPage(p));
            console.log(`${p.key}: wrote ${fp} (${p.legacy.length} legacy + ${p.fresh.length} new entries) sha256 ${sha256(renderPage(p))}`);
        }
        return 0;
    }
    if (!o.base) refuse('build needs --base <the develop sha you read with ls-remote>, or --out DIR for a preview');
    if (!/^[0-9a-f]{40}$/.test(o.base)) refuse('--base must be a full 40-hex sha');
    const anc = git(o.root, ['merge-base', '--is-ancestor', o.base, 'HEAD'], { allowFail: true });
    if (anc.status === 1) refuse(`--base ${o.base} is not an ancestor of HEAD: this checkout is on an old base; merge that develop in first`);
    if (anc.status !== 0) refuse(`--base ${o.base} cannot be resolved in this checkout`);
    const out = [];
    for (const p of pages) {
        const text = committedText(o, p, null);
        if (text === null) { p.findings.forEach((f) => console.log(f)); return 1; }
        const c = compareCommitted(p, text);
        // never destroy content: a hand-appended or hand-edited entry is absorbed by adopt first (or is a hand step)
        if (c.state === 'extras' || c.state === 'differs') {
            console.log(`${p.page}: FAIL the committed page has content the fragments do not (${c.state === 'extras' ? 'hand-appended after the last rendered entry: run adopt' : `an edit at ${c.where}: a hand step`}); build would overwrite it`);
            return 1;
        }
        out.push([p, text]);
    }
    for (const [p, text] of out) {
        const next = renderPage(p);
        if (next !== text) writeFileSync(path.join(o.root, p.page), next);
        console.log(`${p.key}: ${next === text ? 'unchanged' : 'rewritten'} ${p.page} (${p.legacy.length} legacy + ${p.fresh.length} new entries) sha256 ${sha256(next)}`);
    }
    return 0;
}

function cmdLegacyHash(o) {
    const pages = Object.keys(PAGES).map((k) => loadPage(o.root, k));
    const findings = pages.flatMap((p) => p.findings);
    if (findings.length) { findings.forEach((f) => console.log(f)); return 1; }
    for (const p of pages) console.log(`${p.key} ${sha256(p.head + p.legacy.map((l) => l.text).join('') + p.tail)}`);
    return 0;
}

// --- adopt --------------------------------------------------------------------
function splitEntries(text) {
    const lines = text.match(/[^\n]*\n|[^\n]+$/g) || [];
    const h2s = lines.map((l, i) => (l.startsWith('<h2') ? i : -1)).filter((i) => i >= 0);
    if (h2s.length === 0) return null;
    const starts = h2s.map((i, k) => {
        let j = i;
        while (j > (k ? h2s[k - 1] + 1 : 0) && LEAD_RE.test(lines[j - 1].replace(/\n$/, ''))) j--;
        return j;
    });
    if (starts[0] !== 0) return null;
    return starts.map((s, k) => lines.slice(s, k + 1 < starts.length ? starts[k + 1] : lines.length).join(''));
}

const ENTITIES = { amp: '&', lt: '<', gt: '>', quot: '"', apos: "'", rsquo: "'", lsquo: "'", mdash: '-', ndash: '-', hellip: '...', nbsp: ' ', rarr: '-', larr: '-' };
const decode = (s) => s.replace(/&#(\d+);|&([a-z]+);/gi, (m, d, n) => (d ? String.fromCodePoint(Number(d)) : ENTITIES[n.toLowerCase()] || ' '));

function fragmentName(entry) {
    const h2 = /<h2\b[^>]*>([\s\S]*?)<\/h2>/.exec(entry);
    const text = decode(innerText(h2 ? h2[1] : ''));
    const key = (/\b([A-Z]{2,4}-\d+)\b/.exec(text) || [])[1] || 'adopted';
    const slug = text.replace(/\b[A-Z]{2,4}-\d+\b/g, ' ').replace(/^\s*\d+\.\s*/, '').normalize('NFKD').replace(/[^\x00-\x7f]/g, '')
        .toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-+|-+$/g, '').slice(0, 56).replace(/-+$/, '') || 'entry';
    return `${key}-${slug}.html`;
}

function tokenise(entry, L) {
    return entry
        .replace(/(<h2\b[^>]*>\s*)(\d+)\./, (m, pre, num) => (num === String(L) ? `${pre}<!--n-->.` : m))
        .replace(/(<h3\b[^>]*>\s*)(\d+)\.(?=\d)/g, (m, pre, num) => (num === String(L) ? `${pre}<!--n-->.` : m));
}

// What a PR appended to a page since the PR's OWN base: the page at REF against the page at merge-base(REF, DEVELOP).
// The PR's page is stale (it was branched from an older develop), so comparing it with today's render would count
// every edit other PRs have made since as the PR's own; the merge-base page is the right yardstick. Anything the PR
// changed before its appended entries is not an append: a hand step (the first run of this against a real PR, #1837,
// was refused by the render comparison for exactly this reason).
function appendedBy(o, p) {
    const mb = git(o.root, ['merge-base', o.fromRef, o.against], { allowFail: true });
    if (mb.status !== 0) refuse(`no merge base between ${o.fromRef} and ${o.against}`);
    const baseText = git(o.root, ['show', `${mb.out.trim()}:${p.page}`]).out;
    const oldText = git(o.root, ['show', `${o.fromRef}:${p.page}`]).out;
    if (!baseText.endsWith(p.tail) || !oldText.endsWith(p.tail)) return { state: 'differs', where: 'a page that does not end with the fixed tail' };
    const stem = baseText.slice(0, baseText.length - p.tail.length);
    if (!oldText.startsWith(stem)) return { state: 'differs', where: firstDiff(oldText, baseText) };
    const extra = oldText.slice(stem.length, oldText.length - p.tail.length);
    return extra === '' ? { state: 'current' } : { state: 'extras', extra };
}

// An entry written with a literal number, put into token form, so two copies that differ only in the number are equal.
const normalise = (p, text) => (p.numbered ? tokenise(text, (/<h2\b[^>]*>\s*(\d+)\./.exec(text) || [])[1]) : text);

function cmdAdopt(o) {
    const { pages, findings } = prepare(o);
    if (findings.length) { findings.forEach((f) => console.log(f)); console.log('FAIL — fix the fragments first; adopt reads them'); return 1; }
    const plan = [];
    const problems = [];
    for (const p of pages) {
        let c;
        if (o.fromRef && o.against) c = appendedBy(o, p);
        else {
            const text = committedText(o, p, o.fromRef);
            if (text === null) { p.findings.forEach((f) => problems.push(f)); continue; }
            c = compareCommitted(p, text);
        }
        if (c.state === 'current' || c.state === 'lagging') { console.log(`${p.key}: nothing to adopt (the committed page holds no entry beyond the fragments)`); continue; }
        if (c.state === 'differs') { problems.push(`${p.page}: the page differs from the ${o.against ? 'PR\'s own base' : 'render inside the rendered range'}, at ${c.where}; adopt only absorbs entries appended after the last one, so this is a hand step`); continue; }
        const entries = splitEntries(c.extra);
        if (!entries) { problems.push(`${p.page}: the content added after the last entry does not start with an <h2> (it extends an existing entry, or the page ended differently when the PR branched); adopt cannot split it into entries, so this is a hand step`); continue; }
        for (const entry of entries) {
            const L = p.numbered ? (/<h2\b[^>]*>\s*(\d+)\./.exec(entry) || [])[1] : null;
            if (p.numbered && !L) { problems.push(`${p.page}: an appended entry has no leading section number in its <h2>`); continue; }
            const text2 = p.numbered ? tokenise(entry, L) : entry;
            const name = fragmentName(entry);
            const sameHeading = entriesOf(p).find((x) => headingKey(x.text) === headingKey(entry));
            if (sameHeading) {
                if (normalise(p, sameHeading.source) === normalise(p, entry)) console.log(`${p.key}: ${name} is already ${sameHeading.fresh ? 'a fragment' : 'in the legacy set'} (identical apart from its number); skipped`);
                else problems.push(`${p.rel}/${name}: an entry with that heading exists with different content; reconcile the two by hand`);
                continue;
            }
            if (p.fresh.some((f) => f.name === name)) { problems.push(`${p.rel}/${name}: a fragment of that name exists with different content; rename one of them`); continue; }
            const probe = { rel: `${p.rel}/${name}`, text: text2 };
            const before = p.findings.length;
            lintOne(p, probe, 'fresh', new Set([...p.fresh.map((f) => f.base), name.replace(/\.html$/, '')]));
            if (p.findings.length > before) { problems.push(...p.findings.splice(before)); continue; }
            plan.push({ p, name, text: text2, L, original: entry });
        }
    }
    if (problems.length) { problems.forEach((f) => console.log(f)); console.log(`FAIL — ${problems.length} problem(s); nothing was written`); return 1; }
    for (const a of plan) writeFileSync(path.join(a.p.dir, a.name), a.text);
    if (plan.length) {
        const re = prepare(o);
        for (const a of plan) {
            const fr = re.pages.find((x) => x.key === a.p.key).fresh.find((f) => f.name === a.name);
            const renders = a.p.numbered ? `renders as section ${fr.number}${String(fr.number) === a.L ? '' : ` (it was written as ${a.L})`}` : 'renders unnumbered';
            if (String(fr.number) === a.L && fr.expanded !== a.original) { console.log(`INTERNAL: ${a.name} does not re-expand to the appended text`); return 1; }
            console.log(`${a.p.key}: adopted ${a.p.rel}/${a.name}; ${renders}`);
        }
    }
    return 0;
}

// --- main -----------------------------------------------------------------------
function main() {
    const o = parseArgs(process.argv.slice(2));
    if (o.cmd === 'check') return cmdCheck(o);
    if (o.cmd === 'build') return cmdBuild(o);
    if (o.cmd === 'adopt') return cmdAdopt(o);
    if (o.cmd === 'legacy-hash') return cmdLegacyHash(o);
    return refuse('usage: docs-fragments.mjs check [--committed] | build --base <sha> | build --out DIR | adopt [--from-ref REF [--against SHA]] | legacy-hash   [--root DIR] [--html-check FILE]');
}

try {
    process.exitCode = main();
} catch (e) {
    if (!(e instanceof Refusal)) throw e;
    console.error(`docs-fragments: REFUSED — ${e.message}`);
    process.exitCode = 2;
}
