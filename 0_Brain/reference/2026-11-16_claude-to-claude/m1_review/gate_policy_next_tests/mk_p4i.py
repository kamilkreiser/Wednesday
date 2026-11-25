# QA-POLICY-NEXT: instrument a scratch copy of t26 (head) to count where the 200 000 cases go and compare old/new p3b/p4.
import sys
p=sys.argv[1]; s=open(p).read()
def rep(o,n):
    global s
    assert s.count(o)==1,(o,s.count(o)); s=s.replace(o,n)
rep('    let mut item_reach: BTreeMap<&\'static str, usize> = BTreeMap::new();\n',
    '    let mut item_reach: BTreeMap<&\'static str, usize> = BTreeMap::new();\n'
    '    let (mut q_total, mut q_b, mut q_reach, mut q_gen, mut q_corp, mut q_d3, mut q_d4, mut q_p3b, mut q_p4, mut q_corp_p4, mut q_corp_p3b) = (0usize,0usize,0usize,0usize,0usize,0usize,0usize,0usize,0usize,0usize,0usize);\n'
    '    { let mut fl: BTreeMap<String, usize> = BTreeMap::new(); let mut cw: BTreeMap<String, usize> = BTreeMap::new();\n'
    '      for it in &items { if let Some((c, f)) = &it.hook_raw { *fl.entry(format!("{f:?}")).or_default() += 1; *cw.entry(if c.is_empty() {"empty".into()} else if c.starts_with(\'/\') {"absolute".into()} else {format!("relative {c:?}")}).or_default() += 1; } }\n'
    '      eprintln!("QPX generated items {} corpus {}; sandbox flag values {fl:?}; cwd kinds {cw:?}", items.len()-corpus_len, corpus_len); }\n')
rep('        let d = decide_with_owner_allow(a, st, view, &it.facts, surface, NOW);\n',
    '        let d = decide_with_owner_allow(a, st, view, &it.facts, surface, NOW);\n        q_total += 1; if view.is_none() { q_b += 1; }\n')
rep('        // (k)\n',
    '        q_reach += 1; if it.hook_raw.is_some() { q_gen += 1; } else { q_corp += 1; if it.facts.cwd_not_absolute { q_corp_p4 += 1; } if it.facts.sandbox_flag_not_false { q_corp_p3b += 1; } }\n'
    '        if p3b != it.facts.sandbox_flag_not_false { q_d3 += 1; } if p4 != it.facts.cwd_not_absolute { q_d4 += 1; } if p3b { q_p3b += 1; } if p4 { q_p4 += 1; }\n'
    '        // (k)\n')
rep('    eprintln!("REACH owner allow: {owner_allows}");\n',
    '    eprintln!("REACH owner allow: {owner_allows}");\n'
    '    eprintln!("QPX cases {q_total}; left at (b) {q_b}; reached the predicates {q_reach} (generated {q_gen}, corpus {q_corp}); old/new differ p3b {q_d3} p4 {q_d4}; p3b true {q_p3b} p4 true {q_p4}; corpus cases with fixture p4 true {q_corp_p4} p3b true {q_corp_p3b}");\n')
open(p,'w').write(s)
