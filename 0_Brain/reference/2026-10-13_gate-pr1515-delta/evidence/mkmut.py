import sys
MD = sys.argv[1]
P = open(MD + '/pristine.cjs', encoding='utf8').read()
MUT = {
 'L1a': ("  for (const e of SUFFIX[kind]) { out.push(rel + e); out.push(path.posix.join(rel, 'index' + e)); }", "  // variants removed"),
 'L2b': ("    if (c === '/' && d === '/') { const s0 = i; while (i < N && src[i] !== '\\n') i += 1; comments.push([s0, i]); continue; }",
         "    if (c === '/' && d === '/') { while (i < N && src[i] !== '\\n') i += 1; continue; }"),
 'X2': ("if (src[i] === '\\\\') { i += 2; continue; }", "if (src[i] === '\\\\') { i += 1; continue; }"),
 'X3': ("        if (src[i] === '\\n' && q !== '`') { i += 1; break; }\n", ""),
 'X6': ("      i = Math.min(i + 2, N); comments.push([s0, i]); continue;", "      i = Math.min(i + 2, N); continue;"),
}
for k, (o, n) in MUT.items():
    assert P.count(o) == 1, k
    open(f'{MD}/{k}.cjs', 'w', encoding='utf8').write(P.replace(o, n, 1))
    print(k, 'written')
