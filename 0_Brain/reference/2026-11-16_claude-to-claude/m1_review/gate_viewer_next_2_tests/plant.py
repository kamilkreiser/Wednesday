# usage: python3 -B plant.py <la_wrap.rs> <mode>   modes: extra | drop | mid | extra2
# Plants the viewer text `t` of la_fields_narrow only (right after `let t = v.text();`). Written for QA-VIEWER-NEXT-2.
import sys
path, mode = sys.argv[1], sys.argv[2]
s = open(path).read()
f = s.index("fn la_fields_narrow()")
anchor = "    let t = v.text();\n"
i = s.index(anchor, f)
assert s.count(anchor, f, f + 3000) == 1
code = {
 # one extra trailing entry: a copy of the last printed entry's rows
 "extra": '''    let mut t = v.text();
    {
        let last = printed_entries(&t).last().unwrap().join("\\n");
        t.push_str(&last);
        t.push('\\n');
    }
''',
 # two extra trailing entries
 "extra2": '''    let mut t = v.text();
    {
        let last = printed_entries(&t).last().unwrap().join("\\n");
        t.push_str(&last);
        t.push('\\n');
        t.push_str(&last);
        t.push('\\n');
    }
''',
 # the last printed entry dropped: text cut at its head row
 "drop": '''    let mut t = v.text();
    {
        let rows: Vec<&str> = t.lines().collect();
        let k = rows.iter().rposition(|r| entry_head(r)).unwrap();
        let cut = rows[..k].join("\\n") + "\\n";
        t = cut;
    }
''',
 # one extra entry in the MIDDLE: entry 5's rows repeated right after themselves
 "mid": '''    let mut t = v.text();
    {
        let rows: Vec<&str> = t.lines().collect();
        let heads: Vec<usize> = (0..rows.len()).filter(|&j| entry_head(rows[j])).collect();
        let (a, b) = (heads[5], heads[6]);
        let mut out: Vec<&str> = rows[..b].to_vec();
        out.extend_from_slice(&rows[a..b]);
        out.extend_from_slice(&rows[b..]);
        t = out.join("\\n") + "\\n";
    }
''',
}[mode]
s = s[:i] + code + s[i + len(anchor):]
open(path, "w").write(s)
print("planted", mode, path)
